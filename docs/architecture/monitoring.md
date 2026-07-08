# Monitoring and Observability

## Purpose

This document describes the monitoring, logging, and alerting strategy for the homelab. Monitoring should help identify failures, explain performance issues, and create operational habits similar to a small production environment.

## Current Status

Monitoring is planned but not yet fully implemented. The immediate goal is to define what should eventually be monitored before adding tools.

Monitoring should start small and answer practical questions:

- Is the infrastructure reachable?
- Are important services running?
- Are hosts running out of CPU, memory, disk, or network capacity?
- Did backups run successfully?
- Are there security-relevant events worth investigating?

## Design Goals

- Detect service failures and host issues early.
- Track resource usage trends for capacity planning.
- Practice operational monitoring concepts used in professional environments.
- Keep monitoring useful without overcomplicating the initial build.
- Document alerts so future troubleshooting is faster.

## Monitoring Scope

| Area | What to Monitor | Why It Matters |
| --- | --- | --- |
| Network | Gateway reachability, switch availability, DNS/DHCP health | Connectivity issues affect every service |
| Proxmox host | CPU, memory, disk, uptime, updates, VM state | Hypervisor health affects all workloads |
| Storage | Disk usage, storage pool health, backup target availability | Storage failures can cause data loss |
| Services | Uptime, ports, HTTP checks, process health | Confirms services are usable |
| Backups | Job success, failure, age, restore tests | Backups are only useful if they can be trusted |
| Security events | Authentication failures, unexpected exposure, suspicious logs | Supports future defensive security projects |

## Tooling Direction

Specific tools should be selected based on the problem being solved. The initial stack may eventually include:

- Host metrics collection.
- Service uptime checks.
- Centralized dashboards.
- Log collection.
- Alert routing.
- Backup job monitoring.

Tool choices should be documented in service pages and architecture decision records once selected.

## Alerting Philosophy

Alerts should be actionable. An alert should usually answer:

- What failed?
- Why does it matter?
- What should be checked first?
- Is there a runbook?

Avoid creating alerts that are noisy, unclear, or ignored. A small number of useful alerts is better than a large number of low-value alerts.

## Dashboard Philosophy

Dashboards should support troubleshooting and capacity planning. Good dashboards should show:

- Current host health.
- Service availability.
- Storage usage.
- Network status.
- Backup status.
- Recent security-relevant events where appropriate.

Dashboards should avoid exposing sensitive values in screenshots or public documentation.

## Logging Strategy

Centralized logging is a future improvement. When implemented, documentation should include:

- Which systems send logs.
- Where logs are stored.
- Retention period.
- Access controls.
- Security-relevant event sources.
- Privacy and sanitization considerations.

Logs may contain sensitive information and should not be committed to the repository.

## Security Considerations

- Monitoring tools often have broad visibility and should be protected.
- Dashboards should not be exposed publicly without strong authentication.
- Alert destinations should not leak sensitive infrastructure details.
- Logs should be treated as potentially sensitive.
- Security lab systems should be monitored without allowing them to control trusted infrastructure.

## Future Improvements

- Select and document the initial monitoring stack.
- Create a monitoring service page.
- Add host and service dashboards.
- Add backup job monitoring.
- Add alert routing for critical failures.
- Add security detection experiments after segmentation is in place.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Storage Architecture](storage.md)
- [Security Architecture](security.md)
