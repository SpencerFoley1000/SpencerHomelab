# Monitoring and Observability

## Purpose

This document describes the deployed monitoring architecture, what each monitoring layer proves, and the operational direction for metrics, dashboards, alerts, and recovery.

Monitoring should identify failures, explain performance problems, support capacity planning, and create repeatable operational habits similar to a small production environment.

## Current Status

Project 002 has delivered a functional host- and service-monitoring foundation.

| Component | Host | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VE | Active | Dedicated monitoring and observability VM |
| Node Exporter | `mon01`, `dns01`, `pve01` | Active | Exposes Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Scrapes, stores, and queries metrics |
| Grafana | `mon01` | Active | Visualizes host and service metrics |
| Blackbox Exporter | `mon01` | Active | Performs service-level DNS probes |

Current Prometheus targets:

| Job | Target | Expected state | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | `UP` | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | `UP` | Linux host metrics for `mon01` |
| `node_exporter` | `<DNS01_IP>:9100` | `UP` | Linux host metrics for `dns01` |
| `node_exporter` | `<PVE01_IP>:9100` | `UP` | Linux operating-system metrics for `pve01` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | `UP` | Recursive DNS probe through `dns01` |

Current Grafana dashboards:

| Dashboard | Status | Purpose |
| --- | --- | --- |
| Imported Node Exporter dashboard | Active | CPU, memory, filesystem, network, and uptime visibility for `mon01`, `dns01`, and `pve01` |
| Homelab Service Health | Active | DNS availability, probe duration, and status history for `dns01` |
| Custom Linux and hypervisor dashboard | Planned | Homelab-specific host panels and PromQL learning |

## Operational Questions

The current stack answers:

- Are `mon01`, `dns01`, and `pve01` reachable through their metrics endpoints?
- Are CPU, memory, filesystem, and network resources within expected ranges?
- Is recursive DNS resolution through `dns01` succeeding?
- Is the Proxmox host operating system under resource pressure?
- Did a dashboard stop updating because Grafana failed, Prometheus lost a target, or an exporter became unreachable?
- Is the monitoring infrastructure itself under resource pressure?

The current stack does not yet answer:

- Which Proxmox VMs or containers are running?
- Did a Proxmox task or backup job succeed?
- Are Proxmox storage pools healthy from the platform API perspective?
- Are backup ages and restore tests acceptable?
- Are there actionable security-relevant events?

## Architecture

### Host Metrics Path

```text
mon01, dns01, and pve01
          |
          | /metrics on TCP 9100
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

### DNS Service Probe Path

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

This layered design separates failure domains:

- Node Exporter reports Linux host state.
- Blackbox Exporter reports DNS behavior from another system's point of view.
- Prometheus stores and queries metrics.
- Grafana visualizes the results.
- Future Proxmox API monitoring will report platform-specific state that Node Exporter cannot observe.

## Monitoring Layers

### Host Monitoring

Node Exporter reports:

- CPU time and load.
- Available memory.
- Filesystem capacity.
- Disk activity.
- Network traffic.
- Host uptime.
- Exporter reachability.

A healthy Node Exporter target does not prove that every application or virtual machine is usable.

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

A future local-record probe should isolate internal DNS functionality from upstream recursion.

### Application Monitoring

Pi-hole-specific application metrics are not yet collected. Future metrics may include query volume, blocked-query rate, cache behavior, and upstream response behavior.

### Hypervisor Platform Monitoring

`pve01` currently exposes Linux operating-system metrics through Node Exporter.

This baseline provides useful visibility without introducing API credentials, but it does not expose:

- VM or container state.
- Cluster status.
- Proxmox task results.
- Storage-pool state.
- Backup-job health.
- Replication or migration status.

A future Proxmox exporter or API integration should use a dedicated least-privilege identity and must be documented before credentials are created.

## Current Tooling Decisions

| Tool | Role | Reason |
| --- | --- | --- |
| Node Exporter | Linux host metrics | Standard Prometheus-compatible telemetry with minimal complexity |
| Prometheus | Metrics collection and storage | Central pull-based scraping, target health, PromQL, and time-series history |
| Grafana | Dashboards | Flexible visualization backed by Prometheus |
| Blackbox Exporter | Service probes | Separates service availability from host availability |

The monitoring stack is documented in [ADR-0002](../decisions/ADR-0002-prometheus-grafana-monitoring-stack.md).

## Labels and Target Design

Prometheus uses one shared `node_exporter` job with host and role labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

This keeps job names consistent while allowing dashboards and queries to distinguish systems.

Remote targets use static addresses so monitoring continues during DNS failure. Exact addresses remain private and are represented with placeholders.

## Proxmox Host Monitoring Implementation

The first `pve01` monitoring baseline was completed on 2026-07-10.

Validated sequence:

1. Verified Proxmox VE `9.2.2` on Debian 13 Trixie.
2. Verified the Proxmox firewall was active.
3. Installed Node Exporter package version `1.9.0-1+b4`.
4. Confirmed the service was active and enabled.
5. Confirmed `/metrics` responded locally and TCP `9100` was listening.
6. Confirmed `mon01` could reach the endpoint before editing Prometheus.
7. Added `<PVE01_IP>:9100` to the existing `node_exporter` job.
8. Applied `host="pve01"` and `role="hypervisor"` labels.
9. Validated the Prometheus configuration with `promtool`.
10. Reloaded Prometheus and confirmed the service remained active.
11. Confirmed both general and role-specific `up` queries returned `1`.
12. Confirmed Grafana displayed the expected host panels.

No broad firewall rule was added because the existing policy already allowed the trusted monitoring connection.

## PromQL Validation

Inventory expected jobs and instances:

```promql
count by (job, instance) (up)
```

All monitored Linux hosts:

```promql
up{job="node_exporter"}
```

Proxmox host specifically:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

DNS probe availability:

```promql
probe_success{job="blackbox_dns"}
```

Available memory:

```promql
node_memory_MemAvailable_bytes
```

Root-filesystem capacity:

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Configuration validation and PromQL validation must both be performed after Prometheus changes. Valid syntax does not prove the intended jobs and targets are present.

## Dashboard Strategy

Current approach:

- Use an imported Node Exporter dashboard for immediate host visibility.
- Use a manually built Homelab Service Health dashboard for DNS probe metrics.
- Build a custom Linux and hypervisor dashboard later to demonstrate intentional panel design and PromQL understanding.

Host and service dashboards remain separate:

- Host dashboard: **Is the system healthy?**
- Service dashboard: **Is the service usable?**
- Future Proxmox dashboard: **Is the virtualization platform operating correctly?**

Important dashboards are protected through private JSON exports documented by Project 003.

## Alerting Philosophy

Alerting is not yet enabled.

An alert should answer:

- What failed?
- Why does it matter?
- What should be checked first?
- Which runbook should be followed?

Alerts should be added only after the check, threshold, response procedure, and notification route are understood.

## Security Considerations

- Keep Prometheus, Grafana, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose ports `9090`, `3000`, `9100`, or `9115` publicly.
- Treat metrics and dashboards as operationally sensitive.
- Do not publish screenshots containing exact addresses, usernames, tokens, or private topology.
- Keep the Proxmox management interface internal-only.
- Do not create broad firewall allowances when a narrower trusted-monitoring path is sufficient.
- Introduce Proxmox API credentials only through a documented least-privilege design.
- Keep security-lab workloads isolated from monitoring infrastructure.

## Backup and Recovery

Important monitoring state includes:

- Prometheus configuration.
- Blackbox Exporter configuration.
- Grafana database, data source, and dashboard exports.
- Future alerting and recording rules.
- Historical metrics if retention becomes operationally important.

Project 003 completed the configuration inventory and private dashboard exports. VM backup implementation and restore testing remain pending.

## Troubleshooting Lessons

### Prometheus Job Loss

A syntactically valid Prometheus configuration can still be operationally wrong if a job is removed or malformed.

Required checks:

- Validate with `promtool`.
- Query `count by (job, instance) (up)`.
- Confirm every intended host label remains present.
- Back up configuration before edits.

See [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md).

### Piped Curl Output

When `curl` output is piped to `head`, `curl: (23)` may appear because `head` closes the pipe after receiving the requested lines. The metric output still proves endpoint reachability.

### Proxmox Firewall Reachability

The Proxmox firewall was active during deployment. Testing from `mon01` before changing firewall rules showed that the existing policy already permitted the required connection, avoiding unnecessary exposure.

### Imported Dashboard Variables

Imported dashboards may assume different job names or variables. Refresh or select the `node_exporter` job and verify the intended host before changing panel queries.

## Next Improvements

- Build a custom Linux and hypervisor dashboard.
- Add Proxmox-specific VM, storage, task, and backup metrics through a least-privilege integration.
- Add a local-record DNS probe.
- Evaluate Pi-hole-specific metrics.
- Add actionable alerts only after runbooks and notification routing exist.
- Complete backup implementation and restore testing under Project 003.

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
- [Proxmox VE Platform](../services/proxmox.md)
