# Monitoring and Observability

## Purpose

This document describes the deployed monitoring architecture, what each monitoring layer proves, and the operational direction for future metrics, dashboards, alerts, and recovery.

Monitoring should identify failures, explain performance problems, support capacity planning, and create repeatable operational habits similar to a small production environment.

## Current Status

Project 002 has delivered a functional host- and service-monitoring foundation.

| Component | Host | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VE | Active | Dedicated monitoring and observability VM |
| Node Exporter | `mon01`, `dns01` | Active | Exposes Linux host metrics |
| Prometheus | `mon01` | Active | Scrapes, stores, and queries metrics |
| Grafana | `mon01` | Active | Visualizes host and service metrics |
| Blackbox Exporter | `mon01` | Active | Performs service-level DNS probes |

Current Prometheus targets:

| Job | Target | Expected State | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | `UP` | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | `UP` | Linux host metrics for `mon01` |
| `node_exporter` | `<DNS01_IP>:9100` | `UP` | Linux host metrics for `dns01` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | `UP` | Recursive DNS resolution probe through `dns01` |

Current Grafana dashboards:

| Dashboard | Status | Purpose |
| --- | --- | --- |
| Imported Node Exporter dashboard | Active | Initial CPU, memory, disk, network, and uptime visibility for `mon01` and `dns01` |
| Homelab Service Health | Active | DNS availability, probe duration, and status history for `dns01` |
| Custom Linux host dashboard | Planned | Homelab-specific host panels and PromQL learning |

## Operational Questions

The current stack should answer:

- Are `mon01` and `dns01` reachable through their metrics endpoints?
- Are CPU, memory, disk, and network resources within expected ranges?
- Is recursive DNS resolution through `dns01` succeeding?
- Did a dashboard stop updating because Grafana failed, Prometheus lost a job, or an exporter became unreachable?
- Is monitoring infrastructure itself under resource pressure?

Future monitoring should also answer:

- Is the Proxmox host healthy?
- Did backups complete successfully?
- Are backup ages and restore tests acceptable?
- Are there actionable security-relevant events?

## Architecture

Host metrics path:

```text
mon01 and dns01
      |
      | /metrics
      v
Node Exporter
      |
      | Prometheus scrape
      v
Prometheus on mon01
      |
      | PromQL
      v
Grafana on mon01
```

DNS service probe path:

```text
Prometheus on mon01
      |
      | scrape /probe
      v
Blackbox Exporter on localhost:9115
      |
      | UDP DNS query
      v
dns01:53
      |
      | recursive resolution
      v
Configured upstream resolver
```

This layered design separates different failure domains:

- Node Exporter reports host state.
- Blackbox Exporter reports service behavior from another system's point of view.
- Prometheus stores and queries the data.
- Grafana visualizes the results.

## Monitoring Layers

### Host Monitoring

Node Exporter answers questions about the Linux operating system:

- CPU time and load.
- Available memory.
- Filesystem capacity.
- Network traffic.
- Host uptime.
- Exporter reachability.

A healthy Node Exporter target does not prove that every application on the host is usable.

### Service Monitoring

Blackbox Exporter checks the DNS endpoint from `mon01`.

The current module queries a public DNS name. A successful result validates:

```text
mon01 -> dns01/Pi-hole -> upstream resolver -> public DNS result
```

A failed probe could indicate:

- Pi-hole or `dns01` failure.
- Internal routing or firewall failure.
- Upstream internet or resolver failure.
- Failure of the configured query.

A future local-record probe should isolate internal DNS functionality from upstream recursive resolution.

### Application Monitoring

Pi-hole-specific application metrics are not yet collected.

Future metrics may include:

- Query volume.
- Blocked-query rate.
- Cache behavior.
- Upstream response behavior.
- Pi-hole application health.

Application metrics should be added only after the operational questions and exporter maintenance requirements are understood.

## Current Tooling Decisions

| Tool | Role | Reason |
| --- | --- | --- |
| Node Exporter | Linux host metrics | Standard Prometheus-compatible host metrics with minimal complexity |
| Prometheus | Metrics collection and storage | Central pull-based scraping, target health, PromQL, and time-series history |
| Grafana | Dashboards | Flexible visualization backed by Prometheus queries |
| Blackbox Exporter | Service probes | Separates service availability from host availability |

The monitoring stack is documented in [ADR-0002](../decisions/ADR-0002-prometheus-grafana-monitoring-stack.md).

## Labels and Target Design

Prometheus uses a shared `node_exporter` job with host and role labels.

Example labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
```

This keeps job names consistent while allowing dashboards and queries to distinguish systems.

`dns01` is monitored using its static address rather than its DNS name so a DNS failure does not prevent the monitoring system from reaching the DNS server.

## PromQL Validation

Expected job and target inventory:

```promql
count by (job, instance) (up)
```

Linux host availability:

```promql
up{job="node_exporter"}
```

DNS probe availability:

```promql
probe_success{job="blackbox_dns"}
```

DNS probe duration:

```promql
probe_duration_seconds{job="blackbox_dns"}
```

Available memory:

```promql
node_memory_MemAvailable_bytes
```

Root-filesystem capacity:

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Configuration validation and PromQL validation must both be performed after Prometheus changes. A syntactically valid configuration can still be operationally wrong if an intended job was removed or renamed.

## Dashboard Strategy

Current approach:

- Use an imported Node Exporter dashboard for immediate host visibility.
- Use a manually built Homelab Service Health dashboard for DNS probe metrics.
- Build a custom Linux host dashboard later to demonstrate intentional panel design and PromQL understanding.

Host and service dashboards remain separate because they answer different questions:

- Host dashboard: **Is the server healthy?**
- Service dashboard: **Is the service usable?**

Important dashboards should eventually be exported as JSON or provisioned from version-controlled configuration.

## Alerting Philosophy

Alerting is not yet enabled.

An alert should answer:

- What failed?
- Why does it matter?
- What should be checked first?
- Which runbook should be followed?

Alerts should be added only after:

- The check is understood.
- A meaningful threshold exists.
- A runbook exists.
- The notification route is documented.
- Repeated low-value notifications are unlikely.

A small number of actionable alerts is more useful than a large noisy ruleset.

## Logging Strategy

Centralized logging is future work.

When implemented, document:

- Log sources.
- Storage location.
- Retention.
- Access controls.
- Security-relevant event sources.
- Privacy and sanitization requirements.

Logs may contain sensitive addresses, usernames, query data, and authentication events and must not be committed to the repository.

## Security Considerations

- Keep Prometheus, Grafana, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose ports `9090`, `3000`, `9100`, or `9115` to untrusted networks.
- Use non-default Grafana credentials stored outside the repository.
- Treat metrics and dashboards as operationally sensitive.
- Do not publish screenshots containing exact addresses, usernames, tokens, or private topology.
- Keep future security-lab monitoring from granting untrusted systems control over monitoring infrastructure.
- Review API credentials carefully before adding Proxmox monitoring.

## Backup and Recovery

The monitoring stack is rebuildable but not protected by validated backups.

Important state includes:

- Prometheus configuration.
- Blackbox Exporter configuration.
- Grafana data sources and dashboards.
- Future alerting and recording rules.
- Historical metrics if retention becomes operationally important.

Project 003 should define how monitoring configuration and dashboards are backed up and restored. Important Grafana dashboards should be exported after their design stabilizes.

## Troubleshooting Lessons

### QEMU Guest Agent Device

During `mon01` deployment, the guest-agent package was installed but the required virtio device was missing. A full Proxmox stop/start recreated the virtual hardware; a guest-only reboot did not.

See [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md).

### Prometheus Job Loss

After adding a scrape job, Grafana stopped showing current Node Exporter data. Prometheus configuration remained syntactically valid, but the intended `node_exporter` job was missing or malformed.

Operational lesson:

- Check Prometheus before changing Grafana.
- Validate expected jobs with `count by (job, instance) (up)`.
- Back up configuration before edits.
- Use both `promtool` and PromQL validation.

See [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md).

### Local-Only Exporter Access

Blackbox Exporter did not need LAN exposure because Prometheus runs on the same VM. `localhost:9115` is sufficient and reduces unnecessary network exposure.

### Imported Dashboard Variables

The imported Node Exporter dashboard expected different job naming. Selecting the local `node_exporter` job allowed both hosts to appear. Imported dashboards should be treated as starting points rather than authoritative configuration.

## Next Improvements

- Build a custom Linux host dashboard.
- Add a local-record DNS probe.
- Evaluate Pi-hole-specific metrics.
- Add Proxmox host monitoring through a documented and least-privilege method.
- Export stable Grafana dashboards.
- Add monitoring configuration backup coverage under Project 003.
- Add actionable alerts only after runbooks and notification routing exist.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
- [Project 002](../projects/project-002-monitoring-observability.md)
- [ADR-0002: Monitoring Stack](../decisions/ADR-0002-prometheus-grafana-monitoring-stack.md)
- [Node Exporter](../services/node-exporter.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
