/**
 * Conjugation paradigm UI: mood anchors + active/passive voice tabs.
 * Tables are already in the static HTML; this only toggles visibility.
 * Voice + last mood persist across verb pages via sessionStorage.
 */
(() => {
  const root = document.querySelector(".conjugation");
  if (!root) return;

  const VOICE_KEY = "plumera:conjugation:voice";
  const MOOD_KEY = "plumera:conjugation:mood";

  const activePanel = root.querySelector(
    '.conjugation-voice-panel[data-voice="active"]',
  );
  const passivePanel = root.querySelector(
    '.conjugation-voice-panel[data-voice="passive"]',
  );
  const tabs = [...document.querySelectorAll(".voice-tab[data-voice]")];
  const moodLinks = [...document.querySelectorAll(".mood-nav-link[href^='#']")];

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

  function markMoodActive(id) {
    const base = (id || "").replace(/-passive$/, "");
    for (const link of moodLinks) {
      const href = (link.getAttribute("href") || "").replace(/^#/, "");
      const linkBase = href.replace(/-passive$/, "");
      const on = Boolean(base) && linkBase === base;
      link.classList.toggle("mood-nav-link--active", on);
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
      const id = href.replace(/^#/, "").replace(/-passive$/, "");
      if (!id) continue;
      link.setAttribute("href", `#${id}${suffix}`);
    }
    writeStoredVoice(voice);
  }

  for (const tab of tabs) {
    tab.addEventListener("click", () => {
      setVoice(tab.dataset.voice || "active");
    });
  }

  for (const link of moodLinks) {
    link.addEventListener("click", () => {
      const href = link.getAttribute("href") || "";
      const id = href.replace(/^#/, "");
      writeStoredMood(id.replace(/-passive$/, ""));
      markMoodActive(id);
    });
  }

  setVoice(readStoredVoice());

  // Restore mood highlight only — do not scroll. Header → /conjugation/ must
  // land at the top of the page; scrolling to the last mood felt like a jump
  // to the middle.
  const storedMood = readStoredMood();
  markMoodActive(storedMood || "mood-indicatif");

  function syncMoodScrollMargin() {
    const header = document.querySelector(".conjugation-header");
    if (!header) return;
    const px = Math.ceil(header.getBoundingClientRect().height) + 12;
    document.documentElement.style.setProperty(
      "--conjugation-sticky-offset",
      `${px}px`,
    );
  }
  syncMoodScrollMargin();
  window.addEventListener("resize", syncMoodScrollMargin);
})();
