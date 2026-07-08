# Hardware Inventory

## Purpose

This document provides a sanitized inventory of the physical devices used in the homelab. It is intended to help with planning, troubleshooting, documentation, and future expansion.

The inventory focuses on device roles and architecture impact rather than publishing sensitive identifying information.

## Current Inventory

| Device | Role | Current Status | Notes |
| --- | --- | --- | --- |
| Primary virtualization server | Proxmox host for lab workloads | Active / baseline configuration | Core compute platform for the lab |
| Managed switch | Wired lab connectivity and future VLAN support | Active / baseline configuration | Management address is intentionally sanitized |
| Router / upstream gateway | Internet access and routing boundary | Existing dependency / future improvement | Long-term router/firewall design is still planned |
| Desktop workstation | Administration and lab interaction | Active | Used for documentation, GitHub work, management access, and future lab tasks |
| Secondary / security lab system | Potential attacker or isolated test system | Planned / optional | May be used for cyber security lab work if performance is acceptable |

## Sanitized Device Naming

Public documentation should refer to systems by role instead of personal or identifying names.

Suggested labels:

- `pve01` - Primary Proxmox host.
- `switch01` - Managed switch.
- `router01` - Router or firewall device.
- `admin-workstation` - Primary desktop or administrative workstation.
- `sec-lab-client` - Optional security testing endpoint.

## Information to Track Privately

The following should be tracked outside the public repository, such as in a password manager or private inventory:

- Serial numbers.
- Warranty information.
- Purchase receipts.
- Exact management IP addresses if not safe to publish.
- Credentials.
- Recovery codes.
- License keys.
- Asset tags.

## Information Safe to Track Publicly

The following can usually be documented safely when sanitized:

- Device role.
- General hardware class.
- Operating system or firmware family.
- Network role.
- Dependencies.
- Backup and recovery expectations.
- Maintenance responsibilities.
- Lessons learned.

## Current Assumptions

- The Proxmox host is the primary compute platform.
- The managed switch is part of the current lab network baseline.
- The lab still depends on existing upstream home networking for internet access.
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

- Add sanitized hardware specs for each device.
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
