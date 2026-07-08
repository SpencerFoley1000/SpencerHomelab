# Virtualization Architecture

## Purpose

This document describes the virtualization design for the homelab. It focuses on the role of Proxmox, the intended workload model, and the operational assumptions that should guide future VM and container decisions.

## Current Status

The homelab currently uses Proxmox as the primary virtualization platform. The initial goal is to establish a stable host foundation before adding a large number of services.

Current priorities:

- Keep the Proxmox host reachable and documented.
- Establish clear VM and container naming conventions.
- Separate stable infrastructure from experimental workloads.
- Document storage, networking, backup, and recovery assumptions.

## Platform

| Area | Current Direction |
| --- | --- |
| Hypervisor | Proxmox VE |
| Primary role | Run lab infrastructure, services, and test workloads |
| Management access | Internal network only; exact endpoint omitted from public documentation |
| Documentation level | Sanitized architecture and operational notes |

## Design Goals

- Provide a flexible platform for infrastructure services and lab workloads.
- Practice VM lifecycle management, resource planning, backups, and recovery.
- Keep core infrastructure separate from experimental systems.
- Avoid making the hypervisor dependent on undocumented manual changes.
- Support future automation without requiring automation on day one.

## Workload Categories

| Category | Examples | Stability Expectation |
| --- | --- | --- |
| Core infrastructure | DNS, monitoring, backup services, management tooling | Stable and documented |
| Lab services | Dashboards, test applications, learning projects | Documented, but may change frequently |
| Security lab | Attacker machines, vulnerable VMs, detection engineering projects | Isolated and clearly labeled |
| Temporary experiments | Short-lived tests and proof-of-concepts | Disposable unless promoted to documented services |

## Naming Convention

A consistent naming convention should make it easy to identify workload purpose.

Suggested pattern:

```text
<role>-<number>
```

Examples using sanitized names:

- `dns-01`
- `mon-01`
- `docker-01`
- `sec-lab-01`
- `test-vm-01`

Avoid using personal names, family names, or identifying labels in VM names committed to public documentation.

## Resource Allocation Strategy

Resource allocation should start conservative and be adjusted based on observed usage.

Guidelines:

- Avoid overcommitting memory for stable infrastructure until monitoring is in place.
- Keep enough host resources available for maintenance and emergency access.
- Document unusually large CPU, memory, or disk allocations.
- Treat experimental workloads as lower priority than core infrastructure.

## Networking Model

Initial Proxmox networking should remain simple until VLANs and routing are intentionally implemented.

Planned future documentation should include:

- Proxmox bridge layout.
- VLAN-aware bridge configuration if used.
- Management network placement.
- Which VM groups are allowed on each network segment.
- Security lab isolation boundaries.

Exact bridge addresses and internal addressing should be sanitized.

## Backup and Recovery

Virtualization documentation should eventually include:

- Which VMs are backed up.
- Backup frequency.
- Backup destination.
- Retention policy.
- Restore testing procedure.
- Recovery priority for critical services.

Until backups are implemented and tested, any service should be considered recoverable only from its documented configuration and notes.

## Security Considerations

- Do not expose Proxmox management directly to the internet.
- Use strong unique credentials stored outside the repository.
- Limit administrative access to trusted devices and future management networks.
- Keep security lab workloads isolated from trusted infrastructure.
- Document privileged containers or unusual VM permissions when used.
- Apply Proxmox and host updates through a deliberate maintenance process.

## Maintenance Notes

Future maintenance procedures should document:

- Proxmox update process.
- Reboot expectations.
- VM shutdown order.
- Backup checks before major changes.
- Recovery steps if the host becomes unreachable.

## Future Improvements

- Add host-specific documentation under hardware docs.
- Create a VM inventory table once workloads are deployed.
- Add a standard VM provisioning runbook.
- Add a backup and restore validation runbook.
- Add architecture decision records for major virtualization choices.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
- [Hardware Inventory](../hardware/inventory.md)
