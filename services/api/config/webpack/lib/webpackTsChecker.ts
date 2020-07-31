import ForkTsCheckerWebpackPlugin from 'fork-ts-checker-webpack-plugin'

export interface WebpackTsCheckerOptions {
  eslint: boolean
  typeChecking: boolean
  memoryLimit?: number
  exclude?: string[]
}

export default function webpackTsChecker({
  typeChecking,
  eslint,
  memoryLimit = 512, // Megabytes
  exclude = [],
}: WebpackTsCheckerOptions) {
  return new ForkTsCheckerWebpackPlugin({
    issue: {
      exclude: exclude?.map((file) => ({ origin: 'typescript', file })),
    },

    typescript: {
      enabled: typeChecking,
      memoryLimit,
      mode: 'write-references',
      diagnosticOptions: {
        declaration: true,
        global: true,
        semantic: true,
        syntactic: true,
      },
      configOverwrite: {
        exclude,
      },
    },

    eslint: {
      enabled: eslint,
      memoryLimit,
      files: ['**/*.{js,jsx,ts,tsx}'],
      options: { cache: false },
    },

    formatter: 'codeframe',
  })
}
