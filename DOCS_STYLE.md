# Homelab Documentation Standard

This repository documents a production-style homelab that also serves as a public portfolio. Documentation should help future me operate the environment and help reviewers understand the engineering decisions behind it.

## Core Principles

- Write for future me.
- Explain what changed and why it changed.
- Keep content practical, concise, and maintainable.
- Document meaningful infrastructure changes before moving on.
- Prefer architecture, decision-making, and operational clarity over raw configuration dumps.
- Keep indexes, roadmaps, status tables, and future-work sections synchronized with detailed service pages.

## Public Repository Sanitization

Assume all documentation is public.

Never publish:

- Passwords, tokens, API keys, private keys, recovery codes, cookies, certificates with private material, or license keys.
- Public IP addresses, ISP account information, exact home address details, or personally identifying SSIDs.
- Device serial numbers, asset tags, or unnecessary exact internal layouts.
- Personal usernames unless intentionally part of the public portfolio.

Use placeholders when exact values are unnecessary or sensitive:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PRIVATE_DNS>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

The `.gitignore` file reduces accidental commits of common local secret files and generated artifacts, but it is not a security boundary. Always review staged changes before committing.

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
- Storage
- Backup strategy
- Recovery procedure
- Monitoring
- Security considerations
- Maintenance notes
- Future improvements

Future-work sections must describe work that is still incomplete. Remove or replace items after they are implemented.

## Infrastructure Documentation

Infrastructure pages should include, when applicable:

- Architecture overview
- Hardware involved
- Network design
- VLANs or segmentation model
- Routing and DNS assumptions
- Virtualization layout
- Storage design
- Backup architecture
- Monitoring
- Security decisions

Architecture indexes and summaries should reflect the deployed environment, not only the original plan.

## Runbooks

Runbooks should clearly state their maturity:

- Operational / tested
- Operational checklist
- Draft baseline
- Planned
- Retired

A planned backup or disaster-recovery outline must not be presented as a validated recovery procedure.

Operational runbooks should include:

- Purpose
- Preconditions and required access
- Safety notes
- Procedure
- Validation
- Rollback or recovery
- Related documentation

## Architecture Decision Records

Create an ADR when a decision:

- Introduces a core platform or dependency.
- Changes networking, monitoring, storage, backup, or security architecture.
- Has meaningful tradeoffs.
- Would be difficult to understand later without context.

Update ADR follow-up checklists as work is completed.

## Change Tracking

Every meaningful infrastructure change should update:

- The relevant documentation page.
- `CHANGELOG.md`.
- `ROADMAP.md`, if the change advances or completes planned work.
- An ADR, if the change represents a major technical decision.
- Relevant indexes and future-work lists.

Historical changelog entries should preserve the state and lessons recorded at that point in time. Current-state summaries should be updated as the environment changes.

## Link Validation

Run the relative Markdown link validator after moving, deleting, or renaming documentation:

```bash
python scripts/check-markdown-links.py
```

The validator checks repository-local Markdown links and exits with a non-zero status when a target is missing or a link escapes the repository.

External URLs, anchor-only links, and image links are outside the script's current scope and should be reviewed manually when changed.

## Review Checklist

Before merging a meaningful documentation change:

- Confirm status summaries match detailed service pages.
- Confirm completed work is removed from future-work lists.
- Confirm new or moved pages are present in the correct index.
- Confirm sensitive values are sanitized.
- Run the Markdown link validator.
- Update the changelog.
- Update the roadmap or ADRs when applicable.

## Tone

Write professionally without exaggeration. Label experiments clearly. Document failed approaches when they produce useful lessons learned.
