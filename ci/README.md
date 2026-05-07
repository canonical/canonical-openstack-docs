# Documentation Testing Framework

## Purpose

The goal is to ensure that every command shown in our documentation matches the software.
Each tutorial or how-to snippet contains **both display and execution blocks**:

- `[docs-view:<name>]` — what appears in the rendered documentation (human-readable example)
- `[docs-exec:<name>]` — what CI executes (machine-runnable equivalent)

Both appear in the same `.task.sh` snippet file, so you only maintain one source of truth.

---

## Block Types

### `[docs-view:<name>]` — for rendered docs
Used with the Sphinx `literalinclude` directive.
Contains clean, readable shell commands.

Example:
```bash
# [docs-view:enable-secrets]
sunbeam enable secrets
# [docs-view:enable-secrets-end]
```

### `[docs-exec:<name>]`
Used for **execution** in CI or local validation runs.
It can include wrappers, environment variables, or anything needed to actually make it work.

Example:
```bash
# [docs-exec:enable-secrets]
sg snap_daemon 'sunbeam enable secrets'
# [docs-exec:enable-secrets-end]
```

> The `docs-view` block is what appears in the docs.
> The `docs-exec` block is what actually runs — but they should mirror each other closely.

## Creating or Editing a Snippet

Create a new file like `how-to/snippets/secrets.task.sh`:


```bash
# [docs-view:enable-secrets]
sunbeam enable secrets
# [docs-view:enable-secrets-end]

# [docs-exec:enable-secrets]
sg snap_daemon 'sunbeam enable secrets'
# [docs-exec:enable-secrets-end]

# [docs-view:disable-secrets]
sunbeam disable secrets
# [docs-view:disable-secrets-end]

# [docs-exec:disable-secrets]
sg snap_daemon 'sunbeam disable secrets'
# [docs-exec:disable-secrets-end]
```

**Rules**
- Use `# [docs-exec:<name>]` … `# [docs-exec:<name>-end]` for every runnable block.
- Blocks must not overlap or nest.
- Keep commands non-interactive and idempotent where possible.

---

## Including `[docs-view]` Blocks in RST Files

To include a `docs-view` block in the rendered documentation, use `literalinclude` with `start-after` and `end-before` markers:

```rst
.. literalinclude:: ../snippets/ldap.task.sh
   :language: bash
   :start-after: [docs-view:enable-ldap]
   :end-before:  [docs-view:enable-ldap-end]
```

**Tips**
- Always point to your `*.task.sh` file in the appropriate `snippets/` directory.
- Make sure your markers (`[docs-view:NAME]` and `[docs-view:NAME-end]`) match exactly.
- Sphinx will automatically include only the lines between those markers.

---

## Declaring Dependencies

If one snippet must run after another (e.g., a feature enable depends on sunbeam being deployed), add a `# @depends:` line near the top pointing to the prerequisite `*.task.sh` script:

```bash
# @depends: tutorial/snippets/get-started-with-openstack.task.sh
```

**Notes**
- Colon after `@depends` is **required**.
- Paths must be **repo-relative**.
- Multiple dependencies are allowed (one per line).
- The selector resolves them such that dependencies always appear **before** dependents in the plan.

---


## CI Workflows

There are two workflows using this system:

### 1. **Documentation Functional Testing**
- Triggers when `*.task.sh` files change.
- Uses the selector to build `plan.txt`.
- Runs the runner in dry-run mode to verify parsing and order.
- Artifacts: `plan.txt`, `changed_snippets.txt`, `run.log`.

### 2. **Documentation Unit Tests**
- Triggers when `ci/**` changes.
- Runs `pytest` on the selector/runner themselves.

---

## Adding Certificates, DNS, or Other Setup

If a how-to requires additional setup (e.g., certificates, DNS records), wrap those commands in their own `[docs-exec:*]` blocks inside the same `.task.sh` file:

```bash
# [docs-exec:generate-cert]
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout /tmp/demo.key -out /tmp/demo.crt \
  -subj "/CN=demo.internal" -days 365
# [docs-exec:generate-cert-end]
```

These commands will appear in the printed (or executed) plan just like any other snippet.