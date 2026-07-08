# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, and ADRs.

## Current Focus

- Project 002: Monitoring and Observability Stack.
- Deploy a dedicated monitoring VM named `mon01`.
- Learn monitoring fundamentals before adding dashboards and alerting.
- Build host and service visibility for Proxmox, `dns01`, and `mon01`.
- Continue updating public, sanitized, portfolio-quality documentation as each milestone is completed.

## Planned Projects

1. Project 002: Monitoring and Observability Stack
   - `mon01`
   - Prometheus
   - Grafana
   - Node Exporter
   - Host metrics
   - DNS/service health checks

2. Project 003: Backup and Recovery
   - Proxmox Backup Server
   - Backup validation
   - Restore testing

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
