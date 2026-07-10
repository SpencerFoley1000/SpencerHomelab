# Hardware

This directory documents the physical hardware used in the homelab.

Hardware documentation is sanitized for a public repository. It should explain the role of each device, how it fits into the architecture, and what operational assumptions depend on it without publishing serial numbers, asset tags, public IP details, personally identifying labels, or unnecessary exact internal addressing.

## Hardware Documents

- [Inventory](inventory.md) - Sanitized inventory of physical devices and their roles.
- [Switch](switch.md) - Managed switch role, management access, and future VLAN usage.
- [Router](router.md) - Routing/firewall role and current upstream dependency.
- [Server](server.md) - Primary virtualization server and Proxmox host notes.

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

Use placeholders where appropriate:

- `<HOST_IP>`
- `<SWITCH_MGMT_IP>`
- `<ROUTER_IP>`
- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<REDACTED_SSID>`
- `<SERIAL_REDACTED>`

## Operational Standard

Each hardware page should explain:

- Purpose
- Role in the lab
- Operating system or firmware where relevant
- Network placement
- Dependencies
- Security considerations
- Maintenance notes
- Future improvements

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../architecture/security.md)
