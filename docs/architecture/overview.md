# Architecture Overview

## Purpose

This document describes the homelab architecture at a high level. It is intended to help future maintainers understand what exists, why it exists, and how the major infrastructure components relate to each other.

The homelab is designed as a production-style learning environment for systems administration, networking, virtualization, automation, monitoring, backup and recovery, and security engineering.

## Current Architecture Summary

The current environment includes:

- A dedicated X299 server running Proxmox VE as the active virtualization host `pve01`.
- A TP-Link TL-SG108E managed switch for wired lab connectivity.
- A GL.iNet Opal router providing a dedicated homelab routing boundary through upstream household Wi-Fi.
- `dns01`, a Debian VM running Pi-hole for internal DNS, local records, DNS filtering, and Node Exporter metrics.
- `mon01`, a Debian VM running Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- `proxy01`, a Debian VM running Docker, NGINX Proxy Manager, and Node Exporter.
- Node Exporter metrics for `mon01`, `dns01`, `proxy01`, and the Proxmox host `pve01`.
- Separate recursive and local-record DNS probes from `mon01` to `dns01`.
- Internal HTTPS probes and certificate-expiration monitoring for proxied Grafana and Pi-hole services.
- Grafana dashboards for detailed host troubleshooting, DNS service health, infrastructure-wide status, internal HTTPS availability, and certificate lifetime.
- A private root CA kept off the proxy and a wildcard service certificate used for `lab.home.arpa` HTTPS endpoints.
- Proxmox management authentication using named routine administration, a protected root break-glass path, TOTP, and independent recovery keys.
- A dedicated 5 TB external Proxmox backup target with ext4, UUID-based mounting, backup-only content restriction, and mount-point enforcement.
- Daily VM backups for `dns01`, `mon01`, and `proxy01` with tiered retention.
- Validated isolated whole-VM restore paths for `dns01` and `proxy01`.
- Protected application-level exports and recovery inventories for infrastructure services.
- A completed hardware migration that preserved the existing `pve01` installation, workloads, backup configuration, and monitoring identity.
- X299 CPU temperature telemetry collected through Node Exporter and Prometheus.

Sensitive implementation details are intentionally generalized. Exact IP addresses, public IP information, SSIDs, serial numbers, drive UUIDs, backup filenames, environment-specific account names, recovery material, and credentials must not be committed.

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
  |-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter
  |-- proxy01: NGINX Proxy Manager, Docker, Node Exporter
  `-- Dedicated external Proxmox backup storage
      |-- Daily dns01 VM backups
      |-- Daily mon01 VM backups
      `-- Daily proxy01 VM backups

Internal service path
  Trusted client
      |-- DNS query --> dns01 / Pi-hole
      `-- HTTPS --> proxy01 --> selected backend service

Protected recovery assets outside Git
  |-- Pi-hole Teleporter export
  |-- Grafana dashboard exports
  |-- Encrypted private PKI material
  `-- Private identifiers and recovery records

Retired server role
  `-- ThinkPad returned to endpoint use after the X299 migration
```

The household network is an upstream dependency, not part of the managed homelab. The Opal creates a separate lab boundary so DNS, routing, monitoring, reverse proxying, certificates, and future segmentation changes can be tested without directly changing the household network.

## Design Goals

- Provide a realistic environment for entry-level IT, systems administration, networking, and security practice.
- Keep infrastructure understandable enough to troubleshoot without relying on memory.
- Document decisions in a way that demonstrates engineering thought process.
- Separate stable infrastructure roles where practical.
- Build gradually without adding complexity that does not solve a documented problem.
- Support tested backup, recovery, monitoring, and security practices.
- Keep public documentation useful without exposing operational secrets.

## Operating Model

The homelab is treated like a small production environment:

- Meaningful changes are documented before they are considered complete.
- Permanent infrastructure changes are reflected in GitHub and the changelog.
- Secrets and personally identifying information are stored outside the repository.
- Experimental services are clearly labeled.
- Important systems have documented validation and recovery expectations.
- Monitoring is used to validate changes and identify capacity constraints.
- Backup maturity distinguishes successful backup jobs from restore-tested recovery.
- Restore documentation states what was proven and what remained outside the test boundary.
- Direct recovery paths are preserved when convenience layers such as reverse proxies are introduced.
- Roadmaps, indexes, ADRs, and future-work lists are synchronized with current implementation.

## Major Components

| Component | Current Role | Documentation |
| --- | --- | --- |
| Network | Provides the routing boundary, switching, DNS path, proxy flows, monitoring flows, and future segmentation foundation | [Network](network.md) |
| Virtualization | Runs infrastructure workloads on the dedicated X299 Proxmox host and records the completed ThinkPad transition | [Virtualization](virtualization.md) |
| Virtual machines | Tracks active VM resources, status, backup maturity, and recovery priority | [VM Inventory](vm-inventory.md) |
| Storage | Provides local VM storage and operational backup and recovery design | [Storage](storage.md) |
| Monitoring | Collects four-host metrics and independently checks DNS, internal HTTPS, and certificate expiration | [Monitoring](monitoring.md) |
| Security | Defines baseline controls, management authentication, private PKI boundaries, isolation goals, and safe public documentation | [Security](security.md) |
| Reverse proxy | Provides internal TLS termination and hostname-based routing for selected service UIs | [NGINX Proxy Manager](../services/nginx-proxy-manager.md) |

## Current Assumptions

- The lab depends on existing household connectivity for internet access.
- The GL.iNet Opal is sufficient for the current routing boundary but may not meet future segmentation requirements.
- Proxmox is the active virtualization platform.
- Foundational services use stable addressing and sanitized public placeholders.
- `dns01`, `mon01`, and `proxy01` have daily VM backup coverage.
- `dns01` and `proxy01` have representative isolated restore tests; `mon01` has not been independently restored.
- The directly attached backup disk is not immutable, offline, or off-site.
- Dedicated VLANs and security-lab isolation are planned but not yet stable architecture.
- Monitoring covers Linux host metrics for four systems, recursive and local DNS checks, and internal HTTPS plus certificate checks.
- The root CA private key is intentionally outside the proxy VM and repository.
- Direct backend access remains available if the reverse proxy fails.
- Proxmox platform state, backup-job health, Pi-hole application metrics, and alerting remain future monitoring work.
- The X299 server is the sole production hypervisor; the ThinkPad is not a failover node.

## Next Architecture Priorities

- Measure power consumption and implement UPS-backed graceful shutdown before centralized identity services.
- Create a second protected root CA key copy in a separate failure domain.
- Add Proxmox platform and backup metrics through a least-privilege design.
- Add a second backup copy in a separate failure domain when justified.
- Record sanitized Proxmox bridge and local-storage layouts.
- Add VLANs and firewall boundaries only after the routing design is understood and recoverable.
- Add service dependency maps as the environment grows.

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
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Project 004: Reverse Proxy and Internal HTTPS](../projects/project-004-reverse-proxy-internal-https.md)
- [Project 005: X299 Virtualization Server](../projects/project-005-x299-virtualization-server.md)
- [Infrastructure Change Records](../changes/)
