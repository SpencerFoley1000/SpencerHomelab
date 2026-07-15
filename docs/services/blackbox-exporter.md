# Blackbox Exporter

## Status

Active

## Purpose

Blackbox Exporter performs service-level probes from `mon01`. Node Exporter reports Linux host condition; Blackbox Exporter verifies whether a network service behaves correctly from another system's perspective.

The deployed probes answer:

- Can `dns01` resolve a public name through its upstream resolver?
- Can `dns01` return the expected internal A record without upstream DNS or internet access?
- Can `mon01` resolve and reach selected internal HTTPS services through `proxy01`?
- Does the TLS certificate validate for the requested hostname?
- When does the earliest served certificate expire?

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
| `https_internal` | `blackbox_https_internal` | Grafana and Pi-hole through `proxy01` | Internal DNS resolves; TLS and hostname validation succeed; NGINX Proxy Manager routes the request; the backend returns an HTTP response |

Exact addresses and private DNS values remain outside Git.

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

  https_internal:
    prober: http
    timeout: 5s
    http:
      method: GET
      preferred_ip_protocol: ip4
      fail_if_not_ssl: true
```

The local DNS probe validates the answer section instead of accepting any `NOERROR` response.

The HTTPS probe uses the `mon01` system trust store. The public root CA certificate is installed there; the root CA private key is not.

## Probe Paths

Recursive:

```text
Prometheus -> Blackbox Exporter -> dns01 / Pi-hole -> upstream resolver -> public answer
```

Local:

```text
Prometheus -> Blackbox Exporter -> dns01 / Pi-hole -> expected local answer
```

Internal HTTPS:

```text
Prometheus -> Blackbox Exporter -> Pi-hole local DNS -> proxy01 -> selected backend
```

Interpretation:

- Recursive down, local up: investigate upstream resolver or internet dependencies.
- Both DNS probes down: investigate `dns01`, Pi-hole, routing, firewall policy, or monitoring path.
- Local down, recursive up: investigate local-record configuration or answer matching.
- HTTPS down with `proxy01` host up: investigate DNS, trust store, certificate, NGINX Proxy Manager, route, or backend.
- HTTPS down with `proxy01` host down: investigate `proxy01`, networking, or broader infrastructure.
- HTTPS up with low certificate lifetime: renew the service certificate.

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

Manual HTTPS probe:

```bash
curl -sG http://localhost:9115/probe \
  --data-urlencode 'module=https_internal' \
  --data-urlencode 'target=https://grafana.lab.home.arpa' |
grep -E '^(probe_success|probe_http_status_code|probe_ssl_earliest_cert_expiry)'
```

Expected results include:

```text
probe_success 1
```

Prometheus:

```promql
probe_success{job="blackbox_dns"}
```

```promql
probe_success{job="blackbox_dns_local", scope="local"}
```

```promql
probe_success{job="blackbox_https_internal"}
```

Certificate lifetime:

```promql
(probe_ssl_earliest_cert_expiry{job="blackbox_https_internal"} - time()) / 86400
```

Both DNS probes and both HTTPS service series should return success.

## Troubleshooting Lessons

### Module Indentation Failure

A module placed at the wrong YAML level produces an application-schema error. Restore the known-good file, confirm service recovery, correct indentation, preflight on an alternate port, and restart production only after validation.

### Local-Only Exporter Endpoint

Prometheus and Blackbox Exporter share `mon01`, so `localhost:9115` avoids unnecessary LAN exposure.

### Private CA Trust Failure

If the HTTPS module fails certificate validation:

1. Test the endpoint with `curl` from `mon01`.
2. Confirm the public root CA certificate exists in the Debian trust store.
3. Run `sudo update-ca-certificates` after intentional trust changes.
4. Confirm the served certificate hostname and chain.
5. Never copy the root CA private key to `mon01`.

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
- Public root CA certificate in the `mon01` trust store.
- Grafana panels using probe metrics.
- Sanitized documentation.

Project 003 provides daily full-VM backup of `mon01`, tiered retention, dedicated external storage, configuration inventory, and recovery runbooks.

Recovery order:

1. Restore the `mon01` VM backup or rebuild Debian.
2. Restore or recreate `blackbox.yml`.
3. Install the public root CA certificate in the system trust store.
4. Preflight the complete configuration on an alternate local port.
5. Start and validate Blackbox Exporter.
6. Restore or recreate DNS and HTTPS Prometheus jobs.
7. Validate all `probe_success` series and certificate lifetime.
8. Confirm Grafana displays DNS, HTTPS, and certificate state.

Current limitation: `mon01` has not been independently restored.

## Security Considerations

- Keep Blackbox Exporter internal-only.
- Do not expose TCP `9115` to untrusted networks.
- Do not publish exact probe targets or private record values unnecessarily.
- Treat probe configuration and output as topology-revealing.
- Install only the public root CA certificate on `mon01`.
- Keep security-lab probes isolated from trusted infrastructure.

## Maintenance Notes

- Revalidate probes after DNS, routing, firewall, upstream-resolver, trust-store, certificate, or proxy changes.
- Keep dashboard labels aligned with probe scope.
- Confirm a recent successful `mon01` backup before major changes.
- Remove temporary rollback files only after a protected known-good copy exists.
- Add alerts only after response procedures and notification routing are documented.

## Future Improvements

- Add actionable internal HTTPS and certificate-expiration alerts.
- Add narrowly scoped ICMP or TCP probes only for defined operational questions.
- Add actionable DNS alerts with runbooks.
- Perform an independent `mon01` restore test.

## Related Documentation

- [Project 002](../projects/project-002-monitoring-observability.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus](prometheus.md)
- [Grafana](grafana.md)
- [Node Exporter](node-exporter.md)
- [Pi-hole](pihole.md)
- [NGINX Proxy Manager](nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
