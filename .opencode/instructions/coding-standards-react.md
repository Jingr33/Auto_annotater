# Coding Standards — React TypeScript Frontend

## Naming Convention

- Component files: `PascalCase.tsx` (e.g. `AnnotationPanel.tsx`).
- Hook files: `camelCase.ts` with `use` prefix (e.g. `useAnnotations.ts`).
- Utility/helper files: `camelCase.ts` (e.g. `formatLabel.ts`).
- Type definition files: `camelCase.types.ts` or inside a `types/` folder.
- Folders use `camelCase` (e.g. `components/`, `hooks/`, `services/`).

## Project Structure

- All frontend source code lives under `src/frontend_pro/`.
- React app follows standard Vite + React structure:
  ```
  src/frontend_pro/
  ├── src/
  │   ├── components/       # Reusable UI components
  │   │   └── ComponentName/
  │   │       ├── ComponentName.tsx
  │   │       ├── ComponentName.test.tsx
  │   │       └── index.ts
  │   ├── hooks/            # Custom React hooks
  │   ├── services/         # API calls, external services
  │   ├── types/            # Shared TypeScript types
  │   ├── utils/            # Pure utility functions
  │   ├── App.tsx
  │   └── main.tsx
  ├── public/
  ├── index.html
  ├── package.json
  ├── tsconfig.json
  └── vite.config.ts
  ```

## Component Rules

- Each class, component, type, and any other structure must be in its own separate file.
- One component per file. Component name matches file name.
- Use functional components with hooks, never class components.
- Props must be defined as a named interface or type, exported from the same file:
  ```typescript
  export interface AnnotationPanelProps {
    items: Annotation[];
    onSelect: (id: string) => void;
  }

  export function AnnotationPanel({ items, onSelect }: AnnotationPanelProps) {
    // ...
  }
  ```
- Keep components small and focused. If a component exceeds ~150 lines, split it.
- Co-locate component-specific types, hooks, and utilities with the component.

## Styling

- Use **Material UI only** (`@mui/material`) for all styling and UI components.

## Code Style

- Use `const` by default. Use `let` only when reassignment is necessary. Never use `var`.
- Use arrow functions for components and callbacks:
  ```typescript
  const handleClick = (id: string) => {
    setSelected(id);
  };
  ```
- Prefer named exports over default exports.
- Use TypeScript `interface` for object shapes, `type` for unions/intersections.
- Always specify return types on non-trivial functions.
- Use optional chaining (`?.`) and nullish coalescing (`??`) instead of manual null checks.
- Add an empty line between JSX components and siblings to improve readability.

## Comments

- Add a brief comment at the top of complex components explaining their purpose.
- Write inline comments only where the logic is non-obvious.
- Do not comment self-explanatory code.

## Language

- Everything — code, comments, commit messages — must be written in English.
