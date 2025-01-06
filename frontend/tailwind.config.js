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
                    'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji',
                ],
            },
        },
    },
    plugins: [require('flyonui'), require('flyonui/plugin')],
    flyonui: {
        themes: ['light', 'dark'],
    },
};
