# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, and ADRs.

## Current Focus

- Complete Project 003 backup implementation when the external HDD is available.
- Mount and register the backup target in Proxmox.
- Define VM backup scheduling, retention, and recovery priorities.
- Back up `dns01` and `mon01`.
- Perform and document a representative isolated restore test.
- Export and privately validate the Homelab Infrastructure Overview dashboard.
- Add alerting only after each condition has a clear response and supporting runbook.
- Continue maintaining public, sanitized, portfolio-quality documentation after meaningful changes.

## Recently Completed Monitoring Work

Project 002 has delivered a functional host- and service-monitoring foundation:

- Dedicated monitoring VM: `mon01`.
- Prometheus metrics collection and PromQL validation.
- Grafana dashboarding.
- Node Exporter host metrics for `mon01`, `dns01`, and `pve01`.
- Linux operating-system monitoring for the Proxmox host without introducing API credentials.
- Recursive DNS monitoring through `dns01` and its upstream resolver.
- Local-record DNS monitoring independent of upstream recursion.
- Homelab Service Health dashboard.
- Homelab Infrastructure Overview with host availability, CPU, memory, filesystem, uptime, recursive DNS, local DNS, and probe-duration panels.
- Prometheus scrape-target troubleshooting documentation based on a real incident.
- Blackbox Exporter configuration validation using rollback and alternate-port preflight testing.

Remaining monitoring work should improve operational coverage and recovery value rather than add tools without a defined purpose.

## Planned Projects

1. Project 002: Monitoring and Observability Stack
   - Operational foundation:
     - `mon01`
     - Prometheus
     - Grafana
     - Node Exporter
     - Blackbox Exporter
     - Host metrics for `mon01`, `dns01`, and `pve01`
     - Recursive and local DNS probes
     - Service-health and infrastructure-overview dashboards
   - Remaining improvements:
     - Export the new infrastructure dashboard as a private recovery artifact
     - Pi-hole-specific application metrics
     - Proxmox VM, storage, task, and backup metrics through least-privilege integration
     - Alerting after runbooks exist
     - Monitoring configuration backup and restore validation

2. Project 003: Backup and Recovery
   - External Proxmox backup target
   - Backup scheduling and retention
   - Initial backups for core VMs
   - Restore testing
   - Recovery priorities and operational runbooks
   - Backup-health monitoring after jobs exist

3. Project 004: Reverse Proxy and Internal HTTPS
   - NGINX Proxy Manager or equivalent
   - Internal HTTPS
   - Friendly hostnames

4. Project 005: Identity and Authentication
   - LDAP or Active Directory
   - Centralized identity management
   - Administrative access patterns

5. Project 006+: Security Engineering Projects
   - Wazuh
   - Suricata
   - Zeek
   - Vulnerability management
   - Azure integration

## Future Ideas

- Containerized service platform.
- Infrastructure-as-code experiments.
- Intrusion detection and prevention project.
- Public documentation site generated from this repository.
- Azure-focused cloud security lab after the local foundation matures.

## Completed

- Initial repository documentation scaffold.
- Baseline hardware inventory and roles.
- Initial network documentation.
- Virtualization host setup and documentation.
- Project 001: Pi-hole DNS service on `dns01`.
- Project 002 monitoring foundation: Prometheus, Grafana, Node Exporter, Blackbox Exporter, three-host metrics, recursive and local DNS probing, service-health visualization, and a custom infrastructure overview dashboard.
