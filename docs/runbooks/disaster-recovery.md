# Disaster Recovery Runbook

## Purpose

Define the process for recovering core homelab services after hardware failure, configuration loss, or major service outage.

## Current Status

Status: Planned / baseline procedure pending.

## Recovery Priorities

1. Restore network access.
2. Restore virtualization management.
3. Restore DNS / identity / reverse proxy services, if deployed.
4. Restore storage and backups.
5. Restore application services in priority order.
6. Validate monitoring and documentation updates.

## Required Information

Sensitive values must not be stored in this repository. Store secrets in a password manager or other secure system.

Document only sanitized references such as:

- `<ROUTER_RECOVERY_NOTES>`
- `<HYPERVISOR_BACKUP_LOCATION>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Procedure Template

1. Identify failure scope.
2. Confirm physical hardware status.
3. Restore network baseline.
4. Restore management access.
5. Restore critical VMs or services.
6. Validate service health.
7. Review logs for recurring errors.
8. Update documentation and changelog with lessons learned.

## Post-Recovery Review

After each incident or recovery test, document:

- What failed
- Root cause, if known
- Recovery steps used
- What worked well
- What needs improvement

## Related Documentation

- [Backup Runbook](backup.md)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../architecture/security.md)
