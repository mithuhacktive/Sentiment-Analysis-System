/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#090d16',
        surface: '#0f172a',
        'surface-elevated': '#1e293b',
        'surface-border': '#334155',
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
        },
        sentiment: {
          positive: '#10b981', // emerald-500
          'positive-bg': 'rgba(16, 185, 129, 0.12)',
          negative: '#f43f5e', // rose-500
          'negative-bg': 'rgba(244, 63, 94, 0.12)',
          neutral: '#f59e0b', // amber-500
          'neutral-bg': 'rgba(245, 158, 11, 0.12)',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'spin-slow': 'spin 12s linear infinite',
      }
    },
  },
  plugins: [],
}
