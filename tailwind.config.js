/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/**/*.html",
    "./frontend/**/*.js",
    "./templates/**/*.html",
    "./*/templates/**/*.html",
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [
    require("daisyui"),
  ],
  daisyui: {
    themes: ["light"],
  },
};
