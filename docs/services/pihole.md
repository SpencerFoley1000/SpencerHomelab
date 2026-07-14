# Pi-hole DNS Service

## Status

Active

## Purpose

Pi-hole provides DNS resolution, DNS-based filtering, and local hostname resolution for the homelab LAN. Its primary architectural value is foundational DNS for infrastructure services.

## Service Summary

| Field | Value |
| --- | --- |
| Hostname | `dns01` |
| Internal DNS name | `dns01.lab` |
| Exposure | Internal homelab LAN only |
| Public access | None |
| Backup maturity | Daily Proxmox backup active; Teleporter export protected; isolated whole-VM restore tested 2026-07-14 |
| Host monitoring | Node Exporter |
| Service monitoring | Recursive and local Blackbox DNS probes |

## Technology Stack

| Component | Details |
| --- | --- |
| Pi-hole Core | v6.4.3 |
| Pi-hole Web | v6.6 |
| Pi-hole FTL | v6.7 |
| Node Exporter | `1.9.0-1+b4` |
| Operating system | Debian 13.5 Trixie |
| Platform | Proxmox VE VM |
| Deployment method | Official Pi-hole installer |
| Upstream DNS | Cloudflare selected during initial deployment |
| Local DNS zone | `lab` |

Versions were verified during Project 003 recovery inventory work.

## Architecture

```text
Clients
  |
  | DNS
  v
dns01 / Pi-hole
  |-- local records and filtering
  `-- upstream resolver for public names

mon01
  |-- Node Exporter scrape of dns01
  |-- recursive DNS probe
  `-- local-record DNS probe
```

The household network remains an upstream dependency. The GL.iNet Opal provides the current homelab boundary.

Pi-hole currently serves selected clients configured intentionally. Router-wide DNS assignment remains deferred until secondary DNS and recovery implications are addressed.

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

Exact private addressing is omitted. Public documentation uses `<DNS01_IP>` and `<LAB_GATEWAY>`.

## Verified Baseline

| Item | State |
| --- | --- |
| Pi-hole unit | `/etc/systemd/system/pihole-FTL.service` |
| Pi-hole service | Active and enabled |
| Node Exporter unit | `/usr/lib/systemd/system/prometheus-node-exporter.service` |
| Node Exporter service | Active and enabled |
| Static network file | `/etc/network/interfaces` |
| Host resolver design | Public resolvers configured for the VM itself |

The operating-system resolver does not depend on Pi-hole. This reduces circular dependency during Pi-hole failure, but queries originating from `dns01` bypass local filtering.

## DNS Responsibilities

### Public Resolution

- Clients query Pi-hole.
- Pi-hole checks local records and filtering policy.
- Allowed public queries are forwarded to the configured upstream resolver.

### Internal Records

Sanitized examples:

| Record | Purpose |
| --- | --- |
| `dns01.lab` | DNS server |
| `pve01.lab` | Proxmox host |
| `switch01.lab` | Managed switch |

Avoid records that expose personal names, locations, ISP information, or identifying context.

## Monitoring

| Layer | Tool | What it proves |
| --- | --- | --- |
| Host | Node Exporter | Linux host metrics are reachable |
| Recursive service | Blackbox `dns_udp` | Public resolution works through Pi-hole and the upstream resolver |
| Local service | Blackbox `dns_udp_local` | The expected internal record is returned independently of upstream DNS |

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

- Recursive and local up: both DNS paths healthy.
- Recursive down, local up: investigate upstream DNS or internet connectivity.
- Recursive up, local down: investigate local-record configuration or answer validation.
- Both down: investigate `dns01`, Pi-hole, networking, firewall policy, or the monitoring path.

## Deployment Summary

1. Created a Debian VM in Proxmox.
2. Installed a minimal headless system with SSH.
3. Configured non-root administration and QEMU Guest Agent.
4. Configured static addressing through `ifupdown`.
5. Corrected resolver configuration after the initial static-network setup.
6. Installed Pi-hole and selected the upstream resolver.
7. Added initial local records.
8. Verified public and local resolution from another client.
9. Installed Node Exporter.
10. Added recursive and local Blackbox probes from `mon01`.
11. Added daily Proxmox backup coverage.
12. Completed an isolated whole-VM restore test.

## Validation

Local service checks:

```bash
systemctl is-active pihole-FTL prometheus-node-exporter
systemctl is-enabled pihole-FTL prometheus-node-exporter
pihole status
```

Client checks:

```text
nslookup dns01.lab <DNS01_IP>
nslookup pve01.lab <DNS01_IP>
```

Expected production state:

- Pi-hole FTL active and enabled.
- Required local records resolve.
- Public DNS resolves through Pi-hole.
- Node Exporter is scraped by Prometheus.
- Recursive and local Blackbox probes return `1`.
- Grafana displays host and both DNS service states.

## Backup Strategy

### Whole-VM Backup

`dns01` is included in the daily Project 003 Proxmox backup job:

- Snapshot mode.
- Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external backup storage with mount-point enforcement.

### Pi-hole Teleporter

A protected Teleporter ZIP provides an application-level recovery path.

Verified properties:

- Archive integrity passed.
- SHA-256 recorded privately.
- Artifact contains databases, leases, network identifiers, URLs, and authentication-related state.
- Archive remains outside Git.
- Independent Teleporter import testing remains future work.

### Documentation

Sanitized documentation records versions, paths, dependencies, rebuild steps, and validation requirements without publishing exact addresses, query history, or credentials.

## Restore Validation

On 2026-07-14, the Proxmox backup was restored to a temporary VM under a different VM ID.

Safety steps:

- The active `dns01` VM was not overwritten.
- The restored copy was renamed as a restore test.
- Its virtual network adapter was removed before boot.

Validated:

- Debian booted to a normal login prompt.
- The expected root filesystem was present.
- `pihole-FTL` reported active.
- Node Exporter reported active.
- The temporary VM was shut down and deleted afterward.

Not validated by the isolated test:

- Client DNS traffic.
- Local-record responses over the network.
- Remote Node Exporter reachability.
- Prometheus target health.
- Blackbox probe success.

Those require an actual replacement recovery or a controlled connected test after the production instance is safely isolated.

## Recovery Procedure

Preferred path:

1. Confirm network, Proxmox, and backup storage availability.
2. Restore the latest appropriate VM backup.
3. Keep the restored copy isolated until duplicate identity risk is eliminated.
4. Confirm Debian, filesystem, Pi-hole FTL, and Node Exporter locally.
5. Review the restored network adapter and protected static configuration.
6. Reconnect only after the original VM cannot conflict.
7. Validate public DNS, local records, Node Exporter, both Blackbox probes, and Grafana.

Manual rebuild path:

1. Deploy supported Debian.
2. Recreate protected static networking.
3. Install Pi-hole and Node Exporter.
4. Import the protected Teleporter archive.
5. Confirm upstream resolver settings and local records.
6. Revalidate host and service monitoring.

See [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md) and [Disaster Recovery](../runbooks/disaster-recovery.md).

## Security Considerations

- Keep Pi-hole internal-only.
- Store administrative credentials outside Git.
- Treat query logs as sensitive browsing data.
- Avoid personally identifying local records.
- Keep exporter and management endpoints on trusted networks.
- Do not commit raw `/etc/pihole/` contents, Teleporter archives, backup artifacts, or inspection copies.
- Never publish authentication fields, leases, exact addresses, drive identifiers, or query-history databases.

## Maintenance Notes

- Apply Debian and Pi-hole updates during planned maintenance.
- Confirm a recent successful VM backup before major changes.
- Create a new Teleporter export after meaningful Pi-hole changes.
- Retain the latest known-good private export and hash.
- Revalidate recursive and local probes after DNS, firewall, or network changes.
- Re-test restoration after major Pi-hole, Debian, Proxmox, or storage changes.
- Avoid router-wide Pi-hole assignment until secondary DNS and recovery design are addressed.

## Troubleshooting Lessons

- Hardware virtualization required firmware enablement before Proxmox could start VMs.
- Debian `sudo` access required correction after a separate root account was created.
- QEMU Guest Agent required Proxmox-side hardware plus a full stop/start.
- Static networking initially left resolver configuration incomplete.
- Teleporter artifact format must be verified from the actual generated file.
- Recursive and local probes represent different failure domains.
- Local service startup and end-to-end DNS behavior are separate recovery validation layers.

## Future Improvements

- Validate Teleporter import during a controlled recovery test.
- Perform a controlled network-connected VM recovery test.
- Decide whether the VM-level public-resolver bypass should remain long term.
- Add Pi-hole-specific application metrics.
- Add secondary DNS before broader client dependence.

## Related Documentation

- [Project 001: Pi-hole DNS](../projects/project-001-pihole-dns.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Storage Architecture](../architecture/storage.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Blackbox Exporter](blackbox-exporter.md)
- [Node Exporter](node-exporter.md)