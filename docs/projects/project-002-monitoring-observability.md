# Project 002: Monitoring and Observability Stack

## Status

In Progress — core monitoring baseline operational; alerting, Pi-hole application metrics, and Proxmox platform metrics remain.

## Current Progress

| Milestone | Status | Notes |
| --- | --- | --- |
| 1. Design and VM Creation | Complete | `mon01` deployed as a dedicated Debian 13.5 monitoring VM. |
| 2. Node Exporter | Complete | Active on `mon01`, `dns01`, and `pve01`. |
| 3. Prometheus | Complete | Scrapes itself, three Node Exporter targets, and two DNS probe jobs. |
| 4. Grafana | Complete | Imported host dashboard, service-health dashboard, and custom infrastructure overview are active. |
| 5. Expand Monitoring Coverage | Complete | `dns01` host and DNS monitoring plus `pve01` operating-system monitoring are active. |
| 6. Alerting and Operational Runbooks | Not Started | Alerts require thresholds, response procedures, and notification routing. |

## Purpose

Project 002 establishes production-style monitoring habits for the homelab. The objective is not merely to install tools, but to understand what each layer proves, validate changes safely, and document operational boundaries honestly.

The project builds on Project 001, where `dns01` became the first core infrastructure VM and Pi-hole became the homelab DNS service.

## Learning Goals

- Distinguish host, service, application, and platform monitoring.
- Understand Prometheus exporters and pull-based collection.
- Write and validate PromQL queries.
- Build useful Grafana panels rather than relying only on imported dashboards.
- Practice configuration backup, validation, rollback, and layered troubleshooting.
- Separate Linux hypervisor metrics from Proxmox platform-specific metrics.
- Document public infrastructure without exposing private addresses or sensitive state.

## Monitoring VM

| Component | Value |
| --- | --- |
| VM name | `mon01` |
| Operating system | Debian 13.5 |
| Deployment model | Dedicated Proxmox VM |
| Primary role | Monitoring and observability |
| Public exposure | None |
| Initial allocation | 2 vCPU, 2 GB RAM, 32 GB disk |
| Current allocation | 2 vCPU, 3 GB RAM, 32 GB disk |

## Current Stack

| Tool | Host or scope | Status | Role |
| --- | --- | --- | --- |
| Node Exporter | `mon01`, `dns01`, `pve01` | Active | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Scraping, time-series storage, and PromQL |
| Grafana | `mon01` | Active | Summary, service-health, and detailed host dashboards |
| Blackbox Exporter | `mon01` | Active | Recursive and local DNS service probes |

## Current Monitoring Scope

| Target | Current checks | Remaining opportunities |
| --- | --- | --- |
| `mon01` | Prometheus self-monitoring, Node Exporter, Grafana, Blackbox Exporter | Alerting and deeper service monitoring |
| `dns01` | Node Exporter, recursive DNS probe, local-record DNS probe, Grafana panels | Pi-hole-specific application metrics |
| `pve01` | Node Exporter host metrics in Prometheus and Grafana | VM, storage-pool, task, and backup metrics through least-privilege Proxmox integration |

## Design Decisions

### Dedicated Monitoring VM

Monitoring runs on `mon01` rather than on `dns01` or directly on the hypervisor.

Reasons:

- Keeps DNS, monitoring, and virtualization responsibilities separate.
- Matches enterprise shared-infrastructure patterns.
- Simplifies backup, restore, and migration testing.
- Avoids making the hypervisor responsible for every application role.

Tradeoffs:

- Adds another system to patch, back up, and monitor.
- Consumes additional compute and storage.
- Requires centralized documentation to control configuration drift.

### Host Metrics Before Service and Application Metrics

Node Exporter was deployed first because it provides a standardized Linux telemetry baseline. Blackbox Exporter was added separately because a host can be healthy while a service is broken. Pi-hole application metrics remain a third layer for future work.

### Shared Node Exporter Job

All Linux systems use one `node_exporter` job with host and role labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

This keeps queries and dashboards consistent.

### Static Infrastructure Targets

Remote targets use static addresses so monitoring remains available during DNS failure. Public documentation uses placeholders such as `<DNS01_IP>` and `<PVE01_IP>`.

### Linux Baseline Before Proxmox API Monitoring

The first Proxmox phase uses Node Exporter.

Reasons:

- Immediate CPU, memory, filesystem, disk, network, and uptime visibility.
- Reuses the existing Prometheus and Grafana architecture.
- Avoids API credentials before a least-privilege model is documented.

Boundary:

- Node Exporter cannot report authoritative VM state, storage-pool health, task results, or backup-job status.

### Separate Recursive and Local DNS Probes

Two jobs isolate different dependencies:

- `blackbox_dns` tests a public A-record query through the upstream resolver.
- `blackbox_dns_local` tests an internal A record and validates the returned answer.

This allows upstream failure to be distinguished from local Pi-hole record failure.

### Summary Dashboard and Detailed Dashboard

- Homelab Infrastructure Overview: at-a-glance health and capacity view.
- Imported Node Exporter dashboard: detailed host troubleshooting.
- Homelab Service Health: DNS service history.

## Implementation Summary

### `mon01` Baseline

- Deployed Debian 13.5 as a headless server.
- Configured non-root administration and QEMU Guest Agent.
- Installed Node Exporter, Prometheus, Grafana, and Blackbox Exporter.
- Configured Grafana to query Prometheus at `http://localhost:9090`.
- Imported a Node Exporter dashboard.
- Created the Homelab Service Health dashboard.
- Increased memory from 2 GB to 3 GB after monitoring showed limited headroom.

### `dns01` Host Monitoring

- Installed Node Exporter.
- Validated metrics locally.
- Confirmed reachability from `mon01` before editing Prometheus.
- Added `<DNS01_IP>:9100` to the shared `node_exporter` job.
- Applied `host="dns01"` and `role="dns"` labels.
- Confirmed Prometheus target health and Grafana visibility.

### Recursive DNS Monitoring

- Installed Blackbox Exporter on `mon01`.
- Added the `dns_udp` module.
- Validated the probe manually before Prometheus integration.
- Added the `blackbox_dns` job.
- Confirmed `probe_success{job="blackbox_dns"}` returns `1`.
- Added DNS availability, duration, and state-history visualization.

Path:

```text
Prometheus -> Blackbox Exporter -> dns01/Pi-hole -> upstream resolver -> public DNS
```

### Local DNS Monitoring

Completed on 2026-07-11:

- Verified the internal record returned an A answer from `dns01`.
- Added `dns_udp_local` as a separate Blackbox module.
- Required an answer-record regular expression so `NOERROR` alone is insufficient.
- Recovered from an initial YAML nesting error by restoring the rollback copy.
- Preflighted the corrected configuration on `127.0.0.1:19115` before restarting the live service.
- Confirmed `probe_dns_answer_rrs 1`, `probe_dns_query_succeeded 1`, and `probe_success 1`.
- Added the `blackbox_dns_local` Prometheus job with `scope="local"`.
- Validated `prometheus.yml` with `promtool`.
- Reloaded Prometheus and confirmed the service remained active.
- Confirmed both recursive and local DNS `probe_success` series returned `1`.

Path:

```text
Prometheus -> Blackbox Exporter -> dns01/Pi-hole -> internal record
```

### `pve01` Host Monitoring

Completed on 2026-07-10:

- Verified Proxmox VE `9.2.2` on Debian 13 Trixie.
- Confirmed the Proxmox firewall was active.
- Installed Node Exporter `1.9.0-1+b4`.
- Confirmed the exporter was active, enabled, and listening on TCP `9100`.
- Confirmed `mon01` could reach the endpoint before editing Prometheus.
- Determined that no broad firewall rule was required.
- Added `<PVE01_IP>:9100` to the shared `node_exporter` job.
- Applied `host="pve01"` and `role="hypervisor"` labels.
- Validated and reloaded Prometheus.
- Confirmed target-specific `up` queries returned `1`.
- Confirmed Grafana displayed host metrics for `pve01`.

### Homelab Infrastructure Overview

Created on 2026-07-11 as a manually built dashboard.

| Panel | Purpose |
| --- | --- |
| Host Availability | Shows current state for `mon01`, `dns01`, and `pve01` |
| CPU Utilization by Host | Compares CPU demand across hosts |
| Memory Utilization by Host | Compares memory usage across hosts |
| Root Filesystem Utilization | Shows filesystem consumption with thresholds |
| Host Uptime | Shows time since each host booted |
| DNS Availability | Shows Recursive DNS and Local DNS independently |
| DNS Probe Duration | Shows DNS latency and spikes over time |

Layout decisions:

- Full-width trend panels improve readability and remove unused grid space.
- Uptime is informational and does not use misleading failure thresholds.
- Recursive and local DNS appear as separate status values.

The dashboard is operational. Its private Classic JSON export remains pending and is not yet a validated recovery artifact.

## Current Prometheus Targets

| Job | Target | Status |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Up |
| `node_exporter` | `localhost:9100` | Up |
| `node_exporter` | `<DNS01_IP>:9100` | Up |
| `node_exporter` | `<PVE01_IP>:9100` | Up |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Up |
| `blackbox_dns_local` | `<DNS01_IP>:53` through `localhost:9115` | Up |

## Validation

### Configuration

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
sudo systemctl reload prometheus
systemctl is-active prometheus
```

### Host Targets

```promql
up{job="node_exporter"}
```

Expected hosts: `mon01`, `dns01`, and `pve01`.

### DNS Probes

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

```promql
probe_success{job=~"blackbox_dns.*", host="dns01"}
```

Both DNS series should return `1`.

### Grafana

Validated:

- All three hosts show `UP`.
- CPU, memory, filesystem, and uptime panels populate.
- Recursive DNS and Local DNS both show `UP`.
- DNS probe duration updates over time.
- The detailed Node Exporter dashboard still displays all monitored hosts.

## Monitoring Boundaries

### `dns01`

- Node Exporter proves the Linux host reports metrics.
- Recursive Blackbox probe proves the public-resolution path works.
- Local Blackbox probe proves the expected internal record is returned.
- Future Pi-hole metrics should describe application behavior.

### `pve01`

Node Exporter proves the hypervisor operating system reports metrics. It does not prove:

- Individual VMs or containers are running.
- Proxmox storage pools are healthy.
- Backup jobs succeeded.
- Proxmox tasks completed.
- Cluster state is healthy.

## Troubleshooting Lessons

### Blackbox YAML Structure

The initial `dns_udp_local` module was nested at the wrong level and Blackbox Exporter rejected the file with:

```text
field dns_udp_local not found in type config.plain
```

Restoring the known-good file first prevented extended monitoring downtime. Preflighting the corrected configuration on an alternate port reduced risk before the live restart.

### New Prometheus Job Delay

An immediate query after reload returned an empty vector. The next scrape showed the new job at `1`. New targets may need one scrape interval before data appears.

### Grafana Query Reference IDs

Prometheus contained both DNS series, but Grafana displayed one until the panel queries used distinct reference IDs `A` and `B`. User-facing labels belong in legends rather than reference-ID fields.

### Dashboard v2 Numeric Thresholds

Grafana dashboard v2 parsing rejected quoted threshold numbers. Numeric threshold values must be JSON numbers, not strings.

### Existing Firewall Policy Before New Rules

Testing from the real monitoring source prevented an unnecessary broad firewall rule on `pve01`.

### Syntactically Valid but Operationally Wrong Prometheus Configuration

`promtool` must be paired with PromQL target validation. A valid file can still omit an intended job or target.

## Security Considerations

- Keep Grafana, Prometheus, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose TCP `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics, dashboard JSON, and screenshots as operationally sensitive.
- Do not publish exact addresses, usernames, tokens, or private record values.
- Avoid broad firewall rules when a trusted path already works.
- Introduce Proxmox API credentials only through a documented least-privilege design.
- Store all credentials outside Git.

## Backup and Recovery

Project 003 Phase 003A inventoried monitoring configuration, Grafana state, existing dashboard exports, and the Prometheus data-source mapping.

Remaining work:

- Export and privately validate the Homelab Infrastructure Overview.
- Implement protected VM backups.
- Validate restoration.
- Expand recovery runbooks from tested results.
- Add backup-job monitoring after the backup platform exists.

## Future Improvements

- Export the Homelab Infrastructure Overview as Classic JSON.
- Add Proxmox-specific VM, storage, task, and backup metrics.
- Add Pi-hole-specific application metrics.
- Add Alertmanager only after runbooks and thresholds exist.
- Add capacity-planning views as historical data matures.
- Integrate future security monitoring without weakening infrastructure isolation.

## Related Documentation

- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Project 003: Backup and Recovery](project-003-backup-recovery.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
