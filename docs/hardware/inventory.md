# Hardware Inventory

This page tracks sanitized hardware roles for the homelab.

## Documentation Rules

Do not publish:

- Device serial numbers
- Asset tags
- Warranty identifiers
- Exact personally identifying labels
- Public IP addresses

Use generalized names such as:

- `Primary Desktop`
- `Lab Laptop`
- `Managed Switch`
- `Router / Firewall`
- `Virtualization Host`

## Inventory

| Device | Role | Status | Notes |
|---|---|---:|---|
| Primary Desktop | Workstation / possible VM host | Planned | May be used for local lab VMs or testing. |
| Lab Laptop | Security lab / attacker system candidate | Planned | May remain separate for security-related lab work. |
| Managed Switch | Network segmentation | Planned | Document VLAN and management design once configured. |
| Router / Firewall | Network edge / routing | Planned | Document sanitized role and design decisions once installed. |

## Future Documentation

For each significant device, document:

- Purpose
- Hardware class
- Operating system or firmware
- Network role
- Management approach
- Backup or recovery considerations
- Security considerations
- Replacement considerations
