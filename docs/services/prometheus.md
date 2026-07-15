# Prometheus

## Status

Active

## Purpose

Prometheus collects, stores, and queries metrics for the homelab. It scrapes Linux host metrics from Node Exporter, DNS and HTTPS probe metrics through Blackbox Exporter, and its own health metrics. Grafana uses Prometheus as its primary data source.

The current configuration answers:

- Are `mon01`, `dns01`, `pve01`, and `proxy01` reporting host metrics?
- Is recursive DNS through `dns01` working?
- Is the expected internal DNS record available independently of upstream recursion?
- Are the internal Grafana and Pi-hole HTTPS routes working?
- How many days remain before the internal service certificate expires?
- How are resource use and probe duration changing over time?

## Technology Stack

| Component | Value |
| --- | --- |
| Package version | `2.53.3+ds1-2` |
| Host | `mon01` |
| Operating system | Debian 13.5 Trixie |
| Configuration | `/etc/prometheus/prometheus.yml` |
| Metrics storage | `/var/lib/prometheus/metrics2/` |
| Grafana connection | `http://localhost:9090` |
| Trusted UI access | Internal homelab only |
| Public exposure | None |
| Backup maturity | Daily `mon01` VM backup active; configuration inventoried; independent restore not yet tested |

TCP `9090` must not be publicly exposed.

## Current Jobs

| Job | Target role | Labels or purpose | Expected state |
| --- | --- | --- | --- |
| `prometheus` | Prometheus self-monitoring | Local service | Up |
| `node_exporter` | `mon01` | `host="mon01"`, `role="monitoring"` | Up |
| `node_exporter` | `dns01` | `host="dns01"`, `role="dns"` | Up |
| `node_exporter` | `pve01` | `host="pve01"`, `role="hypervisor"` | Up |
| `node_exporter` | `proxy01` | `host="proxy01"`, `role="reverse-proxy"` | Up |
| `blackbox_dns` | Recursive DNS through `dns01` | Public-name query | Up |
| `blackbox_dns_local` | Local DNS through `dns01` | Expected answer with `scope="local"` | Up |
| `blackbox_https_internal` | Grafana and Pi-hole through `proxy01` | HTTPS and certificate validation with service labels | Up |

Exact addresses remain private. Use `<DNS01_IP>`, `<MON01_IP>`, `<PVE01_IP>`, and `<PROXY01_IP>` publicly.

## Sanitized Scrape Design

### Shared Node Exporter Job

```yaml
- job_name: node_exporter
  static_configs:
    - targets: ['localhost:9100']
      labels:
        host: 'mon01'
        role: 'monitoring'
    - targets: ['<DNS01_IP>:9100']
      labels:
        host: 'dns01'
        role: 'dns'
    - targets: ['<PVE01_IP>:9100']
      labels:
        host: 'pve01'
        role: 'hypervisor'
    - targets: ['<PROXY01_IP>:9100']
      labels:
        host: 'proxy01'
        role: 'reverse-proxy'
```

### Recursive DNS Job

```yaml
- job_name: blackbox_dns
  metrics_path: /probe
  params:
    module: [dns_udp]
  static_configs:
    - targets: ['<DNS01_IP>:53']
      labels:
        host: 'dns01'
        service: 'dns'
        protocol: 'udp'
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

### Local DNS Job

```yaml
- job_name: blackbox_dns_local
  metrics_path: /probe
  params:
    module: [dns_udp_local]
  static_configs:
    - targets: ['<DNS01_IP>:53']
      labels:
        host: 'dns01'
        service: 'dns'
        scope: 'local'
        protocol: 'udp'
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

### Internal HTTPS Job

```yaml
- job_name: 'blackbox_https_internal'
  metrics_path: /probe
  params:
    module: [https_internal]
  static_configs:
    - targets:
        - 'https://grafana.lab.home.arpa'
      labels:
        service: 'grafana'
        scope: 'internal'
    - targets:
        - 'https://pihole.lab.home.arpa'
      labels:
        service: 'pihole'
        scope: 'internal'
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9115
```

Separate jobs keep DNS and HTTPS failure domains explicit.

## Safe Configuration Changes

Create a rollback copy:

```bash
sudo cp /etc/prometheus/prometheus.yml \
  /etc/prometheus/prometheus.yml.bak-$(date +%Y%m%d-%H%M)
```

Validate:

```bash
sudo promtool check config /etc/prometheus/prometheus.yml
```

Reload or restart and confirm service state:

```bash
sudo systemctl restart prometheus
systemctl is-active prometheus
```

`promtool` validates syntax and structure. It does not prove every intended job remains present, so PromQL and target-inventory validation are mandatory.

## Validation

Service health:

```bash
systemctl is-active prometheus
systemctl is-enabled prometheus
curl localhost:9090/-/ready
curl localhost:9090/-/healthy
```

Target inventory:

```promql
count by (job, instance) (up)
```

Linux hosts:

```promql
up{job="node_exporter"}
```

Expected hosts: `mon01`, `dns01`, `pve01`, and `proxy01`.

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

Certificate lifetime:

```promql
(probe_ssl_earliest_cert_expiry{job="blackbox_https_internal"} - time()) / 86400
```

Both DNS probes and both HTTPS probes should return `1`.

A new job may briefly return no data until its first scrape completes. An empty vector differs from a target returning `0`.

## Monitoring Boundaries

Node Exporter on `pve01` does not provide authoritative VM, task, storage-pool, cluster, or backup-job state. Those require a future Proxmox-specific integration using least-privilege credentials.

DNS boundaries:

- `blackbox_dns` includes Pi-hole, upstream resolver, and internet dependencies.
- `blackbox_dns_local` isolates Pi-hole local-record behavior from upstream recursion.

HTTPS boundaries:

- `blackbox_https_internal` includes internal DNS, `proxy01`, TLS validation, proxy routing, and the backend HTTP response.
- It does not prove interactive login or every application feature.
- It depends on the public root CA certificate being installed in the `mon01` trust store.

## Troubleshooting Notes

### Valid Configuration but Missing Target

A configuration can pass `promtool` while an intended target is absent or incorrectly nested. Pair syntax validation with:

```promql
count by (job, instance) (up)
```

and target-specific queries.

### Initial Empty Query

Allow one scrape interval after adding a new target before diagnosing an empty result.

### Private CA Trust

If HTTPS probes fail while browser access works, confirm that `mon01` trusts the public root CA certificate. Never copy the root CA private key to `mon01`.

### Grafana Display Labels

Prometheus labels such as `service="grafana"` and `service="pihole"` support concise Grafana display names without publishing addresses.

## Backup and Recovery

Important state:

- `/etc/prometheus/prometheus.yml`.
- `/etc/prometheus/blackbox.yml`.
- Public root CA certificate in the Debian trust store.
- Future alerting and recording rules.
- Local time-series history when operationally important.
- Documentation and validation queries.

Project 003 provides daily full-VM backup coverage for `mon01`, tiered retention, protected configuration inventories, and recovery runbooks.

At current scale, configuration is more important than short-term metric history for manual reconstruction.

Recovery order:

1. Restore the `mon01` VM backup or rebuild Debian.
2. Restore or recreate Prometheus and Blackbox configuration.
3. Reinstall the public root CA certificate in the trust store.
4. Validate with `promtool` and Blackbox preflight checks.
5. Start Prometheus and Blackbox Exporter.
6. Confirm all four host targets, both DNS probes, and both HTTPS probes.
7. Confirm Grafana dashboards display current data.

Current limitation: `mon01` has not been independently restore-tested.

## Security Considerations

- Keep Prometheus internal-only.
- Do not expose TCP `9090` publicly.
- Restrict UI access to trusted administrators.
- Do not publish raw metrics, exact targets, private labels, credentials, certificate keys, or screenshots containing topology.
- Install only the public root CA certificate on `mon01`.
- Introduce Proxmox API credentials only through least privilege.

## Maintenance Notes

- Validate configuration before every restart or reload.
- Verify target inventory after every change.
- Confirm backup coverage before significant upgrades.
- Monitor local storage growth.
- Record package-version changes.
- Update recovery inventories when jobs, trust stores, or labels change.
- Perform an independent `mon01` restore after major monitoring changes or before migration.

## Future Improvements

- Add Proxmox VM, storage, task, and backup metrics.
- Add backup-age and failure monitoring.
- Add recording rules where repeated expensive queries justify them.
- Add Alertmanager only after thresholds, runbooks, and notification routing exist.
- Add actionable internal HTTPS and certificate-expiration alerts.
- Define metrics retention based on measured storage growth.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Grafana](grafana.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Node Exporter](node-exporter.md)
- [NGINX Proxy Manager](nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
