# Contributing

Thanks for helping improve delego's Claude Code skills. Contributions are welcome
— more authoring and operating skills make the toolkit more useful.

**Important:** a skill is an *instruction set that runs in other people's Claude
Code sessions.* A contribution is a prompt, not just documentation — review it as
you would code that executes on someone else's machine.

## How to contribute

- **Fork** the repo and open a PR from a branch in your fork.
- A skill is a directory `<name>/SKILL.md` with YAML frontmatter: a kebab-case
  `name` matching the directory, and a `description` that says *when* to use it.
- Keep `python scripts/validate.py` green (CI runs it).
- Fill in the PR template, including the AI-assistance disclosure.

## The bar for a good skill

- **Correct delego semantics.** Fail-closed; the evaluation order
  (forbidden → rules → default deny); the invariants (no LLM in the decision
  path, no credential custody, fingerprint + intent binding, single-use
  approvals, an append-only signed audit). Don't describe behaviour delego
  doesn't have.
- **Honest caveats.** Don't oversell — e.g. the audit chain does *not* detect
  truncation of the most recent receipts, and the policy can't see the URL query
  string (until protocol 0.3).
- **Safe instructions.** No destructive or credential-exfiltrating guidance, and
  nothing that bypasses the firewall.
- **A precise `description`.** It drives auto-invocation — specific enough to fire
  on the right requests, not so broad it hijacks unrelated ones.

## AI-assisted contributions

AI assistants are welcome tools, but AI-generated skills get **stricter review**
(they're prompts that run for others). Disclose AI use in the PR template, expect
closer scrutiny, and own every line — "the model wrote it" is not a defence.
Fork + PR + green CI; no fast path.

## License

Apache-2.0. By contributing you agree your contribution is licensed under it.
