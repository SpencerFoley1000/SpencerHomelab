# Hardware Inventory

## Purpose

This document provides a sanitized inventory of the physical devices used, acquired, or intentionally planned for the homelab. It supports planning, troubleshooting, capacity review, recovery design, and future expansion.

The inventory focuses on device roles and architecture impact rather than publishing sensitive identifying information.

## Current Inventory

| Device | Role | Current status | Notes |
| --- | --- | --- | --- |
| Lenovo ThinkPad E16 Gen 1 | Former Proxmox host; current endpoint | Retired from server role | Initial `pve01` platform; returned to general endpoint use after Project 005 |
| TP-Link TL-SG108E Easy Smart Switch | Managed wired switching and future VLAN support | Active / stock firmware | Current Layer 2 switching foundation for lab connectivity |
| GL.iNet GL-SFT1200 Opal | Homelab router and upstream boundary | Active / stock firmware | Routes the homelab through upstream household Wi-Fi |
| X299 virtualization server | Primary Proxmox host, `pve01` | Active and monitored | ASRock X299M Extreme4, Intel Core i7-7800X, 32 GB DDR4, Noctua NH-U12S, Radeon R7 350, 500 W PSU, and NZXT H510 chassis |
| Two 1 TB NVMe devices | Available expansion storage | Available; production role pending | Storage topology will be selected only when a documented requirement exists |
| 5 TB external hard drive | Dedicated Project 003 Proxmox backup target | Active and validated | ext4, UUID-mounted, backup-only Proxmox storage; SMART and extended self-test passed; backs up `dns01` and `mon01` |
| UPS | Power resilience, monitoring, and graceful shutdown | Acquired; integration planned under Project 006 | Implementation follows Project 005 server completion |
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

## X299 Server Known Limitation

The acquired ASRock X299M Extreme4 has one known nonfunctional inner DIMM slot.

Current evidence:

- The seller provided BIOS validation showing the Intel Core i7-7800X and 32 GB memory detected.
- Dual-channel memory operation was shown during that validation.
- The board has four total DIMM slots, leaving three physically usable slots if the reported defect is accurate.

Operational implications:

- The system is suitable for the initial 32 GB configuration if local testing confirms stability.
- Future memory expansion must account for the failed slot and supported memory topology.
- The production system uses the verified working-slot arrangement.
- Future memory changes require renewed detection, stability, and thermal validation.

See [X299 Virtualization Server](server-build.md) for the production configuration and maintenance requirements.

## Sanitized Device Naming

Public documentation should refer to systems by role or safe model name instead of personal or identifying names.

Suggested labels:

- `pve01` - Current X299 Proxmox host.
- `initial-pve-host` - Historical reference to the ThinkPad's former server role.
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

- The X299 server is the active and sole Proxmox host.
- The TP-Link switch remains the current managed switching platform.
- The Opal remains the current homelab routing boundary.
- The ThinkPad is not a backup hypervisor or cluster node.
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

- Continue observing X299 temperatures and stability under production workloads.
- Record the selected storage layout if the two 1 TB NVMe devices enter production use.
- Add measured idle, startup, and load power consumption.
- Select and document the UPS after load measurement.
- Add lifecycle and maintenance history for major devices.
- Complete Project 006 UPS monitoring and graceful shutdown.
- Evaluate a second backup copy in a separate failure domain.

## Related Documentation

- [Initial Proxmox Host](server.md)
- [X299 Virtualization Server](server-build.md)
- [Switch](switch.md)
- [Router](router.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Architecture Overview](../architecture/overview.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [ADR-0005: Migrate pve01 to the X299 Server](../decisions/ADR-0005-migrate-pve01-to-x299-server.md)
- [Roadmap](../../ROADMAP.md)
