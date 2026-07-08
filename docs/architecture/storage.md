# Storage Architecture

This page documents storage design decisions, assumptions, and recovery considerations.

## Current Status

Status: Planned / baseline documentation pending.

## Goals

- Store service data in predictable locations.
- Separate system disks from application data where practical.
- Define what must be backed up versus what can be rebuilt.
- Practice restore-first thinking rather than backup-only thinking.

## Topics to Document

- Storage devices and roles
- Filesystems or storage pools
- VM disk placement
- Container volume placement
- Backup targets
- Retention policy
- Restore testing process
- Data that is intentionally excluded from backup

## Documentation Rules

- Do not publish disk serial numbers.
- Do not publish personally identifying dataset names.
- Use generalized labels such as `<PRIMARY_DATASTORE>` or `<BACKUP_TARGET>` when needed.

## Related Documentation

- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
