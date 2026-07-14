# Architecture

This directory documents the high-level architecture of the homelab.

The goal is to describe how the environment is designed, why major choices were made, and what assumptions future changes depend on. Exact sensitive values are intentionally sanitized because this repository is public.

## Architecture Documents

- [Overview](overview.md) - Overall design, goals, and current operating model.
- [Network](network.md) - Network design, addressing, DNS flows, segmentation, and future VLAN plans.
- [Virtualization](virtualization.md) - Proxmox role, VM strategy, workload layout, backup integration, and platform boundaries.
- [VM Inventory](vm-inventory.md) - Active virtual machines, resources, status, backup maturity, and recovery priority.
- [Storage](storage.md) - Local storage, operational backup design, recovery layers, and future shared storage.
- [Monitoring](monitoring.md) - Three-host metrics, recursive and local DNS probes, dashboards, recovery state, and alerting philosophy.
- [Security](security.md) - Security principles, public documentation boundaries, management authentication, backup protection, and isolation goals.

## Design Principles

- Keep the lab understandable and recoverable.
- Prefer documented, repeatable changes over one-off fixes.
- Separate experimental work from stable infrastructure.
- Avoid publishing secrets, exact private network details, serial numbers, drive identifiers, or personally identifying information.
- Build toward production-style practices without unnecessary complexity.
- Keep summaries synchronized with detailed service, project, ADR, runbook, and change pages.
- State what validation proved and what remained outside the test boundary.

## Current State

The homelab currently includes:

- A Proxmox VE host with internal-only management and TOTP-protected routine and break-glass identities.
- A managed switch and dedicated homelab routing boundary.
- `dns01` providing Pi-hole DNS, local records, filtering, and host metrics.
- `mon01` providing Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Host metrics for `mon01`, `dns01`, and `pve01`.
- Separate recursive and local-record DNS probes for `dns01`.
- Detailed host, service-health, and infrastructure-overview Grafana dashboards.
- A dedicated 5 TB external Proxmox backup target using ext4, UUID-based mounting, backup-only content restriction, and mount-point enforcement.
- Daily snapshot-mode backups for `dns01` and `mon01` with tiered retention.
- A validated isolated `dns01` whole-VM restore path.
- Protected application-level recovery exports and sanitized rebuild documentation.
- Acquired hardware for a future dedicated virtualization server, pending assembly and validation.

The next primary architecture focus is Project 004 reverse proxy and internal HTTPS. Future priorities include new-server validation, power resilience, Proxmox platform and backup monitoring, second-copy backup design, and network segmentation.

## Related Documentation

- [Repository README](../../README.md)
- [Documentation Style Guide](../../DOCS_STYLE.md)
- [Security Policy](../../SECURITY.md)
- [Projects](../projects/)
- [Architecture Decision Records](../decisions/)
- [Infrastructure Change Records](../changes/)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)