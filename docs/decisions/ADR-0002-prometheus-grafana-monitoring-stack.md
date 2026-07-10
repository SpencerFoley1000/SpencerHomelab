# ADR-0002: Use Prometheus and Grafana for Homelab Monitoring

## Status

Accepted

## Date

2026-07-09

## Context

The homelab needed a monitoring foundation that could answer practical operational questions without introducing excessive complexity.

The initial requirements were:

- Collect Linux host metrics from multiple VMs.
- Store metrics over time.
- Query target and resource health.
- Visualize host and service state.
- Distinguish host availability from application availability.
- Remain internal-only and suitable for a resource-constrained 16 GB Proxmox host.
- Provide learning value relevant to systems administration, networking, and infrastructure roles.

The first monitored systems are:

- `mon01`, the dedicated monitoring VM.
- `dns01`, the Pi-hole DNS VM.

## Decision

Use the following monitoring stack:

- Node Exporter for Linux host metrics.
- Prometheus for pull-based scraping, time-series storage, target health, and PromQL.
- Grafana for dashboards and visualization.
- Blackbox Exporter for service-level probes.

Run Prometheus, Grafana, and Blackbox Exporter on the dedicated `mon01` VM. Install Node Exporter on monitored Debian VMs.

## Rationale

### Dedicated Monitoring VM

Monitoring runs on `mon01` instead of directly on the Proxmox host or `dns01`.

Reasons:

- Separates monitoring from DNS responsibilities.
- Avoids adding application dependencies directly to the hypervisor.
- Creates a clear shared-infrastructure role.
- Makes monitoring backup, rebuild, and migration planning easier.
- Provides a realistic operational pattern without requiring multiple physical servers.

### Prometheus Pull Model

Prometheus pulls metrics from centrally configured targets.

Reasons:

- Target inventory is managed from one location.
- Prometheus controls scrape timing.
- Missing targets become observable through the `up` metric and target-health interface.
- New monitored systems can be added incrementally.
- PromQL provides both direct validation and dashboard data.

### Separate Host and Service Checks

Node Exporter and Blackbox Exporter are used for different failure domains.

- Node Exporter reports host operating-system metrics.
- Blackbox Exporter tests whether a service responds from the monitoring system's point of view.

This distinction matters because a VM can remain online while DNS or another application is unavailable.

### Grafana for Visualization

Grafana is used after the underlying Prometheus queries are validated.

Reasons:

- Supports imported dashboards for quick initial visibility.
- Supports custom panels for homelab-specific operational questions.
- Makes trends and service state easier to interpret than raw query results alone.
- Provides portfolio value when dashboards are intentionally designed and documented.

## Alternatives Considered

| Alternative | Reason Not Chosen |
| --- | --- |
| Install monitoring directly on the Proxmox host | Increases hypervisor complexity and mixes management-plane responsibilities with application tooling |
| Install monitoring on `dns01` | Combines unrelated DNS and monitoring roles and creates a larger shared failure domain |
| Uptime-only monitoring | Does not provide capacity, trend, or host-resource information |
| Single all-in-one commercial platform | Adds unnecessary licensing, resource, or operational complexity for the current scale |
| Centralized logging first | Logs are useful but do not replace basic host metrics, target health, and service probes |
| Push-based custom scripts | Requires more custom maintenance and provides less standardized tooling than Prometheus exporters |

## Consequences

### Positive

- Provides centralized host and service visibility.
- Supports historical resource analysis and capacity planning.
- Separates monitoring roles from DNS and the hypervisor.
- Uses widely adopted infrastructure concepts and tools.
- Makes target failures visible through standard metrics.
- Supports gradual expansion to Proxmox, backup, HTTP, and security monitoring.
- Produces practical troubleshooting and documentation experience.

### Negative / Tradeoffs

- `mon01` consumes dedicated CPU, memory, and storage.
- The monitoring stack becomes another system that requires updates, backup, and recovery.
- Prometheus configuration errors can remove existing scrape jobs while remaining syntactically valid.
- Imported Grafana dashboards may assume different labels or job names.
- Metrics and dashboards reveal operational details and require internal-only access.
- The monitoring system cannot observe an outage if `mon01` itself is completely unavailable unless an external monitor is added later.

## Security Decisions

- Prometheus, Grafana, Node Exporter, and Blackbox Exporter remain internal-only.
- Grafana default credentials are changed and stored outside the repository.
- Public documentation uses sanitized placeholders for addresses.
- Raw metrics and sensitive dashboard screenshots are not committed.
- Future Proxmox API monitoring must use least-privilege credentials.
- Security-lab systems must not be allowed to control trusted monitoring infrastructure.

## Validation

The decision has been validated through:

- Successful Node Exporter metrics from `mon01` and `dns01`.
- Prometheus target health for local and remote scrape targets.
- PromQL queries returning host and probe data.
- Grafana visualization for both monitored Linux hosts.
- Blackbox Exporter recursive DNS probing through `dns01`.
- A manually built service-health dashboard.
- Recovery from a Prometheus configuration incident using layered troubleshooting.
- Resource tuning of `mon01` from 2 GB to 3 GB RAM based on observed usage.

## Follow-Up Work

- [ ] Build a custom Linux host dashboard.
- [ ] Add a local-record DNS probe.
- [ ] Evaluate Pi-hole-specific metrics.
- [ ] Select a least-privilege Proxmox monitoring method.
- [ ] Export stable Grafana dashboards.
- [ ] Back up Prometheus, Blackbox Exporter, and Grafana configuration.
- [ ] Add alerting only after thresholds and runbooks exist.
- [ ] Reassess whether external monitoring is justified as the lab becomes more important.

## Related Documentation

- [Monitoring Architecture](../architecture/monitoring.md)
- [Project 002: Monitoring and Observability](../projects/project-002-monitoring-observability.md)
- [Node Exporter](../services/node-exporter.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
