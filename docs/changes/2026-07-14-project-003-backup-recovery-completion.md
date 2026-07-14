# Project 003 Backup and Recovery Completion

## Date

2026-07-14

## Status

Implemented and validated.

## Scope

This change established the first operational VM backup and recovery system for the homelab.

Affected areas:

- Proxmox storage.
- `dns01` and `mon01` backup coverage.
- Backup scheduling and retention.
- VM restore testing.
- Storage, recovery, hardware, service, and project documentation.

## Changed

- Inspected the dedicated 5 TB external backup drive and confirmed its expected capacity.
- Confirmed SMART overall health passed.
- Completed an extended SMART self-test without error.
- Replaced the factory NTFS layout with a dedicated ext4 filesystem.
- Configured a persistent UUID-based mount using a private identifier.
- Registered the target in Proxmox as directory storage dedicated to backup content.
- Enabled mount-point enforcement so Proxmox will not silently write backups to the host root filesystem when the external target is absent.
- Completed initial snapshot-mode, Zstandard-compressed backups for `dns01` and `mon01`.
- Configured a daily backup job for both stable infrastructure VMs.
- Configured retention for 7 daily, 4 weekly, and 3 monthly backups.
- Restored `dns01` to a temporary isolated VM without overwriting the active guest.
- Removed the restored VM's network adapter before boot to prevent duplicate address or service conflicts.
- Confirmed the restored Debian guest booted, mounted its filesystem, and reported `pihole-FTL` and Node Exporter active.
- Removed the temporary restored VM after validation.
- Added a tested Proxmox VM restore runbook.
- Added ADR-0003 for the direct-attached backup and layered recovery design.

Exact drive identifiers, UUIDs, backup filenames, internal addresses, and raw recovery artifacts remain outside the repository.

## Why

- `dns01` and `mon01` are stable infrastructure workloads and required recovery paths beyond manual reconstruction.
- Separate backup storage reduces the risk that failure of the Proxmox VM datastore destroys the only recovery copy.
- Scheduled backups reduce dependence on memory and manual execution.
- Tiered retention provides recent and historical recovery points without unlimited growth.
- Mount-point enforcement prevents a missing USB disk from turning a backup job into unexpected root-filesystem consumption.
- A successful backup file is incomplete evidence until the restore path is exercised.
- Application exports and rebuild documentation remain useful because whole-VM backups do not replace service-level recovery knowledge.

## Validation

- Drive health: SMART passed.
- Extended self-test: completed without error.
- Filesystem: ext4 mounted with expected multi-terabyte free capacity.
- Proxmox storage: active and restricted to backup content.
- Mount safety: mount-point enforcement enabled.
- Initial backup coverage: `dns01` and `mon01` completed successfully.
- Schedule: daily snapshot backups using Zstandard compression.
- Retention: 7 daily, 4 weekly, and 3 monthly.
- Restore: `dns01` restored to a temporary VM on normal VM storage.
- Isolation: restored network adapter removed before startup.
- Guest validation: Debian booted; root filesystem present; `pihole-FTL` active; Node Exporter active.
- Cleanup: temporary restored VM deleted after shutdown.

The isolated restore did not validate client DNS traffic or remote monitoring because the network adapter was intentionally absent. Those checks remain part of a controlled network-connected recovery or actual replacement recovery.

## Lessons Learned

- Device identification must be completed before any destructive storage command.
- Manufacturer capacity and Linux-reported usable capacity use different units; the observed usable space was expected.
- SMART health plus an extended self-test provides stronger initial evidence than filesystem creation alone.
- Stable UUID mounting is safer than relying on `/dev/sdX` naming.
- Proxmox mount-point enforcement is a critical safeguard for removable backup storage.
- A temporary restore must be isolated before boot when the source VM is still active.
- Service validation should distinguish local boot and process state from end-to-end network behavior.
- A nonessential hardware-management service failure inside a virtual machine does not automatically invalidate the restore, but failed units must be assessed individually.
- Backup maturity should be documented per guest: `dns01` has a tested restore; `mon01` currently has backup coverage without an independent restore test.

## Remaining Work

- Observe the first scheduled backup run and ongoing pruning behavior.
- Add backup-age, task-failure, and capacity monitoring through a least-privilege Proxmox integration.
- Define an actionable backup-job failure notification path.
- Perform an independent `mon01` restore test when operationally useful.
- Perform a controlled network-connected `dns01` recovery test when duplicate identity risk can be removed.
- Add a second failure-domain copy, such as offline rotation, off-site storage, a NAS, or Proxmox Backup Server, when justified.
- Export and privately validate the Homelab Infrastructure Overview dashboard as a portable recovery asset.

## Related Documentation

- [Change Records Index](README.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Storage Architecture](../architecture/storage.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Proxmox VE Platform](../services/proxmox.md)