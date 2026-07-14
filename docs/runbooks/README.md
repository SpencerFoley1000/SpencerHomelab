# Runbooks

Runbooks document repeatable operational procedures.

A good runbook should allow future me to perform a task safely without reconstructing the entire reasoning process from memory.

## Runbook Standards

Each operational runbook should include:

- Purpose
- Lifecycle status and last validation date where practical
- Preconditions and required access
- Safety and security notes
- Procedure
- Validation steps
- Rollback or recovery notes
- Documentation requirements
- Related documentation

Use the [Runbook Template](TEMPLATE.md) when creating a new procedure.

## Maturity Definitions

| Status | Meaning |
| --- | --- |
| Operational / tested | Procedure was exercised successfully in the documented environment |
| Operational baseline | Representative parts were exercised successfully; some scenario-specific validation remains |
| Operational checklist | Creation or inspection steps were exercised, but full recovery was not validated |
| Baseline checklist | Individual steps were used, but the complete standardized process is still maturing |
| Draft baseline | Environment-specific guidance exists but has not been exercised end to end |
| Planned | Infrastructure or testing required for validation does not yet exist |
| Retired | Procedure is retained only for history and should not be used for current operations |

## Current Runbooks

| Runbook | Status | Notes |
| --- | --- | --- |
| [Prometheus Scrape Target Troubleshooting](prometheus-scrape-target-troubleshooting.md) | Operational / tested | Created from a real Prometheus configuration incident and validated during recovery. |
| [QEMU Guest Agent Troubleshooting](qemu-guest-agent-troubleshooting.md) | Operational / tested | Created from a real missing virtio guest-agent device incident. |
| [Proxmox VM Restore](proxmox-vm-restore.md) | Operational / tested | `dns01` was restored to an isolated temporary VM, booted, locally validated, and removed. |
| [Backup](backup.md) | Operational / tested | Dedicated backup storage, initial backups, scheduling, retention, and representative restore validation are complete. |
| [Disaster Recovery](disaster-recovery.md) | Operational baseline | Recovery order is documented and the `dns01` whole-VM path is tested; connected-service and `mon01` recovery remain less mature. |
| [Service Configuration Export and Inspection](service-config-export.md) | Operational checklist | Pi-hole Teleporter and Grafana export creation and private inspection were exercised; imports remain untested. |
| [Adding a Service](adding-service.md) | Operational checklist | Repeatable deployment and documentation checklist for new services. |
| [VM Provisioning](vm-provisioning.md) | Baseline checklist | Grounded in `dns01` and `mon01`; further standardization remains useful. |
| [Maintenance](maintenance.md) | Draft baseline | Includes current Proxmox, monitoring, DNS, authentication, backup, and rollback checks but is not yet validated as a complete maintenance window. |

A tested procedure should state exactly what the test proved. Network-isolated restore validation does not automatically prove production network behavior.

## Current Runbook Gaps

- Proxmox maintenance and management-access recovery.
- Backup-job failure notification and response after automated monitoring exists.
- DNS failure response and future alert handling.
- UPS power-loss, graceful-shutdown, and recovery procedure after Project 005.
- VM decommissioning.
- Independent `mon01` restore validation.

## Related Documentation

- [Runbook Template](TEMPLATE.md)
- [Services Documentation](../services/)
- [Projects](../projects/)
- [Architecture Documentation](../architecture/)
- [Architecture Decision Records](../decisions/)
- [Infrastructure Change Records](../changes/)
- [Changelog](../../CHANGELOG.md)