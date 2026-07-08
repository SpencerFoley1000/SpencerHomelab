# Storage Architecture

## Purpose

This document describes storage design decisions, assumptions, and recovery considerations for the homelab. It is intended to make future storage changes easier to understand and safer to operate.

## Current Status

Storage is currently in the baseline documentation phase. The initial focus is on local virtualization storage and future backup planning.

The storage design should eventually answer three practical questions:

- Where does each workload store its data?
- What data must be backed up?
- How would the workload be restored after failure?

## Design Goals

- Store service data in predictable locations.
- Separate system disks from application data where practical.
- Define what must be backed up versus what can be rebuilt.
- Practice restore-first thinking rather than backup-only thinking.
- Avoid exposing disk serial numbers, exact labels, or personal dataset names.

## Storage Categories

| Category | Purpose | Recovery Expectation |
| --- | --- | --- |
| Hypervisor system storage | Proxmox operating system and host configuration | Rebuildable with documentation and backups |
| VM and container disks | Workload operating systems and application data | Should be backed up for stable workloads |
| Configuration data | Service configs, compose files, scripts, and notes | Should be versioned or backed up |
| Bulk data | Large files, ISOs, test datasets, media, or lab artifacts | Backup depends on importance |
| Backup storage | Backup destination for important workloads | Must be protected from accidental loss |

## Public Documentation Rules

Do not publish:

- Disk serial numbers.
- Device asset tags.
- Exact storage paths that reveal personal information.
- Personal dataset names.
- Cloud backup account identifiers.
- Encryption keys or recovery material.

Use placeholders when needed:

- `<PRIMARY_DATASTORE>`
- `<VM_STORAGE>`
- `<BACKUP_TARGET>`
- `<CONFIG_REPOSITORY>`
- `<ENCRYPTION_KEY_STORED_IN_PASSWORD_MANAGER>`

## Backup Philosophy

Backups should be designed around restore requirements, not just scheduled copies.

For each stable service, future service documentation should identify:

- What data must be backed up.
- Where the backup is stored.
- How often backups run.
- How long backups are retained.
- How to restore the service.
- When restore testing was last performed.

A backup that has never been restored should be treated as unproven.

## Initial Backup Priorities

Early backup planning should prioritize:

1. Proxmox host configuration notes.
2. VM and container definitions for stable workloads.
3. Service configuration files.
4. Documentation repository content.
5. Monitoring and security tooling configuration after those services are deployed.

Temporary experiments do not need the same backup level unless they become stable services.

## Future NAS / Shared Storage Considerations

A future NAS or dedicated backup server may be useful if the lab outgrows local storage.

Potential use cases:

- Central backup target.
- Shared ISO/template storage.
- Long-term service data.
- Restore testing environment.
- Separation of compute and storage responsibilities.

A NAS should not be added just to add complexity. It should solve a documented storage or recovery problem.

## Security Considerations

- Backup targets should not be writable from every workload.
- Sensitive backups should be encrypted where practical.
- Recovery keys must be stored outside the repository.
- Administrative storage interfaces should remain internal-only.
- Backup credentials should be unique and stored in a password manager.
- Security lab workloads should not be allowed to modify trusted backup storage.

## Future Improvements

- Document actual storage devices using sanitized labels.
- Define a retention policy for stable workloads.
- Add backup and restore runbooks.
- Add restore test records for important services.
- Evaluate whether a dedicated NAS or backup host is justified.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [Security Architecture](security.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
