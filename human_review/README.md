# Human Review Queue

This folder contains cases that require manual review.

## How it works

- When ML output is unsafe, a JSON file is created in `queue/`
- Each file represents ONE case
- Human reviewer opens the file
- Updates `human_verdict`
- Saves the file

## What to edit

Only edit this section:

```json
"human_verdict": {
  "status": "approved | corrected | rejected",
  "comments": "Your explanation here"
}
