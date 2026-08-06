/**
 * Conjugation paradigm UI: mood filter + active/passive voice tabs.
 * Tables are already in the static HTML; this only toggles visibility.
 * Voice + last mood persist across verb pages via sessionStorage.
 */
(() => {
  const root = document.querySelector(".conjugation");
  if (!root) return;

  const VOICE_KEY = "plumera:conjugation:voice";
  const MOOD_KEY = "plumera:conjugation:mood";
  const DEFAULT_MOOD = "mood-indicatif";

  const activePanel = root.querySelector(
    '.conjugation-voice-panel[data-voice="active"]',
  );
  const passivePanel = root.querySelector(
    '.conjugation-voice-panel[data-voice="passive"]',
  );
  const tabs = [...document.querySelectorAll(".voice-tab[data-voice]")];
  const moodLinks = [...document.querySelectorAll(".mood-nav-link[href^='#']")];
  const moodSections = [...root.querySelectorAll(".mood-section")];

  function passiveHasContent(panel) {
    if (!panel) return false;
    if (panel.hasAttribute("hidden") && !panel.querySelector(".mood-section")) {
      return false;
    }
    return Boolean(panel.querySelector(".mood-section"));
  }

  const hasPassive = passiveHasContent(passivePanel);

  if (!hasPassive) {
    const passiveTab = tabs.find((tab) => tab.dataset.voice === "passive");
    if (passiveTab) passiveTab.hidden = true;
    const tablist = document.querySelector(".voice-tabs");
    if (tablist && tabs.every((tab) => tab.hidden || tab.dataset.voice === "active")) {
      const visible = tabs.filter((tab) => !tab.hidden);
      if (visible.length <= 1) tablist.hidden = true;
    }
    if (passivePanel) {
      passivePanel.hidden = true;
      passivePanel.setAttribute("hidden", "");
    }
  }

  function readStoredVoice() {
    try {
      const v = sessionStorage.getItem(VOICE_KEY);
      return v === "passive" || v === "active" ? v : "active";
    } catch {
      return "active";
    }
  }

  function writeStoredVoice(voice) {
    try {
      sessionStorage.setItem(VOICE_KEY, voice);
    } catch {
      /* ignore */
    }
  }

  function readStoredMood() {
    try {
      return sessionStorage.getItem(MOOD_KEY) || "";
    } catch {
      return "";
    }
  }

  function writeStoredMood(id) {
    try {
      if (id) sessionStorage.setItem(MOOD_KEY, id);
    } catch {
      /* ignore */
    }
  }

  function moodBase(id) {
    return (id || "").replace(/-passive$/, "") || DEFAULT_MOOD;
  }

  function currentVoice() {
    const open = root.querySelector(
      '.conjugation-voice-panel:not([hidden])[data-voice]',
    );
    return open?.dataset.voice === "passive" ? "passive" : "active";
  }

  function markMoodActive(id) {
    const base = moodBase(id);
    for (const link of moodLinks) {
      const href = (link.getAttribute("href") || "").replace(/^#/, "");
      const on = moodBase(href) === base;
      link.classList.toggle("mood-nav-link--active", on);
      if (on) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    }
  }

  function setMood(id, { updateHash = true } = {}) {
    const base = moodBase(id);
    for (const section of moodSections) {
      const heading = section.querySelector(".mood-heading[id]");
      const sectionBase = moodBase(heading?.id || "");
      const on = sectionBase === base;
      section.hidden = !on;
      if (on) section.removeAttribute("hidden");
      else section.setAttribute("hidden", "");
    }
    markMoodActive(base);
    writeStoredMood(base);
    if (updateHash) {
      const suffix = currentVoice() === "passive" && hasPassive ? "-passive" : "";
      const hash = `#${base}${suffix}`;
      if (window.location.hash !== hash) {
        history.replaceState(null, "", hash);
      }
    }
  }

  function setVoice(voice) {
    if (voice === "passive" && !hasPassive) voice = "active";
    for (const panel of [activePanel, passivePanel]) {
      if (!panel) continue;
      const on = panel.dataset.voice === voice;
      if (on) {
        panel.hidden = false;
        panel.removeAttribute("hidden");
      } else {
        panel.hidden = true;
        panel.setAttribute("hidden", "");
      }
    }
    for (const tab of tabs) {
      if (tab.hidden) continue;
      const on = tab.dataset.voice === voice;
      tab.classList.toggle("voice-tab--active", on);
      tab.setAttribute("aria-selected", on ? "true" : "false");
    }
    const suffix = voice === "passive" ? "-passive" : "";
    for (const link of moodLinks) {
      const href = link.getAttribute("href") || "";
      const id = moodBase(href.replace(/^#/, ""));
      if (!id) continue;
      link.setAttribute("href", `#${id}${suffix}`);
    }
    writeStoredVoice(voice);
    // Keep the selected mood visible in the newly shown panel.
    setMood(readStoredMood() || DEFAULT_MOOD);
  }

  for (const tab of tabs) {
    tab.addEventListener("click", () => {
      setVoice(tab.dataset.voice || "active");
    });
  }

  for (const link of moodLinks) {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      const href = link.getAttribute("href") || "";
      setMood(href.replace(/^#/, ""));
    });
  }

  const hashMood = moodBase(window.location.hash.replace(/^#/, ""));
  const initialMood =
    (hashMood.startsWith("mood-") && hashMood) ||
    readStoredMood() ||
    DEFAULT_MOOD;

  setVoice(readStoredVoice());
  setMood(initialMood);
})();
