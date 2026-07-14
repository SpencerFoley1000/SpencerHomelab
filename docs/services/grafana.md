# Grafana

## Status

Active

## Purpose

Grafana visualizes homelab metrics from Prometheus for troubleshooting, capacity review, and rapid health checks.

Current dashboards answer:

- Are `mon01`, `dns01`, and `pve01` reporting metrics?
- How are CPU, memory, filesystem use, and uptime changing?
- Are recursive and local DNS checks both succeeding?
- Is DNS probe duration changing or spiking?

## Technology Stack

| Component | Value |
| --- | --- |
| Package version | `13.1.0` |
| Host | `mon01` |
| Operating system | Debian 13.5 Trixie |
| Data source | Prometheus at `http://localhost:9090` |
| Listen port | TCP `3000` |
| Access | Internal homelab only |
| Public exposure | None |
| Backup maturity | Daily `mon01` VM backup active; existing dashboard exports protected; independent VM restore not yet tested |

Exact addresses, data-source identifiers, raw dashboard JSON, and credentials remain outside the repository.

## Data Source

| Setting | Value |
| --- | --- |
| Name | `prometheus` |
| Type | Prometheus |
| URL | `http://localhost:9090` |
| UID | Retained privately as `<PROMETHEUS_DATASOURCE_UID>` |
| Storage | Grafana local database |

Grafana and Prometheus share `mon01`, so the data source uses `localhost`.

The active data source is not yet managed through reviewed provisioning files. Recovery requires either:

- a consistency-preserving restore of `grafana.db`, or
- manual data-source recreation before dashboard import.

## Current Dashboards

### Imported Node Exporter Dashboard

Purpose:

- Detailed CPU, memory, filesystem, disk, network, and uptime views.
- Multi-host troubleshooting through the shared `node_exporter` job.

Hosts:

- `mon01`
- `dns01`
- `pve01`

A protected JSON export exists outside Git and passed private syntax inspection.

### Homelab Service Health

Purpose:

- Separate DNS service behavior from host health.
- Display current availability, response duration, and state history.

A protected JSON export exists outside Git and passed private syntax inspection.

### Homelab Infrastructure Overview

Created manually on 2026-07-11.

| Panel | Visualization | Purpose |
| --- | --- | --- |
| Host Availability | Stat | Current state of all three Node Exporter targets |
| CPU Utilization by Host | Time series | Compare CPU demand |
| Memory Utilization by Host | Time series | Compare memory pressure |
| Root Filesystem Utilization | Gauge | Show capacity risk |
| Host Uptime | Stat | Show time since boot |
| DNS Availability | Stat | Show Recursive DNS and Local DNS independently |
| DNS Probe Duration | Time series | Show recursive DNS latency and spikes |

The dashboard is operational. Its protected Classic JSON export remains pending and must not be described as a portable recovery artifact yet.

## Key PromQL

Host availability:

```promql
up{job="node_exporter"}
```

CPU utilization:

```promql
100 - (
  avg by (host) (
    rate(node_cpu_seconds_total{job="node_exporter", mode="idle"}[5m])
  ) * 100
)
```

Memory utilization:

```promql
100 * (
  1 -
  node_memory_MemAvailable_bytes{job="node_exporter"}
  /
  node_memory_MemTotal_bytes{job="node_exporter"}
)
```

Root filesystem utilization:

```promql
100 * (
  1 -
  node_filesystem_avail_bytes{job="node_exporter", mountpoint="/", fstype!~"tmpfs|overlay"}
  /
  node_filesystem_size_bytes{job="node_exporter", mountpoint="/", fstype!~"tmpfs|overlay"}
)
```

Host uptime:

```promql
time() - node_boot_time_seconds{job="node_exporter"}
```

Recursive DNS:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

Local DNS:

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Probe duration:

```promql
probe_duration_seconds{job="blackbox_dns", host="dns01"}
```

## Dashboard Design Decisions

### Summary and Detail Separation

The Infrastructure Overview provides rapid status. The imported Node Exporter dashboard supports detailed host troubleshooting.

### Full-Width Trend Panels

Longer trend panels use the dashboard width to improve visibility into gradual changes and latency spikes.

### Uptime Is Informational

A recent reboot is not automatically a fault, so uptime does not use misleading critical thresholds.

### Independent DNS States

Recursive DNS and Local DNS remain separate so an upstream outage cannot hide healthy local records and vice versa.

## Validation

Service checks:

```bash
systemctl is-active grafana-server
systemctl is-enabled grafana-server
curl -I localhost:3000
```

Dashboard checks:

1. Confirm the Prometheus data source passes **Save & test**.
2. Confirm `mon01`, `dns01`, and `pve01` show current data.
3. Confirm CPU, memory, filesystem, and uptime panels populate.
4. Confirm Recursive DNS and Local DNS both show expected state.
5. Confirm DNS probe duration updates.
6. Confirm labels do not expose private addresses.

## Troubleshooting Lessons

### Only One DNS Stat Appeared

Prometheus returned both DNS series, but Grafana initially displayed one.

Resolution:

- Use distinct query reference IDs such as `A` and `B`.
- Put friendly labels in the legend fields.
- Validate raw Prometheus results before changing panels.

### Dashboard Threshold Parsing

Threshold values must be JSON numbers such as `70`, not quoted strings such as `"70"`.

### Imported Dashboard Variables

Imported dashboards may assume different job names. Refresh variables and select `node_exporter` before modifying working queries.

### Grafana Is Often the Symptom

Troubleshoot in this order:

1. Grafana data source.
2. Prometheus service.
3. Expected jobs and targets.
4. Exporter endpoints.
5. Panel queries and reference IDs.

## Backup Strategy

Grafana recovery uses multiple layers:

1. **Daily Proxmox VM backup**
   - Snapshot mode with Zstandard compression.
   - Retention of 7 daily, 4 weekly, and 3 monthly backups.
   - Dedicated external storage with mount-point enforcement.

2. **Grafana database state**
   - `/var/lib/grafana/grafana.db` contains dashboards, data sources, and local state.
   - Any separate copy must preserve SQLite consistency.

3. **Dashboard JSON exports**
   - Existing Node Exporter and Service Health exports are protected outside Git.
   - The Infrastructure Overview export remains pending.

4. **Private data-source mapping**
   - Records name, type, URL, and UID.

5. **Sanitized documentation**
   - Records architecture and recovery steps without secrets.

`mon01` has successful VM backup coverage but has not been independently restored. The Project 003 `dns01` restore proved the Proxmox restore workflow, not Grafana application recovery.

## Recovery Procedure

Preferred path:

1. Restore the latest appropriate `mon01` VM backup.
2. Keep the VM isolated during initial boot checks if duplicate identity is possible.
3. Confirm Grafana, Prometheus, Node Exporter, and Blackbox Exporter are active.
4. Confirm the Prometheus data source is healthy.
5. Confirm all host and DNS panels display current data.

Manual rebuild path:

1. Install Grafana on supported Debian.
2. Restore configuration and `grafana.db` consistently, or recreate the data source.
3. Import protected dashboards.
4. Rebind panels and variables to the intended data source.
5. Reinstall required non-bundled plugins.
6. Validate all three hosts and both DNS probe series.

## Security Considerations

- Change default administrative credentials.
- Store credentials in a password manager, never Git.
- Keep Grafana internal-only and do not expose TCP `3000` publicly.
- Treat dashboards and exports as operationally sensitive.
- Do not publish screenshots with exact addresses, usernames, tokens, or private topology.
- Keep original recovery exports and VM backups outside Git.

## Maintenance Notes

- Export dashboards after meaningful changes.
- Validate exported JSON privately before treating it as recoverable.
- Review data-source health after Prometheus changes.
- Record manually installed plugins.
- Update the private data-source record if its UID changes.
- Confirm a recent successful VM backup before major upgrades.
- Perform an independent `mon01` restore after major changes or before migration.

## Future Improvements

- Export and privately validate the Infrastructure Overview.
- Create reviewed provisioning files for data sources and dashboards.
- Create sanitized dashboard examples suitable for version control.
- Add Pi-hole-specific panels after application metrics exist.
- Add Proxmox platform and backup-health panels after those metrics exist.
- Validate Grafana-specific recovery through an independent `mon01` restore.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus](prometheus.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Node Exporter](node-exporter.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)