module.exports = {
    tabWidth: 2,
    jsxSingleQuote: true,
    printWidth: 100,
    singleQuote: true,
    semi: false,
    endOfLine: 'auto',
    overrides: [
        {
            files: '*.json',
            options: {
                printWidth: 200,
            },
        },
    ],
    arrowParens: 'always',
}
