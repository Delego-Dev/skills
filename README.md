# delego skills

Claude Code **skills** for working with [delego](https://github.com/Delego-Dev/delego)
— the policy & audit firewall for agent actions. Skills are the *interactive*
surface: you drive them in a Claude Code session to set delego up, write a policy,
triage approvals, and read the audit trail.

## Quick start

```bash
# in your project: clone the skills into the folder Claude Code reads
git clone https://github.com/Delego-Dev/skills .claude/skills
```

Skills hot-load (no restart). Then, in Claude Code, run **`/delego-init`** — it
installs delego, creates the firewall home, wires the MCP server, and verifies.
That's the whole setup.

| Skill | Invoke | Use it to… |
|---|---|---|
| `delego-init` | `/delego-init` | Install delego, create a project-scoped firewall home + keys, wire the MCP server into `.mcp.json`, and verify. |
| `delego-policy-drafter` | `/delego-policy-drafter` | Draft or harden a `policy.yaml` from what your agent should/shouldn't do — schema-correct, fail-closed, footguns covered. |
| `delego-approval-triage` | `/delego-approval-triage` | Review pending approvals, sanity-check each against intent, and approve/deny. |
| `delego-audit-explainer` | `/delego-audit-explainer` | Verify the signed audit chain and explain what the agent did and why. |

For autonomous **review** (policy/broker reviewers, audit investigator) see the
companion [agents](https://github.com/Delego-Dev/agents) repo.

## Setup (Claude Code)

Claude Code discovers skills **one level deep** at `.claude/skills/<name>/SKILL.md`.
The skill directories live at this repo's root, so the simplest install is to
clone it straight into `.claude/skills/`:

```bash
cd your-project
git clone https://github.com/Delego-Dev/skills .claude/skills
```

Skills **hot-load** — available immediately, no restart. Update with
`git -C .claude/skills pull`. (The repo's `README`, `scripts/`, etc. sit alongside
the skill dirs and are ignored by skill discovery.)

**Already have a `.claude/skills/`?** A nested clone won't be found (skills are one
level deep), so keep this repo separate and symlink each skill in:

```bash
git clone https://github.com/Delego-Dev/skills .claude/delego-skills
.claude/delego-skills/install.sh        # symlinks each skill into .claude/skills/
```

## Invoke

Type the slash command, optionally with a hint:

```
/delego-init
/delego-policy-drafter   our agent reads GitHub issues and posts comments; nothing else
/delego-approval-triage
/delego-audit-explainer   why was the transfer denied?
```

Claude will also invoke a skill on its own when your request matches its
`description` — e.g. "set up delego in this repo" triggers `delego-init`.

## Typical flow

1. `/delego-init` — stand up delego + the MCP server in this project.
2. `/delego-policy-drafter` — write the policy for your agent.
3. Review it with the **delego-policy-reviewer** agent (from the
   [agents](https://github.com/Delego-Dev/agents) repo).
4. At runtime: `/delego-approval-triage` to decide parked actions, and
   `/delego-audit-explainer` to read the signed trail.

## Contributing

Each skill is a directory with a `SKILL.md` (YAML frontmatter: kebab-case `name`
matching the directory, plus a `description` that says *when* to use it).
`python scripts/validate.py` (run in CI) checks every skill. PRs welcome — fork
and open one.

## Roadmap

Planned skills: a broker-adapter scaffolder (generate a `BrokerAdapter` for your
vault/proxy), a policy-from-traffic drafter (infer a starting policy from request
logs), and a deny-explainer ("why was X denied, and what's the safe policy
change?").

## License

Apache-2.0. Built for [delego](https://github.com/Delego-Dev/delego); see the
[wire specification](https://github.com/Delego-Dev/specification).
