/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */
import withMT from "@material-tailwind/html/utils/withMT";

/** @type {import('tailwindcss').Config} */

module.exports = withMT( {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

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
    media: false, // Disables media-query based `prefers-reduced-motion`
    darkMode: "class", // Enables class-based dark mode
    theme: {
        extend: {
            colors: {
                primary: {
                    50: "rgb(var(--color-primary-100) / <alpha-value>)",
                    100: "rgb(var(--color-primary-100) / <alpha-value>)",
                    200: "rgb(var(--color-primary-200) / <alpha-value>)",
                    300: "rgb(var(--color-primary-300) / <alpha-value>)",
                    400: "rgb(var(--color-primary-400) / <alpha-value>)",
                    500: "rgb(var(--color-primary-500) / <alpha-value>)",
                    600: "rgb(var(--color-primary-600) / <alpha-value>)",
                    700: "rgb(var(--color-primary-700) / <alpha-value>)",
                    800: "rgb(var(--color-primary-800) / <alpha-value>)",
                    900: "rgb(var(--color-primary-900) / <alpha-value>)",
                },
                'navy-blue': '#0E2E76',
                'medium-dark-blue': '#1D2088',
                'true-royal-blue': '#3B82F6',
                'white': '#FFFFFF',
                'black': '#000000',
                'dark-navy-blue': '#270089',
                'raven-black': '#222222',
                'gray-dark': '#273444',
                'gray': '#8492A6',
                'gray-light': '#D3DCE6',
                'red': '#FF0000',
                'green': '#75F94C'
              },
            fontFamily: {
                'roboto': ['Roboto', 'sans-serif']
            },
            fontSize: {
                0: [0, 1],
                xxs: ["11px", "14px"],
            },
            minWidth: {
                sidebar: "18rem",
            },
            spacing: {
                68: "17rem",
                128: "32rem",
            },
            transitionProperty: {
                height: "height",
                width: "width",
            },
            width: {
                sidebar: "18rem",
            },
        },
    },
    variants: {
        extend: {
            borderColor: ["checked", "focus-within", "hover"],
            display: ["group-hover"],
            overflow: ["hover"],
            textColor: ["hover"],
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
});
