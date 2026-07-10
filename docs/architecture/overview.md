# Architecture Overview

## Purpose

This document describes the homelab architecture at a high level. It is intended to help future maintainers understand what exists, why it exists, and how the major infrastructure components relate to each other.

The homelab is designed as a production-style learning environment for systems administration, networking, virtualization, automation, monitoring, backup and recovery, and security engineering.

## Current Architecture Summary

The current environment includes:

- A Lenovo ThinkPad E16 Gen 1 running Proxmox VE as the primary virtualization host.
- A TP-Link TL-SG108E managed switch for wired lab connectivity.
- A GL.iNet Opal router providing a dedicated homelab routing boundary through upstream household Wi-Fi.
- `dns01`, a Debian VM running Pi-hole for internal DNS, local records, and DNS-based blocking.
- `mon01`, a Debian VM running Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Host-level monitoring for `mon01` and `dns01`.
- Service-level DNS availability monitoring for `dns01`.

Sensitive implementation details are intentionally generalized. Exact IP addresses, public IP information, SSIDs, serial numbers, account-specific information, and credentials must not be committed.

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
Proxmox VE host
  |-- dns01: Pi-hole DNS and Node Exporter
  `-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter
```

The household network is an upstream dependency, not part of the managed homelab. The Opal creates a separate lab boundary so DNS, DHCP, routing, and future segmentation changes can be tested without directly changing the household network.

## Design Goals

- Provide a realistic environment for entry-level IT, systems administration, networking, and security practice.
- Keep infrastructure understandable enough to troubleshoot without relying on memory.
- Document decisions in a way that demonstrates engineering thought process.
- Separate stable infrastructure roles where practical.
- Build gradually without adding complexity that does not solve a documented problem.
- Support tested backup, recovery, monitoring, and security practices as the lab matures.

## Operating Model

The homelab is treated like a small production environment:

- Meaningful changes are documented before they are considered complete.
- Permanent infrastructure changes are reflected in GitHub and the changelog.
- Secrets and personally identifying information are stored outside the repository.
- Experimental services are clearly labeled.
- Important systems have documented validation and recovery expectations.
- Monitoring is used to validate changes and identify capacity constraints.

## Major Components

| Component | Current Role | Documentation |
| --- | --- | --- |
| Network | Provides the routing boundary, switching, DNS path, and future segmentation foundation | [Network](network.md) |
| Virtualization | Runs infrastructure workloads using Proxmox VE | [Virtualization](virtualization.md) |
| Virtual machines | Tracks active VM resources, status, and recovery priority | [VM Inventory](vm-inventory.md) |
| Storage | Provides local VM storage and defines future backup requirements | [Storage](storage.md) |
| Monitoring | Collects host metrics and checks DNS service availability | [Monitoring](monitoring.md) |
| Security | Defines baseline controls, isolation goals, and safe public documentation practices | [Security](security.md) |

## Current Assumptions

- The lab depends on existing household connectivity for internet access.
- The GL.iNet Opal is sufficient for the current simple routing boundary but may not meet future segmentation requirements.
- Proxmox is the primary virtualization platform.
- Foundational services use static addressing and sanitized public placeholders.
- Backups are not yet implemented or restore-tested.
- Dedicated VLANs and security-lab isolation are planned but not yet stable architecture.
- Monitoring covers Linux VMs and DNS availability but not yet the Proxmox host, backup jobs, or Pi-hole-specific application metrics.

## Next Architecture Priorities

- Design and test Project 003 backup and recovery.
- Add Proxmox host monitoring through a documented method.
- Record the Proxmox bridge and storage layout using sanitized values.
- Add VLANs and firewall boundaries only after the routing design is understood and recoverable.
- Add service dependency maps as the environment grows.
- Create new ADRs for major monitoring, backup, routing, and segmentation decisions.

## Related Documentation

- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Monitoring Architecture](monitoring.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Architecture Decision Records](../decisions/)
