document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("projects-root");
  if (!root) return; // Not on the portfolio page

  const chips = document.querySelectorAll(".filter-chip");
  const sections = document.querySelectorAll(".account-section");
  const emptyState = document.getElementById("empty-state");
  const countEl = document.getElementById("filter-count");

  // Build state from whichever filter groups actually exist in the markup
  // (currently "account" and "lang"), instead of hardcoding them, so a new
  // chip group just works without touching this file.
  const groups = new Set();
  chips.forEach((chip) => groups.add(chip.dataset.filterGroup));

  const params = new URLSearchParams(window.location.search);
  const state = {};
  groups.forEach((group) => {
    state[group] = params.get(group) || "all";
  });

  function syncChipState() {
    chips.forEach((chip) => {
      const group = chip.dataset.filterGroup;
      const isActive = chip.dataset.filterValue === state[group];
      chip.classList.toggle("is-active", isActive);
      chip.setAttribute("aria-pressed", String(isActive));
    });
  }

  function syncUrl() {
    const next = new URLSearchParams(window.location.search);
    groups.forEach((group) => {
      if (state[group] && state[group] !== "all") {
        next.set(group, state[group]);
      } else {
        next.delete(group);
      }
    });
    const query = next.toString();
    const url = query ? `${window.location.pathname}?${query}` : window.location.pathname;
    window.history.replaceState(null, "", url);
  }

  function applyFilters() {
    let visibleTotal = 0;

    sections.forEach((section) => {
      let visibleInSection = 0;

      section.querySelectorAll(".project-card").forEach((card) => {
        const matches = [...groups].every((group) => {
          return state[group] === "all" || card.dataset[group] === state[group];
        });

        card.hidden = !matches;
        if (matches) {
          visibleInSection += 1;
          visibleTotal += 1;
        }
      });

      section.hidden = visibleInSection === 0;
    });

    if (emptyState) emptyState.classList.toggle("hidden", visibleTotal > 0);
    if (countEl) {
      countEl.textContent = visibleTotal === 1 ? "1 project" : `${visibleTotal} projects`;
    }
  }

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const group = chip.dataset.filterGroup;
      const value = chip.dataset.filterValue;

      // Clicking the already-active chip resets that group back to "all"
      // instead of doing nothing, so chips double as their own clear button.
      state[group] = state[group] === value ? "all" : value;

      syncChipState();
      syncUrl();
      applyFilters();
    });
  });

  syncChipState();
  applyFilters();
});