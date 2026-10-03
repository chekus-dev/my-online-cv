document.addEventListener("DOMContentLoaded", () => {
	const root = document.getElementById("projects-root");
	if (!root) return; // Not on the portfolio page

	const chips = document.querySelectorAll(".filter-chip");
	const cards = document.querySelectorAll(".project-card");
	const sections = document.querySelectorAll(".account-section");
	const emptyState = document.getElementById("empty-state");
	const countEl = document.getElementById("filter-count");

	const state = { account: "all", lang: "all" };

	function applyFilters() {
		let visibleTotal = 0;

		sections.forEach((section) => {
			let visibleInSection = 0;
			const sectionAccount = section.dataset.account;

			section.querySelectorAll(".project-card").forEach((card) => {
				const matchesAccount = state.account === "all" || card.dataset.account === state.account;
				const matchesLang = state.lang === "all" || card.dataset.lang === state.lang;
				const show = matchesAccount && matchesLang;
				card.hidden = !show;
				if (show) {
					visibleInSection += 1;
					visibleTotal += 1;
				}
			});

			section.hidden = visibleInSection === 0;
		});

		emptyState.classList.toggle("hidden", visibleTotal > 0);
		if (countEl) {
			countEl.textContent = visibleTotal === 1 ? "1 project" : `${visibleTotal} projects`;
		}
	}

	chips.forEach((chip) => {
		chip.addEventListener("click", () => {
			const group = chip.dataset.filterGroup;
			const value = chip.dataset.filterValue;

			state[group] = value;

			document
				.querySelectorAll(`.filter-chip[data-filter-group="${group}"]`)
				.forEach((el) => el.classList.toggle("is-active", el === chip));

			applyFilters();
		});
	});

	applyFilters();
});
