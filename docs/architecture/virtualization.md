# Virtualization Architecture

## Purpose

Describe the homelab virtualization design, Proxmox platform role, workload model, security controls, monitoring boundaries, backup architecture, and future host transition.

## Current Status

Proxmox VE is the active virtualization platform. Two stable infrastructure VMs run on `pve01`, and hardware has been acquired for a future dedicated server.

Current priorities:

- Keep `pve01` reachable, secure, monitored, backed up, and documented.
- Track every persistent VM in the [VM Inventory](vm-inventory.md).
- Keep DNS and monitoring on separate guests.
- Include stable VMs in backup and recovery planning before considering deployment complete.
- Complete Project 004 reverse proxy and internal HTTPS.
- Assemble and validate the future server before assigning it a production role.
- Prevent experimental workloads from consuming resources required by core infrastructure.

## Active Platform

| Area | Current state |
| --- | --- |
| Hypervisor | Proxmox VE `9.2.2` |
| Debian base | Debian 13 Trixie |
| Running kernel | `7.0.2-6-pve` |
| Active host | Lenovo ThinkPad E16 Gen 1, `pve01` |
| Management access | Internal-only |
| Administrative model | Named routine administrator plus root break-glass identity, both protected by TOTP and independent recovery keys |
| Local storage | 1 TB PCIe SSD |
| Backup storage | Dedicated 5 TB external ext4 target |
| Host monitoring | Node Exporter, Prometheus, and Grafana |
| Backup status | Daily backups active for `dns01` and `mon01`; isolated `dns01` restore tested |

Exact bridges, addresses, VM IDs, storage identifiers, drive UUIDs, authentication material, and backup filenames remain private.

## Current Workloads

| VM | Role | Status | Backup maturity |
| --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and Node Exporter | Active | Daily backup; isolated whole-VM restore tested 2026-07-14 |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active | Daily backup; independent restore not yet tested |

See [VM Inventory](vm-inventory.md) for resources, monitoring coverage, and recovery priority.

## Planned Dedicated Server

Acquired baseline:

| Component | Sanitized specification |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| Cooling | Noctua NH-U12S |
| Power supply | Existing 500 W unit |
| Chassis | Existing NZXT H510 |
| Planned local storage | Two existing 1 TB NVMe devices |
| Known limitation | One inner DIMM slot reported nonfunctional |
| Status | Acquired; assembly and local validation pending |

The future server is not production infrastructure until it passes:

- Visual inspection and assembly validation.
- CPU and memory detection checks.
- Memory stability and thermal testing.
- Storage-health validation and layout selection.
- Network validation.
- Hypervisor installation and security baseline.
- Monitoring and backup integration.
- Power measurement and operational review.

A future ADR must decide whether it replaces the ThinkPad, supplements it, or changes the ThinkPad to a secondary role.

## Design Goals

- Provide a flexible platform for infrastructure services and lab workloads.
- Keep core infrastructure separate from experimental systems.
- Practice VM lifecycle, capacity, backup, and recovery operations.
- Make workload criticality and restore order explicit.
- Avoid undocumented hypervisor changes.
- Support automation only after the manual design is understood.
- Treat host transitions as documented migrations rather than hardware swaps.

## Workload Categories

| Category | Examples | Stability expectation |
| --- | --- | --- |
| Core infrastructure | DNS, monitoring, backup-related tooling, management services | Stable, monitored, documented, and backed up |
| Lab services | Reverse proxy, internal applications, dashboards | Documented and recoverable; may evolve frequently |
| Security lab | Attacker systems, vulnerable VMs, detection projects | Isolated and clearly labeled |
| Temporary experiments | Short-lived tests and proofs of concept | Disposable unless promoted through documentation and onboarding |

## VM Onboarding Standard

Before a persistent VM is considered complete:

- Assign a role-based hostname.
- Record purpose, operating system, resources, storage, and network placement.
- Configure non-root administration where appropriate.
- Install QEMU Guest Agent when supported.
- Add host or service monitoring.
- Define recovery priority and dependencies.
- Add backup coverage.
- Document validation and security considerations.
- Update the VM inventory, project page, service page, roadmap, and changelog as applicable.

## Naming Convention

Use:

```text
<role><number>
```

Examples include `dns01`, `mon01`, `proxy01`, `pbs01`, and `sec-lab01`.

Avoid personal names, family names, locations, or identifying labels in public VM names.

## Resource Allocation

Resource allocation starts conservatively and changes based on observed behavior.

Current lessons:

- `mon01` increased from 2 GB to 3 GB RAM after Grafana showed limited headroom.
- The current host's 16 GB RAM is the main workload-growth constraint.
- Core infrastructure receives priority over experiments.
- Host capacity must remain available for Proxmox management and recovery.
- The future server's 32 GB baseline improves capacity but does not eliminate planning.
- The failed DIMM slot must be validated before memory expansion decisions.

## Networking Model

- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use static addressing.
- Internal DNS records are managed through Pi-hole.
- Public documentation sanitizes bridge names, addresses, VM IDs, and MAC addresses.
- `mon01` scrapes Node Exporter on `dns01` and `pve01`.
- `mon01` probes recursive and local DNS behavior on `dns01`.
- Security-lab networking remains a future isolation project.

Project 004 will add a reverse proxy and internal HTTPS. Its network placement, DNS names, certificate trust, and service dependencies must be documented before it becomes foundational infrastructure.

## Guest Integration

QEMU Guest Agent is installed on `dns01` and `mon01`.

It depends on:

- The guest package and systemd service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling the virtual hardware. See [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

Current monitoring:

- Node Exporter on `pve01`, `dns01`, and `mon01`.
- Prometheus target health for all three systems.
- Grafana CPU, memory, filesystem, network, and uptime views.
- Recursive and local DNS probes for `dns01`.

Node Exporter on `pve01` does not provide authoritative:

- VM or container state.
- Storage-pool health.
- Proxmox task results.
- Backup-job success or age.
- Cluster or quorum state.
- Replication or migration state.

Future Proxmox platform monitoring requires a documented least-privilege identity.

## Backup and Recovery

Project 003 implemented:

- A dedicated 5 TB external ext4 backup target.
- Persistent UUID-based mounting.
- Proxmox backup-only directory storage.
- Mount-point enforcement.
- Daily snapshot-mode backups with Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Initial successful backups for `dns01` and `mon01`.
- A successful isolated `dns01` whole-VM restore.
- Tested backup and restore runbooks.

Restore testing used a temporary VM ID and removed the virtual network adapter before boot. It proved VM reconstruction, Debian boot, filesystem availability, Pi-hole FTL startup, and Node Exporter startup. It did not prove network-facing DNS or monitoring behavior.

Current recovery priority:

1. Restore physical networking and Proxmox management access.
2. Confirm local and backup storage.
3. Restore `dns01` and validate public plus local DNS.
4. Restore `mon01` and validate Prometheus, both Blackbox jobs, and Grafana.
5. Confirm monitoring observes all restored systems.
6. Restore lower-priority workloads.

## Security Considerations

- Do not expose Proxmox management publicly.
- Use the named routine administrator and reserve root for break-glass work.
- Store credentials, TOTP material, recovery keys, API credentials, and private keys outside Git.
- Keep backup storage away from attacker-style workloads.
- Limit administrative access to trusted systems and future management networks.
- Document privileged containers, passthrough, nesting, and unusual permissions.
- Avoid publishing VM IDs, addresses, MAC addresses, storage identifiers, or raw configuration exports.
- Introduce platform-monitoring credentials only through least privilege.

## Maintenance Notes

Before major hypervisor work:

- Confirm a recent successful backup.
- Confirm the external target is truly mounted and active.
- Record VM shutdown and startup order.
- Review available host resources.
- Preserve management and physical-console access.

After maintenance:

- Validate `dns01`, `mon01`, and `pve01` monitoring.
- Confirm system time and TOTP authentication.
- Confirm backup storage remounts.
- Review the next scheduled backup.
- Re-test recovery after major storage, hypervisor, or migration changes.

## Future Improvements

- Complete Project 004 reverse proxy and internal HTTPS.
- Document sanitized bridge and local-storage layouts.
- Add Proxmox VM, storage, task, and backup metrics.
- Add a tested Proxmox maintenance and management-access recovery runbook.
- Perform an independent `mon01` restore test.
- Add a second backup copy in a separate failure domain.
- Assemble and validate the future server.
- Create the future host-role and migration ADR.
- Integrate power measurement, UPS monitoring, and graceful shutdown.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Proxmox Platform](../services/proxmox.md)
- [Current Proxmox Host](../hardware/server.md)
- [Future Virtualization Server](../hardware/server-build.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)