# Project 002: Monitoring and Observability Stack

## Status

In Progress

## Current Progress

| Milestone | Status | Notes |
| --- | --- | --- |
| Milestone 1: Design and VM Creation | Complete | `mon01` deployed as a dedicated Debian 13.5 monitoring VM on Proxmox VE. |
| Milestone 2: Node Exporter | Complete | Node Exporter installed on `mon01` and local metrics endpoint validated. |
| Milestone 3: Prometheus | Complete | Prometheus installed on `mon01` and scraping itself plus Node Exporter. |
| Milestone 4: Grafana | Complete | Grafana installed on `mon01`, connected to Prometheus, and displaying imported and custom dashboards. |
| Milestone 5: Expand Monitoring Coverage | In Progress | `dns01` host metrics, DNS availability probes, and DNS service-health dashboard panels are active. Pi-hole metrics and Proxmox monitoring remain future work. |
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

## Monitoring VM

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
| Current Resource Allocation | 2 vCPU, 3 GB RAM, 32 GB disk |

## Current Software Stack

| Tool | Role | Status | Reason |
| --- | --- | --- | --- |
| Node Exporter | Host metrics exporter | Installed on `mon01` and `dns01` | Exposes Linux host metrics such as CPU, memory, disk, network, and uptime. |
| Blackbox Exporter | Service probe exporter | Installed on `mon01` | Probes whether `dns01` answers DNS queries. |
| Prometheus | Metrics collection and time-series storage | Installed on `mon01` | Scrapes metrics from configured targets and stores historical metric samples. |
| Grafana | Visualization and dashboards | Installed on `mon01` | Provides host and service-health dashboards backed by Prometheus data. |

## Current Monitoring Scope

| Target | Current / Planned Metrics and Checks | Why It Matters |
| --- | --- | --- |
| `mon01` | Current: Prometheus self-monitoring, Node Exporter host metrics, Grafana dashboarding, Blackbox Exporter service. | The monitoring system must monitor itself so failures are visible. |
| `dns01` | Current: Node Exporter host metrics, DNS availability probe, and Grafana service-health dashboard panels. Planned: Pi-hole-specific metrics. | DNS is foundational; if DNS fails, many other systems appear broken. |
| Proxmox host | Planned: CPU, memory, storage, uptime, VM health | Hypervisor health affects every VM in the lab. |
| Pi-hole | Current: DNS availability through Blackbox Exporter. Planned: query metrics. | Confirms core name resolution remains reliable. |

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

### Monitoring VM Memory Increase

`mon01` was increased from 2 GB RAM to 3 GB RAM after Grafana showed sustained memory usage near the original allocation.

**Reasons:**

- Prometheus and Grafana are the core monitoring services and should have enough headroom to remain stable.
- Prometheus memory usage can grow as scrape targets, metrics, retention, and dashboards increase.
- Grafana dashboards can create short-term memory pressure during query and panel rendering.
- 3 GB provides additional breathing room without overcommitting the 16 GB Proxmox host.

### Host Metrics Before Service Probes

Node Exporter was deployed first because it exposes host metrics in a format Prometheus can scrape.

Blackbox Exporter was added after host metrics were working because service availability is a different layer of monitoring. A host can be powered on while a service is broken, so `dns01` needs both host metrics and DNS query probes.

### Pull-Based Metrics Collection

Prometheus is configured to pull metrics from known targets instead of requiring each monitored host to push data somewhere.

**Reasons:**

- Scrape targets are centrally configured.
- Prometheus controls scrape intervals.
- Target health is visible from the Prometheus web UI.
- Missing or unreachable targets become observable failures.
- The model scales cleanly as additional homelab systems are added.

### Use Static IP for `dns01` Monitoring Targets

`dns01` is monitored by IP address instead of depending on its own DNS name.

**Reason:**

If DNS fails, monitoring should still be able to check whether the DNS host and DNS service are reachable. Using the static address avoids making the DNS server's monitoring path depend on DNS itself.

The exact address is not published. Public documentation uses `<DNS01_IP>`.

### Imported Dashboard First, Manual Panels Later

An imported Node Exporter dashboard was used first to validate host metrics quickly. A custom service-health dashboard was then created manually for DNS probe status.

**Reasons:**

- Imported dashboards are useful for immediate validation.
- Manually built panels demonstrate understanding of the PromQL queries behind the visualization.
- Separating host health from service health makes dashboards easier to interpret.

## Implementation Notes

### `mon01` Baseline

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
- Installed Grafana using the Grafana APT repository.
- Configured Grafana to use Prometheus as a data source.
- Imported a Node Exporter dashboard to validate end-to-end visualization.
- Increased VM memory from 2 GB to 3 GB after monitoring showed limited headroom.
- Installed Blackbox Exporter using the Debian package repository.

### `dns01` Remote Host Monitoring

`dns01` was added as the first remote scrape target after the local `mon01` monitoring path was working.

Completed items:

- Installed Node Exporter on `dns01`.
- Validated `dns01` metrics locally with `curl localhost:9100/metrics`.
- Validated remote reachability from `mon01` to `http://<DNS01_IP>:9100/metrics`.
- Added `<DNS01_IP>:9100` to the `node_exporter` scrape job in Prometheus.
- Labeled the target as `host: dns01` and `role: dns`.
- Validated Prometheus target health as `UP`.
- Confirmed Grafana can display both `mon01` and `dns01` under the `node_exporter` job.

### `dns01` DNS Availability Monitoring

Blackbox Exporter was added on `mon01` to monitor whether `dns01` is actually answering DNS queries.

Completed items:

- Installed `prometheus-blackbox-exporter` on `mon01`.
- Added a `dns_udp` module in `/etc/prometheus/blackbox.yml`.
- Validated Blackbox Exporter locally on `localhost:9115`.
- Manually validated the DNS probe against `<DNS01_IP>:53`.
- Confirmed `probe_success 1` from the manual probe.
- Added a `blackbox_dns` scrape job to Prometheus.
- Validated Prometheus configuration with `promtool check config`.
- Restarted Prometheus successfully.
- Confirmed `probe_success{job="blackbox_dns"}` returns `1`.

Current probe flow:

```text
Prometheus -> Blackbox Exporter on localhost:9115 -> dns01:53
```

### Grafana Service Health Dashboard

A `Homelab Service Health` dashboard was created to visualize service-level DNS monitoring.

Current panels:

| Panel | Query | Purpose |
| --- | --- | --- |
| `dns01 DNS Availability` | `probe_success{job="blackbox_dns", host="dns01"}` | Shows whether DNS probing is currently succeeding. |
| `dns01 DNS Probe Duration` | `probe_duration_seconds{job="blackbox_dns", host="dns01"}` | Shows DNS probe response time over time. |
| `dns01 DNS Probe Status` | `probe_success{job="blackbox_dns", host="dns01"}` | Shows DNS probe status over time. |

This dashboard separates service availability from host health. `dns01` can be online while DNS itself is broken, so both views are useful.

## Validation

### Node Exporter Validation

Node Exporter exposes host metrics over HTTP on port `9100`.

Validated locally on monitored hosts:

```bash
curl localhost:9100/metrics
```

For remote targets, validate from `mon01` before changing Prometheus:

```bash
curl http://<DNS01_IP>:9100/metrics
```

### Blackbox Exporter Validation

Blackbox Exporter exposes probe metrics over HTTP on port `9115`.

Validated locally from `mon01`:

```bash
curl localhost:9115/metrics
```

Manual DNS probe:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

Successful result:

```text
probe_success 1
```

### Prometheus Validation

Prometheus runs on port `9090` and is currently configured with these scrape targets:

| Job | Target | Status |
| --- | --- | --- |
| `prometheus` | `localhost:9090` | Up |
| `node_exporter` | `localhost:9100` | Up |
| `node_exporter` | `<DNS01_IP>:9100` | Up |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | Up |

Useful validation queries:

```promql
up
```

```promql
up{job="node_exporter"}
```

```promql
probe_success{job="blackbox_dns"}
```

```promql
probe_duration_seconds{job="blackbox_dns"}
```

```promql
node_memory_MemAvailable_bytes
```

```promql
node_filesystem_avail_bytes{mountpoint="/"}
```

### Grafana Validation

Grafana runs on port `3000` and is connected to Prometheus as its first data source.

Validation completed:

- `grafana-server` service started successfully.
- Local HTTP check returned a redirect to `/login`.
- Grafana web UI loaded from the internal homelab network.
- Default credentials were changed during initial login.
- Prometheus data source test succeeded.
- Imported Node Exporter dashboard displayed metrics from Prometheus.
- After selecting the `node_exporter` job and waiting for Prometheus to scrape, Grafana displayed both `mon01` and `dns01`.
- `Homelab Service Health` dashboard displays DNS availability, probe duration, and DNS probe status for `dns01`.

## Troubleshooting Notes

### QEMU Guest Agent Device Missing

During `mon01` setup, the QEMU Guest Agent package was installed, but the service remained inactive because the expected virtio serial device was missing.

**Resolution:**

- Shut down `mon01` completely from Proxmox.
- Waited until the VM showed as stopped.
- Started the VM again from Proxmox.
- Verified `/dev/virtio-ports/org.qemu.guest_agent.0` existed.
- Verified `qemu-guest-agent` returned `active`.

**Lesson Learned:**

A guest reboot restarts the operating system, but a full Proxmox stop/start recreates the virtual hardware presented to the VM. When virtual devices are missing, troubleshoot both the guest OS and the hypervisor layer.

### Prometheus Target Initially Unknown

After adding a new scrape target, Prometheus may briefly show the target state as `UNKNOWN`.

**Lesson Learned:**

Prometheus target health may not update instantly after a configuration reload or restart. `UNKNOWN` can mean the target exists in configuration but has not completed a scrape yet.

### Blackbox Exporter Probe Endpoint Scope

Blackbox Exporter was active, but a test request to the `mon01` LAN IP on port `9115` failed.

**Lesson Learned:**

A service can be healthy while only listening locally. Local-only access is acceptable and safer when Prometheus and the exporter run on the same host.

### Grafana Package Not Found

During Grafana setup, `apt-get install grafana` initially failed because APT could not locate the package.

**Lesson Learned:**

When a package from a third-party repository cannot be located, verify the repository file, signing key, architecture, and `apt-get update` output before retrying the install.

### Imported Dashboard Job Selector

The imported dashboard initially showed only `mon01` under one dashboard job selector.

**Lesson Learned:**

Imported dashboards may assume different Prometheus job names. Dashboard variables may need to be refreshed, adjusted, or replaced with custom panels once the lab's monitoring design is better understood.

### Manual Service Health Panels

The service health dashboard was built manually using direct Prometheus queries.

**Lesson Learned:**

Manual panels make the relationship between the metric, query, and operational question clearer than relying only on imported dashboards.

## Security Considerations

- Grafana should not be exposed to the public internet.
- Prometheus should remain internal because metrics can reveal infrastructure details.
- Node Exporter should only be reachable from trusted internal monitoring systems.
- Blackbox Exporter should remain internal and only perform intentional probes.
- Default Grafana credentials must be changed during setup.
- Grafana credentials must be stored in a password manager and never committed to the repository.
- Dashboards and screenshots must not publish sensitive hostnames, IP addresses, usernames, tokens, or private topology details.
- Monitoring credentials and API keys must not be committed to the repository.
- Firewall exposure should be limited to required internal systems only.
- Exact internal IP addresses should be replaced with placeholders such as `<DNS01_IP>` and `<MON01_IP>` in public documentation.

## Enterprise Considerations

This project mirrors enterprise infrastructure patterns at small scale:

- Dedicated monitoring infrastructure.
- Centralized metrics collection.
- Historical performance data.
- Dashboards for troubleshooting and capacity planning.
- Host labeling by function and role.
- Service-level probing in addition to host-level metrics.
- Manual dashboard panels that map metrics to operational questions.
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

Status: Complete

- Installed Grafana on `mon01`.
- Configured Prometheus as a data source.
- Imported a Node Exporter dashboard.
- Created the `Homelab Service Health` dashboard.
- Validated that Grafana displays host metrics and DNS probe status.
- Added Grafana service documentation.

### Milestone 5: Expand Monitoring Coverage

Status: In Progress

- Installed Node Exporter on `dns01`.
- Validated `dns01` metrics locally.
- Validated remote scrape reachability from `mon01`.
- Configured Prometheus to scrape `<DNS01_IP>:9100`.
- Confirmed `dns01` target health as `UP`.
- Confirmed Grafana can display both `mon01` and `dns01` under the `node_exporter` job.
- Installed Blackbox Exporter on `mon01`.
- Added DNS availability probing for `<DNS01_IP>:53`.
- Confirmed `probe_success{job="blackbox_dns"}` returns `1`.
- Added Grafana panels for DNS availability, DNS probe duration, and DNS probe status.
- Remaining: Proxmox monitoring approach and Pi-hole metric planning.

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
- Confirm service probes work manually before Prometheus scrapes them.
- Confirm Prometheus targets show as healthy.
- Confirm Grafana dashboards display real data.
- Confirm documentation is updated with sanitized values.

## Documentation Updates Required

As this project progresses, update the following documentation:

- `docs/projects/project-002-monitoring-observability.md`
- `docs/architecture/monitoring.md`
- `docs/services/` service pages for Prometheus, Grafana, Node Exporter, and Blackbox Exporter
- `docs/architecture/vm-inventory.md`
- `docs/runbooks/` for monitoring troubleshooting procedures
- `docs/decisions/` if a major architecture decision is made
- `CHANGELOG.md` after meaningful milestones

## Future Improvements

- Custom Grafana dashboards for Linux host metrics.
- Pi-hole exporter or DNS-specific metrics.
- Proxmox exporter or API-based monitoring.
- Alertmanager.
- Email or chat-based notifications.
- Additional Blackbox probes for DNS, HTTP, and ICMP checks.
- Capacity planning dashboards.
- Backup and restore monitoring after Project 003.
- Security monitoring integration with future Wazuh, Suricata, and Zeek projects.

## Related Documentation

- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Pi-hole Service](../services/pihole.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
