# Backup Runbook

## Purpose

Define how homelab data, configuration, and service state should be backed up and restored.

## Current Status

Status: Planned / baseline procedure pending.

## Backup Principles

- Back up irreplaceable data and important configuration.
- Prefer documented restore procedures over untested backup assumptions.
- Separate data that must be preserved from workloads that can be rebuilt.
- Never commit backup secrets, encryption keys, or credentials to this repository.

## Backup Scope Template

| Item | Backup Required | Frequency | Destination | Restore Tested |
|---|---:|---|---|---:|
| Service configuration | TBD | TBD | `<BACKUP_TARGET>` | No |
| Service data | TBD | TBD | `<BACKUP_TARGET>` | No |
| VM definitions | TBD | TBD | `<BACKUP_TARGET>` | No |
| Documentation repo | Yes | GitHub | GitHub | N/A |

## Procedure

1. Identify systems and data that require backup.
2. Define backup frequency and retention.
3. Store credentials in a password manager or secrets manager.
4. Configure backup jobs.
5. Validate backup completion.
6. Perform a restore test.
7. Document results in the relevant service page and changelog.

## Validation

- Confirm backup job success.
- Confirm backup size is reasonable.
- Confirm restore process works for at least one representative service.

## Related Documentation

- [Storage Architecture](../architecture/storage.md)
- [Disaster Recovery](disaster-recovery.md)
