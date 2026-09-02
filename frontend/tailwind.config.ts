import type { Config } from "tailwindcss";

export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./ui/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Slate ink + cloud greys — Anthropic marketing surface
        ink: "#141413",
        "ink-soft": "#3d3d3a",
        "text-muted": "#5e5d59",
        "text-secondary": "#b0aea5",
        "text-tertiary": "#87867f",
        hairline: "#d1cfc5",

        // Cream canvas + warm neutrals — the surface ladder
        canvas: "#faf9f5",
        "surface-secondary": "#f0eee6",
        "surface-secondary-hover": "#e8e6dc",
        "surface-warm": "#e3dacc",
        "surface-manilla": "#ebdbbc",
        "surface-kraft": "#d4a27f",

        // Accent swatches
        "accent-clay": "#d97757",
        "accent-coral": "#ebcece",
        "accent-fig": "#c46686",
        "accent-cactus": "#bcd1ca",
        "accent-olive": "#788c5d",
        "accent-sky": "#6a9bcc",
        "accent-heather": "#cbcadb",
        "accent-deep": "#c6613f",

        // Inverse — for the full-bleed black bands
        inverse: "#000000",
      },
      fontFamily: {
        serif: ['Georgia', 'Tiempos Text', 'serif'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"JetBrains Mono"', '"Berkeley Mono"', 'monospace'],
      },
      borderRadius: {
        sm: "8px",
        md: "16px",
        lg: "24px",
      },
    },
  },
  plugins: [],
} satisfies Config;
