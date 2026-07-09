# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, and ADRs.

## Current Focus

- Stabilize and validate the Project 002 monitoring foundation.
- Confirm the monitoring stack survives normal shutdowns, restarts, and overnight operation.
- Add DNS-specific availability checks after host-level monitoring is confirmed stable.
- Begin planning Project 003: Backup and Recovery.
- Continue updating public, sanitized, portfolio-quality documentation as each meaningful milestone is completed.

## Recently Completed Foundation Work

Project 002 has delivered the first functional monitoring foundation:

- Dedicated monitoring VM: `mon01`.
- Prometheus metrics collection.
- Grafana dashboarding.
- Node Exporter host metrics for `mon01` and `dns01`.
- Multi-host Prometheus scrape targets.
- Grafana visibility for both monitored Linux hosts.

Remaining monitoring work should focus on service-level checks and operational maturity rather than adding more host metrics for their own sake.

## Planned Projects

1. Project 002: Monitoring and Observability Stack
   - Current foundation:
     - `mon01`
     - Prometheus
     - Grafana
     - Node Exporter
     - Host metrics for `mon01` and `dns01`
   - Remaining improvements:
     - DNS/service health checks
     - Custom Grafana dashboard
     - Pi-hole metrics
     - Proxmox monitoring
     - Alerting after runbooks exist

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
- Project 002 monitoring foundation: Prometheus, Grafana, and Node Exporter host metrics for `mon01` and `dns01`.
