# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and Biome for linting, formatting, and import ordering.

## Development

### Prerequisites

- Node.js 20+
- npm

### Setup

```bash
npm install
```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run lint` - Run Biome check
- `npm run lint:fix` - Run Biome check with auto-fix
- `npm run format` - Format code with Biome

## Biome Configuration

Biome is configured in `biome.json` and provides:

- **Linting**: Enforces code quality rules
- **Formatting**: Consistent code style (2 spaces, double quotes, trailing commas)
- **Import Ordering**: Automatic import organization

### VS Code Extension

Install the Biome VS Code extension for real-time linting and formatting:

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Biome"
4. Install "Biome" (biomejs.biome)

The extension will automatically use the `biome.json` configuration.

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Biome Rules

Biome is configured with the following rules:

- Recommended rules enabled
- `noUnusedImports`: Warn on unused imports
- `noUnusedVariables`: Warn on unused variables
- `noNonNullAssertion`: Warn on non-null assertions
- `useConst`: Enforce const for variables that are never reassigned
- `useArrowFunction`: Enforce arrow functions for callbacks
- `noExplicitAny`: Warn on explicit any types

See the [Biome documentation](https://biomejs.dev/) for the full list of rules and options.
