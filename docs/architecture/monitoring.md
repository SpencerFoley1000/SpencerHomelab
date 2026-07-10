# Monitoring and Observability

## Purpose

This document describes the monitoring, logging, and alerting strategy for the homelab. Monitoring should help identify failures, explain performance issues, and create operational habits similar to a small production environment.

## Current Status

Monitoring implementation has started under Project 002.

Current deployed components:

| Component | Host | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VE | Active / In Progress | Dedicated monitoring and observability VM |
| Node Exporter | `mon01`, `dns01` | Active | Exposes Linux host metrics over HTTP |
| Blackbox Exporter | `mon01` | Active | Performs DNS/service reachability probes |
| Prometheus | `mon01` | Active | Scrapes, stores, and queries metrics from configured targets |
| Grafana | `mon01` | Active | Visualizes Prometheus metrics through dashboards |

Current Prometheus scrape targets:

| Job | Target | Status | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Up | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | Up | Linux host metrics for `mon01` |
| `node_exporter` | `<DNS01_IP>:9100` | Up | Linux host metrics for `dns01` |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Up | DNS availability probe for `dns01` |

Current Grafana data sources and dashboards:

| Item | Status | Purpose |
| --- | --- | --- |
| Prometheus data source | Active | Allows Grafana to query Prometheus on `localhost:9090` |
| Imported Node Exporter dashboard | Active | Provides initial CPU, memory, disk, and network visibility for `mon01` and `dns01` |
| Homelab Service Health dashboard | Active | Displays DNS availability, probe duration, and probe status for `dns01` |
| Custom Linux host dashboard | Planned | Will be built later for learning value and portfolio polish |

The core monitoring stack is functional and now includes both host-level and service-level monitoring for `dns01`. Node Exporter confirms the host is running; Blackbox Exporter confirms the DNS service answers queries; Grafana displays the DNS probe as a service-health dashboard.

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
| Services | DNS probes, future HTTP checks, process health | Confirms services are usable |
| Backups | Job success, failure, age, restore tests | Backups are only useful if they can be trusted |
| Security events | Authentication failures, unexpected exposure, suspicious logs | Supports future defensive security projects |

## Architecture

The monitoring stack is being built in layers:

```text
Linux hosts
    |
    | expose host metrics
    v
Node Exporter
    |
    | /metrics
    v
Prometheus
    |
    | PromQL and time-series storage
    v
Grafana
```

Service checks add a second path:

```text
Prometheus
    |
    | scrape /probe locally
    v
Blackbox Exporter on mon01
    |
    | DNS probe
    v
dns01:53
```

Current completed layers:

1. Node Exporter exposes `mon01` Linux host metrics on `localhost:9100`.
2. Node Exporter exposes `dns01` Linux host metrics on `<DNS01_IP>:9100`.
3. Blackbox Exporter runs on `mon01` and probes `<DNS01_IP>:53` for DNS availability.
4. Prometheus scrapes `localhost:9090`, `localhost:9100`, `<DNS01_IP>:9100`, and the `blackbox_dns` probe through `localhost:9115`.
5. Prometheus stores collected samples as time-series data.
6. Grafana queries Prometheus on `localhost:9090`.
7. Grafana displays host metrics through an imported Node Exporter dashboard.
8. Grafana displays DNS service health through the Homelab Service Health dashboard.

Next layer:

1. Add Pi-hole-specific metrics or a DNS-focused exporter.
2. Add Proxmox monitoring through an appropriate exporter or API-based approach.
3. Build a custom dashboard that reflects the actual homelab service priorities.
4. Add alerting only after checks are actionable and documented.

This order is intentional:

1. Export metrics first.
2. Collect and store metrics second.
3. Add service probes after host metrics are validated.
4. Visualize metrics after the underlying checks work.
5. Add alerting only after checks are actionable and documented.

This makes troubleshooting easier because each layer can be validated before the next layer depends on it.

## Tooling Direction

Initial selected tools:

| Tool | Role | Notes |
| --- | --- | --- |
| Node Exporter | Host metrics exporter | Installed on `mon01` and `dns01` to expose Linux host metrics. |
| Blackbox Exporter | Service probe exporter | Installed on `mon01`; currently probing DNS availability on `dns01`. |
| Prometheus | Metrics collection and time-series database | Installed on `mon01`; scraping itself, Node Exporter targets, and Blackbox DNS probes. |
| Grafana | Dashboard and visualization platform | Installed on `mon01`; connected to Prometheus and displaying host and DNS service health dashboards. |

Future additions may include:

- Custom dashboards.
- Log collection.
- Alert routing.
- Backup job monitoring.
- Pi-hole-specific metrics.

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

Blackbox Exporter performs external-style probes and exposes the result as metrics such as `probe_success`.

Prometheus repeatedly scrapes configured targets and stores returned metric samples with timestamps. This makes it possible to query both current state and historical trends.

Grafana uses Prometheus as a data source and turns PromQL query results into dashboards.

## PromQL Validation Examples

Useful queries for the current deployment:

```promql
up
```

Shows whether configured scrape targets are currently reachable.

```promql
up{job="node_exporter"}
```

Shows whether monitored Linux hosts are reachable through Node Exporter.

```promql
probe_success{job="blackbox_dns"}
```

Shows whether the DNS probe against `dns01` is succeeding.

```promql
probe_duration_seconds{job="blackbox_dns"}
```

Shows DNS probe duration from the monitoring system's point of view.

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

Current dashboard state:

- An imported Node Exporter dashboard is used for immediate host visibility.
- The imported dashboard can display both `mon01` and `dns01` when using the `node_exporter` job selector.
- The Homelab Service Health dashboard displays DNS availability, DNS probe duration, and DNS probe status over time.
- A custom Linux host dashboard is planned to demonstrate intentional panel design and PromQL understanding.

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
- Blackbox Exporter should not be exposed outside trusted internal networks.
- Prometheus should remain internal because metrics can reveal infrastructure details.
- Grafana should remain internal and protected with non-default credentials.
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

### Blackbox Probe Endpoint Scope

Blackbox Exporter was active, but a test request to the `mon01` LAN IP on port `9115` failed.

Operational takeaway:

- A service can be healthy while only listening locally.
- Because Prometheus and Blackbox Exporter both run on `mon01`, `localhost:9115` is sufficient and preferable.
- Validate the local probe before wiring it into Prometheus.

### Grafana Package Installation

Grafana package installation initially failed because APT could not locate the package from the third-party repository.

Operational takeaway:

- Verify third-party repository files under `/etc/apt/sources.list.d/`.
- Verify signing keys under `/etc/apt/keyrings/`.
- Run `apt-get update` after adding repositories.
- Confirm package availability before retrying installation.

### Grafana Service Validation

Grafana service status showed active, but an initial port check did not clearly show port `3000`.

Operational takeaway:

- Use application-layer validation such as `curl -I localhost:3000`.
- A redirect to `/login` confirms Grafana is responding.

### Grafana Dashboard Variables

The imported Node Exporter dashboard initially showed only `mon01` under one dashboard job selector.

Operational takeaway:

- Imported dashboards may assume different Prometheus job names.
- The current Prometheus job name is `node_exporter`.
- After Prometheus completed a scrape cycle, selecting the `node_exporter` job allowed Grafana to display both `mon01` and `dns01`.

### Service Health Dashboard Design

The DNS service health dashboard was built manually using direct Prometheus queries.

Operational takeaway:

- Manually built panels help confirm understanding of what each metric means.
- Host metrics and service availability should be displayed separately because they answer different operational questions.

## Future Improvements

- Add Pi-hole-specific metrics.
- Build a custom Grafana dashboard for Linux host and DNS service metrics.
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
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
