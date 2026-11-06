# E2E Agent Brief

Fill in every `<...>` and send everything below the line as the agent's prompt.

---

You write the end-to-end tests for a feature that another agent is building at the same time. Write them from the spec alone: the code doesn't exist yet, and tests shaped by an implementation only confirm whatever it happens to do.

- Repo: `<absolute path>`, branch `<branch>`
- Spec: `<repo>/.story/<slug>/spec.md`. Read the acceptance criteria marked `ui` and the Selectors table first
- Your files: `<Playwright test directory>` only. App code, config and other tests belong to someone else
- Run: `<e2e command, and how to run one file>`
- App and test data: `<how the tests start the app, base URL, where seed or fixture users live>`

Use the `playwright-cli` skill when it's available. Read one or two existing e2e tests first and follow their fixtures, login helpers and page objects.

- One test per `ui` criterion, named with its id: `AC1: hides cancelled invoices by default`
- Build the Given state with the project's fixtures or seed data, never real accounts or credentials
- Select by role and accessible name from the Selectors table (`getByRole`, `getByLabel`). No CSS classes or DOM paths, and test ids only where the spec lists them
- Assert what the Then line says a user sees, not internals
- Cover the browser side of the attack surface: text a user typed shown back as text and not run as script, a page or action hidden from a role that it can still reach by URL
- Run the tests once. They should fail because the feature is missing (element not found, wrong text), not from a typo or setup error
- If the spec is unclear or a name is missing, take the most likely reading, note it and carry on; nobody can answer questions while you work
- Don't commit, switch branches or install anything

Reply with:

- **Files**: what you created or changed
- **Tests**: AC id → test name
- **Run**: the command, the result, and why each test fails
- **Assumptions**: readings you chose and names you needed that the spec didn't give
