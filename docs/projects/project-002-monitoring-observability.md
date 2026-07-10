# Project 002: Monitoring and Observability Stack

## Status

In Progress — monitoring baseline operational; alerting and advanced platform metrics remain.

## Current Progress

| Milestone | Status | Notes |
| --- | --- | --- |
| 1. Design and VM Creation | Complete | `mon01` deployed as a dedicated Debian 13.5 monitoring VM. |
| 2. Node Exporter | Complete | Node Exporter active on `mon01`, `dns01`, and `pve01`. |
| 3. Prometheus | Complete | Prometheus scrapes itself, three Node Exporter endpoints, and the DNS probe. |
| 4. Grafana | Complete | Grafana visualizes host metrics and DNS service health. |
| 5. Expand Monitoring Coverage | Complete | `dns01` host and DNS monitoring plus `pve01` operating-system monitoring are active. |
| 6. Alerting and Operational Runbooks | Not Started | Alerts will be added only after thresholds, ownership, and response runbooks are defined. |

## Purpose

Project 002 introduces a dedicated monitoring and observability stack for the homelab. The goal is not simply to deploy tools, but to understand what each monitoring layer proves and to build operational habits resembling a small production environment.

The project builds on Project 001, where `dns01` became the first core infrastructure VM and Pi-hole became the homelab DNS service.

## Learning Goals

- Understand the difference between host, service, and application monitoring.
- Learn how Prometheus exporters expose metrics.
- Understand pull-based metrics collection and time-series storage.
- Build and interpret PromQL queries.
- Use Grafana for troubleshooting and capacity visibility.
- Practice safe configuration changes, validation, rollback preparation, and documentation.
- Distinguish Linux hypervisor metrics from Proxmox platform-specific metrics.

## Monitoring VM

| Component | Value |
| --- | --- |
| VM name | `mon01` |
| Operating system | Debian 13.5 |
| Deployment model | Dedicated VM on Proxmox VE |
| Primary role | Monitoring and observability services |
| Network role | Internal-only monitoring endpoint |
| Public exposure | None |
| Initial allocation | 2 vCPU, 2 GB RAM, 32 GB disk |
| Current allocation | 2 vCPU, 3 GB RAM, 32 GB disk |

## Current Software Stack

| Tool | Host or scope | Status | Role |
| --- | --- | --- | --- |
| Node Exporter | `mon01`, `dns01`, `pve01` | Active | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Metrics scraping, storage, and PromQL |
| Grafana | `mon01` | Active | Host and service-health dashboards |
| Blackbox Exporter | `mon01` | Active | DNS availability probe through `dns01` |

## Current Monitoring Scope

| Target | Current checks | Remaining opportunities |
| --- | --- | --- |
| `mon01` | Prometheus self-monitoring, Node Exporter, Grafana, Blackbox Exporter | Alerting and custom dashboards |
| `dns01` | Node Exporter, DNS availability probe, Grafana service-health panels | Pi-hole-specific metrics and local-record probe |
| `pve01` | Node Exporter host metrics in Prometheus and Grafana | VM, storage-pool, task, and backup metrics through a least-privilege Proxmox integration |

## Design Decisions

### Dedicated Monitoring VM

Monitoring runs on `mon01` instead of directly on `dns01` or the Proxmox host.

Reasons:

- Keeps DNS and monitoring roles separate.
- Avoids combining every infrastructure responsibility on the hypervisor.
- Matches enterprise patterns where monitoring is shared infrastructure.
- Makes backup, restore, and migration testing cleaner.

Tradeoffs:

- Consumes additional compute and storage.
- Adds another system that must be patched, backed up, and monitored.
- Requires centralized documentation to prevent configuration drift.

### Host Metrics Before Service and Application Metrics

Node Exporter was deployed first because it provides a simple, standardized Linux telemetry baseline.

Blackbox Exporter was added separately because a host can be running while DNS is unavailable. Pi-hole-specific metrics remain future work because they answer a third class of question: how the application behaves internally.

### Pull-Based Collection

Prometheus pulls metrics from known targets.

Reasons:

- Targets are centrally configured.
- Prometheus controls scrape intervals.
- Missing targets become visible failures.
- The model scales cleanly as hosts are added.

### Shared Node Exporter Job

All Linux hosts use one `node_exporter` job with `host` and `role` labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

This keeps queries and dashboard variables consistent.

### Static Addresses for Infrastructure Targets

Remote targets use static addresses rather than DNS names.

Reasons:

- Monitoring continues during DNS failure.
- The monitoring path does not depend on the service being monitored.
- Public documentation can use placeholders without exposing exact addresses.

### Linux Baseline Before Proxmox API Monitoring

The first Proxmox monitoring phase uses Node Exporter rather than an API exporter.

Reasons:

- Delivers immediate CPU, memory, filesystem, disk, network, and uptime visibility.
- Reuses the existing Prometheus and Grafana design.
- Avoids introducing API credentials before a least-privilege model is documented.
- Creates a safe baseline before adding platform-specific complexity.

Tradeoff:

- Node Exporter cannot report authoritative VM state, storage-pool health, task results, or backup-job status.

## Implementation Summary

### `mon01` Baseline

- Deployed Debian 13.5 as a headless server.
- Configured non-root administration and QEMU Guest Agent.
- Installed Node Exporter, Prometheus, Grafana, and Blackbox Exporter.
- Configured Grafana to use Prometheus at `http://localhost:9090`.
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

### `dns01` DNS Availability Monitoring

- Installed Blackbox Exporter on `mon01`.
- Added a `dns_udp` module.
- Validated the probe manually before Prometheus integration.
- Added the `blackbox_dns` job.
- Confirmed `probe_success{job="blackbox_dns"}` returns `1`.
- Added Grafana panels for availability, duration, and state history.

Current path:

```text
Prometheus -> Blackbox Exporter on localhost:9115 -> dns01:53
```

### `pve01` Host Monitoring

Completed on 2026-07-10:

- Verified Proxmox VE `9.2.2` on Debian 13 Trixie.
- Verified running kernel `7.0.2-6-pve`.
- Confirmed the Proxmox firewall was active.
- Installed Node Exporter package version `1.9.0-1+b4`.
- Confirmed the exporter was active and enabled.
- Confirmed `/metrics` responded locally and TCP `9100` was listening.
- Confirmed `mon01` could reach `<PVE01_IP>:9100` before changing Prometheus.
- Determined that no broad firewall rule was required.
- Backed up the Prometheus configuration locally before editing.
- Added `<PVE01_IP>:9100` to the existing `node_exporter` job.
- Applied `host="pve01"` and `role="hypervisor"` labels.
- Validated Prometheus configuration successfully with `promtool`.
- Reloaded Prometheus and confirmed the service remained active.
- Confirmed both general and role-specific `up` queries returned `1`.
- Confirmed Grafana displayed CPU, memory, filesystem, network, and uptime panels for `pve01`.

## Current Prometheus Targets

| Job | Target | Status |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Up |
| `node_exporter` | `localhost:9100` | Up |
| `node_exporter` | `<DNS01_IP>:9100` | Up |
| `node_exporter` | `<PVE01_IP>:9100` | Up |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Up |

## Validation

### Node Exporter

Local validation:

```bash
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
curl -s http://localhost:9100/metrics | head
```

Remote validation from `mon01`:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  http://<TARGET_IP>:9100/metrics | head
```

A `curl: (23)` message may occur when output is piped to `head`; this is expected when `head` closes the pipe after receiving the requested lines.

### Prometheus Configuration

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
sudo systemctl reload prometheus
systemctl is-active prometheus
```

### PromQL

All host targets:

```promql
up{job="node_exporter"}
```

Proxmox host:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

DNS service:

```promql
probe_success{job="blackbox_dns"}
```

Target inventory:

```promql
count by (job, instance) (up)
```

### Grafana

Validated results:

- Prometheus data source test succeeds.
- Node Exporter dashboard displays `mon01`, `dns01`, and `pve01`.
- CPU, memory, filesystem, network, and uptime panels populate for `pve01`.
- Homelab Service Health displays DNS probe state for `dns01`.

## Monitoring Boundaries

### `dns01`

- Node Exporter proves the Linux host reports metrics.
- Blackbox Exporter proves the configured DNS query path works.
- Future Pi-hole metrics should describe application behavior.

### `pve01`

Node Exporter proves the hypervisor operating system reports metrics. It does not prove:

- Individual VMs or containers are running.
- Proxmox storage pools are healthy.
- Backup jobs succeeded.
- Proxmox tasks completed.
- Cluster state is healthy.

Those capabilities require a future Proxmox-specific integration.

## Security Considerations

- Keep Grafana, Prometheus, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose ports `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics and dashboards as operationally sensitive.
- Do not publish screenshots containing exact addresses, usernames, tokens, or private topology.
- Use placeholders such as `<DNS01_IP>`, `<MON01_IP>`, and `<PVE01_IP>`.
- Avoid broad firewall rules when the existing trusted path already works.
- Introduce Proxmox API credentials only through a documented least-privilege design.
- Store all credentials outside Git.

## Troubleshooting Lessons

### QEMU Guest Agent Device

A guest reboot is not always equivalent to a hypervisor-level stop and start. Missing virtual hardware may require a complete Proxmox power cycle of the VM.

### Syntactically Valid but Operationally Wrong Prometheus Configuration

`promtool` validation must be paired with PromQL target validation. A valid file can still omit an intended job or target.

### Local-Only Exporter Access

Blackbox Exporter can remain on `localhost:9115` because Prometheus runs on the same VM. Services do not require unnecessary LAN exposure.

### Existing Firewall Policy Before New Rules

Testing from the actual monitoring source before adding a firewall rule prevented unnecessary exposure on `pve01`.

### Imported Dashboard Variables

Imported dashboards may assume different job or instance variables. Refresh and select the correct `node_exporter` job before modifying panel queries.

## Milestones

### Milestone 1: Design and VM Creation

Status: Complete

### Milestone 2: Node Exporter

Status: Complete

- Active on `mon01`, `dns01`, and `pve01`.
- Local and remote endpoint validation completed.
- Host and role labels documented.

### Milestone 3: Prometheus

Status: Complete

- Self-monitoring active.
- Three Node Exporter endpoints active.
- DNS probe active.
- Configuration and PromQL validation procedures documented.

### Milestone 4: Grafana

Status: Complete

- Prometheus data source active.
- Imported host dashboard active.
- Custom DNS service-health dashboard active.
- `pve01` host data visible.

### Milestone 5: Expand Monitoring Coverage

Status: Complete

- `dns01` host metrics active.
- DNS service probe active.
- `pve01` operating-system metrics active.
- Remaining application and Proxmox API metrics are future enhancements rather than baseline blockers.

### Milestone 6: Alerting and Operational Runbooks

Status: Not Started

- Define actionable thresholds.
- Avoid noisy alerts.
- Create response runbooks.
- Select and document notification routing.

## Backup and Recovery

Project 003 Phase 003A inventoried monitoring configuration, Grafana state, dashboard exports, and data-source mapping.

Remaining work:

- Implement protected VM backups.
- Validate restoration.
- Expand recovery runbooks from tested results.
- Add backup-job monitoring after the backup platform exists.

## Future Improvements

- Build a custom Linux and hypervisor dashboard.
- Add Proxmox-specific VM, storage, task, and backup metrics.
- Add Pi-hole-specific metrics.
- Add a local-record DNS probe.
- Add Alertmanager only after runbooks and thresholds exist.
- Add capacity-planning dashboards.
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
