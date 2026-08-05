(() => {
  const form = document.querySelector("[data-catalog-controls]");
  const list = document.querySelector("[data-catalog-list]");
  const empty = document.querySelector("[data-catalog-empty]");
  if (!form || !list) return;

  const qInput = form.querySelector("[data-catalog-q]");
  const levelSelect = form.querySelector("[data-catalog-level]");
  const typeSelect = form.querySelector("[data-catalog-type]");
  const sortSelect = form.querySelector("[data-catalog-sort]");
  const dateFromInput = form.querySelector("[data-catalog-date-from]");
  const dateToInput = form.querySelector("[data-catalog-date-to]");

  const LEVEL_RANK = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };
  const TYPE_RANK = {
    verb: 0,
    grammar: 1,
    conjugation: 2,
    vocabulary: 3,
    pronunciation: 4,
  };

  const VALID_SORTS = new Set([
    "date-desc",
    "date-asc",
    "level-asc",
    "level-desc",
    "type-asc",
    "type-desc",
  ]);

  function tokens(value) {
    return (value || "").trim().split(/\s+/).filter(Boolean);
  }

  function readState() {
    const params = new URLSearchParams(window.location.search);
    let q = params.get("q") || "";
    let level = params.get("level") || "";
    let type = params.get("type") || "";
    let sort = params.get("sort") || "date-desc";
    let dateFrom = params.get("dateFrom") || params.get("date") || "";
    let dateTo = params.get("dateTo") || params.get("date") || "";

    if (level && levelSelect && ![...levelSelect.options].some((o) => o.value === level)) {
      level = "";
    }
    if (type && typeSelect && ![...typeSelect.options].some((o) => o.value === type)) {
      type = "";
    }
    if (!VALID_SORTS.has(sort)) sort = "date-desc";

    return { q, level, type, sort, dateFrom, dateTo };
  }

  function writeControls(state) {
    if (qInput) qInput.value = state.q;
    if (levelSelect) levelSelect.value = state.level;
    if (typeSelect) typeSelect.value = state.type;
    if (sortSelect) sortSelect.value = state.sort;
    if (dateFromInput) dateFromInput.value = state.dateFrom;
    if (dateToInput) dateToInput.value = state.dateTo;
  }

  function stateFromControls() {
    return {
      q: qInput ? qInput.value.trim() : "",
      level: levelSelect ? levelSelect.value : "",
      type: typeSelect ? typeSelect.value : "",
      sort: sortSelect ? sortSelect.value : "date-desc",
      dateFrom: dateFromInput ? dateFromInput.value : "",
      dateTo: dateToInput ? dateToInput.value : "",
    };
  }

  function syncUrl(state) {
    const params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.level) params.set("level", state.level);
    if (state.type) params.set("type", state.type);
    if (state.sort && state.sort !== "date-desc") params.set("sort", state.sort);
    if (state.dateFrom && state.dateFrom === state.dateTo) {
      params.set("date", state.dateFrom);
    } else {
      if (state.dateFrom) params.set("dateFrom", state.dateFrom);
      if (state.dateTo) params.set("dateTo", state.dateTo);
    }
    const qs = params.toString();
    const next = qs ? `${window.location.pathname}?${qs}` : window.location.pathname;
    window.history.replaceState(null, "", next);
  }

  function matchesDate(entryDate, from, to) {
    if (!from && !to) return true;
    if (!entryDate) return false;
    if (from && entryDate < from) return false;
    if (to && entryDate > to) return false;
    return true;
  }

  function normalizeQuery(q) {
    if (!q) return "";
    // caseFold is not on String; use toLocaleLowerCase for client match.
    // Server-emitted data-search is already casefold()'d in Python.
    return q.toLocaleLowerCase();
  }

  function compare(a, b, sort) {
    const [key, dir] = sort.split("-");
    let av;
    let bv;
    if (key === "date") {
      av = a.dataset.date || "";
      bv = b.dataset.date || "";
    } else if (key === "level") {
      av = LEVEL_RANK[a.dataset.primaryLevel] ?? 99;
      bv = LEVEL_RANK[b.dataset.primaryLevel] ?? 99;
    } else {
      av = TYPE_RANK[a.dataset.primaryType] ?? 99;
      bv = TYPE_RANK[b.dataset.primaryType] ?? 99;
    }
    if (av < bv) return dir === "asc" ? -1 : 1;
    if (av > bv) return dir === "asc" ? 1 : -1;
    const ta = a.querySelector(".content-list__title")?.textContent || "";
    const tb = b.querySelector(".content-list__title")?.textContent || "";
    return ta.localeCompare(tb);
  }

  function apply(state) {
    const qNorm = normalizeQuery(state.q);
    const items = [...list.querySelectorAll(".content-list__item")];
    let visible = 0;
    for (const item of items) {
      const levels = tokens(item.dataset.levels);
      const types = tokens(item.dataset.types);
      const levelOk = !state.level || levels.includes(state.level);
      const typeOk = !state.type || types.includes(state.type);
      const dateOk = matchesDate(item.dataset.date || "", state.dateFrom, state.dateTo);
      const qOk = !qNorm || (item.dataset.search || "").includes(qNorm);
      const show = levelOk && typeOk && dateOk && qOk;
      item.hidden = !show;
      if (show) visible += 1;
    }

    const shown = items.filter((item) => !item.hidden);
    shown.sort((a, b) => compare(a, b, state.sort));
    for (const item of shown) list.appendChild(item);

    if (empty) empty.hidden = visible !== 0;
  }

  function onChange() {
    const state = stateFromControls();
    syncUrl(state);
    apply(state);
  }

  const initial = readState();
  writeControls(initial);
  apply(initial);

  form.addEventListener("change", onChange);
  form.addEventListener("input", onChange);
})();
