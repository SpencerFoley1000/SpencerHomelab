# Proxmox VE Platform

## Purpose

Proxmox VE is the active virtualization platform for the homelab. It provides the management plane, compute environment, VM storage, backup scheduling, and recovery tooling for infrastructure virtual machines including `dns01` and `mon01`.

Hardware-specific details are documented separately. Architecture decisions and long-term tradeoffs are recorded in architecture pages and ADRs.

## Status

| Area | Details |
| --- | --- |
| Lifecycle state | Active |
| Platform role | Primary hypervisor and VM management platform |
| Hostname | `pve01` |
| Hardware | Lenovo ThinkPad E16 Gen 1 |
| Proxmox VE version | `9.2.2` |
| Debian base | Debian 13 Trixie |
| Running kernel | `7.0.2-6-pve` |
| Management exposure | Internal homelab only |
| Public access | None |
| Administrative authentication | Named routine administrator and protected root break-glass identity; TOTP and independent recovery keys enabled |
| Host monitoring | Active through Node Exporter, Prometheus, and Grafana |
| Backup maturity | Daily backups active for `dns01` and `mon01`; isolated `dns01` restore validated 2026-07-14 |
| Future platform | X299 server hardware acquired; assembly and validation pending |

Exact management endpoints, internal addresses, routine administrator names, VM IDs, MAC addresses, drive UUIDs, storage identifiers, authentication seeds, recovery keys, and backup filenames are intentionally omitted.

## Current Workloads

| VM | Role | Status | Backup maturity |
| --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and Node Exporter | Active | Daily backup; isolated whole-VM restore tested |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active | Daily backup; independent restore not yet tested |

The [VM Inventory](../architecture/vm-inventory.md) is the source of truth for VM resources, monitoring, backup maturity, and recovery priority.

## Platform Responsibilities

Proxmox currently provides:

- VM lifecycle management.
- Virtual CPU, memory, storage, and network allocation.
- Internal management access.
- QEMU Guest Agent integration for stable Linux VMs.
- Local virtualization storage.
- Scheduled snapshot-mode VM backups.
- Backup retention and pruning.
- VM restoration through `qmrestore`.
- A platform for future proxy, identity, security, and automation workloads.

## Dependencies

Proxmox operations depend on:

- The Lenovo ThinkPad E16 Gen 1 active host.
- The TP-Link managed switch for wired connectivity.
- The GL.iNet Opal routing boundary.
- Existing upstream household connectivity for package updates and public DNS.
- Local host storage.
- Dedicated external backup storage for VM recovery.
- Private credential and recovery-material storage outside Git.
- Accurate system time for TOTP.

The VMs can continue running during an upstream internet outage, but package updates and public recursive DNS may be affected.

## Networking

Current network model:

- The management interface is reachable only from the internal homelab network.
- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use static addressing.
- Exact bridge names, addresses, MAC addresses, and VM IDs are not published.
- VLAN-aware bridges and isolated workload networks remain planned.

Future networking documentation must record:

- Sanitized bridge roles.
- VLAN-aware configuration.
- Management-network placement.
- Allowed workload networks.
- Security-lab isolation boundaries.
- The network relationship between the ThinkPad and future server.

## Firewall

The Proxmox firewall service is active.

During Node Exporter deployment, `mon01` successfully reached `<PVE01_IP>:9100` while the firewall was enabled. Existing policy already permitted the trusted monitoring connection, so no broad inbound rule was added.

Firewall-change sequence:

1. Test the required path from the intended source.
2. Confirm whether existing policy permits it.
3. Add the narrowest source, destination, protocol, and port rule only when needed.
4. Revalidate management access and monitoring.
5. Document permanent policy changes.

## Administrative Authentication

Proxmox administrative access uses separate routine and emergency identities:

| Identity | Intended use | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine web-interface administration | Unique password, TOTP, propagated Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass and root-only Proxmox actions | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path | Physical access to `pve01` |

Operational rules:

- Use `<PROXMOX_ADMIN_ACCOUNT>` for routine administration.
- Reserve `root@pam` for emergencies and root-only operations.
- Keep actual account names, passwords, TOTP seeds, QR codes, and recovery keys outside Git.
- Keep recovery material separate from the enrolled authenticator device.
- Do not consume recovery keys during routine testing.
- Re-enroll TOTP and rotate affected recovery material after authenticator loss or replacement.

Validation completed during implementation:

- `System clock synchronized: yes`.
- `NTP service: active`.
- Both identities completed clean password-and-TOTP logins from fresh browser sessions.
- Each identity has a separate recovery-key set.
- The named administrator can manage the host and active VMs through its propagated role.
- Root authentication-factor changes require a root-authenticated session.

The routine Proxmox identity is application-level. It does not create a Debian user or grant console or SSH access automatically.

## Storage

### Active Local Storage

The active platform uses the ThinkPad's local 1 TB PCIe SSD for:

- Proxmox system storage.
- VM disks.
- ISOs and templates.
- Active workload state.

### Dedicated Backup Storage

Project 003 added a dedicated 5 TB external backup target.

Implemented controls:

- SMART overall-health validation.
- Extended SMART self-test completed without error.
- ext4 filesystem.
- Persistent UUID-based mount using a private identifier.
- Proxmox directory storage registration.
- Backup-only content restriction.
- Mount-point enforcement to prevent root-filesystem fallback.
- Daily backups of `dns01` and `mon01`.
- Snapshot mode with Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.

Public documentation uses `<BACKUP_MOUNT>` and `<BACKUP_TARGET>` rather than exact local identifiers.

The future X299 server has two existing 1 TB NVMe devices, but its final storage layout is not yet approved.

## Backup and Recovery

### Current Backup Job

| Setting | Current value |
| --- | --- |
| Protected VMs | `dns01`, `mon01` |
| Schedule | Daily at 10:00 local time |
| Mode | Snapshot |
| Compression | Zstandard |
| Retention | 7 daily, 4 weekly, 3 monthly |
| Repeat missed jobs | Disabled in the initial configuration |
| Storage safety | Mount-point enforcement enabled |

### Restore Validation

The `dns01` backup was restored to a temporary VM under a different ID.

Safety and validation steps:

- Restored to normal VM storage without overwriting the active guest.
- Renamed as a restore-test VM.
- Removed the virtual network adapter before startup.
- Confirmed Debian booted to a normal login prompt.
- Confirmed the expected root filesystem was present.
- Confirmed `pihole-FTL` was active.
- Confirmed Node Exporter was active.
- Reviewed `systemctl --failed`; `openipmi.service` was nonblocking for the QEMU guest environment.
- Shut down and destroyed the temporary restore VM.

The test proved whole-VM reconstruction and local service startup. It did not validate network-facing DNS or remote monitoring because the restored VM was intentionally disconnected.

Recovery order:

1. Restore physical network connectivity and Proxmox management access.
2. Confirm local and backup storage.
3. Restore `dns01` and validate public and local DNS.
4. Restore `mon01` and validate Prometheus, all Node Exporter targets, both Blackbox jobs, and Grafana.
5. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
6. Restore lower-priority workloads.

Administrative-access recovery must preserve:

- The protected root break-glass identity.
- Recovery keys independent of the authenticator device.
- Accurate system time.
- Physical-console access as the final path.

## QEMU Guest Agent

QEMU Guest Agent is installed on stable Debian VMs where supported.

The agent depends on:

- The guest package and service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling virtual hardware. See [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

### Current Baseline

Node Exporter `1.9.0-1+b4` is installed directly on `pve01`.

Validated state:

- `prometheus-node-exporter` is active and enabled.
- `/metrics` responds on TCP `9100`.
- `mon01` can reach the endpoint.
- Prometheus scrapes it under the shared `node_exporter` job.
- Labels are `host="pve01"` and `role="hypervisor"`.
- Grafana displays CPU, memory, filesystem, network, and uptime metrics.

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

### Monitoring Boundary

Node Exporter does not provide authoritative:

- VM or container state.
- Cluster or quorum status.
- Proxmox task results.
- Storage-pool state.
- Backup-job success or age.
- Replication or migration state.

A future Proxmox exporter or API integration must use a dedicated least-privilege identity. Credentials remain outside Git.

## Validation Commands

Platform and monitoring:

```bash
pveversion
. /etc/os-release && echo "$PRETTY_NAME"
systemctl is-active pve-firewall
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
curl -s http://localhost:9100/metrics | head
ss -ltnp | grep 9100
timedatectl status
```

Backup storage and jobs:

```bash
findmnt <BACKUP_MOUNT>
df -h <BACKUP_MOUNT>
pvesm status
pvesm list <BACKUP_TARGET>
pvesh get /cluster/backup --output-format yaml
```

Restore procedures are documented in [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md).

## Security Considerations

- Do not expose Proxmox management publicly.
- Use `<PROXMOX_ADMIN_ACCOUNT>` for routine management and reserve `root@pam` for break-glass work.
- Maintain independent recovery keys.
- Keep account names, passwords, TOTP seeds, QR codes, recovery keys, storage identifiers, and backup artifacts outside the repository.
- Limit management access to trusted devices and future management networks.
- Keep experimental and attacker-style workloads isolated.
- Treat the hypervisor and backup target as high-value infrastructure.
- Keep Node Exporter internal-only.
- Introduce API monitoring credentials only through a documented least-privilege design.
- Do not weaken mount-point enforcement to make an unavailable backup target appear active.

## Maintenance Notes

After Proxmox upgrades:

- Record the new version and kernel.
- Confirm the firewall service.
- Confirm Node Exporter remains active and reachable.
- Confirm Prometheus reports `pve01` as up.
- Confirm Grafana panels resume.
- Confirm system time remains synchronized.
- Complete a fresh TOTP login with the routine administrator.
- Validate `dns01` and `mon01` after host reboot.
- Confirm the backup target remounts and reports active.
- Review the next backup run.
- Perform a restore test after major storage or backup changes.

## Future Improvements

- Document sanitized bridge and local-storage layout.
- Add Proxmox-specific VM, storage, task, and backup metrics.
- Add backup-age and job-failure alerting with response runbooks.
- Perform an independent `mon01` restore test.
- Evaluate a second backup copy in a separate failure domain.
- Create a tested Proxmox maintenance and management-access recovery runbook.
- Review SSH authentication and root-login policy after console recovery is documented.
- Restrict management through a dedicated management network when segmentation is implemented.
- Assemble and validate the future X299 server.
- Create an ADR defining whether the new server replaces or supplements `pve01`.
- Integrate UPS monitoring and graceful shutdown under Project 005.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Node Exporter](node-exporter.md)
- [Current Proxmox Host Hardware](../hardware/server.md)
- [Future Virtualization Server Build](../hardware/server-build.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0001: Initial Proxmox Host](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Authentication Hardening Change Record](../changes/2026-07-12-proxmox-administrative-authentication-hardening.md)
- [Project 003 Completion Change Record](../changes/2026-07-14-project-003-backup-recovery-completion.md)
- [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md)