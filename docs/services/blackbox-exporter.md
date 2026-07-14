# Blackbox Exporter

## Status

Active

## Purpose

Blackbox Exporter performs service-level probes from `mon01`. Node Exporter reports Linux host condition; Blackbox Exporter verifies whether a network service behaves correctly from another system's perspective.

The deployed probes answer:

- Can `dns01` resolve a public name through its upstream resolver?
- Can `dns01` return the expected internal A record without upstream DNS or internet access?

## Technology Stack

| Component | Value |
| --- | --- |
| Package | `prometheus-blackbox-exporter` |
| Verified version | `0.26.0-1` |
| Host | `mon01` |
| Operating system | Debian 13.5 Trixie |
| Configuration | `/etc/prometheus/blackbox.yml` |
| Listen endpoint | `localhost:9115` |
| Consumer | Prometheus on `mon01` |
| Public exposure | None |
| Backup maturity | Protected by daily `mon01` VM backup; configuration inventoried; independent restore not yet tested |

## Current Probes

| Module | Prometheus job | Scope | What success proves |
| --- | --- | --- | --- |
| `dns_udp` | `blackbox_dns` | Public A-record query | `mon01` reaches `dns01`; Pi-hole recurses through the upstream resolver; the public query succeeds |
| `dns_udp_local` | `blackbox_dns_local` | Internal A-record query | `mon01` reaches `dns01`; Pi-hole returns the expected local record independently of upstream recursion |

Both jobs target `<DNS01_IP>:53` through `localhost:9115`. Exact addresses and private DNS values remain outside Git.

## Sanitized Configuration

```yaml
modules:
  dns_udp:
    prober: dns
    timeout: 5s
    dns:
      transport_protocol: udp
      preferred_ip_protocol: ip4
      query_name: example.com
      query_type: A
      valid_rcodes:
        - NOERROR

  dns_udp_local:
    prober: dns
    timeout: 5s
    dns:
      transport_protocol: udp
      preferred_ip_protocol: ip4
      query_name: <INTERNAL_RECORD>.
      query_type: A
      valid_rcodes:
        - NOERROR
      validate_answer_rrs:
        fail_if_none_matches_regexp:
          - '^<ESCAPED_INTERNAL_RECORD>\..*[[:space:]]IN[[:space:]]+A[[:space:]]+.*$'
```

The local probe validates the answer section instead of accepting any `NOERROR` response.

## Probe Paths

Recursive:

```text
Prometheus -> Blackbox Exporter -> dns01 / Pi-hole -> upstream resolver -> public answer
```

Local:

```text
Prometheus -> Blackbox Exporter -> dns01 / Pi-hole -> expected local answer
```

Interpretation:

- Recursive down, local up: investigate upstream resolver or internet dependencies.
- Both down: investigate `dns01`, Pi-hole, routing, firewall policy, or monitoring path.
- Local down, recursive up: investigate local-record configuration or answer matching.

## Safe Configuration Procedure

Create a rollback copy:

```bash
sudo cp /etc/prometheus/blackbox.yml \
  /etc/prometheus/blackbox.yml.bak-$(date +%Y%m%d-%H%M)
```

Preflight on an unused local port:

```bash
sudo timeout 3s /usr/bin/prometheus-blackbox-exporter \
  --config.file=/etc/prometheus/blackbox.yml \
  --web.listen-address=127.0.0.1:19115
```

Expected output includes `Loaded config file` and `Listening on`.

Apply and verify:

```bash
sudo systemctl restart prometheus-blackbox-exporter
systemctl is-active prometheus-blackbox-exporter
```

## Validation

Manual recursive probe:

```bash
curl -sG http://localhost:9115/probe \
  --data-urlencode 'module=dns_udp' \
  --data-urlencode 'target=<DNS01_IP>:53' |
grep -E '^(probe_success|probe_dns_)'
```

Manual local probe:

```bash
curl -sG http://localhost:9115/probe \
  --data-urlencode 'module=dns_udp_local' \
  --data-urlencode 'target=<DNS01_IP>:53' |
grep -E '^(probe_success|probe_dns_)'
```

Expected local results include:

```text
probe_dns_answer_rrs 1
probe_dns_query_succeeded 1
probe_success 1
```

Prometheus:

```promql
probe_success{job="blackbox_dns"}
```

```promql
probe_success{job="blackbox_dns_local", scope="local"}
```

Both should return `1`.

## Troubleshooting Lessons

### Module Indentation Failure

The first local module was placed at the wrong YAML level, producing an application-schema error.

Safe resolution:

1. Restore the known-good file.
2. Confirm the service is active.
3. Add the module as a direct child of `modules:`.
4. Preflight the complete file on an alternate port.
5. Restart production only after validation.

### Local-Only Endpoint

Prometheus and Blackbox Exporter share `mon01`, so `localhost:9115` avoids unnecessary LAN exposure.

### Layered Validation

Validate in this order:

1. Exporter service.
2. Module directly through `/probe`.
3. Prometheus configuration.
4. Prometheus target and metric results.
5. Grafana visualization.

## Backup and Recovery

Important state:

- `/etc/prometheus/blackbox.yml`.
- Blackbox jobs in `/etc/prometheus/prometheus.yml`.
- Grafana panels using probe metrics.
- Sanitized documentation.

Project 003 provides:

- Daily full-VM backup of `mon01`.
- Snapshot mode with Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external storage with mount-point enforcement.
- Configuration and dependency inventory.

Recovery order:

1. Restore the `mon01` VM backup or rebuild Debian.
2. Restore or recreate `blackbox.yml`.
3. Preflight on an alternate local port.
4. Start and validate Blackbox Exporter.
5. Restore or recreate both Prometheus jobs.
6. Validate both `probe_success` series.
7. Confirm Grafana displays recursive and local DNS state.

Current limitation: `mon01` has not been independently restored.

## Security Considerations

- Keep Blackbox Exporter internal-only.
- Do not expose TCP `9115` to untrusted networks.
- Do not publish exact probe targets or internal record values.
- Treat probe configuration and output as topology-revealing.
- Keep security-lab probes isolated from trusted infrastructure.

## Maintenance Notes

- Revalidate both probes after DNS, routing, firewall, upstream-resolver, or local-record changes.
- Keep dashboard labels aligned with probe scope.
- Confirm a recent successful `mon01` backup before major changes.
- Remove temporary rollback files only after a protected known-good copy exists.
- Add alerts only after response procedures are documented.

## Future Improvements

- Add HTTP probes for Project 004 services.
- Add certificate-expiry checks through an appropriate monitoring design.
- Add narrowly scoped ICMP or TCP probes only for defined operational questions.
- Add actionable DNS alerts with runbooks.
- Perform an independent `mon01` restore test.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus](prometheus.md)
- [Grafana](grafana.md)
- [Node Exporter](node-exporter.md)
- [Pi-hole](pihole.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)