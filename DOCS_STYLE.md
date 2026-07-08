# Homelab Documentation Standard

This repository documents a production-style homelab that also serves as a public portfolio. Documentation should help future me operate the environment and help reviewers understand the engineering decisions behind it.

## Core Principles

- Write for future me.
- Explain what changed and why it changed.
- Keep content practical, concise, and maintainable.
- Document meaningful infrastructure changes before moving on.
- Prefer architecture, decision-making, and operational clarity over raw configuration dumps.

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

## Service Documentation

Service pages should include, when applicable:

- Purpose
- Technology stack
- Host
- Operating system
- Deployment method
- Dependencies
- Networking
- Storage
- Backup strategy
- Recovery procedure
- Security considerations
- Maintenance notes
- Future improvements

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

## Change Tracking

Every meaningful infrastructure change should update:

- The relevant documentation page.
- `CHANGELOG.md`.
- `ROADMAP.md`, if the change advances or completes planned work.
- An ADR, if the change represents a major technical decision.

## Tone

Write professionally without exaggeration. Label experiments clearly. Document failed approaches when they produce useful lessons learned.
