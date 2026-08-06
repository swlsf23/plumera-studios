/**
 * Catalog filter/sort enhancement only.
 *
 * SEO / delivery contract (do not break):
 * - The catalog URL is a full static HTML document (title, description, canonical
 *   are baked in at build time). This script must not mutate them.
 * - Result rows are plain <a href> links to other static HTML pages. No SPA/MPA
 *   client routing, fetch-and-replace, or intercepting navigation.
 * - history.replaceState may sync the filter query string on this same document;
 *   it must not change the document title or load a different page body.
 */
(() => {
  const form = document.querySelector("[data-catalog-controls]");
  const list = document.querySelector("[data-catalog-list]");
  const empty = document.querySelector("[data-catalog-empty]");
  const chipsEl = document.querySelector("[data-catalog-chips]");
  const countEl = document.querySelector("[data-catalog-count]");
  const enhanceEl = form?.querySelector("[data-catalog-enhance]");
  if (!form || !list) return;

  const qInput = form.querySelector("[data-catalog-q]");
  const levelSelect = form.querySelector("[data-catalog-level]");
  const typeInputs = [...form.querySelectorAll("[data-catalog-type]")];
  const sortSelect = form.querySelector("[data-catalog-sort]");
  const dateFromInput = form.querySelector("[data-catalog-date-from]");
  const dateToInput = form.querySelector("[data-catalog-date-to]");
  const dateClearBtn = form.querySelector("[data-catalog-date-clear]");
  const filtersDetails = form.querySelector("[data-catalog-filters]");
  const filtersBadge = form.querySelector("[data-catalog-filters-badge]");

  const INPUT_DEBOUNCE_MS = 150;
  let inputTimer = null;

  const LEVEL_RANK = { A1: 0, A2: 1, B1: 2, B2: 3, C1: 4, C2: 5 };
  const TYPE_RANK = {
    verb: 0,
    grammar: 1,
    conjugation: 2,
    vocabulary: 3,
    pronunciation: 4,
    guide: 5,
  };

  const VALID_SORTS = new Set([
    "date-desc",
    "date-asc",
    "level-asc",
    "level-desc",
    "type-asc",
    "type-desc",
  ]);

  const chipSearchTpl = form.dataset.chipSearch || "Search: {q}";
  const chipDateLabel = form.dataset.chipDate || "Date";
  const countAllTpl = form.dataset.countAll || "{n} lessons";
  const countFilteredTpl = form.dataset.countFiltered || "{n} matching lessons";

  function tokens(value) {
    return (value || "").trim().split(/\s+/).filter(Boolean);
  }

  function typeValues() {
    return typeInputs.map((input) => input.value);
  }

  function selectedType() {
    const checked = typeInputs.find((input) => input.checked);
    return checked ? checked.value : "";
  }

  function setType(value) {
    const match = typeInputs.find((input) => input.value === value) || typeInputs[0];
    if (match) match.checked = true;
  }

  function typeLabel(value) {
    if (!value) return "";
    const input = typeInputs.find((el) => el.value === value);
    const span = input?.closest("label")?.querySelector("span");
    return span?.textContent?.trim() || value;
  }

  function normalizeDateRange(dateFrom, dateTo) {
    if (dateFrom && dateTo && dateFrom > dateTo) {
      return { dateFrom: dateTo, dateTo: dateFrom, swapped: true };
    }
    return { dateFrom, dateTo, swapped: false };
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
    if (type && !typeValues().includes(type)) {
      type = "";
    }
    if (!VALID_SORTS.has(sort)) sort = "date-desc";

    const dates = normalizeDateRange(dateFrom, dateTo);
    return {
      q,
      level,
      type,
      sort,
      dateFrom: dates.dateFrom,
      dateTo: dates.dateTo,
    };
  }

  function writeControls(state) {
    if (qInput) qInput.value = state.q;
    if (levelSelect) levelSelect.value = state.level;
    setType(state.type);
    if (sortSelect) sortSelect.value = state.sort;
    if (dateFromInput) dateFromInput.value = state.dateFrom;
    if (dateToInput) dateToInput.value = state.dateTo;
  }

  function stateFromControls() {
    const dates = normalizeDateRange(
      dateFromInput ? dateFromInput.value : "",
      dateToInput ? dateToInput.value : "",
    );
    return {
      q: qInput ? qInput.value.trim() : "",
      level: levelSelect ? levelSelect.value : "",
      type: selectedType(),
      sort: sortSelect ? sortSelect.value : "date-desc",
      dateFrom: dates.dateFrom,
      dateTo: dates.dateTo,
      dateSwapped: dates.swapped,
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
    const dates = normalizeDateRange(from, to);
    from = dates.dateFrom;
    to = dates.dateTo;
    if (!from && !to) return true;
    if (!entryDate) return false;
    // One field only → that exact day (range needs both ends).
    if (from && !to) return entryDate === from;
    if (to && !from) return entryDate === to;
    if (entryDate < from) return false;
    if (entryDate > to) return false;
    return true;
  }

  function refreshDateLabels() {
    let prev = null;
    for (const item of list.querySelectorAll(".content-list__item")) {
      const label = item.querySelector(".content-list__date");
      if (!label) continue;
      if (item.hidden) {
        label.hidden = true;
        continue;
      }
      const d = item.dataset.date || "";
      const show = Boolean(d) && d !== prev;
      label.hidden = !show;
      if (d) prev = d;
    }
  }

  function normalizeQuery(q) {
    if (!q) return "";
    // Must match CatalogEntry.search_blob() / Python str.casefold().
    const fold = globalThis.PlumeraCaseFold;
    if (typeof fold !== "function") {
      throw new Error("PlumeraCaseFold is required for catalog search");
    }
    return fold(q);
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

  function hasActiveFilters(state) {
    return Boolean(state.q || state.level || state.type || state.dateFrom || state.dateTo);
  }

  function activeFilterCount(state) {
    let n = 0;
    if (state.q) n += 1;
    if (state.level) n += 1;
    if (state.type) n += 1;
    if (state.dateFrom || state.dateTo) n += 1;
    if (state.sort && state.sort !== "date-desc") n += 1;
    return n;
  }

  function syncFiltersPanel(state, { openIfActive = false } = {}) {
    const count = activeFilterCount(state);
    if (filtersBadge) {
      if (count > 0) {
        filtersBadge.hidden = false;
        filtersBadge.textContent = String(count);
      } else {
        filtersBadge.hidden = true;
        filtersBadge.textContent = "";
      }
    }
    if (openIfActive && filtersDetails && count > 0) {
      filtersDetails.open = true;
    }
  }

  function formatCount(template, n) {
    return template.replace(/\{n\}/g, String(n));
  }

  function dateChipText(state) {
    if (state.dateFrom && state.dateTo && state.dateFrom === state.dateTo) {
      return `${chipDateLabel}: ${state.dateFrom}`;
    }
    if (state.dateFrom && state.dateTo) {
      return `${chipDateLabel}: ${state.dateFrom} – ${state.dateTo}`;
    }
    if (state.dateFrom) return `${chipDateLabel}: ${state.dateFrom}`;
    if (state.dateTo) return `${chipDateLabel}: ${state.dateTo}`;
    return "";
  }

  function renderChips(state) {
    if (!chipsEl) return;
    const emptyChip = chipsEl.querySelector("[data-catalog-chips-empty]");
    const chips = [];
    if (state.q) {
      chips.push({ key: "q", label: chipSearchTpl.replace(/\{q\}/g, state.q) });
    }
    if (state.level) {
      chips.push({ key: "level", label: state.level });
    }
    if (state.type) {
      chips.push({ key: "type", label: typeLabel(state.type) });
    }
    const dateLabel = dateChipText(state);
    if (dateLabel) {
      chips.push({ key: "date", label: dateLabel });
    }

    // Keep the idle placeholder node; swap only the active filter chips.
    for (const node of [...chipsEl.children]) {
      if (node !== emptyChip) node.remove();
    }

    if (emptyChip) emptyChip.hidden = chips.length > 0;

    for (const chip of chips) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "catalog-chip";
      btn.dataset.clear = chip.key;
      btn.setAttribute("aria-label", `Clear ${chip.label}`);
      btn.innerHTML = `<span class="catalog-chip__label"></span><span class="catalog-chip__x" aria-hidden="true">×</span>`;
      btn.querySelector(".catalog-chip__label").textContent = chip.label;
      chipsEl.appendChild(btn);
    }
  }

  function renderCount(state, visible) {
    if (!countEl) return;
    const filtered = hasActiveFilters(state);
    const tpl = filtered ? countFilteredTpl : countAllTpl;
    countEl.textContent = formatCount(tpl, visible);
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
    refreshDateLabels();
    renderChips(state);
    renderCount(state, visible);
    syncFiltersPanel(state);

    if (empty) empty.hidden = visible !== 0;
  }

  let lastAppliedSig = null;

  function stateSignature(state) {
    return [
      state.q,
      state.level,
      state.type,
      state.sort,
      state.dateFrom,
      state.dateTo,
    ].join("\0");
  }

  function onChange() {
    const state = stateFromControls();
    // Keep inputs ordered when the user enters an inverted range.
    if (state.dateSwapped) {
      writeControls(state);
    }
    const sig = stateSignature(state);
    if (sig === lastAppliedSig) return;
    lastAppliedSig = sig;
    syncUrl(state);
    apply(state);
  }

  function onChangeImmediate() {
    if (inputTimer !== null) {
      clearTimeout(inputTimer);
      inputTimer = null;
    }
    onChange();
  }

  function onChangeDebounced() {
    if (inputTimer !== null) clearTimeout(inputTimer);
    inputTimer = setTimeout(() => {
      inputTimer = null;
      onChange();
    }, INPUT_DEBOUNCE_MS);
  }

  function clearFilter(key) {
    if (key === "q" && qInput) qInput.value = "";
    if (key === "level" && levelSelect) levelSelect.value = "";
    if (key === "type") setType("");
    if (key === "date") {
      if (dateFromInput) dateFromInput.value = "";
      if (dateToInput) dateToInput.value = "";
    }
    onChangeImmediate();
  }

  function bindDebouncedField(el) {
    if (!el) return;
    // Typing / stepwise date edits: debounce.
    el.addEventListener("input", onChangeDebounced);
    // Picker commit / blur: flush once (signature guard skips true dupes).
    el.addEventListener("change", onChangeImmediate);
  }

  // Progressive enhancement: reveal filters only when JS can drive them.
  if (enhanceEl) enhanceEl.hidden = false;
  form.setAttribute("data-catalog-ready", "");

  const initial = readState();
  writeControls(initial);
  syncFiltersPanel(initial, { openIfActive: true });
  apply(initial);
  lastAppliedSig = stateSignature(initial);

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    onChangeImmediate();
  });

  // Selects / radios: change only (no parallel input handler).
  if (levelSelect) levelSelect.addEventListener("change", onChangeImmediate);
  if (sortSelect) sortSelect.addEventListener("change", onChangeImmediate);
  for (const input of typeInputs) {
    input.addEventListener("change", onChangeImmediate);
  }

  bindDebouncedField(qInput);
  bindDebouncedField(dateFromInput);
  bindDebouncedField(dateToInput);

  if (dateClearBtn) {
    dateClearBtn.addEventListener("click", () => {
      if (dateFromInput) dateFromInput.value = "";
      if (dateToInput) dateToInput.value = "";
      onChangeImmediate();
      dateFromInput?.focus();
    });
  }

  if (chipsEl) {
    chipsEl.addEventListener("click", (event) => {
      const btn = event.target.closest("[data-clear]");
      if (!btn || !chipsEl.contains(btn)) return;
      clearFilter(btn.dataset.clear);
    });
  }
})();
