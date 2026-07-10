# Grafana

## Status

Active

## Purpose

Grafana provides dashboarding and visualization for the homelab monitoring stack. It connects to Prometheus as a data source and displays collected metrics in human-readable dashboards.

Grafana helps answer operational questions such as:

- Are monitored systems healthy at a glance?
- How are CPU, memory, disk, and network usage trending?
- Which host or service needs attention first?
- Is the monitoring stack collecting usable data?
- Are critical services, such as DNS, currently available?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Grafana |
| Package | `grafana` version `13.1.0` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Deployment method | Grafana APT repository |
| Default port | `3000/tcp` |
| Data source | Prometheus on `http://localhost:9090` |
| Current dashboards | Imported Node Exporter dashboard; Homelab Service Health dashboard |
| Backup maturity | Dashboard exports and data-source recovery mapping complete; VM backup and restore validation pending |

## Host

| Hostname | Role |
| --- | --- |
| `mon01` | Dedicated monitoring VM |

Exact private addresses are intentionally omitted. Use `<MON01_IP>` and `<DNS01_IP>` in public documentation.

## Deployment Notes

Grafana was installed from the Grafana APT repository so it can be maintained through normal Debian package management.

High-level deployment steps:

1. Added the Grafana APT signing key under `/etc/apt/keyrings/`.
2. Added the Grafana stable APT repository under `/etc/apt/sources.list.d/`.
3. Refreshed package indexes.
4. Installed the `grafana` package.
5. Enabled and started `grafana-server`.
6. Configured Prometheus as the first data source.
7. Imported a Node Exporter dashboard.
8. Created the Homelab Service Health dashboard manually.

Verified service baseline:

| Item | State |
| --- | --- |
| Systemd unit | `/usr/lib/systemd/system/grafana-server.service` |
| Unit overrides | None detected |
| Runtime state | Active and running |
| Boot state | Enabled |

## Data Sources

### Prometheus

| Setting | Value |
| --- | --- |
| Name | `prometheus` |
| Type | `prometheus` |
| URL | `http://localhost:9090` |
| Access scope | Local from `mon01` |
| Status | Successfully tested |
| Current UID | Retained privately as `<PROMETHEUS_DATASOURCE_UID>` |
| Storage model | Stored in local Grafana database state |

`localhost` is used because Grafana and Prometheus run on the same VM.

The data-source name, type, and current UID were verified through a read-only query against `/var/lib/grafana/grafana.db`. The exact UID is environment-specific and is retained with the private recovery artifacts rather than published in the repository.

The current provisioning directories contain only package-provided sample files. The active Prometheus data source is therefore not represented as portable provisioning configuration. Recovery currently requires either:

- A consistency-preserving restore of `grafana.db`.
- Manual recreation of a Prometheus data source named `prometheus` with URL `http://localhost:9090`.

### Dashboard Import Mapping

Private inspection of both dashboard exports found:

- No `__inputs` section.
- No explicit `datasource` object discovered by the inspection script.
- No sensitive-looking credential property names.

The exports must not be assumed to bind automatically to the intended data source. During recovery:

1. Create or restore the Prometheus data source first.
2. Import each dashboard.
3. Select or verify the Prometheus data source for panels and variables.
4. Confirm the `node_exporter` and `blackbox_dns` queries return current data.
5. Record any newly assigned UID if the original UID is not preserved.

## Dashboards

### Imported Node Exporter Dashboard

The imported Node Exporter dashboard provides host-level visibility for `mon01` and `dns01`.

Current behavior:

- Prometheus is selected as the dashboard data source.
- The `node_exporter` job exposes both monitored hosts.
- Dashboard variables may require the correct job selection after import.
- The export is large because panel definitions, queries, variables, thresholds, and formatting are embedded in JSON.

Protected export:

| Item | Value |
| --- | --- |
| Filename | `node-exporter-dashboard.json` |
| Logical size | 723,648 bytes |
| JSON validation | Successful |
| Storage | Private location outside Git |

### Homelab Service Health Dashboard

The custom service health dashboard visualizes service-level checks separately from host metrics.

| Panel | Prometheus metric | Purpose |
| --- | --- | --- |
| `dns01 DNS Availability` | `probe_success` for `blackbox_dns` | Shows whether the DNS probe is succeeding |
| `dns01 DNS Probe Duration` | `probe_duration_seconds` for `blackbox_dns` | Shows probe response time over time |
| `dns01 DNS Probe Status` | `probe_success` for `blackbox_dns` | Shows probe state over time |

Protected export:

| Item | Value |
| --- | --- |
| Filename | `homelab-service-health-dashboard.json` |
| Logical size | 11,873 bytes |
| JSON validation | Successful |
| Storage | Private location outside Git |

Both dashboard exports were inspected privately on 2026-07-10. They contain expected internal environment values, including private addressing, but no JSON property names suggesting passwords, secrets, API keys, authorization headers, bearer values, or authentication tokens. The original exports must remain outside the public repository unless sanitized copies are created.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `3000/tcp` |
| Access scope | Internal homelab only |
| Public exposure | None |
| Browser access | `http://<MON01_IP>:3000` |

Grafana should remain internal-only. Do not expose it directly to the public internet.

## Local State Inventory

| Item | Verified location or size |
| --- | --- |
| Main configuration | `/etc/grafana/grafana.ini` |
| Configuration directory | Approximately 156 KB under `/etc/grafana/` |
| Provisioning directory | `/etc/grafana/provisioning/`; sample files only |
| SQLite database | `/var/lib/grafana/grafana.db`, approximately 2.2 MB |
| Installed plugins | Approximately 112 MB under `/var/lib/grafana/plugins/` |
| Bundled plugins | Approximately 64 MB under `/var/lib/grafana/plugins-bundled/` |
| CSV export directory | Approximately 4 KB |
| PDF export directory | Approximately 4 KB |
| PNG export directory | Approximately 4 KB |
| Unified-search state | Approximately 8 KB |

Approximately 176 MB of the 177 MB Grafana state directory is plugin content. Operationally unique recovery state is concentrated primarily in:

- `grafana.db`
- Dashboard JSON exports
- Prometheus data-source settings
- Modified Grafana configuration
- Any future non-bundled plugin requirements

Plugin directories are mostly replaceable through package or plugin reinstallation. They should not be treated as more important merely because they occupy more space.

## Validation Procedure

Run on `mon01`:

```bash
systemctl is-active grafana-server
systemctl is-enabled grafana-server
curl -I localhost:3000
```

Expected results:

- The service is active.
- The service is enabled.
- The HTTP request returns a response, commonly a redirect to `/login`.

Validate from the Grafana web interface:

1. Confirm the Prometheus data source test succeeds.
2. Open the imported Node Exporter dashboard.
3. Select the `node_exporter` job.
4. Confirm `mon01` and `dns01` are available.
5. Confirm host panels display current data.
6. Open the Homelab Service Health dashboard.
7. Confirm DNS availability reports success.
8. Confirm duration and status-history panels contain data.

Dashboard export validation on the private workstation:

```powershell
Get-Content <DASHBOARD_JSON> -Raw | ConvertFrom-Json
```

A successful parse verifies JSON syntax. It does not prove that the dashboard will import correctly against a recreated data source, so a controlled import test remains required.

## Security Considerations

- Change the default administrative password during initial setup.
- Store Grafana credentials in a password manager, not in Git.
- Keep Grafana internal-only.
- Do not expose port `3000` to untrusted networks.
- Treat dashboards as operationally sensitive.
- Do not publish screenshots or raw JSON containing internal addresses, usernames, private URLs, tokens, or topology details.
- Use placeholders such as `<MON01_IP>`, `<DNS01_IP>`, and `<PROMETHEUS_DATASOURCE_UID>` in public documentation.
- Keyword matches such as `token` do not automatically prove a secret exists; inspect JSON property paths without printing values.
- Preserve original recovery exports outside Git even when sanitized portfolio copies are later created.

## Backup Strategy

Grafana recovery uses multiple layers:

1. **Proxmox VM backup**
   - Preserves the complete VM, package installation, plugins, database, and configuration.
   - Remains unvalidated until a restore test succeeds.

2. **Consistent Grafana database backup**
   - Protects dashboards, users, data sources, and other local database state.
   - Direct copies must use a procedure that preserves SQLite consistency.

3. **Dashboard JSON exports**
   - Provide portable dashboard recovery independent of the local database.
   - Require data-source verification during import.
   - Raw exports remain private because they contain environment-specific values.

4. **Data-source recovery record**
   - Records the data-source name, type, URL, and current UID.
   - The exact UID remains in private storage; public documentation uses a placeholder.

5. **Sanitized documentation**
   - Records package versions, paths, dependencies, state classification, and validation steps.
   - Excludes credentials and exact internal addressing.

The current application-level backup milestone covers dashboard export, inspection, and data-source recovery mapping. The full backup design is incomplete until Proxmox backup storage is available and restore testing succeeds.

## Recovery Procedure

1. Restore the validated VM backup when available.
2. For a manual rebuild, install a supported Grafana version on `mon01`.
3. Restore modified configuration from `/etc/grafana/` as appropriate.
4. Restore `grafana.db` using a consistency-preserving procedure, or recreate the Prometheus data source manually.
5. When recreating the data source, use:
   - Name: `prometheus`
   - Type: `prometheus`
   - URL: `http://localhost:9090`
   - UID: protected value represented publicly as `<PROMETHEUS_DATASOURCE_UID>`, or a newly assigned UID that is recorded after creation
6. Reinstall required non-bundled plugins.
7. Import the Node Exporter dashboard JSON.
8. Import the Homelab Service Health dashboard JSON.
9. Select or verify the Prometheus data source for imported panels and variables.
10. Confirm `grafana-server` is active and enabled.
11. Confirm both dashboards display current Prometheus data.

This procedure remains a draft recovery baseline until exercised during a controlled restore or rebuild test.

## Troubleshooting Notes

### Grafana Package Not Found

If APT cannot locate Grafana from the third-party repository:

- Verify the repository file exists under `/etc/apt/sources.list.d/`.
- Verify the signing key and architecture.
- Run `apt-get update` and inspect repository errors.
- Retry installation only after the package appears in APT metadata.

### Service Active but Port Check Is Unclear

Use an application-layer request before assuming the service is broken:

```bash
curl -I localhost:3000
```

A redirect to `/login` confirms Grafana is responding.

### Imported Dashboard Job Selector

Imported dashboards may expect different Prometheus job names. Select or adjust the `node_exporter` job and refresh variables after adding or restoring targets.

### Dashboard Import Has No Data

Check in this order:

1. The Prometheus data source exists and passes **Save & test**.
2. Imported panels and variables reference the intended data source.
3. Prometheus contains the `node_exporter` and `blackbox_dns` jobs.
4. Expected targets are `UP`.
5. Dashboard job and host variables are refreshed.

### Empty Service Health Panels

Check the dependency chain in order:

1. Grafana data source
2. Prometheus service and target health
3. `blackbox_dns` job presence
4. Blackbox Exporter local endpoint
5. Manual DNS probe result

Grafana is often where a monitoring failure becomes visible, not where it originates.

## Maintenance Notes

- Keep Grafana updated through normal package management.
- Export dashboards after meaningful changes.
- Review data-source health after Prometheus changes.
- Avoid storing secrets in dashboards, panel queries, or documentation.
- Keep dashboard labels aligned with Prometheus job labels.
- Record any manually installed plugins.
- Update the private data-source recovery record if its UID changes.
- Repeat private export inspection before publishing a sanitized dashboard copy.
- Update Project 003 after backup or restore validation.

## Future Improvements

- Create reviewed provisioning files for the Prometheus data source and dashboards.
- Create sanitized dashboard copies suitable for version control.
- Build a custom Linux host dashboard for `mon01` and `dns01`.
- Add Pi-hole-specific panels after metrics are available.
- Add Proxmox and backup-health panels after those systems are monitored.
- Validate Grafana database backup and restore.
- Add authentication and reverse-proxy design only if broader access is needed.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Node Exporter Service](node-exporter.md)
- [VM Inventory](../architecture/vm-inventory.md)
