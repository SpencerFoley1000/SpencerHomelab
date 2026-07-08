# Spencer Homelab

A production-style homelab used to build practical experience in systems administration, networking, virtualization, automation, monitoring, and security engineering.

This repository is maintained as both operational documentation and a public portfolio. Sensitive implementation details are intentionally sanitized.

## Goals

- Build a realistic small-scale infrastructure environment.
- Practice enterprise-style documentation and change management.
- Demonstrate troubleshooting, architecture, and security decision-making.
- Develop skills relevant to help desk, systems administration, network administration, and security engineering roles.

## Documentation Structure

- [`docs/architecture/`](docs/architecture/) - Core infrastructure architecture and design notes.
- [`docs/hardware/`](docs/hardware/) - Sanitized hardware inventory and device roles.
- [`docs/services/`](docs/services/) - Service documentation and deployment notes.
- [`docs/runbooks/`](docs/runbooks/) - Repeatable operational procedures.
- [`docs/projects/`](docs/projects/) - Planned, active, and completed project notes.
- [`docs/decisions/`](docs/decisions/) - Architecture Decision Records explaining major technical choices.
- [`CHANGELOG.md`](CHANGELOG.md) - Chronological record of meaningful changes.
- [`ROADMAP.md`](ROADMAP.md) - Current project direction and future improvements.
- [`SECURITY.md`](SECURITY.md) - Public documentation and sanitization policy.

## Public Documentation Notice

This repository is public by design. It avoids publishing secrets, personally identifying information, private network details, exact SSIDs, public IP addresses, serial numbers, and other sensitive operational data.

Placeholders such as `<LAN_SUBNET>`, `<HOST_IP>`, `<REDACTED_SSID>`, and `<SECRET_STORED_IN_PASSWORD_MANAGER>` are used where exact values are unnecessary or unsafe to publish.

## Current Status

Initial documentation scaffold created. Detailed implementation documentation will be added as the homelab is built and modified.
