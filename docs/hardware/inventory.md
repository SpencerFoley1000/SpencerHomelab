# Hardware Inventory

## Purpose

This document provides a sanitized inventory of the physical devices used, acquired, or intentionally planned for the homelab. It supports planning, troubleshooting, capacity review, recovery design, and future expansion.

The inventory focuses on device roles and architecture impact rather than publishing sensitive identifying information.

## Current Inventory

| Device | Role | Current status | Notes |
| --- | --- | --- | --- |
| Lenovo ThinkPad E16 Gen 1 | Active Proxmox virtualization host, `pve01` | Active | 13th Gen Intel Core i5-1335U, 16 GB RAM, 1 TB PCIe SSD; hosts `dns01` and `mon01` |
| TP-Link TL-SG108E Easy Smart Switch | Managed wired switching and future VLAN support | Active / stock firmware | Current Layer 2 switching foundation for lab connectivity |
| GL.iNet GL-SFT1200 Opal | Homelab router and upstream boundary | Active / stock firmware | Routes the homelab through upstream household Wi-Fi |
| X299 virtualization server build | Future dedicated virtualization server | Hardware acquired; assembly and validation pending | ASRock X299M Extreme4, Intel Core i7-7800X, 32 GB Crucial DDR4-2133, Noctua NH-U12S, existing 500 W PSU and NZXT H510 chassis |
| Two 1 TB NVMe devices | Planned local storage for the future server | Available; final layout pending | Storage topology must be selected after health and platform validation |
| 5 TB external hard drive | Dedicated Project 003 Proxmox backup target | Active and validated | ext4, UUID-mounted, backup-only Proxmox storage; SMART and extended self-test passed; backs up `dns01` and `mon01` |
| UPS | Power resilience, monitoring, and graceful shutdown | Planned under Project 005 | Selection will follow power measurement and new-server validation |
| Secondary / security-lab system | Potential attacker or isolated test system | Planned / optional | May be used for cybersecurity lab work if performance is acceptable |

## Backup Drive Operational Role

The 5 TB external hard drive is dedicated to backup storage and is not used for primary VM disks.

Validated characteristics:

- Expected capacity confirmed before destructive operations.
- SMART overall-health result passed.
- Extended SMART self-test completed without error.
- ext4 filesystem created for native Linux and Proxmox use.
- Persistent mount configured using a private filesystem UUID.
- Proxmox storage restricted to backup content.
- Mount-point enforcement enabled.
- Initial backups completed for `dns01` and `mon01`.
- A `dns01` whole-VM restore was completed in an isolated temporary VM.

Exact model identifiers, serial numbers, UUIDs, backup volume names, and private mount details remain outside Git.

## Future Server Known Limitation

The acquired ASRock X299M Extreme4 has one known nonfunctional inner DIMM slot.

Current evidence:

- The seller provided BIOS validation showing the Intel Core i7-7800X and 32 GB memory detected.
- Dual-channel memory operation was shown during that validation.
- The board has four total DIMM slots, leaving three physically usable slots if the reported defect is accurate.

Operational implications:

- The system is suitable for the initial 32 GB configuration if local testing confirms stability.
- Future memory expansion must account for the failed slot and supported memory topology.
- The defect must be revalidated locally before the system receives a production role.
- Memory errors, thermal behavior, and stability must be tested before migrating workloads.

See [Future Virtualization Server Build](server-build.md) for the validation plan.

## Sanitized Device Naming

Public documentation should refer to systems by role or safe model name instead of personal or identifying names.

Suggested labels:

- `pve01` - Current Lenovo ThinkPad E16 Gen 1 Proxmox host.
- `<FUTURE_PVE_HOST>` - Future X299 virtualization server until its final hostname and role are approved.
- `switch01` - TP-Link TL-SG108E managed switch.
- `router01` - GL.iNet GL-SFT1200 Opal router.
- `admin-workstation` - Personal workstation used for administration and documentation.
- `sec-lab-client` - Optional security testing endpoint.
- `<BACKUP_TARGET>` - Sanitized label for external Proxmox backup storage.
- `<BACKUP_MOUNT>` - Sanitized backup filesystem mount reference.

## Information to Track Privately

Track the following outside the public repository:

- Serial numbers.
- Warranty information.
- Purchase receipts.
- Exact management IP addresses.
- MAC addresses.
- Credentials and recovery material.
- License keys.
- Asset tags.
- Drive UUIDs and partition identifiers.
- Exact backup artifact names.
- Private hashes for backup and export artifacts.

## Information Safe to Track Publicly

The following can usually be documented safely when sanitized:

- Device model when technically relevant.
- General specifications relevant to architecture.
- Device role.
- Lifecycle state.
- Known hardware limitations.
- Operating system or firmware family.
- Network and storage role.
- Dependencies.
- Backup and recovery expectations.
- Validation results.
- Maintenance responsibilities.
- Lessons learned.

## Current Assumptions

- The ThinkPad remains the active Proxmox host until a documented transition occurs.
- The TP-Link switch remains the current managed switching platform.
- The Opal remains the current homelab routing boundary.
- The future X299 server is not production infrastructure until assembly, hardware testing, thermals, storage, networking, monitoring, backup, and power integration are complete.
- The 5 TB external drive is dedicated backup storage, not primary workload storage.
- The current backup drive is directly attached and does not provide immutable, offline, or off-site protection.
- The administrative workstation is a personal endpoint, not core lab infrastructure, so detailed specifications remain omitted.
- Exact internal addressing and private device identifiers are not required to explain the architecture publicly.

## Maintenance Notes

When hardware changes, update this inventory, the relevant device page, architecture documentation, roadmap, and changelog.

Changes that require documentation include:

- New hardware acquired or placed into service.
- Device retired, replaced, or repurposed.
- Firmware or operating system changed.
- Management address or network role changed.
- Storage added, reformatted, replaced, or reassigned.
- Known hardware fault discovered or resolved.
- Device becomes part of backup, monitoring, authentication, or security infrastructure.
- Power requirements or UPS behavior changes.

Backup drive maintenance should include:

- Periodic SMART review.
- Review after unexpected disconnects or I/O errors.
- Capacity and retention review.
- Restore revalidation after major storage or Proxmox changes.

## Future Improvements

- Record future-server assembly and validation results.
- Record the selected storage layout for the two 1 TB NVMe devices.
- Add measured idle, startup, and load power consumption.
- Select and document the UPS after load measurement.
- Add lifecycle and maintenance history for major devices.
- Create an ADR for the future server's production role.
- Evaluate a second backup copy in a separate failure domain.

## Related Documentation

- [Current Proxmox Host](server.md)
- [Future Virtualization Server Build](server-build.md)
- [Switch](switch.md)
- [Router](router.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Architecture Overview](../architecture/overview.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Roadmap](../../ROADMAP.md)