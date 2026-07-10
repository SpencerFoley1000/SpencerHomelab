# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab monitoring stack. It scrapes host metrics from Node Exporter, DNS probe metrics through Blackbox Exporter, and its own health metrics. Grafana uses Prometheus as its primary data source.

Prometheus helps answer operational questions such as:

- Are configured scrape targets reachable?
- Are monitored Linux hosts reporting metrics?
- Is the DNS service answering the configured probe?
- How have CPU, memory, disk, network, and service metrics changed over time?
- Which monitoring layer failed when a dashboard stops updating?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Prometheus |
| Package | `prometheus` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Deployment method | Debian package repository |
| Default port | `9090/tcp` |
| Configuration file | `/etc/prometheus/prometheus.yml` |
| Data model | Time-series metrics |
| Visualization consumer | Grafana on `mon01` |
| Backup maturity | Rebuildable; configuration and historical data are not yet protected by validated backups |

## Deployment Notes

Prometheus was installed from the Debian package repository:

```bash
sudo apt install -y prometheus
```

The service was validated locally from `mon01`:

```bash
systemctl is-active prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

The internal web UI was also validated. Grafana queries Prometheus at:

```text
http://localhost:9090
```

`localhost` is used because Grafana and Prometheus run on the same VM.

## Current Scrape Configuration

Prometheus is configured through:

```text
/etc/prometheus/prometheus.yml
```

Current jobs:

| Job | Target | Purpose |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | Linux host metrics from `mon01` |
| `node_exporter` | `<DNS01_IP>:9100` | Linux host metrics from `dns01` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | DNS recursive-resolution probe for `dns01` |

The Node Exporter job applies host and role labels:

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
```

The Blackbox DNS job sends a target parameter to Blackbox Exporter, then rewrites the actual scrape address to the exporter on `mon01`:

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

Exact addresses are omitted. Public documentation uses placeholders such as `<MON01_IP>` and `<DNS01_IP>`.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9090/tcp` |
| Access scope | Trusted internal network only |
| Public exposure | None |
| Scrape targets | Prometheus, two Node Exporter endpoints, and one Blackbox DNS probe |
| Grafana consumer | `localhost:3000` on `mon01` |

Prometheus should not be exposed publicly. Metrics and target labels can reveal hostnames, service names, paths, versions, resource usage, and infrastructure structure.

## Validation Procedure

### Service Health

Run on `mon01`:

```bash
systemctl is-active prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

Expected results:

- The service returns `active`.
- The readiness endpoint confirms Prometheus is ready.
- The health endpoint confirms Prometheus is healthy.

### Configuration Validation

Before restarting Prometheus after an edit:

```bash
sudo cp /etc/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
promtool check config /etc/prometheus/prometheus.yml
```

Only restart after validation passes:

```bash
sudo systemctl restart prometheus
systemctl is-active prometheus
```

`promtool` verifies syntax and structural validity, but it does not prove that every intended job is still present. Post-change PromQL validation is required.

### Target Health

In the Prometheus web UI, open:

```text
Status -> Target health
```

Expected targets:

| Job | Target | Expected Health |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | `UP` |
| `node_exporter` | `localhost:9100` | `UP` |
| `node_exporter` | `<DNS01_IP>:9100` | `UP` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | `UP` |

A newly added target may briefly show `UNKNOWN` before its first scrape completes.

### Endpoint Validation

Remote Node Exporter:

```bash
curl http://<DNS01_IP>:9100/metrics
```

Manual DNS probe:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

Expected probe output includes:

```text
probe_success 1
```

### PromQL Smoke Tests

```promql
count by (job, instance) (up)
```

Confirms expected jobs and targets exist.

```promql
up{job="node_exporter"}
```

Expected: `mon01` and `dns01` return `1`.

```promql
probe_success{job="blackbox_dns"}
```

Expected: the DNS probe returns `1`.

```promql
probe_duration_seconds{job="blackbox_dns"}
```

Shows probe duration.

```promql
node_memory_MemAvailable_bytes
```

Shows available memory for monitored Linux hosts.

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Shows available root-filesystem space.

### Grafana Data Source Validation

In Grafana:

1. Open the Prometheus data source.
2. Confirm the URL is `http://localhost:9090`.
3. Select **Save & test**.
4. Confirm Grafana can query the Prometheus API.
5. Open both the Node Exporter and Homelab Service Health dashboards.

## DNS Probe Interpretation

The current Blackbox module queries a public DNS name through `dns01`.

A successful probe validates:

```text
mon01 -> dns01/Pi-hole -> configured upstream resolver -> public DNS result
```

A failed probe does not automatically mean the Pi-hole process alone failed. Possible causes include:

- `dns01` or Pi-hole being unavailable.
- Internal routing or firewall failure.
- Upstream internet failure.
- Upstream resolver failure.
- The configured public query failing.

A separate local-record probe should be added to isolate internal DNS functionality from upstream recursive resolution.

## Backup Strategy

Prometheus stores time-series data locally on `mon01`.

Important state:

- `/etc/prometheus/prometheus.yml`
- Local Prometheus time-series database
- Future alerting and recording rules
- Any future service-discovery configuration
- Documentation in this repository

Until Project 003 is implemented, Prometheus is rebuildable but not fully protected. Configuration is more important than short-term historical metrics at the current scale, but retention and recovery goals should be documented before the monitoring history becomes operationally important.

## Recovery Procedure

If Prometheus is not responding or dashboards stop updating:

1. Check Prometheus service status.
2. Validate the configuration with `promtool`.
3. Check readiness and health endpoints.
4. Review logs:

   ```bash
   journalctl -u prometheus --no-pager -n 100
   ```

5. Confirm Node Exporter endpoints respond directly.
6. Confirm the Blackbox DNS probe works manually.
7. Run `count by (job, instance) (up)` and verify all expected jobs are present.
8. Restore the most recent known-good configuration if a job was removed or malformed.
9. Restart Prometheus after fixing the issue.
10. Confirm Grafana dashboards resume updating.

Use the [Prometheus Scrape Target Troubleshooting Runbook](../runbooks/prometheus-scrape-target-troubleshooting.md) for the detailed incident procedure.

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose port `9090` to untrusted networks.
- Do not publish raw metric output or screenshots containing sensitive infrastructure details.
- Do not commit credentials, API tokens, private URLs, or secret-bearing service-discovery configuration.
- Treat metrics and labels as operationally sensitive.
- Add authentication or reverse-proxy controls before any broader access is considered.
- Use sanitized placeholders instead of exact internal addresses.

## Maintenance Notes

- Back up the configuration before editing.
- Validate syntax with `promtool` before restarting.
- Validate intended job presence with PromQL after restarting.
- Review target health after every scrape-configuration change.
- Add new targets intentionally and document what each target proves.
- Re-test the Grafana data source after Prometheus changes.
- Avoid alerts until they are actionable and tied to runbooks.

## Future Improvements

- Add a local-record DNS probe to separate internal DNS health from upstream recursive resolution.
- Add Pi-hole-specific metrics.
- Add Proxmox monitoring through a documented exporter or API-based approach.
- Add Alertmanager only after alert thresholds and response runbooks are defined.
- Add backup coverage for Prometheus configuration and any required historical retention.
- Consider version-controlled configuration deployment after the environment stabilizes.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Node Exporter Service](node-exporter.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
