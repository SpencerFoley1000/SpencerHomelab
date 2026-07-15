# Roadmap

This roadmap tracks planned homelab work at a high level. Detailed implementation notes belong in project pages, service pages, runbooks, change records, and ADRs.

## Current Focus

- Assemble and validate the acquired X299 virtualization server.
- Verify CPU, memory, thermals, storage, network connectivity, and the reported failed DIMM slot.
- Decide the long-term relationship between the ThinkPad host and new server through an ADR.
- Integrate the future server with monitoring and backup only after local validation passes.
- Complete Project 005 power resilience, UPS monitoring, and graceful shutdown automation before centralized identity services.
- Measure combined power consumption before final UPS sizing.
- Export and privately validate the updated Homelab Infrastructure Overview dashboard.
- Create a second encrypted or offline root CA private-key copy in a separate failure domain.
- Add alerting only after each condition has a clear response and supporting runbook.
- Begin Project 006 Active Directory only after the new server and power-protection controls are operational.
- Continue maintaining public, sanitized, portfolio-quality documentation after meaningful changes.

## Recently Completed Work

### Project 004: Reverse Proxy and Internal HTTPS

Project 004 delivered:

- Dedicated reverse-proxy VM: `proxy01`.
- Debian 13, QEMU Guest Agent, Node Exporter, Docker Engine, and Docker Compose.
- NGINX Proxy Manager with persistent state.
- Friendly `lab.home.arpa` service names through Pi-hole.
- Internal HTTPS for Grafana and Pi-hole administration.
- An encrypted private root CA key kept off the proxy.
- A wildcard service certificate for `*.lab.home.arpa` and `lab.home.arpa`.
- Trusted root CA installation on Windows and `mon01`.
- HTTP-to-HTTPS redirects and a Pi-hole root-path redirect.
- `proxy01` host metrics.
- Blackbox HTTPS and certificate-expiration monitoring.
- Grafana panels for HTTPS availability and certificate days remaining.
- Daily Proxmox backup coverage.
- A successful isolated whole-VM restore of `proxy01`.
- NGINX Proxy Manager service documentation, certificate lifecycle runbook, ADR-0004, and a dated completion record.

Remaining improvements are follow-up hardening rather than Project 004 blockers:

- Create a second protected root CA key copy.
- Define a formal renewal calendar and ownership process.
- Add certificate-expiration alerts after notification routing exists.
- Restrict proxy administration through future segmentation.
- Re-evaluate wildcard certificates as the service count grows.

### Project 003: Backup and Recovery

Project 003 delivered:

- Backup-readiness and service-state inventories for `dns01` and `mon01`.
- Protected Pi-hole Teleporter and Grafana dashboard recovery assets.
- A dedicated 5 TB external Proxmox backup target.
- SMART validation and an extended drive self-test.
- ext4 filesystem and persistent UUID-based mounting.
- Proxmox backup-only directory storage with mount-point enforcement.
- Daily VM backups using snapshot mode and Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- A successful isolated `dns01` whole-VM restore.
- A tested Proxmox VM restore runbook.
- ADR-0003 documenting the initial backup architecture.

Project 004 extended the same backup design to `proxy01` and completed a second isolated restore test.

Remaining backup improvements:

- Monitor backup age, job results, pruning, and capacity.
- Define an actionable failure-notification path.
- Perform an independent `mon01` restore test.
- Add a second failure-domain copy when justified.

### Monitoring Foundation

Project 002 has delivered:

- Dedicated monitoring VM: `mon01`.
- Prometheus metrics collection and PromQL validation.
- Grafana dashboarding.
- Node Exporter host metrics for `mon01`, `dns01`, `pve01`, and `proxy01`.
- Linux operating-system monitoring for the Proxmox host without API credentials.
- Recursive DNS monitoring through `dns01` and its upstream resolver.
- Local-record DNS monitoring independent of upstream recursion.
- Internal HTTPS and certificate-expiration monitoring through `proxy01`.
- Homelab Service Health dashboard.
- Homelab Infrastructure Overview with host, DNS, HTTPS, and certificate panels.
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
- Four-host metrics
- Recursive and local DNS probes
- Internal HTTPS and certificate probes
- Service-health and infrastructure-overview dashboards

Remaining improvements:

- Refresh the infrastructure overview private recovery export.
- Add Pi-hole-specific application metrics.
- Add Proxmox VM, storage, task, and backup metrics through least-privilege integration.
- Add backup-age and backup-failure monitoring.
- Add alerting after runbooks and notification routing exist.

### 2. Project 003: Backup and Recovery — Completed

Completed scope:

- Integrated the 5 TB external backup target.
- Configured backup scheduling, retention, and pruning.
- Completed backup coverage for `dns01`, `mon01`, and later `proxy01`.
- Completed representative isolated restore testing for `dns01` and `proxy01`.
- Finalized operational backup and restore runbooks.
- Added a backup architecture ADR and dated change record.

Future improvements:

- Add backup-health monitoring.
- Independently restore-test `mon01`.
- Evaluate an offline, rotated, off-site, NAS, or Proxmox Backup Server copy.

### 3. Project 004: Reverse Proxy and Internal HTTPS — Completed

Completed scope:

- Selected and deployed NGINX Proxy Manager.
- Added friendly internal hostnames.
- Implemented internal HTTPS.
- Defined the private CA and client trust model.
- Documented certificate issuance, renewal, replacement, backup, and recovery.
- Preserved direct backend and Proxmox recovery paths.
- Monitored proxy host availability, HTTPS endpoints, and certificate expiration.
- Added backup coverage and completed isolated restore validation.

Future improvements:

- Add a second protected root CA key copy.
- Add actionable certificate alerts.
- Introduce future segmentation and narrower firewall policy.
- Evaluate per-service certificates and configuration automation when justified.

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
- Project 002 monitoring foundation: Prometheus, Grafana, Node Exporter, Blackbox Exporter, four-host metrics, DNS and internal HTTPS probing, certificate metrics, service-health visualization, and a custom infrastructure overview dashboard.
- Project 003: dedicated backup storage, automatic VM backups, tiered retention, and representative restore validation.
- Project 004: reverse proxy, friendly internal DNS, private-CA HTTPS, monitoring, backup, and restore validation.
- Proxmox administrative authentication hardening with named routine administration, TOTP, recovery keys, and break-glass access.
