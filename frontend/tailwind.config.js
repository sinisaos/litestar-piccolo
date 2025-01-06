/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './node_modules/flyonui/flyonui.js',
        './src/**/*.{vue,js,ts}',
        '*.html',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: [
                    'Inter, ui-sans-serif, system-ui'
                ],
            },
        },
    },
    plugins: [require('flyonui'), require('flyonui/plugin')],
    flyonui: {
        themes: ['light', 'dark'],
    },
};
