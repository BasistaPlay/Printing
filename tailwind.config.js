module.exports = {
  content: [
    './forum/templates/**/*.html',
    './home/templates/**/*.html',
    './Product/templates/**/*.html',
    './shoping_cart/templates/**/*.html',
    './User_app/templates/**/*.html',
    './ecommerce/static/src/**/*.js',
    './static/**/*.js', // Only your own JavaScript files
    './static/**/*.css',
    // Exclude node_modules by being more specific
    '!./node_modules/**/*',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
