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

## Technology Stack

| Component | Details |
| --- | --- |
| Application | Pi-hole |
| Operating system | Debian 13 |
| Platform | Proxmox virtual machine |
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
dns01 - Pi-hole DNS
```

The household network is treated as an upstream dependency, not as managed homelab infrastructure. The GL.iNet Opal router acts as the homelab edge router and keeps the lab isolated from the rest of the household network.

Pi-hole currently provides DNS services for systems that are manually configured to use it. A future improvement is to configure DHCP on the homelab router so clients automatically receive Pi-hole as their DNS server.

## VM Specifications

| Area | Value |
| --- | --- |
| VM name | `dns01` |
| Role | DNS infrastructure |
| OS | Debian 13 |
| vCPU | 2 vCPU |
| Memory | 2 GB RAM |
| Disk | 20 GB |
| Network | Homelab LAN bridge |
| IP assignment | Static address on homelab LAN |
| Guest agent | QEMU Guest Agent installed and running |

Exact IP addresses are intentionally omitted from public documentation. Use `<DNS01_IP>` or local private notes when an operational runbook requires the deployed address.

## DNS Role

Pi-hole handles two DNS responsibilities:

1. **External DNS forwarding**
   - Clients ask Pi-hole for public domain resolution.
   - Pi-hole checks blocklists and local records.
   - Allowed queries are forwarded to the configured upstream DNS provider.

2. **Internal DNS records**
   - Homelab systems receive readable names such as `dns01.lab` and `pve01.lab`.
   - This avoids relying on memorized IP addresses for infrastructure access.
   - Future services should receive DNS records as part of deployment.

## Local DNS Records

Initial local DNS records were added for core homelab infrastructure.

Examples:

| Record | Purpose |
| --- | --- |
| `dns01.lab` | Pi-hole / DNS server |
| `pve01.lab` | Proxmox host |
| `switch01.lab` | Managed switch |

Only sanitized hostnames should be committed to this repository. Avoid names that reveal personal details, exact locations, family names, or ISP information.

## Deployment Notes

High-level deployment flow:

1. Created a Debian 13 VM in Proxmox.
2. Installed a minimal, headless Debian system with SSH enabled.
3. Configured a non-root administrative user with `sudo` access.
4. Installed and verified the QEMU Guest Agent.
5. Converted the VM from DHCP to a static IP using Debian `ifupdown` networking.
6. Resolved a DNS issue caused by an empty `/etc/resolv.conf` after static networking was configured.
7. Installed Pi-hole using the official installer.
8. Selected Cloudflare as the upstream DNS provider.
9. Added initial local DNS records for core infrastructure.
10. Verified local DNS resolution from another client.

## Validation

Validation performed after deployment:

- Confirmed the VM is reachable on the homelab LAN.
- Confirmed the QEMU Guest Agent is running.
- Confirmed the Pi-hole dashboard is accessible internally.
- Confirmed Pi-hole service status is active.
- Confirmed local DNS records resolve from a separate client.
- Confirmed public DNS resolution works through Pi-hole.

Useful checks:

```bash
systemctl status pihole-FTL
pihole status
```

From a client configured to use Pi-hole:

```text
nslookup dns01.lab <DNS01_IP>
nslookup pve01.lab <DNS01_IP>
```

## Security Considerations

- Pi-hole is internal-only and should not be exposed directly to the internet.
- The admin password must be stored in a password manager, not in the repository.
- Local DNS records should avoid personally identifying names.
- Query logs can reveal browsing behavior and should be treated as sensitive operational data.
- Router, switch, Proxmox, and Pi-hole management interfaces should remain reachable only from trusted homelab networks.

## Backup Strategy

Current backup maturity is early-stage.

Until a dedicated backup solution is deployed:

- Pi-hole should be considered recoverable from documentation and reinstallation.
- Important configuration should be exported using Pi-hole Teleporter after meaningful changes.
- VM backups should be added once Proxmox Backup Server or another backup target is implemented.

Future backup target:

- Schedule regular VM backups.
- Export Pi-hole configuration after DNS or blocklist changes.
- Test restore by rebuilding `dns01` or restoring to a temporary VM.

## Recovery Procedure

If Pi-hole fails:

1. Confirm the VM is powered on in Proxmox.
2. Confirm network connectivity to `dns01`.
3. Check Pi-hole service status:

   ```bash
   sudo systemctl status pihole-FTL
   pihole status
   ```

4. Temporarily point clients to a public DNS resolver if DNS service is unavailable.
5. Restore from VM backup if available.
6. If no backup exists, rebuild Debian and Pi-hole using this documentation, then restore local DNS records from export or notes.

## Maintenance Notes

Routine maintenance should include:

- Apply Debian updates during planned maintenance windows.
- Review Pi-hole dashboard for abnormal query patterns.
- Export Pi-hole configuration after meaningful DNS record or blocklist changes.
- Document new local DNS records when new infrastructure services are deployed.
- Avoid changing router-wide DNS settings until Pi-hole has been stable long enough to rely on.

## Troubleshooting Notes

Issues encountered during deployment:

- Hardware virtualization was unavailable until virtualization support was enabled in system firmware.
- `sudo` access required manual correction after the Debian install path created a separate root account.
- The QEMU Guest Agent required Proxmox-side enablement and a VM restart before working correctly.
- Static networking succeeded, but DNS resolution initially failed because `/etc/resolv.conf` did not contain nameserver entries.

These issues are useful to preserve because they represent realistic systems administration troubleshooting rather than a clean tutorial path.

## Future Improvements

- Configure the GL.iNet Opal DHCP settings to hand out Pi-hole as DNS for homelab clients.
- Deploy a secondary DNS server for resilience.
- Add Unbound as a local recursive resolver.
- Evaluate DNSSEC, DNS-over-HTTPS, or DNS-over-TLS after the basic DNS design is stable.
- Add monitoring for Pi-hole availability and DNS query health.
- Add a Pi-hole configuration export runbook.
- Add VM backup and restore validation once backup infrastructure is deployed.

## Related Documentation

- [Services Index](README.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Router Documentation](../hardware/router.md)
- [Security Architecture](../architecture/security.md)
