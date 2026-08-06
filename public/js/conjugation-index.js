/**
 * Conjugation verb browser — layout matches corpus-generation/viewer Sidebar.
 *
 * verbs.json fills the left lemma list. Filters narrow it. Click navigates to
 * that verb's static HTML page; filter state persists via sessionStorage + query
 * (lemma links carry the query so middle-click / open-in-new-tab keep filters).
 */
(() => {
  const form = document.querySelector("[data-conjugation-controls]");
  if (!form) return;

  const indexUrl = form.dataset.conjugationIndexUrl;
  if (!indexUrl) return;

  const STORAGE_KEY = `plumera:conjugation:filters:${indexUrl}`;
  // …/conjugation/verbs.json → …/conjugation/
  const hubPath = indexUrl.replace(/\/verbs\.json$/, "/");

  const enhanceEl = form.querySelector("[data-conjugation-enhance]");
  const qInput = form.querySelector("[data-conjugation-q]");
  const levelSelect = form.querySelector("[data-conjugation-level]");
  const classSelect = form.querySelector("[data-conjugation-class]");
  const constructionSelect = form.querySelector("[data-conjugation-construction]");
  const resultsEl = form.querySelector("[data-conjugation-results]");
  const emptyEl = form.querySelector("[data-conjugation-empty]");
  const countEl = form.querySelector("[data-conjugation-count]");

  const INPUT_DEBOUNCE_MS = 120;
  let inputTimer = null;
  let verbs = [];
  let activeIndex = -1;

  const emptyMsg = form.dataset.empty || "No verbs match.";
  const collapseLabel = form.dataset.collapseLabel || "Collapse verb list";
  const expandLabel = form.dataset.expandLabel || "Expand verb list";
  const currentSlug = form.dataset.conjugationCurrent || "";
  const SIDEBAR_KEY = "plumera:conjugation:sidebar-collapsed";
  const shell = document.querySelector(".conjugation-shell");
  const toggleBtn = form.querySelector("[data-conjugation-sidebar-toggle]");

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

  function readState() {
    // sessionStorage is the baseline; URL params overlay (so verb links and
    // shared URLs win per-key without wiping other stored filters).
    const next = readStoredState();
    const params = new URLSearchParams(window.location.search);
    for (const key of ["q", "level", "class", "construction"]) {
      if (params.has(key)) next[key] = params.get(key) || "";
    }
    return sanitizeState(next);
  }

  function writeControls(state) {
    if (qInput) qInput.value = state.q;
    if (levelSelect) levelSelect.value = state.level;
    if (classSelect) classSelect.value = state.class;
    if (constructionSelect) constructionSelect.value = state.construction;
  }

  function queryString(state) {
    const params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.level) params.set("level", state.level);
    if (state.class) params.set("class", state.class);
    if (state.construction) params.set("construction", state.construction);
    return params.toString();
  }

  function syncUrl(state) {
    const qs = queryString(state);
    const next = qs
      ? `${window.location.pathname}?${qs}`
      : window.location.pathname;
    window.history.replaceState(null, "", next);
  }

  function syncHubNavLinks(state) {
    const qs = queryString(state);
    const hubWithQs = qs ? `${hubPath}?${qs}` : hubPath;
    const hubNorm = hubPath.replace(/\/$/, "") || "/";
    for (const a of document.querySelectorAll("a[href]")) {
      let path;
      try {
        path = new URL(a.href, window.location.origin).pathname;
      } catch {
        continue;
      }
      const pathNorm = path.replace(/\/$/, "") || "/";
      if (pathNorm !== hubNorm) continue;
      a.setAttribute("href", hubWithQs);
    }
  }

  function persist(state) {
    writeStoredState(state);
    syncUrl(state);
    syncHubNavLinks(state);
  }

  function hrefWithState(href, state) {
    const qs = queryString(state);
    const base = href.split("#")[0].split("?")[0];
    return qs ? `${base}?${qs}` : base;
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

  function setSidebarCollapsed(collapsed) {
    if (!shell) return;
    shell.classList.toggle("conjugation-shell--sidebar-collapsed", collapsed);
    if (toggleBtn) {
      toggleBtn.setAttribute("aria-expanded", collapsed ? "false" : "true");
      const label = collapsed ? expandLabel : collapseLabel;
      toggleBtn.setAttribute("aria-label", label);
      toggleBtn.title = label;
      toggleBtn.textContent = collapsed ? "›" : "‹";
    }
    try {
      sessionStorage.setItem(SIDEBAR_KEY, collapsed ? "1" : "0");
    } catch {
      /* ignore */
    }
  }

  function go(href) {
    if (!href) return;
    const state = stateFromControls();
    persist(state);
    window.location.href = hrefWithState(href, state);
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
      link.href = hrefWithState(verb.href, state);
      link.textContent = verb.lemma;
      if (verb.slug === currentSlug) {
        link.setAttribute("aria-current", "page");
        currentEl = link;
      }
      // Keep sessionStorage warm even when the browser follows href directly
      // (middle-click / open in new tab still carries filters via the query).
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
        persist(stateFromControls());
      });
      li.appendChild(link);
      resultsEl.appendChild(li);
    }

    resultsEl.hidden = false;
    if (currentEl) currentEl.scrollIntoView({ block: "nearest" });
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

  // Restore controls immediately so filters are visible before verbs.json loads.
  // Always open the rail on load — a collapsed leftover from the old fixed layout
  // looked like a cut-off box with no selector.
  setSidebarCollapsed(false);
  const bootState = readState();
  writeControls(bootState);
  syncHubNavLinks(bootState);

  async function init() {
    const response = await fetch(indexUrl, { credentials: "same-origin" });
    if (!response.ok) {
      throw new Error(`Failed to load conjugation index (${response.status})`);
    }
    const payload = await response.json();
    verbs = Array.isArray(payload.verbs) ? payload.verbs : [];

    if (enhanceEl) enhanceEl.hidden = false;

    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const collapsed = !shell?.classList.contains(
          "conjugation-shell--sidebar-collapsed",
        );
        setSidebarCollapsed(collapsed);
      });
    }

    const initial = readState();
    writeControls(initial);
    persist(initial);
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
