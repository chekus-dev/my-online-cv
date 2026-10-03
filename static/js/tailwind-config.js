// Maps Tailwind colour names to the CSS variables defined in site.css.
// Loaded after the Tailwind CDN script on every page.
tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: "rgb(var(--bg) / <alpha-value>)",
        surface: "rgb(var(--surface) / <alpha-value>)",
        surface2: "rgb(var(--surface2) / <alpha-value>)",
        ink: "rgb(var(--ink) / <alpha-value>)",
        muted: "rgb(var(--muted) / <alpha-value>)",
        mutedstrong: "rgb(var(--mutedstrong) / <alpha-value>)",
        borderstrong: "rgb(var(--borderstrong) / <alpha-value>)",
        accent: "rgb(var(--accent) / <alpha-value>)",
        accentstrong: "rgb(var(--accentstrong) / <alpha-value>)",
        accentdim: "rgb(var(--accentdim) / <alpha-value>)",
      },
      fontFamily: {
        display: ['"Space Grotesk"', "Inter", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ['"JetBrains Mono"', "ui-monospace", "monospace"],
      },
    },
  },
};