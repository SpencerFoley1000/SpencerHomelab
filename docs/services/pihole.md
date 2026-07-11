# Pi-hole DNS Service

## Status

Active

## Purpose

Pi-hole provides DNS resolution, DNS-based blocking, and local hostname resolution for the homelab LAN. Its main architectural value is foundational DNS for current and future infrastructure rather than ad blocking alone.

## Service Summary

| Field | Value |
| --- | --- |
| Hostname | `dns01` |
| Internal DNS name | `dns01.lab` |
| Exposure | Internal homelab LAN only |
| Public access | None |
| Backup maturity | Teleporter export created, integrity-checked, and privately inspected; VM backup and restore validation pending |
| Host monitoring | Node Exporter |
| Service monitoring | Recursive and local Blackbox DNS probes |

## Technology Stack

| Component | Details |
| --- | --- |
| Pi-hole Core | v6.4.3 |
| Pi-hole Web | v6.6 |
| Pi-hole FTL | v6.7 |
| Node Exporter | `1.9.0-1+b4` |
| Operating system | Debian 13.5 (Trixie) |
| Platform | Proxmox VE virtual machine |
| Deployment method | Official Pi-hole installer |
| Upstream DNS | Cloudflare DNS selected during initial deployment |
| Local DNS zone | `lab` |

Versions were verified during Project 003 backup-readiness work.

## Architecture

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal router
  |
Managed switch
  |
Proxmox host
  |-- dns01: Pi-hole and Node Exporter
  `-- mon01: Prometheus, Grafana, and Blackbox Exporter
```

The household network is an upstream dependency, not managed homelab infrastructure. The Opal creates the current lab boundary.

Pi-hole currently serves selected clients configured manually. Router-provided DNS remains deferred until secondary DNS and tested recovery procedures exist.

## VM Specifications

| Area | Value |
| --- | --- |
| VM name | `dns01` |
| Role | DNS infrastructure |
| OS | Debian 13.5 |
| vCPU | 2 |
| Memory | 2 GB |
| Disk | 20 GB |
| Network | Homelab LAN bridge |
| Addressing | Static through Debian `ifupdown` |
| Interface | `ens18` |
| Network configuration | `/etc/network/interfaces` |
| Guest agent | QEMU Guest Agent active |

Exact private addresses are omitted. Use `<DNS01_IP>` and `<LAB_GATEWAY>` publicly.

## Verified Baseline

| Item | State |
| --- | --- |
| Pi-hole systemd unit | `/etc/systemd/system/pihole-FTL.service` |
| Pi-hole service | Active and enabled |
| Node Exporter unit | `/usr/lib/systemd/system/prometheus-node-exporter.service` |
| Node Exporter service | Active and enabled |
| Static network file | `/etc/network/interfaces` |
| Addressing model | Static `/24` address with homelab gateway |
| Host resolver design | Public resolvers configured for the VM itself |

The operating-system resolver does not depend on Pi-hole. This reduces circular dependency during Pi-hole failure, but DNS queries originating from `dns01` bypass Pi-hole filtering.

## DNS Responsibilities

### External Resolution

- Clients query Pi-hole.
- Pi-hole checks blocklists and local records.
- Allowed public queries are forwarded to the configured upstream resolver.

### Internal Records

Sanitized infrastructure records include:

| Record | Purpose |
| --- | --- |
| `dns01.lab` | Pi-hole DNS server |
| `pve01.lab` | Proxmox host |
| `switch01.lab` | Managed switch |

Avoid records that expose personal names, locations, ISP information, or other identifying context.

## Monitoring

| Layer | Tool | What it proves |
| --- | --- | --- |
| Host | Node Exporter | `dns01` is reachable and Linux host metrics are available |
| Recursive service | Blackbox Exporter `dns_udp` | Public resolution works through Pi-hole and its upstream resolver |
| Local service | Blackbox Exporter `dns_udp_local` | The expected local A record is returned independently of upstream DNS |

Prometheus queries:

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Interpretation:

- Recursive and local up: DNS paths healthy.
- Recursive down, local up: investigate upstream resolver or internet connectivity.
- Recursive up, local down: investigate local-record configuration or answer validation.
- Both down: investigate `dns01`, Pi-hole, routing, firewall policy, or the monitoring path.

The Homelab Infrastructure Overview displays Recursive DNS and Local DNS as separate status values.

## Deployment Summary

1. Created a Debian VM in Proxmox.
2. Installed a minimal headless system with SSH.
3. Configured non-root administration and QEMU Guest Agent.
4. Configured a static address through `ifupdown`.
5. Corrected resolver configuration after static networking initially left `/etc/resolv.conf` incomplete.
6. Installed Pi-hole.
7. Selected the upstream resolver.
8. Added initial local records.
9. Verified public and local resolution from another client.
10. Installed Node Exporter.
11. Added recursive and local Blackbox Exporter probes from `mon01`.

## Validation

Service checks:

```bash
systemctl is-active pihole-FTL prometheus-node-exporter
systemctl is-enabled pihole-FTL prometheus-node-exporter
pihole status
```

Direct client checks:

```text
nslookup dns01.lab <DNS01_IP>
nslookup pve01.lab <DNS01_IP>
```

Verified state:

- Pi-hole FTL active and enabled.
- Local records resolve.
- Public DNS resolves through Pi-hole.
- Node Exporter is scraped by Prometheus.
- Recursive Blackbox probe returns `1`.
- Local Blackbox probe returns one answer record and `probe_success 1`.
- Grafana displays host and both DNS service states.

## Security Considerations

- Keep Pi-hole internal-only.
- Store administrative credentials outside Git.
- Treat query logs as sensitive browsing data.
- Avoid personally identifying local records.
- Keep management and exporter endpoints on trusted networks.
- Do not commit raw `/etc/pihole/` contents.
- Keep Teleporter archives and extracted inspection copies outside Git.
- Never publish authentication-related fields, TOTP material, leases, exact addresses, or query-history databases.

## Backup Strategy

### Verified State

| Item | Verified value |
| --- | --- |
| Primary state directory | `/etc/pihole/` |
| Approximate state size | 16 MB during inventory |
| Network configuration | `/etc/network/interfaces` |
| Teleporter export | Private ZIP outside Git |
| Archive integrity | Pass |
| SHA-256 | Recorded privately |

The Teleporter archive contains databases, leases, private addresses, network identifiers, URLs, and authentication-related state. It must remain private.

### Recovery Layers

1. **Proxmox VM backup**
   - Intended whole-system recovery path.
   - Pending implementation and restore validation.

2. **Pi-hole Teleporter export**
   - Portable application-level recovery artifact.
   - Integrity and private sensitivity inspection complete.
   - Import validation pending.

3. **Sanitized documentation**
   - Records versions, paths, dependencies, and validation procedures.
   - Excludes credentials, exact addresses, query history, and authentication values.

## Recovery Procedure

1. Confirm the VM is powered on and reachable.
2. Check `/etc/network/interfaces` if addressing or gateway configuration is missing.
3. Check Pi-hole and Node Exporter service state.
4. Test local and public DNS directly from `mon01` or another client.
5. Temporarily configure affected clients with a public resolver if necessary.
6. Restore a validated VM backup when available.
7. For a manual rebuild, recreate Debian networking, reinstall Pi-hole and Node Exporter, and import the protected Teleporter archive.
8. Confirm upstream resolver settings and required local records.
9. Revalidate both Blackbox jobs, Node Exporter, and Grafana.

This remains a draft recovery baseline until exercised during a controlled restore.

## Maintenance Notes

- Apply Debian and Pi-hole updates during planned maintenance.
- Record major version changes that may affect export compatibility.
- Create a new Teleporter export after meaningful DNS, blocklist, authentication, or configuration changes.
- Retain the latest known-good export privately and record its hash.
- Document new local records when services are deployed.
- Revalidate recursive and local probes after DNS, firewall, or network changes.
- Avoid router-wide Pi-hole assignment until secondary DNS and recovery procedures exist.

## Troubleshooting Lessons

- Hardware virtualization required firmware enablement before Proxmox could start VMs.
- Debian `sudo` access required manual correction after a separate root account was created.
- QEMU Guest Agent required Proxmox-side enablement and a full VM stop/start.
- Static networking initially left resolver configuration incomplete.
- The generated Teleporter artifact used ZIP format; inspect the actual artifact rather than assuming format or filename.
- Recursive and local probes should remain separate because they represent different failure domains.

## Future Improvements

- Validate Teleporter import during a controlled recovery test.
- Decide whether the VM-level public resolver bypass should remain long term.
- Configure router DHCP to provide Pi-hole after resilience improves.
- Deploy secondary DNS.
- Add Pi-hole-specific metrics and Grafana panels.
- Validate VM backup and restore under Project 003.
- Evaluate Unbound or encrypted DNS after the current operating model is stable.

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
