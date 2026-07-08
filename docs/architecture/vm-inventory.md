# VM Inventory

## Purpose

This inventory tracks virtual machines that are intentionally part of the homelab environment.

The goal is to document what exists, why it exists, where it runs, and how important it is to the rest of the lab. Exact IP addresses and sensitive implementation details are intentionally sanitized for public documentation.

## Inventory Standards

Each VM should document:

- Hostname
- Purpose
- Platform
- Operating system
- Resource allocation
- Network placement
- IP assignment model
- Service owner or role
- Backup status
- Recovery priority
- Documentation link

Avoid publishing:

- Exact internal IPs unless they are necessary and intentionally sanitized.
- MAC addresses.
- Serial numbers.
- Personal usernames.
- Secrets, tokens, keys, or passwords.
- Hostnames that reveal personally identifying information.

## Active Virtual Machines

| Hostname | Purpose | OS | vCPU | RAM | Disk | Network | IP Model | Status | Backup Status | Documentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dns01` | Pi-hole DNS and local DNS records | Debian 13.5 (Trixie) | 2 | 2 GB | 20 GB | Homelab LAN | Static, sanitized as `<DNS01_IP>` | Active | Not yet backed up | [Pi-hole](../services/pihole.md) |

## Recovery Priority

| Priority | VM | Reason |
| --- | --- | --- |
| High | `dns01` | Provides internal DNS for homelab services and local records |

## Naming Convention

Current naming convention:

```text
<role><number>
```

Examples:

- `dns01` - DNS service
- `mon01` - Monitoring service
- `pbs01` - Backup service
- `proxy01` - Reverse proxy service

This format is short, readable, and easy to expand as the lab grows.

## Notes

- `dns01` is the first production-style infrastructure VM.
- Future infrastructure VMs should be added here before being considered complete.
- Experimental VMs should be clearly labeled as experimental or temporary.
- Backup status should be updated once Proxmox Backup Server or another backup target is deployed.

## Future Improvements

- Add VM IDs if they can be documented safely.
- Add backup schedule and retention once backup infrastructure exists.
- Add monitoring status once the monitoring stack is deployed.
- Add owner, service tier, and restore-time expectations for critical services.
- Link VM entries to service pages, runbooks, and architecture decision records.

## Related Documentation

- [Virtualization Architecture](virtualization.md)
- [Network Architecture](network.md)
- [Pi-hole Service](../services/pihole.md)
- [Hardware Inventory](../hardware/inventory.md)
