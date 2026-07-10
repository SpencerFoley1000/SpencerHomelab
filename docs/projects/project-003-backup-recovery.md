# Project 003: Backup and Recovery

## Status

| Area | Details |
| --- | --- |
| Status | Active |
| Start date | 2026-07-09 |
| Completion date | Pending |
| Owner | Homelab administrator |
| Related services | Proxmox VE, Pi-hole, Prometheus, Grafana, Node Exporter, Blackbox Exporter |

## Current Phase

Project 003 is beginning with **Phase 003A: Backup Readiness and Configuration Inventory**.

The external backup target is not yet available. This phase identifies the service state that must be preserved, records sanitized configuration locations, exports application-level configuration where practical, and drafts recovery procedures before automated VM backups are configured.

## Purpose

Establish a documented, testable backup and recovery process for the homelab.

The immediate question for each system is:

> If this VM failed tonight, what information and service state would be required to rebuild it?

This phase prevents VM-level backups from becoming the only recovery strategy. Full-VM backups are valuable, but service-specific exports and documented rebuild procedures provide additional recovery options and demonstrate that the contents of each workload are understood.

## Objectives

- Identify critical configuration and service state on `dns01` and `mon01`.
- Assign recovery priority based on service dependencies and operational impact.
- Record verified configuration paths and service dependencies.
- Export Grafana dashboards and Pi-hole configuration for inspection.
- Sanitize all artifacts before considering them for version control.
- Draft service recovery notes before implementing the final Proxmox backup target.
- Configure and validate VM backups after the external backup drive is available.
- Perform at least one representative restore test and document the result.

## Scope

### In Scope: Phase 003A

- `dns01` configuration and recovery inventory.
- `mon01` configuration and recovery inventory.
- Pi-hole Teleporter export.
- Grafana dashboard JSON exports.
- Prometheus and Blackbox Exporter configuration inventory.
- Grafana data source and local state inventory.
- Node Exporter package and service-state inventory.
- Sanitized rebuild and recovery notes.
- Identification of sensitive values that must remain outside the public repository.

### In Scope: Backup Implementation Phase

- Prepare and mount the external backup drive.
- Add the drive as Proxmox backup storage.
- Configure backup jobs and retention.
- Run initial VM backups.
- Validate backup completion and file size.
- Perform and document a representative restore test.

### Out of Scope

- Treating same-disk backups as the final backup design.
- Building a dedicated storage server or NAS.
- Deploying Proxmox Backup Server before it is justified.
- Adding monitoring alerts before response runbooks exist.
- Purchasing additional hardware beyond the planned backup target.
- Publishing raw exports containing internal addresses, hostnames, credentials, tokens, or sensitive topology details.

## Architecture Impact

| Area | Impact |
| --- | --- |
| Network | No planned topology change during Phase 003A. Recovery documentation will use sanitized placeholders for addresses and internal names. |
| Virtualization | Future Proxmox backup jobs will cover the current infrastructure VMs. Restore testing may create a temporary isolated recovery VM. |
| Storage | Introduces a dedicated external backup destination rather than relying on the Proxmox system disk. |
| Monitoring | Monitoring configuration and dashboards become defined backup assets. Future backup-job monitoring remains follow-up work. |
| Security | Exports must be reviewed before commit. Secrets and private topology remain outside the repository. |
| Backup and recovery | Establishes recovery priorities, backup scope, service exports, and tested restore procedures. |
| Documentation | Updates project, runbook, architecture, service, and changelog documentation as milestones are completed. |

## Design Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| Inventory service state before configuring backup jobs | A successful VM backup is not a substitute for understanding what must be recovered. | Delays backup-job configuration until the backup target arrives, but improves recovery readiness. |
| Use both VM backups and application-level exports | Provides fast full-system recovery plus portable service-level recovery options. | Requires maintaining more than one recovery method. |
| Treat `dns01` as the highest-priority application VM | DNS failure affects access to and troubleshooting of other services. | Monitoring may be restored later even though it provides useful visibility. |
| Keep raw exports outside Git until inspected | Pi-hole and Grafana exports may expose private names, addresses, or embedded connection details. | Artifacts require manual review and possible sanitization before versioning. |
| Mark runbooks as planned until tested | Prevents draft instructions from being mistaken for validated procedures. | Recovery documentation will mature incrementally rather than appearing complete immediately. |
| Prefer Pi-hole Teleporter over a raw live directory copy | `/etc/pihole/` contains live databases, authentication data, TLS material, and generated files in addition to configuration. | The portable export must still be protected and inspected, and a VM backup remains necessary for fastest full recovery. |

## Backup Inventory

| System | Role | Critical configuration and state | Planned backup method | Restore priority | Current notes |
| --- | --- | --- | --- | --- | --- |
| `dns01` | DNS and Pi-hole | Pi-hole settings, local DNS records, upstream DNS configuration, service configuration, Node Exporter service state, static addressing assumptions | Proxmox VM backup plus Pi-hole Teleporter export and sanitized rebuild notes | High | `/etc/pihole/` is verified as the main Pi-hole state directory and currently uses approximately 16 MB. Pi-hole FTL and Node Exporter are active and enabled. |
| `mon01` | Monitoring and observability | Prometheus scrape configuration, Blackbox Exporter modules, Grafana dashboards, Grafana data source, Grafana local state, exporter service state, service dependencies | Proxmox VM backup plus reviewed configuration copies, dashboard JSON exports, and sanitized rebuild notes | Medium | Monitoring does not provide production traffic, but losing it removes health visibility and historical metrics. Live configuration inventory remains pending. |

## Configuration Inventory

The following locations are expected based on the current deployment and must be verified on the live systems before the inventory is considered complete.

### `dns01`

| Item | Location or method | Verification status |
| --- | --- | --- |
| Pi-hole configuration and local DNS data | `/etc/pihole/` | Verified; approximately 16 MB on 2026-07-09 |
| Pi-hole portable export | Pi-hole Teleporter | Pending |
| Pi-hole service definition | `systemctl cat pihole-FTL` | Pending |
| Pi-hole service state | `systemctl is-active` and `systemctl is-enabled` | Verified active and enabled |
| Node Exporter service definition | `systemctl cat prometheus-node-exporter` | Pending |
| Node Exporter service state | `systemctl is-active` and `systemctl is-enabled` | Verified active and enabled |
| Static addressing configuration | Debian network configuration and documented Proxmox/network assumptions | Documented static assignment; live configuration path pending verification |
| Installed Pi-hole versions | `pihole version` | Verified: Core v6.4.3, Web v6.6, FTL v6.7 |
| Installed package inventory | Debian package inventory | Pending |

#### Observed Pi-hole State

The `/etc/pihole/` inventory includes:

- Primary Pi-hole configuration and generated DNS configuration.
- Gravity databases and Pi-hole-generated configuration backups.
- Local host data and list cache directories.
- The active FTL database and SQLite write-ahead-log files.
- Authentication and TLS-related files that must be treated as sensitive.

Raw directory contents must not be committed to the public repository. Query-history databases, private DNS information, authentication material, and TLS private material require protected storage outside Git.

### `mon01`

| Item | Candidate location or method | Verification status |
| --- | --- | --- |
| Prometheus scrape configuration | `/etc/prometheus/prometheus.yml` | Pending |
| Blackbox Exporter configuration | `/etc/prometheus/blackbox.yml` | Pending |
| Prometheus service definition | `systemctl cat prometheus` | Pending |
| Blackbox Exporter service definition | `systemctl cat prometheus-blackbox-exporter` | Pending |
| Grafana main configuration | `/etc/grafana/grafana.ini` | Pending |
| Grafana provisioning configuration | `/etc/grafana/provisioning/` | Pending |
| Grafana local state | `/var/lib/grafana/` | Pending |
| Grafana dashboards | Dashboard JSON export from the Grafana UI | Pending |
| Grafana Prometheus data source | Grafana UI and provisioning/state review | Pending |
| Node Exporter service definition | `systemctl cat prometheus-node-exporter` | Pending |
| Installed service versions | Debian package inventory | Pending |

## Milestones

| Milestone | Status | Completion criteria |
| --- | --- | --- |
| 1. Create backup inventory | Complete | Both systems have documented roles, critical state, recovery priority, and intended backup methods. |
| 2. Verify configuration locations | In Progress | Candidate paths and service definitions are checked on each live VM without publishing sensitive values. |
| 3. Export Grafana dashboards | Not Started | Node Exporter and Homelab Service Health dashboards are exported and inspected. |
| 4. Export Pi-hole configuration | Not Started | Teleporter archive is created, stored outside Git, and inspected for sensitive content. |
| 5. Draft recovery notes | Not Started | Each service has a documented manual rebuild path and validation procedure. |
| 6. Configure backup storage | Blocked | External backup target is mounted and added to Proxmox storage. |
| 7. Run initial VM backups | Blocked | Backups complete successfully and retention is documented. |
| 8. Perform restore test | Blocked | A representative VM restore succeeds and service validation is documented. |
| 9. Final documentation review | Not Started | Runbooks, service pages, storage architecture, project status, roadmap, and changelog agree. |

## Implementation Plan

1. Create the initial backup inventory and mark Project 003 active.
2. Inventory `dns01` service versions, unit definitions, configuration directories, and network assumptions.
3. Inventory `mon01` service versions, unit definitions, configuration directories, Grafana state, and dependencies.
4. Export Pi-hole configuration and Grafana dashboards to a private staging location.
5. Inspect exports for internal names, addresses, credentials, tokens, and embedded topology.
6. Create sanitized configuration examples only where they improve recovery documentation.
7. Expand the backup and disaster-recovery runbooks with environment-specific draft procedures.
8. Add dedicated Proxmox VM restore and service configuration export runbooks.
9. Configure the external backup target when available.
10. Run backup jobs and perform a representative restore test.
11. Promote only tested procedures to operational status.
12. Synchronize related service, architecture, project, roadmap, and changelog documentation.

## Validation Plan

- **Functional validation:** Confirm all inventoried services are currently active before exporting or documenting their state.
- **Configuration validation:** Validate Prometheus configuration with `promtool check config` and confirm expected scrape jobs remain present.
- **Monitoring validation:** Confirm `up`, `up{job="node_exporter"}`, and `probe_success{job="blackbox_dns"}` return expected data after any recovery test.
- **DNS validation:** Confirm Pi-hole answers a known DNS query and local records resolve after recovery.
- **Backup validation:** Confirm Proxmox backup jobs report success and produce reasonably sized backup artifacts on the external target.
- **Recovery validation:** Restore at least one representative VM to an isolated or controlled state and verify its services.
- **Security validation:** Review every export before commit and keep unsanitized artifacts outside the public repository.
- **Documentation validation:** Run `python scripts/check-markdown-links.py` after adding or moving documentation.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Raw exports expose internal hostnames, addresses, or credentials | High | Store exports outside Git until reviewed; commit only sanitized artifacts when useful. |
| Raw copies of live Pi-hole state are inconsistent | High | Prefer Teleporter for portable configuration and use Proxmox VM backup for whole-system recovery; do not rely on copying active SQLite files. |
| Backup target resides on the same physical disk as the source | High | Use the planned external drive and document same-disk copies as temporary only. |
| Backup completes but restore fails | High | Require a representative restore test before calling the project complete. |
| Recovery notes omit service dependencies | Medium | Record startup order, network assumptions, data sources, exporters, and validation checks. |
| Draft runbooks are mistaken for tested procedures | Medium | Retain planned or draft labels until procedures are executed successfully. |
| Exported Grafana dashboard depends on an environment-specific data source UID | Medium | Inspect JSON and document required data source mapping during import. |
| Historical Prometheus metrics are not preserved in a manual rebuild | Low / Medium | Treat configuration and dashboard recovery as higher priority; document retention expectations separately. |

## Initial Recovery Order

1. Restore basic network and Proxmox management access.
2. Restore `dns01` and validate DNS service operation.
3. Restore `mon01` and validate Prometheus, exporters, and Grafana.
4. Confirm monitoring can observe both restored systems.
5. Review logs and update documentation with any differences discovered during recovery.

## Preliminary Manual Recovery Notes

### `dns01`

1. Restore the VM backup when available.
2. If rebuilding manually, deploy a supported Debian VM with documented baseline administration and network settings.
3. Reinstall Pi-hole and Node Exporter.
4. Restore the reviewed Pi-hole Teleporter export or recreate equivalent settings manually.
5. Confirm upstream DNS configuration and required local DNS records.
6. Validate Pi-hole service state, DNS queries, local records, and Node Exporter metrics.
7. Confirm `mon01` can reach the Node Exporter endpoint and complete the DNS availability probe.

### `mon01`

1. Restore the VM backup when available.
2. If rebuilding manually, deploy a supported Debian VM with documented baseline administration and network settings.
3. Reinstall Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
4. Restore or recreate the reviewed Prometheus and Blackbox Exporter configuration.
5. Recreate the Grafana Prometheus data source.
6. Import reviewed dashboard JSON.
7. Validate service states, Prometheus targets, required PromQL queries, Blackbox DNS probes, and Grafana panels.

These steps are preliminary and are not operationally validated until a restore or controlled rebuild test is completed.

## Results

- What worked: The first live `dns01` inventory verified the primary Pi-hole state directory, its approximate size, exact Pi-hole component versions, and enabled service state for Pi-hole FTL and Node Exporter.
- What failed: Nothing during the initial read-only inventory.
- What changed from the original plan: The raw `/etc/pihole/` directory was confirmed to contain sensitive and actively changing state, reinforcing Teleporter as the preferred application-level export rather than a raw directory copy.
- What remains unfinished: `dns01` unit definitions and network path verification, Pi-hole Teleporter export, complete `mon01` inventory, dashboard exports, backup implementation, and restore testing.

## Lessons Learned

- Application configuration directories can mix essential configuration, generated data, credentials, certificates, logs, and active databases; inventory must classify the contents rather than treating the directory as one safe artifact.
- A small configuration footprint does not mean the directory is safe for public version control.
- Service recovery planning should verify both current runtime state and boot-time enablement.

## Follow-Up Tasks

- [x] Create the initial backup inventory and recovery priorities.
- [ ] Verify remaining `dns01` service definitions and live network configuration path.
- [ ] Record the `dns01` Debian package inventory relevant to recovery.
- [ ] Verify all `mon01` configuration locations and service definitions.
- [ ] Export and inspect both Grafana dashboards.
- [ ] Export and inspect Pi-hole Teleporter configuration.
- [ ] Expand `docs/runbooks/backup.md` with the selected backup schedule and retention.
- [ ] Expand `docs/runbooks/disaster-recovery.md` with tested service recovery order.
- [ ] Add `docs/runbooks/proxmox-vm-restore.md`.
- [ ] Add `docs/runbooks/service-config-export.md`.
- [ ] Update `docs/architecture/storage.md` after the backup target is implemented.
- [ ] Update affected service pages with backup and recovery details.
- [ ] Run the Markdown link validator.
- [ ] Record completed implementation and recovery milestones in `CHANGELOG.md`.

## Related Documentation

- [Projects README](README.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Pi-hole Service](../services/pihole.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)