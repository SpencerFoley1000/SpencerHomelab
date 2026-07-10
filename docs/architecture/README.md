# Architecture

This directory documents the high-level architecture of the homelab.

The goal is to describe how the environment is designed, why major choices were made, and what assumptions future changes depend on. Exact sensitive values are intentionally sanitized because this repository is public.

## Architecture Documents

- [Overview](overview.md) - Overall design, goals, and current operating model.
- [Network](network.md) - Network design, addressing approach, segmentation, DNS, and future VLAN plans.
- [Virtualization](virtualization.md) - Proxmox role, VM strategy, and workload layout.
- [VM Inventory](vm-inventory.md) - Active virtual machines, resources, status, and recovery priority.
- [Storage](storage.md) - Local storage, backup assumptions, and future NAS planning.
- [Monitoring](monitoring.md) - Deployed observability stack, monitoring scope, dashboards, and alerting philosophy.
- [Security](security.md) - Security principles, public documentation boundaries, and operational controls.

## Design Principles

- Keep the lab understandable and recoverable.
- Prefer documented, repeatable changes over one-off manual fixes.
- Separate experimental work from stable infrastructure where practical.
- Avoid publishing secrets, private network details, serial numbers, or personally identifying information.
- Build toward production-style practices without over-engineering the environment.

## Current State

The homelab has moved beyond its initial foundation phase and currently includes:

- A Proxmox VE virtualization host.
- A managed switch and dedicated homelab routing boundary.
- `dns01` providing Pi-hole DNS and local records.
- `mon01` providing Prometheus, Grafana, Node Exporter, and Blackbox Exporter monitoring.
- Host-level monitoring for `mon01` and `dns01`.
- Service-level DNS availability monitoring for `dns01`.

The next architecture priorities are backup and recovery, Proxmox monitoring, and future network segmentation.

## Related Documentation

- [Repository README](../../README.md)
- [Documentation Style Guide](../../DOCS_STYLE.md)
- [Security Policy](../../SECURITY.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
