# ADR-0002: Use Prometheus and Grafana for Homelab Monitoring

## Status

Accepted

## Date

2026-07-09

## Context

The homelab needed a monitoring foundation that could answer practical operational questions without adding excessive complexity.

Requirements:

- Collect Linux host metrics from multiple systems.
- Store metrics over time.
- Query target and resource health.
- Visualize host and service state.
- Distinguish host availability from service availability.
- Separate recursive DNS health from local-record DNS health.
- Remain internal-only and suitable for a resource-constrained homelab.
- Provide learning value relevant to systems administration, networking, and infrastructure roles.

Current monitored systems:

- `mon01`, the dedicated monitoring VM.
- `dns01`, the Pi-hole DNS VM.
- `pve01`, the Proxmox host operating system.

## Decision

Use:

- Node Exporter for Linux host metrics.
- Prometheus for pull-based scraping, target health, time-series storage, and PromQL.
- Grafana for dashboards and visualization.
- Blackbox Exporter for service-level probes.

Run Prometheus, Grafana, and Blackbox Exporter on `mon01`. Install Node Exporter on monitored Linux systems, including the Proxmox host when Linux-level metrics are sufficient.

Use separate Blackbox modules and Prometheus jobs for recursive and local DNS checks.

## Rationale

### Dedicated Monitoring VM

Monitoring runs on `mon01` instead of directly on `dns01` or the hypervisor.

Reasons:

- Separates monitoring, DNS, and virtualization responsibilities.
- Avoids application dependencies directly on the hypervisor.
- Creates a clear shared-infrastructure role.
- Simplifies backup, rebuild, and migration planning.
- Matches common production patterns at small scale.

### Prometheus Pull Model

Prometheus pulls from centrally configured targets.

Reasons:

- Target inventory is controlled from one location.
- Prometheus controls scrape timing.
- Missing targets are visible through `up` and target health.
- New systems can be added incrementally.
- PromQL supports both validation and dashboarding.

### Separate Host and Service Checks

- Node Exporter reports Linux operating-system state.
- Blackbox Exporter tests service behavior from `mon01`.

A host can remain online while DNS is unavailable, so both layers are required.

### Separate Recursive and Local DNS Checks

- Recursive DNS includes Pi-hole, the upstream resolver, and internet dependencies.
- Local DNS validates an internal record without relying on upstream recursion.

Separate jobs make failure domains explicit in PromQL, Grafana, and future alerting.

### Grafana for Visualization

Grafana is used after underlying Prometheus queries are validated.

Reasons:

- Imported dashboards provide quick initial visibility.
- Custom panels answer homelab-specific operational questions.
- Trends are easier to interpret visually than through raw queries alone.
- Manually designed dashboards demonstrate PromQL and operational thinking.

### Linux Baseline Before Proxmox API Monitoring

Node Exporter was selected for the initial `pve01` monitoring phase.

Reasons:

- Immediate CPU, memory, filesystem, disk, network, and uptime visibility.
- Reuses the existing architecture.
- Avoids API credentials before least-privilege requirements are documented.

Boundary:

- Node Exporter cannot provide authoritative VM state, storage-pool health, task results, or backup-job status.

## Alternatives Considered

| Alternative | Reason not chosen |
| --- | --- |
| Install monitoring directly on the Proxmox host | Mixes hypervisor management with application tooling |
| Install monitoring on `dns01` | Combines unrelated DNS and monitoring roles |
| Uptime-only monitoring | Lacks resource, trend, and capacity visibility |
| Single all-in-one commercial platform | Adds unnecessary licensing or operational complexity |
| Centralized logging first | Logs do not replace basic metrics and service checks |
| Push-based custom scripts | More custom maintenance and less standardization |
| Proxmox API exporter as the first host check | Introduces credentials and complexity before a Linux baseline exists |

## Consequences

### Positive

- Centralized host and service visibility.
- Historical resource analysis and capacity planning.
- Clear separation between host, recursive DNS, and local DNS failure domains.
- Gradual expansion to Proxmox platform, backup, HTTP, and security monitoring.
- Practical troubleshooting and documentation experience.
- Summary and detailed dashboards for different operational needs.

### Negative / Tradeoffs

- `mon01` consumes dedicated compute and storage.
- The monitoring stack requires patching, backup, and recovery.
- Prometheus files can be syntactically valid while omitting an intended job.
- YAML indentation errors can map valid-looking fields into the wrong Blackbox schema level.
- Imported dashboards may assume different labels or jobs.
- Metrics and dashboards reveal operational details and require internal-only access.
- A total `mon01` outage is not visible without an external monitor.

## Security Decisions

- Prometheus, Grafana, Node Exporter, and Blackbox Exporter remain internal-only.
- Grafana credentials are changed and stored outside the repository.
- Public documentation uses sanitized placeholders.
- Raw metrics, exact targets, dashboard exports, and sensitive screenshots are not committed.
- Future Proxmox API monitoring must use least-privilege credentials.
- Security-lab systems must not control trusted monitoring infrastructure.

## Validation

The decision has been validated through:

- Node Exporter metrics from `mon01`, `dns01`, and `pve01`.
- Prometheus target health for local and remote scrape targets.
- Recursive DNS probing through `dns01`.
- Local-record DNS probing with answer-record validation.
- PromQL queries returning both DNS series at `1`.
- Imported host dashboards.
- A manually built Homelab Service Health dashboard.
- A manually built Homelab Infrastructure Overview dashboard.
- Recovery from a Prometheus configuration incident.
- Recovery from a Blackbox YAML nesting error using rollback and alternate-port preflight validation.
- Resource tuning of `mon01` based on observed memory usage.

## Follow-Up Work

- [x] Build a custom Linux and hypervisor overview dashboard.
- [x] Add a local-record DNS probe.
- [x] Add Linux host monitoring for `pve01`.
- [ ] Export and privately validate the Homelab Infrastructure Overview.
- [ ] Evaluate Pi-hole-specific application metrics.
- [ ] Select a least-privilege Proxmox platform-monitoring method.
- [ ] Back up Prometheus, Blackbox Exporter, and Grafana state through Project 003.
- [ ] Add alerting only after thresholds and runbooks exist.
- [ ] Reassess external monitoring as the lab becomes more operationally important.

## Related Documentation

- [Monitoring Architecture](../architecture/monitoring.md)
- [Project 002: Monitoring and Observability](../projects/project-002-monitoring-observability.md)
- [Node Exporter](../services/node-exporter.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
