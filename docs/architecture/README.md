# Architecture

This directory documents the high-level architecture of the homelab.

The goal is to describe how the environment is designed, why major choices were made, and what assumptions future changes depend on. Exact sensitive values are intentionally sanitized because this repository is public.

## Architecture Documents

- [Overview](overview.md) - Overall design, goals, and current operating model.
- [Network](network.md) - Network design, addressing approach, segmentation, and future VLAN plans.
- [Virtualization](virtualization.md) - Proxmox role, VM/container strategy, and host layout.
- [Storage](storage.md) - Local storage, backup assumptions, and future NAS planning.
- [Monitoring](monitoring.md) - Observability goals, planned monitoring stack, and alerting philosophy.
- [Security](security.md) - Security principles, public documentation boundaries, and operational controls.

## Design Principles

- Keep the lab understandable and recoverable.
- Prefer documented, repeatable changes over one-off manual fixes.
- Separate experimental work from stable infrastructure where practical.
- Avoid publishing secrets, private network details, serial numbers, or personally identifying information.
- Build toward production-style practices without over-engineering the first version of the lab.

## Current State

The homelab is in its early foundation phase. Initial hardware, switching, and virtualization work are being documented before higher-level services are added.

## Related Documentation

- [Repository README](../../README.md)
- [Documentation Style Guide](../DOCS_STYLE.md)
- [Security Policy](../../SECURITY.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
