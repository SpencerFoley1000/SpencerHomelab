# Monitoring and Observability

## Purpose

Describe the deployed monitoring architecture, what each layer proves, and the remaining boundaries for application, platform, alerting, and recovery work.

The design separates:

- Host metrics: Linux availability and resource pressure.
- Service probes: behavior from another system's perspective.
- Application metrics: service-specific internal behavior.
- Platform metrics: authoritative Proxmox state.
- Dashboards: visualization, not a substitute for source-level validation.

## Current Status

| Component | Host or scope | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VM | Active and backed up | Dedicated monitoring system |
| Node Exporter | `mon01`, `dns01`, `pve01` | Active | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Scraping, storage, and PromQL |
| Grafana | `mon01` | Active | Summary and detailed dashboards |
| Blackbox Exporter | `mon01` | Active | Recursive and local DNS probes |

`mon01` receives daily Project 003 VM backups. Its backup has not yet been independently restored.

## Prometheus Inventory

| Job | Target role | Expected state | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Up | Prometheus self-monitoring |
| `node_exporter` | `mon01` | Up | Monitoring-host metrics |
| `node_exporter` | `dns01` | Up | DNS-host metrics |
| `node_exporter` | `pve01` | Up | Proxmox Linux metrics |
| `blackbox_dns` | `dns01` recursive path | Up | Public-name DNS validation |
| `blackbox_dns_local` | `dns01` local record | Up | Expected internal answer validation |

Exact addresses and private record values remain outside Git.

## Grafana Dashboards

| Dashboard | Status | Purpose |
| --- | --- | --- |
| Imported Node Exporter dashboard | Active | Detailed Linux host troubleshooting |
| Homelab Service Health | Active | DNS availability, duration, and state history |
| Homelab Infrastructure Overview | Active | At-a-glance host health, capacity, uptime, and DNS status |

The Infrastructure Overview is operational but still requires a protected Classic JSON export.

## Architecture

### Host Metrics

```text
mon01, dns01, pve01
        |
        | TCP 9100
        v
   Node Exporter
        |
        v
Prometheus on mon01
        |
        v
 Grafana on mon01
```

### Recursive DNS Probe

```text
Prometheus
    |
    v
Blackbox Exporter: dns_udp
    |
    v
dns01 / Pi-hole
    |
    v
Upstream resolver and public DNS
```

### Local DNS Probe

```text
Prometheus
    |
    v
Blackbox Exporter: dns_udp_local
    |
    v
dns01 / Pi-hole local record
    |
    v
Expected internal answer
```

The DNS probes share an endpoint but test different failure domains.

## Monitoring Layers

### Host Monitoring

Node Exporter reports:

- CPU and load.
- Available and total memory.
- Filesystem capacity.
- Disk and network counters.
- Boot time and uptime.
- Exporter reachability.

A healthy Node Exporter target does not prove hosted applications or Proxmox guests are functioning.

### Service Monitoring

| Recursive | Local | Likely investigation area |
| --- | --- | --- |
| Up | Up | DNS paths healthy |
| Down | Up | Upstream resolver, internet path, or public query |
| Up | Down | Pi-hole local-record configuration or answer validation |
| Down | Down | `dns01`, Pi-hole, network, firewall, or monitoring path |

### Application Monitoring

Pi-hole-specific metrics are not yet collected. Future visibility may include query volume, blocking rate, cache behavior, upstream performance, and process health.

### Proxmox Platform Monitoring

Node Exporter on `pve01` does not report authoritative:

- VM or container state.
- Cluster or quorum state.
- Task results.
- Storage-pool health.
- Backup-job success or age.
- Replication or migration state.

A future Proxmox exporter or API integration must use a dedicated least-privilege identity.

## Design Decisions

### Shared Node Exporter Job

All Linux systems use one job with host and role labels:

```text
host="mon01", role="monitoring"
host="dns01", role="dns"
host="pve01", role="hypervisor"
```

### Static Remote Targets

Infrastructure targets use static addresses so monitoring does not depend on the DNS service being monitored. Public documentation uses placeholders.

### Linux Baseline Before API Credentials

Node Exporter delivered useful host visibility without introducing privileged Proxmox credentials. Platform monitoring remains a separate security-reviewed phase.

### Separate DNS Jobs

Different Prometheus jobs make recursive and local behavior explicit in PromQL, Grafana, troubleshooting, and future alerts.

### Summary and Detail Dashboards

- Infrastructure Overview: rapid status and capacity review.
- Imported Node Exporter dashboard: detailed host troubleshooting.
- Service Health: DNS behavior over time.

## Validation

Inventory:

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

Both DNS probes should return `1`.

Prometheus configuration validation and PromQL inventory validation are both required. Valid syntax does not prove every intended job remains present.

## Backup and Recovery

Important monitoring state:

- `/etc/prometheus/prometheus.yml`.
- `/etc/prometheus/blackbox.yml`.
- Grafana configuration and SQLite database.
- Prometheus data-source mapping.
- Dashboard JSON exports.
- Future alerting and recording rules.
- Historical metrics when retention becomes operationally important.

Project 003 completed:

- Daily VM backup coverage for `mon01`.
- Snapshot mode with Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external storage with mount-point enforcement.
- Configuration and state inventory.
- Protected existing dashboard exports.
- Recovery runbooks based on the tested Proxmox restore workflow.

Current limitations:

- `mon01` has not been independently restored.
- The Infrastructure Overview export is still pending.
- The `dns01` restore test proved the Proxmox VM workflow, not Grafana and Prometheus application recovery.

## Troubleshooting Lessons

### Blackbox YAML Nesting

The initial local-DNS module was nested incorrectly. The safe pattern was:

1. Restore the known-good file.
2. Confirm live service recovery.
3. Correct indentation.
4. Preflight on an alternate local port.
5. Restart production only after validation.

### New Target Delay

A new job may return an empty vector until its first scrape completes.

### Grafana Query IDs

Distinct query reference IDs are required when a panel contains multiple queries. Friendly names belong in legends.

### Dashboard Threshold Types

Grafana dashboard threshold values must be JSON numbers, not quoted strings.

### Firewall Validation

An active firewall does not prove a path is blocked. Testing from `mon01` showed no broad `pve01` rule was required.

## Alerting Philosophy

Alerting is not yet enabled. Every alert must have:

- A meaningful condition.
- An actionable threshold.
- A documented first response.
- A runbook.
- A notification route.

A small useful rule set is preferable to noise.

## Security Considerations

- Keep monitoring services internal-only.
- Do not expose TCP `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics, labels, JSON, and screenshots as operationally sensitive.
- Do not publish exact targets, private record values, credentials, or tokens.
- Introduce Proxmox credentials only through least privilege.
- Keep attacker and vulnerable workloads isolated from monitoring and backup systems.

## Next Improvements

- Export and privately validate the Infrastructure Overview.
- Add Proxmox VM, storage, task, and backup metrics.
- Add backup-age, capacity, and failure monitoring.
- Add Pi-hole-specific application metrics.
- Perform an independent `mon01` restore test.
- Add actionable alerts only after runbooks and routing exist.
- Add reverse-proxy and certificate monitoring during Project 004.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)