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
      // Rounder corners site-wide. Every rounded-* utility already used
      // in the templates (rounded-lg, rounded-xl, rounded-2xl, etc.)
      // now resolves to a larger radius without touching any HTML —
      // this is Tailwind's default scale with each step bumped up.
      borderRadius: {
        sm: "0.375rem",   // was 0.125rem
        DEFAULT: "0.5rem", // was 0.25rem
        md: "0.625rem",   // was 0.375rem
        lg: "1rem",       // was 0.5rem
        xl: "1.25rem",    // was 0.75rem
        "2xl": "1.75rem", // was 1rem
        "3xl": "2.25rem", // was 1.5rem
      },
    },
  },
};