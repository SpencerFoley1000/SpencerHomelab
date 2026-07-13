# Project 003: Backup and Recovery

## Status

| Area | Details |
| --- | --- |
| Status | Active — Phase 003A complete; backup implementation pending 5 TB target availability and integration |
| Start date | 2026-07-09 |
| Completion date | Pending |
| Owner | Homelab administrator |
| Related services | Proxmox VE, Pi-hole, Prometheus, Grafana, Node Exporter, Blackbox Exporter |

## Current Phase

**Phase 003A: Backup Readiness and Configuration Inventory is complete.**

The recoverable state, dependencies, configuration locations, portable exports, sensitive-data boundaries, and preliminary recovery procedures for `dns01` and `mon01` are documented.

A 5 TB external hard drive has been ordered for the first dedicated Proxmox backup target. Project 003 moves into implementation when the drive is physically available and passes basic inspection.

Remaining implementation work:

- Prepare and mount the external backup target.
- Register it in Proxmox.
- Define protected VMs, scheduling, retention, and pruning.
- Run initial backups for `dns01` and `mon01`.
- Validate backup results and capacity usage.
- Perform and document a representative isolated restore test.

## Purpose

Establish a documented and testable backup and recovery process for the homelab.

The guiding question for each system is:

> If this VM failed tonight, what information and service state would be required to rebuild it?

Full-VM backups are valuable, but they are not a substitute for understanding service configuration, dependencies, portable exports, and validation requirements.

## Objectives

- Identify critical configuration and service state on `dns01` and `mon01`.
- Assign recovery priority based on dependencies and operational impact.
- Record verified configuration paths, package versions, storage footprints, and service dependencies.
- Create protected Pi-hole and Grafana application exports.
- Inspect exports without publishing private values.
- Maintain recovery notes that reflect the full deployed monitoring configuration.
- Configure and validate VM backups after the external target is available.
- Perform at least one representative restore test and document the result.

## Scope

### Phase 003A — Complete

- `dns01` configuration and recovery inventory.
- `mon01` configuration and recovery inventory.
- Pi-hole Teleporter export and private inspection.
- Grafana dashboard JSON exports and private inspection.
- Prometheus and Blackbox Exporter configuration inventory.
- Grafana data-source and local-state inventory.
- Node Exporter package and service-state inventory.
- Sanitized rebuild and recovery notes.
- Reusable service export and inspection runbook.

### Backup Implementation Phase — Pending

- Inspect and prepare the 5 TB external hard drive.
- Select and document the filesystem and mount strategy.
- Add the drive as Proxmox backup storage using a sanitized public label.
- Configure backup jobs, retention, and pruning.
- Run initial VM backups.
- Validate completion, artifact size, and capacity usage.
- Perform and document a representative restore test.

### Out of Scope

- Treating same-disk backups as the final backup design.
- Building a dedicated NAS or Proxmox Backup Server before justified.
- Adding monitoring alerts before response runbooks exist.
- Publishing raw exports containing internal addresses, credentials, tokens, query history, or sensitive topology details.
- Claiming recovery readiness before an actual restore succeeds.

## Architecture Impact

| Area | Impact |
| --- | --- |
| Network | No topology change during Phase 003A. Backup implementation adds only the required host-to-target storage path. |
| Virtualization | Proxmox backup jobs will protect the current infrastructure VMs. Restore testing may create a temporary isolated VM. |
| Storage | Introduces a dedicated 5 TB external backup destination separate from the Proxmox system SSD. |
| Monitoring | Monitoring configuration, both DNS probe jobs, Grafana state, and dashboard exports are defined recovery assets. |
| Security | Raw exports remain outside Git. Backup storage must be access-controlled and isolated from experimental workloads. |
| Documentation | Project, runbook, service, architecture, hardware, and changelog pages are updated as milestones complete. |

## Design Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| Inventory service state before configuring backup jobs | A successful VM backup is not a substitute for understanding what must be recovered. | Backup implementation waits for the target, but recovery knowledge improves first. |
| Use VM backups and application-level exports | Provides fast whole-system recovery plus portable service-level recovery. | Multiple recovery layers must be maintained. |
| Restore `dns01` before `mon01` | DNS affects access to and troubleshooting of other services. | Monitoring visibility returns after DNS. |
| Keep raw exports outside Git | Pi-hole and Grafana exports contain environment-specific operational data. | Artifacts require protected private storage. |
| Mark recovery procedures as draft until tested | Prevents overstating recovery maturity. | Final validation waits for a controlled restore. |
| Prefer Pi-hole Teleporter over a raw live directory copy | `/etc/pihole/` mixes active databases, configuration, leases, history, and authentication state. | The Teleporter archive remains sensitive. |
| Preserve Prometheus configuration separately from metrics history | Configuration is small and essential; short-term history is lower priority at current scale. | Manual recovery may lose historical metrics. |
| Export Grafana dashboards even when `grafana.db` is protected | Portable JSON reduces dependence on one SQLite database. | Data-source mappings must be verified during import. |
| Treat plugin directories as replaceable | Grafana plugin files account for most local state and can be reinstalled. | Custom plugin requirements must still be recorded. |
| Store environment-specific identifiers privately | Exact UIDs, hashes, addresses, and drive identifiers are unnecessary in public documentation. | Private recovery records must remain available. |
| Require both DNS probe jobs after recovery | Recursive and local DNS checks validate different failure domains. | Recovery validation includes more than a single generic DNS check. |

## Backup Inventory

| System | Role | Planned backup method | Restore priority | Current status |
| --- | --- | --- | --- | --- |
| `dns01` | DNS and Pi-hole | Proxmox VM backup, Pi-hole Teleporter export, and sanitized rebuild notes | High | Live inventory, Teleporter export, integrity validation, and private inspection complete. VM backup and restore validation pending. |
| `mon01` | Monitoring and observability | Proxmox VM backup, reviewed configuration copies, dashboard JSON exports, and sanitized rebuild notes | Medium | Live inventory, state classification, dashboard exports, and data-source recovery mapping complete. Infrastructure-overview export, VM backup, and restore validation pending. |

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
| Node Exporter service state | Active, running, and enabled |
| Node Exporter package | `prometheus-node-exporter` version `1.9.0-1+b4` |
| Static network configuration | `/etc/network/interfaces` using `ifupdown` |
| Interface model | `ens18` with static addressing and sanitized gateway `<LAB_GATEWAY>` |
| Host resolver configuration | Public resolvers defined in `/etc/network/interfaces` |

The host resolver does not depend on Pi-hole itself. This reduces circular dependency during recovery, but DNS queries originating from `dns01` bypass local Pi-hole filtering.

### Pi-hole Teleporter Artifact

| Item | Verified result |
| --- | --- |
| Filename | Recorded privately; generated ZIP format verified |
| Logical size | 23,868 bytes during inspection |
| Archive integrity | Pass |
| Archive entries | 5 |
| Uncompressed size | 123,439 bytes |
| SHA-256 | Recorded privately |
| Database files | `gravity.db` and `pihole-FTL.db` |
| Other content | Lease data, TOML configuration, and environment-specific state |
| Key or certificate entries | None detected by filename classification |

Private inspection detected private addressing, URLs, MAC-address references, lease data, and a `totp_secret` property name. No protected values were published. The archive must remain outside Git.

### `mon01` — Verified

#### Service and Package Baseline

| Service | Package version | Unit path | Runtime and boot state |
| --- | --- | --- | --- |
| Prometheus | `2.53.3+ds1-2` | `/usr/lib/systemd/system/prometheus.service` | Active, running, and enabled |
| Grafana | `13.1.0` | `/usr/lib/systemd/system/grafana-server.service` | Active, running, and enabled |
| Node Exporter | `1.9.0-1+b4` | `/usr/lib/systemd/system/prometheus-node-exporter.service` | Active, running, and enabled |
| Blackbox Exporter | `0.26.0-1` | `/usr/lib/systemd/system/prometheus-blackbox-exporter.service` | Active, running, and enabled |

No unit overrides were detected during inventory.

#### Configuration and State Locations

| Item | Verified location or state |
| --- | --- |
| Prometheus configuration | `/etc/prometheus/prometheus.yml` |
| Blackbox Exporter configuration | `/etc/prometheus/blackbox.yml` |
| Prometheus configuration footprint | Approximately 44 KB under `/etc/prometheus/` |
| Prometheus local data | Approximately 59 MB under `/var/lib/prometheus/metrics2/` during inventory |
| Node Exporter collector state | Approximately 16 KB under `/var/lib/prometheus/node-exporter/` |
| Grafana main configuration | `/etc/grafana/grafana.ini` |
| Grafana provisioning root | `/etc/grafana/provisioning/`; package-provided samples only |
| Grafana SQLite database | `/var/lib/grafana/grafana.db`, approximately 2.2 MB during inventory |
| Grafana installed plugins | Replaceable package/plugin content; record custom requirements separately |
| Node Exporter dashboard export | Protected JSON outside Git; syntax validated |
| Homelab Service Health export | Protected JSON outside Git; syntax validated |
| Homelab Infrastructure Overview export | Pending private Classic JSON export and validation |
| Grafana Prometheus data source | Name `prometheus`; URL `http://localhost:9090`; UID retained privately as `<PROMETHEUS_DATASOURCE_UID>` |

Dashboard exports may not preserve automatic data-source binding. Recovery must validate the Prometheus data source and all panel and variable mappings after import.

#### Prometheus and Blackbox Inventory

`promtool check config /etc/prometheus/prometheus.yml` completed successfully during Phase 003A.

Current required Prometheus jobs:

- `prometheus`
- `node_exporter`
- `blackbox_dns`
- `blackbox_dns_local`

Current required Blackbox modules:

- `dns_udp`
- `dns_udp_local`

The local DNS job and module were added after the original Phase 003A inventory and are now part of the required recovery baseline.

Local `.bak-*` files are useful short-term rollback artifacts but are not a protected backup system.

## Milestones

| Milestone | Status | Completion criteria |
| --- | --- | --- |
| 1. Create backup inventory | Complete | Systems have documented roles, recovery priorities, and intended backup methods. |
| 2. Verify configuration locations | Complete | Live configuration, service state, package versions, storage footprints, and state classifications are documented. |
| 3. Export existing Grafana dashboards | Complete | Node Exporter and Service Health JSON files exist outside Git and passed syntax/private inspection. |
| 4. Export Pi-hole configuration | Complete | Teleporter ZIP exists outside Git and passed integrity/private inspection. |
| 5. Draft recovery notes | Complete | Application-level dependencies and service-export procedure are documented but untested. |
| 6. Export Infrastructure Overview | Pending | Classic JSON exists outside Git and passes syntax and private inspection. |
| 7. Configure backup storage | Pending target availability | 5 TB drive is mounted and registered in Proxmox. |
| 8. Run initial VM backups | Pending | Backups complete successfully and retention is documented. |
| 9. Perform restore test | Pending | A representative VM restore succeeds and service validation is documented. |
| 10. Final documentation review | Pending | Runbooks, architecture, service pages, changelog, and link validation reflect tested results. |

## Validation Plan

Completed during Phase 003A:

- Confirmed inventoried services are active and enabled.
- Validated Prometheus configuration with `promtool`.
- Confirmed then-current Prometheus jobs.
- Validated application-export syntax or archive integrity.
- Inspected exports without publishing private values.
- Ran the repository Markdown link validator at that milestone.

Required during backup implementation and restore testing:

- Inspect the external drive and confirm expected capacity.
- Confirm the backup target is mounted consistently.
- Confirm Proxmox backup jobs report success and produce reasonable artifacts.
- Confirm retention and pruning behave as documented.
- Restore at least one representative VM in an isolated or controlled state.
- Confirm Pi-hole answers public and local DNS queries after recovery.
- Confirm Node Exporter metrics recover for all intended targets.
- Confirm both `blackbox_dns` and `blackbox_dns_local` return success.
- Confirm Grafana reconnects to Prometheus and imports all protected dashboard exports.
- Verify imported panels and variables against the recreated data source.
- Confirm the Homelab Infrastructure Overview shows all three hosts and both DNS states.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Raw exports expose private values | High | Store exports outside Git and commit only sanitized documentation. |
| Teleporter archive contains authentication and network state | High | Preserve it only in protected storage and avoid printing values during inspection. |
| Raw copies of live Pi-hole state are inconsistent | High | Use Teleporter for portable recovery and Proxmox backup for whole-system recovery. |
| Grafana dashboards depend on local database state | High | Preserve `grafana.db` consistently and maintain portable dashboard JSON. |
| Dashboard import does not bind to the intended data source | High | Create and validate the Prometheus data source before importing dashboards. |
| Backup target is accidentally treated as primary storage | High | Keep the external drive dedicated to backup and document content types. |
| Backup completes but restore fails | High | Require a representative restore test before completion. |
| Local DNS monitoring is omitted during rebuild | Medium | Require `blackbox_dns_local` and `dns_udp_local` in the recovery checklist. |
| Draft runbooks are mistaken for tested procedures | Medium | Retain explicit planned or unvalidated labels until exercised. |
| Historical Prometheus metrics are lost | Low / Medium | Prioritize configuration and dashboard recovery; document retention separately. |
| Local rollback files are mistaken for backups | Medium | Treat `.bak-*` files only as temporary change rollback copies. |

## Recovery Order

1. Restore physical network connectivity and Proxmox management access.
2. Restore `dns01` and validate public and local DNS behavior.
3. Restore `mon01` and validate Prometheus, Node Exporter, Blackbox Exporter, and Grafana.
4. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
5. Review logs and update documentation with any recovery differences.

## Preliminary Manual Recovery Notes

### `dns01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM with `ifupdown` networking.
3. Recreate static networking using protected operational values.
4. Reinstall Pi-hole and Node Exporter.
5. Import the protected Teleporter archive.
6. Confirm upstream DNS settings and required local records.
7. Confirm `pihole-FTL` and `prometheus-node-exporter` are active and enabled.
8. Validate public resolution, local records, Node Exporter metrics, and both Blackbox DNS jobs.

### `mon01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM.
3. Reinstall supported versions of Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
4. Restore or recreate `/etc/prometheus/prometheus.yml` and `/etc/prometheus/blackbox.yml`.
5. Validate Prometheus and confirm `prometheus`, `node_exporter`, `blackbox_dns`, and `blackbox_dns_local` exist.
6. Confirm Blackbox modules `dns_udp` and `dns_udp_local` exist and preflight successfully.
7. Restore Grafana through a consistency-preserving SQLite backup, or recreate the Prometheus data source.
8. Import all protected dashboard JSON files available at recovery time.
9. Verify Prometheus data-source mapping for all panels and variables.
10. Reinstall required non-bundled plugins.
11. Confirm all four services are active and enabled.
12. Validate all host targets, both DNS probes, and Grafana panels.

These procedures remain unvalidated until a controlled restore or rebuild test succeeds.

## Results to Date

- Completed live backup-readiness inventories for `dns01` and `mon01`.
- Created and privately inspected the Pi-hole Teleporter ZIP.
- Created and privately inspected the existing Grafana dashboard exports.
- Classified Grafana plugin content and Prometheus metrics history.
- Verified the Grafana Prometheus data-source recovery mapping.
- Added a reusable service configuration export and inspection runbook.
- Updated the monitoring recovery baseline for the local DNS job and infrastructure overview.
- Confirmed raw exports must remain outside Git.

## Lessons Learned

- Configuration directories can mix essential state, generated data, credentials, logs, and active databases.
- Directory size does not indicate recovery importance.
- Export formats and filenames should be verified from the generated artifact rather than assumed.
- Valid Prometheus syntax does not prove all intended jobs remain present.
- Package-provided provisioning samples do not protect Grafana state created through the web interface.
- Dashboard exports do not necessarily preserve automatic data-source binding.
- Archive integrity validation does not make an export safe to publish.
- A portable export is not a validated backup until an import or restore succeeds.
- Recovery inventories must be updated whenever monitoring jobs, dashboards, or service dependencies change.

## Follow-Up Tasks

- [x] Create the initial backup inventory and recovery priorities.
- [x] Verify `dns01` configuration, service, package, and network state.
- [x] Create and protect the Pi-hole Teleporter archive.
- [x] Inspect the Teleporter archive privately.
- [x] Verify `mon01` configuration, package, service, and storage state.
- [x] Classify Grafana and Prometheus local state.
- [x] Export and inspect the Node Exporter and Service Health dashboards.
- [x] Document the Grafana data-source recovery mapping.
- [x] Add `docs/runbooks/service-config-export.md`.
- [x] Update recovery requirements for `blackbox_dns_local` and `dns_udp_local`.
- [ ] Export and privately validate the Homelab Infrastructure Overview.
- [ ] Inspect, prepare, mount, and register the 5 TB backup target.
- [ ] Expand `docs/runbooks/backup.md` with the selected schedule and retention.
- [ ] Run initial VM backups for `dns01` and `mon01`.
- [ ] Perform and document a representative isolated restore.
- [ ] Expand `docs/runbooks/disaster-recovery.md` from restore-test findings.
- [ ] Add `docs/runbooks/proxmox-vm-restore.md`.
- [ ] Update storage architecture after implementation details are validated.
- [ ] Run the Markdown link validator and review GitHub Actions before project completion.

## Related Documentation

- [Projects README](README.md)
- [Service Configuration Export and Inspection Runbook](../runbooks/service-config-export.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Hardware Inventory](../hardware/inventory.md)
- [Pi-hole Service](../services/pihole.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
