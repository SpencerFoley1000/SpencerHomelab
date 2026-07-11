# Blackbox Exporter

## Status

Active

## Purpose

Blackbox Exporter performs service-level probes from `mon01`. Node Exporter reports the condition of a Linux host; Blackbox Exporter verifies whether a network service behaves correctly from another system's point of view.

The deployed DNS probes answer two separate questions:

- Can `dns01` resolve a public name through its configured upstream resolver?
- Can `dns01` return the expected internal A record without depending on upstream DNS or internet connectivity?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Blackbox Exporter |
| Package | `prometheus-blackbox-exporter` |
| Verified version | `0.26.0-1` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Configuration | `/etc/prometheus/blackbox.yml` |
| Listen endpoint | `localhost:9115` |
| Consumer | Prometheus on `mon01` |
| Public exposure | None |

## Current Probes

| Module | Prometheus job | Query scope | What success proves | Status |
| --- | --- | --- | --- | --- |
| `dns_udp` | `blackbox_dns` | Public A-record query | `mon01` can reach `dns01`, Pi-hole can recurse through its upstream resolver, and the public query returns successfully | Active |
| `dns_udp_local` | `blackbox_dns_local` | Internal A-record query | `mon01` can reach `dns01` and Pi-hole returns the expected local record independently of upstream recursion | Active |

Both jobs target `<DNS01_IP>:53` through Blackbox Exporter on `localhost:9115`. Exact addresses and environment-specific DNS values remain private.

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

The local probe validates the answer section instead of accepting any `NOERROR` response. This prevents a successful result when the expected local A record is absent.

## Probe Paths

Recursive DNS:

```text
Prometheus on mon01
        |
        | scrape /probe?module=dns_udp
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

Local DNS:

```text
Prometheus on mon01
        |
        | scrape /probe?module=dns_udp_local
        v
Blackbox Exporter on localhost:9115
        |
        | UDP DNS query
        v
dns01 / Pi-hole local record
```

Separating the probes narrows incidents:

- Recursive probe down, local probe up: investigate upstream resolver or internet dependencies.
- Both probes down: investigate `dns01`, Pi-hole, routing, firewall policy, or the monitoring path.
- Local probe down, recursive probe up: investigate Pi-hole local-record configuration or the expected answer pattern.

## Safe Configuration Procedure

Create a rollback copy before editing:

```bash
sudo cp /etc/prometheus/blackbox.yml \
  /etc/prometheus/blackbox.yml.bak-$(date +%Y%m%d-%H%M)
```

Preflight a changed configuration on an unused local port before restarting the systemd service:

```bash
sudo timeout 3s /usr/bin/prometheus-blackbox-exporter \
  --config.file=/etc/prometheus/blackbox.yml \
  --web.listen-address=127.0.0.1:19115
```

Expected output includes `Loaded config file` and `Listening on`. The timeout sends SIGTERM after the short validation window.

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

Manual local-record probe:

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

Prometheus validation:

```promql
probe_success{job="blackbox_dns"}
```

```promql
probe_success{job="blackbox_dns_local", scope="local"}
```

Both should return `1`.

## Troubleshooting Lessons

### Module Indentation Failure

The first local-module edit placed `dns_udp_local` at the wrong YAML level. Blackbox Exporter failed with:

```text
field dns_udp_local not found in type config.plain
```

Resolution:

1. Restore the known-good rollback copy.
2. Confirm the service returns to `active`.
3. Add the new module as a direct child of `modules:`.
4. Preflight the full file on an alternate port.
5. Restart the live service only after the preflight succeeds.

This incident demonstrated that YAML can be syntactically readable while still mapping fields into the wrong application structure.

### Local-Only Endpoint

Prometheus and Blackbox Exporter run on the same VM. `localhost:9115` is sufficient and avoids unnecessary LAN exposure.

### Layered Validation

Validate in this order:

1. Exporter service.
2. Module directly through `/probe`.
3. Prometheus configuration with `promtool`.
4. Prometheus target and metric results.
5. Grafana visualization.

## Security Considerations

- Keep Blackbox Exporter internal-only.
- Do not expose TCP `9115` to untrusted networks.
- Do not publish exact probe targets or internal record values when unnecessary.
- Treat probe configuration and output as topology-revealing operational data.
- Keep security-lab probes isolated from trusted infrastructure.

## Backup and Recovery

Important state:

- `/etc/prometheus/blackbox.yml`
- Blackbox-related jobs in `/etc/prometheus/prometheus.yml`
- Grafana panels using probe metrics
- Sanitized documentation in this repository

The service is rebuildable, but protected VM backups and restore validation remain pending under Project 003.

Recovery order:

1. Restore or recreate `/etc/prometheus/blackbox.yml`.
2. Preflight the file on an alternate port.
3. Start and validate Blackbox Exporter.
4. Restore or recreate both Prometheus jobs.
5. Validate both `probe_success` series.
6. Confirm Grafana displays recursive and local DNS state.

## Maintenance Notes

- Revalidate both probes after DNS, routing, firewall, upstream-resolver, or local-record changes.
- Keep dashboard labels aligned with actual probe scope.
- Export affected dashboards after meaningful changes.
- Remove temporary rollback files after a protected known-good copy exists.
- Add alerts only after response procedures are documented.

## Future Improvements

- Add HTTP probes for future internal web services.
- Add narrowly scoped ICMP or TCP probes only when they answer a defined operational question.
- Add actionable DNS alerts with runbooks.
- Protect configuration through Project 003 backups and restore testing.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Grafana Service](grafana.md)
- [Node Exporter Service](node-exporter.md)
- [Pi-hole Service](pihole.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
