# Blackbox Exporter

## Status

Active

## Purpose

Blackbox Exporter performs service-level probes for the homelab monitoring stack. Unlike Node Exporter, which reports host metrics from inside a Linux system, Blackbox Exporter checks whether a service is reachable and responding correctly from the monitoring system's point of view.

The first deployed probe checks whether `dns01` answers DNS queries.

Blackbox Exporter helps answer operational questions such as:

- Is the DNS service reachable?
- Is `dns01` actually answering DNS queries, not just powered on?
- Can Prometheus detect service-level failures before users notice them?
- Which service should be investigated first during an outage?

## Technology Stack

| Component | Value |
| --- | --- |
| Service | Blackbox Exporter |
| Package | `prometheus-blackbox-exporter` |
| Host | `mon01` |
| Operating System | Debian 13.5 |
| Deployment Method | Debian package repository |
| Default Port | `9115/tcp` |
| Configuration File | `/etc/prometheus/blackbox.yml` |
| Current Consumer | Prometheus on `mon01` |

## Host

Blackbox Exporter is installed on:

| Hostname | Role |
| --- | --- |
| `mon01` | Dedicated monitoring VM |

Blackbox Exporter runs on the monitoring VM so probes reflect the monitoring system's ability to reach services across the homelab network.

## Current Probes

| Probe | Target | Protocol | Purpose | Status |
| --- | --- | --- | --- | --- |
| `dns_udp` | `<DNS01_IP>:53` | UDP DNS | Confirm `dns01` answers DNS queries | Active |

Exact IP addresses are intentionally omitted from public documentation. Use placeholders such as `<DNS01_IP>` and `<MON01_IP>`.

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

The DNS probe was then validated manually before Prometheus was configured to scrape it:

```bash
curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53'
```

The successful validation result was:

```text
probe_success 1
```

## Configuration

Blackbox Exporter modules are configured in:

```text
/etc/prometheus/blackbox.yml
```

The initial DNS module is documented in sanitized form:

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

Prometheus scrapes the probe through a dedicated `blackbox_dns` job. Prometheus talks to Blackbox Exporter locally on `mon01`, and Blackbox Exporter performs the probe against `dns01`.

```text
Prometheus -> localhost:9115 Blackbox Exporter -> <DNS01_IP>:53
```

## Networking

| Item | Value |
| --- | --- |
| Listen Port | `9115/tcp` |
| Access Scope | Local/internal monitoring only |
| Public Exposure | None |
| Current Probe Target | `<DNS01_IP>:53` |
| Intended Consumer | Prometheus on `mon01` |

Blackbox Exporter does not need to be exposed publicly. Prometheus and Blackbox Exporter currently run on the same VM, so Prometheus can scrape it through `localhost:9115`.

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

Expected result:

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

## Troubleshooting Notes

### Probe Endpoint Not Reachable on LAN IP

During validation, Blackbox Exporter was active but a probe request to the `mon01` LAN IP on port `9115` failed.

Resolution:

- Used `localhost:9115` from `mon01` instead.
- Confirmed that local access is sufficient because Prometheus and Blackbox Exporter both run on `mon01`.

Operational lesson:

- A service can be healthy while only listening locally.
- Local-only access is preferable when no other host needs to reach the exporter directly.

### Probe Succeeds Manually Before Prometheus Scrape

The DNS probe was tested manually before being added to Prometheus.

Operational lesson:

- Validate the exporter and probe module directly before adding Prometheus scrape configuration.
- This keeps troubleshooting layered: service first, probe second, Prometheus scrape third, dashboard fourth.

## Security Considerations

- Keep Blackbox Exporter internal-only.
- Do not expose port `9115` to untrusted networks.
- Do not publish exact probe targets, internal IP addresses, or private service names when unnecessary.
- Treat probe configuration as infrastructure-revealing information.
- Avoid probing external systems aggressively or without a clear operational reason.

## Backup Strategy

Blackbox Exporter is mostly stateless. Important state is configuration and documentation.

Important state:

- `/etc/prometheus/blackbox.yml`
- Prometheus scrape configuration for blackbox jobs
- Documentation in this repository

Until backup infrastructure is deployed, Blackbox Exporter should be treated as rebuildable but its configuration should be documented and eventually backed up.

## Recovery Procedure

If DNS probing stops working:

1. Check Blackbox Exporter service status:

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

4. If needed, run with debug output:

   ```bash
   curl 'http://localhost:9115/probe?module=dns_udp&target=<DNS01_IP>:53&debug=true'
   ```

5. Confirm Prometheus scrape health:

   ```promql
   probe_success{job="blackbox_dns"}
   ```

6. Validate Prometheus configuration before restarting Prometheus:

   ```bash
   promtool check config /etc/prometheus/prometheus.yml
   ```

## Maintenance Notes

- Keep the package updated through normal Debian patching.
- Revalidate probes after DNS, routing, or firewall changes.
- Add new probes intentionally and document what each one proves.
- Avoid adding alerts until probe failures have clear runbooks.

## Future Improvements

- Add Grafana panels for DNS probe success and latency.
- Add DNS checks for local homelab records, not only public names.
- Add HTTP probes for future web services.
- Add ICMP or TCP probes for critical infrastructure where appropriate.
- Add alerting only after failure response procedures are documented.

## Related Documentation

- [Project 002: Monitoring and Observability Stack](../projects/project-002-monitoring-observability.md)
- [Monitoring and Observability Architecture](../architecture/monitoring.md)
- [Prometheus Service](prometheus.md)
- [Grafana Service](grafana.md)
- [Node Exporter Service](node-exporter.md)
- [Pi-hole Service](pihole.md)
