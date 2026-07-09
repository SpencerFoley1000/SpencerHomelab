# Project 002: Monitoring and Observability Stack

## Status

In Progress

## Current Progress

| Milestone | Status | Notes |
| --- | --- | --- |
| Milestone 1: Design and VM Creation | Complete | `mon01` deployed as a dedicated Debian 13.5 monitoring VM on Proxmox VE. |
| Milestone 2: Node Exporter | Complete | Node Exporter installed on `mon01` and local metrics endpoint validated. |
| Milestone 3: Prometheus | Complete | Prometheus installed on `mon01` and scraping both itself and Node Exporter. |
| Milestone 4: Grafana | Not Started | Grafana will be added next for dashboarding and visualization. |
| Milestone 5: Expand Monitoring Coverage | Not Started | Future scope includes `dns01`, Proxmox, Pi-hole, and service health checks. |
| Milestone 6: Alerting and Operational Runbooks | Not Started | Alerting will be added only after useful checks and runbooks exist. |

## Purpose

Project 002 introduces a dedicated monitoring and observability stack for the homelab. The goal is not simply to deploy popular tools, but to understand why monitoring exists, what operational problems it solves, and how monitoring patterns resemble real enterprise infrastructure.

This project builds on Project 001, where `dns01` was deployed as the first core infrastructure VM and Pi-hole became the DNS service for the homelab.

## Learning Goals

- Understand why monitoring exists in production environments.
- Learn the difference between metrics, logs, dashboards, and alerts.
- Understand why Prometheus and Grafana are commonly paired.
- Learn how exporters expose host and service metrics.
- Understand how time-series data differs from relational data.
- Practice Linux service installation, validation, and troubleshooting.
- Build operational habits around documentation, validation, and change tracking.

## Target Design

A dedicated monitoring VM has been deployed:

| Component | Value |
| --- | --- |
| VM Name | `mon01` |
| Operating System | Debian 13.5 |
| Deployment Model | Dedicated VM on Proxmox VE |
| Primary Role | Monitoring and observability services |
| Network Role | Internal-only monitoring endpoint |
| Public Exposure | None planned |
| Initial Resource Allocation | 2 vCPU, 2 GB RAM, 32 GB disk |

## Initial Software Stack

| Tool | Role | Status | Reason |
| --- | --- | --- | --- |
| Node Exporter | Host metrics exporter | Installed on `mon01` | Exposes Linux host metrics such as CPU, memory, disk, network, and uptime. |
| Prometheus | Metrics collection and time-series storage | Installed on `mon01` | Scrapes metrics from configured targets and stores historical metric samples. |
| Grafana | Visualization and dashboards | Planned | Provides human-readable dashboards backed by Prometheus data. |

## Initial Monitoring Scope

The first phase focuses on host-level and service-level visibility for core infrastructure.

| Target | Current / Planned Metrics and Checks | Why It Matters |
| --- | --- | --- |
| `mon01` | Current: Prometheus self-monitoring and Node Exporter host metrics. Planned: Grafana dashboarding. | The monitoring system must monitor itself so failures are visible. |
| `dns01` | Planned: CPU, memory, disk, network, uptime, DNS service health | DNS is foundational; if DNS fails, many other systems appear broken. |
| Proxmox host | Planned: CPU, memory, storage, uptime, VM health | Hypervisor health affects every VM in the lab. |
| Pi-hole | Planned: DNS availability and future query metrics | Confirms core name resolution remains reliable. |

## Design Decisions

### Dedicated Monitoring VM

Monitoring runs on a separate VM instead of being installed directly on `dns01` or the Proxmox host.

**Reasons:**

- Keeps DNS and monitoring roles separated.
- Avoids making the first infrastructure VM responsible for unrelated services.
- Matches enterprise patterns where monitoring is treated as shared infrastructure.
- Makes future backup, restore, and migration testing cleaner.

**Tradeoffs:**

- Consumes additional CPU, memory, and storage.
- Adds another system that must be patched, backed up, and monitored.
- Requires clear documentation so the lab does not become a collection of disconnected services.

### Prometheus and Grafana Pairing

Prometheus and Grafana are paired because they solve different problems.

- Prometheus collects, stores, and queries metrics.
- Grafana visualizes metrics and helps humans interpret trends.

This separation is common in enterprise environments because collection, storage, querying, visualization, and alerting are separate concerns.

### Exporter-Based Metrics

Node Exporter is the first deployed monitoring component. Exporters translate system or application state into metric endpoints that Prometheus can scrape.

This model allows Prometheus to collect metrics from many different systems using a consistent pull-based approach.

### Pull-Based Metrics Collection

Prometheus is configured to pull metrics from known targets instead of requiring each monitored host to push data somewhere.

**Reasons:**

- Scrape targets are centrally configured.
- Prometheus controls scrape intervals.
- Target health is visible from the Prometheus web UI.
- Missing or unreachable targets become observable failures.
- The model scales cleanly as additional homelab systems are added.

## Implementation Notes

### `mon01` Baseline

`mon01` was installed as a minimal Debian 13.5 server with no desktop environment.

Completed baseline items:

- Installed Debian as a headless server.
- Configured non-root administration with `sudo`.
- Installed baseline administrative tools.
- Installed and validated QEMU Guest Agent.
- Verified basic network and package repository functionality.
- Installed Node Exporter using the Debian package repository.
- Validated Node Exporter locally with `curl localhost:9100/metrics`.
- Installed Prometheus using the Debian package repository.
- Configured Prometheus to scrape `localhost:9100` for Node Exporter metrics.
- Validated Prometheus target health in the web UI.

### Node Exporter Validation

Node Exporter exposes host metrics over HTTP on port `9100`.

Validated locally from `mon01`:

```bash
curl localhost:9100/metrics
```

The endpoint returned Prometheus-formatted metrics, confirming that Linux host metrics are available for Prometheus scraping.

### Prometheus Validation

Prometheus runs on port `9090` and is currently configured with two scrape targets:

| Job | Target | Status |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Up |
| `node_exporter` | `localhost:9100` | Up |

Validation completed:

- Prometheus service started successfully.
- Prometheus web UI loaded from the internal homelab network.
- Target health page showed both configured targets as `UP`.
- Initial PromQL queries returned data.

Useful validation queries:

```promql
up
```

```promql
node_memory_MemAvailable_bytes
```

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

## Troubleshooting Notes

### QEMU Guest Agent Device Missing

During `mon01` setup, the QEMU Guest Agent package was installed, but the service remained inactive because the expected virtio serial device was missing.

**Symptoms:**

- `qemu-guest-agent` was installed but inactive.
- Starting the service failed due to a dependency job.
- `/dev/virtio-ports/` did not exist inside the VM.
- Proxmox showed QEMU Guest Agent as enabled.
- `qm config` showed `agent: 1`.

**Root Cause:**

The Proxmox VM configuration had the guest agent enabled, but the running VM process had not recreated the virtual hardware channel required by the guest agent.

**Resolution:**

- Shut down `mon01` completely from Proxmox.
- Waited until the VM showed as stopped.
- Started the VM again from Proxmox.
- Verified `/dev/virtio-ports/org.qemu.guest_agent.0` existed.
- Verified `qemu-guest-agent` returned `active`.

**Lesson Learned:**

A guest reboot restarts the operating system, but a full Proxmox stop/start recreates the virtual hardware presented to the VM. When virtual devices are missing, troubleshoot both the guest OS and the hypervisor layer.

### Prometheus Target Initially Unknown

After adding the Node Exporter target, Prometheus briefly showed the target state as `UNKNOWN`.

**Resolution:**

Waited for Prometheus to complete the next scrape cycle. The target changed to `UP` after the first successful scrape.

**Lesson Learned:**

Prometheus target health may not update instantly after a configuration reload or restart. `UNKNOWN` can mean the target exists in configuration but has not completed a scrape yet.

## Security Considerations

- Grafana should not be exposed to the public internet.
- Prometheus should remain internal because metrics can reveal infrastructure details.
- Node Exporter should only be reachable from trusted internal monitoring systems.
- Default Grafana credentials must be changed during setup.
- Dashboards and screenshots must not publish sensitive hostnames, IP addresses, usernames, tokens, or private topology details.
- Monitoring credentials and API keys must not be committed to the repository.
- Firewall exposure should be limited to required internal systems only.

## Enterprise Considerations

This project mirrors enterprise infrastructure patterns at small scale:

- Dedicated monitoring infrastructure.
- Centralized metrics collection.
- Historical performance data.
- Dashboards for troubleshooting and capacity planning.
- Future alerting tied to actionable operational runbooks.
- Documentation that explains design choices, not just commands.

## Milestones

### Milestone 1: Design and VM Creation

Status: Complete

- Defined the purpose and scope of `mon01`.
- Created the Debian VM in Proxmox.
- Assigned static addressing using sanitized documentation.
- Installed baseline packages and enabled administrative access.
- Verified network connectivity and DNS resolution.
- Validated QEMU Guest Agent.

### Milestone 2: Node Exporter

Status: Complete

- Installed Node Exporter on `mon01`.
- Validated the metrics endpoint locally.
- Confirmed host metrics are exposed in Prometheus text format.
- Added Node Exporter service documentation.

### Milestone 3: Prometheus

Status: Complete

- Installed Prometheus on `mon01`.
- Configured Prometheus to scrape `mon01` Node Exporter.
- Validated Prometheus service health.
- Confirmed Prometheus target health showed both `localhost:9090` and `localhost:9100` as `UP`.
- Confirmed initial PromQL queries returned data.
- Added Prometheus service documentation.

### Milestone 4: Grafana

Status: Not Started

- Install Grafana on `mon01`.
- Configure Prometheus as a data source.
- Create or import a basic Linux host dashboard.
- Document access, security, and maintenance considerations.

### Milestone 5: Expand Monitoring Coverage

Status: Not Started

- Add `dns01` host metrics.
- Add DNS availability checks.
- Add Proxmox monitoring approach.
- Plan Pi-hole metric collection.

### Milestone 6: Alerting and Operational Runbooks

Status: Not Started

- Define actionable alerts.
- Avoid noisy alerts.
- Add runbooks for common failures.
- Document alert routing only after the mechanism is selected.

## Validation Plan

Each milestone should include validation before being considered complete:

- Confirm services are enabled and running.
- Confirm listening ports are expected.
- Confirm metrics endpoints respond locally before remote scraping.
- Confirm Prometheus targets show as healthy.
- Confirm Grafana dashboards display real data.
- Confirm documentation is updated with sanitized values.

## Documentation Updates Required

As this project progresses, update the following documentation:

- `docs/projects/project-002-monitoring-observability.md`
- `docs/architecture/monitoring.md`
- `docs/services/` service pages for Prometheus, Grafana, and Node Exporter
- `docs/architecture/vm-inventory.md`
- `docs/runbooks/` for monitoring troubleshooting procedures
- `docs/decisions/` if a major architecture decision is made
- `CHANGELOG.md` after meaningful milestones

## Future Improvements

- Grafana dashboards for Linux host metrics.
- Pi-hole exporter or DNS-specific metrics.
- Proxmox exporter or API-based monitoring.
- Alertmanager.
- Email or chat-based notifications.
- Blackbox probing for DNS, HTTP, and ICMP checks.
- Capacity planning dashboards.
- Backup and restore monitoring after Project 003.
- Security monitoring integration with future Wazuh, Suricata, and Zeek projects.

## Related Documentation

- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Pi-hole Service](../services/pihole.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
