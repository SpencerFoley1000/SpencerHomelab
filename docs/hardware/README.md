# Hardware

This directory documents the physical hardware used or intentionally planned for the homelab.

Hardware documentation is sanitized for a public repository. It should explain the role of each device, how it fits into the architecture, known limitations, validation requirements, and operational assumptions without publishing serial numbers, asset tags, public IP details, personally identifying labels, or unnecessary exact internal addressing.

## Hardware Documents

- [Inventory](inventory.md) - Sanitized inventory of active, acquired, and planned physical devices.
- [Switch](switch.md) - Managed switch role, management access, and future VLAN usage.
- [Router](router.md) - Routing/firewall role and current upstream dependency.
- [Current Proxmox Host](server.md) - Lenovo ThinkPad E16 Gen 1 and active `pve01` role.
- [Future Virtualization Server Build](server-build.md) - Acquired X299 platform, known limitation, validation plan, and intended role.

The 5 TB external backup drive and future UPS are tracked in the inventory because their current architecture role does not yet justify separate device pages.

The personal administrative workstation is intentionally referenced only by role because it is not core homelab infrastructure and detailed hardware specifications are not required to explain the architecture.

## Documentation Rules

Do not publish:

- Device serial numbers.
- Asset tags.
- Public IP addresses.
- Home address or ISP account information.
- Personally identifying hostnames or SSIDs.
- Exact internal IP addresses unless there is a strong reason and the value is safe to expose.
- Credentials, recovery codes, license keys, private keys, or certificates containing private material.
- Private drive identifiers, UUIDs, or mount paths when placeholders are sufficient.

Use placeholders where appropriate:

- `<HOST_IP>`
- `<SWITCH_MGMT_IP>`
- `<ROUTER_IP>`
- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<BACKUP_TARGET>`
- `<REDACTED_SSID>`
- `<SERIAL_REDACTED>`

## Operational Standard

Each hardware page should explain:

- Purpose and intended role.
- Lifecycle state.
- Known specifications.
- Known limitations or defects.
- Operating system or firmware where relevant.
- Network and storage placement.
- Dependencies.
- Validation requirements.
- Security considerations.
- Maintenance and recovery notes.
- Future improvements.

Hardware should not be described as production infrastructure until it has been physically inspected, tested, monitored, and integrated into backup and recovery workflows.

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../architecture/security.md)
- [Roadmap](../../ROADMAP.md)
