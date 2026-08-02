# Coding Standards

## Naming Convention

- Folders and files use `snake_case` always.
- Class names use `PascalCase`.
- Runnable folders (files intended to be executed from console) are named with an `-or` suffix: `processors`, `predictors`, `trainers`, etc.
- Non-runnable folders holding reusable classes or utilities (e.g. `loss_functions`, `datasets`) do not follow the `-or` rule.

## Project Structure

- All source code lives under `src/`.
- Runnable files (`train_one_gpu_custom_loss.py`) are placed in `-or` folders such as `trainers/`.
- Utility files (`custom_loss.py`) are placed in descriptive folders such as `loss_functions/`.

## File Organization

- Every class, enum, dataclass, or type alias must have its own file.
- Enums go in an `enums/` folder, one file per enum.
- Structurally related dataclasses go in a descriptive folder (e.g. `annotations/`), one file per dataclass.
- Groups of simple config classes go in a `config/` folder, one file per class.
- Only pure-function modules may contain multiple functions in one file.

## Code Style

- Write readable, explicit code. Do **not** use one-liner shortcuts:
  ```python
  # Wrong
  if condition: return result

  # Correct
  if condition:
      return result
  ```
- Every function argument must have a type annotation.
- Every function and method must declare a return type annotation, even if it is `-> None`.
- Follow Python OOP conventions when using classes: `__init__`, `super().__init__()`, explicit `self`, proper inheritance.
- All imports must be at the top of the file, before any function or class definition. Group them: standard library, third-party, local.
- Never write an import inside a function or method body. If a circular dependency makes a top-level import impossible, create a new file that both modules can import from, and put the import there at the top.
- Empty function or method bodies (e.g. abstract method stubs, no-op implementations) must use `pass`, never `...`.

## Comments

- You may add a docstring at the top of a file to briefly explain the purpose of the file.
- Write inline comments only where the code is genuinely hard to read or the intent is not obvious.
- Do not add docstrings or comments to trivial or self-explanatory code.

## Error Handling

- This is an internal research tool. Do **not** validate parameters, inputs, or data types.
- If a mistake is made, let the script crash immediately with a traceback so the developer can fix the root cause.

## Language

- Everything — code, comments, commit messages — must be written in English.
