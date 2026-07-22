# Virtualization Architecture

## Purpose

Describe the homelab virtualization design, Proxmox platform role, workload model, security controls, monitoring boundaries, backup architecture, and completed host transition.

## Current Status

Proxmox VE is the active virtualization platform. Three stable infrastructure VMs run on the dedicated X299 host `pve01`.

Current priorities:

- Keep `pve01` reachable, secure, monitored, backed up, and documented.
- Track every persistent VM in the [VM Inventory](vm-inventory.md).
- Keep DNS, monitoring, and reverse proxy roles on separate guests.
- Include stable VMs in backup and recovery planning before considering deployment complete.
- Continue validating X299 thermals and stability through production monitoring.
- Prevent experimental workloads from consuming resources required by core infrastructure.

## Active Platform

| Area | Current state |
| --- | --- |
| Hypervisor | Proxmox VE `9.2.2` |
| Debian base | Debian 13 Trixie |
| Running kernel | `7.0.2-6-pve` |
| Active host | Dedicated X299 server, `pve01` |
| Management access | Internal-only |
| Administrative model | Named routine administrator plus root break-glass identity, both protected by TOTP and independent recovery keys |
| Local storage | 1 TB PCIe SSD |
| Backup storage | Dedicated 5 TB external ext4 target |
| Host monitoring | Node Exporter, Prometheus, and Grafana |
| Backup status | Daily backups active for `dns01`, `mon01`, and `proxy01`; isolated `dns01` and `proxy01` restores tested |

Exact bridges, addresses, VM IDs, storage identifiers, drive UUIDs, authentication material, certificate keys, and backup filenames remain private.

## Current Workloads

| VM | Role | Status | Backup maturity |
| --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and Node Exporter | Active | Daily backup; isolated whole-VM restore tested 2026-07-14 |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active | Daily backup; independent restore not yet tested |
| `proxy01` | NGINX Proxy Manager, Docker, internal TLS termination, and Node Exporter | Active | Daily backup; isolated whole-VM restore tested 2026-07-14 |

See [VM Inventory](vm-inventory.md) for resources, monitoring coverage, and recovery priority.

## Dedicated X299 Server

Acquired baseline:

| Component | Sanitized specification |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| Cooling | Noctua NH-U12S |
| Power supply | Existing 500 W unit |
| Chassis | Existing NZXT H510 |
| System storage | Transferred 1 TB SATA Proxmox system disk |
| Available expansion | Two 1 TB NVMe devices with no assigned production role |
| Known limitation | One inner DIMM slot is nonfunctional |
| Status | Active production host; monitored and backed up at the VM layer |

Project 005 completed:

- Physical assembly, POST, CPU, and 32 GB memory detection.
- Migration of the existing Proxmox SATA system disk.
- Network and internal management validation.
- Startup validation for `dns01`, `mon01`, and `proxy01`.
- Backup-target access validation.
- Node Exporter and X299 CPU temperature telemetry validation.

ADR-0005 records the X299 server as the sole production host and retires the ThinkPad from the hypervisor role.

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

`proxy01` is classified as a stable lab service. It is a dependency for friendly HTTPS access, but direct backend paths remain available during proxy failure.

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

Project 004 followed this standard for `proxy01` and added isolated restore testing before closeout.

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
- `proxy01` begins with 2 vCPU, 2 GB RAM, and a 20 GB disk.
- The former ThinkPad host's 16 GB RAM was the main workload-growth constraint.
- Core infrastructure receives priority over experiments.
- Host capacity must remain available for Proxmox management and recovery.
- The X299 server's 32 GB baseline improves capacity but does not eliminate planning.
- The failed DIMM slot must be validated before memory expansion decisions.

## Networking Model

- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use stable addressing.
- Internal DNS records are managed through Pi-hole.
- `lab.home.arpa` service records point selected names to `proxy01`.
- `proxy01` forwards trusted internal traffic to Grafana and Pi-hole backends.
- Direct backend access remains available for recovery.
- Public documentation sanitizes bridge names, addresses, VM IDs, and MAC addresses.
- `mon01` scrapes Node Exporter on `dns01`, `pve01`, and `proxy01`.
- `mon01` probes recursive DNS, local DNS, internal HTTPS, and certificate expiration.
- Security-lab networking remains a future isolation project.

## Guest Integration

QEMU Guest Agent is installed on `dns01`, `mon01`, and `proxy01`.

It depends on:

- The guest package and systemd service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling the virtual hardware. See [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

Current monitoring:

- Node Exporter on `pve01`, `dns01`, `mon01`, and `proxy01`.
- Prometheus target health for all four systems.
- Grafana CPU, memory, filesystem, network, and uptime views.
- Recursive and local DNS probes for `dns01`.
- Internal HTTPS and certificate-expiration probes through `proxy01`.
- X299 CPU temperature metrics through Node Exporter's hardware-monitoring collector.

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
- Recovery runbooks and a tested isolated restore workflow.

Project 004 added `proxy01` to the backup job and validated an isolated whole-VM restore.

Restore testing used temporary VM IDs and removed virtual network adapters before boot. The tests prove VM reconstruction and local service state; they do not prove live network cutover.

Current recovery priority:

1. Restore physical networking and Proxmox management access.
2. Confirm local and backup storage.
3. Restore `dns01` and validate public plus local DNS.
4. Restore `proxy01` if friendly HTTPS is required; retain direct backend access during outage.
5. Restore `mon01` and validate Prometheus, Blackbox jobs, and Grafana.
6. Confirm monitoring observes all restored systems and services.
7. Restore lower-priority workloads.

The root CA private key is intentionally outside the `proxy01` VM backup boundary and requires separate protected storage.

## Security Considerations

- Do not expose Proxmox or NGINX Proxy Manager administration publicly.
- Use the named routine Proxmox administrator and reserve root for break-glass work.
- Store credentials, TOTP material, recovery keys, API credentials, and private certificate keys outside Git.
- Keep backup storage and CA material away from attacker-style workloads.
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
- Preserve direct backend access if the proxy is being changed.

After maintenance:

- Validate `dns01`, `mon01`, `proxy01`, and `pve01` monitoring.
- Confirm system time and TOTP authentication.
- Confirm backup storage remounts.
- Confirm DNS, HTTPS, and certificate probes.
- Review the next scheduled backup.
- Re-test recovery after major storage, hypervisor, migration, or proxy changes.

## Future Improvements

- Document sanitized bridge and local-storage layouts.
- Add Proxmox VM, storage, task, and backup metrics.
- Add a tested Proxmox maintenance and management-access recovery runbook.
- Perform an independent `mon01` restore test.
- Add a second backup copy in a separate failure domain.
- Integrate power measurement, UPS monitoring, and graceful shutdown.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Proxmox Platform](../services/proxmox.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Initial Proxmox Host](../hardware/server.md)
- [X299 Virtualization Server](../hardware/server-build.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md)
- [Project 005](../projects/project-005-x299-virtualization-server.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
