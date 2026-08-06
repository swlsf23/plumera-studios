/**
 * Conjugation verb browser — overlay drawer inside the content column.
 *
 * verbs.json fills the lemma list. Filters narrow it. Click navigates to that
 * verb's static HTML page; filter state persists in sessionStorage only so
 * verb URLs stay clean (no ?class=&construction= clutter).
 * The drawer covers the tables only — it must not widen the page shell.
 */
(() => {
  const form = document.querySelector("[data-conjugation-controls]");
  if (!form) return;

  const indexUrl = form.dataset.conjugationIndexUrl;
  if (!indexUrl) return;

  const indexPath = indexUrl.split("?")[0];
  const STORAGE_KEY = `plumera:conjugation:filters:${indexPath}`;

  const drawer = document.querySelector("[data-conjugation-drawer]");
  const openBtns = [
    ...document.querySelectorAll("[data-conjugation-drawer-open]"),
  ];
  const closeBtns = [
    ...document.querySelectorAll("[data-conjugation-drawer-close]"),
  ];

  const enhanceEl = form.querySelector("[data-conjugation-enhance]");
  const qInput = form.querySelector("[data-conjugation-q]");
  const levelSelect = form.querySelector("[data-conjugation-level]");
  const classSelect = form.querySelector("[data-conjugation-class]");
  const constructionSelect = form.querySelector(
    "[data-conjugation-construction]",
  );
  const resultsEl = form.querySelector("[data-conjugation-results]");
  const emptyEl = form.querySelector("[data-conjugation-empty]");
  const countEl = form.querySelector("[data-conjugation-count]");

  const INPUT_DEBOUNCE_MS = 120;
  let inputTimer = null;
  let verbs = [];
  let activeIndex = -1;
  let lastFocus = null;

  const emptyMsg = form.dataset.empty || "No verbs match.";
  const currentSlug = form.dataset.conjugationCurrent || "";

  function fold(text) {
    const fn = globalThis.PlumeraCaseFold;
    if (typeof fn !== "function") {
      throw new Error("PlumeraCaseFold is required for conjugation search");
    }
    return fn(text || "");
  }

  function emptyState() {
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

  function readStoredState() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return emptyState();
      const parsed = JSON.parse(raw);
      if (!parsed || typeof parsed !== "object") return emptyState();
      return {
        q: typeof parsed.q === "string" ? parsed.q : "",
        level: typeof parsed.level === "string" ? parsed.level : "",
        class: typeof parsed.class === "string" ? parsed.class : "",
        construction:
          typeof parsed.construction === "string" ? parsed.construction : "",
      };
    } catch {
      return emptyState();
    }
  }

  function writeStoredState(state) {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state));
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
    const next = emptyState();
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
    for (const key of ["q", "level", "class", "construction"]) {
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

  function readState() {
    const legacy = readLegacyQueryState();
    const next = legacy
      ? { ...readStoredState(), ...legacy }
      : readStoredState();
    return sanitizeState(next);
  }

  function writeControls(state) {
    if (qInput) qInput.value = state.q;
    if (levelSelect) levelSelect.value = state.level;
    if (classSelect) classSelect.value = state.class;
    if (constructionSelect) constructionSelect.value = state.construction;
  }

  function persist(state) {
    writeStoredState(state);
  }

  function cleanHref(href) {
    return (href || "").split("#")[0].split("?")[0];
  }

  function matchVerbs(state) {
    const q = fold(state.q);
    return verbs.filter((verb) => {
      if (q && !(verb.search || "").includes(q)) return false;
      if (state.level && verb.cefr !== state.level) return false;
      if (state.class && verb.class !== state.class) return false;
      if (state.construction && verb.construction !== state.construction) {
        return false;
      }
      return true;
    });
  }
  function isOpen() {
    return Boolean(drawer && !drawer.hidden);
  }

  function setOpen(open) {
    if (!drawer) return;
    drawer.hidden = !open;
    drawer.classList.toggle("is-open", open);
    for (const btn of openBtns) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    document.documentElement.classList.toggle(
      "conjugation-drawer-open",
      open,
    );
    if (open) {
      lastFocus = document.activeElement;
      const focusTarget = qInput || form.querySelector("button, input, select");
      if (focusTarget) focusTarget.focus();
    } else if (lastFocus && typeof lastFocus.focus === "function") {
      lastFocus.focus();
      lastFocus = null;
    }
  }

  function go(href) {
    if (!href) return;
    persist(stateFromControls());
    window.location.href = cleanHref(href);
  }

  function renderList(state) {
    if (!resultsEl) return;

    const matched = matchVerbs(state);
    resultsEl.replaceChildren();
    activeIndex = -1;

    if (countEl) countEl.textContent = String(matched.length);

    if (matched.length === 0) {
      resultsEl.hidden = true;
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

    let currentEl = null;
    for (const verb of matched) {
      const li = document.createElement("li");
      const link = document.createElement("a");
      link.className =
        verb.slug === currentSlug
          ? "lemma-item lemma-item--selected"
          : "lemma-item";
      link.href = cleanHref(verb.href);
      link.textContent = verb.lemma;
      if (verb.slug === currentSlug) {
        link.setAttribute("aria-current", "page");
        currentEl = link;
      }
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
      resultsEl.appendChild(li);
    }

    resultsEl.hidden = false;
    if (currentEl && isOpen()) currentEl.scrollIntoView({ block: "nearest" });
  }

  function runFromControls() {
    const state = stateFromControls();
    persist(state);
    renderList(state);
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

  const bootState = readState();
  writeControls(bootState);
  writeStoredState(bootState);
  clearFilterQueryFromUrl();

  async function init() {
    const response = await fetch(indexUrl, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error(`Failed to load conjugation index (${response.status})`);
    }
    const payload = await response.json();
    verbs = Array.isArray(payload.verbs) ? payload.verbs : [];

    if (enhanceEl) enhanceEl.hidden = false;

    for (const btn of openBtns) {
      btn.addEventListener("click", () => setOpen(!isOpen()));
    }
    for (const btn of closeBtns) {
      btn.addEventListener("click", () => setOpen(false));
    }
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && isOpen()) {
        event.preventDefault();
        setOpen(false);
      }
    });

    const initial = readState();
    writeControls(initial);
    persist(initial);
    clearFilterQueryFromUrl();
    renderList(initial);

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (!resultsEl || resultsEl.hidden) return;
      const options = [...resultsEl.querySelectorAll(".lemma-item")];
      const chosen =
        (activeIndex >= 0 && options[activeIndex]) ||
        options.find((el) => el.classList.contains("lemma-item--selected")) ||
        options[0];
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

  init().catch((err) => {
    console.error(err);
  });
})();
