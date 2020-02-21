const path = require('path')

module.exports = {
  root: true,
  parser: '@typescript-eslint/parser',
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
    ecmaFeatures: {
      jsx: true,
      globalReturn: false,
    },
    tsconfigRootDir: __dirname,
    project: ['./tsconfig.json'],
    extraFileExtensions: ['.json'],
    warnOnUnsupportedTypeScriptVersion: true,
  },
  globals: {},
  extends: [
    'eslint:recommended',
    'airbnb',
    'react-app',

    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:array-func/all',
    'plugin:import/errors',
    'plugin:import/typescript',
    'plugin:import/warnings',
    'plugin:jest/recommended',
    'plugin:jest/style',
    'plugin:jsx-a11y/recommended',
    'plugin:lodash/recommended',
    'plugin:promise/recommended',
    'plugin:react-redux/recommended',
    'plugin:react/recommended',
    'plugin:redux-saga/recommended',
    'plugin:security/recommended',
    'plugin:sonarjs/recommended',
    'plugin:unicorn/recommended',

    // prettier should go last
    'plugin:prettier/recommended',
    'prettier/react',
    'prettier/@typescript-eslint',
  ],
  plugins: [
    'array-func',
    'cflint',
    'import',
    'jest',
    'json',
    'jsx-a11y',
    'lodash',
    'no-loops',
    'no-secrets',
    'node',
    'only-ascii',
    'promise',
    'react',
    'react-hooks',
    'react-redux',
    'redux-saga',
    'security',
    'sonarjs',
    'unicorn',

    'only-warn',

    '@typescript-eslint',
    '@typescript-eslint/tslint',

    // prettier should go last
    'prettier',
  ],
  rules: {
    '@typescript-eslint/array-type': 'off',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/unbound-method': ['off'],
    'array-func/prefer-array-from': 'off',
    'cflint/no-substr': 'warn',
    'cflint/no-this-assignment': 'warn',
    'import/extensions': [
      'warn',
      'ignorePackages',
      {
        js: 'never',
        jsx: 'never',
        mjs: 'never',
        ts: 'never',
        tsx: 'never',
      },
    ],
    'import/no-extraneous-dependencies': ['warn', { devDependencies: true }],
    'import/order': 'warn',
    'import/prefer-default-export': 'off',
    'jest/consistent-test-it': 'warn',
    'jest/expect-expect': 'warn',
    'jest/no-test-callback': 'warn',
    'jsx-a11y/label-has-associated-control': ['warn', { assert: 'either' }],
    'lodash/chaining': 'off',
    'lodash/import-scope': 'off',
    'lodash/prefer-constant': 'off',
    'lodash/prefer-lodash-chain': 'off',
    'lodash/prefer-lodash-method': 'off',
    'lodash/prefer-lodash-typecheck': 'off',
    'no-console': ['warn', { allow: ['info', 'warn', 'error'] }],
    'no-loops/no-loops': 'warn',
    'no-secrets/no-secrets': ['warn', { tolerance: 5 }],
    'no-shadow': 'off',
    'only-ascii/only-ascii': 'warn',
    'prettier/prettier': 'warn',
    'react-redux/prefer-separate-component-file': 'off',
    'react/jsx-curly-brace-presence': 'off',
    'react/jsx-filename-extension': [
      'warn',
      { extensions: ['.js', '.jsx', '.ts', '.tsx'] },
    ],
    'react/jsx-props-no-spreading': 'off',
    'react/prop-types': 'off',
    'react/state-in-constructor': 'off',
    'redux-saga/no-unhandled-errors': 'off',
    'security/detect-non-literal-fs-filename': 'off',
    'security/detect-object-injection': 'off',
    'unicorn/filename-case': 'off',
    'unicorn/new-for-builtins': 'off',
    'unicorn/no-abusive-eslint-disable': 'warn',
    'unicorn/prefer-query-selector': 'off',
    'unicorn/prevent-abbreviations': 'off',

    'lines-between-class-members': [
      'warn',
      'always',
      { exceptAfterSingleLine: true },
    ],

    '@typescript-eslint/tslint/config': [
      'warn',
      { lintFile: path.join(__dirname, 'tslint.json') },
    ],

    'require-await': 'off',
    '@typescript-eslint/require-await': 'off',

    'no-unused-expressions': 'off',
    '@typescript-eslint/no-unused-expressions': 'warn',
  },
  env: {
    browser: true,
    es6: true,
    jest: true,
    node: true,
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  overrides: [
    {
      files: ['*.json'],
      rules: {
        '@typescript-eslint/no-useless-files': 'off',
      },
    },
    {
      files: ['*.d.ts'],
      rules: {
        '@typescript-eslint/no-unused-vars': 'off',
        'no-useless-constructor': 'off',
      },
    },
    {
      files: [
        '.eslintrc.js',
        'babel.config.js',
        'config/**/*.js',
        'config/**/*.ts',
        'jest-runner-eslint.config.js',
        'jest.config.js',
        'postcss.config.js',
        'lib/findModuleRoot.js',
        'stylelint.config.js',
        'webpack.config.js',
      ],
      rules: {
        'global-require': 'off',
        '@typescript-eslint/no-var-requires': 'off',
        'sonarjs/cognitive-complexity': ['warn', 50],
      },
    },
    {
      files: ['src/index.polyfilled.*'],
      rules: {
        '@typescript-eslint/no-typeof-undefined': 'off',
        '@typescript-eslint/tslint/no-typeof-undefined': 'off',
        'global-require': 'off',
        'lodash/prefer-lodash-typecheck': 'off',
        'no-typeof-undefined': 'off',
        'tslint:no-typeof-undefined': 'off',
        'unicorn/import-index': 'off',
      },
    },
    {
      files: ['src/state/store.ts'],
      rules: {
        'global-require': 'off',
        'no-underscore-dangle': 'off',
      },
    },
    {
      files: ['src/state/sagas.ts'],
      rules: {
        'no-loops/no-loops': 'off',
      },
    },
    {
      files: ['**/__tests__/**', '**/*.test.*'],
      rules: {
        'sonarjs/no-identical-functions': 'off',
      },
    },
    {
      files: [
        '**/__tests__/*.reducer.*',
        '**/__tests__/*.reducers.*',
        '**/*.reducer.test.*',
        '**/*.reducers.test.*',
        '**/__tests__/*.saga.*',
        '**/__tests__/*.sagas.*',
        '**/*.saga.test.*',
        '**/*.sagas.test.*',
      ],
      rules: {
        'jest/expect-expect': 'off',
      },
    },
    {
      files: ['**/*.reducer.*', '**/*.reducers.*'],
      rules: {
        'no-param-reassign': [
          'warn',
          { ignorePropertyModificationsFor: ['draft'] },
        ],
      },
    },
  ],
}
