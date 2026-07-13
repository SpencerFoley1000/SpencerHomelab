# Storage Architecture

## Purpose

This document describes storage design decisions, current recovery assets, and backup requirements for the homelab. It is intended to make future storage changes easier to understand and safer to operate.

## Current Status

Storage and recovery work is in active implementation under Project 003.

Completed during Phase 003A:

- Inventoried critical service and configuration state for `dns01` and `mon01`.
- Created and privately inspected a Pi-hole Teleporter export.
- Created and privately inspected Grafana dashboard exports.
- Classified Prometheus, Blackbox Exporter, Grafana, and Node Exporter state by recovery importance.
- Documented preliminary recovery order and manual rebuild requirements.
- Added a service configuration export and inspection runbook.

Current implementation state:

- The active Proxmox host uses a local 1 TB PCIe SSD for its system and VM storage.
- A 5 TB external hard drive has been acquired as the first dedicated Proxmox backup target.
- The drive still requires connection, filesystem preparation, mounting, Proxmox storage registration, scheduling, retention policy, initial backups, and restore testing.
- Protected VM backups are not yet considered proven.

The storage design must answer:

- Where does each workload store its state?
- Which state must be protected and which can be rebuilt?
- Which backup layer is appropriate: VM backup, application export, configuration copy, or documentation?
- How would the service be validated after restoration?

## Design Goals

- Store service data in predictable locations.
- Separate system storage from backup storage.
- Define what must be backed up versus what can be rebuilt.
- Combine whole-VM backups with portable application-level recovery assets where useful.
- Practice restore-first thinking rather than backup-only thinking.
- Protect backup targets from untrusted or experimental workloads.
- Avoid exposing disk serial numbers, exact labels, mount paths, or personal dataset names.

## Current Storage Components

| Component | Role | Current status | Public documentation boundary |
| --- | --- | --- | --- |
| Proxmox host 1 TB PCIe SSD | Hypervisor, local VM disks, ISOs, and current service state | Active | Exact device and storage identifiers omitted |
| 5 TB external HDD | Planned Proxmox backup destination for core VMs | Acquired; integration pending | Model and serial number omitted unless later needed for a documented technical decision |
| Private administrative-workstation storage | Temporary protected location for application exports and hashes | Active interim recovery layer | Exact paths, usernames, hashes, and identifiers omitted |
| GitHub repository | Sanitized architecture, service, project, runbook, ADR, and change documentation | Active | No raw secrets or private exports |
| Two 1 TB NVMe devices | Planned local storage for the future dedicated server | Acquired; role and layout pending validation | Exact serial numbers and final pool names omitted |

## Storage Categories

| Category | Purpose | Recovery expectation |
| --- | --- | --- |
| Hypervisor system storage | Proxmox operating system and host configuration | Rebuildable from documentation; selected host state should be recorded privately |
| VM and container disks | Workload operating systems and application data | Stable workloads require protected VM backups and restore testing |
| Service configuration | Pi-hole, Prometheus, Blackbox Exporter, Grafana, and future service configuration | Protect through VM backup, reviewed copies, or application export as appropriate |
| Application exports | Pi-hole Teleporter and Grafana dashboard JSON | Portable recovery layer; must remain private and be import-tested |
| Metrics history | Prometheus local time-series data | Lower priority than configuration at current scale; retention should be intentional |
| Replaceable content | Package files, Grafana plugins, ISOs, and caches | Reinstall or redownload unless custom requirements exist |
| Backup storage | Dedicated external destination for important workloads | Must be separate from source storage, access-controlled, monitored, and restore-tested |
| Documentation | Sanitized operational knowledge and architecture | Version-controlled in GitHub; not a substitute for protected service state |

## Project 003 Recovery Assets

### `dns01`

Current recovery layers:

1. Planned Proxmox VM backup to the 5 TB external target.
2. Protected Pi-hole Teleporter export.
3. Sanitized service and network documentation.
4. Package, service, static-networking, and validation inventory.

The Teleporter archive passed integrity checks and private sensitivity inspection. Import validation remains pending.

### `mon01`

Current recovery layers:

1. Planned Proxmox VM backup to the 5 TB external target.
2. Prometheus and Blackbox Exporter configuration inventory.
3. Grafana database and data-source recovery mapping.
4. Protected Node Exporter and Homelab Service Health dashboard exports.
5. Sanitized service, architecture, and troubleshooting documentation.

The Homelab Infrastructure Overview is operational but still requires a private Classic JSON export and validation.

## Backup Target Implementation Requirements

Before the 5 TB drive is considered operational backup storage:

1. Inspect the device and confirm expected capacity.
2. Record the device identity privately without committing serial numbers.
3. Select and document the filesystem and mount strategy.
4. Use a stable private identifier for mounting.
5. Add the target to Proxmox using a sanitized public storage label.
6. Restrict content types and write access to intended backup operations.
7. Define protected VMs.
8. Define schedule, retention, and pruning behavior.
9. Run initial backups and validate completion and artifact size.
10. Restore at least one representative VM in an isolated or controlled state.
11. Document recovery validation and lessons learned.

## Backup Philosophy

Backups are designed around restore requirements, not only scheduled copies.

For each stable service, documentation must identify:

- Critical state.
- Backup method.
- Destination.
- Frequency.
- Retention.
- Restore order.
- Post-restore validation.
- Last successful restore-test date.

A backup that has never been restored should be treated as unproven.

Application exports do not replace VM backups, and VM backups do not replace understanding service dependencies and configuration.

## Recovery Priority

Current infrastructure recovery order:

1. Physical network and Proxmox management access.
2. `dns01`, followed by public and local DNS validation.
3. `mon01`, followed by Prometheus, both Blackbox DNS jobs, and Grafana validation.
4. Confirm `pve01`, `dns01`, and `mon01` monitoring state.
5. Restore lower-priority or experimental workloads.

## Public Documentation Rules

Do not publish:

- Disk serial numbers.
- Device asset tags.
- Exact private mount paths that reveal personal information.
- Personal dataset names.
- Raw backup storage identifiers when unnecessary.
- Cloud backup account identifiers.
- Private hashes when they provide no public documentation value.
- Encryption keys or recovery material.
- Raw application exports.

Use placeholders when needed:

- `<PRIMARY_DATASTORE>`
- `<VM_STORAGE>`
- `<BACKUP_TARGET>`
- `<BACKUP_MOUNT>`
- `<PRIVATE_EXPORT_ROOT>`
- `<ENCRYPTION_KEY_STORED_IN_PASSWORD_MANAGER>`

## Security Considerations

- Backup targets should not be writable from every workload.
- Sensitive backups should be encrypted where practical.
- Recovery keys must be stored outside the repository.
- Administrative storage interfaces should remain internal-only.
- Backup credentials should be unique and stored in a password manager.
- Security-lab workloads should not be allowed to modify trusted backup storage.
- Raw Pi-hole and Grafana exports must remain outside Git.
- The external backup drive should be mounted and exposed only as broadly as required.
- A single directly attached drive improves recoverability but is not a complete off-site or immutable backup strategy.

## Maintenance Notes

After backup implementation:

- Review free capacity and retention regularly.
- Validate backup job results rather than assuming scheduled execution means success.
- Record failed jobs and their resolution.
- Re-test restoration after major Proxmox or service-version changes.
- Replace application exports after meaningful configuration changes.
- Remove obsolete private artifacts intentionally.
- Document drive replacement, filesystem changes, or storage-layout changes.

## Future Improvements

- Integrate the 5 TB external drive into Proxmox.
- Define schedule, retention, pruning, and capacity thresholds.
- Run initial backups for `dns01` and `mon01`.
- Complete and document a representative isolated restore test.
- Expand the backup and disaster-recovery runbooks from tested results.
- Add backup-job and backup-age monitoring.
- Export and privately validate the Homelab Infrastructure Overview.
- Document the future server's validated storage layout.
- Evaluate a second backup copy, offline rotation, NAS, or Proxmox Backup Server only when justified by recovery requirements.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Security Architecture](security.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Service Configuration Export and Inspection](../runbooks/service-config-export.md)
- [Hardware Inventory](../hardware/inventory.md)
