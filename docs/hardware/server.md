# Lenovo ThinkPad E16 Gen 1 Proxmox Host

## Purpose

The Lenovo ThinkPad E16 Gen 1 is the active virtualization server for the homelab. It runs Proxmox VE and hosts the stable DNS and monitoring workloads.

This page documents the server at the hardware and operational-role level. Platform configuration, workload placement, storage architecture, and design decisions are documented separately.

## Current Role

| Area | Details |
| --- | --- |
| Device | Lenovo ThinkPad E16 Gen 1 business laptop |
| Public hostname | `pve01` |
| Device role | Active virtualization host |
| Platform | Proxmox VE `9.2.2` on Debian 13 Trixie |
| CPU | 13th Gen Intel Core i5-1335U, 10 cores |
| Memory | 16 GB RAM |
| Local storage | 1 TB PCIe SSD |
| Current status | Active, monitored, and backed up at the VM layer |
| Management | Internal-only; exact endpoint omitted |
| Administrative model | Named routine administrator and root break-glass path, both protected with TOTP and independent recovery keys |
| Monitoring | Node Exporter, Prometheus, and Grafana |
| Backup maturity | Daily backups active for `dns01` and `mon01`; isolated `dns01` restore tested 2026-07-14 |
| Current workloads | `dns01` and `mon01` |

## Responsibilities

The host currently provides:

- Proxmox management and VM lifecycle control.
- Compute, memory, storage, and virtual networking for `dns01` and `mon01`.
- QEMU Guest Agent integration for stable guests.
- Linux host monitoring through Node Exporter.
- Scheduled VM backups to dedicated external storage.
- VM restoration through Proxmox tooling.

The ThinkPad may later become the primary host, a secondary node, a recovery host, or a migration source after the future X299 server is validated. That role change requires an ADR.

## Design Decision

A business-class laptop was selected as the first Proxmox host instead of enterprise rack hardware.

Benefits:

- Low power consumption and noise.
- Sufficient early CPU, memory, and SSD capacity.
- Lower operational complexity while core services and documentation matured.
- Integrated battery ride-through for brief interruptions.
- Practical experience with virtualization, monitoring, security, backup, and recovery.

Tradeoffs:

- 16 GB RAM limits persistent workload growth.
- Internal storage and expansion options are limited.
- The battery does not protect the router, switch, backup drive, or future server.
- A laptop is not a substitute for a monitored UPS and coordinated shutdown.

See [ADR-0001](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md).

## Capacity and Monitoring

Node Exporter is installed directly on `pve01` and scraped from `mon01`.

Current visibility:

- CPU utilization and load.
- Memory availability.
- Filesystem capacity.
- Disk and network activity.
- Uptime and exporter reachability.

Node Exporter does not provide authoritative Proxmox VM, storage-pool, task, cluster, replication, or backup-job state. Those require a future least-privilege Proxmox integration.

## Storage

### Local Storage

The internal 1 TB PCIe SSD contains:

- The Proxmox operating system.
- Local VM disks.
- ISOs and templates.
- Active workload state.

### Backup Storage

A dedicated 5 TB external drive provides backup storage.

Implemented controls:

- SMART health passed.
- Extended SMART self-test completed without error.
- ext4 filesystem.
- Persistent UUID-based mount using a private identifier.
- Proxmox backup-only directory storage.
- Mount-point enforcement to prevent fallback writes into the host root filesystem.
- Daily snapshot-mode, Zstandard-compressed backups for `dns01` and `mon01`.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Successful isolated `dns01` restore validation.

The external drive is not primary workload storage. It remains directly attached and does not provide immutable, offline, or off-site protection.

## Network Placement

The host connects through the TP-Link managed switch.

Current model:

- Proxmox management is internal-only.
- Stable VMs connect to the homelab LAN.
- `mon01` reaches Node Exporter through the trusted internal path.
- The Proxmox firewall was active when monitoring was validated.
- No unnecessary broad monitoring rule was added.

Future documentation should describe sanitized bridge roles, management-network placement, VLAN-aware configuration, security-lab isolation, and the relationship between the ThinkPad and future server.

## Power Considerations

The laptop battery offers limited short-interruption protection but does not provide:

- Coordinated VM and host shutdown.
- Runtime or battery-health monitoring.
- Protection for network devices or external storage.
- Replaceable UPS battery maintenance.

Project 005 will measure actual load and implement a correctly sized UPS, monitoring, and graceful shutdown.

## Security Considerations

- Keep Proxmox management internal-only.
- Use the named routine administrator for normal work.
- Reserve root for break-glass and root-only operations.
- Keep credentials, TOTP material, recovery keys, device identifiers, and backup identifiers outside Git.
- Keep security-lab workloads isolated from trusted infrastructure and backup storage.
- Keep Node Exporter internal-only.
- Validate physical-console recovery before tightening remote access further.

## Recovery Considerations

Current recovery order:

1. Restore physical network connectivity.
2. Restore Proxmox management access.
3. Confirm local storage and the external backup target.
4. Restore `dns01` and validate public plus local DNS.
5. Restore `mon01` and validate Prometheus, exporters, and Grafana.
6. Confirm monitoring observes all restored systems.

Current recovery assets:

- Daily full-VM backups for `dns01` and `mon01`.
- Tested isolated `dns01` restore procedure.
- Protected Pi-hole Teleporter export.
- Protected Grafana dashboard exports and data-source mapping.
- Prometheus and Blackbox configuration inventory.
- Sanitized repository documentation.

## Maintenance Notes

Planned maintenance should include:

- Review the Proxmox release and package changes.
- Confirm a recent successful backup before major work.
- Verify the backup target is actually mounted.
- Record VM shutdown and startup order.
- Validate `dns01`, `mon01`, and `pve01` after reboot.
- Confirm TOTP and NTP remain functional.
- Confirm Node Exporter and Prometheus recover.
- Review the next scheduled backup.
- Re-test restoration after major storage, hypervisor, or migration changes.

## Public Documentation Boundaries

Do not publish:

- Serial numbers, asset tags, warranty or BIOS identifiers.
- Exact management addresses or MAC addresses.
- Filesystem UUIDs, backup filenames, or raw task logs.
- Passwords, TOTP seeds, recovery keys, tokens, or private keys.

Use placeholders including `<PVE01_IP>`, `<MGMT_NETWORK>`, `<VM_STORAGE>`, `<BACKUP_MOUNT>`, and `<BACKUP_TARGET>`.

## Future Improvements

- Document sanitized bridge and local-storage layouts.
- Add Proxmox platform, task, storage, and backup metrics.
- Add backup-age and failure alerting with response runbooks.
- Add a tested management-access recovery runbook.
- Review SSH authentication and root-login policy after console recovery is documented.
- Measure idle, startup, and workload power consumption.
- Integrate the host with Project 005 UPS monitoring and graceful shutdown.
- Decide the ThinkPad's long-term role after future-server validation.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Future Virtualization Server Build](server-build.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
- [ADR-0001](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)