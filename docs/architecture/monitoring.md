# Monitoring and Observability

## Purpose

This document describes the deployed monitoring architecture, what each layer proves, and the boundaries that remain for future platform, application, alerting, and recovery work.

The design prioritizes operational clarity:

- Host metrics answer whether a Linux system is running and under resource pressure.
- Service probes answer whether a network service behaves correctly from another host.
- Application and platform metrics answer what is happening inside Pi-hole or Proxmox.
- Dashboards summarize data but do not replace source-level validation.

## Current Status

| Component | Host or scope | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VM | Active | Dedicated monitoring and observability system |
| Node Exporter | `mon01`, `dns01`, `pve01` | Active | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Metrics scraping, storage, and PromQL |
| Grafana | `mon01` | Active | Summary and detailed dashboards |
| Blackbox Exporter | `mon01` | Active | Recursive and local DNS probes |

## Current Prometheus Inventory

| Job | Target | Expected state | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | `UP` | Prometheus self-monitoring |
| `node_exporter` | `localhost:9100` | `UP` | `mon01` host metrics |
| `node_exporter` | `<DNS01_IP>:9100` | `UP` | `dns01` host metrics |
| `node_exporter` | `<PVE01_IP>:9100` | `UP` | `pve01` Linux operating-system metrics |
| `blackbox_dns` | `<DNS01_IP>:53` through `localhost:9115` | `UP` | Recursive public-name DNS probe |
| `blackbox_dns_local` | `<DNS01_IP>:53` through `localhost:9115` | `UP` | Internal-record DNS probe |

Exact addresses and environment-specific record values remain private.

## Current Grafana Dashboards

| Dashboard | Status | Purpose |
| --- | --- | --- |
| Imported Node Exporter dashboard | Active | Detailed host troubleshooting for `mon01`, `dns01`, and `pve01` |
| Homelab Service Health | Active | DNS availability, duration, and state history |
| Homelab Infrastructure Overview | Active | At-a-glance host health, resource utilization, uptime, and recursive/local DNS state |

The Homelab Infrastructure Overview is operational, but its private Classic JSON export is still pending.

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

### Recursive DNS Probe

```text
Prometheus on mon01
          |
          | /probe?module=dns_udp
          v
Blackbox Exporter on localhost:9115
          |
          | UDP DNS query
          v
      dns01 / Pi-hole
          |
          | upstream recursion
          v
     Public DNS answer
```

### Local DNS Probe

```text
Prometheus on mon01
          |
          | /probe?module=dns_udp_local
          v
Blackbox Exporter on localhost:9115
          |
          | UDP DNS query
          v
      dns01 / Pi-hole
          |
          | local record lookup
          v
    Expected internal answer
```

The two DNS probes intentionally share the same DNS endpoint but use different query modules and Prometheus jobs. This separates local Pi-hole behavior from upstream resolver and internet dependencies.

## Monitoring Layers

### Host Monitoring

Node Exporter reports:

- CPU time and load
- Available and total memory
- Filesystem capacity
- Disk activity
- Network counters
- Boot time and uptime
- Exporter reachability

A healthy Node Exporter target does not prove hosted applications, VMs, or containers are functioning.

### Service Monitoring

Blackbox Exporter validates DNS from `mon01`:

- `blackbox_dns` proves the recursive path through Pi-hole and its upstream resolver.
- `blackbox_dns_local` proves the expected local A record is returned without relying on upstream recursion.

Interpretation:

| Recursive | Local | Likely investigation area |
| --- | --- | --- |
| Up | Up | DNS paths healthy |
| Down | Up | Upstream resolver, internet path, or public query |
| Up | Down | Pi-hole local-record configuration or expected answer validation |
| Down | Down | `dns01`, Pi-hole, network path, firewall, or monitoring path |

### Application Monitoring

Pi-hole-specific application metrics are not yet collected. Future application visibility may include:

- Query volume
- Blocked-query rate
- Cache behavior
- Upstream response behavior
- Pi-hole process health

### Hypervisor Platform Monitoring

`pve01` currently exposes Linux host metrics through Node Exporter. This baseline does not expose authoritative Proxmox state such as:

- VM or container state
- Cluster or quorum state
- Task results
- Storage-pool status
- Backup-job status
- Replication or migration state

A future Proxmox exporter or API integration should use a dedicated least-privilege identity and be documented before credentials are created.

## Design Decisions

### Shared Node Exporter Job

All Linux systems use one `node_exporter` job with host and role labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

This keeps PromQL and dashboard logic consistent as new Linux hosts are added.

### Static Remote Targets

Remote infrastructure targets use static addresses so monitoring remains available during DNS failure. Public documentation uses placeholders instead of exact values.

### Linux Baseline Before Proxmox API Credentials

Node Exporter provided immediate hypervisor-OS visibility without introducing privileged API access. Platform-specific Proxmox metrics remain a separate future phase.

### Separate Recursive and Local DNS Jobs

Different Prometheus jobs make query scope explicit and simplify dashboards, troubleshooting, and future alerting.

### Summary and Detail Dashboards

- Homelab Infrastructure Overview: rapid health and capacity view.
- Imported Node Exporter dashboard: detailed host troubleshooting.
- Homelab Service Health: service-level DNS history.

This avoids overloading one dashboard with every available metric.

## Homelab Infrastructure Overview

The custom dashboard was built manually on 2026-07-11.

| Panel | Purpose |
| --- | --- |
| Host Availability | Current state of all three Node Exporter targets |
| CPU Utilization by Host | Compare CPU demand across infrastructure systems |
| Memory Utilization by Host | Compare memory pressure across hosts |
| Root Filesystem Utilization | Show capacity risk with warning and critical thresholds |
| Host Uptime | Show time since each system booted |
| DNS Availability | Show Recursive DNS and Local DNS independently |
| DNS Probe Duration | Show recursive DNS latency and spikes over time |

The dashboard is intended for quick operational review rather than exhaustive troubleshooting.

## PromQL Validation

Inventory jobs and targets:

```promql
count by (job, instance) (up)
```

All Linux hosts:

```promql
up{job="node_exporter"}
```

Proxmox host:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Recursive DNS:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

Local DNS:

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Both DNS probes:

```promql
probe_success{job=~"blackbox_dns.*", host="dns01"}
```

Configuration validation and PromQL validation are both required after Prometheus changes. A file can be syntactically valid while an intended job or target is missing.

## Security Considerations

- Keep Prometheus, Grafana, Node Exporter, and Blackbox Exporter internal-only.
- Do not expose TCP `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics, labels, raw JSON, and dashboard screenshots as operationally sensitive.
- Do not publish exact addresses, usernames, tokens, private record values, or unnecessary topology details.
- Avoid broad firewall rules when the existing trusted monitoring path is sufficient.
- Introduce Proxmox API credentials only through a documented least-privilege design.
- Keep future attacker and intentionally vulnerable workloads isolated from monitoring infrastructure.

## Backup and Recovery

Important monitoring state includes:

- Prometheus configuration
- Blackbox Exporter configuration
- Grafana database and data-source mapping
- Dashboard JSON exports
- Future alerting and recording rules
- Historical metrics if retention becomes operationally important

Project 003 Phase 003A inventoried this state and validated existing private dashboard exports. The Homelab Infrastructure Overview export, protected VM backups, and restore testing remain pending.

## Troubleshooting Lessons

### Blackbox Module at the Wrong YAML Level

The initial local DNS module was nested incorrectly. Blackbox Exporter rejected the configuration with `field dns_udp_local not found in type config.plain`.

The safe recovery pattern was:

1. Restore the known-good file.
2. Confirm the live service is active.
3. correct the module indentation.
4. Preflight the configuration on an alternate local port.
5. Restart the live service only after the preflight succeeds.

### New Prometheus Job Initially Returned No Data

The first query immediately after reload returned an empty vector. After the next scrape, both DNS jobs returned `1`. Allow one scrape interval before diagnosing a newly created target as missing.

### Grafana Query Reference IDs

Prometheus contained both DNS series, but Grafana displayed only one until the two panel queries used distinct reference IDs (`A` and `B`). Friendly text belongs in the legend, not in the reference-ID field.

### Dashboard v2 Threshold Types

Dashboard v2 parsing rejected quoted numeric threshold values. Threshold numbers must be represented as JSON numbers, while display labels remain strings.

### Active Firewall Does Not Automatically Mean Blocked

`pve01` had an active Proxmox firewall, but validation from `mon01` showed the existing policy already allowed the required Node Exporter connection. No unnecessary broad rule was added.

## Alerting Philosophy

Alerting is not yet enabled. An alert must have:

- A meaningful failure condition
- An actionable threshold
- A documented first response
- A runbook
- A defined notification route

A small set of useful alerts is preferable to a noisy ruleset.

## Next Improvements

- Export and privately validate the Homelab Infrastructure Overview as Classic JSON.
- Add Proxmox-specific VM, storage, task, and backup metrics through least-privilege integration.
- Evaluate Pi-hole-specific application metrics.
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
