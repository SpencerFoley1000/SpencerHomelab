# Hardware Inventory

## Purpose

This document provides a sanitized inventory of the physical devices used in the homelab. It is intended to help with planning, troubleshooting, documentation, and future expansion.

The inventory focuses on device roles and architecture impact rather than publishing sensitive identifying information.

## Current Inventory

| Device | Role | Current Status | Notes |
| --- | --- | --- | --- |
| Lenovo ThinkPad E16 Gen 1 | Primary Proxmox virtualization host | Active / baseline configuration | 13th Gen Intel Core i5-1335U, 16 GB RAM, 1 TB PCIe SSD |
| TP-Link TL-SG108E Easy Smart Switch | Managed wired switching and future VLAN support | Active / stock firmware | Current Layer 2 switching foundation for lab connectivity |
| GL.iNet GL-SFT1200 Opal | Lab router | Active / stock firmware | Serves as the current regular router for the lab; may be repurposed or replaced later |
| Administrative workstation | Documentation and infrastructure administration endpoint | Active | Personal workstation used to manage the lab; hardware specs intentionally omitted |
| Secondary / security lab system | Potential attacker or isolated test system | Planned / optional | May be used for cyber security lab work if performance is acceptable |

## Sanitized Device Naming

Public documentation should refer to systems by role or safe model name instead of personal or identifying names.

Suggested labels:

- `pve01` - Lenovo ThinkPad E16 Gen 1 Proxmox host.
- `switch01` - TP-Link TL-SG108E managed switch.
- `router01` - GL.iNet GL-SFT1200 Opal router.
- `admin-workstation` - Personal workstation used for administration and documentation.
- `sec-lab-client` - Optional security testing endpoint.

## Information to Track Privately

The following should be tracked outside the public repository, such as in a password manager or private inventory:

- Serial numbers.
- Warranty information.
- Purchase receipts.
- Exact management IP addresses if not safe to publish.
- MAC addresses.
- Credentials.
- Recovery codes.
- License keys.
- Asset tags.

## Information Safe to Track Publicly

The following can usually be documented safely when sanitized:

- Device model.
- Device role.
- General hardware class.
- Operating system or firmware family.
- Network role.
- Dependencies.
- Backup and recovery expectations.
- Maintenance responsibilities.
- Lessons learned.

## Current Assumptions

- The Lenovo ThinkPad E16 Gen 1 is the primary compute platform and runs Proxmox VE.
- The TP-Link TL-SG108E is the current managed switch for wired lab connectivity.
- The GL.iNet GL-SFT1200 Opal is currently serving as the lab router using stock firmware.
- The administrative workstation is a personal endpoint, not core lab infrastructure, so detailed hardware specifications are intentionally omitted.
- Exact internal addressing is not required to explain the architecture publicly.
- Hardware documentation will be refined as devices are configured, replaced, or repurposed.

## Maintenance Notes

When hardware changes, update this inventory and the relevant device page.

Examples of changes that should be documented:

- New hardware added.
- Device retired or repurposed.
- Firmware or operating system changed.
- Management address changed.
- Network role changed.
- Storage added or replaced.
- Device becomes part of backup, monitoring, or security infrastructure.

## Future Improvements

- Add firmware version notes if needed without exposing sensitive details.
- Add power and physical placement notes if useful.
- Add lifecycle status for each major device.
- Add maintenance history once hardware updates begin.
- Add a private inventory process for sensitive identifiers.

## Related Documentation

- [Switch](switch.md)
- [Router](router.md)
- [Desktop](desktop.md)
- [Server](server.md)
- [Architecture Overview](../architecture/overview.md)
