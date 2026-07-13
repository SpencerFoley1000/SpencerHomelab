# VM Inventory

## Purpose

This inventory tracks virtual machines that are intentionally part of the homelab environment.

The goal is to document what exists, why it exists, where it runs, how it is monitored, and how mature its recovery path is. Exact IP addresses and sensitive implementation details are intentionally sanitized for public documentation.

## Inventory Standards

Each VM should document:

- Hostname
- Purpose
- Platform
- Operating system
- Resource allocation
- Network placement
- IP assignment model
- Lifecycle status
- Backup and recovery maturity
- Recovery priority
- Monitoring coverage
- Documentation links

Avoid publishing:

- Exact internal IPs unless intentionally sanitized.
- MAC addresses.
- VM IDs unless there is a documented reason.
- Personal usernames.
- Secrets, tokens, keys, or passwords.
- Hostnames that reveal personally identifying information.

## Active Virtual Machines

| Hostname | Purpose | Platform | OS | vCPU | RAM | Disk | Network | IP model | Lifecycle | Backup and recovery maturity | Monitoring | Documentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and DNS filtering | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 2 GB | 20 GB | Homelab LAN | Static, sanitized as `<DNS01_IP>` | Active | VM backup pending; Teleporter export integrity-checked and privately inspected; restore/import untested | Node Exporter plus separate recursive and local Blackbox DNS probes | [Pi-hole](../services/pihole.md), [Node Exporter](../services/node-exporter.md), [Blackbox Exporter](../services/blackbox-exporter.md) |
| `mon01` | Monitoring and observability stack | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 3 GB | 32 GB | Homelab LAN | Static, sanitized as `<MON01_IP>` | Active | VM backup pending; service configuration, Grafana state, data-source mapping, and existing dashboard exports inventoried; restore untested | Prometheus self-monitoring, local Node Exporter, and Blackbox Exporter service state; monitors `dns01` and `pve01` | [Project 002](../projects/project-002-monitoring-observability.md), [Prometheus](../services/prometheus.md), [Grafana](../services/grafana.md), [Blackbox Exporter](../services/blackbox-exporter.md) |

Project status and VM lifecycle are tracked separately. Project 002 remains active for enhancements while `mon01` itself is stable infrastructure.

## Recovery Priority

| Priority | VM | Reason | Required post-restore validation |
| --- | --- | --- | --- |
| High | `dns01` | Provides internal DNS and local records used by homelab services | Pi-hole service, public DNS, local DNS, Node Exporter, `blackbox_dns`, and `blackbox_dns_local` |
| Medium | `mon01` | Provides monitoring visibility and troubleshooting data but is not required for core connectivity | Prometheus jobs, all Node Exporter targets, both Blackbox modules/jobs, Grafana data source, and dashboards |

Recovery priority should be revisited after additional services depend on authentication, reverse proxying, backup infrastructure, or monitoring-based automation.

## Naming Convention

Current naming convention:

```text
<role><number>
```

Examples:

- `dns01` - DNS service
- `mon01` - Monitoring service
- `pbs01` - Backup service
- `proxy01` - Reverse proxy service

This format is short, readable, and easy to expand as the lab grows.

## Operational Notes

- `dns01` is the first production-style infrastructure VM.
- `mon01` is the dedicated monitoring VM for Project 002.
- `mon01` memory was increased from 2 GB to 3 GB after Grafana showed sustained memory usage near the original allocation.
- Monitoring is intentionally separated from DNS to avoid combining unrelated infrastructure roles on `dns01`.
- QEMU Guest Agent is installed on both stable Debian VMs.
- Project 003A documented portable recovery assets and preliminary rebuild requirements for both VMs.
- The 5 TB external drive is the planned VM-backup target but is not yet integrated.
- Future infrastructure VMs should be added here before their deployment is considered complete.
- Experimental VMs should be clearly labeled as experimental or temporary.
- Backup status must be updated after each successful backup or restore milestone.

## Future Improvements

- Add service tier, recovery-time objective, and recovery-point objective where useful.
- Add backup schedule, retention, latest successful backup, and last restore-test date.
- Add sanitized Proxmox node placement if additional nodes are introduced.
- Add monitoring and backup status for future infrastructure VMs during onboarding.
- Link VM entries to relevant runbooks, change records, and ADRs.

## Related Documentation

- [Virtualization Architecture](virtualization.md)
- [Network Architecture](network.md)
- [Monitoring and Observability](monitoring.md)
- [Storage Architecture](storage.md)
- [Proxmox Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Hardware Inventory](../hardware/inventory.md)
