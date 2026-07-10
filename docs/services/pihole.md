# Pi-hole DNS Service

## Purpose

Pi-hole provides DNS resolution, DNS-based blocking, and local hostname resolution for the homelab LAN.

This is the first production-style infrastructure service deployed in the homelab. Its primary architectural value is foundational DNS for current and future systems rather than ad blocking alone.

## Status

| Field | Value |
| --- | --- |
| Lifecycle state | Active |
| Service role | Internal DNS and DNS filtering |
| Hostname | `dns01` |
| Internal DNS name | `dns01.lab` |
| Exposure | Internal homelab LAN only |
| Public access | None |
| Backup maturity | Live configuration inventoried; Teleporter export created, integrity-checked, and privately inspected; VM backup and restore validation pending |
| Monitoring | Node Exporter host metrics and Blackbox DNS availability probe |

## Technology Stack

| Component | Details |
| --- | --- |
| Application | Pi-hole Core v6.4.3 |
| Web interface | Pi-hole Web v6.6 |
| DNS engine | Pi-hole FTL v6.7 |
| Host metrics | Node Exporter package version `1.9.0-1+b4` |
| Operating system | Debian 13.5 (Trixie) |
| Platform | Proxmox VE virtual machine |
| Deployment method | Official Pi-hole installer |
| Upstream DNS | Cloudflare DNS selected during initial deployment |
| Local DNS zone | `lab` |

Versions were verified during the Project 003 backup-readiness inventory.

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

The household network is an upstream dependency, not managed homelab infrastructure. The GL.iNet Opal router creates the current homelab boundary.

Pi-hole currently serves systems that are manually configured to use it. Router-provided DNS remains deferred until secondary DNS and tested recovery procedures exist.

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
| IP assignment | Static address using Debian `ifupdown` |
| Network interface | `ens18` |
| Network configuration | `/etc/network/interfaces` |
| Guest agent | QEMU Guest Agent installed and running |

Exact private addresses are intentionally omitted. Use `<DNS01_IP>` and `<LAB_GATEWAY>` in public documentation.

## Verified Service and Network Baseline

| Item | Verified state |
| --- | --- |
| Pi-hole systemd unit | `/etc/systemd/system/pihole-FTL.service` |
| Pi-hole unit overrides | None detected |
| Pi-hole service state | Active, running, and enabled |
| Node Exporter systemd unit | `/usr/lib/systemd/system/prometheus-node-exporter.service` |
| Node Exporter unit overrides | None detected |
| Node Exporter service state | Active, running, and enabled |
| Static network file | `/etc/network/interfaces` |
| Addressing model | Static `/24` address with a homelab gateway |
| Host DNS resolvers | Public resolvers configured in the interface definition |

The operating system resolver does not depend on Pi-hole itself. This reduces circular dependency during Pi-hole failure or troubleshooting. The tradeoff is that DNS queries originating from `dns01` bypass Pi-hole filtering.

## DNS Role

Pi-hole handles two DNS responsibilities:

1. **External DNS forwarding**
   - Clients send public-domain queries to Pi-hole.
   - Pi-hole checks blocklists and local records.
   - Allowed queries are forwarded to the configured upstream resolver.

2. **Internal DNS records**
   - Infrastructure receives readable names such as `dns01.lab` and `pve01.lab`.
   - Future services should receive a DNS record during deployment.

## Local DNS Records

Initial sanitized records include:

| Record | Purpose |
| --- | --- |
| `dns01.lab` | Pi-hole / DNS server |
| `pve01.lab` | Proxmox host |
| `switch01.lab` | Managed switch |

Avoid records that expose personal names, exact locations, ISP details, or other identifying information.

## Deployment Notes

1. Created a Debian 13.5 VM in Proxmox.
2. Installed a minimal headless system with SSH.
3. Configured a non-root administrative user with `sudo`.
4. Installed and verified QEMU Guest Agent.
5. Configured a static address using Debian `ifupdown`.
6. Corrected resolver configuration after static networking initially left `/etc/resolv.conf` incomplete.
7. Installed Pi-hole with the official installer.
8. Selected Cloudflare as the upstream resolver.
9. Added initial local DNS records.
10. Verified local and public resolution from another client.
11. Installed Node Exporter.
12. Added a Blackbox Exporter DNS probe from `mon01`.

## Validation

Validated operating state:

- VM reachable on the homelab LAN.
- QEMU Guest Agent running.
- Pi-hole dashboard reachable internally.
- Pi-hole FTL active and enabled.
- Local DNS records resolving from a separate client.
- Public DNS resolution working through Pi-hole.
- Node Exporter active and enabled.
- Node Exporter scraped by Prometheus.
- Blackbox DNS probe returning `probe_success 1`.
- Grafana displaying DNS service-health data.

Useful checks:

```bash
systemctl is-active pihole-FTL prometheus-node-exporter
systemctl is-enabled pihole-FTL prometheus-node-exporter
pihole status
```

From a client configured to use Pi-hole:

```text
nslookup dns01.lab <DNS01_IP>
nslookup pve01.lab <DNS01_IP>
```

## Monitoring

| Layer | Tool | What It Proves |
| --- | --- | --- |
| Host | Node Exporter | `dns01` is reachable and Linux host metrics are available |
| Service | Blackbox Exporter | The DNS endpoint answers the configured query from `mon01` |

Current Prometheus queries:

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

The Blackbox probe currently queries a public name, so it validates the full recursive-resolution path through Pi-hole and the upstream resolver. A future local-record probe should isolate internal DNS health from upstream failures.

## Security Considerations

- Pi-hole remains internal-only.
- Administrative credentials belong in a password manager, not Git.
- Query logs are sensitive because they may reveal browsing behavior.
- Local DNS records must avoid personally identifying names.
- Management and exporter endpoints must remain on trusted networks.
- Raw `/etc/pihole/` contents must not be committed.
- Teleporter archives must remain outside Git.
- Extracted inspection copies require the same protection as the original archive.
- Authentication-related fields, including TOTP material, must never be printed or published.

## Backup Strategy

### Verified Application State

| Item | Verified state |
| --- | --- |
| Primary Pi-hole state directory | `/etc/pihole/` |
| Approximate state size | 16 MB during inventory |
| Pi-hole versions | Core v6.4.3, Web v6.6, FTL v6.7 |
| Pi-hole FTL | Active and enabled |
| Node Exporter | Active and enabled; package version `1.9.0-1+b4` |
| Network configuration | `/etc/network/interfaces` |
| Teleporter export | `pi-hole_dns01_teleporter_2026-07-09_22-27-17_MST.zip`; 23,868 bytes; stored outside Git |
| Archive integrity | Pass |
| Archive entries | 5; 123,439 bytes uncompressed |
| SHA-256 | Recorded privately |

`/etc/pihole/` contains a mixture of configuration, gravity data, local DNS state, query-history databases, active SQLite state, authentication material, and generated files. A raw live directory copy is therefore not the preferred portable recovery method.

### Teleporter Inspection Results

The protected archive was inspected without printing matched values.

| Category | Result |
| --- | --- |
| Database files | `etc/pihole/gravity.db` and `etc/pihole/pihole-FTL.db` |
| Other file types | One `.leases`, one `.toml`, and one extensionless entry |
| Private IPv4 references | 24 |
| URL references | 7 |
| MAC-address references | 2 |
| Email-address references | 0 |
| Sensitive property names | `totp_secret` |
| Key or certificate entries | None detected by filename classification |
| Integrity errors | None |

The counts demonstrate why the archive must remain private. No private IP addresses, MAC addresses, URLs, lease values, database contents, or TOTP values were added to the repository.

### Backup Layers

1. **Proxmox VM backup**
   - Fastest whole-system recovery path.
   - Not considered reliable until a restore succeeds.

2. **Pi-hole Teleporter export**
   - Portable application-level configuration recovery.
   - Original ZIP remains intact in protected storage outside Git.
   - Archive integrity and private content classification are complete.

3. **Sanitized recovery documentation**
   - Records versions, configuration locations, dependencies, network assumptions, and validation steps.
   - Excludes credentials, exact private addresses, query history, and authentication values.

## Recovery Procedure

1. Confirm the VM is powered on in Proxmox.
2. Confirm network connectivity to `dns01`.
3. Check `/etc/network/interfaces` if static addressing or gateway configuration is missing.
4. Check service state:

   ```bash
   sudo systemctl status pihole-FTL
   sudo systemctl status prometheus-node-exporter
   pihole status
   ```

5. Test DNS directly from `mon01` or another client.
6. Temporarily use a public resolver on affected clients if DNS is unavailable.
7. Restore a validated VM backup when available.
8. For a manual rebuild, recreate Debian networking, reinstall Pi-hole and Node Exporter, and import the protected Teleporter export.
9. Confirm upstream settings and required local records.
10. Revalidate public resolution, local records, Node Exporter, Blackbox DNS probing, and Grafana panels.

This remains a draft recovery baseline until exercised during a controlled restore test.

## Maintenance Notes

- Apply Debian and Pi-hole updates during planned maintenance windows.
- Record major version changes that could affect export compatibility.
- Create a new Teleporter export after meaningful DNS-record, blocklist, authentication, or service-configuration changes.
- Retain the most recent known-good export in protected storage.
- Record a SHA-256 hash privately for each retained export.
- Document new local records when services are deployed.
- Confirm monitoring after DNS, firewall, or network changes.
- Avoid router-wide Pi-hole assignment until secondary DNS and recovery procedures exist.

## Troubleshooting Notes

- Hardware virtualization required firmware enablement before Proxmox could start VMs.
- `sudo` access required manual correction after Debian created a separate root account.
- QEMU Guest Agent required Proxmox-side enablement and a full VM stop/start.
- Static networking initially left resolver configuration incomplete.
- The generated Teleporter artifact used ZIP format; procedures must inspect the actual artifact rather than assume a format.
- The initially recorded Teleporter timestamp was incorrect and was corrected by locating the actual file before inspection.

These issues are retained because they demonstrate realistic systems-administration troubleshooting and the value of verifying artifacts directly.

## Future Improvements

- Validate Teleporter import during a controlled recovery test.
- Decide whether the host-level public resolver bypass should remain the intentional long-term design.
- Configure router DHCP to provide Pi-hole after resilience improves.
- Deploy a secondary DNS server.
- Add a local-record DNS probe.
- Add Pi-hole-specific metrics and Grafana panels.
- Validate VM backup and restore under Project 003.
- Evaluate Unbound or encrypted DNS only after the current operating model is stable.

## Related Documentation

- [Services Index](README.md)
- [Project 001: Pi-hole DNS Service](../projects/project-001-pihole-dns.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Service Configuration Export and Inspection Runbook](../runbooks/service-config-export.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Router Documentation](../hardware/router.md)
- [Security Architecture](../architecture/security.md)
