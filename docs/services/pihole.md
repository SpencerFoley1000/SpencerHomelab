# Pi-hole DNS Service

## Purpose

Pi-hole provides DNS resolution, DNS-based blocking, and local hostname resolution for the homelab LAN.

This service is the first production-style infrastructure service deployed in the homelab. It exists less as an ad blocker alone and more as a foundational DNS service that future systems can depend on.

## Status

| Field | Value |
| --- | --- |
| Lifecycle state | Active |
| Service role | Internal DNS and DNS filtering |
| Hostname | `dns01` |
| Internal DNS name | `dns01.lab` |
| Exposure | Internal homelab LAN only |
| Public access | None |
| Backup maturity | Rebuildable from documentation; no validated VM backup |
| Monitoring | Node Exporter host metrics and Blackbox DNS availability probe |

## Technology Stack

| Component | Details |
| --- | --- |
| Application | Pi-hole |
| Operating system | Debian 13.5 (Trixie) |
| Platform | Proxmox VE virtual machine |
| Deployment method | Official Pi-hole installer |
| Upstream DNS | Cloudflare DNS selected during initial deployment |
| Local DNS zone | `lab` |

## Architecture

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal travel router
  |
Managed switch
  |
Proxmox host
  |
  |-- dns01: Pi-hole DNS and Node Exporter
  `-- mon01: Prometheus, Grafana, and Blackbox Exporter
```

The household network is treated as an upstream dependency, not as managed homelab infrastructure. The GL.iNet Opal router acts as the homelab edge router and keeps the lab separated from the rest of the household network.

Pi-hole currently provides DNS services for systems that are manually configured to use it. Router-provided DNS remains a future improvement until a secondary DNS path and tested recovery process exist.

## VM Specifications

| Area | Value |
| --- | --- |
| VM name | `dns01` |
| Role | DNS infrastructure |
| OS | Debian 13.5 (Trixie) |
| vCPU | 2 vCPU |
| Memory | 2 GB RAM |
| Disk | 20 GB |
| Network | Homelab LAN bridge |
| IP assignment | Static address on homelab LAN |
| Guest agent | QEMU Guest Agent installed and running |

Exact IP addresses are intentionally omitted. Use `<DNS01_IP>` or private operational notes when the deployed address is required.

## DNS Role

Pi-hole handles two DNS responsibilities:

1. **External DNS forwarding**
   - Clients ask Pi-hole for public domain resolution.
   - Pi-hole checks blocklists and local records.
   - Allowed queries are forwarded to the configured upstream resolver.

2. **Internal DNS records**
   - Homelab systems receive readable names such as `dns01.lab` and `pve01.lab`.
   - This avoids relying on memorized IP addresses for infrastructure access.
   - Future services should receive DNS records as part of deployment.

## Local DNS Records

Initial local DNS records include:

| Record | Purpose |
| --- | --- |
| `dns01.lab` | Pi-hole / DNS server |
| `pve01.lab` | Proxmox host |
| `switch01.lab` | Managed switch |

Only sanitized hostnames should be committed. Avoid names that reveal personal details, exact locations, family names, or ISP information.

## Deployment Notes

High-level deployment flow:

1. Created a Debian 13.5 VM in Proxmox.
2. Installed a minimal headless Debian system with SSH enabled.
3. Configured a non-root administrative user with `sudo` access.
4. Installed and verified QEMU Guest Agent.
5. Converted the VM from DHCP to a static address using Debian `ifupdown` networking.
6. Resolved a DNS issue caused by an empty `/etc/resolv.conf` after static networking was configured.
7. Installed Pi-hole using the official installer.
8. Selected Cloudflare as the upstream DNS provider.
9. Added initial local DNS records for core infrastructure.
10. Verified local and public DNS resolution from another client.
11. Installed Node Exporter for host monitoring.
12. Added a Blackbox Exporter DNS probe from `mon01`.

## Validation

Validation performed after deployment:

- Confirmed the VM is reachable on the homelab LAN.
- Confirmed QEMU Guest Agent is running.
- Confirmed the Pi-hole dashboard is accessible internally.
- Confirmed Pi-hole service status is active.
- Confirmed local DNS records resolve from a separate client.
- Confirmed public DNS resolution works through Pi-hole.
- Confirmed Node Exporter metrics are scraped by Prometheus.
- Confirmed the Blackbox DNS probe returns `probe_success 1`.
- Confirmed the Grafana service-health dashboard shows DNS probe data.

Useful service checks:

```bash
systemctl status pihole-FTL
pihole status
```

From a client configured to use Pi-hole:

```text
nslookup dns01.lab <DNS01_IP>
nslookup pve01.lab <DNS01_IP>
```

## Monitoring

Pi-hole is monitored at two layers:

| Layer | Tool | What It Proves |
| --- | --- | --- |
| Host | Node Exporter | `dns01` is reachable and Linux host metrics are available |
| Service | Blackbox Exporter | The DNS endpoint answers the configured DNS query from `mon01` |

Current Prometheus queries include:

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

The current Blackbox probe queries a public name, so it validates the complete recursive-resolution path through Pi-hole and the configured upstream resolver. A future local-record probe should be added to distinguish internal DNS health from upstream internet or resolver failures.

Pi-hole-specific application metrics such as query volume, blocked domains, and cache behavior are not yet collected.

## Security Considerations

- Pi-hole is internal-only and should not be exposed directly to the internet.
- The admin password must be stored in a password manager, not in the repository.
- Local DNS records should avoid personally identifying names.
- Query logs can reveal browsing behavior and should be treated as sensitive operational data.
- Router, switch, Proxmox, Pi-hole, Prometheus, and Grafana management interfaces should remain reachable only from trusted networks.
- Node Exporter and DNS probe endpoints should not be exposed to untrusted networks.

## Backup Strategy

Current backup maturity is early-stage.

Until Project 003 deploys and validates a backup solution:

- Pi-hole should be considered recoverable from documentation and reinstallation.
- Important configuration should be exported using Pi-hole Teleporter after meaningful changes.
- VM backups should not be described as reliable until a restore has been tested.

Future backup requirements:

- Schedule regular VM backups.
- Export Pi-hole configuration after DNS or blocklist changes.
- Protect exports and credentials outside the public repository.
- Test recovery by restoring to a temporary VM or rebuilding `dns01`.

## Recovery Procedure

If Pi-hole fails:

1. Confirm the VM is powered on in Proxmox.
2. Confirm network connectivity to `dns01`.
3. Check Pi-hole service status:

   ```bash
   sudo systemctl status pihole-FTL
   pihole status
   ```

4. Check the DNS service from `mon01` using the documented Blackbox probe or a direct query.
5. Temporarily point affected clients to a public resolver if DNS service is unavailable.
6. Restore from a validated VM backup when available.
7. If no validated backup exists, rebuild Debian and Pi-hole using this documentation and restore local records from a protected export or private notes.
8. Revalidate Node Exporter, DNS probing, local records, and public resolution.

## Maintenance Notes

Routine maintenance should include:

- Apply Debian and Pi-hole updates during planned maintenance windows.
- Review the Pi-hole dashboard for abnormal query patterns.
- Export Pi-hole configuration after meaningful DNS-record or blocklist changes.
- Document new local DNS records when infrastructure services are deployed.
- Confirm Prometheus and Grafana monitoring after DNS, firewall, or network changes.
- Avoid router-wide DNS changes until secondary DNS and recovery procedures are ready.

## Troubleshooting Notes

Issues encountered during deployment:

- Hardware virtualization was unavailable until virtualization support was enabled in system firmware.
- `sudo` access required manual correction after the Debian installation created a separate root account.
- QEMU Guest Agent required Proxmox-side enablement and a full VM stop/start before working correctly.
- Static networking succeeded, but DNS resolution initially failed because `/etc/resolv.conf` did not contain nameserver entries.

These issues are preserved because they demonstrate realistic systems-administration troubleshooting rather than a clean tutorial path.

## Future Improvements

- Configure the GL.iNet Opal DHCP service to provide Pi-hole as DNS after resilience is improved.
- Deploy a secondary DNS server.
- Add a local-record DNS probe to separate internal DNS health from upstream recursive resolution.
- Add Pi-hole-specific metrics and Grafana panels.
- Add a Pi-hole configuration export runbook.
- Add VM backup and restore validation under Project 003.
- Evaluate Unbound, DNSSEC, DNS-over-HTTPS, or DNS-over-TLS only after the current design is stable and the operational goal is clear.

## Related Documentation

- [Services Index](README.md)
- [Project 001: Pi-hole DNS Service](../projects/project-001-pihole-dns.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Router Documentation](../hardware/router.md)
- [Security Architecture](../architecture/security.md)
