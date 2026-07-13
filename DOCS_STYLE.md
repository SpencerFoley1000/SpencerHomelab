# Homelab Documentation Standard

This repository documents a production-style homelab that also serves as a public portfolio. Documentation should help future me operate the environment and help reviewers understand the engineering decisions behind it.

## Core Principles

- Write for future me.
- Explain what changed and why it changed.
- Keep content practical, concise, and maintainable.
- Document meaningful infrastructure changes before moving on.
- Prefer architecture, decision-making, validation, and operational clarity over raw configuration dumps.
- Keep indexes, roadmaps, status tables, ADR checklists, recovery inventories, and future-work sections synchronized with detailed pages.

## Public Repository Sanitization

Assume all documentation is public.

Never publish:

- Passwords, tokens, API keys, private keys, recovery codes, cookies, certificates with private material, or license keys.
- TOTP seeds, provisioning QR codes, or authenticator exports.
- Public IP addresses, ISP account information, exact home address details, or personally identifying SSIDs.
- Device serial numbers, asset tags, MAC addresses, or unnecessary exact internal layouts.
- Personal or exact administrative usernames when a placeholder communicates the design.
- Raw service exports, backup archives, private hashes, drive identifiers, or recovery artifacts.

Use placeholders when exact values are unnecessary or sensitive:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PRIVATE_DNS>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<BACKUP_TARGET>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

The `.gitignore` file reduces accidental commits of common local secret and recovery files, but it is not a security boundary. Always review staged changes before committing.

## Service Documentation

Service pages should include, when applicable:

- Purpose
- Lifecycle status
- Technology stack
- Host
- Operating system
- Deployment method
- Dependencies
- Networking
- Storage and state
- Monitoring and its boundaries
- Security considerations
- Backup strategy
- Recovery procedure
- Maintenance notes
- Future improvements

Future-work sections must describe work that is still incomplete. Remove, replace, or check off items after implementation.

## Infrastructure Documentation

Infrastructure pages should include, when applicable:

- Architecture overview
- Hardware involved
- Known limitations
- Network design
- VLANs or segmentation model
- Routing and DNS assumptions
- Virtualization layout
- Storage design
- Backup architecture
- Monitoring
- Security decisions
- Validation requirements

Architecture indexes and summaries must reflect the deployed environment, not only the original plan.

## Hardware Documentation

Hardware pages should distinguish:

- Active infrastructure.
- Acquired but unvalidated hardware.
- Planned hardware.
- Retired or repurposed devices.

Known faults or limitations must be documented honestly. Acquired hardware should not be described as production infrastructure until inspection, stability, thermal, storage, network, monitoring, and backup requirements are validated.

## Runbooks

Runbooks should clearly state their maturity:

- Operational / tested
- Operational checklist
- Baseline checklist
- Draft baseline
- Planned
- Retired

A planned backup or disaster-recovery outline must not be presented as a validated recovery procedure.

Operational runbooks should include:

- Purpose
- Lifecycle and last validation date
- Preconditions and required access
- Safety and security notes
- Procedure
- Validation
- Rollback or recovery
- Documentation requirements
- Related documentation

Recovery runbooks must be updated whenever service dependencies, Prometheus jobs, Blackbox modules, dashboard requirements, or backup methods change.

## Architecture Decision Records

Create an ADR when a decision:

- Introduces or changes a core platform.
- Changes networking, monitoring, storage, backup, power, or security architecture.
- Assigns a production role to new hardware.
- Has meaningful tradeoffs.
- Would be difficult to understand later without context.

Update ADR follow-up checklists as work completes. Use a new ADR when an existing decision is superseded rather than rewriting the original decision as though the earlier context never existed.

## Change Tracking

Every meaningful infrastructure change should update:

- The relevant documentation page.
- `CHANGELOG.md`.
- `ROADMAP.md`, if the change advances or completes planned work.
- An ADR, if the change represents a major technical decision.
- Relevant indexes, recovery inventories, and future-work lists.
- A dated change record when the implementation has meaningful scope, validation, and lessons worth preserving separately.

Historical changelog entries should preserve the state and lessons recorded at that point in time. Current-state summaries should be updated as the environment changes.

## Link Validation

Run the relative Markdown link validator locally after moving, deleting, or renaming documentation:

```bash
python scripts/check-markdown-links.py
```

The validator checks repository-local Markdown links and exits with a non-zero status when a target is missing or a link escapes the repository.

GitHub Actions also runs the validator for documentation pull requests and pushes to `main` through `.github/workflows/docs-validation.yml`.

External URLs, anchor-only links, and image links remain outside the script's current scope and should be reviewed manually when changed.

## Review Checklist

Before merging a meaningful documentation change:

- Confirm status summaries match detailed pages.
- Confirm completed work is removed from future-work lists.
- Confirm recovery inventories include every active service dependency.
- Confirm new or moved pages are present in the correct index.
- Confirm acquired hardware is clearly separated from active infrastructure.
- Confirm sensitive values are sanitized.
- Run the Markdown link validator locally when possible.
- Confirm the GitHub Actions validation result.
- Update the changelog.
- Update the roadmap, ADRs, and change records when applicable.

## Tone

Write professionally without exaggeration. Label experiments and untested recovery procedures clearly. Document failed approaches when they produce useful lessons learned.
