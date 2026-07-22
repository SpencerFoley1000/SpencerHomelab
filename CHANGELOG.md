# Changelog

This changelog records meaningful infrastructure, documentation, and process changes in reverse chronological order.

## 2026-07-21 - Project 005 X299 Virtualization Server Completion

### Changed

- Assembled and placed the dedicated X299 server into production as `pve01`.
- Installed the Intel Core i7-7800X, 32 GB DDR4, Noctua cooling, and a Radeon R7 350 for physical-console access.
- Migrated the existing Proxmox installation by transferring its 1 TB SATA system SSD from the ThinkPad.
- Preserved the `pve01` identity, VM configuration, backup configuration, administrative authentication, and monitoring labels.
- Returned `dns01`, `mon01`, and `proxy01` to service on the new hardware.
- Confirmed continued access to the dedicated external backup target.
- Validated Node Exporter hardware-monitoring output and `coretemp` CPU temperature metrics.
- Retired the ThinkPad from the production hypervisor role and returned it to endpoint use.
- Documented the accepted nonfunctional DIMM slot as a capacity constraint.
- Added the Project 005 page, ADR-0005, and a dated completion record.
- Renumbered power resilience as Project 006 and Active Directory as Project 007.
- Synchronized repository entry points, roadmap, architecture, hardware, Proxmox, monitoring, project index, and decision index documentation.

### Why

- The initial ThinkPad host had reached practical memory and expansion limits.
- Reusing the validated Proxmox system disk reduced migration risk and avoided an unnecessary rebuild.
- Dedicated console graphics preserve physical recovery access on a CPU without integrated graphics.
- Newly assembled server hardware requires temperature visibility before unattended long-term operation.

### Validation

- Successful POST, console output, CPU detection, and 32 GB memory detection.
- Successful Proxmox boot from the transferred SATA SSD.
- Internal management access and logical `pve01` identity preserved.
- Core VMs and infrastructure services operational.
- Backup target accessible.
- Node Exporter scrape healthy and X299 CPU temperature sensors visible.

### Lessons Learned

- Integrated graphics capability must be checked during server planning rather than assumed.
- Physical host replacement does not require changing a stable logical host identity.
- Boot success is only the first migration gate; services, backups, monitoring, authentication, and thermals also require validation.
- Known hardware faults can be accepted when their impact and operating constraints are explicit.

### Remaining Work

- Complete Project 006 UPS monitoring and graceful shutdown.
- Record server and required network-device power measurements.
- Continue temperature and stability observation under production workloads.
- Assign the available NVMe devices a production role only when justified by a documented storage requirement.

## 2026-07-14 - Project 004 Reverse Proxy and Internal HTTPS Completion

### Changed

- Provisioned `proxy01` as a dedicated Debian 13 reverse-proxy VM.
- Installed QEMU Guest Agent, Node Exporter, Docker Engine, and Docker Compose.
- Deployed NGINX Proxy Manager with persistent application and certificate state under `/opt/nginx-proxy-manager/`.
- Standardized friendly internal service naming on `lab.home.arpa`.
- Added Pi-hole local records for Grafana and Pi-hole administration that resolve to `proxy01`.
- Configured hostname-based proxy routes to Grafana on `mon01` and Pi-hole on `dns01` while preserving native backend authentication and direct recovery access.
- Kept Proxmox management outside the reverse-proxy dependency.
- Generated an encrypted private root CA key on a trusted administrative workstation and kept it off `proxy01`.
- Issued and validated a wildcard certificate for `*.lab.home.arpa` and `lab.home.arpa`.
- Installed the public root CA certificate on trusted Windows and Debian clients.
- Enabled trusted internal HTTPS and HTTP-to-HTTPS redirects for Grafana and Pi-hole.
- Added a narrow Pi-hole root-path rewrite to redirect `/` to `/admin/`.
- Added `proxy01` to the shared Prometheus Node Exporter job with `host="proxy01"` and `role="reverse-proxy"` labels.
- Added the `https_internal` Blackbox Exporter module and `blackbox_https_internal` Prometheus job.
- Confirmed Grafana and Pi-hole HTTPS probes return success and expose certificate-expiration metrics.
- Added Grafana panels for internal HTTPS service availability and certificate days remaining.
- Added `proxy01` to the daily Proxmox backup job.
- Completed a snapshot-mode, Zstandard-compressed backup and isolated whole-VM restore of `proxy01`.
- Validated Debian boot, Docker, QEMU Guest Agent, Node Exporter, NGINX Proxy Manager, expected listeners, local administration response, and persistent proxy and certificate directories.
- Removed the temporary restore VM and reconfirmed production proxy health.
- Added NGINX Proxy Manager service documentation, an internal certificate lifecycle runbook, ADR-0004, and a dated Project 004 completion change record.
- Synchronized repository entry points, architecture pages, VM inventory, monitoring, storage, security, backup, disaster-recovery, service indexes, runbook indexes, roadmap, and project status.

### Why

- Memorized addresses and ports become difficult to operate and explain as the service count grows.
- Internal HTTPS protects administrative sessions and provides realistic certificate-lifecycle experience without public exposure.
- Separating proxy, DNS, and monitoring roles preserves clearer failure domains.
- Keeping the root CA key off the proxy limits the impact of a proxy compromise.
- Host metrics alone do not prove that DNS, TLS, proxy routing, or backend responses are working.
- Backup completion alone does not prove that NGINX Proxy Manager state and imported certificate material can be recovered.
- Direct backend and Proxmox access must remain available when the proxy is unavailable.

### Validation

- `proxy01` hostname, networking, Debian installation, and guest integration validated.
- Docker Engine, Compose, and NGINX Proxy Manager container validated.
- Grafana and Pi-hole names resolve to the proxy through Pi-hole local DNS.
- Grafana and Pi-hole routes return expected application responses.
- Wildcard certificate chain, issuer, validity, and SAN values validated.
- Trusted HTTPS validated from Windows and Debian clients.
- HTTP-to-HTTPS and Pi-hole `/admin/` redirects validated.
- `proxy01` Node Exporter target returns `1` in Prometheus.
- Both internal HTTPS probe series return `probe_success 1`.
- Certificate days remaining is visible in Prometheus and Grafana.
- `proxy01` backup artifact completed successfully.
- Isolated restore reconstructed the VM and locally recovered the proxy workload and service-certificate state.
- The restored VM remained network-isolated and was deleted after testing.

### Lessons Learned

- Verify actual backend addresses before building proxy routes; an assumed address caused an avoidable troubleshooting detour.
- A service can be active and listening while a proxy still fails because the wrong address or port is configured.
- PowerShell aliases `curl` to `Invoke-WebRequest`; `curl.exe` avoids ambiguity during Windows validation.
- Copying prompts and continuation markers between shells creates misleading command-not-found errors.
- Prometheus syntax validation must be paired with target discovery and direct PromQL checks.
- An empty Prometheus result differs from a target returning `0`.
- Grafana query legend syntax and panel Display name syntax are different; `${__field.labels.service}` is appropriate in the panel field.
- Private CAs without CRL or OCSP endpoints can trigger Windows Schannel revocation-status errors even when chain and hostname validation succeed.
- `--ssl-revoke-best-effort` is narrower than disabling certificate validation, while `--insecure` is not an acceptable acceptance test.
- A reverse proxy should remain a convenience and security layer rather than the only recovery path.
- Removing a restored VM's network adapter provides a repeatable way to validate duplicate infrastructure safely.

### Remaining Work

- Create a second encrypted or offline root CA private-key copy in a separate failure domain.
- Define a formal certificate-renewal calendar and ownership process.
- Add actionable certificate-expiration and HTTPS alerts after notification routing and response runbooks exist.
- Export and privately validate the updated Homelab Infrastructure Overview dashboard.
- Restrict proxy administration and monitoring through future segmentation.
- Re-evaluate wildcard certificates if service count or isolation requirements grow.
- Re-test recovery after major Docker, NGINX Proxy Manager, storage, or PKI changes.
- Assemble and validate the acquired X299 virtualization server.

## 2026-07-14 - Project 003 Backup and Recovery Completion

### Changed

- Placed the dedicated 5 TB external backup drive into operational service.
- Confirmed SMART overall health passed and completed an extended SMART self-test without error.
- Replaced the factory NTFS layout with an ext4 filesystem for dedicated Proxmox backup use.
- Configured a persistent filesystem-UUID mount while retaining the exact UUID and device identity privately.
- Registered the drive as Proxmox directory storage restricted to backup artifacts.
- Enabled mount-point enforcement so an absent external disk cannot silently redirect backup writes into the host root filesystem.
- Completed initial snapshot-mode, Zstandard-compressed backups for `dns01` and `mon01`.
- Configured daily backups at 10:00 local time with retention of 7 daily, 4 weekly, and 3 monthly backups.
- Restored `dns01` to a temporary VM without overwriting the active guest.
- Removed the restored VM's network adapter before boot to prevent duplicate address and service conflicts.
- Confirmed the restored Debian guest booted, mounted its filesystem, and reported `pihole-FTL` and Node Exporter active.
- Removed the temporary restored VM after validation.
- Marked Project 003 completed and moved the primary roadmap focus to Project 004 reverse proxy and internal HTTPS.
- Added a tested Proxmox VM restore runbook.
- Added ADR-0003 documenting the direct-attached backup and layered recovery design.
- Added a dated Project 003 completion change record.
- Synchronized repository entry points, storage architecture, VM inventory, hardware inventory, Proxmox service documentation, runbook indexes, project indexes, roadmap, and recovery documentation.

### Why

- Stable infrastructure VMs required scheduled recovery points separate from the active VM datastore.
- A missing removable backup disk must cause visible failure rather than unexpected consumption of the Proxmox root filesystem.
- Tiered retention provides recent and historical recovery points without unlimited full-backup growth.
- A successful backup job is incomplete evidence until a restoration path is exercised.
- Whole-VM backups, portable application exports, configuration inventories, and runbooks solve different recovery problems and provide stronger coverage together.

### Validation

- Drive health: SMART passed.
- Extended drive self-test: completed without error.
- Filesystem: ext4 mounted with expected multi-terabyte usable capacity.
- Proxmox storage: active, backup-only, and mount-point protected.
- Initial backup coverage: `dns01` and `mon01` completed successfully.
- Scheduled job: enabled for both VMs using snapshot mode and Zstandard compression.
- Retention: 7 daily, 4 weekly, and 3 monthly.
- Restore: `dns01` reconstructed under a temporary VM ID on normal VM storage.
- Isolation: restored network adapter removed before startup.
- Guest state: Debian booted; root filesystem present; Pi-hole FTL active; Node Exporter active.
- Cleanup: temporary restore VM deleted after shutdown.

### Lessons Learned

- Positive device identification must precede every destructive disk operation.
- Manufacturer decimal capacity and Linux binary capacity reporting differ as expected.
- SMART health plus an extended self-test provides stronger initial evidence than formatting alone.
- UUID mounting is safer than depending on `/dev/sdX` naming.
- Proxmox mount-point enforcement is an important safeguard for removable backup storage.
- Restore tests should use a different VM ID and network isolation while the production guest remains online.
- Local boot and service state do not prove end-to-end network behavior; validation boundaries must be documented honestly.
- Backup maturity should be recorded per VM: `dns01` is restore-tested, while `mon01` currently has successful backup coverage without an independent restore test.

### Remaining Work

- Observe scheduled job execution and pruning over time.
- Add backup-age, task-failure, and capacity monitoring through a least-privilege Proxmox integration.
- Define an actionable backup-job failure notification path.
- Perform an independent `mon01` restore test when operationally useful.
- Perform a controlled network-connected `dns01` recovery test when duplicate identity risk can be eliminated.
- Export and privately validate the Homelab Infrastructure Overview dashboard.
- Evaluate an offline, rotated, off-site, NAS, or Proxmox Backup Server copy when justified.
- Begin Project 004 reverse proxy and internal HTTPS.

## 2026-07-12 - Proxmox Security Hardening, Hardware Acquisition, and Documentation Synchronization

### Changed

- Hardened the Proxmox management plane with a named routine administrator, a protected `root@pam` break-glass identity, TOTP for both identities, independent recovery keys, NTP validation, and clean-login testing.
- Sanitized the exact routine Proxmox administrator name as `<PROXMOX_ADMIN_ACCOUNT>` in public documentation.
- Added a dated infrastructure change record for the Proxmox authentication milestone.
- Acquired an ASRock X299M Extreme4, Intel Core i7-7800X, 32 GB Crucial DDR4-2133, Noctua NH-U12S, and related components for a future dedicated virtualization server.
- Documented the reported nonfunctional inner DIMM slot and the required local memory, thermal, storage, network, and stability validation gates.
- Documented two existing 1 TB NVMe devices, an existing 500 W power supply, and an NZXT H510 chassis as planned reused components.
- Ordered a 5 TB external hard drive as the first dedicated Project 003 Proxmox backup target.
- Added the future server, backup drive, and planned UPS to the sanitized hardware inventory.
- Added a dedicated future-server build page and required a future ADR before assigning it a production role.
- Updated the roadmap to sequence Project 003 backup implementation, Project 004 reverse proxy and internal HTTPS, new-server validation, the then-numbered Project 005 UPS work, and the then-numbered Project 006 Active Directory work.
- Synchronized repository entry points, architecture pages, virtualization, storage, hardware, VM inventory, Project 003, ADR-0001, service pages, and runbooks with the deployed monitoring and recovery state.
- Updated Project 003 recovery requirements to include `blackbox_dns_local` and `dns_udp_local` so local-record monitoring cannot be silently omitted during rebuild.
- Expanded backup, disaster-recovery, maintenance, and VM-provisioning runbooks while preserving honest planned or unvalidated maturity labels.
- Added dedicated `.gitignore` rules for private exports, recovery artifacts, and backup artifacts.
- Added a GitHub Actions workflow that compiles and runs `scripts/check-markdown-links.py` on documentation pull requests and pushes to `main`.

### Why

- The Proxmox management plane controls every hosted workload and required stronger, recoverable authentication before the lab became more dependent on it.
- The future server introduces meaningful capacity, hardware-fault, migration, storage, and power-design decisions that should be documented before assembly.
- The 5 TB drive changes Project 003 from abstract planning to a concrete pending implementation.
- High-level architecture and recovery pages had drifted behind the detailed monitoring and service documentation.
- Recovery documentation must include every active Prometheus job, Blackbox module, and Grafana dependency.
- Automated link validation reduces the chance that future file moves or new documentation break repository navigation.

### Lessons Learned

- Strong MFA design includes independent recovery and physical-console paths, not only an authenticator application.
- A broad Proxmox Administrator role does not necessarily permit protected root identity operations.
- Exact administrative usernames are unnecessary in a public portfolio when a placeholder communicates the architecture.
- Hardware with a known limitation can still be useful if the defect, validation requirements, and expansion constraints are documented honestly.
- UPS sizing should follow measured combined load rather than assumptions.
- Recovery inventories must be refreshed whenever monitoring jobs, dashboard dependencies, or service configuration change.
- Documentation drift continues to appear first in summaries, ADR checklists, hardware pages, and recovery runbooks.

### Remaining Work

- Receive, inspect, prepare, mount, and register the 5 TB backup target.
- Define backup scheduling, retention, pruning, and capacity thresholds.
- Run initial VM backups for `dns01` and `mon01`.
- Perform and document a representative isolated restore test.
- Export and privately validate the Homelab Infrastructure Overview.
- Assemble and validate the X299 server.
- Create an ADR defining the future relationship between the ThinkPad and X299 server.
- Measure power consumption and implement UPS monitoring and graceful shutdown, now tracked as Project 006.
- Add Proxmox platform metrics and actionable alerts only after least-privilege and response designs exist.

## 2026-07-11 - Infrastructure Overview and Local DNS Monitoring

### Changed

- Created the `Homelab Infrastructure Overview` Grafana dashboard manually.
- Added host availability, CPU utilization, memory utilization, root-filesystem utilization, host uptime, DNS availability, and DNS probe-duration panels.
- Configured the dashboard to display `mon01`, `dns01`, and `pve01` host metrics.
- Added separate Recursive DNS and Local DNS status values to the DNS Availability panel.
- Added the `dns_udp_local` Blackbox Exporter module for an internal A-record query.
- Required the local probe to match an expected answer record instead of accepting `NOERROR` alone.
- Added the `blackbox_dns_local` Prometheus job with `scope="local"`.
- Confirmed both recursive and local DNS probes return `probe_success 1`.
- Validated Prometheus configuration with `promtool` and reloaded the service successfully.
- Updated Blackbox Exporter, Prometheus, Grafana, monitoring architecture, Project 002, roadmap, and changelog documentation.

### Why

- Recursive public-name resolution and local DNS records depend on different components and should be monitored independently.
- A summary dashboard provides faster operational awareness than navigating a large imported dashboard for routine checks.
- Manually built panels demonstrate PromQL understanding and intentional dashboard design.
- Answer-record validation provides stronger evidence than a successful DNS response code alone.

### Lessons Learned

- A Blackbox Exporter module placed at the wrong YAML level can produce an application-schema error even when the file appears structurally readable.
- Restoring a known-good file before troubleshooting reduced monitoring downtime.
- Preflighting Blackbox Exporter on an alternate local port validated the corrected configuration before restarting the live service.
- A new Prometheus job may return an empty vector until its first scrape completes.
- Grafana query reference IDs and user-facing legends are separate; distinct IDs such as `A` and `B` were required to display both DNS series.
- Grafana dashboard v2 threshold values must be numeric JSON values rather than quoted strings.
- Full-width time-series panels improve readability and avoid unnecessary empty dashboard space.

### Remaining Work

- Export the Homelab Infrastructure Overview as Classic JSON.
- Validate and privately inspect the export before treating it as a recovery artifact.
- Add actionable DNS alerts only after response runbooks and notification routing exist.
- Evaluate Pi-hole-specific application metrics.

## 2026-07-10 - Proxmox Host Monitoring Baseline

### Changed

- Installed Node Exporter `1.9.0-1+b4` on `pve01`.
- Confirmed the exporter was active, enabled, serving `/metrics`, and listening on TCP `9100`.
- Verified reachability from `mon01` while the Proxmox firewall was active.
- Determined that no broad firewall rule was required because the trusted monitoring path already worked.
- Added `<PVE01_IP>:9100` to the existing Prometheus `node_exporter` job.
- Applied `host="pve01"` and `role="hypervisor"` labels.
- Validated the Prometheus configuration, reloaded the service, and confirmed the target returned `1`.
- Confirmed Grafana displayed CPU, memory, filesystem, network, and uptime metrics for `pve01`.
- Updated Node Exporter, Prometheus, Proxmox, monitoring architecture, and Project 002 documentation.

### Why

- Hypervisor resource pressure affects every VM in the lab and needs direct visibility.
- Reusing the existing Node Exporter design provided useful Linux host metrics without introducing Proxmox API credentials.
- Testing the actual path before changing firewall policy avoided unnecessary exposure.

### Lessons Learned

- An active firewall does not automatically mean a required connection is blocked; test from the intended source first.
- Piping metric output to `head` may produce `curl: (23)` after the requested lines are successfully displayed.
- Node Exporter provides a safe baseline but cannot report authoritative VM state, storage-pool health, task results, or backup-job status.

### Remaining Work

- Add Proxmox platform metrics through a documented least-privilege exporter or API integration.
- Add backup-job monitoring after Project 003 backup jobs exist.
- Include `pve01` in future capacity-planning and alerting work.

## 2026-07-10 - Project 003A: Backup Readiness and Configuration Inventory

### Changed

- Completed live backup-readiness inventories for `dns01` and `mon01`.
- Verified service runtime state, boot enablement, package versions, systemd unit paths, configuration locations, and storage footprints.
- Created and privately inspected a Pi-hole Teleporter ZIP as a portable application-level recovery artifact.
- Created and privately inspected Node Exporter and Homelab Service Health Grafana dashboard JSON exports.
- Classified Grafana database, plugin, generated-export, and search state by recovery importance.
- Classified Prometheus configuration separately from historical metrics data.
- Documented the Grafana Prometheus data-source recovery mapping while retaining the environment-specific UID privately.
- Added `docs/runbooks/service-config-export.md` for repeatable export creation, integrity checking, sensitivity inspection, and public-documentation handling.
- Updated Project 003, Pi-hole, Grafana, and runbook documentation to reflect the verified recovery assets and remaining restore-validation requirements.
- Validated 51 Markdown files with no broken relative links.

### Why

- Backup jobs should not be configured before the state, dependencies, and recovery priorities of each service are understood.
- Application-level exports provide a portable recovery option when a full VM restore is unavailable or unnecessary.
- Public portfolio documentation must explain recovery design without publishing authentication state, private addressing, lease data, hashes, or environment-specific identifiers.
- Recovery procedures need honest maturity labels so an untested export or draft runbook is not mistaken for a proven backup.

### Lessons Learned

- Archive integrity and valid JSON syntax confirm readability, not successful restoration.
- Configuration importance is not proportional to directory size; replaceable plugin files can outweigh unique operational state.
- Pi-hole Teleporter exports contain sensitive databases, lease data, network identifiers, and authentication-related state and must remain outside Git.
- Grafana dashboard exports may not preserve automatic Prometheus data-source binding.
- Prometheus configuration and job validation are more important for manual recovery than short-term metrics history at the current lab scale.
- Export filenames and formats should be verified from the generated artifact rather than assumed.
- Inspection scripts can classify sensitive content without printing protected values.

### Remaining Work

- Mount and configure the external backup target in Proxmox.
- Define VM backup scheduling and retention.
- Run initial backups for `dns01` and `mon01`.
- Perform and document a representative isolated restore test.
- Expand the backup and disaster-recovery runbooks using implementation and restore-test findings.
- Add a Proxmox VM restore runbook and synchronize the storage architecture after implementation.

## 2026-07-09 - Repository Documentation Audit and Consistency Cleanup

### Changed

- Audited the public repository for stale status text, broken links, misplaced files, unclear lifecycle labels, and documentation inconsistencies.
- Updated the repository README, roadmap, architecture index, architecture overview, network architecture, virtualization architecture, VM inventory, and monitoring architecture to match the deployed environment.
- Replaced the obsolete planned Proxmox placeholder with active platform documentation.
- Added a dedicated Project 001 Pi-hole project summary.
- Reworked the projects index to use numbered project files with lifecycle status recorded in each document.
- Moved the runbook and project templates into their respective documentation directories.
- Updated the runbooks index to distinguish tested procedures, operational checklists, draft baselines, and planned recovery documents.
- Fixed stale or broken links, including the documentation style guide, service template, removed desktop page, and missing QEMU Guest Agent runbook index entry.
- Updated Pi-hole, Node Exporter, Prometheus, and Blackbox Exporter documentation to remove completed future work and clarify monitoring responsibilities.
- Clarified that the current public-name Blackbox DNS probe validates the complete recursive-resolution path rather than Pi-hole alone.
- Added ADR-0002 documenting the Prometheus, Grafana, Node Exporter, and Blackbox Exporter monitoring stack decision.
- Updated ADR-0001 follow-up status and recorded the first capacity review.
- Added a dependency-free relative Markdown link validator under `scripts/check-markdown-links.py`.
- Added `.gitignore` rules for editor files, local secrets, temporary backups, Python artifacts, and future infrastructure state.
- Expanded the documentation standard with lifecycle, synchronization, link-validation, and review requirements.

### Why

- Detailed service pages accurately reflected recent work, but several entry points and indexes still described the pre-monitoring environment.
- Broken links and obsolete placeholders reduce trust in the repository as an operational reference and public portfolio.
- Runbooks must clearly distinguish tested procedures from unvalidated backup and disaster-recovery plans.
- Monitoring documentation should state exactly what each probe proves so future incidents are diagnosed correctly.
- Lightweight validation and ignore rules reduce the chance of repeated link drift or accidental local-file commits.

### Lessons Learned

- Documentation drift usually appears first in summaries, indexes, roadmaps, and future-work lists rather than detailed implementation pages.
- Historical changelog entries should remain unchanged, while current-state pages must be actively synchronized.
- A service probe name can be technically correct but operationally ambiguous if the complete dependency path is not documented.
- Templates are easier to discover and maintain when stored with the documentation type they govern.
- Public portfolio quality depends on consistency and honest maturity labels as much as technical detail.

### Remaining Work

- Run `python scripts/check-markdown-links.py` from a local clone after future file moves or renames.
- Export stable Grafana dashboards after their design matures.
- Add a local-record DNS probe to separate internal DNS health from upstream recursive resolution.
- Implement and validate Project 003 backup and recovery procedures.
- Add Proxmox host monitoring through a documented least-privilege method.

## 2026-07-09 - Prometheus Scrape Configuration Troubleshooting

### Changed

- Troubleshot a Grafana Node Exporter dashboard that stopped showing current host metrics.
- Confirmed the issue was not Grafana by querying Prometheus directly.
- Identified that `up{job="node_exporter"}` returned no data, indicating the `node_exporter` scrape job was missing, renamed, or malformed in Prometheus.
- Restored the Prometheus scrape configuration so `prometheus`, `node_exporter`, and `blackbox_dns` jobs were all present again.
- Confirmed host metrics and DNS probe metrics recovered after the Prometheus configuration was fixed.
- Added `docs/runbooks/prometheus-scrape-target-troubleshooting.md`.
- Updated the runbooks index to include the new Prometheus scrape target troubleshooting runbook.

### Why

- Grafana dashboards depend on Prometheus data, so missing dashboard data should be traced upstream before changing dashboard panels.
- The incident showed that Prometheus configuration can be syntactically valid while still being operationally wrong if expected scrape jobs are missing.
- A repeatable runbook will make future scrape target failures faster to diagnose and safer to recover from.

### Lessons Learned

- Grafana is often the symptom when dashboard data disappears, not the root cause.
- `up{job="node_exporter"}` returning no data is different from returning `0`; no data usually means the job is missing, renamed, or not being scraped.
- `promtool check config` should be paired with PromQL validation after configuration changes.
- Prometheus scrape jobs should be checked with `count by (job, instance) (up)` after edits.
- Back up `/etc/prometheus/prometheus.yml` before adding or changing scrape jobs.

### Remaining Work

- Consider exporting important Grafana dashboards as JSON once the dashboard layout stabilizes.
- Add a more formal Prometheus configuration backup process when Project 003 backup work begins.
- Add alerting only after service checks have clear runbooks.

## 2026-07-09 - Grafana Service Health Dashboard

### Changed

- Created a `Homelab Service Health` dashboard in Grafana.
- Added a `dns01 DNS Availability` stat panel backed by the `blackbox_dns` probe.
- Added a `dns01 DNS Probe Duration` time series panel.
- Added a `dns01 DNS Probe Status` state timeline panel.
- Updated Grafana service documentation to describe the service health dashboard.
- Updated monitoring architecture documentation to reflect DNS probe visualization.
- Updated Project 002 documentation to mark DNS probe dashboarding as active.

### Why

- Prometheus already confirmed DNS availability, but Grafana makes the service state easier to understand at a glance.
- DNS service health should be visible separately from host health because a VM can be online while DNS itself is broken.
- Manually created panels demonstrate understanding of Prometheus metrics and dashboard design instead of relying only on imported dashboards.

### Lessons Learned

- `probe_success` is useful for simple service availability visualization.
- `probe_duration_seconds` adds latency context to a binary up/down signal.
- Separate host-health and service-health dashboards make troubleshooting clearer.
- Building panels manually improves understanding of what each PromQL query is actually showing.

### Remaining Work

- Export important Grafana dashboards as JSON once they are worth preserving as versioned artifacts.
- Add Pi-hole-specific metrics or a DNS-focused exporter.
- Create runbooks before adding DNS-related alerts.
- Add Proxmox monitoring approach.

## 2026-07-09 - DNS Availability Monitoring

### Changed

- Installed Blackbox Exporter on `mon01` using the Debian package repository.
- Added a `dns_udp` probe module for DNS availability checks.
- Validated Blackbox Exporter locally on `localhost:9115`.
- Validated DNS probing against `dns01` with `probe_success 1`.
- Added a Prometheus `blackbox_dns` scrape job for `<DNS01_IP>:53`.
- Confirmed `probe_success{job="blackbox_dns"}` returns `1`.
- Added Blackbox Exporter service documentation under `docs/services/blackbox-exporter.md`.
- Updated monitoring architecture, Prometheus service documentation, Project 002 documentation, and the services index.

### Why

- Host metrics prove that `dns01` is running, but they do not prove that DNS queries are working.
- DNS is foundational infrastructure, so service-level monitoring is necessary before relying on the lab more heavily.
- Blackbox Exporter adds an external-style check from the monitoring system's point of view.
- This creates a cleaner path toward future HTTP, ICMP, TCP, and alerting checks.

### Lessons Learned

- Node Exporter and Blackbox Exporter solve different monitoring problems: host health versus service availability.
- A service can be healthy while only listening locally; `localhost:9115` is acceptable because Prometheus and Blackbox Exporter both run on `mon01`.
- Manual probe validation should happen before adding Prometheus scrape configuration.
- `probe_success` provides a simple service health signal that can later feed dashboards and alerts.
- DNS monitoring should avoid depending on DNS resolution from the same server being monitored, so sanitized static target placeholders are used in documentation.

### Remaining Work

- Add Pi-hole-specific metrics or a DNS-focused exporter.
- Create runbooks before adding DNS-related alerts.
- Add Proxmox monitoring approach.

## 2026-07-09 - mon01 Resource Tuning

### Changed

- Increased `mon01` memory allocation from 2 GB to 3 GB.
- Left `mon01` CPU and disk allocation unchanged.
- Updated `docs/architecture/vm-inventory.md` to reflect the new RAM allocation.
- Updated `docs/projects/project-002-monitoring-observability.md` with the sizing rationale and troubleshooting lesson.

### Why

- Grafana showed `mon01` using roughly 1.55 GB of RAM consistently, with occasional spikes near 1.85 GB.
- `mon01` runs Prometheus, Grafana, and Node Exporter, making it the core monitoring system for the homelab.
- Additional headroom is appropriate before adding more monitoring components such as DNS availability checks or Blackbox Exporter.
- 3 GB provides a safer operating margin without overcommitting the current 16 GB Proxmox host.

### Lessons Learned

- Monitoring infrastructure should be monitored and resized based on observed behavior.
- Linux memory graphs should be interpreted carefully, but sustained pressure near the VM limit is still worth addressing.
- Small resource changes should still be documented because they affect capacity planning and future troubleshooting.

## 2026-07-09 - Project 002: Monitoring Baseline, Node Exporter, Prometheus, Grafana, and dns01 Monitoring

### Changed

- Deployed `mon01` as the dedicated monitoring and observability VM.
- Installed Debian 13.5 (Trixie) as a minimal headless server.
- Configured non-root administration with `sudo`.
- Installed baseline administrative tools and QEMU Guest Agent.
- Validated package repositories, networking, and DNS resolution on `mon01`.
- Installed Node Exporter using the Debian package repository.
- Verified Node Exporter locally with `curl localhost:9100/metrics`.
- Installed Prometheus using the Debian package repository.
- Configured Prometheus to scrape itself on `localhost:9090` and Node Exporter on `localhost:9100`.
- Validated Prometheus target health in the web UI, with both initial scrape targets reporting `UP`.
- Ran initial PromQL validation queries including `up`, `node_memory_MemAvailable_bytes`, and root filesystem availability checks.
- Installed Grafana using the Grafana APT repository.
- Started and validated the `grafana-server` service.
- Configured Grafana to use Prometheus as its first data source.
- Imported a Node Exporter dashboard to validate end-to-end visualization.
- Installed Node Exporter on `dns01`.
- Validated the `dns01` Node Exporter endpoint locally with `curl localhost:9100/metrics`.
- Validated remote scrape reachability from `mon01` to `dns01`.
- Added `dns01` as the first remote Prometheus scrape target under the `node_exporter` job.
- Confirmed Prometheus target health showed the `dns01` target as `UP`.
- Confirmed Grafana can display both `mon01` and `dns01` when using the `node_exporter` job selector.
- Added `mon01` to the VM inventory under `docs/architecture/vm-inventory.md`.
- Updated `dns01` in the VM inventory to reflect monitored host metrics.
- Updated monitoring architecture documentation under `docs/architecture/monitoring.md`.
- Added Node Exporter service documentation under `docs/services/node-exporter.md`.
- Added Prometheus service documentation under `docs/services/prometheus.md`.
- Added Grafana service documentation under `docs/services/grafana.md`.
- Updated Project 002 progress documentation under `docs/projects/project-002-monitoring-observability.md`.
- Added a QEMU Guest Agent troubleshooting runbook under `docs/runbooks/qemu-guest-agent-troubleshooting.md`.

### Why

- Establish monitoring as a dedicated infrastructure role instead of combining it with DNS or the Proxmox host.
- Build the observability stack from the bottom up by exposing metrics before installing Prometheus or Grafana.
- Move from one-time metric inspection to time-series metric collection and dashboard visualization.
- Expand monitoring coverage beyond the monitoring VM itself by adding `dns01`, the first production-style service VM.
- Practice enterprise-style separation of responsibilities, validation, troubleshooting, and documentation.
- Create a foundation for future host metrics, DNS health checks, dashboards, alerting, and capacity planning.

### Lessons Learned

- Node Exporter exposes Linux host metrics through a simple HTTP `/metrics` endpoint.
- Metrics are numerical measurements of system state over time.
- Prometheus scrapes configured targets on an interval and stores metric samples as time-series data.
- Grafana connects to Prometheus as a data source and visualizes PromQL-backed metrics.
- Building the stack layer-by-layer makes troubleshooting easier because each dependency can be validated independently.
- Remote scrape targets should be validated with `curl` from the Prometheus host before Prometheus configuration is changed.
- Scraping `dns01` by static IP avoids making DNS monitoring depend on DNS resolution from the same host being monitored.
- Prometheus target health may briefly show `UNKNOWN` until the first scrape completes.
- Imported Grafana dashboards may assume different Prometheus job names; selecting or adjusting the correct job variable may be required.
- A successful `curl -I localhost:3000` response can validate Grafana even when a port listing is unclear.
- If APT cannot locate a package from a third-party repository, verify the repository file, signing key, and `apt-get update` output.
- QEMU Guest Agent depends on both the guest package and the Proxmox-provided virtio serial device.
- If `/dev/virtio-ports/org.qemu.guest_agent.0` is missing despite `agent: 1` being enabled, a full Proxmox stop/start may be required to recreate the VM hardware channel.
- A guest OS reboot is not always equivalent to a hypervisor-level power cycle.

### Remaining Work

- Build a custom Linux host dashboard for learning and portfolio polish.
- Add DNS availability checks and future Pi-hole metrics.
- Add Proxmox monitoring approach.
- Add alerting only after checks are documented and actionable.
- Add backup coverage for `mon01` once backup infrastructure is deployed.

## 2026-07-08 - Project 001: Pi-hole DNS Service

### Changed

- Deployed the first production-style infrastructure VM, `dns01`.
- Installed Debian 13.5 (Trixie) as a minimal headless server.
- Configured non-root administration with `sudo`.
- Installed and verified the QEMU Guest Agent for Proxmox integration.
- Configured a static IP for the DNS VM on the homelab LAN.
- Installed Pi-hole as the homelab DNS service.
- Selected Cloudflare as the initial upstream DNS provider.
- Added local DNS records for core homelab infrastructure.
- Verified DNS resolution from a separate client.
- Added service documentation for Pi-hole under `docs/services/pihole.md`.
- Added VM inventory documentation under `docs/architecture/vm-inventory.md`.
- Updated network architecture documentation to reflect the GL.iNet Opal as the homelab edge router.
- Updated router documentation to clarify that the household network is an upstream dependency, not managed lab infrastructure.

### Why

- Establish DNS as the first foundational homelab service.
- Provide readable internal names for infrastructure systems instead of relying on memorized IP addresses.
- Create a safer isolated lab design behind the GL.iNet Opal router without affecting the household network.
- Build practical skills in Linux administration, Proxmox VM deployment, static networking, DNS, and troubleshooting.
- Start documenting real services in a portfolio-ready format as soon as they become part of the environment.

### Lessons Learned

- Hardware virtualization may need to be explicitly enabled in firmware before Proxmox can start VMs.
- Debian installation behavior differs depending on whether a root password is configured; `sudo` access may need to be added manually.
- Minimal Debian installs may not include convenience tools such as `curl` by default.
- QEMU Guest Agent behavior depends on both the guest package and the Proxmox VM option being enabled.
- Static IP configuration can succeed while DNS resolution fails if resolver configuration is incomplete.
- Troubleshooting by layer is effective: verify gateway reachability, internet-by-IP, then DNS resolution.
- The GL.iNet Opal topology gives the homelab a useful isolation boundary while still depending on upstream Wi-Fi for internet access.

### Remaining Work

- Configure the GL.iNet Opal DHCP settings to hand out Pi-hole as DNS for homelab clients after stability is validated.
- Add a secondary DNS server before relying on Pi-hole for all homelab clients.
- Export Pi-hole configuration after meaningful DNS changes.
- Add monitoring for DNS availability and query health.
- Add VM backup coverage and restore testing once backup infrastructure is deployed.
- Consider Unbound as a future recursive DNS resolver project.

## 2026-07-07 - Architecture Decision Records

### Changed

- Added the Architecture Decision Records index under `docs/decisions/`.
- Added a standard ADR template.
- Added ADR-0001 documenting the decision to use the Lenovo ThinkPad E16 Gen 1 as the initial Proxmox host.
- Defined ADR naming, status values, and usage guidance.

### Why

- Preserve the reasoning behind meaningful infrastructure decisions.
- Make design tradeoffs clear for future maintenance and portfolio review.
- Establish a repeatable process for documenting future platform, networking, storage, monitoring, and security decisions.

### Lessons Learned

- Architecture decisions are more useful when they document context and tradeoffs, not just the final choice.
- The first Proxmox host decision is significant enough to preserve because it affects cost, power, noise, and growth options.
- ADRs help future readers understand why the lab evolved the way it did.

### Remaining Work

- Add ADRs for future router/firewall decisions.
- Add ADRs for VLAN segmentation when implemented.
- Add ADRs for monitoring, backup, and security platform choices.

## 2026-07-07 - Services Documentation Templates

### Changed

- Expanded the services documentation index under `docs/services/`.
- Added a standard service documentation template.
- Added a runbook template for repeatable procedures.
- Added a project template for larger service or infrastructure efforts.
- Defined service lifecycle states for planned, experimental, active, deprecated, and retired services.

### Why

- Create a consistent documentation pattern before deploying production-style homelab services.
- Make future service documentation easier to maintain and compare.
- Support operational practices such as validation, rollback planning, troubleshooting, monitoring, backups, and recovery.

### Lessons Learned

- Service documentation should cover operations and recovery, not just installation notes.
- Templates reduce the chance that future services miss important maintenance details.
- Larger service projects should track design decisions, risks, validation, and lessons learned separately from day-to-day service pages.

### Remaining Work

- Add service-specific runbooks as operational procedures are created.
- Link future service decisions to architecture decision records when appropriate.

## 2026-07-07 - Hardware Model Refinement

### Changed

- Updated hardware documentation to reflect actual deployed device models instead of generic placeholders.
- Documented the Lenovo ThinkPad E16 Gen 1 as the primary Proxmox host.
- Documented the TP-Link TL-SG108E Easy Smart Switch using stock firmware.
- Documented the GL.iNet GL-SFT1200 Opal as the current lab router using stock firmware.
- Reframed the desktop page as an administrative workstation without publishing personal workstation hardware details.

### Why

- Make the repository accurately represent the real homelab infrastructure.
- Keep public documentation specific enough to be useful while still avoiding serial numbers, management IPs, MAC addresses, and personal workstation details.
- Improve portfolio quality by documenting engineering tradeoffs behind hardware choices.

### Lessons Learned

- Real model names are useful and safe to publish when they do not expose personally identifying or secret information.
- Personal workstation specifications should be omitted unless they are directly relevant to the lab architecture.
- Business-class laptops can be a practical first Proxmox platform when power, noise, cost, and simplicity matter.

### Remaining Work

- Add sanitized switch port mapping after physical topology is finalized.
- Add VLAN documentation after segmentation is implemented.
- Revisit router/firewall design if the Opal no longer meets lab requirements.
- Add recovery and maintenance runbooks for core hardware.

## 2026-07-07 - Hardware Documentation

### Changed

- Added the hardware documentation index under `docs/hardware/`.
- Expanded the sanitized hardware inventory.
- Added managed switch documentation covering current role, management access, VLAN planning, and maintenance notes.
- Added router/firewall documentation covering current upstream dependency and future routing responsibilities.
- Added desktop workstation documentation covering administrative use, documentation workflow, and security considerations.
- Added primary virtualization server documentation covering the Proxmox host role, storage, networking, security, and recovery considerations.

### Why

- Establish a hardware baseline before adding more services and complex network changes.
- Make physical infrastructure roles clear enough for future troubleshooting.
- Keep public hardware documentation useful without exposing serial numbers, exact management addresses, or personally identifying details.

### Lessons Learned

- Hardware documentation should focus on operational role and architecture impact rather than raw device identifiers.
- Managed switching and Proxmox hosting are foundational enough to document before advanced services are deployed.
- Router/firewall documentation should distinguish current upstream dependency from future dedicated routing design.

### Remaining Work

- Add sanitized hardware specifications once device details are finalized.
- Document switch port mapping and VLAN assignments after segmentation is implemented.
- Document router/firewall platform decision once selected.
- Add hardware maintenance and recovery runbooks as the lab matures.

## 2026-07-07 - Architecture Documentation

### Changed

- Added the architecture documentation index under `docs/architecture/`.
- Expanded the high-level architecture overview.
- Documented the current network baseline, sanitized addressing model, and future segmentation plan.
- Documented the Proxmox virtualization strategy and workload categories.
- Documented storage assumptions, backup philosophy, and future NAS considerations.
- Documented monitoring goals, scope, alerting philosophy, and future observability direction.
- Documented security architecture, public documentation boundaries, management access, and security lab isolation goals.

### Why

- Create a clear architecture baseline before adding more hardware-specific and service-specific documentation.
- Make the repository more useful as both an operational reference and a public portfolio.
- Preserve the reasoning behind early design decisions while the lab is still simple enough to explain cleanly.

### Lessons Learned

- Architecture documentation should describe the intended operating model, not just list devices.
- Sanitized placeholders allow useful public documentation without exposing sensitive infrastructure details.
- Security lab work should be planned around isolation before offensive or intentionally vulnerable workloads are introduced.

### Remaining Work

- Document the hardware inventory and device roles.
- Add switch, router, desktop, and server documentation.
- Add service documentation templates and runbooks for future workloads.
- Create architecture decision records for major design choices.

## 2026-07-07 - Documentation Foundation

### Changed

- Added the initial public portfolio documentation structure.
- Expanded the repository README into a landing page.
- Added documentation standards, sanitization rules, roadmap, security policy, runbooks, service templates, and architecture decision records.

### Why

- Establish the GitHub repository as the source of truth for the homelab.
- Create a maintainable documentation foundation before starting larger infrastructure projects.
- Ensure public documentation is safe, sanitized, and resume-ready from the beginning.

### Lessons Learned

- Public infrastructure documentation needs explicit sanitization rules before detailed implementation notes are added.
- A strong structure early prevents the repo from becoming a collection of disconnected notes.

### Remaining Work

- Document the initial hardware inventory.
- Document the current network assumptions.
- Add the first real service or infrastructure project once implementation begins.
