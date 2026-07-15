# Backup Runbook

## Purpose

Define the operational backup design, routine validation, failure handling, and maintenance process for stable homelab workloads.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational / tested |
| Project | Project 003: Backup and Recovery, extended by Project 004 |
| Backup target | Dedicated 5 TB external ext4 filesystem registered in Proxmox |
| Protected VMs | `dns01`, `mon01`, `proxy01` |
| Initial backups | Completed successfully |
| Restore validation | Isolated `dns01` and `proxy01` restores completed successfully |
| Last reviewed | 2026-07-14 |

This runbook uses sanitized placeholders. Exact drive identifiers, filesystem UUIDs, Proxmox storage labels, backup filenames, VM IDs, certificate keys, and internal addresses remain private.

## Backup Principles

- Keep backup storage separate from source storage.
- Combine whole-VM backups with portable application exports and protected PKI assets where useful.
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
| Existing Grafana dashboards | Protected JSON exports | Private recovery storage | Existing exports syntax-checked and privately inspected; Infrastructure Overview refresh pending after Project 004 |
| `proxy01` VM | Proxmox full-VM backup | `<BACKUP_TARGET>` | Daily backup active; isolated whole-VM restore tested |
| NGINX Proxy Manager state | Included in `proxy01` VM backup | `<BACKUP_TARGET>` | Database, route definitions, imported service certificate, and persistent directories restored successfully |
| Root CA private key | Encrypted protected copy outside VM backup | Private PKI storage | Primary protected copy exists; second failure-domain copy remains follow-up work |
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
| Guests | `dns01`, `mon01`, `proxy01` |
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

4. Confirm stable VMs are present and healthy:

   ```bash
   qm list
   ```

5. Confirm enough free capacity exists for another full backup.
6. Confirm no hardware or filesystem errors are under investigation.
7. For proxy or certificate changes, confirm protected PKI material remains outside the VM and repository.

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

VM IDs and exact artifact names should be recorded privately, not in public documentation.

## Scheduled Job Verification

View configured jobs:

```bash
pvesh get /cluster/backup --output-format yaml
```

Verify:

- Job is enabled.
- Node is correct.
- Storage is `<BACKUP_TARGET>`.
- `dns01`, `mon01`, and `proxy01` are included.
- Mode is snapshot.
- Compression is Zstandard.
- Schedule is daily at the intended local time.
- Retention is 7 daily, 4 weekly, and 3 monthly.

## Routine Validation

After each scheduled or manual run, verify:

- Task completed successfully.
- An artifact exists for each intended guest.
- Artifact size is plausible relative to guest usage.
- Target free capacity remains healthy.
- No unexpected warnings appear.
- Previous known-good artifacts remain present.
- Retention and pruning do not remove more history than intended.

Useful commands:

```bash
pvesm status
pvesm list <BACKUP_TARGET>
df -h <BACKUP_MOUNT>
```

## Restore Validation

At least one representative isolated restore is required for an operational backup design.

### `dns01`

Project 003 validated:

- Restore to an unused temporary VM ID.
- Disk restoration to normal VM storage.
- Temporary restore-test name.
- Removal of `net0` before first boot.
- Debian boot and expected filesystem.
- Active `pihole-FTL` and Node Exporter.
- Shutdown and removal of the temporary VM.

The test did not validate client DNS traffic or remote probes.

### `proxy01`

Project 004 validated:

- Restore to an unused temporary VM ID.
- Removal of the network adapter before first boot.
- Debian boot.
- Active Docker, Node Exporter, and QEMU Guest Agent.
- Running NGINX Proxy Manager container.
- Expected TCP listeners on `80`, `81`, `443`, and `9100`.
- HTTP response from the local administration endpoint.
- Presence of Compose, application-data, and certificate directories.
- Shutdown and deletion of the temporary VM.
- Continued production proxy health after cleanup.

The test proved local recovery of NGINX Proxy Manager and imported service-certificate state. It did not validate live network cutover or root CA private-key restoration.

See [Proxmox VM Restore](proxmox-vm-restore.md) for the tested procedure.

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

## Application and PKI Recovery Assets

Whole-VM backups do not remove the need to maintain:

- Pi-hole Teleporter exports after meaningful DNS changes.
- Grafana dashboard exports after meaningful dashboard changes.
- Prometheus and Blackbox configuration inventories.
- Grafana data-source recovery mapping.
- NGINX Proxy Manager Compose and manual rebuild documentation.
- Protected service certificate and private-key copies.
- Encrypted root CA private key and public certificate.
- Separate CA passphrase storage.
- Package and service baselines.
- Sanitized rebuild instructions.

Raw exports and private keys remain outside Git because they may contain credentials, private addressing, leases, identifiers, and operational state.

## Security Considerations

- Treat every VM backup as sensitive.
- `proxy01` backups contain the wildcard service private key and proxy database.
- Keep exact UUIDs, serial numbers, paths, backup names, hashes, and identifiers outside Git.
- Restrict target write access to trusted backup operations.
- Keep security-lab systems away from trusted backup storage and PKI assets.
- Do not expose the backup target through unnecessary network shares.
- Use a separate failure-domain copy later for stronger ransomware, physical-loss, and operator-error resilience.
- Store encryption keys and CA passphrases independently from backup media.

## Known Limitations

- The current drive is directly attached and normally connected to the Proxmox host.
- It is not immutable, offline, or off-site.
- Full backups do not provide Proxmox Backup Server deduplication.
- `mon01` has not been independently restored.
- Missed scheduled runs are not repeated automatically in the initial configuration.
- Backup task and backup-age alerting are not yet implemented.
- Root CA private-key recovery has not been tested and a second failure-domain copy remains required.

## Documentation Requirements

After a meaningful backup change or restore test, update:

- [Project 003](../projects/project-003-backup-recovery.md).
- The affected project, such as [Project 004](../projects/project-004-reverse-proxy-internal-https.md).
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

- [Project 003](../projects/project-003-backup-recovery.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](internal-certificate-lifecycle.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [Disaster Recovery](disaster-recovery.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Proxmox VE Platform](../services/proxmox.md)
