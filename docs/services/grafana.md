# Grafana

## Status

Active

## Purpose

Grafana provides visualization for the homelab monitoring stack. It queries Prometheus and turns host and service metrics into operational dashboards for troubleshooting, capacity review, and rapid health checks.

Grafana currently answers:

- Are `mon01`, `dns01`, and `pve01` reporting metrics?
- How are CPU, memory, filesystem utilization, and uptime trending?
- Are recursive and local DNS checks both succeeding?
- Is DNS probe duration changing or spiking?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Grafana |
| Package version | `13.1.0` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Data source | Prometheus at `http://localhost:9090` |
| Listen port | `3000/tcp` |
| Access scope | Internal homelab only |
| Public exposure | None |
| Backup maturity | Existing dashboards exported privately; new infrastructure overview export pending |

Exact private addresses, data-source identifiers, and raw dashboard JSON remain outside the public repository.

## Data Source

| Setting | Value |
| --- | --- |
| Name | `prometheus` |
| Type | Prometheus |
| URL | `http://localhost:9090` |
| Current UID | Retained privately as `<PROMETHEUS_DATASOURCE_UID>` |
| Storage | Local Grafana database state |

`localhost` is used because Grafana and Prometheus run on the same VM.

The active data source is not yet represented by reviewed provisioning files. Recovery therefore requires either:

- a consistency-preserving restore of `grafana.db`, or
- manual recreation of the Prometheus data source before dashboard import.

## Current Dashboards

### Imported Node Exporter Dashboard

Purpose:

- Detailed host-level CPU, memory, filesystem, disk, network, and uptime visibility.
- Multi-host selection through the shared `node_exporter` job.
- Deeper troubleshooting than the summary dashboard.

Current hosts:

- `mon01`
- `dns01`
- `pve01`

Protected export:

| Item | Value |
| --- | --- |
| Filename | `node-exporter-dashboard.json` |
| JSON validation | Successful |
| Storage | Private location outside Git |

### Homelab Service Health

Purpose:

- Visualize DNS availability and probe history separately from host health.

Current panels:

| Panel | Metric | Purpose |
| --- | --- | --- |
| DNS availability | `probe_success` | Shows current DNS probe state |
| DNS probe duration | `probe_duration_seconds` | Shows response duration over time |
| DNS probe status | `probe_success` | Shows state history |

Protected export:

| Item | Value |
| --- | --- |
| Filename | `homelab-service-health-dashboard.json` |
| JSON validation | Successful |
| Storage | Private location outside Git |

### Homelab Infrastructure Overview

Created on 2026-07-11 as a manually built summary dashboard. It demonstrates intentional PromQL and panel design rather than relying entirely on imported dashboards.

| Panel | Visualization | Purpose |
| --- | --- | --- |
| Host Availability | Stat | Shows `UP` or `DOWN` for `mon01`, `dns01`, and `pve01` |
| CPU Utilization by Host | Time series | Compares CPU utilization across all monitored hosts |
| Memory Utilization by Host | Time series | Compares memory utilization across all monitored hosts |
| Root Filesystem Utilization | Gauge | Shows root-filesystem consumption with warning and critical thresholds |
| Host Uptime | Stat | Displays uptime for each monitored host |
| DNS Availability | Stat | Shows independent Recursive DNS and Local DNS states |
| DNS Probe Duration | Full-width time series | Shows recursive DNS probe latency and makes spikes easier to inspect |

The dashboard uses:

- `node_exporter` metrics for `mon01`, `dns01`, and `pve01`
- `blackbox_dns` for recursive DNS
- `blackbox_dns_local` for the internal-record probe

The dashboard is operational, but its Classic JSON export and private validation remain pending. It must not be described as a protected recovery artifact until that export is created and tested.

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
probe_success{job="blackbox_dns_local", host="dns01"}
```

DNS probe duration:

```promql
probe_duration_seconds{job="blackbox_dns", host="dns01"}
```

## Dashboard Design Decisions

### Summary and Detail Separation

The Homelab Infrastructure Overview is the at-a-glance operational dashboard. The imported Node Exporter dashboard remains available for detailed host troubleshooting.

### Full-Width Trend Panels

Memory utilization and DNS probe duration use the full dashboard width. This removes unused grid space and improves visibility into small changes and latency spikes.

### Uptime Is Informational

Uptime values use a healthy neutral or green presentation rather than red thresholds. A recent reboot is not automatically a fault.

### Independent DNS States

The DNS Availability panel shows two separate stats:

- Recursive DNS
- Local DNS

This prevents a working local-record service from being hidden by an upstream outage and vice versa.

## Validation

Service checks on `mon01`:

```bash
systemctl is-active grafana-server
systemctl is-enabled grafana-server
curl -I localhost:3000
```

Dashboard validation:

1. Confirm the Prometheus data source passes **Save & test**.
2. Confirm `mon01`, `dns01`, and `pve01` all show `UP`.
3. Confirm host CPU, memory, filesystem, and uptime panels populate.
4. Confirm Recursive DNS and Local DNS both show `UP`.
5. Confirm DNS probe duration continues updating.
6. Confirm panel labels do not expose exact private addresses.

## Troubleshooting Lessons

### Only One DNS Stat Appeared

Prometheus returned both DNS series, but Grafana initially displayed only one. The panel queries did not have clean, distinct query reference IDs.

Resolution:

- Use query reference IDs `A` and `B`.
- Put `Recursive DNS` and `Local DNS` in the legend fields.
- Use Instant queries for current-state stats.
- Validate the raw Prometheus results before assuming Grafana is the data source of the failure.

Operational lesson: query reference IDs and user-facing legends are separate concepts.

### Dashboard v2 Threshold Parsing

A dashboard v2 operation failed when threshold values were stored as strings instead of numbers:

```text
cannot unmarshal string ... thresholds.steps.value of type float64
```

Threshold values must be numeric JSON values such as `70`, not quoted strings such as `"70"`. Value-mapping labels such as `UP` and `DOWN` remain strings.

### Imported Dashboard Variables

Imported dashboards may expect different job names. Refresh variables and select the `node_exporter` job before modifying working panel queries.

### Grafana Is Often the Symptom

When a dashboard is empty, validate in this order:

1. Prometheus data source
2. Prometheus service
3. Expected jobs and targets
4. Exporter endpoints
5. Panel query and query reference IDs

## Security Considerations

- Change default administrative credentials during deployment.
- Store credentials in a password manager, never Git.
- Keep Grafana internal-only.
- Do not expose TCP `3000` publicly.
- Treat dashboards and JSON exports as operationally sensitive.
- Do not publish screenshots containing exact addresses, usernames, tokens, or private topology.
- Use placeholders such as `<MON01_IP>`, `<DNS01_IP>`, and `<PROMETHEUS_DATASOURCE_UID>`.
- Keep original recovery exports outside Git even if sanitized portfolio copies are created later.

## Backup Strategy

Grafana recovery uses multiple layers:

1. Proxmox VM backup — pending implementation and restore validation.
2. Consistent `grafana.db` backup — procedure must preserve SQLite consistency.
3. Dashboard JSON exports — portable but require data-source verification.
4. Private data-source recovery mapping — records name, type, URL, and UID.
5. Sanitized repository documentation — records architecture and recovery steps without secrets.

The existing Node Exporter and Homelab Service Health exports were created and privately inspected. The Homelab Infrastructure Overview export is pending and should be completed after the next work session begins.

## Recovery Procedure

1. Restore a validated VM backup when available.
2. For a manual rebuild, install Grafana on `mon01`.
3. Restore configuration and `grafana.db` consistently, or recreate the Prometheus data source.
4. Import the Node Exporter dashboard.
5. Import the Homelab Service Health dashboard.
6. Import the Homelab Infrastructure Overview after its private export is created.
7. Verify each panel uses the intended Prometheus data source.
8. Confirm all three host series and both DNS probe series display current data.

This remains a draft recovery baseline until exercised during a controlled restore.

## Maintenance Notes

- Export dashboards after meaningful changes.
- Validate exported JSON privately before treating it as a recovery artifact.
- Review data-source health after Prometheus changes.
- Keep query legends aligned with job scope.
- Record manually installed plugins.
- Update the private data-source record if its UID changes.
- Update Project 003 after backup or restore validation.

## Future Improvements

- Export and privately validate the Homelab Infrastructure Overview as Classic JSON.
- Create reviewed provisioning files for data sources and dashboards.
- Create sanitized dashboard copies suitable for version control.
- Add Pi-hole-specific panels after application metrics exist.
- Add Proxmox platform and backup-health panels after those metrics are available.
- Validate Grafana database backup and restore.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Node Exporter Service](node-exporter.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
