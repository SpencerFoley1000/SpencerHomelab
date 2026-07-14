# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab. It scrapes Linux host metrics from Node Exporter, DNS probe metrics through Blackbox Exporter, and its own health metrics. Grafana uses Prometheus as its primary data source.

The current configuration answers:

- Are `mon01`, `dns01`, and `pve01` reporting host metrics?
- Is recursive DNS through `dns01` working?
- Is the expected internal DNS record available independently of upstream recursion?
- How are resource use and DNS probe duration changing over time?

## Technology Stack

| Component | Value |
| --- | --- |
| Package version | `2.53.3+ds1-2` |
| Host | `mon01` |
| Operating system | Debian 13.5 Trixie |
| Configuration | `/etc/prometheus/prometheus.yml` |
| Metrics storage | `/var/lib/prometheus/metrics2/` |
| Grafana connection | `http://localhost:9090` |
| Trusted UI access | Internal homelab only |
| Public exposure | None |
| Backup maturity | Daily `mon01` VM backup active; configuration inventoried; independent restore not yet tested |

TCP `9090` must not be publicly exposed.

## Current Jobs

| Job | Target role | Labels or purpose | Expected state |
| --- | --- | --- | --- |
| `prometheus` | Prometheus self-monitoring | Local service | Up |
| `node_exporter` | `mon01` | `host="mon01"`, `role="monitoring"` | Up |
| `node_exporter` | `dns01` | `host="dns01"`, `role="dns"` | Up |
| `node_exporter` | `pve01` | `host="pve01"`, `role="hypervisor"` | Up |
| `blackbox_dns` | Recursive DNS through `dns01` | Public-name query | Up |
| `blackbox_dns_local` | Local DNS through `dns01` | Expected answer with `scope="local"` | Up |

Exact addresses remain private. Use `<DNS01_IP>`, `<MON01_IP>`, and `<PVE01_IP>` publicly.

## Sanitized Scrape Design

### Shared Node Exporter Job

```yaml
- job_name: node_exporter
  static_configs:
    - targets: ['localhost:9100']
      labels:
        host: mon01
        role: monitoring
    - targets: ['<DNS01_IP>:9100']
      labels:
        host: dns01
        role: dns
    - targets: ['<PVE01_IP>:9100']
      labels:
        host: pve01
        role: hypervisor
```

### Recursive DNS Job

```yaml
- job_name: blackbox_dns
  metrics_path: /probe
  params:
    module: [dns_udp]
  static_configs:
    - targets: ['<DNS01_IP>:53']
      labels:
        host: dns01
        service: dns
        protocol: udp
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
- job_name: blackbox_dns_local
  metrics_path: /probe
  params:
    module: [dns_udp_local]
  static_configs:
    - targets: ['<DNS01_IP>:53']
      labels:
        host: dns01
        service: dns
        scope: local
        protocol: udp
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

Separate jobs keep recursive and local DNS failure domains explicit.

## Safe Configuration Changes

Create a rollback copy:

```bash
sudo cp /etc/prometheus/prometheus.yml \
  /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
```

Validate:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
```

Reload and confirm service state:

```bash
sudo systemctl reload prometheus
systemctl is-active prometheus
```

`promtool` validates syntax and structure. It does not prove every intended job remains present, so PromQL validation is mandatory.

## Validation

Service health:

```bash
systemctl is-active prometheus
systemctl is-enabled prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

Target inventory:

```promql
count by (job, instance) (up)
```

Linux hosts:

```promql
up{job="node_exporter"}
```

Expected hosts: `mon01`, `dns01`, and `pve01`.

Proxmox host:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Recursive DNS:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

Local DNS:

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Both DNS probes should return `1`.

A new job may briefly return no data until its first scrape completes.

## Monitoring Boundaries

Node Exporter on `pve01` does not provide authoritative:

- VM or container state.
- Cluster quorum.
- Task results.
- Storage-pool health.
- Backup-job status or age.
- Replication state.

Those require a future Proxmox-specific integration using least-privilege credentials.

DNS boundaries:

- `blackbox_dns` includes Pi-hole, the upstream resolver, and internet dependencies.
- `blackbox_dns_local` isolates Pi-hole local-record behavior from upstream recursion.

## Troubleshooting Notes

### Valid Configuration but Missing Job

A configuration can pass `promtool` while an intended job is absent. Pair syntax validation with:

```promql
count by (job, instance) (up)
```

### Initial Empty Query

Allow one scrape interval after adding a new target before diagnosing an empty result.

### Grafana Displays One DNS Series

Confirm the Grafana panel uses distinct query reference IDs such as `A` and `B`. Friendly labels belong in legends.

## Backup and Recovery

Important state:

- `/etc/prometheus/prometheus.yml`.
- `/etc/prometheus/blackbox.yml` through the related Blackbox service.
- Future alerting and recording rules.
- Local time-series history when operationally important.
- Documentation and validation queries.

Project 003 provides:

- Daily full-VM backup coverage for `mon01`.
- Snapshot mode and Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external storage with mount-point enforcement.
- A verified configuration inventory.
- Recovery runbooks grounded in the tested Proxmox restore workflow.

At current scale, configuration is more important than short-term metric history for manual reconstruction.

Recovery order:

1. Restore the `mon01` VM backup or rebuild Debian.
2. Restore or recreate Prometheus and Blackbox configuration.
3. Validate with `promtool`.
4. Start or reload Prometheus.
5. Confirm `prometheus`, `node_exporter`, `blackbox_dns`, and `blackbox_dns_local`.
6. Confirm all three host targets and both DNS probes.
7. Confirm Grafana dashboards display current data.

Current limitation: `mon01` has not been independently restore-tested.

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose TCP `9090` publicly.
- Restrict UI access to trusted administrators.
- Do not publish raw metrics, exact targets, private labels, credentials, or screenshots containing topology.
- Introduce Proxmox API credentials only through least privilege.

## Maintenance Notes

- Validate configuration before every reload.
- Verify target inventory after every change.
- Confirm backup coverage before significant upgrades.
- Monitor local storage growth.
- Record package-version changes.
- Update recovery inventories when jobs or labels change.
- Perform an independent `mon01` restore after major monitoring changes or before migration.

## Future Improvements

- Add Proxmox VM, storage, task, and backup metrics.
- Add backup-age and failure monitoring.
- Add recording rules where repeated expensive queries justify them.
- Add Alertmanager only after thresholds, runbooks, and notification routing exist.
- Define metrics retention based on measured storage growth.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Grafana](grafana.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Node Exporter](node-exporter.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)