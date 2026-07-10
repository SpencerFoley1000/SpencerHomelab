# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, and ADRs.

## Current Focus

- Stabilize and validate the Project 002 monitoring stack through normal shutdowns, restarts, and extended operation.
- Define a safe and maintainable approach for Proxmox host monitoring.
- Evaluate Pi-hole-specific metrics beyond the existing DNS availability probe.
- Add alerting only after each alert has a clear operational response and supporting runbook.
- Begin Project 003: Backup and Recovery planning, including backup targets, retention, and restore testing.
- Continue updating public, sanitized, portfolio-quality documentation after each meaningful milestone.

## Recently Completed Monitoring Work

Project 002 has delivered a functional host- and service-monitoring foundation:

- Dedicated monitoring VM: `mon01`.
- Prometheus metrics collection and PromQL validation.
- Grafana dashboarding.
- Node Exporter host metrics for `mon01` and `dns01`.
- Multi-host Prometheus scrape targets.
- Blackbox Exporter DNS availability probing for `dns01`.
- Grafana visibility for Linux host metrics and DNS service health.
- A Prometheus scrape-target troubleshooting runbook based on a real configuration incident.

Remaining monitoring work should improve operational coverage and recovery value rather than add tools without a defined purpose.

## Planned Projects

1. Project 002: Monitoring and Observability Stack
   - Current foundation:
     - `mon01`
     - Prometheus
     - Grafana
     - Node Exporter
     - Blackbox Exporter
     - Host metrics for `mon01` and `dns01`
     - DNS availability monitoring
     - DNS service-health dashboard
   - Remaining improvements:
     - Custom Linux host dashboard
     - Pi-hole-specific metrics
     - Proxmox monitoring
     - Alerting after runbooks exist
     - Monitoring configuration backup coverage

2. Project 003: Backup and Recovery
   - Proxmox Backup Server or another documented backup target
   - Backup validation
   - Restore testing
   - Recovery priorities and retention planning

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
- Intrusion detection / prevention project.
- Public documentation site generated from this repository.
- Azure-focused cloud security lab once the local foundation is mature.

## Completed

- Initial repository documentation scaffold.
- Baseline hardware inventory and roles.
- Initial network documentation.
- Virtualization host setup and documentation.
- Project 001: Pi-hole DNS service on `dns01`.
- Project 002 monitoring foundation: Prometheus, Grafana, Node Exporter, Blackbox Exporter, multi-host metrics, DNS availability probing, and DNS service-health visualization.
