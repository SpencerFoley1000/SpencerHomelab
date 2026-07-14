# ADR-0003: Use Direct-Attached Proxmox Backup Storage with Layered Recovery Assets

## Status

Accepted

## Date

2026-07-14

## Context

The homelab required a first operational backup system for the stable infrastructure VMs `dns01` and `mon01`.

Requirements:

- Store VM backups separately from the Proxmox system and VM disk.
- Use hardware already appropriate for the current two-VM environment.
- Support automatic scheduling, retention, pruning, and manual restore testing.
- Avoid introducing a NAS or Proxmox Backup Server before the additional complexity is justified.
- Preserve portable application-level recovery options for Pi-hole and Grafana-related state.
- Prevent Proxmox from silently writing backup data into the host root filesystem when the external target is absent.
- Keep exact drive identifiers, mount identifiers, backup filenames, and private service exports outside the public repository.

A 5 TB external hard drive was available for the initial implementation. The lab currently has one active Proxmox node and a small number of stable VMs, so a direct-attached target provides useful recovery capability without requiring another always-on storage server.

## Decision

Use a dedicated 5 TB external hard drive as the first Proxmox backup destination.

Implementation characteristics:

- Format the target with ext4.
- Mount it persistently by filesystem UUID at `<BACKUP_MOUNT>`.
- Register it as Proxmox directory storage using the sanitized label `<BACKUP_TARGET>`.
- Restrict the Proxmox content type to VM backup artifacts.
- Enable Proxmox mount-point validation so the storage is unavailable when the external filesystem is not mounted.
- Protect `dns01` and `mon01` with daily snapshot-mode backups.
- Use Zstandard compression.
- Retain 7 daily, 4 weekly, and 3 monthly backups.
- Keep missed-run repetition disabled in the initial configuration and review job history operationally.
- Maintain application-level recovery assets and sanitized rebuild documentation in addition to whole-VM backups.
- Require a representative isolated restore test before calling the design operational.

The first restore validation used `dns01`. The backup was restored to a temporary VM, its virtual network adapter was removed before boot, Debian and the filesystem loaded normally, and `pihole-FTL` plus Node Exporter reported active. The temporary VM was then removed.

## Rationale

### Separate Source and Backup Storage

The external disk is physically separate from the Proxmox system SSD. Failure of the VM datastore does not automatically destroy the backup copy.

### ext4 for the Proxmox-Managed Target

ext4 provides native Linux ownership, permissions, reliability, and tooling without the cross-platform compromises of retaining the factory NTFS filesystem.

### UUID-Based Persistent Mount

Linux device names such as `/dev/sdX` can change. A filesystem UUID provides stable mounting while the exact identifier remains private.

### Mount-Point Enforcement

A missing external drive must fail visibly. Without mount-point enforcement, a backup path can exist on the host root filesystem and accept data even though the intended disk is absent, creating both capacity and recovery risk.

### Snapshot Backups with Zstandard

Snapshot mode minimizes service interruption for the current QEMU VMs. Zstandard provides a practical balance of compression and backup duration for the current hardware.

### Tiered Retention

Daily, weekly, and monthly retention provides recent recovery points plus limited historical depth without keeping every full backup indefinitely.

### Layered Recovery Assets

Whole-VM backups optimize recovery speed, while Pi-hole Teleporter exports, Grafana dashboard exports, configuration inventories, and runbooks reduce dependence on a single backup format and support selective or manual recovery.

## Alternatives Considered

| Alternative | Reason not chosen |
| --- | --- |
| Store backups on the Proxmox system SSD | A host-storage failure could destroy both the workload and its backup |
| Keep the factory NTFS filesystem | Less appropriate for a dedicated Linux/Proxmox backup target and its ownership model |
| Manual backups only | Easy to forget and provides inconsistent recovery-point coverage |
| Application exports only | Does not preserve the complete operating system, package state, and VM configuration |
| VM backups only | Does not replace portable exports, dependency knowledge, or manual rebuild documentation |
| Dedicated NAS | Adds cost, another operating system, network dependencies, and maintenance before current scale requires it |
| Proxmox Backup Server | Provides stronger deduplication and backup features but is unnecessary complexity for the first two protected VMs |
| Cloud-only backup | Introduces bandwidth, recurring cost, credentials, and privacy considerations before the local recovery process is proven |

## Consequences

### Positive

- Stable infrastructure VMs now have automatic full-VM backups.
- Backup storage is separated from the active VM datastore.
- Retention is automatically managed.
- A representative whole-VM restore path has been proven.
- The design remains understandable and maintainable for the current scale.
- Public documentation demonstrates backup architecture, validation, and tradeoff analysis without exposing private identifiers.

### Negative / Tradeoffs

- The drive is normally connected to the same physical host, so it is not an immutable, offline, or off-site copy.
- A host-wide electrical, physical, malware, or operator event could still affect both source and backup.
- Direct-attached storage does not provide network-independent recovery from another Proxmox node without physically reconnecting the disk.
- Full QEMU backups consume more capacity than a deduplicating backup platform.
- `mon01` has a successful backup but has not been independently restore-tested.
- The isolated `dns01` test did not validate live client DNS traffic because the network adapter was intentionally removed.

## Security Decisions

- Backup artifacts are treated as sensitive because they contain complete VM state.
- Exact serial numbers, UUIDs, backup volume identifiers, internal addresses, and raw task logs remain outside Git.
- The target is dedicated to trusted backup operations and must not be writable from experimental or attacker-style workloads.
- Application exports remain outside Git and are inspected without publishing protected values.
- A future second copy should use a separate failure domain.

## Validation

The decision has been validated through:

- Capacity and device identity verification before destructive changes.
- SMART overall-health success.
- An extended SMART self-test completed without error.
- ext4 filesystem creation and expected usable capacity.
- Persistent UUID-based mounting.
- Active Proxmox directory storage registration.
- Backup-only content restriction.
- Mount-point enforcement.
- Successful manual backups of `dns01` and `mon01`.
- A daily scheduled job using snapshot mode and Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Successful isolated restore and local service validation for `dns01`.
- Removal of the temporary restored VM after testing.

## Follow-Up Work

- [ ] Monitor scheduled job completion and backup age.
- [ ] Add actionable failure notification and a backup-job response runbook.
- [ ] Perform an independent `mon01` restore test after meaningful monitoring-stack changes or before relying on it for a major migration.
- [ ] Perform a controlled network-connected recovery test when duplicate-address risk can be eliminated.
- [ ] Export and privately validate the Homelab Infrastructure Overview dashboard.
- [ ] Evaluate an offline, rotated, off-site, NAS, or Proxmox Backup Server copy when the lab's recovery requirements justify it.
- [ ] Revisit missed-run behavior if the Proxmox host is not consistently online at the scheduled time.

## Related Documentation

- [Storage Architecture](../architecture/storage.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [VM Inventory](../architecture/vm-inventory.md)