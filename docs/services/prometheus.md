# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab monitoring stack. It is the second deployed component in Project 002 after Node Exporter and now serves as the data source for Grafana.

Prometheus helps answer operational questions such as:

- Are monitored targets reachable?
- Is Node Exporter being scraped successfully?
- Is the DNS service answering queries?
- How have CPU, memory, disk, and network metrics changed over time?
- Which services or hosts should be investigated first during an outage?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Prometheus |
| Package | `prometheus` |
| Host | `mon01` |
| Operating System | Debian 13.5 |
| Deployment Method | Debian package repository |
| Default Port | `9090/tcp` |
| Configuration File | `/etc/prometheus/prometheus.yml` |
| Data Model | Time-series metrics |
| Current Visualization Consumer | Grafana on `mon01` |

## Host

Prometheus is currently installed on:

| Hostname | Role |
| --- | --- |
| `mon01` | Dedicated monitoring VM |

## Deployment Notes

Prometheus was installed from the Debian package repository:

```bash
sudo apt install -y prometheus
```

The service was validated locally from `mon01`:

```bash
systemctl status prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

The Prometheus web UI was also validated from the internal homelab network.

Grafana is configured to query Prometheus using:

```text
http://localhost:9090
```

`localhost` is used because Grafana and Prometheus both run on `mon01`.

## Configuration

Prometheus is configured through:

```text
/etc/prometheus/prometheus.yml
```

The current scrape configuration includes:

| Job | Target | Purpose |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | Linux host metrics from `mon01` |
| `node_exporter` | `<DNS01_IP>:9100` | Linux host metrics from `dns01` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | DNS availability probe for `dns01` |

The Node Exporter scrape target includes labels for host and role identification:

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

The Blackbox DNS scrape job sends probe requests to Blackbox Exporter on `mon01`, then Blackbox Exporter probes the DNS service on `dns01`:

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

Exact IP addresses are intentionally omitted from public documentation. Use sanitized placeholders such as `<MON01_IP>` and `<DNS01_IP>` when documenting browser access or remote scrape targets.

## Networking

| Item | Value |
| --- | --- |
| Listen Port | `9090/tcp` |
| Access Scope | Internal homelab only |
| Public Exposure | None |
| Current Scrape Targets | `localhost:9090`, `localhost:9100`, `<DNS01_IP>:9100`, `blackbox_dns` probe for `<DNS01_IP>:53` |
| Current Visualization Consumer | Grafana on `localhost:3000` |

Prometheus should not be exposed to the public internet. Metrics can reveal hostnames, paths, service names, kernel information, resource usage patterns, and other infrastructure details.

## Validation Procedure

### Service Health

Run on `mon01`:

```bash
systemctl is-active prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

Expected results:

- `systemctl` returns `active`.
- The readiness endpoint returns that the Prometheus server is ready.
- The health endpoint returns that the Prometheus server is healthy.

### Configuration Validation

Before restarting Prometheus after edits:

```bash
promtool check config /etc/prometheus/prometheus.yml
```

Only restart Prometheus after the configuration passes validation.

### Target Health

In the Prometheus web UI:

```text
Status -> Target health
```

Expected current targets:

| Job | Target | Expected Health |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | `UP` |
| `node_exporter` | `localhost:9100` | `UP` |
| `node_exporter` | `<DNS01_IP>:9100` | `UP` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | `UP` |

A newly added target may briefly show `UNKNOWN` until Prometheus completes a scrape cycle.

### Remote Target Validation

Before adding a remote Node Exporter target to Prometheus, validate the exporter from `mon01`:

```bash
curl http://<DNS01_IP>:9100/metrics
```

Before adding a Blackbox DNS probe to Prometheus, validate the probe manually from `mon01`:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

Expected probe result:

```text
probe_success 1
```

### Grafana Data Source Validation

In Grafana:

1. Open the Prometheus data source.
2. Confirm the URL is `http://localhost:9090`.
3. Use **Save & test**.
4. Confirm Grafana successfully queries the Prometheus API.

### PromQL Smoke Tests

Useful validation queries:

```promql
up
```

Expected: configured healthy targets return `1`.

```promql
up{job="node_exporter"}
```

Expected: both `mon01` and `dns01` return `1`.

```promql
probe_success{job="blackbox_dns"}
```

Expected: the DNS probe returns `1`.

```promql
node_memory_MemAvailable_bytes
```

Expected: available memory metrics from Node Exporter for monitored hosts.

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Expected: available space for the root filesystem.

## Backup Strategy

Prometheus stores time-series data locally on `mon01`. The service can be reinstalled from the Debian package repository, but configuration and historical metrics may be useful depending on the recovery goal.

Important state:

- `/etc/prometheus/prometheus.yml`
- Local Prometheus time-series database
- Future alerting rules and scrape target configuration
- Documentation in this repository

Until backup infrastructure is deployed, Prometheus should be treated as rebuildable but not fully protected.

## Recovery Procedure

If Prometheus is not responding:

1. Check service status:

   ```bash
   systemctl status prometheus
   ```

2. Validate the configuration:

   ```bash
   promtool check config /etc/prometheus/prometheus.yml
   ```

3. Check local health endpoints:

   ```bash
   curl localhost:9090/-/ready
   curl localhost:9090/-/healthy
   ```

4. Review logs:

   ```bash
   journalctl -u prometheus --no-pager -n 100
   ```

5. Confirm local Node Exporter is still responding:

   ```bash
   curl localhost:9100/metrics
   ```

6. Confirm remote Node Exporter targets are reachable:

   ```bash
   curl http://<DNS01_IP>:9100/metrics
   ```

7. Confirm the DNS probe works manually:

   ```bash
   curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
   ```

8. Confirm Grafana can query Prometheus:

   ```bash
   curl -I localhost:3000
   ```

9. Restart Prometheus after fixing configuration or service issues:

   ```bash
   sudo systemctl restart prometheus
   ```

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose port `9090` to untrusted networks.
- Do not publish raw metrics output or screenshots containing sensitive infrastructure details.
- Avoid committing secrets, API tokens, credentials, or private URLs in scrape configurations.
- Treat metrics as operationally sensitive because they can reveal infrastructure structure and behavior.
- Add authentication or reverse proxy controls before any broader access is considered.
- Use sanitized placeholders instead of exact internal IP addresses in public documentation.

## Maintenance Notes

- Validate configuration with `promtool` before restarting Prometheus.
- Keep the package updated through normal Debian patching.
- Review target health after any scrape configuration change.
- Add new scrape targets intentionally and document why each target matters.
- Re-test the Grafana data source after Prometheus configuration changes.
- Avoid adding alerts until they are actionable and tied to runbooks.

## Future Improvements

- Add Grafana panels for DNS availability and latency.
- Add Pi-hole metrics or DNS-specific exporters.
- Add Proxmox monitoring through an appropriate exporter or API-based method.
- Add Alertmanager after dashboards and runbooks exist.
- Add backup coverage for Prometheus configuration and any long-term metric retention goals.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Node Exporter Service](node-exporter.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [VM Inventory](../architecture/vm-inventory.md)
