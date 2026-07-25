import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#eef6ff",
          100: "#d9ecff",
          200: "#bcdcff",
          300: "#8ec4ff",
          400: "#59a3ff",
          500: "#2f7dff",
          600: "#1a5cf0",
          700: "#1547d1",
          800: "#173aa8",
          900: "#183485",
          950: "#121f52",
        },
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease-in-out",
        shimmer: "shimmer 1.6s infinite linear",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0", transform: "translateY(4px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        shimmer: { "0%": { backgroundPosition: "-700px 0" }, "100%": { backgroundPosition: "700px 0" } },
      },
    },
  },
  plugins: [],
};
export default config;
