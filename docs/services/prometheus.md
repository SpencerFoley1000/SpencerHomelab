# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab monitoring stack. It scrapes Linux host metrics from Node Exporter, DNS probe metrics through Blackbox Exporter, and its own health metrics. Grafana uses Prometheus as its primary data source.

Prometheus helps answer:

- Are configured scrape targets reachable?
- Are monitored Linux hosts reporting metrics?
- Is recursive DNS resolution through `dns01` succeeding?
- How have CPU, memory, filesystem, network, and service metrics changed over time?
- Which monitoring layer failed when a dashboard stops updating?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Prometheus |
| Package | `prometheus` |
| Package version | `2.53.3+ds1-2` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Deployment method | Debian package repository |
| Default port | `9090/tcp` |
| Configuration file | `/etc/prometheus/prometheus.yml` |
| Local data | `/var/lib/prometheus/metrics2/` |
| Visualization consumer | Grafana on `mon01` |
| Backup maturity | Configuration inventoried; validated VM backup pending |

## Deployment Notes

Prometheus was installed from the Debian package repository:

```bash
sudo apt install -y prometheus
```

Local health checks:

```bash
systemctl is-active prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

Grafana queries Prometheus at:

```text
http://localhost:9090
```

`localhost` is used because Grafana and Prometheus run on the same VM.

## Current Scrape Configuration

Prometheus is configured through:

```text
/etc/prometheus/prometheus.yml
```

Current jobs and targets:

| Job | Target | Labels or purpose | Expected state |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Prometheus self-monitoring | `UP` |
| `node_exporter` | `localhost:9100` | `host="mon01"`, `role="monitoring"` | `UP` |
| `node_exporter` | `<DNS01_IP>:9100` | `host="dns01"`, `role="dns"` | `UP` |
| `node_exporter` | `<PVE01_IP>:9100` | `host="pve01"`, `role="hypervisor"` | `UP` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Recursive DNS probe | `UP` |

Sanitized Node Exporter configuration:

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

Sanitized Blackbox DNS configuration:

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

Exact addresses are private. Public documentation uses `<DNS01_IP>`, `<MON01_IP>`, and `<PVE01_IP>`.

## Proxmox Host Target Addition

The `pve01` Node Exporter target was added on 2026-07-10.

Procedure and validation:

1. Verified the exporter locally on `pve01`.
2. Confirmed `mon01` could reach `http://<PVE01_IP>:9100/metrics` while the Proxmox firewall was active.
3. Created a local rollback copy of `prometheus.yml` before editing.
4. Added the target to the existing `node_exporter` job instead of creating a duplicate job.
5. Applied `host="pve01"` and `role="hypervisor"` labels.
6. Ran `promtool check config /etc/prometheus/prometheus.yml` successfully.
7. Reloaded Prometheus without interrupting the service.
8. Confirmed both target-specific queries returned `1`.
9. Confirmed Grafana panels displayed `pve01` metrics.

The local `.bak-pve01` file is a short-term rollback copy, not a protected backup.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9090/tcp` |
| Access scope | Trusted internal network only |
| Public exposure | None |
| Node Exporter endpoints | Three |
| Blackbox probe targets | One DNS target |
| Grafana consumer | Local Grafana service on `mon01` |

Prometheus must not be exposed publicly. Metrics, labels, and target metadata can reveal hostnames, service names, versions, paths, and infrastructure relationships.

## Safe Configuration Change Procedure

Back up the current configuration before editing:

```bash
sudo cp /etc/prometheus/prometheus.yml \
  /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
```

Validate before applying:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
```

Prefer a reload for valid scrape-target changes:

```bash
sudo systemctl reload prometheus
systemctl is-active prometheus
```

A restart may be used when required:

```bash
sudo systemctl restart prometheus
```

`promtool` confirms syntax and structure. It does not prove that every intended job or target still exists, so post-change PromQL validation is mandatory.

## Validation Procedure

### Service Health

```bash
systemctl is-active prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

### Endpoint Reachability

From `mon01`:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  http://<TARGET_IP>:9100/metrics | head
```

Manual DNS probe:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

Expected DNS probe output includes:

```text
probe_success 1
```

### PromQL Smoke Tests

Inventory all jobs and instances:

```promql
count by (job, instance) (up)
```

All Linux hosts:

```promql
up{job="node_exporter"}
```

Proxmox host specifically:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

DNS service probe:

```promql
probe_success{job="blackbox_dns"}
```

Resource checks:

```promql
node_memory_MemAvailable_bytes
```

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

A new target may briefly show `UNKNOWN` before the first scrape completes.

### Grafana

- Confirm the Prometheus data source URL remains `http://localhost:9090`.
- Run **Save & test** if the data source is changed.
- Open the Node Exporter dashboard.
- Select the `node_exporter` job and the intended host.
- Confirm panels populate for `mon01`, `dns01`, and `pve01`.

## Monitoring Boundaries

The current `pve01` target provides Linux operating-system metrics only. It does not provide authoritative Proxmox information such as:

- VM or container state.
- Cluster quorum or node status.
- Proxmox task results.
- Storage-pool health.
- Backup-job status.
- Replication state.

Those capabilities require a future Proxmox-specific exporter or API integration with documented least-privilege credentials.

## DNS Probe Interpretation

The current Blackbox module queries a public DNS name through `dns01`.

A successful probe validates:

```text
mon01 -> dns01/Pi-hole -> configured upstream resolver -> public DNS result
```

A failure could indicate Pi-hole, host, routing, firewall, internet, upstream-resolver, or query failure. A future local-record probe should isolate internal DNS functionality from upstream recursion.

## Backup Strategy

Important state includes:

- `/etc/prometheus/prometheus.yml`
- Future alerting and recording rules
- Any future service-discovery configuration
- Local time-series data if retention becomes operationally important
- Documentation in this repository

Project 003 established that configuration is more important than short-term metrics history at the current lab scale. Protected VM backups and restore testing remain pending.

## Recovery Procedure

If Prometheus or dashboards stop updating:

1. Check Prometheus service state.
2. Validate the configuration with `promtool`.
3. Check readiness and health endpoints.
4. Review logs.
5. Test Node Exporter endpoints directly.
6. Test the Blackbox DNS probe manually.
7. Run `count by (job, instance) (up)`.
8. Confirm `mon01`, `dns01`, and `pve01` targets remain present.
9. Restore the most recent known-good configuration if required.
10. Reload or restart Prometheus.
11. Confirm Grafana dashboards resume updating.

Use the [Prometheus Scrape Target Troubleshooting Runbook](../runbooks/prometheus-scrape-target-troubleshooting.md) for the detailed incident workflow.

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose port `9090` publicly.
- Do not publish raw metrics or screenshots containing private values.
- Do not commit API tokens, credentials, exact addresses, or secret-bearing service-discovery files.
- Treat metrics and labels as operationally sensitive.
- Use sanitized placeholders in public documentation.
- Introduce Proxmox API credentials only through a documented least-privilege design.

## Maintenance Notes

- Back up configuration before editing.
- Validate with `promtool` before reload or restart.
- Validate expected jobs and targets with PromQL afterward.
- Review target health after every scrape change.
- Re-test Grafana after Prometheus changes.
- Remove stale rollback files after a protected known-good copy exists.
- Avoid alerts until they are actionable and tied to runbooks.

## Future Improvements

- Add Proxmox-specific VM, storage, task, and backup metrics through a least-privilege integration.
- Add a local-record DNS probe.
- Add Pi-hole-specific metrics.
- Add Alertmanager only after thresholds and response runbooks are defined.
- Add protected backup coverage and restore validation.
- Consider version-controlled configuration deployment after the environment stabilizes.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Node Exporter Service](node-exporter.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [Proxmox VE Platform](proxmox.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
