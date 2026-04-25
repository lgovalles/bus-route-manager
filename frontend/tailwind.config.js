/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        somos: {
          primary: '#0C304C',
          secondary: '#78A269',
          accent: '#F2B944',
          alert: '#B51F29',
        },
      },
      maxWidth: {
        container: '1280px',
      },
    },
  },
  plugins: [],
}