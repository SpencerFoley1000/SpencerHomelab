# Spencer Homelab

A production-style homelab used to build practical experience in systems administration, networking, virtualization, automation, monitoring, backup and recovery, and security engineering.

This repository is maintained as both operational documentation and a public portfolio. Sensitive implementation details are intentionally sanitized.

## Goals

- Build a realistic small-scale infrastructure environment.
- Practice enterprise-style documentation and change management.
- Demonstrate troubleshooting, architecture, monitoring, recovery, and security decision-making.
- Develop skills relevant to help desk, systems administration, network administration, cloud, and security engineering roles.

## Current Status

The homelab currently includes:

- A documented Proxmox VE virtualization host, `pve01`.
- Proxmox management authentication using a named routine administrator and protected root break-glass identity, both with TOTP and independent recovery keys.
- A dedicated DNS VM, `dns01`, running Pi-hole for internal DNS, local records, and DNS filtering.
- A dedicated monitoring VM, `mon01`, running Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Node Exporter host metrics for `mon01`, `dns01`, and `pve01`.
- Recursive DNS monitoring through Pi-hole and its configured upstream resolver.
- Local-record DNS monitoring independent of upstream recursion.
- Grafana dashboards for detailed host metrics, DNS service health, and an at-a-glance infrastructure overview.
- Operational troubleshooting documentation based on real configuration incidents.
- Project 003A backup-readiness inventories and protected application-level recovery exports.
- A 5 TB external backup drive acquired for Project 003 and pending Proxmox integration.
- Hardware acquired for a future dedicated virtualization server, pending assembly and validation.

The current primary focus is Project 003 backup implementation and restore testing. Project 004 reverse proxy and internal HTTPS work follows, then the new virtualization server build and Project 005 power-resilience work. Monitoring improvements remain planned for Pi-hole application metrics, Proxmox platform metrics, backup-health monitoring, and actionable alerting.

## Documentation Structure

- [`docs/architecture/`](docs/architecture/) - Infrastructure architecture, service flows, and design boundaries.
- [`docs/hardware/`](docs/hardware/) - Sanitized hardware inventory and device roles.
- [`docs/services/`](docs/services/) - Service deployment, validation, security, maintenance, and recovery notes.
- [`docs/runbooks/`](docs/runbooks/) - Repeatable operational and troubleshooting procedures.
- [`docs/projects/`](docs/projects/) - Planned, active, and completed project records.
- [`docs/decisions/`](docs/decisions/) - Architecture Decision Records explaining major technical choices.
- [`docs/changes/`](docs/changes/) - Dated implementation records for meaningful infrastructure changes.
- [`CHANGELOG.md`](CHANGELOG.md) - Chronological record of meaningful infrastructure and documentation changes.
- [`ROADMAP.md`](ROADMAP.md) - Current priorities and future direction.
- [`SECURITY.md`](SECURITY.md) - Public documentation and sanitization policy.
- [`DOCS_STYLE.md`](DOCS_STYLE.md) - Repository documentation standards.

## Public Documentation Notice

This repository is public by design. It avoids publishing secrets, personally identifying information, exact private network details, SSIDs, public IP addresses, serial numbers, recovery artifacts, and other sensitive operational data.

Placeholders such as `<LAN_SUBNET>`, `<HOST_IP>`, `<MON01_IP>`, `<DNS01_IP>`, `<PVE01_IP>`, `<PROXMOX_ADMIN_ACCOUNT>`, `<REDACTED_SSID>`, and `<SECRET_STORED_IN_PASSWORD_MANAGER>` are used where exact values are unnecessary or unsafe to publish.
