# Monitoring and Observability

## Purpose

This document describes the monitoring, logging, and alerting strategy for the homelab. Monitoring should help identify failures, explain performance issues, and create operational habits similar to a small production environment.

## Current Status

Monitoring implementation has started under Project 002.

Current deployed components:

| Component | Host | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VE | Active / In Progress | Dedicated monitoring and observability VM |
| Node Exporter | `mon01` | Active | Exposes Linux host metrics over HTTP |
| Prometheus | `mon01` | Active | Scrapes, stores, and queries metrics from configured targets |

Current Prometheus scrape targets:

| Job | Target | Status | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Up | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | Up | Linux host metrics for `mon01` |

Grafana is planned next. The monitoring stack is being built from the bottom up so each layer is validated before the next layer depends on it.

Monitoring should start small and answer practical questions:

- Is the infrastructure reachable?
- Are important services running?
- Are hosts running out of CPU, memory, disk, or network capacity?
- Did backups run successfully?
- Are there security-relevant events worth investigating?

## Design Goals

- Detect service failures and host issues early.
- Track resource usage trends for capacity planning.
- Practice operational monitoring concepts used in professional environments.
- Keep monitoring useful without overcomplicating the initial build.
- Document alerts so future troubleshooting is faster.

## Monitoring Scope

| Area | What to Monitor | Why It Matters |
| --- | --- | --- |
| Network | Gateway reachability, switch availability, DNS/DHCP health | Connectivity issues affect every service |
| Proxmox host | CPU, memory, disk, uptime, updates, VM state | Hypervisor health affects all workloads |
| Storage | Disk usage, storage pool health, backup target availability | Storage failures can cause data loss |
| Services | Uptime, ports, HTTP checks, process health | Confirms services are usable |
| Backups | Job success, failure, age, restore tests | Backups are only useful if they can be trusted |
| Security events | Authentication failures, unexpected exposure, suspicious logs | Supports future defensive security projects |

## Initial Architecture

The monitoring stack is being built in layers:

```text
Linux hosts
    |
    | expose metrics
    v
Node Exporter
    |
    | HTTP /metrics endpoint
    v
Prometheus
    |
    | query and time-series storage
    v
Grafana
```

Current completed layers:

1. Node Exporter exposes `mon01` Linux host metrics on `localhost:9100`.
2. Prometheus scrapes `localhost:9090` and `localhost:9100`.
3. Prometheus stores collected samples as time-series data.

Next layer:

1. Grafana will connect to Prometheus as a data source.
2. Grafana will display host metrics through dashboards.

This order is intentional:

1. Export metrics first.
2. Collect and store metrics second.
3. Visualize metrics last.

This makes troubleshooting easier because each layer can be validated before the next layer depends on it.

## Tooling Direction

Initial selected tools:

| Tool | Role | Notes |
| --- | --- | --- |
| Node Exporter | Host metrics exporter | Installed first to expose Linux metrics from `mon01`. |
| Prometheus | Metrics collection and time-series database | Installed on `mon01`; currently scraping itself and Node Exporter. |
| Grafana | Dashboard and visualization platform | Planned next after Prometheus target health has been validated. |

Future additions may include:

- Service uptime checks.
- Centralized dashboards.
- Log collection.
- Alert routing.
- Backup job monitoring.
- DNS-specific and Pi-hole-specific metrics.

Tool choices should be documented in service pages and architecture decision records once selected.

## Metrics Model

A metric is a numerical measurement of system or application state at a point in time.

Examples:

- CPU time.
- Available memory.
- Filesystem size and free space.
- Network bytes received and transmitted.
- Uptime.
- Service health.

Node Exporter reads Linux kernel and operating system data from sources such as `/proc` and `/sys`, then exposes that data in a Prometheus-compatible text format at `/metrics`.

Prometheus repeatedly scrapes configured targets and stores returned metric samples with timestamps. This makes it possible to query both current state and historical trends.

## PromQL Validation Examples

Useful queries for the current deployment:

```promql
up
```

Shows whether configured scrape targets are currently reachable.

```promql
node_memory_MemAvailable_bytes
```

Shows available memory reported by Node Exporter.

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

Shows available disk space for the root filesystem.

## Alerting Philosophy

Alerts should be actionable. An alert should usually answer:

- What failed?
- Why does it matter?
- What should be checked first?
- Is there a runbook?

Avoid creating alerts that are noisy, unclear, or ignored. A small number of useful alerts is better than a large number of low-value alerts.

Alerting will not be enabled until the underlying checks are understood and documented.

## Dashboard Philosophy

Dashboards should support troubleshooting and capacity planning. Good dashboards should show:

- Current host health.
- Service availability.
- Storage usage.
- Network status.
- Backup status.
- Recent security-relevant events where appropriate.

Dashboards should avoid exposing sensitive values in screenshots or public documentation.

## Logging Strategy

Centralized logging is a future improvement. When implemented, documentation should include:

- Which systems send logs.
- Where logs are stored.
- Retention period.
- Access controls.
- Security-relevant event sources.
- Privacy and sanitization considerations.

Logs may contain sensitive information and should not be committed to the repository.

## Security Considerations

- Monitoring tools often have broad visibility and should be protected.
- Node Exporter should not be exposed outside trusted internal networks.
- Prometheus should remain internal because metrics can reveal infrastructure details.
- Dashboards should not be exposed publicly without strong authentication.
- Alert destinations should not leak sensitive infrastructure details.
- Logs should be treated as potentially sensitive.
- Security lab systems should be monitored without allowing them to control trusted infrastructure.

## Troubleshooting Lessons

### QEMU Guest Agent Virtual Device

During `mon01` setup, QEMU Guest Agent was enabled in Proxmox and installed inside Debian, but the service initially could not start because `/dev/virtio-ports/org.qemu.guest_agent.0` was missing.

A full Proxmox stop/start recreated the VM hardware and exposed the virtio serial device. A guest-only reboot was not enough.

Operational takeaway:

- If a service depends on virtual hardware, check both the guest OS and the hypervisor configuration.
- If virtual hardware is missing after a configuration change, perform a full power cycle from the hypervisor.

### Prometheus Target State

After adding a new scrape target, Prometheus may briefly show the target as `UNKNOWN` until it completes a scrape cycle.

Operational takeaway:

- Wait for at least one scrape interval before assuming a newly added target is broken.
- If the target remains unhealthy, check target health details in the Prometheus web UI.
- Validate local access to the exporter before troubleshooting Prometheus itself.

## Future Improvements

- Install Grafana and configure Prometheus as a data source.
- Add host and service dashboards.
- Add `dns01` host metrics.
- Add DNS availability checks.
- Add backup job monitoring.
- Add alert routing for critical failures.
- Add security detection experiments after segmentation is in place.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
- [VM Inventory](vm-inventory.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
