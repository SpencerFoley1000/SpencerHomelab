# Architecture Overview

## Purpose

This document describes the homelab architecture at a high level. It is intended to help future maintainers understand what exists, why it exists, and how the major infrastructure components relate to each other.

The homelab is designed as a production-style learning environment for systems administration, networking, virtualization, automation, monitoring, backup and recovery, and security engineering.

## Current Architecture Summary

The current environment includes:

- A Lenovo ThinkPad E16 Gen 1 running Proxmox VE as the active virtualization host.
- A TP-Link TL-SG108E managed switch for wired lab connectivity.
- A GL.iNet Opal router providing a dedicated homelab routing boundary through upstream household Wi-Fi.
- `dns01`, a Debian VM running Pi-hole for internal DNS, local records, DNS filtering, and Node Exporter metrics.
- `mon01`, a Debian VM running Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Node Exporter metrics for `mon01`, `dns01`, and the Proxmox host `pve01`.
- Separate recursive and local-record DNS probes from `mon01` to `dns01`.
- Grafana dashboards for detailed host troubleshooting, DNS service health, and infrastructure-wide status.
- Proxmox management authentication using named routine administration, a protected root break-glass path, TOTP, and independent recovery keys.
- Project 003A recovery inventories and private application-level exports for `dns01` and `mon01`.
- A 5 TB external backup drive awaiting integration as the first dedicated Proxmox backup target.
- Acquired components for a future dedicated virtualization server, awaiting assembly and validation.

Sensitive implementation details are intentionally generalized. Exact IP addresses, public IP information, SSIDs, serial numbers, environment-specific account names, recovery material, and credentials must not be committed.

## Current Logical Design

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal router
  |
TP-Link managed switch
  |
Proxmox VE host: pve01
  |-- dns01: Pi-hole DNS and Node Exporter
  `-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter

Planned additions
  |-- 5 TB external Proxmox backup target
  `-- Future dedicated virtualization server
```

The household network is an upstream dependency, not part of the managed homelab. The Opal creates a separate lab boundary so DNS, DHCP, routing, monitoring, and future segmentation changes can be tested without directly changing the household network.

## Design Goals

- Provide a realistic environment for entry-level IT, systems administration, networking, and security practice.
- Keep infrastructure understandable enough to troubleshoot without relying on memory.
- Document decisions in a way that demonstrates engineering thought process.
- Separate stable infrastructure roles where practical.
- Build gradually without adding complexity that does not solve a documented problem.
- Support tested backup, recovery, monitoring, and security practices as the lab matures.
- Keep public documentation useful without exposing operational secrets.

## Operating Model

The homelab is treated like a small production environment:

- Meaningful changes are documented before they are considered complete.
- Permanent infrastructure changes are reflected in GitHub and the changelog.
- Secrets and personally identifying information are stored outside the repository.
- Experimental services are clearly labeled.
- Important systems have documented validation and recovery expectations.
- Monitoring is used to validate changes and identify capacity constraints.
- Recovery procedures remain labeled draft until a restore succeeds.
- Roadmaps, indexes, ADRs, and future-work lists are synchronized with current implementation.

## Major Components

| Component | Current Role | Documentation |
| --- | --- | --- |
| Network | Provides the routing boundary, switching, DNS path, monitoring flows, and future segmentation foundation | [Network](network.md) |
| Virtualization | Runs infrastructure workloads using Proxmox VE and defines the future server transition | [Virtualization](virtualization.md) |
| Virtual machines | Tracks active VM resources, status, backup maturity, and recovery priority | [VM Inventory](vm-inventory.md) |
| Storage | Provides local VM storage and tracks Project 003 backup and recovery design | [Storage](storage.md) |
| Monitoring | Collects three-host metrics and independently checks recursive and local DNS | [Monitoring](monitoring.md) |
| Security | Defines baseline controls, management authentication, isolation goals, and safe public documentation | [Security](security.md) |

## Current Assumptions

- The lab depends on existing household connectivity for internet access.
- The GL.iNet Opal is sufficient for the current routing boundary but may not meet future segmentation requirements.
- Proxmox is the active virtualization platform.
- Foundational services use static addressing and sanitized public placeholders.
- Project 003A is complete, but protected VM backups and restore testing are not yet complete.
- Dedicated VLANs and security-lab isolation are planned but not yet stable architecture.
- Monitoring covers Linux host metrics for `mon01`, `dns01`, and `pve01`, plus recursive and local DNS service checks.
- Proxmox platform state, Pi-hole application metrics, backup-job health, and alerting remain future monitoring work.
- The future dedicated server is not production infrastructure until hardware, memory, storage, networking, thermals, and stability are validated.

## Next Architecture Priorities

- Integrate the 5 TB backup drive, run initial VM backups, define retention, and complete a representative restore test.
- Complete Project 004 reverse proxy and internal HTTPS work.
- Assemble and validate the future dedicated virtualization server.
- Decide and document whether the new server replaces, supplements, or changes the role of the ThinkPad host.
- Measure power consumption and implement UPS-backed graceful shutdown before centralized identity services.
- Record sanitized Proxmox bridge and storage layouts.
- Add VLANs and firewall boundaries only after the routing design is understood and recoverable.
- Add service dependency maps as the environment grows.
- Create ADRs for the new server role, backup design, power-resilience design, and future segmentation.

## Related Documentation

- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Architecture Decision Records](../decisions/)
