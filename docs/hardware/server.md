# Lenovo ThinkPad E16 Gen 1 — Initial Proxmox Host

## Purpose

This page records the Lenovo ThinkPad E16 Gen 1's former role as the first `pve01` virtualization host and its current lifecycle state after Project 005.

## Current Role

| Area | Details |
| --- | --- |
| Previous role | Initial Proxmox VE host, `pve01` |
| Previous platform | Proxmox VE on Debian 13 |
| CPU | 13th Gen Intel Core i5-1335U |
| Memory | 16 GB RAM |
| Current status | Retired from the production hypervisor role |
| Current use | General endpoint / temporary administrative workstation |
| Production workloads | None |
| Cluster membership | None |

## Historical Value

The ThinkPad provided a low-cost, low-power bootstrap platform for:

- Pi-hole DNS.
- Prometheus and Grafana monitoring.
- NGINX Proxy Manager and internal HTTPS.
- Proxmox authentication hardening.
- Scheduled VM backups and isolated restore testing.

Its integrated battery provided limited ride-through, but 16 GB RAM and limited expansion constrained future growth.

## Project 005 Transition

The Proxmox SATA SSD was removed only after a clean VM and host shutdown, then installed in the dedicated X299 server. The X299 system retained the hostname `pve01` and the existing workloads and configuration.

After validation, the ThinkPad was returned to endpoint use. It is not a backup hypervisor, cluster member, or automatic recovery target. Assigning it a future infrastructure role requires a new documented decision.

## Security and Data Handling

- The ThinkPad must not retain stale production credentials or recovery material beyond what its current administrative role requires.
- Endpoint use must not be described as hypervisor redundancy.
- If used for future security testing, it must be isolated from trusted infrastructure and backup storage.
- Serial numbers, device identifiers, exact addresses, and personal endpoint details remain outside Git.

## Lessons Learned

- Existing business hardware can bootstrap a capable production-style lab without waiting for dedicated server equipment.
- Laptop batteries are useful for brief interruptions but are not substitutes for coordinated UPS protection.
- Capacity limits should trigger a planned migration before they become an outage or block critical services.
- A cleanly transferred system disk can preserve platform state while allowing the original endpoint to be repurposed.

## Related Documentation

- [X299 Virtualization Server](server-build.md)
- [Project 005](../projects/project-005-x299-virtualization-server.md)
- [ADR-0001](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md)
- [Hardware Inventory](inventory.md)
