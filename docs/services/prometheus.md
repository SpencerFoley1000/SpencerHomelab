# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab monitoring stack. It scrapes Linux host metrics from Node Exporter, DNS probe metrics through Blackbox Exporter, and its own health metrics. Grafana uses Prometheus as its primary data source.

The current configuration answers:

- Are `mon01`, `dns01`, and `pve01` reporting Linux host metrics?
- Is recursive DNS resolution through `dns01` working?
- Is the expected internal DNS record available independently of upstream recursion?
- How are CPU, memory, filesystem, network, uptime, and DNS probe duration changing over time?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Prometheus |
| Package version | `2.53.3+ds1-2` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Configuration | `/etc/prometheus/prometheus.yml` |
| Metrics storage | `/var/lib/prometheus/metrics2/` |
| Grafana access | `http://localhost:9090` from `mon01` |
| Trusted browser access | `<MON01_IP>:9090` on the internal homelab network |
| Public exposure | None |
| Backup maturity | Configuration inventoried; protected VM backup and restore validation pending |

Prometheus is not bound exclusively for local-only use: Grafana consumes it through `localhost`, while trusted internal administrators may use the UI through the sanitized `mon01` address. TCP `9090` must not be publicly exposed.

## Current Jobs

| Job | Target | Labels or purpose | Expected state |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Prometheus self-monitoring | `UP` |
| `node_exporter` | `localhost:9100` | `host="mon01"`, `role="monitoring"` | `UP` |
| `node_exporter` | `<DNS01_IP>:9100` | `host="dns01"`, `role="dns"` | `UP` |
| `node_exporter` | `<PVE01_IP>:9100` | `host="pve01"`, `role="hypervisor"` | `UP` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Recursive public-name DNS probe | `UP` |
| `blackbox_dns_local` | `<DNS01_IP>:53` through `localhost:9115` | Internal-record DNS probe with `scope="local"` | `UP` |

Exact addresses remain private. Public documentation uses `<DNS01_IP>`, `<MON01_IP>`, and `<PVE01_IP>`.

## Sanitized Scrape Configuration

### Shared Node Exporter Job

```yaml
- job_name: 'node_exporter'
  static_configs:
    - targets: ['localhost:9100']
      labels:
        host: 'mon01'
        role: 'monitoring'

    - targets: ['<DNS01_IP>:9100']
      labels:
        host: 'dns01'
        role: 'dns'

    - targets: ['<PVE01_IP>:9100']
      labels:
        host: 'pve01'
        role: 'hypervisor'
```

### Recursive DNS Job

```yaml
- job_name: 'blackbox_dns'
  metrics_path: /probe
  params:
    module: [dns_udp]
  static_configs:
    - targets:
        - '<DNS01_IP>:53'
      labels:
        host: 'dns01'
        service: 'dns'
        protocol: 'udp'
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

### Local DNS Job

```yaml
- job_name: 'blackbox_dns_local'
  metrics_path: /probe
  params:
    module: [dns_udp_local]
  static_configs:
    - targets:
        - '<DNS01_IP>:53'
      labels:
        host: 'dns01'
        service: 'dns'
        scope: 'local'
        protocol: 'udp'
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

Separate jobs keep recursive and local DNS failure domains explicit in PromQL, Grafana, recovery validation, and future alert rules.

## Safe Configuration Changes

Create a rollback copy:

```bash
sudo cp /etc/prometheus/prometheus.yml \
  /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
```

Validate before applying:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
```

Prefer a reload for valid scrape changes:

```bash
sudo systemctl reload prometheus
systemctl is-active prometheus
```

`promtool` verifies syntax and structure. It does not prove every intended job or target exists, so PromQL validation is mandatory after reload.

## Validation

### Service Health

```bash
systemctl is-active prometheus
systemctl is-enabled prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

### Target Inventory

```promql
count by (job, instance) (up)
```

Expected jobs:

- `prometheus`
- `node_exporter`
- `blackbox_dns`
- `blackbox_dns_local`

### Linux Host Targets

```promql
up{job="node_exporter"}
```

Expected hosts:

- `mon01`
- `dns01`
- `pve01`

Proxmox host specifically:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

### DNS Probes

Recursive DNS:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

Local DNS:

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Both probes:

```promql
probe_success{job=~"blackbox_dns.*", host="dns01"}
```

Both series should return `1`.

A newly added job may briefly return an empty result until its first scrape completes. Re-query after the configured interval before treating an initial empty result as a failure.

## Resource Queries Used by Grafana

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

## Monitoring Boundaries

Node Exporter on `pve01` provides Linux operating-system metrics. It does not provide authoritative Proxmox platform state such as:

- VM or container state.
- Cluster quorum.
- Task results.
- Storage-pool health.
- Backup-job status.
- Replication state.

Those capabilities require a future Proxmox-specific exporter or API integration using documented least-privilege credentials.

The DNS jobs also have distinct boundaries:

- `blackbox_dns` includes Pi-hole, the upstream resolver, and internet dependency.
- `blackbox_dns_local` isolates Pi-hole local-record behavior from upstream recursion.

## Troubleshooting Notes

### Valid Configuration but Missing Job

A configuration can pass `promtool` while an intended job is absent or malformed. Always pair configuration validation with:

```promql
count by (job, instance) (up)
```

### Initial Empty Query

The first local-DNS query returned an empty vector immediately after reload, while a later query showed both jobs at `1`. New jobs may need one scrape interval before data appears.

### Grafana Shows One DNS Series

When Prometheus returns both series but Grafana shows only one, verify the panel has distinct query reference IDs such as `A` and `B`. Friendly labels belong in legends, not the reference-ID field.

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose TCP `9090` publicly.
- Restrict UI access to trusted internal administrators.
- Do not publish raw metrics, exact targets, or screenshots containing private topology.
- Do not commit credentials, API tokens, or secret-bearing discovery configuration.
- Treat metrics and labels as operationally sensitive.
- Introduce Proxmox API credentials only through a documented least-privilege design.

## Backup and Recovery

Important state:

- `/etc/prometheus/prometheus.yml`
- Future alerting and recording rules.
- Future service-discovery configuration.
- Local time-series data if retention becomes operationally important.
- Documentation in this repository.

At current scale, validated configuration is more important than short-term metrics history. Project 003 inventories the configuration but protected VM backups and restore testing remain pending.

Recovery order:

1. Restore or recreate Prometheus configuration.
2. Validate with `promtool`.
3. Start or reload Prometheus.
4. Verify `prometheus`, `node_exporter`, `blackbox_dns`, and `blackbox_dns_local`.
5. Verify all three Node Exporter hosts.
6. Verify both DNS `probe_success` series.
7. Confirm Grafana dashboards display current data.

## Maintenance Notes

- Back up configuration before editing.
- Validate with `promtool` before reload or restart.
- Validate intended jobs and labels with PromQL afterward.
- Review target health after every scrape change.
- Re-test Grafana after Prometheus changes.
- Remove temporary rollback files after a protected known-good copy exists.
- Add alerts only after thresholds and response runbooks exist.
- Add the future server only after its hardware and production role are validated.

## Future Improvements

- Add Proxmox-specific VM, storage, task, and backup metrics through a least-privilege integration.
- Add Pi-hole-specific application metrics.
- Add Alertmanager only after actionable thresholds and response procedures are defined.
- Protect Prometheus configuration and validate restoration under Project 003.
- Add backup-job and backup-age metrics after Project 003 implementation.
- Consider version-controlled configuration deployment after the environment stabilizes.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Node Exporter Service](node-exporter.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [Proxmox VE Platform](proxmox.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
