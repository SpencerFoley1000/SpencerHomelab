# Runbooks

Runbooks document repeatable operational procedures.

A good runbook should allow future me to perform a task safely without reconstructing the entire reasoning process from memory.

## Runbook Standards

Each operational runbook should include:

- Purpose
- Status and last validation date where practical
- Preconditions
- Required access
- Procedure
- Validation steps
- Rollback or recovery notes
- Related documentation

Use the [Runbook Template](TEMPLATE.md) when creating a new procedure.

## Current Runbooks

| Runbook | Status | Notes |
| --- | --- | --- |
| [Prometheus Scrape Target Troubleshooting](prometheus-scrape-target-troubleshooting.md) | Operational / tested | Created from a real Prometheus configuration incident and validated during recovery. |
| [QEMU Guest Agent Troubleshooting](qemu-guest-agent-troubleshooting.md) | Operational / tested | Created from a real missing virtio guest-agent device incident. |
| [Adding a Service](adding-service.md) | Operational checklist | Repeatable deployment and documentation checklist for new services. |
| [VM Provisioning](vm-provisioning.md) | Baseline checklist | General VM creation process; expand as provisioning standards mature. |
| [Maintenance](maintenance.md) | Draft baseline | General maintenance sequence; not yet a tested environment-specific procedure. |
| [Backup](backup.md) | Planned | Backup platform, schedule, retention, and restore testing are not yet implemented. |
| [Disaster Recovery](disaster-recovery.md) | Planned | Recovery order is documented at a high level but has not yet been tested. |

Planned or draft documents must not be treated as validated recovery procedures until the relevant infrastructure exists and a test has been completed.

## Related Documentation

- [Runbook Template](TEMPLATE.md)
- [Services Documentation](../services/)
- [Projects](../projects/)
- [Architecture Documentation](../architecture/)
- [Changelog](../../CHANGELOG.md)
