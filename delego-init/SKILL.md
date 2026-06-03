---
name: delego-init
description: Initialize delego — the policy & audit firewall for agent actions — in the current project. Installs the package, creates a project-scoped firewall home with signing keys and a starter policy, wires the delego MCP server into .mcp.json, optionally installs the delego skills and review agents, and verifies the setup. Use when the user wants to "set up delego", "add delego to this project", or "initialize the delego firewall / MCP".
---

# delego-init

Set up [delego](https://github.com/Delego-Dev/delego) in this project so an
agent's actions are authorised against a deterministic policy, sensitive ones are
parked for human approval, and every decision lands in a signed audit trail —
all *before* any credential is used.

## Say this first
delego authorises an agent's **declared** action; it is only a real control when
the credential is reachable **solely** through a broker the agent can't bypass.
If the agent also has raw network/shell access, delego is advisory. Make sure the
user understands that before relying on it.

Require Python ≥ 3.10.

## Steps

1. **Scope.** Confirm the project root. State that state lives under
   `.claude/.delego/` (Ed25519 signing key + ledger + approvals), kept out of git.

2. **Install delego with the MCP extra** into the project's environment:
   ```bash
   python3 -m venv .venv 2>/dev/null || true
   .venv/bin/pip install -U "delego[mcp]"
   ```
   (Use the project's existing venv / uv / poetry env if it has one. The `[mcp]`
   extra is required for the server — `mcp` is not a core dependency.)

3. **Initialise the firewall home** (project-scoped):
   ```bash
   .venv/bin/delego --home .claude/.delego init
   ```
   Creates the signing keypair, an example policy, and a `.gitignore` that keeps
   the private key, ledger, approvals, and `*.lock` out of git. Idempotent — it
   won't overwrite an existing key or policy.

4. **Wire the MCP server** into `.mcp.json` at the project root (merge, do not
   clobber an existing file). Resolve **absolute** paths first so it works
   regardless of the server's working directory:
   ```json
   {
     "mcpServers": {
       "delego": {
         "type": "stdio",
         "command": "<ABS path>/.venv/bin/delego-mcp",
         "args": [],
         "env": { "DELEGO_HOME": "<ABS path>/.claude/.delego" }
       }
     }
   }
   ```

5. **Draft a real policy.** Offer to run the **delego-policy-drafter** skill to
   write a policy for this project's agent. Never leave `default` as anything but
   `deny`. (Keep the example policy only as a placeholder.)

6. **(Optional) install the authoring + review toolkit.** If the user wants it:
   - skills → clone https://github.com/Delego-Dev/skills and run its
     `install.sh` (symlinks each skill into `.claude/skills/`).
   - agents → clone https://github.com/Delego-Dev/agents and run its
     `install.sh` (symlinks each agent into `.claude/agents/`).

7. **Verify**:
   ```bash
   .venv/bin/delego --home .claude/.delego policy   # show the loaded policy
   .venv/bin/delego --home .claude/.delego verify   # check the audit chain
   ```
   Report both.

8. **Restart Claude Code** so the new MCP server loads. After restart the agent
   can call `delego_propose_action` / `delego_resolve_action`; the human approves
   with `delego --home .claude/.delego approve <id>` (or the **delego-approval-triage**
   skill).

## Guardrails
- Never commit `.claude/.delego/signing_key.pem`, the ledger, or `*.lock`.
- If `.mcp.json` already has a `delego` server, update it rather than duplicating.
- Re-running this skill is safe.
