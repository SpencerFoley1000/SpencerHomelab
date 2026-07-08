# Lenovo ThinkPad E16 Gen 1 Proxmox Host

## Purpose

The Lenovo ThinkPad E16 Gen 1 is the primary virtualization server for the homelab. It runs Proxmox VE and hosts lab workloads, infrastructure services, and future security or systems administration projects.

This page documents the server role at a hardware level. Virtualization design details are documented separately in the architecture section.

## Current Role

| Area | Details |
| --- | --- |
| Device | Lenovo ThinkPad E16 Gen 1 Business Laptop |
| Device role | Primary virtualization host |
| Platform | Proxmox VE |
| CPU | 13th Gen Intel Core i5-1335U, 10-core |
| Memory | 16 GB RAM |
| Storage | 1 TB PCIe SSD |
| Current status | Active / baseline configuration |
| Management | Internal-only management access; exact endpoint omitted |
| Primary responsibility | Run VMs and containers for homelab workloads |

## Responsibilities

The server is expected to support:

- Proxmox host management.
- Virtual machines and containers.
- Core infrastructure services as they are deployed.
- Lab workloads for systems administration and networking practice.
- Future monitoring, backup, and security tooling.
- Isolated security lab workloads after proper network segmentation is implemented.

## Design Decision

The homelab uses a business-class laptop as the initial Proxmox host instead of enterprise rack hardware.

This is an intentional tradeoff for the first phase of the lab:

- Lower power consumption than typical rack servers.
- Quiet operation suitable for a home environment.
- Enough CPU, memory, and SSD capacity for early virtualization workloads.
- Lower complexity while networking, documentation, and service foundations are still being built.
- Integrated battery provides limited protection against brief power interruptions, though it should not be treated as a replacement for a proper UPS long term.

This approach prioritizes practical learning, reliability, and maintainability over building a more expensive or noisy rack environment too early.

## Design Reasoning

Using a dedicated Proxmox host creates a realistic platform for learning infrastructure operations.

Benefits:

- Centralized place to run lab workloads.
- Practice with hypervisor administration.
- Support for snapshots, VM lifecycle management, and resource planning.
- Separation between server workloads and the administrative workstation.
- Foundation for future automation, monitoring, backup, and recovery work.

## Hardware Documentation Boundaries

Do not publish:

- Serial numbers.
- Asset tags.
- Warranty identifiers.
- Exact management IP address if unnecessary.
- Personally identifying hostnames.
- Screenshots showing sensitive values.
- Passwords, tokens, SSH private keys, or recovery material.

Use placeholders:

- `<PROXMOX_HOST_IP>`
- `<MGMT_NETWORK>`
- `<VM_STORAGE>`
- `<BACKUP_TARGET>`
- `<SERIAL_REDACTED>`

## Network Placement

The server is currently connected to the lab network through the TP-Link TL-SG108E managed switch.

Future documentation should describe:

- Management network placement.
- Proxmox bridge layout.
- VLAN-aware configuration if implemented.
- Which VM networks are trusted, experimental, or isolated.
- Security lab boundaries before attacker-style workloads are used.

## Storage Notes

The host currently has a 1 TB PCIe SSD. Storage documentation should use sanitized labels rather than raw device identifiers.

Future storage documentation should include:

- Which storage pool holds VM disks.
- Which storage is used for ISOs and templates.
- Which workloads require backup.
- Which data can be rebuilt from documentation.
- Restore testing results for important workloads.

## Security Considerations

- Do not expose Proxmox management directly to the internet.
- Use strong unique credentials stored outside the repository.
- Keep administrative access limited to trusted devices and future management networks.
- Document privileged containers or unusual VM permissions.
- Keep security lab workloads isolated from trusted infrastructure.
- Review host updates and reboots as planned maintenance.

## Maintenance Notes

Future maintenance records should include:

- Proxmox update process.
- Reboot procedure.
- VM shutdown/startup expectations.
- Backup checks before major changes.
- Recovery steps if the host becomes unreachable.
- Hardware changes such as memory, storage, or network upgrades.

## Recovery Considerations

The server should eventually have a documented recovery process that explains:

- How to rebuild the Proxmox host.
- Where configuration notes are stored.
- How VM backups are restored.
- Which services should be restored first.
- Which workloads are disposable experiments.

## Future Improvements

- Add Proxmox host maintenance runbook.
- Add backup and restore validation notes.
- Add monitoring coverage for host health.
- Add architecture decision record for Proxmox as the virtualization platform.
- Revisit whether memory or storage upgrades are needed as services are added.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
