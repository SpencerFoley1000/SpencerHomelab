# Architecture

This directory documents the high-level architecture of the homelab.

The goal is to describe how the environment is designed, why major choices were made, and what assumptions future changes depend on. Exact sensitive values are intentionally sanitized because this repository is public.

## Architecture Documents

- [Overview](overview.md) - Overall design, goals, and current operating model.
- [Network](network.md) - Network design, addressing approach, DNS flows, segmentation, and future VLAN plans.
- [Virtualization](virtualization.md) - Proxmox role, VM strategy, workload layout, and platform boundaries.
- [VM Inventory](vm-inventory.md) - Active virtual machines, resources, status, backup maturity, and recovery priority.
- [Storage](storage.md) - Local storage, Project 003 recovery assets, backup target planning, and future shared storage.
- [Monitoring](monitoring.md) - Deployed observability stack, three-host metrics, recursive and local DNS probes, dashboards, and alerting philosophy.
- [Security](security.md) - Security principles, public documentation boundaries, management authentication, and isolation goals.

## Design Principles

- Keep the lab understandable and recoverable.
- Prefer documented, repeatable changes over one-off manual fixes.
- Separate experimental work from stable infrastructure where practical.
- Avoid publishing secrets, private network details, serial numbers, or personally identifying information.
- Build toward production-style practices without over-engineering the environment.
- Keep architecture summaries synchronized with detailed service and project pages.

## Current State

The homelab currently includes:

- A Proxmox VE virtualization host with internal-only management access and TOTP-protected routine and break-glass identities.
- A managed switch and dedicated homelab routing boundary.
- `dns01` providing Pi-hole DNS, local records, DNS filtering, and host metrics.
- `mon01` providing Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Host-level metrics for `mon01`, `dns01`, and `pve01`.
- Separate recursive and local-record DNS probes for `dns01`.
- Detailed host, service-health, and infrastructure-overview Grafana dashboards.
- Project 003A recovery inventories and private application-level exports.
- A 5 TB external backup drive pending Proxmox integration.
- Acquired hardware for a future dedicated virtualization server, pending assembly and validation.

The next architecture priorities are backup implementation and restore testing, reverse proxy and internal HTTPS, new-server validation, power resilience, and future network segmentation. Proxmox platform metrics remain future work; Linux host monitoring for `pve01` is already active.

## Related Documentation

- [Repository README](../../README.md)
- [Documentation Style Guide](../../DOCS_STYLE.md)
- [Security Policy](../../SECURITY.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
