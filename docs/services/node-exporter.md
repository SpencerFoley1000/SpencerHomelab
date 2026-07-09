# Node Exporter

## Status

Active

## Purpose

Node Exporter exposes Linux host metrics in a Prometheus-compatible format. It is the first monitoring component deployed for Project 002 because it provides the raw host metrics that Prometheus scrapes and stores.

Node Exporter helps answer operational questions such as:

- How much CPU time is the host using?
- How much memory is available?
- How much disk space is used?
- How much network traffic is passing through the host?
- Is the host up and responding to metric collection?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Node Exporter |
| Package | `prometheus-node-exporter` |
| Hosts | `mon01`, `dns01` |
| Operating System | Debian 13.5 |
| Deployment Method | Debian package repository |
| Default Port | `9100/tcp` |
| Metrics Path | `/metrics` |
| Current Scraper | Prometheus on `mon01` |

## Hosts

Node Exporter is currently installed on:

| Hostname | Role | Prometheus Target |
| --- | --- | --- |
| `mon01` | Dedicated monitoring VM | `localhost:9100` |
| `dns01` | Pi-hole DNS VM | `<DNS01_IP>:9100` |

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

The `curl` test returned Prometheus-formatted metric output, confirming that the exporter is exposing host metrics successfully.

Prometheus has been configured to scrape both endpoints as part of the `node_exporter` job.

## Networking

| Item | Value |
| --- | --- |
| Listen Port | `9100/tcp` |
| Access Scope | Internal homelab only |
| Public Exposure | None |
| Intended Consumer | Prometheus on `mon01` |
| Current Prometheus Targets | `localhost:9100`, `<DNS01_IP>:9100` |

Node Exporter should not be exposed to the public internet. Metrics can reveal infrastructure details such as hostnames, filesystem paths, kernel information, network interfaces, and resource usage patterns.

## Metrics

Node Exporter exposes metrics collected from Linux kernel and operating system interfaces such as `/proc` and `/sys`.

Examples of useful metric families:

| Metric Family | Purpose |
| --- | --- |
| `node_cpu_seconds_total` | CPU time by CPU core and mode |
| `node_memory_*` | Memory totals, availability, and usage indicators |
| `node_filesystem_*` | Filesystem capacity, free space, and availability |
| `node_network_*` | Network receive/transmit counters |
| `node_boot_time_seconds` | Host boot time for uptime calculations |

## Validation Procedure

Use these commands on the host running Node Exporter:

```bash
systemctl is-active prometheus-node-exporter
curl localhost:9100/metrics
```

Expected results:

- The service returns `active`.
- The `/metrics` endpoint returns a large text response containing metrics beginning with names such as `node_cpu`, `node_memory`, `node_filesystem`, and `node_network`.

Remote scrape validation from `mon01`:

```bash
curl http://<DNS01_IP>:9100/metrics
```

Prometheus validation:

- In the Prometheus web UI, `Status -> Target health` should show the `node_exporter` targets as `UP`.
- The PromQL query `up{job="node_exporter"}` should return `1` for both `mon01` and `dns01`.
- The PromQL query `node_memory_MemAvailable_bytes` should return memory metrics for both monitored hosts.

Grafana validation:

- Open the imported Node Exporter dashboard.
- Select the `node_exporter` job.
- Confirm both `mon01` and `dns01` are available as monitored hosts.
- Confirm dashboard panels populate after Prometheus completes a scrape cycle.

## Security Considerations

- Keep Node Exporter internal-only.
- Do not publish raw metrics output in the repository.
- Do not expose port `9100` to untrusted networks.
- Restrict future Prometheus scrape access to trusted monitoring systems where practical.
- Treat metrics as operationally sensitive because they can reveal infrastructure details.
- Use sanitized placeholders such as `<DNS01_IP>` instead of publishing exact internal addresses.

## Backup Strategy

Node Exporter itself is stateless. The package can be reinstalled from the Debian repository if the host is rebuilt.

Important state belongs to:

- Host configuration.
- Prometheus scrape configuration.
- Documentation in this repository.

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

3. From `mon01`, confirm remote scrape reachability for remote targets:

   ```bash
   curl http://<DNS01_IP>:9100/metrics
   ```

4. Confirm Prometheus can scrape the target:

   ```promql
   up{job="node_exporter"}
   ```

5. Review logs if the service fails to start:

   ```bash
   journalctl -u prometheus-node-exporter --no-pager -n 50
   ```

6. Reinstall the package if needed:

   ```bash
   sudo apt install --reinstall prometheus-node-exporter
   ```

## Maintenance Notes

- Keep the package updated through normal Debian patching.
- Revalidate the `/metrics` endpoint after major OS updates.
- Watch for changes to exposed metrics when Debian or Node Exporter versions change.
- Confirm Prometheus target health after changes to Node Exporter or Prometheus configuration.
- Add future Linux hosts to Prometheus intentionally and label them by host and role.

## Future Improvements

- Add DNS availability checks for `dns01`.
- Add dashboards showing CPU, memory, disk, network, and uptime for all monitored hosts.
- Add Proxmox host monitoring through an appropriate exporter or API-based method.
- Add alerting only after Prometheus and Grafana are working and runbooks exist.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Grafana Service](grafana.md)
- [VM Inventory](../architecture/vm-inventory.md)
