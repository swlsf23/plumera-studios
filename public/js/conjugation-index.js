/**
 * Conjugation hub — search/filter list + A–Z browse section.
 *
 * verbs.json fills both lists. Search filters persist in sessionStorage so
 * hub/verb URLs stay clean. Letter browse state is stored separately.
 */
(() => {
  const root = document.querySelector("[data-conjugation-hub]");
  if (!root) return;

  const indexUrl = root.dataset.conjugationIndexUrl;
  if (!indexUrl) return;

  const indexPath = indexUrl.split("?")[0];
  // v2: reset pre-hub session filters that could hide pronominals (e.g. construction=simple).
  const FILTER_KEY = `plumera:conjugation:filters:v2:${indexPath}`;
  const AZ_KEY = `plumera:conjugation:az:${indexPath}`;

  const form = root.querySelector("[data-conjugation-controls]");
  const enhanceEl = form?.querySelector("[data-conjugation-enhance]");
  const qInput = form?.querySelector("[data-conjugation-q]");
  const levelSelect = form?.querySelector("[data-conjugation-level]");
  const classSelect = form?.querySelector("[data-conjugation-class]");
  const constructionSelect = form?.querySelector(
    "[data-conjugation-construction]",
  );
  const resultsEl = form?.querySelector("[data-conjugation-results]");
  const emptyEl = form?.querySelector("[data-conjugation-empty]");
  const countEl = form?.querySelector("[data-conjugation-count]");

  const azSection = root.querySelector("[data-conjugation-az]");
  const azNav = root.querySelector("[data-conjugation-az-nav]");
  const azListEl = root.querySelector("[data-conjugation-az-list]");
  const azResultsEl = root.querySelector("[data-conjugation-az-results]");
  const azEmptyEl = root.querySelector("[data-conjugation-az-empty]");
  const azCountEl = root.querySelector("[data-conjugation-az-count]");
  const azButtons = azNav
    ? [...azNav.querySelectorAll("[data-conjugation-az-letter]")]
    : [];

  const INPUT_DEBOUNCE_MS = 120;
  let inputTimer = null;
  let verbs = [];
  let activeIndex = -1;
  let selectedLetter = "";

  const emptyMsg = root.dataset.empty || "No verbs match.";
  const azEmptyMsg = root.dataset.azEmpty || "No verbs for this letter.";

  function fold(text) {
    const fn = globalThis.PlumeraCaseFold;
    if (typeof fn !== "function") {
      throw new Error("PlumeraCaseFold is required for conjugation search");
    }
    return fn(text || "");
  }

  /** First A–Z letter of a lemma (accents stripped); "" if none. */
  function lemmaLetter(lemma) {
    const folded = fold(lemma);
    // Strip combining marks after NFD so être → e.
    const base = folded.normalize("NFD").replace(/\p{M}/gu, "");
    const ch = base.charAt(0);
    if (ch >= "a" && ch <= "z") return ch;
    return "";
  }

  function emptyFilterState() {
    return { q: "", level: "", class: "", construction: "" };
  }

  function stateFromControls() {
    return {
      q: qInput ? qInput.value.trim() : "",
      level: levelSelect ? levelSelect.value : "",
      class: classSelect ? classSelect.value : "",
      construction: constructionSelect ? constructionSelect.value : "",
    };
  }

  function readStoredFilters() {
    try {
      const raw = sessionStorage.getItem(FILTER_KEY);
      if (!raw) return emptyFilterState();
      const parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== "object") return emptyFilterState();
      return {
        q: typeof parsed.q === "string" ? parsed.q : "",
        level: typeof parsed.level === "string" ? parsed.level : "",
        class: typeof parsed.class === "string" ? parsed.class : "",
        construction:
          typeof parsed.construction === "string" ? parsed.construction : "",
      };
    } catch {
      return emptyFilterState();
    }
  }

  function writeStoredFilters(state) {
    try {
      sessionStorage.setItem(FILTER_KEY, JSON.stringify(state));
    } catch {
      /* ignore */
    }
  }

  function readStoredLetter() {
    try {
      const raw = sessionStorage.getItem(AZ_KEY);
      if (!raw) return "";
      const letter = String(raw).toLowerCase();
      return letter.length === 1 && letter >= "a" && letter <= "z" ? letter : "";
    } catch {
      return "";
    }
  }

  function writeStoredLetter(letter) {
    try {
      if (letter) sessionStorage.setItem(AZ_KEY, letter);
      else sessionStorage.removeItem(AZ_KEY);
    } catch {
      /* ignore */
    }
  }

  function sanitizeState(state) {
    const next = { ...state };
    const check = (select, key) => {
      if (!select || !next[key]) return;
      const ok = [...select.options].some((o) => o.value === next[key]);
      if (!ok) next[key] = "";
    };
    check(levelSelect, "level");
    check(classSelect, "class");
    check(constructionSelect, "construction");
    return next;
  }

  function readLegacyQueryState() {
    const params = new URLSearchParams(window.location.search);
    const next = emptyFilterState();
    let any = false;
    for (const key of ["q", "level", "class", "construction"]) {
      if (!params.has(key)) continue;
      next[key] = params.get(key) || "";
      any = true;
    }
    return any ? next : null;
  }

  function clearFilterQueryFromUrl() {
    if (!window.location.search) return;
    const params = new URLSearchParams(window.location.search);
    let dirty = false;
    for (const key of ["q", "level", "class", "construction", "letter"]) {
      if (params.has(key)) {
        params.delete(key);
        dirty = true;
      }
    }
    if (!dirty) return;
    const qs = params.toString();
    const next = qs
      ? `${window.location.pathname}?${qs}`
      : window.location.pathname;
    window.history.replaceState(null, "", next);
  }

  function readFilterState() {
    const legacy = readLegacyQueryState();
    const next = legacy
      ? { ...readStoredFilters(), ...legacy }
      : readStoredFilters();
    return sanitizeState(next);
  }

  function writeControls(state) {
    if (qInput) qInput.value = state.q;
    if (levelSelect) levelSelect.value = state.level;
    if (classSelect) classSelect.value = state.class;
    if (constructionSelect) constructionSelect.value = state.construction;
  }

  function cleanHref(href) {
    return (href || "").split("#")[0].split("?")[0];
  }

  function matchVerbs(state) {
    const q = fold(state.q);
    const tokens = q.split(/\s+/).filter(Boolean);

    const matched = verbs.filter((verb) => {
      const hay = verb.search || "";
      if (tokens.length && !tokens.every((t) => hay.includes(t))) return false;
      if (state.level && verb.cefr !== state.level) return false;
      if (state.class && verb.class !== state.class) return false;
      if (state.construction && verb.construction !== state.construction) {
        return false;
      }
      return true;
    });

    if (!tokens.length) return matched;

    const score = (verb) => {
      const lemma = fold(verb.lemma || "");
      if (lemma === q) return 300;
      if (lemma.startsWith(q)) return 200;
      if (tokens.length > 1 && tokens.every((t) => lemma.includes(t))) return 150;
      if (lemma.includes(q)) return 100;
      return 0;
    };

    return matched.slice().sort((a, b) => {
      const d = score(b) - score(a);
      if (d) return d;
      return fold(a.lemma).localeCompare(fold(b.lemma));
    });
  }

  function go(href) {
    if (!href) return;
    writeStoredFilters(stateFromControls());
    writeStoredLetter(selectedLetter);
    window.location.href = cleanHref(href);
  }

  function makeLemmaLink(verb, { activeClass = false } = {}) {
    const li = document.createElement("li");
    const link = document.createElement("a");
    link.className = activeClass ? "lemma-item lemma-item--active" : "lemma-item";
    link.href = cleanHref(verb.href);
    link.textContent = verb.lemma;
    link.addEventListener("click", (event) => {
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey
      ) {
        return;
      }
      event.preventDefault();
      go(link.getAttribute("href"));
    });
    li.appendChild(link);
    return li;
  }

  function makeBrowseItem(verb) {
    const li = document.createElement("li");
    li.className = "content-list__item";
    const row = document.createElement("div");
    row.className = "content-list__row";
    const link = document.createElement("a");
    link.className = "content-list__link";
    link.href = cleanHref(verb.href);
    const title = document.createElement("span");
    title.className = "content-list__title";
    const lemma = verb.lemma || "";
    const level = verb.cefr || "";
    title.textContent = level ? `${lemma} · ${level}` : lemma;
    link.appendChild(title);
    link.addEventListener("click", (event) => {
      if (
        event.defaultPrevented ||
        event.button !== 0 ||
        event.metaKey ||
        event.ctrlKey ||
        event.shiftKey ||
        event.altKey
      ) {
        return;
      }
      event.preventDefault();
      go(link.getAttribute("href"));
    });
    row.appendChild(link);
    li.appendChild(row);
    return li;
  }

  function setLemmaListRows(count) {
    if (!resultsEl) return;
    const min = 3;
    const max = 5;
    const shown =
      count <= 0 ? min : Math.min(max, Math.max(min, count));
    // Fewer than min results: shrink toward the count (floor at 2).
    const rows =
      count > 0 && count < min ? Math.max(2, count) : shown;
    resultsEl.style.setProperty("--conjugation-lemma-shown", String(rows));
  }

  function renderFilterList(state) {
    if (!resultsEl) return;

    const matched = matchVerbs(state);
    resultsEl.replaceChildren();
    activeIndex = -1;

    if (countEl) countEl.textContent = String(matched.length);

    if (matched.length === 0) {
      resultsEl.hidden = true;
      setLemmaListRows(0);
      if (emptyEl) {
        emptyEl.hidden = false;
        emptyEl.textContent = emptyMsg;
      }
      return;
    }

    if (emptyEl) {
      emptyEl.hidden = true;
      emptyEl.textContent = "";
    }

    for (const verb of matched) {
      resultsEl.appendChild(makeLemmaLink(verb));
    }
    setLemmaListRows(matched.length);
    resultsEl.hidden = false;
  }

  function runFromControls() {
    const state = stateFromControls();
    writeStoredFilters(state);
    renderFilterList(state);
  }

  function moveActive(delta) {
    if (!resultsEl || resultsEl.hidden) return;
    const options = [...resultsEl.querySelectorAll(".lemma-item")];
    if (!options.length) return;
    activeIndex = (activeIndex + delta + options.length) % options.length;
    options.forEach((el, i) => {
      el.classList.toggle("lemma-item--active", i === activeIndex);
    });
    options[activeIndex].scrollIntoView({ block: "nearest" });
  }

  function lettersPresent() {
    const set = new Set();
    for (const verb of verbs) {
      const letter = lemmaLetter(verb.lemma);
      if (letter) set.add(letter);
    }
    return set;
  }

  function syncAzButtons(present) {
    for (const btn of azButtons) {
      const letter = (btn.dataset.conjugationAzLetter || "").toLowerCase();
      const ok = present.has(letter);
      btn.hidden = !ok;
      btn.disabled = !ok;
      btn.setAttribute("aria-pressed", letter === selectedLetter ? "true" : "false");
      btn.classList.toggle("is-active", letter === selectedLetter && ok);
    }
  }

  function renderAzList() {
    if (!azResultsEl) return;

    const matched = selectedLetter
      ? verbs.filter((verb) => lemmaLetter(verb.lemma) === selectedLetter)
      : [];

    azResultsEl.replaceChildren();

    if (azCountEl) {
      if (selectedLetter) {
        azCountEl.hidden = false;
        azCountEl.textContent = String(matched.length);
      } else {
        azCountEl.hidden = true;
        azCountEl.textContent = "";
      }
    }

    if (!selectedLetter || matched.length === 0) {
      if (azListEl) azListEl.hidden = true;
      azResultsEl.replaceChildren();
      if (azEmptyEl) {
        const show = Boolean(selectedLetter);
        azEmptyEl.hidden = !show;
        azEmptyEl.textContent = show ? azEmptyMsg : "";
      }
      return;
    }

    if (azEmptyEl) {
      azEmptyEl.hidden = true;
      azEmptyEl.textContent = "";
    }

    for (const verb of matched) {
      azResultsEl.appendChild(makeBrowseItem(verb));
    }
    if (azListEl) azListEl.hidden = false;
  }

  function setLetter(letter) {
    const next = (letter || "").toLowerCase();
    if (next && (next < "a" || next > "z")) return;
    selectedLetter = next;
    writeStoredLetter(selectedLetter);
    syncAzButtons(lettersPresent());
    renderAzList();
  }

  function defaultLetter(present) {
    const stored = readStoredLetter();
    if (stored && present.has(stored)) return stored;
    for (let i = 0; i < 26; i += 1) {
      const letter = String.fromCharCode(97 + i);
      if (present.has(letter)) return letter;
    }
    return "";
  }

  async function init() {
    const response = await fetch(indexUrl, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error(`Failed to load conjugation index (${response.status})`);
    }
    const payload = await response.json();
    verbs = Array.isArray(payload.verbs) ? payload.verbs : [];

    if (enhanceEl) enhanceEl.hidden = false;
    if (azSection) azSection.hidden = false;

    clearFilterQueryFromUrl();
    const initial = readFilterState();
    writeControls(initial);
    writeStoredFilters(initial);
    renderFilterList(initial);

    const present = lettersPresent();
    selectedLetter = defaultLetter(present);
    writeStoredLetter(selectedLetter);
    syncAzButtons(present);
    renderAzList();

    if (form) {
      form.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!resultsEl || resultsEl.hidden) return;
        const options = [...resultsEl.querySelectorAll(".lemma-item")];
        const chosen =
          (activeIndex >= 0 && options[activeIndex]) || options[0];
        if (chosen) go(chosen.getAttribute("href") || chosen.dataset.href);
      });

      form.addEventListener("change", runFromControls);

      if (qInput) {
        qInput.addEventListener("input", () => {
          clearTimeout(inputTimer);
          inputTimer = setTimeout(runFromControls, INPUT_DEBOUNCE_MS);
        });
        qInput.addEventListener("keydown", (event) => {
          if (event.key === "ArrowDown") {
            event.preventDefault();
            moveActive(1);
          } else if (event.key === "ArrowUp") {
            event.preventDefault();
            moveActive(-1);
          } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            const options = [...resultsEl.querySelectorAll(".lemma-item")];
            if (options[activeIndex]) {
              go(options[activeIndex].getAttribute("href"));
            }
          }
        });
      }
    }

    if (azNav) {
      azNav.addEventListener("click", (event) => {
        const btn = event.target.closest("[data-conjugation-az-letter]");
        if (!btn || btn.disabled || !azNav.contains(btn)) return;
        setLetter(btn.dataset.conjugationAzLetter || "");
      });
    }
  }

  init().catch((err) => {
    console.error(err);
  });
})();
