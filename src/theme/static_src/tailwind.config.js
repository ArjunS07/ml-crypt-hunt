/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

const colors = require("tailwindcss/colors");

module.exports = {
  darkMode: 'class',
  content: [
    /**
     * HTML. Paths to Django template files that will contain Tailwind CSS classes.
     */

    /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
    "../templates/**/*.html",

    /*
     * Main templates directory of the project (BASE_DIR/templates).
     * Adjust the following line to match your project structure.
     */
    "../../templates/**/*.html",

    /*
     * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
     * Adjust the following line to match your project structure.
     */
    "../../**/templates/**/*.html",

    /**
     * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
     * patterns match your project structure.
     */
    /* JS 1: Ignore any JavaScript in node_modules folder. */
    // '!../../**/node_modules',
    /* JS 2: Process all JavaScript files in the project. */
    // '../../**/*.js',

    /**
     * Python: If you use Tailwind CSS classes in Python, uncomment the following line
     * and make sure the pattern below matches your project structure.
     */
    // '../../**/*.py'
  ],
  theme: {
    fontFamily: {
      'sans': ['Prompt'],
      'display': ['IBM Plex Mono']
    },
    extend: {
      colors: {
        "primary-light": colors.violet[500],
        "secondary-light": colors.gray[100],

        "green-house-light": colors.green[300],
        "red-house-light": colors.red[400],
        "blue-house-light": colors.blue[300],
        "yellow-house-light": colors.amber[400],

        "primary-dark": colors.violet[400],
        "secondary-dark": colors.neutral[800],

        "green-house-dark": colors.green[400],
        "red-house-dark": colors.rose[500],
        "blue-house-dark": colors.blue[400],
        "yellow-house-dark": colors.yellow[400],
      },
    },
  },
  plugins: [
    /**
     * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
     * for forms. If you don't like it or have own styling for forms,
     * comment the line below to disable '@tailwindcss/forms'.
     */
    // require('@tailwindcss/forms'),
    require("@tailwindcss/typography"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
  safelist: [
    'bg-green-house-light',
    'bg-red-house-light',
    'bg-blue-house-light',
    'bg-yellow-house-light',

    'bg-green-house-dark',
    'bg-red-house-dark',
    'bg-blue-house-dark',
    'bg-yellow-house-dark',

    'text-green-house-light',
    'text-red-house-light',
    'text-blue-house-light',
    'text-yellow-house-light',

    'dark:text-green-house-dark',
    'dark:text-red-house-dark',
    'dark:text-blue-house-dark',
    'dark:text-yellow-house-dark',

    'dark:border-green-600',
    'dark:border-red-600',
    'dark:border-blue-600',
    'dark:border-yellow-600',
  ]
};
