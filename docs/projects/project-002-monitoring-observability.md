# Project 002: Monitoring and Observability Stack

## Status

In Progress — core monitoring foundation operational; alerting, Pi-hole application metrics, and Proxmox platform metrics remain.

## Current Progress

| Milestone | Status | Notes |
| --- | --- | --- |
| 1. Design and VM creation | Complete | `mon01` deployed as a dedicated Debian 13.5 monitoring VM. |
| 2. Node Exporter | Complete | Active on `mon01`, `dns01`, and `pve01`. |
| 3. Prometheus | Complete | Scrapes itself, three Node Exporter targets, and two DNS probe jobs. |
| 4. Grafana | Complete | Detailed host dashboard, service-health dashboard, and custom infrastructure overview are active. |
| 5. Expanded coverage | Complete | `dns01` host and DNS monitoring plus `pve01` operating-system monitoring are active. |
| 6. Backup coverage | Complete | `mon01` receives daily Proxmox backups under Project 003. |
| 7. Alerting and response runbooks | Not started | Alerts require thresholds, response procedures, and notification routing. |

## Purpose

Establish production-style monitoring habits rather than merely install tools. The project documents what each monitoring layer proves, how changes are validated, and where current visibility ends.

## Learning Goals

- Distinguish host, service, application, and platform monitoring.
- Understand exporter-based pull monitoring.
- Write and validate PromQL.
- Build useful Grafana dashboards.
- Practice configuration validation, rollback, backup, and layered troubleshooting.
- Separate Linux hypervisor metrics from Proxmox platform state.
- Document operational data without exposing private topology.

## Monitoring VM

| Component | Value |
| --- | --- |
| VM name | `mon01` |
| Operating system | Debian 13.5 Trixie |
| Deployment | Dedicated Proxmox VM |
| Role | Monitoring and observability |
| Exposure | Internal-only |
| Resources | 2 vCPU, 3 GB RAM, 32 GB disk |
| Backup | Daily Proxmox backup |
| Independent restore test | Not yet completed |

Memory increased from 2 GB to 3 GB after Grafana showed limited headroom.

## Current Stack

| Tool | Host or scope | Role |
| --- | --- | --- |
| Node Exporter | `mon01`, `dns01`, `pve01` | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Scraping, time-series storage, and PromQL |
| Grafana | `mon01` | Summary, service-health, and detailed host dashboards |
| Blackbox Exporter | `mon01` | Recursive and local DNS probes |

## Current Monitoring Scope

| Target | Current checks | Remaining opportunities |
| --- | --- | --- |
| `mon01` | Prometheus self-monitoring, Node Exporter, Grafana, Blackbox service state | Alerting and deeper service metrics |
| `dns01` | Node Exporter, recursive DNS probe, local-record DNS probe, Grafana panels | Pi-hole-specific application metrics |
| `pve01` | Node Exporter metrics in Prometheus and Grafana | VM, storage, task, and backup metrics through least privilege |

## Design Decisions

### Dedicated Monitoring VM

Monitoring runs on `mon01`, not on `dns01` or directly on the hypervisor.

Reasons:

- Separates DNS, monitoring, and virtualization responsibilities.
- Matches shared-infrastructure patterns.
- Avoids turning the hypervisor into an application server.
- Simplifies migration and recovery planning.

Tradeoffs:

- Adds another VM to patch, monitor, and back up.
- Monitoring depends on the host and network it observes.

### Host Metrics Before Application Metrics

Node Exporter established a consistent Linux baseline first. Blackbox Exporter was added because host health does not prove service behavior. Pi-hole application metrics remain a separate future layer.

### Shared Node Exporter Job

All Linux systems use one job with labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

This keeps queries and dashboards consistent.

### Static Infrastructure Targets

Remote monitoring targets use static addresses so monitoring does not depend on the DNS service being monitored. Public documentation uses placeholders such as `<DNS01_IP>` and `<PVE01_IP>`.

### Linux Baseline Before Proxmox API Monitoring

Node Exporter provides CPU, memory, filesystem, disk, network, and uptime visibility without Proxmox API credentials.

It does not report authoritative:

- VM or container state.
- Storage-pool health.
- Task results.
- Backup-job success or age.
- Cluster state.

### Separate Recursive and Local DNS Probes

- `blackbox_dns` tests a public query through Pi-hole and the upstream resolver.
- `blackbox_dns_local` tests an expected internal record and validates its answer.

Separate jobs make failure domains explicit.

## Implementation Summary

### `mon01`

- Deployed Debian 13.5 as a headless VM.
- Configured non-root administration and QEMU Guest Agent.
- Installed Node Exporter, Prometheus, Grafana, and Blackbox Exporter.
- Configured Grafana to use local Prometheus.
- Imported a detailed Node Exporter dashboard.
- Created Homelab Service Health and Infrastructure Overview dashboards.
- Increased RAM after observed utilization showed limited headroom.
- Added daily VM backup coverage under Project 003.

### `dns01`

- Installed Node Exporter.
- Validated local and remote metric reachability.
- Added it to the shared `node_exporter` job.
- Added recursive and local DNS probes.
- Required expected-answer validation for the local record.

### `pve01`

- Installed Node Exporter directly on the Proxmox host.
- Confirmed the existing firewall policy allowed the trusted monitoring path.
- Avoided adding an unnecessary broad rule.
- Added host and role labels.

## Dashboards

| Dashboard | Purpose |
| --- | --- |
| Imported Node Exporter dashboard | Detailed Linux host troubleshooting |
| Homelab Service Health | DNS availability, probe duration, and state history |
| Homelab Infrastructure Overview | Host availability, CPU, memory, root filesystem, uptime, recursive DNS, and local DNS |

The Infrastructure Overview is operational. Its protected Classic JSON export remains follow-up work.

## Prometheus Inventory

| Job | Target role | Expected state |
| --- | --- | --- |
| `prometheus` | Prometheus self-monitoring | Up |
| `node_exporter` | `mon01` | Up |
| `node_exporter` | `dns01` | Up |
| `node_exporter` | `pve01` | Up |
| `blackbox_dns` | Recursive DNS through `dns01` | Up |
| `blackbox_dns_local` | Expected local record through `dns01` | Up |

## Validation

Configuration:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
sudo systemctl reload prometheus
systemctl is-active prometheus
```

Host targets:

```promql
up{job="node_exporter"}
```

Expected hosts: `mon01`, `dns01`, and `pve01`.

DNS probes:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Both should return `1`.

Grafana validation:

- All three hosts show current data.
- CPU, memory, filesystem, and uptime panels populate.
- Recursive and local DNS display independently.
- Probe duration updates.

## Troubleshooting Lessons

### Blackbox YAML Structure

The first local-DNS module was placed at the wrong YAML level. The safe recovery pattern was:

1. Restore the known-good file.
2. Confirm the live service recovered.
3. Correct indentation.
4. Preflight on an alternate local port.
5. Restart the production service only after validation.

### New Prometheus Target Delay

A new job may return an empty vector until the first scrape completes. Wait one scrape interval before treating it as missing.

### Grafana Query Reference IDs

Prometheus returned both DNS series, but Grafana displayed one until queries used distinct reference IDs. User-facing names belong in legends.

### Valid Syntax Is Not Complete Validation

`promtool` can pass while an intended job or target is absent. Always pair syntax checks with PromQL inventory queries.

### Firewall State Is Not Proof of Blocking

Testing from the intended source showed the existing `pve01` policy already allowed Node Exporter. No broad rule was needed.

## Security Considerations

- Keep Grafana, Prometheus, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose TCP `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics, labels, dashboard JSON, and screenshots as operationally sensitive.
- Do not publish exact targets, private record values, tokens, or credentials.
- Add Proxmox API credentials only through a documented least-privilege design.
- Keep attacker-style workloads isolated from monitoring and backup infrastructure.

## Backup and Recovery

Project 003 completed VM-level backup implementation for `mon01`:

- Daily snapshot-mode backup.
- Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external Proxmox storage with mount-point enforcement.

Additional recovery assets:

- Prometheus and Blackbox configuration inventory.
- Grafana database and Prometheus data-source mapping.
- Protected Node Exporter and Homelab Service Health dashboard exports.
- Sanitized rebuild documentation.

Current boundary:

- `mon01` has a successful backup but has not been independently restored.
- The Infrastructure Overview still needs a protected Classic JSON export.
- Project 003's `dns01` restore proved the general Proxmox backup and restore workflow, but not `mon01` application recovery.

## Future Improvements

- Export and privately validate the Homelab Infrastructure Overview.
- Add Proxmox VM, storage, task, and backup metrics.
- Add backup-age and job-failure monitoring.
- Add Pi-hole-specific application metrics.
- Add Alertmanager only after thresholds, runbooks, and notification routing exist.
- Perform an independent `mon01` restore test.
- Add capacity-planning views as historical data matures.

## Related Documentation

- [Monitoring Architecture](../architecture/monitoring.md)
- [Node Exporter](../services/node-exporter.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Project 003](project-003-backup-recovery.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)