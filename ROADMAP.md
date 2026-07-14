# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, change records, and ADRs.

## Current Focus

- Begin Project 004 reverse proxy and internal HTTPS implementation.
- Select NGINX Proxy Manager or an equivalent reverse proxy based on documented requirements.
- Define friendly internal service names without exposing private DNS details publicly.
- Select and document the internal certificate-authority and trust-distribution model.
- Implement HTTPS for selected internal services.
- Document certificate issuance, renewal, backup, and recovery.
- Monitor proxy availability and certificate expiration after deployment.
- Export and privately validate the Homelab Infrastructure Overview dashboard.
- Add alerting only after each condition has a clear response and supporting runbook.
- Assemble and validate the acquired X299 virtualization server after Project 004 is complete unless hardware timing justifies an explicitly documented sequencing change.
- Decide the long-term relationship between the ThinkPad host and new server through an ADR.
- Complete Project 005 power resilience, UPS monitoring, and graceful shutdown automation before centralized identity services.
- Begin Project 006 Active Directory only after the new server and power-protection controls are operational.
- Continue maintaining public, sanitized, portfolio-quality documentation after meaningful changes.

## Recently Completed Work

### Project 003: Backup and Recovery

Project 003 delivered:

- Backup-readiness and service-state inventories for `dns01` and `mon01`.
- Protected Pi-hole Teleporter and Grafana dashboard recovery assets.
- A dedicated 5 TB external Proxmox backup target.
- SMART validation and an extended drive self-test.
- ext4 filesystem and persistent UUID-based mounting.
- Proxmox backup-only directory storage with mount-point enforcement.
- Initial successful VM backups for `dns01` and `mon01`.
- A daily backup job using snapshot mode and Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- A successful isolated `dns01` whole-VM restore.
- Validation of Debian boot, filesystem availability, Pi-hole FTL, and Node Exporter.
- A tested Proxmox VM restore runbook.
- ADR-0003 documenting the initial backup architecture.

Remaining backup improvements are operational follow-up rather than Project 003 blockers:

- Monitor backup age, job results, pruning, and capacity.
- Define an actionable failure-notification path.
- Perform an independent `mon01` restore test.
- Add a second failure-domain copy when justified.

### Monitoring Foundation

Project 002 has delivered:

- Dedicated monitoring VM: `mon01`.
- Prometheus metrics collection and PromQL validation.
- Grafana dashboarding.
- Node Exporter host metrics for `mon01`, `dns01`, and `pve01`.
- Linux operating-system monitoring for the Proxmox host without API credentials.
- Recursive DNS monitoring through `dns01` and its upstream resolver.
- Local-record DNS monitoring independent of upstream recursion.
- Homelab Service Health dashboard.
- Homelab Infrastructure Overview with host availability, CPU, memory, filesystem, uptime, recursive DNS, local DNS, and probe-duration panels.
- Prometheus scrape-target troubleshooting documentation based on a real incident.
- Blackbox Exporter configuration validation using rollback and alternate-port preflight testing.

Remaining monitoring work should improve operational coverage and recovery value rather than add tools without a defined purpose.

### Management-Plane Security

- Added a named routine Proxmox administrator.
- Protected routine and root break-glass management identities with TOTP.
- Created independent recovery-key sets.
- Validated system time and clean login paths.
- Preserved physical console as the final recovery path.

## Planned Projects and Milestones

### 1. Project 002: Monitoring and Observability Stack

Operational foundation:

- `mon01`
- Prometheus
- Grafana
- Node Exporter
- Blackbox Exporter
- Host metrics for `mon01`, `dns01`, and `pve01`
- Recursive and local DNS probes
- Service-health and infrastructure-overview dashboards

Remaining improvements:

- Export the infrastructure overview as a private recovery artifact.
- Add Pi-hole-specific application metrics.
- Add Proxmox VM, storage, task, and backup metrics through least-privilege integration.
- Add backup-age and backup-failure monitoring.
- Add alerting after runbooks exist.

### 2. Project 003: Backup and Recovery — Completed

Completed scope:

- Integrated the 5 TB external backup target.
- Configured backup scheduling, retention, and pruning.
- Completed initial backups for core VMs.
- Completed representative isolated restore testing.
- Finalized the operational backup and restore runbooks.
- Added a backup architecture ADR and dated change record.

Future improvements:

- Add backup-health monitoring.
- Independently restore-test `mon01`.
- Evaluate an offline, rotated, off-site, NAS, or Proxmox Backup Server copy.

### 3. Project 004: Reverse Proxy and Internal HTTPS

- Select NGINX Proxy Manager or an equivalent reverse proxy.
- Provide friendly internal hostnames.
- Implement internal HTTPS.
- Define the internal CA and client trust model.
- Document certificate issuance, renewal, revocation, backup, and recovery.
- Avoid placing the proxy in front of services where it creates unnecessary risk or dependency.
- Monitor proxy availability and certificate expiration.
- Add service and disaster-recovery dependencies to current documentation.

### 4. Infrastructure Milestone: New Virtualization Server

Acquired baseline:

- ASRock X299M Extreme4.
- Intel Core i7-7800X.
- 32 GB Crucial DDR4-2133.
- Noctua NH-U12S.
- Existing 500 W power supply and NZXT H510 chassis.
- Two existing 1 TB NVMe devices.
- One reported nonfunctional inner DIMM slot.

Required work:

- Assemble and inspect the hardware.
- Verify CPU and memory detection.
- Confirm the failed DIMM-slot behavior.
- Test memory stability and temperatures.
- Validate storage health and select a storage layout.
- Install and secure the virtualization platform.
- Integrate monitoring and backup.
- Create an ADR for the production role and migration plan.

### 5. Project 005: Power Resilience and Graceful Shutdown

- Measure idle, normal, startup, and higher-load power consumption.
- Include both virtualization hosts if both remain active.
- Select and install a correctly sized UPS.
- Monitor utility power, battery charge, runtime, load, input voltage, and battery health where supported.
- Integrate UPS metrics and alerts with Prometheus and Grafana.
- Configure orderly guest and Proxmox host shutdown behavior.
- Document power-loss, shutdown, recovery, and battery-maintenance procedures.
- Test and document a controlled utility-power failure and recovery scenario.

### 6. Project 006: Active Directory and Centralized Identity

- Deploy Active Directory Domain Services.
- Centralize identity and authentication.
- Establish administrative access patterns.
- Document dependencies, recovery requirements, security decisions, and maintenance procedures.
- Protect identity services with tested backup and UPS-backed shutdown first.

### 7. Project 007+: Security Engineering Projects

- Wazuh.
- Suricata.
- Zeek.
- Vulnerability management.
- Azure integration.

## Future Ideas

- Containerized service platform.
- Infrastructure-as-code experiments.
- Intrusion detection and prevention project.
- Public documentation site generated from this repository.
- Azure-focused cloud security lab after the local foundation matures.
- Proxmox Backup Server or dedicated storage only when justified by recovery requirements.

## Completed

- Initial repository documentation scaffold.
- Baseline hardware inventory and roles.
- Initial network documentation.
- Virtualization host setup and documentation.
- Project 001: Pi-hole DNS service on `dns01`.
- Project 002 monitoring foundation: Prometheus, Grafana, Node Exporter, Blackbox Exporter, three-host metrics, recursive and local DNS probing, service-health visualization, and a custom infrastructure overview dashboard.
- Project 003: dedicated backup storage, automatic VM backups, tiered retention, and representative restore validation.
- Proxmox administrative authentication hardening with named routine administration, TOTP, recovery keys, and break-glass access.