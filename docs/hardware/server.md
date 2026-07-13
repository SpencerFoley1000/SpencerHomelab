# Lenovo ThinkPad E16 Gen 1 Proxmox Host

## Purpose

The Lenovo ThinkPad E16 Gen 1 is the active virtualization server for the homelab. It runs Proxmox VE and currently hosts the stable DNS and monitoring workloads.

This page documents the server role at a hardware level. Virtualization design, workload placement, platform operations, and architecture decisions are documented separately.

## Current Role

| Area | Details |
| --- | --- |
| Device | Lenovo ThinkPad E16 Gen 1 business laptop |
| Public hostname | `pve01` |
| Device role | Active virtualization host |
| Platform | Proxmox VE `9.2.2` on Debian 13 Trixie |
| CPU | 13th Gen Intel Core i5-1335U, 10 cores |
| Memory | 16 GB RAM |
| Storage | 1 TB PCIe SSD |
| Current status | Active / monitored |
| Management | Internal-only; exact endpoint omitted |
| Administrative model | Named routine administrator and root break-glass path, both protected with TOTP and independent recovery keys |
| Monitoring | Node Exporter, Prometheus, and Grafana |
| Backup maturity | Project 003A readiness complete; protected VM backups and restore testing pending |
| Current workloads | `dns01` and `mon01` |

## Responsibilities

The server currently supports:

- Proxmox host management.
- VM lifecycle and resource allocation.
- `dns01`, the Pi-hole DNS VM.
- `mon01`, the monitoring and observability VM.
- QEMU Guest Agent integration for stable guests.
- Linux host monitoring through Node Exporter.
- The active foundation for Project 003 backup and restore implementation.

The server may later retain one of several roles after the future X299 server is validated:

- Primary host.
- Secondary Proxmox node.
- Recovery or lower-priority workload host.
- Temporary migration source.

The final role must be documented through an ADR rather than assumed.

## Design Decision

The homelab uses a business-class laptop as its initial Proxmox host instead of enterprise rack hardware.

This was an intentional first-phase tradeoff:

- Lower power consumption than typical rack servers.
- Quiet operation suitable for a home environment.
- Enough CPU, memory, and SSD capacity for early infrastructure workloads.
- Lower complexity while networking, monitoring, recovery, and documentation foundations were established.
- Integrated battery provides limited ride-through during brief power interruptions, although it is not a replacement for a proper UPS.
- Proxmox provides practical experience with virtualization, capacity planning, management-plane security, and VM recovery.

The decision and its tradeoffs are recorded in [ADR-0001](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md).

## Capacity and Monitoring

Node Exporter is installed directly on `pve01` and Prometheus scrapes it from `mon01`.

Current visibility includes:

- CPU utilization.
- Memory availability and utilization.
- Filesystem capacity.
- Disk and network activity.
- Boot time and uptime.
- Exporter reachability.

Current boundary:

- Node Exporter shows Linux operating-system health.
- It does not provide authoritative Proxmox VM, storage-pool, task, cluster, replication, or backup-job state.

The current host remains suitable for the deployed foundation, but 16 GB memory and local storage are the main growth constraints. The future X299 system is intended to provide more capacity after it passes validation.

## Hardware Documentation Boundaries

Do not publish:

- Serial numbers.
- Asset tags.
- Warranty identifiers.
- Exact management IP addresses.
- MAC addresses.
- BIOS identifiers.
- Screenshots showing sensitive values.
- Passwords, TOTP seeds, recovery keys, tokens, SSH private keys, or private backup identifiers.

Use placeholders:

- `<PVE01_IP>`
- `<MGMT_NETWORK>`
- `<VM_STORAGE>`
- `<BACKUP_TARGET>`
- `<SERIAL_REDACTED>`

## Network Placement

The server is connected to the homelab network through the TP-Link TL-SG108E managed switch.

Current model:

- Proxmox management is internal-only.
- Stable VMs connect to the homelab LAN.
- `mon01` reaches Node Exporter on TCP `9100` through the existing trusted path.
- The Proxmox firewall was active when monitoring was validated; no unnecessary broad rule was added.

Future documentation should describe:

- Sanitized bridge roles.
- Management-network placement.
- VLAN-aware configuration if implemented.
- Which VM networks are trusted, experimental, or isolated.
- The network relationship between the ThinkPad and future server.

## Storage Notes

The host currently has a 1 TB PCIe SSD containing the Proxmox system and local VM storage.

Project 003 will add a separate 5 TB external backup target. The external drive must not be treated as operational backup infrastructure until it is mounted, registered in Proxmox, scheduled, validated, and used for a successful restore test.

Storage documentation should record:

- Sanitized storage-pool roles.
- VM disk placement.
- ISO and template storage.
- Backup target and retention.
- Capacity thresholds.
- Restore-test results.

## Power Considerations

The laptop battery offers limited short-interruption protection but does not provide:

- Coordinated guest shutdown.
- Runtime monitoring across all lab equipment.
- Replaceable UPS battery maintenance.
- Protection for the switch, router, external backup drive, or future server.

Project 005 will measure the lab's actual power demand and introduce a correctly sized UPS, monitoring, and graceful-shutdown behavior.

## Security Considerations

- Do not expose Proxmox management directly to the internet.
- Use the named routine administrator for normal Proxmox management.
- Reserve the root identity for break-glass and root-only operations.
- Keep TOTP seeds, passwords, QR codes, and recovery keys outside Git.
- Keep administrative access limited to trusted devices and future management networks.
- Document privileged containers or unusual VM permissions.
- Keep security-lab workloads isolated from trusted infrastructure.
- Review host updates and reboots as planned maintenance.
- Keep Node Exporter internal-only.

## Maintenance Notes

Future tested maintenance procedures should include:

- Proxmox release and package review.
- Backup checks before major changes.
- VM shutdown and startup order.
- Host reboot expectations.
- Node Exporter and Prometheus validation.
- `dns01` and `mon01` service validation.
- TOTP and NTP validation after major platform changes.
- Management-access recovery.
- Hardware changes such as memory, storage, or network upgrades.

## Recovery Considerations

Current recovery order:

1. Restore physical network connectivity.
2. Restore Proxmox management access.
3. Restore `dns01` and validate recursive and local DNS.
4. Restore `mon01` and validate Prometheus, both Blackbox jobs, and Grafana.
5. Confirm monitoring observes all restored systems.

Current recovery assets include:

- Sanitized repository documentation.
- Protected Pi-hole Teleporter export.
- Protected Grafana dashboard exports and data-source mapping.
- Prometheus and Blackbox Exporter configuration inventory.
- Planned Proxmox VM backups to the 5 TB external target.

VM recovery remains unproven until Project 003 completes a representative restore test.

## Future Improvements

- Document the sanitized Proxmox bridge and storage layout.
- Complete backup scheduling, retention, and restore validation.
- Add Proxmox platform-specific metrics beyond Node Exporter.
- Add a tested Proxmox maintenance and management-access recovery runbook.
- Review SSH authentication and root-login policy after console recovery is documented.
- Measure idle, startup, and workload power consumption.
- Integrate the host into Project 005 UPS monitoring and graceful shutdown.
- Decide the ThinkPad's long-term role after the future server passes validation.

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
- [Project 003](../projects/project-003-backup-recovery.md)
