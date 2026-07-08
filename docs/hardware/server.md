# Primary Virtualization Server

## Purpose

The primary virtualization server is the core compute platform for the homelab. It runs Proxmox and hosts lab workloads, infrastructure services, and future security or systems administration projects.

This page documents the server role at a hardware level. Virtualization design details are documented separately in the architecture section.

## Current Role

| Area | Details |
| --- | --- |
| Device role | Primary virtualization host |
| Platform | Proxmox VE |
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

## Design Reasoning

Using a dedicated Proxmox host creates a realistic platform for learning infrastructure operations.

Benefits:

- Centralized place to run lab workloads.
- Practice with hypervisor administration.
- Support for snapshots, VM lifecycle management, and resource planning.
- Separation between server workloads and the desktop workstation.
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

The server is currently connected to the lab network through the managed switch.

Future documentation should describe:

- Management network placement.
- Proxmox bridge layout.
- VLAN-aware configuration if implemented.
- Which VM networks are trusted, experimental, or isolated.
- Security lab boundaries before attacker-style workloads are used.

## Storage Notes

Current storage details should be documented using sanitized labels rather than raw device identifiers.

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

- Add sanitized hardware specifications.
- Add VM inventory once workloads are deployed.
- Add Proxmox host maintenance runbook.
- Add backup and restore validation notes.
- Add monitoring coverage for host health.
- Add architecture decision record for Proxmox as the virtualization platform.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
