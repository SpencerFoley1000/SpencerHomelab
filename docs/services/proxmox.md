# Proxmox VE Platform

## Purpose

Proxmox VE is the active virtualization platform for the homelab. It provides the management plane and compute environment for infrastructure virtual machines, including `dns01` and `mon01`.

This page documents Proxmox as an operational platform. Hardware-specific details are documented separately on the server page, while design decisions belong in the virtualization architecture and ADR documentation.

## Status

| Area | Details |
| --- | --- |
| Lifecycle state | Active |
| Platform role | Primary hypervisor and VM management platform |
| Hostname | `pve01` |
| Hardware | Lenovo ThinkPad E16 Gen 1 |
| Management exposure | Internal homelab only |
| Public access | None |
| Version | Not yet recorded in public documentation |
| Backup maturity | Not yet implemented or restore-tested |

The exact management endpoint, internal address, VM IDs, and sensitive configuration values are intentionally omitted.

## Current Workloads

| VM | Role | Status |
| --- | --- | --- |
| `dns01` | Pi-hole DNS and local records | Active |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active |

The [VM Inventory](../architecture/vm-inventory.md) is the source of truth for current virtual machines and resource allocations.

## Platform Responsibilities

Proxmox currently provides:

- VM lifecycle management.
- Virtual CPU, memory, storage, and network allocation.
- Internal management access for the homelab administrator.
- QEMU Guest Agent integration for stable Linux VMs.
- A foundation for future snapshots, backups, templates, containers, and isolated security workloads.

## Dependencies

Proxmox operations currently depend on:

- The Lenovo ThinkPad E16 Gen 1 virtualization host.
- The TP-Link managed switch for wired connectivity.
- The GL.iNet Opal routing boundary.
- Existing upstream household connectivity for internet access and package updates.
- Local storage on the Proxmox host.
- Private credential storage outside the repository.

The VMs can continue running during an upstream internet outage, but package updates and public DNS resolution may be affected.

## Networking

The current network model is intentionally simple:

- The Proxmox management interface is reachable only from the internal homelab network.
- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use static addressing.
- Exact bridge names, addresses, MAC addresses, and VM IDs are not published.
- VLAN-aware bridges and isolated workload networks are planned but not yet implemented as stable architecture.

Future networking documentation should record:

- Bridge layout.
- VLAN-aware configuration.
- Management network placement.
- Allowed workload networks.
- Security lab isolation boundaries.

## Storage

The platform currently uses the host's local 1 TB PCIe SSD.

Public documentation does not yet record the exact Proxmox storage layout. Before storage becomes more complex, document:

- Storage pool roles.
- VM disk placement.
- ISO and template storage.
- Available-capacity thresholds.
- Backup destination and retention.
- Restore-test results.

Until backup infrastructure is deployed and tested, workloads should be considered recoverable only from their service documentation, configuration exports, and manual reconstruction.

## QEMU Guest Agent

QEMU Guest Agent is installed on stable Debian VMs where supported.

The agent improves guest visibility and shutdown behavior, but depends on both:

- The guest package and systemd service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling virtual hardware. See the [QEMU Guest Agent Troubleshooting Runbook](../runbooks/qemu-guest-agent-troubleshooting.md).

## Security Considerations

- Do not expose the Proxmox management interface directly to the internet.
- Use strong, unique administrative credentials stored outside the repository.
- Limit management access to trusted devices and future management networks.
- Keep experimental and attacker-style workloads isolated from trusted infrastructure.
- Do not publish exact management addresses, VM IDs, MAC addresses, storage identifiers, or configuration exports containing sensitive values.
- Treat the Proxmox host as high-value infrastructure because every active VM depends on it.
- Review privileged containers, passthrough devices, and unusual VM permissions before use.

## Backup and Recovery

Backup infrastructure is not yet implemented or validated.

Project 003 should define:

- The backup platform and destination.
- Which VMs are protected.
- Backup frequency and retention.
- Encryption and credential handling.
- Restore order and recovery priorities.
- A representative restore test.

Current recovery priority is:

1. Restore Proxmox management and networking.
2. Restore `dns01` because other services may depend on DNS.
3. Restore `mon01` to regain monitoring visibility.
4. Restore lower-priority or experimental workloads.

## Monitoring

Guest VMs are monitored through Node Exporter and service-specific probes, but the Proxmox host itself does not yet have dedicated monitoring coverage.

Future monitoring should include:

- Host CPU and memory pressure.
- Local storage capacity and health.
- Host uptime and update status.
- VM state.
- Backup job health after Project 003.

The selected monitoring method should be documented before credentials or API access are introduced.

## Maintenance Notes

Routine Proxmox maintenance should eventually have a tested runbook covering:

- Update review and package installation.
- Backup checks before major changes.
- VM shutdown and startup order.
- Host reboot expectations.
- Validation of `dns01` and `mon01` after maintenance.
- Recovery steps if management access is lost.

Record the installed Proxmox version and sanitized storage/bridge layout during the next maintenance review.

## Future Improvements

- Record the installed Proxmox VE version.
- Document the sanitized bridge and storage layout.
- Add Proxmox host monitoring.
- Implement and test VM backups under Project 003.
- Create a Proxmox maintenance runbook.
- Document VLAN-aware networking after segmentation is implemented.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Proxmox Host Hardware](../hardware/server.md)
- [Storage Architecture](../architecture/storage.md)
- [Network Architecture](../architecture/network.md)
- [ADR-0001: Initial Proxmox Host](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md)
