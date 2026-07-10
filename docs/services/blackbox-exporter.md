# Blackbox Exporter

## Status

Active

## Purpose

Blackbox Exporter performs service-level probes for the homelab monitoring stack. Unlike Node Exporter, which reports host metrics from inside Linux, Blackbox Exporter checks whether a network service is reachable and responding from the monitoring system's point of view.

The first deployed probe validates recursive DNS resolution through `dns01`.

Blackbox Exporter helps answer operational questions such as:

- Is the DNS endpoint reachable from `mon01`?
- Can `dns01` complete the configured DNS query?
- Is a service failure visible even when the host remains online?
- How long does the probe take?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Blackbox Exporter |
| Package | `prometheus-blackbox-exporter` |
| Host | `mon01` |
| Operating system | Debian 13.5 |
| Deployment method | Debian package repository |
| Default port | `9115/tcp` |
| Configuration file | `/etc/prometheus/blackbox.yml` |
| Current consumer | Prometheus on `mon01` |

## Current Probes

| Probe | Target | Query Scope | Purpose | Status |
| --- | --- | --- | --- | --- |
| `dns_udp` | `<DNS01_IP>:53` | Public A-record query through Pi-hole and its upstream resolver | Validate recursive DNS resolution from `mon01` | Active |

Exact IP addresses are omitted. Use placeholders such as `<DNS01_IP>` and `<MON01_IP>`.

## Deployment Notes

Blackbox Exporter was installed from the Debian package repository:

```bash
sudo apt install -y prometheus-blackbox-exporter
```

The service was validated locally from `mon01`:

```bash
systemctl is-active prometheus-blackbox-exporter
curl localhost:9115/metrics
```

The DNS probe was tested manually before Prometheus was configured:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

A successful probe returned:

```text
probe_success 1
```

## Configuration

Blackbox Exporter modules are configured in:

```text
/etc/prometheus/blackbox.yml
```

The current DNS module is documented in sanitized form:

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
```

Prometheus scrapes the probe through the `blackbox_dns` job:

```text
Prometheus -> localhost:9115 Blackbox Exporter -> <DNS01_IP>:53
```

The exporter performs the probe, Prometheus stores the returned metrics, and Grafana visualizes the result.

## Probe Interpretation

The current module queries a public name, so a successful result validates the complete path:

```text
mon01 -> dns01/Pi-hole -> configured upstream resolver -> public DNS result
```

A failed probe does not prove that Pi-hole alone failed. Possible causes include:

- `dns01` or Pi-hole being unavailable.
- Internal routing or firewall failure.
- Upstream internet failure.
- Upstream resolver failure.
- Failure of the configured public query.

A second probe for a sanitized local record should be added later. That would validate internal DNS independently from upstream recursive resolution.

## Networking

| Item | Value |
| --- | --- |
| Listen port | `9115/tcp` |
| Access scope | Local/internal monitoring only |
| Public exposure | None |
| Current probe target | `<DNS01_IP>:53` |
| Intended consumer | Prometheus on `mon01` |

Prometheus and Blackbox Exporter run on the same VM, so Prometheus uses `localhost:9115`. The exporter does not need to listen on or be exposed through the LAN interface.

## Validation Procedure

Run on `mon01`:

```bash
systemctl is-active prometheus-blackbox-exporter
curl localhost:9115/metrics
```

Manual DNS probe:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

Expected output includes:

```text
probe_success 1
```

Prometheus validation:

```promql
probe_success{job="blackbox_dns"}
```

Expected result:

```text
1
```

Probe duration:

```promql
probe_duration_seconds{job="blackbox_dns"}
```

Grafana validation:

- Open the `Homelab Service Health` dashboard.
- Confirm DNS availability shows success.
- Confirm probe duration is present.
- Confirm the status timeline continues updating.

## Troubleshooting Notes

### Probe Endpoint Not Reachable on LAN IP

During validation, Blackbox Exporter was active but a request to the `mon01` LAN address on port `9115` failed.

Resolution:

- Used `localhost:9115` from `mon01`.
- Confirmed local access is sufficient because Prometheus and Blackbox Exporter run on the same VM.

Operational lesson:

- A service can be healthy while listening only locally.
- Local-only access is preferable when no remote host needs the endpoint.

### Layered Probe Validation

The DNS probe was tested manually before being added to Prometheus.

Operational lesson:

1. Validate the exporter service.
2. Validate the probe module directly.
3. Add the Prometheus scrape job.
4. Validate PromQL results.
5. Add or update dashboard panels.

This sequence narrows failures to a specific layer.

## Security Considerations

- Keep Blackbox Exporter internal-only.
- Do not expose port `9115` to untrusted networks.
- Do not publish exact probe targets or internal addresses when unnecessary.
- Treat probe configuration as infrastructure-revealing information.
- Avoid probing external systems aggressively or without a clear operational reason.
- Keep intentional security-lab probes isolated from trusted infrastructure.

## Backup Strategy

Blackbox Exporter is mostly stateless.

Important state:

- `/etc/prometheus/blackbox.yml`
- Prometheus scrape configuration for blackbox jobs
- Grafana panels based on probe metrics
- Documentation in this repository

Until Project 003 is implemented, the service is rebuildable but its configuration is not protected by a validated backup process.

## Recovery Procedure

If DNS probing stops working:

1. Check service status:

   ```bash
   systemctl status prometheus-blackbox-exporter
   ```

2. Confirm the exporter responds locally:

   ```bash
   curl localhost:9115/metrics
   ```

3. Run the probe manually:

   ```bash
   curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
   ```

4. Run with debug output if required:

   ```bash
   curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53&debug=true'
   ```

5. Confirm Prometheus has the `blackbox_dns` job and query result:

   ```promql
   probe_success{job="blackbox_dns"}
   ```

6. Validate Prometheus configuration before restarting it:

   ```bash
   promtool check config /etc/prometheus/prometheus.yml
   ```

7. Confirm Grafana resumes displaying current probe data.

## Maintenance Notes

- Keep the package updated through normal Debian patching.
- Revalidate probes after DNS, routing, firewall, or upstream-resolver changes.
- Add new probes intentionally and document exactly what each probe proves.
- Avoid alerts until failure-response procedures are documented.
- Keep dashboard labels aligned with the actual probe scope.

## Future Improvements

- Add a local-record DNS probe to isolate internal DNS health.
- Add HTTP probes for future internal web services.
- Add ICMP or TCP probes for critical infrastructure only where they answer a defined operational question.
- Add alerting after failure thresholds and response runbooks are established.
- Back up Blackbox and Prometheus configuration under Project 003.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Grafana Service](grafana.md)
- [Node Exporter Service](node-exporter.md)
- [Pi-hole Service](pihole.md)
- [Prometheus Scrape Target Troubleshooting](../runbooks/prometheus-scrape-target-troubleshooting.md)
