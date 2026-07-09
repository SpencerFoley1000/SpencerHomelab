# Monitoring and Observability

## Purpose

This document describes the monitoring, logging, and alerting strategy for the homelab. Monitoring should help identify failures, explain performance issues, and create operational habits similar to a small production environment.

## Current Status

Monitoring implementation has started under Project 002.

Current deployed components:

| Component | Host | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VE | Active / In Progress | Dedicated monitoring and observability VM |
| Node Exporter | `mon01` | Active | Exposes Linux host metrics over HTTP for future Prometheus scraping |

Prometheus and Grafana are planned next. The current focus is building the stack from the bottom up by first validating that host metrics are being exposed correctly.

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
| Prometheus | Metrics collection and time-series database | Planned next; will scrape Node Exporter endpoints. |
| Grafana | Dashboard and visualization platform | Planned after Prometheus is collecting real data. |

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

## Future Improvements

- Install and configure Prometheus on `mon01`.
- Configure Prometheus to scrape `mon01` Node Exporter.
- Create a monitoring service page for Prometheus.
- Add Grafana after Prometheus is collecting data.
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
- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
