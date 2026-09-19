import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        studio: {
          bg: "#090d16",
          surface: "#0d1117",
          card: "#161b22",
          border: "#30363d",
          muted: "#8b949e",
          text: "#c9d1d9",
          highlight: "#f0f6fc",
          amber: "#f59e0b",
          cyan: "#06b6d4",
          emerald: "#10b981",
          crimson: "#f43f5e",
        },
      },
      fontFamily: {
        mono: ["var(--font-mono)", "JetBrains Mono", "Courier New", "monospace"],
        sans: ["var(--font-sans)", "Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
