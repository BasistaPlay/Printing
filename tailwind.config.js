/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './templates/*.html',
    './static/**/*.js',
    './static/**/*.css',
    './home/templates/**/*.html',
    './Product/templates/**/*.html',
    './shoping_cart/templates/**/*.html',
    './User_app/templates/**/*.html',
    './User_app/templates/*.html',
    './payments/templates/**/*.html',
    './payments/templates/*.html',
    './ecommerce/static/src/**/*.js',
    './static/**/*.js',
    './static/**/*.css',
    '!./node_modules/**/*',
    './ecomerce/templates/**/*.html',
    './ecomerce/static/src/**/*.js',
    './ecomerce/static/src/**/*.css',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'bg2-color': 'var(--bg2-color)',
        'text-color': 'var(--text-color)',
        'bg-color': 'var(--bg-color)',
        'main-color': 'var(--main-color)',
        'second-color': 'var(--second-color)',
        'other-color': 'var(--other-color)',
        'hover-color': 'var(--hover-color)',
        'input-color': 'var(--input-color)',
        'input-readonly-color': 'var(--input-readonly-color)',
        'main-hover-color': 'var(--main-hover-color)',
      },
      animation: {
        'infinite-scroll': 'infinite-scroll 25s linear infinite',
      },
      keyframes: {
        'infinite-scroll': {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(-100%)' },
        },
      },
      gridTemplateColumns: {
        'custom': 'repeat(3, 200px)',
      },
    },
  },
  plugins: [],
};