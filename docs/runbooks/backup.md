# Backup Runbook

## Purpose

Define the operational backup design, routine validation, failure handling, and maintenance process for stable homelab workloads.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational / tested |
| Project | Project 003: Backup and Recovery |
| Backup target | Dedicated 5 TB external ext4 filesystem registered in Proxmox |
| Protected VMs | `dns01`, `mon01` |
| Initial backups | Completed successfully |
| Restore validation | `dns01` isolated restore completed successfully |
| Last reviewed | 2026-07-14 |

This runbook uses sanitized placeholders. Exact drive identifiers, filesystem UUIDs, Proxmox storage labels, backup filenames, and internal addresses remain private.

## Backup Principles

- Keep backup storage separate from source storage.
- Combine whole-VM backups with portable application exports where useful.
- Treat backup artifacts as sensitive system state.
- Prefer tested restore procedures over assumptions based only on successful jobs.
- Document what is protected, how often, how long, and how restoration is validated.
- Do not expose backup storage to untrusted or attacker-style workloads.
- Recognize that one connected local disk is not immutable, offline, or off-site protection.

## Current Backup Scope

| System or asset | Protection method | Destination | Current maturity |
| --- | --- | --- | --- |
| `dns01` VM | Proxmox full-VM backup | `<BACKUP_TARGET>` | Daily backup active; isolated whole-VM restore tested |
| Pi-hole configuration | Protected Teleporter ZIP | Private recovery storage | Export integrity-checked and privately inspected; import not independently tested |
| `mon01` VM | Proxmox full-VM backup | `<BACKUP_TARGET>` | Daily backup active; independent restore not yet tested |
| Prometheus and Blackbox configuration | VM backup plus reviewed inventory | `<BACKUP_TARGET>` and protected private records | Backup active; manual rebuild requirements documented |
| Grafana database and data-source mapping | VM backup plus protected recovery mapping | `<BACKUP_TARGET>` and protected private records | Backup active; data-source mapping documented |
| Existing Grafana dashboards | Protected JSON exports | Private recovery storage | Existing exports syntax-checked and privately inspected |
| Homelab Infrastructure Overview | Future protected Classic JSON export | Private recovery storage | Export remains follow-up work |
| Documentation repository | Git history and GitHub | GitHub | Active; does not replace service-state backups |

## Backup Target Design

| Setting | Current design |
| --- | --- |
| Physical target | Dedicated 5 TB external HDD |
| Filesystem | ext4 |
| Mount method | Persistent filesystem UUID |
| Public mount reference | `<BACKUP_MOUNT>` |
| Proxmox storage reference | `<BACKUP_TARGET>` |
| Storage type | Directory storage |
| Content type | Backup only |
| Missing-mount protection | Proxmox mount-point enforcement enabled |
| Approximate usable capacity | Multi-terabyte capacity consistent with a 5 TB marketed device |

The target passed SMART overall-health validation and an extended SMART self-test before use.

## Scheduled Job

| Setting | Value |
| --- | --- |
| Guests | `dns01`, `mon01` |
| Schedule | Daily at 10:00 local time |
| Mode | Snapshot |
| Compression | Zstandard |
| Keep daily | 7 |
| Keep weekly | 4 |
| Keep monthly | 3 |
| Repeat missed jobs | Disabled in the initial configuration |
| Notification mode | Proxmox notification system |

Review missed-run behavior if the Proxmox host is not consistently online at the scheduled time.

## Pre-Backup Checks

Before a manual backup or troubleshooting a scheduled job:

1. Confirm the target is mounted:

   ```bash
   findmnt <BACKUP_MOUNT>
   ```

2. Confirm expected capacity:

   ```bash
   df -h <BACKUP_MOUNT>
   ```

3. Confirm Proxmox reports the target active:

   ```bash
   pvesm status
   ```

4. Confirm the stable VMs are present and healthy:

   ```bash
   qm list
   ```

5. Confirm there is enough free capacity for another full backup.
6. Confirm no hardware or filesystem errors are under investigation.

Do not manually create the mount directory as a substitute when the external filesystem is absent. Mount-point enforcement is intended to make that condition fail visibly.

## Manual Backup Procedure

Run a manual backup when validating a new guest, testing after a major change, or retrying a failed scheduled job:

```bash
vzdump <VM_ID> \
  --storage <BACKUP_TARGET> \
  --mode snapshot \
  --compress zstd
```

Expected completion evidence:

```text
INFO: Backup finished successfully
```

Confirm the artifact exists:

```bash
pvesm list <BACKUP_TARGET>
```

Repeat for each intended guest.

VM IDs and exact artifact names should be recorded privately, not in public documentation.

## Scheduled Job Verification

View the configured jobs in a readable format:

```bash
pvesh get /cluster/backup --output-format yaml
```

Verify:

- Job is enabled.
- Node is correct.
- Storage is `<BACKUP_TARGET>`.
- Both `dns01` and `mon01` are included.
- Mode is snapshot.
- Compression is Zstandard.
- Schedule is daily at the intended local time.
- Retention is 7 daily, 4 weekly, and 3 monthly.

The default table output may be wider than a terminal. YAML or pretty JSON is preferred for inspection.

## Routine Validation

After each scheduled or manual run, verify:

- Task completed successfully.
- An artifact exists for each intended guest.
- Artifact size is plausible relative to guest usage.
- Target free capacity remains healthy.
- No unexpected warnings appear.
- The previous known-good artifacts remain present.
- Retention and pruning do not remove more history than intended.

Useful commands:

```bash
pvesm status
pvesm list <BACKUP_TARGET>
df -h <BACKUP_MOUNT>
```

## Restore Validation

At least one representative isolated restore is required for an operational backup design.

Project 003 validated `dns01` by:

- Restoring to an unused temporary VM ID.
- Writing the restored disk to normal VM storage.
- Renaming the VM as a restore test.
- Removing `net0` before the first boot.
- Confirming Debian booted.
- Confirming the expected filesystem existed.
- Confirming `pihole-FTL` and Node Exporter were active.
- Shutting down and deleting the temporary VM.

See [Proxmox VM Restore](proxmox-vm-restore.md) for the tested procedure.

The isolated test did not validate client DNS traffic, local DNS responses, remote metrics, or Blackbox probes because the restored VM had no network adapter. Those checks require a controlled network-connected test or an actual replacement recovery.

## Backup Failure Handling

If a job fails:

1. Do not delete the last known-good backup.
2. Confirm `<BACKUP_MOUNT>` is a real mounted filesystem.
3. Confirm `<BACKUP_TARGET>` is active in Proxmox.
4. Check free capacity and inode availability.
5. Review the Proxmox task result and relevant system logs.
6. Confirm the source VM is healthy.
7. Check for USB disconnects, I/O errors, filesystem errors, or power instability.
8. Correct the narrowest identified issue.
9. Run a manual backup for the affected VM.
10. Confirm the artifact exists and update documentation if a permanent change was required.

Useful host checks:

```bash
findmnt <BACKUP_MOUNT>
df -h <BACKUP_MOUNT>
pvesm status
journalctl -p warning..alert --since today
```

Do not disable mount-point enforcement to make a failed job appear successful.

## Capacity and Retention Maintenance

Review periodically:

- Total and available capacity.
- Backup growth by VM.
- Oldest and newest recovery points.
- Pruning behavior.
- Whether the daily, weekly, and monthly mix still matches recovery needs.
- Whether new stable VMs were added to the job.
- Whether retired VMs still consume retention capacity.

Capacity thresholds should be added to monitoring after a least-privilege Proxmox metrics design exists.

## Drive Health Maintenance

Review SMART information periodically and after unusual I/O behavior:

```bash
smartctl -a <BACKUP_DEVICE>
```

Run an extended test during a suitable maintenance window:

```bash
smartctl -t long <BACKUP_DEVICE>
smartctl -l selftest <BACKUP_DEVICE>
```

The exact device path and serial number remain private. Do not run destructive filesystem repair commands without confirming the target and preserving available evidence.

## Application-Level Recovery Assets

Whole-VM backups do not remove the need to maintain:

- Pi-hole Teleporter exports after meaningful DNS changes.
- Grafana dashboard exports after meaningful dashboard changes.
- Prometheus and Blackbox configuration inventories.
- Grafana data-source recovery mapping.
- Package and service baselines.
- Sanitized rebuild instructions.

Raw exports remain outside Git because they may contain credentials, private addressing, leases, identifiers, and operational state.

## Security Considerations

- Treat every VM backup as sensitive.
- Keep exact UUIDs, serial numbers, paths, backup names, hashes, and identifiers outside Git.
- Restrict target write access to trusted backup operations.
- Keep security-lab systems away from trusted backup storage.
- Do not expose the backup target through unnecessary network shares.
- Use a separate failure-domain copy later for stronger ransomware, physical-loss, and operator-error resilience.
- Store any future encryption keys independently from the backup media.

## Known Limitations

- The current drive is directly attached and normally connected to the Proxmox host.
- It is not immutable, offline, or off-site.
- Full backups do not provide Proxmox Backup Server deduplication.
- `mon01` has not been independently restored.
- Missed scheduled runs are not repeated automatically in the initial configuration.
- Backup task and backup-age alerting are not yet implemented.

## Documentation Requirements

After a meaningful backup change or restore test, update:

- [Project 003](../projects/project-003-backup-recovery.md).
- [Storage Architecture](../architecture/storage.md).
- [VM Inventory](../architecture/vm-inventory.md).
- [Proxmox VE Platform](../services/proxmox.md).
- [Disaster Recovery](disaster-recovery.md).
- The relevant ADR or dated change record.
- `CHANGELOG.md`.
- `ROADMAP.md` when priorities or milestones change.

Run the repository Markdown link validator from a local clone:

```bash
python scripts/check-markdown-links.py
```

## Related Documentation

- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [Disaster Recovery](disaster-recovery.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Proxmox VE Platform](../services/proxmox.md)