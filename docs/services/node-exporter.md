# Node Exporter

## Status

Active

## Purpose

Node Exporter exposes Linux host metrics in a Prometheus-compatible format. It was the first monitoring component deployed for Project 002 because it provides the raw host metrics that Prometheus scrapes and stores.

Node Exporter helps answer operational questions such as:

- How much CPU time is the host using?
- How much memory is available?
- How much disk space remains?
- How much network traffic is passing through the host?
- Is the host reachable by the monitoring system?

Node Exporter reports host health. It does not prove that an application such as DNS is working correctly, so service-level probes are documented separately.

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Node Exporter |
| Package | `prometheus-node-exporter` |
| Hosts | `mon01`, `dns01` |
| Operating system | Debian 13.5 |
| Deployment method | Debian package repository |
| Default port | `9100/tcp` |
| Metrics path | `/metrics` |
| Current scraper | Prometheus on `mon01` |

## Hosts

| Hostname | Role | Prometheus Target | Status |
| --- | --- | --- | --- |
| `mon01` | Dedicated monitoring VM | `localhost:9100` | Active |
| `dns01` | Pi-hole DNS VM | `<DNS01_IP>:9100` | Active |

`dns01` was added as the first remote scrape target after the local `mon01` monitoring path was validated.

## Deployment Notes

Node Exporter was installed from the Debian package repository:

```bash
sudo apt install -y prometheus-node-exporter
```

The service was validated locally on each monitored host:

```bash
systemctl is-active prometheus-node-exporter
curl localhost:9100/metrics
```

The endpoint returned Prometheus-formatted metric output, confirming that the exporter was running. Remote reachability from `mon01` was tested before adding `dns01` to Prometheus.

Prometheus scrapes both endpoints under the `node_exporter` job and applies host and role labels so dashboards can distinguish the systems.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9100/tcp` |
| Access scope | Internal homelab only |
| Public exposure | None |
| Intended consumer | Prometheus on `mon01` |
| Current targets | `localhost:9100`, `<DNS01_IP>:9100` |

Node Exporter must not be exposed to the public internet. Metrics can reveal hostnames, filesystem paths, kernel information, network interfaces, and resource-usage patterns.

## Metrics

Node Exporter reads Linux kernel and operating-system data from sources such as `/proc` and `/sys`.

| Metric Family | Purpose |
| --- | --- |
| `node_cpu_seconds_total` | CPU time by core and mode |
| `node_memory_*` | Memory totals and availability |
| `node_filesystem_*` | Filesystem capacity and free space |
| `node_network_*` | Network receive and transmit counters |
| `node_boot_time_seconds` | Host boot time for uptime calculations |

## Validation Procedure

Run on each monitored host:

```bash
systemctl is-active prometheus-node-exporter
curl localhost:9100/metrics
```

Expected results:

- The service returns `active`.
- The endpoint returns metrics beginning with names such as `node_cpu`, `node_memory`, `node_filesystem`, and `node_network`.

Remote validation from `mon01`:

```bash
curl http://<DNS01_IP>:9100/metrics
```

Prometheus validation:

```promql
up{job="node_exporter"}
```

Expected result: both `mon01` and `dns01` return `1`.

Additional validation:

```promql
node_memory_MemAvailable_bytes
```

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Grafana validation:

- Open the imported Node Exporter dashboard.
- Select the `node_exporter` job.
- Confirm `mon01` and `dns01` are selectable.
- Confirm panels populate after the Prometheus scrape interval.

## Monitoring Role and Limitations

Node Exporter confirms that Linux host metrics are available. It does not confirm that hosted applications are usable.

For `dns01`:

- Node Exporter answers: **Is the host running and reporting metrics?**
- Blackbox Exporter answers: **Does the DNS endpoint answer the configured query?**
- Future Pi-hole metrics should answer: **How is the DNS application behaving internally?**

These layers should remain separate because they represent different failure modes.

## Security Considerations

- Keep Node Exporter internal-only.
- Do not publish raw metrics output.
- Do not expose port `9100` to untrusted networks.
- Restrict scrape access to trusted monitoring systems where practical.
- Treat metrics as operationally sensitive.
- Use sanitized placeholders such as `<DNS01_IP>` instead of exact internal addresses.

## Backup Strategy

Node Exporter is stateless and can be reinstalled from the Debian repository.

Important state belongs to:

- Host configuration.
- Prometheus scrape configuration.
- Firewall rules if access becomes restricted.
- Documentation in this repository.

No dedicated Node Exporter data backup is required.

## Recovery Procedure

If Node Exporter is not responding:

1. Check service status:

   ```bash
   systemctl status prometheus-node-exporter
   ```

2. Confirm the endpoint responds locally:

   ```bash
   curl localhost:9100/metrics
   ```

3. From `mon01`, confirm remote reachability for `dns01`:

   ```bash
   curl http://<DNS01_IP>:9100/metrics
   ```

4. Confirm Prometheus can scrape the target:

   ```promql
   up{job="node_exporter"}
   ```

5. Review service logs:

   ```bash
   journalctl -u prometheus-node-exporter --no-pager -n 50
   ```

6. Confirm firewall and network changes have not blocked port `9100`.
7. Reinstall the package if required:

   ```bash
   sudo apt install --reinstall prometheus-node-exporter
   ```

8. Revalidate Prometheus and Grafana after recovery.

## Maintenance Notes

- Keep the package updated through normal Debian patching.
- Revalidate `/metrics` after major operating-system updates.
- Watch for metric-name or collector changes after package upgrades.
- Confirm Prometheus target health after exporter or scrape-configuration changes.
- Add future Linux hosts intentionally and label them by host and role.
- Keep service availability checks separate from host metrics.

## Future Improvements

- Add Node Exporter or another documented monitoring method for the Proxmox host.
- Build a custom Linux host dashboard for the actual homelab priorities.
- Add actionable host-resource alerts only after thresholds and runbooks are defined.
- Restrict scrape access with network segmentation or host firewall rules when the network design matures.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
