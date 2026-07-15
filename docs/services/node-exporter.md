# Node Exporter

## Status

Active

## Purpose

Node Exporter exposes Linux host metrics in a Prometheus-compatible format. It provides the operating-system telemetry used for CPU, memory, filesystem, disk, network, and uptime monitoring.

Node Exporter answers:

- Is the host reachable by Prometheus?
- How much CPU time and load is the host experiencing?
- How much memory remains available?
- Are monitored filesystems approaching capacity?
- How much network and disk activity is occurring?
- When was the host last booted?

Node Exporter reports host state. It does not prove that an application, proxy route, certificate, virtual machine, backup job, storage pool, or Proxmox management function is working correctly.

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Node Exporter |
| Package | `prometheus-node-exporter` |
| Verified package version | `1.9.0-1+b4` on the established hosts |
| Hosts | `mon01`, `dns01`, `pve01`, `proxy01` |
| Deployment method | Debian package repository |
| Default port | `9100/tcp` |
| Metrics path | `/metrics` |
| Scraper | Prometheus on `mon01` |
| Public exposure | None |

## Monitored Hosts

| Hostname | Role | Prometheus target | Label set | Status |
| --- | --- | --- | --- | --- |
| `mon01` | Monitoring VM | `localhost:9100` | `host="mon01"`, `role="monitoring"` | Active |
| `dns01` | DNS VM | `<DNS01_IP>:9100` | `host="dns01"`, `role="dns"` | Active |
| `pve01` | Proxmox hypervisor | `<PVE01_IP>:9100` | `host="pve01"`, `role="hypervisor"` | Active |
| `proxy01` | Reverse-proxy VM | `<PROXY01_IP>:9100` | `host="proxy01"`, `role="reverse-proxy"` | Active |

Stable addresses are used for remote infrastructure targets so monitoring does not depend on DNS during an outage. Exact addresses are intentionally omitted.

## Deployment

Install from the Debian package repository:

```bash
sudo apt install --no-install-recommends prometheus-node-exporter
```

Validate locally:

```bash
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
curl -s http://localhost:9100/metrics | head
ss -ltnp | grep 9100
```

Expected results:

- Service state is `active`.
- Boot state is `enabled`.
- `/metrics` returns Prometheus-formatted output.
- The process listens on TCP `9100`.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9100/tcp` |
| Access scope | Trusted internal homelab network |
| Intended consumer | Prometheus on `mon01` |
| Remote targets | `<DNS01_IP>:9100`, `<PVE01_IP>:9100`, `<PROXY01_IP>:9100` |

Node Exporter must not be exposed publicly. Metrics can reveal hostnames, kernel details, filesystem paths, network interfaces, device names, and usage patterns.

Monitoring reachability must be revalidated after firewall, VLAN, routing, or management-network changes.

## Metrics

| Metric family | Purpose |
| --- | --- |
| `node_cpu_seconds_total` | CPU time by core and mode |
| `node_load1`, `node_load5`, `node_load15` | System load averages |
| `node_memory_*` | Memory totals and availability |
| `node_filesystem_*` | Filesystem capacity and free space |
| `node_disk_*` | Block-device activity |
| `node_network_*` | Network receive and transmit counters |
| `node_boot_time_seconds` | Host boot time for uptime calculations |

## Validation Procedure

### Local Endpoint

```bash
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
curl -s http://localhost:9100/metrics | head
```

### Remote Endpoint

Run from `mon01`:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  http://<TARGET_IP>:9100/metrics | head
```

A `curl: (23)` message may appear when output is piped to `head`; `head` closes the pipe after receiving the requested lines.

### Prometheus

```promql
up{job="node_exporter"}
```

Expected hosts:

- `mon01`
- `dns01`
- `pve01`
- `proxy01`

Target-specific validation:

```promql
up{job="node_exporter", host="proxy01", role="reverse-proxy"}
```

Expected result: `1`.

### Grafana

- Open the detailed Node Exporter dashboard for troubleshooting.
- Open the Homelab Infrastructure Overview for at-a-glance comparison.
- Confirm all four hosts display current CPU, memory, filesystem, and uptime data.

## Monitoring Boundaries

For `dns01`:

- Node Exporter answers: **Is the Linux host running and reporting metrics?**
- Blackbox Exporter answers: **Do recursive and local DNS checks succeed?**

For `proxy01`:

- Node Exporter answers: **Is the Linux host running and reporting metrics?**
- Blackbox Exporter answers: **Do the HTTPS routes and certificates work from `mon01`?**
- NGINX Proxy Manager and Docker state require service-level checks or local troubleshooting.

For `pve01`:

- Node Exporter answers: **Is the hypervisor operating system reporting expected Linux metrics?**
- It does not report authoritative VM state, cluster state, task results, storage-pool status, or backup-job success.
- Proxmox-specific monitoring should use a documented least-privilege API or exporter design.

## Security Considerations

- Keep Node Exporter internal-only.
- Do not publish raw metrics output.
- Do not expose TCP `9100` to untrusted networks.
- Restrict scrape access to trusted monitoring systems where practical.
- Treat metrics as operationally sensitive.
- Use placeholders such as `<DNS01_IP>`, `<PVE01_IP>`, and `<PROXY01_IP>` publicly.
- Reassess access after segmentation or firewall changes.

## Backup Strategy

Node Exporter is stateless and can be reinstalled from the Debian repository.

Important recovery state belongs to:

- Prometheus scrape configuration.
- Host firewall or network policy.
- Package and service-state documentation.
- The repository.
- Whole-VM backup for stable infrastructure guests.

No dedicated Node Exporter data backup is required.

## Recovery Procedure

If a target stops reporting:

1. Check the exporter service locally.
2. Confirm `/metrics` responds on `localhost:9100`.
3. Confirm remote reachability from `mon01`.
4. Validate Prometheus configuration with `promtool`.
5. Query `up{job="node_exporter"}` and inspect labels.
6. Review exporter and Prometheus logs.
7. Check routing, VLAN, and firewall changes.
8. Reinstall the package if required.
9. Confirm both detailed and overview Grafana dashboards resume updating.

Useful commands:

```bash
systemctl status prometheus-node-exporter
journalctl -u prometheus-node-exporter --no-pager -n 50
sudo apt install --reinstall prometheus-node-exporter
```

## Maintenance Notes

- Keep the package updated through normal Debian maintenance.
- Revalidate `/metrics` after major operating-system or Proxmox upgrades.
- Review target health after every Prometheus configuration change.
- Add new hosts with consistent `host` and `role` labels.
- Keep host monitoring separate from service and application monitoring.
- Revalidate access after firewall or segmentation changes.
- Add the future X299 server only after local hardware validation and a documented role decision.

## Future Improvements

- Add Proxmox-specific VM, storage-pool, task, and backup metrics using least-privilege credentials.
- Add actionable resource alerts only after thresholds and runbooks are defined.
- Restrict scrape traffic further when management-network segmentation is implemented.
- Add the future server to Prometheus and Grafana after it passes deployment gates.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [NGINX Proxy Manager](nginx-proxy-manager.md)
- [Proxmox VE Platform](proxmox.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Future Virtualization Server Build](../hardware/server-build.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
