# Project 002: Monitoring and Observability Stack

## Status

Planned / In Progress

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

A dedicated monitoring VM will be deployed:

| Component | Value |
| --- | --- |
| VM Name | `mon01` |
| Operating System | Debian 13 |
| Deployment Model | Dedicated VM on Proxmox VE |
| Primary Role | Monitoring and observability services |
| Network Role | Internal-only monitoring endpoint |
| Public Exposure | None planned |

## Initial Software Stack

| Tool | Role | Reason |
| --- | --- | --- |
| Prometheus | Metrics collection and time-series storage | Pulls metrics from configured targets and stores historical metric samples. |
| Grafana | Visualization and dashboards | Provides human-readable dashboards backed by Prometheus data. |
| Node Exporter | Host metrics exporter | Exposes Linux host metrics such as CPU, memory, disk, network, and uptime. |

## Initial Monitoring Scope

The first milestone will focus on host-level and service-level visibility for core infrastructure.

| Target | Planned Metrics / Checks | Why It Matters |
| --- | --- | --- |
| `mon01` | CPU, memory, disk, network, uptime, service status | The monitoring system must monitor itself so failures are visible. |
| `dns01` | CPU, memory, disk, network, uptime, DNS service health | DNS is foundational; if DNS fails, many other systems appear broken. |
| Proxmox host | CPU, memory, storage, uptime, VM health | Hypervisor health affects every VM in the lab. |
| Pi-hole | DNS availability and future query metrics | Confirms core name resolution remains reliable. |

## Design Decisions

### Dedicated Monitoring VM

Monitoring will run on a separate VM instead of being installed directly on `dns01` or the Proxmox host.

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

Prometheus and Grafana will be deployed together because they solve different problems.

- Prometheus collects and stores metrics.
- Grafana visualizes metrics and helps humans interpret trends.

This separation is common in enterprise environments because collection, storage, querying, visualization, and alerting are separate concerns.

### Exporter-Based Metrics

Node Exporter will be used for Linux host metrics. Exporters translate system or application state into metric endpoints that Prometheus can scrape.

This model allows Prometheus to collect metrics from many different systems using a consistent pull-based approach.

## Security Considerations

- Grafana should not be exposed to the public internet.
- Prometheus should remain internal because metrics can reveal infrastructure details.
- Default credentials must be changed during setup.
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

- Define the purpose and scope of `mon01`.
- Create the Debian VM in Proxmox.
- Assign a static IP or DHCP reservation using sanitized documentation.
- Install baseline packages and enable administrative access.
- Verify network connectivity and DNS resolution.

### Milestone 2: Node Exporter

- Install Node Exporter on `mon01`.
- Validate the metrics endpoint locally.
- Document what host metrics are exposed.
- Add Node Exporter to the service documentation.

### Milestone 3: Prometheus

- Install Prometheus on `mon01`.
- Configure Prometheus to scrape `mon01`.
- Validate metric collection.
- Add future scrape targets for `dns01` and the Proxmox host.

### Milestone 4: Grafana

- Install Grafana on `mon01`.
- Configure Prometheus as a data source.
- Create or import a basic Linux host dashboard.
- Document access, security, and maintenance considerations.

### Milestone 5: Expand Monitoring Coverage

- Add `dns01` host metrics.
- Add DNS availability checks.
- Add Proxmox monitoring approach.
- Plan Pi-hole metric collection.

### Milestone 6: Alerting and Operational Runbooks

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
- [Pi-hole Service](../services/pihole.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
