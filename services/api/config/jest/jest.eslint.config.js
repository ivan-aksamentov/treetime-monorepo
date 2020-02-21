require('../dotenv')

const { findModuleRoot } = require('../../lib/findModuleRoot')

const { moduleRoot } = findModuleRoot()

module.exports = {
  rootDir: moduleRoot,
  roots: ['<rootDir>/src'],
  runner: 'jest-runner-eslint',
  displayName: { name: 'lint', color: 'blue' },
  testEnvironment: 'jest-environment-node',
  preset: 'ts-jest',
  globals: {
    'ts-jest': {
      babelConfig: true,
      diagnostics: {
        pathRegex: /(\/__tests__\/.*|([./])(test|spec))\.[jt]sx?$/,
        warnOnly: true,
      },
    },
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.(spec|test).{js,jsx,ts,tsx}',
  ],
  watchPlugins: [
    'jest-runner-eslint/watch-fix', // prettier-ignore
  ],
}
