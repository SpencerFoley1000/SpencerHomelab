# Backup Runbook

## Purpose

Define the current backup design, implementation prerequisites, validation requirements, and documentation process for stable homelab workloads.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Planned implementation baseline |
| Project | Project 003: Backup and Recovery |
| Inventory phase | Complete |
| Backup target | 5 TB external HDD ordered; integration pending |
| VM backups | Not yet configured |
| Restore validation | Not yet completed |
| Last reviewed | 2026-07-12 |

This page is not a validated backup procedure. Replace planned values with tested implementation details as Project 003 progresses.

## Backup Principles

- Back up irreplaceable data and important configuration.
- Keep backup storage separate from source storage.
- Prefer documented restore procedures over untested backup assumptions.
- Combine whole-VM backups with portable application exports where useful.
- Separate data that must be preserved from workloads that can be rebuilt.
- Treat a successful backup job as incomplete evidence until restoration succeeds.
- Never commit backup secrets, drive identifiers, encryption keys, hashes, or raw recovery artifacts to this repository.

## Current Backup Scope

| System or asset | Protection method | Destination | Current maturity |
| --- | --- | --- | --- |
| `dns01` VM | Proxmox VM backup | `<BACKUP_TARGET>` on 5 TB external drive | Pending implementation |
| Pi-hole configuration | Protected Teleporter ZIP | Private recovery storage and future backup target | Exported, integrity-checked, privately inspected; import untested |
| `mon01` VM | Proxmox VM backup | `<BACKUP_TARGET>` on 5 TB external drive | Pending implementation |
| Prometheus and Blackbox configuration | VM backup plus reviewed configuration inventory | `<BACKUP_TARGET>` and protected private records | Inventory complete; restore untested |
| Grafana database and data-source mapping | VM backup plus protected recovery mapping | `<BACKUP_TARGET>` and protected private records | Inventory complete; restore untested |
| Node Exporter dashboard | Protected JSON export | Private recovery storage and future backup target | Syntax and private inspection complete |
| Homelab Service Health dashboard | Protected JSON export | Private recovery storage and future backup target | Syntax and private inspection complete |
| Homelab Infrastructure Overview | Protected Classic JSON export | Private recovery storage and future backup target | Export pending |
| Documentation repository | Git history and GitHub | GitHub | Active; does not replace service-state backups |

## Preconditions

Before integrating the external target:

- The 5 TB drive is physically available.
- The drive has passed visual inspection and capacity verification.
- Important existing data on the drive, if any, has been handled intentionally.
- The selected filesystem and mount strategy are documented privately.
- A stable device identifier is available for mounting.
- Proxmox management access and a physical-console recovery path are available.
- `dns01` and `mon01` are healthy before the first backup.
- Existing application exports remain protected outside Git.

## Target Preparation Procedure

The exact device path, UUID, model, serial number, and mount path must remain private.

1. Identify the intended external drive carefully.
2. Confirm expected capacity before destructive operations.
3. Record the hardware identity privately.
4. Review drive health where supported.
5. Select and create the intended filesystem.
6. Create a stable mount using a private identifier rather than an unstable device path.
7. Confirm ownership and permissions.
8. Mount the filesystem and verify expected free capacity.
9. Add the target to Proxmox using a sanitized storage label such as `<BACKUP_TARGET>`.
10. Restrict the configured content type to the intended backup artifacts.
11. Confirm the target is visible and writable from Proxmox.
12. Reboot or remount-test if required to confirm persistence.

Do not copy literal commands into public documentation until the actual device, filesystem, and mount design are validated and sanitized.

## Backup Job Design

Define and document before enabling scheduled jobs:

- Protected guests: initially `dns01` and `mon01`.
- Backup mode.
- Schedule.
- Compression.
- Retention and pruning.
- Expected backup window.
- Available-capacity thresholds.
- Failure-notification path.
- Whether the external drive remains connected continuously or follows a documented rotation process.

The selected values should balance recoverability, drive capacity, service importance, and the current small number of VMs.

## Initial Backup Procedure

1. Confirm `dns01`, `mon01`, Prometheus, Grafana, and both DNS probes are healthy.
2. Confirm the backup target is mounted and available in Proxmox.
3. Run the first backup manually rather than waiting for a schedule.
4. Observe task output and record only sanitized results.
5. Confirm the task reports success.
6. Confirm an artifact exists for the intended VM.
7. Confirm the artifact size is plausible relative to the guest disk and used space.
8. Repeat for the second core VM.
9. Review target free capacity.
10. Enable the documented schedule only after manual backups succeed.

## Backup Validation

For each protected VM, record privately:

- Backup date and time.
- Guest identity.
- Backup mode.
- Completion status.
- Artifact size.
- Duration.
- Relevant warning or error state.
- Target free capacity after completion.

Public documentation may summarize success, duration category, and lessons learned without exposing exact paths or identifiers.

## Restore Validation

At least one representative isolated restore is required before Project 003 is complete.

The restore test must confirm:

1. The selected backup artifact can be read.
2. The VM can be restored without overwriting the active production guest.
3. The restored VM boots in an isolated or controlled network state.
4. QEMU Guest Agent behavior is checked where applicable.
5. Service state is validated.
6. The restored guest is either safely removed or intentionally promoted through a separate change process.

### `dns01` post-restore checks

- `pihole-FTL` is active and enabled.
- Static networking is correct using protected values.
- Public DNS resolution works.
- Required local records work.
- Node Exporter responds.
- `blackbox_dns` returns success.
- `blackbox_dns_local` returns success and the expected answer.

### `mon01` post-restore checks

- Prometheus, Grafana, Node Exporter, and Blackbox Exporter are active and enabled.
- Prometheus includes `prometheus`, `node_exporter`, `blackbox_dns`, and `blackbox_dns_local`.
- Blackbox includes `dns_udp` and `dns_udp_local`.
- `pve01`, `dns01`, and `mon01` host targets are visible.
- Both DNS probe series return success.
- Grafana data-source health is valid.
- Available protected dashboards display current data.

## Failure Handling

If a backup job fails:

1. Do not delete the last known-good artifact.
2. Confirm the external target is mounted and writable.
3. Confirm available capacity.
4. Review the Proxmox task result and relevant logs.
5. Confirm the source VM is healthy.
6. Correct the narrowest identified issue.
7. Rerun the backup manually.
8. Document the root cause and permanent fix.
9. Update monitoring or runbooks if the failure revealed a missing control.

## Security Considerations

- Keep the target inaccessible to untrusted or security-lab workloads.
- Restrict write access to required backup operations.
- Keep encryption keys and credentials outside Git.
- Do not publish drive serial numbers, UUIDs, exact mount paths, or raw task logs.
- Treat backup artifacts as sensitive because they may contain credentials, tokens, leases, private addresses, and application state.
- Consider an offline, rotated, or second copy later; one always-connected drive is not immutable or off-site protection.

## Documentation Requirements

After implementation or a restore test, update:

- [Project 003](../projects/project-003-backup-recovery.md).
- [Storage Architecture](../architecture/storage.md).
- [VM Inventory](../architecture/vm-inventory.md).
- Relevant service pages.
- [Disaster Recovery Runbook](disaster-recovery.md).
- `CHANGELOG.md`.
- `ROADMAP.md` if a milestone is completed.

Run:

```bash
python scripts/check-markdown-links.py
```

## Related Documentation

- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Disaster Recovery](disaster-recovery.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
