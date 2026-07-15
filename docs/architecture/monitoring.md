# Monitoring and Observability

## Purpose

Describe the deployed monitoring architecture, what each layer proves, and the remaining boundaries for application, platform, alerting, certificate, and recovery work.

The design separates:

- Host metrics: Linux availability and resource pressure.
- Service probes: behavior from another system's perspective.
- Certificate metrics: TLS presence and remaining lifetime.
- Application metrics: service-specific internal behavior.
- Platform metrics: authoritative Proxmox state.
- Dashboards: visualization, not a substitute for source-level validation.

## Current Status

| Component | Host or scope | Status | Purpose |
| --- | --- | --- | --- |
| `mon01` | Proxmox VM | Active and backed up | Dedicated monitoring system |
| Node Exporter | `mon01`, `dns01`, `pve01`, `proxy01` | Active | Linux host and hypervisor-OS metrics |
| Prometheus | `mon01` | Active | Scraping, storage, and PromQL |
| Grafana | `mon01` | Active | Summary and detailed dashboards |
| Blackbox Exporter | `mon01` | Active | Recursive DNS, local DNS, internal HTTPS, and certificate probes |

`mon01` receives daily Project 003 VM backups. Its backup has not yet been independently restored.

## Prometheus Inventory

| Job | Target role | Expected state | Purpose |
| --- | --- | --- | --- |
| `prometheus` | `localhost:9090` | Up | Prometheus self-monitoring |
| `node_exporter` | `mon01` | Up | Monitoring-host metrics |
| `node_exporter` | `dns01` | Up | DNS-host metrics |
| `node_exporter` | `pve01` | Up | Proxmox Linux metrics |
| `node_exporter` | `proxy01` | Up | Reverse-proxy host metrics |
| `blackbox_dns` | `dns01` recursive path | Up | Public-name DNS validation |
| `blackbox_dns_local` | `dns01` local record | Up | Expected internal answer validation |
| `blackbox_https_internal` | Grafana and Pi-hole through `proxy01` | Up | Internal HTTPS, hostname, trust, and certificate-expiration validation |

Exact addresses and private record values remain outside Git.

## Grafana Dashboards

| Dashboard | Status | Purpose |
| --- | --- | --- |
| Imported Node Exporter dashboard | Active | Detailed Linux host troubleshooting |
| Homelab Service Health | Active | DNS availability, duration, and state history |
| Homelab Infrastructure Overview | Active | At-a-glance host health, capacity, uptime, DNS, internal HTTPS, and certificate lifetime |

Current Project 004 panels include:

- Internal HTTPS Services.
- Internal Certificate Days Remaining.

The Infrastructure Overview requires a refreshed protected Classic JSON export after the Project 004 panel additions.

## Architecture

### Host Metrics

```text
mon01, dns01, pve01, proxy01
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

### DNS Probes

```text
Prometheus
    |
    v
Blackbox Exporter
    |-- dns_udp ------> dns01 -> upstream resolver -> public answer
    `-- dns_udp_local -> dns01 -> expected internal answer
```

### Internal HTTPS Probe

```text
Prometheus
    |
    v
Blackbox Exporter: https_internal
    |
    | HTTPS using mon01 trust store
    v
proxy01 / NGINX Proxy Manager
    |
    v
Selected backend service
```

This probe path exercises:

- DNS resolution from `mon01`.
- Network reachability to `proxy01`.
- TLS negotiation.
- Certificate chain and hostname validation.
- NGINX Proxy Manager routing.
- Backend HTTP response.

It does not prove interactive login or every application feature.

## Monitoring Layers

### Host Monitoring

Node Exporter reports:

- CPU and load.
- Available and total memory.
- Filesystem capacity.
- Disk and network counters.
- Boot time and uptime.
- Exporter reachability.

A healthy Node Exporter target does not prove hosted applications, proxy routes, certificates, or Proxmox guests are functioning.

### DNS Service Monitoring

| Recursive | Local | Likely investigation area |
| --- | --- | --- |
| Up | Up | DNS paths healthy |
| Down | Up | Upstream resolver, internet path, or public query |
| Up | Down | Pi-hole local-record configuration or answer validation |
| Down | Down | `dns01`, Pi-hole, network, firewall, or monitoring path |

### HTTPS and Certificate Monitoring

Important metrics:

```promql
probe_success{job="blackbox_https_internal"}
```

```promql
probe_http_status_code{job="blackbox_https_internal"}
```

```promql
(probe_ssl_earliest_cert_expiry{job="blackbox_https_internal"} - time()) / 86400
```

Interpretation:

| Host target | HTTPS probe | Likely investigation area |
| --- | --- | --- |
| Up | Up | Proxy host and selected service route healthy |
| Up | Down | NGINX Proxy Manager, TLS, DNS, trust, route, or backend issue |
| Down | Down | `proxy01`, networking, firewall, or broader infrastructure issue |
| Up | Up but days remaining low | Certificate renewal required |

### Application Monitoring

Pi-hole- and NGINX Proxy Manager-specific application metrics are not collected. Current service probes intentionally validate user-facing behavior rather than internal application counters.

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
host="proxy01", role="reverse-proxy"
```

### Static Remote Targets

Infrastructure host targets use static addresses or stable assignments so host monitoring does not depend on the DNS service being monitored. Public documentation uses placeholders.

### Service Names for HTTPS Probes

HTTPS probes intentionally use internal DNS names because certificate hostname validation is part of the question being tested. `mon01` trusts the public root CA certificate but does not contain the root CA private key.

### Separate Probe Jobs

Separate Prometheus jobs make recursive DNS, local DNS, and internal HTTPS behavior explicit in PromQL, Grafana, troubleshooting, and future alerts.

### Summary and Detail Dashboards

- Infrastructure Overview: rapid status, capacity, HTTPS, and certificate review.
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

Reverse proxy host:

```promql
up{job="node_exporter", host="proxy01", role="reverse-proxy"}
```

Recursive DNS:

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

Local DNS:

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Internal HTTPS:

```promql
probe_success{job="blackbox_https_internal"}
```

Both DNS probes and both HTTPS probes should return `1`.

Prometheus configuration validation and PromQL inventory validation are both required. Valid syntax does not prove every intended job remains present.

## Backup and Recovery

Important monitoring state:

- `/etc/prometheus/prometheus.yml`.
- `/etc/prometheus/blackbox.yml`.
- Debian trust-store copy of the public root CA certificate.
- Grafana configuration and SQLite database.
- Prometheus data-source mapping.
- Dashboard JSON exports.
- Future alerting and recording rules.
- Historical metrics when retention becomes operationally important.

Project 003 provides daily `mon01` VM backup coverage, configuration inventory, protected dashboard exports, and recovery runbooks.

Project 004 added:

- `proxy01` host target.
- `https_internal` Blackbox module.
- `blackbox_https_internal` job.
- Grafana HTTPS availability and certificate lifetime panels.

Current limitations:

- `mon01` has not been independently restored.
- The Infrastructure Overview export must be refreshed after Project 004.
- The `proxy01` restore proved the proxy workload, not restoration of `mon01` monitoring state.

## Troubleshooting Lessons

### YAML Placement and Target Discovery

A configuration can pass syntax validation while an intended target remains absent or incorrectly nested. Pair `promtool` with target inventory and direct PromQL queries.

### New Target Delay

A new job may return an empty vector until its first scrape completes.

### Trust Store Dependency

HTTPS probing with a private CA requires the public root certificate in the `mon01` system trust store. The root CA private key is not required and must not be copied to `mon01`.

### Grafana Display Names

Prometheus query legends can use `{{service}}`, while Grafana panel Display name fields use field variables such as:

```text
${__field.labels.service}
```

### Revocation Availability

The current private CA has no CRL or OCSP endpoint. Browser and tool behavior should distinguish unavailable revocation information from failed certificate chain or hostname validation.

## Alerting Philosophy

Alerting is not yet enabled. Every alert must have:

- A meaningful condition.
- An actionable threshold.
- A documented first response.
- A runbook.
- A notification route.

Potential future alerts include:

- Internal HTTPS probe failure.
- Certificate lifetime below the documented warning threshold.
- `proxy01` host target failure.

A small useful rule set is preferable to noise.

## Security Considerations

- Keep monitoring services internal-only.
- Do not expose TCP `3000`, `9090`, `9100`, or `9115` publicly.
- Treat metrics, labels, JSON, screenshots, probe targets, and certificate metadata as operationally sensitive.
- Do not publish exact targets, private record values, credentials, keys, or tokens.
- Install only the public root CA certificate on `mon01`.
- Introduce Proxmox credentials only through least privilege.
- Keep attacker and vulnerable workloads isolated from monitoring, proxy, PKI, and backup systems.

## Next Improvements

- Refresh and privately validate the Infrastructure Overview export.
- Add Proxmox VM, storage, task, and backup metrics.
- Add backup-age, capacity, and failure monitoring.
- Add Pi-hole-specific application metrics.
- Perform an independent `mon01` restore test.
- Add actionable HTTPS and certificate alerts only after runbooks and routing exist.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
