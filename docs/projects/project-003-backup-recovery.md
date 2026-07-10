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

Project 003 is in **Phase 003A: Backup Readiness and Configuration Inventory**.

The external backup target is not yet available. Phase 003A identifies the state that must be preserved, records sanitized configuration locations, creates portable service exports, and drafts recovery procedures before automated VM backups are configured.

The live inventory and application-export work are complete. Remaining work is documentation validation plus the future backup-storage, VM-backup, and restore-test phases.

## Purpose

Establish a documented and testable backup and recovery process for the homelab.

The guiding question for each system is:

> If this VM failed tonight, what information and service state would be required to rebuild it?

Full-VM backups are valuable, but they are not a substitute for understanding service configuration, dependencies, portable exports, and validation requirements.

## Objectives

- Identify critical configuration and service state on `dns01` and `mon01`.
- Assign recovery priority based on service dependencies and operational impact.
- Record verified configuration paths, package versions, storage footprints, and service dependencies.
- Create protected Pi-hole and Grafana application exports.
- Inspect exports without publishing private values.
- Draft service recovery notes before implementing the final Proxmox backup target.
- Configure and validate VM backups after the external backup drive is available.
- Perform at least one representative restore test and document the result.

## Scope

### Phase 003A

- `dns01` configuration and recovery inventory.
- `mon01` configuration and recovery inventory.
- Pi-hole Teleporter export and private inspection.
- Grafana dashboard JSON exports and private inspection.
- Prometheus and Blackbox Exporter configuration inventory.
- Grafana data-source and local-state inventory.
- Node Exporter package and service-state inventory.
- Sanitized rebuild and recovery notes.
- Reusable service export and inspection runbook.

### Backup Implementation Phase

- Prepare and mount the external backup drive.
- Add the drive as Proxmox backup storage.
- Configure backup jobs and retention.
- Run initial VM backups.
- Validate backup completion and artifact size.
- Perform and document a representative restore test.

### Out of Scope

- Treating same-disk backups as the final backup design.
- Building a dedicated storage server or NAS.
- Deploying Proxmox Backup Server before it is justified.
- Adding monitoring alerts before response runbooks exist.
- Publishing raw exports containing internal addresses, credentials, tokens, query history, or sensitive topology details.

## Architecture Impact

| Area | Impact |
| --- | --- |
| Network | No topology change during Phase 003A. Recovery documentation uses sanitized placeholders. |
| Virtualization | Future Proxmox backup jobs will cover the current infrastructure VMs. Restore testing may create a temporary isolated recovery VM. |
| Storage | Introduces a dedicated external backup destination instead of relying on the Proxmox system disk. |
| Monitoring | Monitoring configuration, Grafana state, and dashboard exports become defined recovery assets. |
| Security | Raw exports remain outside Git. Only sanitized documentation or reviewed artifacts may be published. |
| Documentation | Project, runbook, service, architecture, and changelog pages are updated as milestones are completed. |

## Design Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| Inventory service state before configuring backup jobs | A successful VM backup is not a substitute for understanding what must be recovered. | Backup-job configuration waits for the external target, but recovery readiness improves first. |
| Use VM backups and application-level exports | Provides fast full-system recovery plus portable service-level recovery. | More than one recovery method must be maintained. |
| Restore `dns01` before `mon01` | DNS failure affects access to and troubleshooting of other services. | Monitoring visibility returns after DNS. |
| Keep raw exports outside Git | Pi-hole and Grafana exports contain environment-specific operational data. | Artifacts require protected storage and manual review. |
| Mark recovery procedures as draft until tested | Prevents documentation from overstating recovery maturity. | Final validation waits for a controlled restore. |
| Prefer Pi-hole Teleporter over a raw live directory copy | `/etc/pihole/` mixes active databases, configuration, query history, authentication data, and generated state. | The Teleporter archive still requires protected storage. |
| Preserve Prometheus configuration separately from metrics history | Configuration is small and essential; short-term metrics history is less critical at the current scale. | A manual rebuild may lose historical monitoring data. |
| Export Grafana dashboards even when `grafana.db` is protected | Portable JSON reduces dependence on one local database. | Data-source mappings must be verified during import. |
| Treat Grafana plugin directories as replaceable content | Plugin files account for nearly all Grafana state-directory usage and can be reinstalled. | Custom plugin requirements must still be recorded. |
| Store environment-specific identifiers privately | Exact data-source UIDs, hashes, addresses, and MAC values are unnecessary in public architecture documentation. | Private recovery records must remain available. |

## Backup Inventory

| System | Role | Planned backup method | Restore priority | Current status |
| --- | --- | --- | --- | --- |
| `dns01` | DNS and Pi-hole | Proxmox VM backup, Pi-hole Teleporter export, and sanitized rebuild notes | High | Live inventory, Teleporter export, integrity validation, and private inspection complete. VM backup and restore validation remain pending. |
| `mon01` | Monitoring and observability | Proxmox VM backup, reviewed configuration copies, dashboard JSON exports, and sanitized rebuild notes | Medium | Live inventory, state classification, dashboard export, dashboard inspection, and data-source recovery mapping complete. VM backup and restore validation remain pending. |

## Configuration Inventory

### `dns01` — Verified

| Item | Verified location or state |
| --- | --- |
| Pi-hole state directory | `/etc/pihole/`, approximately 16 MB during inventory |
| Pi-hole versions | Core v6.4.3, Web v6.6, FTL v6.7 |
| Pi-hole systemd unit | `/etc/systemd/system/pihole-FTL.service` |
| Pi-hole unit overrides | None detected |
| Pi-hole service state | Active, running, and enabled |
| Node Exporter systemd unit | `/usr/lib/systemd/system/prometheus-node-exporter.service` |
| Node Exporter unit overrides | None detected |
| Node Exporter service state | Active, running, and enabled |
| Node Exporter package | `prometheus-node-exporter` version `1.9.0-1+b4` |
| Static network configuration | `/etc/network/interfaces` using `ifupdown` |
| Interface model | `ens18` with a static `/24` address and sanitized gateway `<LAB_GATEWAY>` |
| Host resolver configuration | Public resolvers defined in `/etc/network/interfaces` |

The host resolver does not depend on Pi-hole itself. This reduces circular dependency during troubleshooting or recovery, but DNS queries originating from `dns01` bypass local Pi-hole filtering.

### Pi-hole Teleporter Artifact

| Item | Verified result |
| --- | --- |
| Filename | `pi-hole_dns01_teleporter_2026-07-09_22-27-17_MST.zip` |
| Logical size | 23,868 bytes |
| Archive integrity | Pass |
| Archive entries | 5 |
| Uncompressed size | 123,439 bytes |
| SHA-256 | Recorded privately |
| Database files | `etc/pihole/gravity.db`, `etc/pihole/pihole-FTL.db` |
| Other file types | One `.leases`, one `.toml`, and one extensionless entry |
| Key or certificate entries | None detected by filename classification |

Private content inspection detected:

- 24 private IPv4 references.
- 7 URL references.
- 2 MAC-address references.
- No email-address matches.
- A `totp_secret` property name.

No values were published. The archive remains private because it contains authentication-related state, network identifiers, lease data, and Pi-hole databases.

### `mon01` — Verified

#### Service and Package Baseline

| Service | Package version | Unit path | Runtime and boot state | Unit overrides |
| --- | --- | --- | --- | --- |
| Prometheus | `2.53.3+ds1-2` | `/usr/lib/systemd/system/prometheus.service` | Active, running, and enabled | None detected |
| Grafana | `13.1.0` | `/usr/lib/systemd/system/grafana-server.service` | Active, running, and enabled | None detected |
| Node Exporter | `1.9.0-1+b4` | `/usr/lib/systemd/system/prometheus-node-exporter.service` | Active, running, and enabled | None detected |
| Blackbox Exporter | `0.26.0-1` | `/usr/lib/systemd/system/prometheus-blackbox-exporter.service` | Active, running, and enabled | None detected |

#### Configuration and State Locations

| Item | Verified location or state |
| --- | --- |
| Prometheus configuration | `/etc/prometheus/prometheus.yml` |
| Blackbox Exporter configuration | `/etc/prometheus/blackbox.yml` |
| Prometheus configuration footprint | Approximately 44 KB under `/etc/prometheus/` |
| Prometheus local data | Approximately 59 MB under `/var/lib/prometheus/metrics2/` |
| Node Exporter collector state | Approximately 16 KB under `/var/lib/prometheus/node-exporter/` |
| Grafana main configuration | `/etc/grafana/grafana.ini` |
| Grafana provisioning root | `/etc/grafana/provisioning/`; package-provided samples only |
| Grafana configuration footprint | Approximately 156 KB under `/etc/grafana/` |
| Grafana SQLite database | `/var/lib/grafana/grafana.db`, approximately 2.2 MB |
| Grafana installed plugins | Approximately 112 MB under `/var/lib/grafana/plugins/` |
| Grafana bundled plugins | Approximately 64 MB under `/var/lib/grafana/plugins-bundled/` |
| Node Exporter dashboard export | `node-exporter-dashboard.json`, 723,648 bytes; stored outside Git |
| Service Health dashboard export | `homelab-service-health-dashboard.json`, 11,873 bytes; stored outside Git |
| Grafana Prometheus data source | Name `prometheus`; type `prometheus`; URL `http://localhost:9090`; UID retained privately as `<PROMETHEUS_DATASOURCE_UID>` |

Approximately 176 MB of the 177 MB Grafana state directory is plugin content. Operationally unique state is concentrated primarily in `grafana.db`, dashboard JSON, data-source configuration, modified settings, and future custom plugin requirements.

Both dashboard exports parse as valid JSON. Private inspection found expected internal addressing but no sensitive-looking credential property names. The exports contained no `__inputs` section and no explicit data-source object discovered by the inspection script, so recovery must validate data-source mappings after import.

#### Prometheus Validation

`promtool check config /etc/prometheus/prometheus.yml` completed successfully.

Verified scrape job names:

- `prometheus`
- `node_exporter`
- `blackbox_dns`

Local `.bak-*` files are useful short-term rollback artifacts but are not a substitute for protected backups and restore testing.

## Milestones

| Milestone | Status | Completion criteria |
| --- | --- | --- |
| 1. Create backup inventory | Complete | Both systems have documented roles, recovery priorities, and intended backup methods. |
| 2. Verify configuration locations | Complete | Live configuration, service state, package versions, storage footprints, and state classification are documented. |
| 3. Export Grafana dashboards | Complete | Both JSON files exist outside Git, parse successfully, and were privately inspected. |
| 4. Export Pi-hole configuration | Complete | Teleporter ZIP exists outside Git, passes integrity validation, and was privately inspected. |
| 5. Draft recovery notes | Complete | Application-level recovery dependencies and the service-export runbook are documented. Procedures remain unvalidated until a restore test. |
| 6. Configure backup storage | Blocked | External backup target is mounted and added to Proxmox storage. |
| 7. Run initial VM backups | Blocked | Backups complete successfully and retention is documented. |
| 8. Perform restore test | Blocked | A representative VM restore succeeds and service validation is documented. |
| 9. Final documentation review | In Progress | Link validation and future implementation synchronization remain. |

## Validation Plan

- Confirm inventoried services are active and enabled.
- Validate Prometheus configuration with `promtool`.
- Confirm expected Prometheus jobs remain present with PromQL.
- Confirm Pi-hole answers public and local DNS queries after recovery.
- Confirm Node Exporter and Blackbox Exporter metrics recover.
- Confirm Grafana can reconnect to Prometheus and import both dashboard exports.
- Verify imported dashboard panels and variables against the recreated data source.
- Confirm Proxmox backup jobs report success and produce reasonable artifacts.
- Restore at least one representative VM in an isolated or controlled state.
- Run `python scripts/check-markdown-links.py` after documentation changes.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Raw exports expose private values | High | Store exports outside Git and commit only sanitized documentation or reviewed derivatives. |
| Teleporter archive contains authentication and network state | High | Preserve it only in protected storage and avoid printing values during inspection. |
| Raw copies of live Pi-hole state are inconsistent | High | Use Teleporter for portable recovery and Proxmox backup for whole-system recovery. |
| Grafana dashboards depend on local database state | High | Preserve `grafana.db` consistently and maintain portable dashboard JSON. |
| Dashboard import does not bind to the intended data source | High | Create and test the Prometheus data source first, then verify imported panels and variables. |
| Backup target resides on the source disk | High | Use the planned external drive. |
| Backup completes but restore fails | High | Require a representative restore test before project completion. |
| Draft runbooks are mistaken for tested procedures | Medium | Retain explicit draft or unvalidated labels until exercised. |
| Historical Prometheus metrics are lost in a manual rebuild | Low / Medium | Prioritize configuration and dashboard recovery; document retention separately. |
| Manual `.bak-*` files are mistaken for a backup system | Medium | Treat them only as local rollback copies. |

## Recovery Order

1. Restore basic network and Proxmox management access.
2. Restore `dns01` and validate DNS operation.
3. Restore `mon01` and validate Prometheus, exporters, and Grafana.
4. Confirm monitoring observes both restored systems.
5. Review logs and update documentation with recovery differences.

## Preliminary Manual Recovery Notes

### `dns01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM with `ifupdown` networking.
3. Recreate static networking using protected operational values.
4. Reinstall Pi-hole and Node Exporter.
5. Import the protected Teleporter archive.
6. Confirm upstream DNS settings and required local records.
7. Confirm `pihole-FTL` and `prometheus-node-exporter` are active and enabled.
8. Validate public resolution, local records, Node Exporter metrics, and the Blackbox DNS probe.

### `mon01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM.
3. Reinstall supported versions of Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
4. Restore or recreate `/etc/prometheus/prometheus.yml` and `/etc/prometheus/blackbox.yml`.
5. Validate Prometheus and confirm the `prometheus`, `node_exporter`, and `blackbox_dns` jobs exist.
6. Restore Grafana through a consistency-preserving SQLite backup, or recreate the Prometheus data source.
7. Import the reviewed dashboard JSON files.
8. Verify the Prometheus mapping for all panels and variables.
9. Reinstall required non-bundled plugins.
10. Confirm all four services are active and enabled.
11. Validate target health, PromQL queries, DNS probes, and Grafana panels.

These procedures remain unvalidated until a controlled restore or rebuild test succeeds.

## Results

- Completed live backup-readiness inventories for `dns01` and `mon01`.
- Created and privately validated the Pi-hole Teleporter ZIP.
- Created and privately validated both Grafana dashboard exports.
- Classified Grafana plugin content and Prometheus metrics history.
- Verified the Grafana Prometheus data-source recovery mapping.
- Added a reusable service configuration export and inspection runbook.
- Corrected the recorded Teleporter filename after the original timestamp was found to be inaccurate.
- Confirmed raw exports must remain outside Git.

## Lessons Learned

- Configuration directories can mix essential state, generated data, credentials, certificates, logs, and active databases.
- Directory size does not indicate recovery importance.
- Export formats and filenames should be verified from the generated artifact rather than assumed.
- Valid Prometheus syntax does not prove all intended jobs remain present.
- Package-provided provisioning samples do not protect Grafana state created through the web interface.
- Dashboard exports do not necessarily preserve automatic data-source binding.
- Keyword matches do not automatically indicate a secret; inspection should classify property names without printing values.
- Archive integrity validation does not make an export safe to publish.
- A portable export is not a validated backup until an import or restore succeeds.

## Follow-Up Tasks

- [x] Create the initial backup inventory and recovery priorities.
- [x] Verify `dns01` configuration, service, package, and network state.
- [x] Create and protect the Pi-hole Teleporter archive.
- [x] Inspect the Teleporter archive privately.
- [x] Verify all `mon01` configuration, package, service, and storage state.
- [x] Classify Grafana and Prometheus local state.
- [x] Export and inspect both Grafana dashboards.
- [x] Document the Grafana data-source recovery mapping.
- [x] Add `docs/runbooks/service-config-export.md`.
- [ ] Expand `docs/runbooks/backup.md` with the selected schedule and retention after the target is available.
- [ ] Expand `docs/runbooks/disaster-recovery.md` from restore-test findings.
- [ ] Add `docs/runbooks/proxmox-vm-restore.md`.
- [ ] Update `docs/architecture/storage.md` after the backup target is implemented.
- [ ] Run the Markdown link validator.
- [ ] Record the completed Phase 003A milestone in `CHANGELOG.md`.

## Related Documentation

- [Projects README](README.md)
- [Service Configuration Export and Inspection Runbook](../runbooks/service-config-export.md)
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
