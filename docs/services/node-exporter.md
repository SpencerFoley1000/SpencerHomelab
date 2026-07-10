# Node Exporter

## Status

Active

## Purpose

Node Exporter exposes Linux host metrics in a Prometheus-compatible format. It provides the operating-system telemetry used for CPU, memory, filesystem, network, and uptime monitoring.

Node Exporter answers questions such as:

- Is the host reachable by Prometheus?
- How much CPU time and load is the host experiencing?
- How much memory remains available?
- Are monitored filesystems approaching capacity?
- How much network traffic is passing through the host?
- When was the host last booted?

Node Exporter reports host state. It does not prove that an application, virtual machine, backup job, or Proxmox management function is working correctly.

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Node Exporter |
| Package | `prometheus-node-exporter` |
| Package version | `1.9.0-1+b4` |
| Hosts | `mon01`, `dns01`, `pve01` |
| Deployment method | Debian package repository |
| Default port | `9100/tcp` |
| Metrics path | `/metrics` |
| Scraper | Prometheus on `mon01` |

## Monitored Hosts

| Hostname | Role | Prometheus target | Label set | Status |
| --- | --- | --- | --- | --- |
| `mon01` | Monitoring VM | `localhost:9100` | `host="mon01"`, `role="monitoring"` | Active |
| `dns01` | DNS VM | `<DNS01_IP>:9100` | `host="dns01"`, `role="dns"` | Active |
| `pve01` | Proxmox hypervisor | `<PVE01_IP>:9100` | `host="pve01"`, `role="hypervisor"` | Active |

Static addresses are used for remote targets so monitoring does not depend on DNS during an outage. Exact addresses are intentionally omitted from the public repository.

## Deployment Notes

Node Exporter is installed from the Debian package repository:

```bash
sudo apt install --no-install-recommends prometheus-node-exporter
```

The service is enabled automatically by the package and was validated locally on each host:

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
- The process listens on TCP port `9100`.

### Proxmox Host Deployment

The initial `pve01` monitoring baseline was added on 2026-07-10:

- Proxmox VE version verified as `9.2.2`.
- Debian base verified as Debian 13 Trixie.
- Node Exporter package version `1.9.0-1+b4` installed.
- Local `/metrics` endpoint validated.
- Remote reachability validated from `mon01` before changing Prometheus.
- Existing Proxmox firewall policy allowed the trusted monitoring connection; no broad firewall rule was added.
- Prometheus configuration passed `promtool` validation before reload.
- Both host and role-specific PromQL queries returned `1`.
- Grafana displayed CPU, memory, filesystem, network, and uptime data for `pve01`.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9100/tcp` |
| Access scope | Trusted internal homelab network |
| Public exposure | None |
| Intended consumer | Prometheus on `mon01` |
| Remote targets | `<DNS01_IP>:9100`, `<PVE01_IP>:9100` |

Node Exporter must not be exposed to the public internet. Metrics can reveal hostnames, kernel details, filesystem paths, network interfaces, device names, and resource-usage patterns.

The current Proxmox firewall is active. Monitoring reachability should be revalidated after firewall, VLAN, routing, or management-network changes.

## Metrics

Node Exporter reads Linux kernel and operating-system data from sources such as `/proc` and `/sys`.

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

Run on the monitored host:

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

A `curl: (23)` message can appear when output is piped to `head`; this is expected because `head` closes the pipe after receiving the requested lines.

### Prometheus

```promql
up{job="node_exporter"}
```

Expected hosts:

- `mon01`
- `dns01`
- `pve01`

Target-specific validation:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

Additional checks:

```promql
node_memory_MemAvailable_bytes
```

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

### Grafana

- Open the Node Exporter dashboard.
- Select the `node_exporter` job.
- Select the intended host or instance.
- Confirm CPU, memory, filesystem, network, and uptime panels populate.

## Monitoring Boundaries

For `dns01`:

- Node Exporter answers: **Is the Linux host running and reporting metrics?**
- Blackbox Exporter answers: **Does the DNS endpoint answer the configured query?**
- Future Pi-hole metrics should answer: **How is the DNS application behaving internally?**

For `pve01`:

- Node Exporter answers: **Is the hypervisor operating system healthy?**
- It does not report authoritative VM state, cluster state, Proxmox task results, storage-pool status, or backup-job success.
- Proxmox-specific monitoring should be added later through a documented least-privilege API or exporter design.

## Security Considerations

- Keep Node Exporter internal-only.
- Do not publish raw metrics output.
- Do not expose port `9100` to untrusted networks.
- Restrict scrape access to trusted monitoring systems where practical.
- Treat metrics as operationally sensitive.
- Use placeholders such as `<DNS01_IP>` and `<PVE01_IP>` in public documentation.
- Reassess access after management-network or firewall segmentation is implemented.

## Backup Strategy

Node Exporter is stateless and can be reinstalled from the Debian repository.

Important recovery state belongs to:

- Prometheus scrape configuration.
- Host firewall or network policy.
- Package and service-state documentation.
- This repository.

No dedicated Node Exporter data backup is required.

## Recovery Procedure

If a target stops reporting:

1. Check the exporter service locally.
2. Confirm `/metrics` responds on `localhost:9100`.
3. Confirm remote reachability from `mon01`.
4. Validate Prometheus configuration with `promtool`.
5. Query `up{job="node_exporter"}` and inspect the target labels.
6. Review exporter and Prometheus logs.
7. Check routing, VLAN, and firewall changes.
8. Reinstall the package if required.
9. Confirm Grafana panels resume updating.

Useful commands:

```bash
systemctl status prometheus-node-exporter
journalctl -u prometheus-node-exporter --no-pager -n 50
sudo apt install --reinstall prometheus-node-exporter
```

## Maintenance Notes

- Keep the package updated through normal Debian patching.
- Revalidate `/metrics` after major operating-system or Proxmox upgrades.
- Review target health after every Prometheus configuration change.
- Add new hosts intentionally with consistent `host` and `role` labels.
- Keep host monitoring separate from service and application monitoring.
- Revalidate `pve01` access after Proxmox firewall changes.

## Future Improvements

- Add Proxmox-specific VM, storage-pool, task, and backup metrics using least-privilege credentials.
- Build a custom Linux and hypervisor dashboard for the actual homelab priorities.
- Add actionable resource alerts only after thresholds and runbooks are defined.
- Restrict scrape traffic further when management-network segmentation is implemented.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Blackbox Exporter Service](blackbox-exporter.md)
- [Grafana Service](grafana.md)
- [Proxmox VE Platform](proxmox.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
