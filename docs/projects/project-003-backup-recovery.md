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

The external backup target is not yet available. This phase identifies the state that must be preserved, records sanitized configuration locations, creates portable service exports, and drafts recovery procedures before automated VM backups are configured.

## Purpose

Establish a documented and testable backup and recovery process for the homelab.

The guiding question for each system is:

> If this VM failed tonight, what information and service state would be required to rebuild it?

Full-VM backups are valuable, but they are not a substitute for understanding service configuration, dependencies, portable exports, and validation requirements.

## Objectives

- Identify critical configuration and service state on `dns01` and `mon01`.
- Assign recovery priority based on service dependencies and operational impact.
- Record verified configuration paths, package versions, storage footprints, and service dependencies.
- Export Pi-hole configuration and Grafana dashboards for protected storage and inspection.
- Keep raw exports and sensitive values outside the public repository.
- Draft service recovery notes before implementing the final Proxmox backup target.
- Configure and validate VM backups after the external backup drive is available.
- Perform at least one representative restore test and document the result.

## Scope

### Phase 003A

- `dns01` configuration and recovery inventory.
- `mon01` configuration and recovery inventory.
- Pi-hole Teleporter export.
- Grafana dashboard JSON exports.
- Prometheus and Blackbox Exporter configuration inventory.
- Grafana data-source and local-state inventory.
- Node Exporter package and service-state inventory.
- Sanitized rebuild and recovery notes.
- Identification of sensitive values that must remain outside Git.

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
- Publishing raw exports containing internal addresses, credentials, tokens, private keys, query history, or sensitive topology details.

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
| Mark runbooks as planned until tested | Prevents draft instructions from being mistaken for validated procedures. | Documentation matures incrementally. |
| Prefer Pi-hole Teleporter over a raw live directory copy | `/etc/pihole/` contains active databases, authentication data, TLS material, and generated state. | The Teleporter archive still requires protected storage and inspection. |
| Preserve Prometheus configuration separately from metrics history | Configuration is small and essential; short-term historical metrics are less critical at the current scale. | A manual rebuild may lose historical monitoring data. |
| Export Grafana dashboards even when `grafana.db` is protected | Portable JSON reduces dependence on one local database and is easier to inspect and import. | Exports and data-source mappings must be maintained after meaningful changes. |
| Treat Grafana plugin directories as replaceable content | Plugin files account for nearly all Grafana state-directory usage and can be restored through VM backup or reinstallation. | Custom or externally installed plugins must still be recorded if introduced later. |
| Store the current Grafana data-source UID privately | The UID helps reproduce the current mapping, but it is environment-specific and unnecessary in a public architecture document. | Manual recovery must use the protected UID record or validate a newly assigned UID after import. |

## Backup Inventory

| System | Role | Planned backup method | Restore priority | Current status |
| --- | --- | --- | --- | --- |
| `dns01` | DNS and Pi-hole | Proxmox VM backup, Pi-hole Teleporter export, and sanitized rebuild notes | High | Live inventory complete. Teleporter ZIP exists outside Git; private content inspection remains pending. |
| `mon01` | Monitoring and observability | Proxmox VM backup, reviewed configuration copies, dashboard JSON exports, and sanitized rebuild notes | Medium | Live inventory, state classification, dashboard export, dashboard inspection, and data-source recovery mapping are complete. VM backup and restore validation remain pending. |

## Configuration Inventory

### `dns01` — Verified

| Item | Verified location or state |
| --- | --- |
| Pi-hole state directory | `/etc/pihole/`, approximately 16 MB during inventory |
| Pi-hole portable export | Teleporter ZIP created on 2026-07-09; 23,868 bytes; stored outside Git |
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
| Pi-hole versions | Core v6.4.3, Web v6.6, FTL v6.7 |

The host resolver does not depend on Pi-hole itself. This reduces circular dependency during troubleshooting or recovery, but DNS queries originating from `dns01` bypass local Pi-hole filtering.

The `/etc/pihole/` directory mixes configuration, gravity databases, local host data, generated backups, query-history databases, active SQLite files, authentication material, and TLS-related files. Raw directory contents must not be committed to the public repository.

The original Teleporter ZIP remains intact outside the repository. Any extracted inspection copy must also remain in protected private storage.

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
| Grafana generated export directories | `csv/`, `pdf/`, and `png/`; approximately 4 KB each |
| Grafana unified-search state | Approximately 8 KB under `/var/lib/grafana/unified-search/` |
| Node Exporter dashboard export | `node-exporter-dashboard.json`, 723,648 bytes; stored outside Git |
| Service Health dashboard export | `homelab-service-health-dashboard.json`, 11,873 bytes; stored outside Git |
| Grafana Prometheus data source | Name `prometheus`; type `prometheus`; URL `http://localhost:9090`; current UID retained privately as `<PROMETHEUS_DATASOURCE_UID>` |

Approximately 176 MB of the 177 MB Grafana state directory is plugin content. Operationally unique state is concentrated primarily in `grafana.db`, dashboard JSON, data-source configuration, modified settings, and any future custom plugin requirements.

Both dashboard exports were validated as syntactically valid JSON on 2026-07-10. Private inspection found expected internal addressing but no JSON property names suggesting passwords, secrets, API keys, authorization headers, bearer values, or authentication tokens. The original files remain outside Git because they contain environment-specific values.

The exported dashboard models contained no `__inputs` section and no explicit `datasource` object discovered by the private inspection script. Recovery must therefore create or validate the Prometheus data source before import and verify panel mappings afterward instead of assuming automatic data-source binding.

The active data-source record was verified with a read-only query against `grafana.db`. The exact UID is retained with the private exports and is represented publicly by `<PROMETHEUS_DATASOURCE_UID>`.

A full VM backup should preserve the complete installation. For application-level recovery, the priority is the SQLite database, reviewed dashboard JSON, data-source details, modified Grafana configuration, and a record of any non-bundled plugins. Direct SQLite file copies must use a procedure that preserves database consistency.

#### Prometheus Validation

`promtool check config /etc/prometheus/prometheus.yml` completed successfully.

Verified scrape job names:

- `prometheus`
- `node_exporter`
- `blackbox_dns`

The configuration directory also contains several manually created `.bak-*` copies. These are useful short-term rollback artifacts but are not a substitute for protected, versioned, and tested backups.

## Milestones

| Milestone | Status | Completion criteria |
| --- | --- | --- |
| 1. Create backup inventory | Complete | Both systems have documented roles, recovery priorities, and intended backup methods. |
| 2. Verify configuration locations | Complete | Live configuration, service state, package versions, storage footprints, and state classification are documented for `dns01` and `mon01`. |
| 3. Export Grafana dashboards | Complete | Both JSON files exist outside Git, parse successfully, and were privately inspected for sensitive fields and environment-specific values. |
| 4. Export Pi-hole configuration | In Progress | Teleporter archive exists outside Git; private content inspection remains pending. |
| 5. Draft recovery notes | In Progress | `mon01` application-level recovery mapping is documented; remaining runbooks and tested procedures are pending. |
| 6. Configure backup storage | Blocked | External backup target is mounted and added to Proxmox storage. |
| 7. Run initial VM backups | Blocked | Backups complete successfully and retention is documented. |
| 8. Perform restore test | Blocked | A representative VM restore succeeds and service validation is documented. |
| 9. Final documentation review | Not Started | Runbooks, service pages, storage architecture, project status, roadmap, and changelog agree. |

## Validation Plan

- Confirm inventoried services are active and enabled.
- Validate Prometheus configuration with `promtool`.
- Confirm expected Prometheus jobs remain present with PromQL.
- Confirm Pi-hole answers public and local DNS queries after recovery.
- Confirm Node Exporter and Blackbox Exporter metrics recover.
- Confirm Grafana can reconnect to Prometheus and import both dashboard exports.
- Verify imported dashboard panels against the recreated Prometheus data source.
- Confirm Proxmox backup jobs report success and produce reasonable artifacts.
- Restore at least one representative VM in an isolated or controlled state.
- Run `python scripts/check-markdown-links.py` after documentation changes.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Raw exports expose private values | High | Store exports outside Git and commit only sanitized artifacts. |
| Raw copies of live Pi-hole state are inconsistent | High | Use Teleporter for portable configuration and Proxmox backup for whole-system recovery. |
| Grafana dashboards depend on local database state | High | Preserve `grafana.db` consistently and maintain portable dashboard JSON. |
| Inconsistent direct copy of `grafana.db` | High | Use a controlled backup procedure that preserves SQLite integrity. |
| Dashboard import does not bind to the intended data source | High | Create and test the Prometheus data source first, then verify every imported dashboard. |
| Backup target resides on the source disk | High | Use the planned external drive. |
| Backup completes but restore fails | High | Require a representative restore test before project completion. |
| Recovery notes omit dependencies | Medium | Record network assumptions, startup state, data sources, exporters, and validation checks. |
| Draft runbooks are mistaken for tested procedures | Medium | Retain planned or draft labels until executed successfully. |
| Historical Prometheus metrics are lost in a manual rebuild | Low / Medium | Prioritize configuration and dashboard recovery; document retention separately. |
| Manual `.bak-*` files are mistaken for a backup system | Medium | Treat them only as local rollback copies and use protected external backups for recovery. |

## Recovery Order

1. Restore basic network and Proxmox management access.
2. Restore `dns01` and validate DNS operation.
3. Restore `mon01` and validate Prometheus, exporters, and Grafana.
4. Confirm monitoring observes both restored systems.
5. Review logs and update documentation with any recovery differences.

## Preliminary Manual Recovery Notes

### `dns01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM with `ifupdown` networking.
3. Recreate the static interface configuration in `/etc/network/interfaces` using protected operational values.
4. Reinstall Pi-hole and Node Exporter.
5. Restore the protected Pi-hole Teleporter archive or recreate equivalent settings manually.
6. Confirm upstream DNS configuration and local DNS records.
7. Confirm `pihole-FTL` and `prometheus-node-exporter` are active and enabled.
8. Validate public DNS queries, local records, Node Exporter metrics, and the Blackbox DNS probe.

### `mon01`

1. Restore the VM backup when available.
2. For a manual rebuild, deploy a supported Debian VM with documented baseline administration and networking.
3. Reinstall supported versions of Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
4. Restore or recreate `/etc/prometheus/prometheus.yml` and `/etc/prometheus/blackbox.yml`.
5. Validate Prometheus configuration before restart and confirm the `prometheus`, `node_exporter`, and `blackbox_dns` jobs exist.
6. Restore Grafana through a consistent SQLite backup, or create a Prometheus data source named `prometheus` with type `prometheus` and URL `http://localhost:9090`.
7. Use the protected UID record when preserving the existing mapping, or record and validate the newly assigned UID.
8. Import the reviewed Node Exporter and Homelab Service Health dashboard JSON files.
9. Select or verify the Prometheus data source for all imported panels and variables.
10. Reinstall any required non-bundled plugins.
11. Confirm all four services are active and enabled.
12. Validate Prometheus target health, required PromQL queries, DNS probes, and Grafana panels.

These procedures remain unvalidated until a controlled restore or rebuild test succeeds.

## Results

- **Completed:** Initial backup inventory and live configuration inventory for both `dns01` and `mon01`.
- **Created:** A 23,868-byte Pi-hole Teleporter ZIP stored outside the public repository.
- **Created and validated:** A 723,648-byte Node Exporter dashboard JSON export stored outside Git.
- **Created and validated:** An 11,873-byte Homelab Service Health dashboard JSON export stored outside Git.
- **Verified on `dns01`:** Pi-hole state location and size, Pi-hole versions, service unit paths, runtime and boot state, Node Exporter package version, and static network configuration path.
- **Verified on `mon01`:** Four active and enabled monitoring services, package versions, standard package unit paths, configuration locations, storage footprints, Grafana database location, valid Prometheus syntax, and expected scrape job names.
- **Classified:** Grafana state is approximately 112 MB installed plugins, 64 MB bundled plugins, 2.2 MB SQLite database, and negligible generated-export/search directories.
- **Classified:** Prometheus local state is approximately 59 MB of metrics history under `metrics2`, plus negligible Node Exporter collector state.
- **Verified:** Grafana Prometheus data source name, type, local URL, and current UID through a read-only SQLite query; the exact UID remains private.
- **Inspection result:** Dashboard JSON contains internal environment values but no sensitive-looking credential property names. Raw exports remain private.
- **Failed:** Initial PowerShell instructions incorrectly assumed a `.tar.gz` Teleporter format; the actual export is a ZIP archive. The workflow was corrected without affecting the export.
- **Design finding:** `dns01` host resolution is independent of Pi-hole, reducing circular dependency while bypassing local filtering for host-originated queries.
- **Design finding:** Grafana dashboards and data source are not actively provisioned from files, increasing the importance of JSON exports, data-source recovery notes, and local database protection.
- **Remaining:** Private Teleporter inspection, backup implementation, runbook expansion, and restore testing.

## Lessons Learned

- Configuration directories can mix essential state, generated data, credentials, certificates, logs, and active databases.
- A small configuration footprint does not make a directory safe for public version control.
- Recovery planning must verify runtime state, boot-time enablement, unit locations, package versions, network configuration, and data locations.
- Host-level resolver configuration can create an intentional resilience tradeoff that should be documented explicitly.
- Export formats should be verified from the generated artifact rather than assumed.
- Windows `Size` is the logical file length; `Size on disk` reflects filesystem allocation.
- Valid Prometheus syntax does not prove the intended jobs exist; job-name and target validation remain necessary.
- Package-provided sample provisioning files do not protect dashboards or data sources created through the Grafana UI.
- Local `.bak-*` files improve short-term rollback but do not replace external backups and restore testing.
- Directory size alone does not indicate recovery importance; replaceable plugin binaries can occupy far more space than unique application state.
- Imported dashboards can produce very large JSON exports because panel definitions, queries, variables, thresholds, and formatting are embedded in the file.
- Keyword matches in JSON do not automatically indicate a secret; property-path inspection can distinguish sensitive fields from ordinary dashboard content without exposing values.
- Dashboard exports do not necessarily preserve automatic data-source binding, so recovery validation must include explicit panel and variable checks.

## Follow-Up Tasks

- [x] Create the initial backup inventory and recovery priorities.
- [x] Verify `dns01` configuration locations, service definitions, package version, and live network configuration.
- [x] Create and protect the Pi-hole Teleporter archive.
- [ ] Inspect the Teleporter archive privately for sensitive or environment-specific content.
- [x] Verify all `mon01` configuration locations, package versions, service definitions, and storage footprints.
- [x] Classify additional content under `/var/lib/grafana/` beyond `grafana.db`.
- [x] Classify Prometheus local data under `/var/lib/prometheus/`.
- [x] Export both Grafana dashboards to protected JSON files.
- [x] Validate and inspect both dashboard exports privately.
- [x] Document the Grafana Prometheus data-source recovery requirements.
- [ ] Expand `docs/runbooks/backup.md` with the selected schedule and retention.
- [ ] Expand `docs/runbooks/disaster-recovery.md` with tested recovery order.
- [ ] Add `docs/runbooks/proxmox-vm-restore.md`.
- [ ] Add `docs/runbooks/service-config-export.md`.
- [ ] Update `docs/architecture/storage.md` after the backup target is implemented.
- [ ] Run the Markdown link validator.
- [ ] Record completed Phase 003A and implementation milestones in `CHANGELOG.md`.

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
