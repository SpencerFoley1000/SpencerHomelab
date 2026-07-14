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
- Backup filenames or private storage identifiers.
- Hostnames that reveal personally identifying information.

## Active Virtual Machines

| Hostname | Purpose | Platform | OS | vCPU | RAM | Disk | Network | IP model | Lifecycle | Backup and recovery maturity | Monitoring | Documentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and DNS filtering | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 2 GB | 20 GB | Homelab LAN | Static, sanitized as `<DNS01_IP>` | Active | Daily Proxmox backup active; Teleporter export protected; isolated whole-VM restore, Debian boot, filesystem, `pihole-FTL`, and Node Exporter validation completed 2026-07-14 | Node Exporter plus separate recursive and local Blackbox DNS probes | [Pi-hole](../services/pihole.md), [Node Exporter](../services/node-exporter.md), [Blackbox Exporter](../services/blackbox-exporter.md) |
| `mon01` | Monitoring and observability stack | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 3 GB | 32 GB | Homelab LAN | Static, sanitized as `<MON01_IP>` | Active | Daily Proxmox backup active; configuration, Grafana state, data-source mapping, and existing dashboard exports inventoried; independent whole-VM restore not yet tested | Prometheus self-monitoring, local Node Exporter, and Blackbox Exporter service state; monitors `dns01` and `pve01` | [Project 002](../projects/project-002-monitoring-observability.md), [Prometheus](../services/prometheus.md), [Grafana](../services/grafana.md), [Blackbox Exporter](../services/blackbox-exporter.md) |

Project status and VM lifecycle are tracked separately. Project 002 remains active for enhancements while `mon01` itself is stable infrastructure. Project 003 is complete and provides scheduled backup coverage for both VMs.

## Backup Baseline

| Setting | Current value |
| --- | --- |
| Backup frequency | Daily |
| Backup mode | Snapshot |
| Compression | Zstandard |
| Retention | 7 daily, 4 weekly, 3 monthly |
| Destination | Dedicated external Proxmox backup storage |
| Restore-tested VM | `dns01` |
| Restore-test date | 2026-07-14 |

The `dns01` test was intentionally network-isolated. It proves VM reconstruction and local service startup, not end-to-end DNS or monitoring behavior.

## Recovery Priority

| Priority | VM | Reason | Required post-restore validation |
| --- | --- | --- | --- |
| High | `dns01` | Provides internal DNS and local records used by homelab services | Pi-hole service, public DNS, local DNS, Node Exporter, `blackbox_dns`, and `blackbox_dns_local` |
| Medium | `mon01` | Provides monitoring visibility and troubleshooting data but is not required for core connectivity | Prometheus jobs, all Node Exporter targets, both Blackbox modules/jobs, Grafana data source, and dashboards |

Recovery priority should be revisited after additional services depend on reverse proxying, certificates, authentication, backup automation, or monitoring-based actions.

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
- Both VMs are included in the Project 003 daily Proxmox backup job.
- The backup target uses mount-point enforcement so a missing external disk does not redirect backups into the host root filesystem.
- `dns01` was restored to a temporary VM with its network adapter removed, validated, and deleted after testing.
- `mon01` backup coverage is operational but independently untested.
- Future infrastructure VMs must be added here and onboarded to backup and monitoring before deployment is considered complete.
- Experimental VMs should be clearly labeled as experimental or temporary.

## Future Improvements

- Add service tier, recovery-time objective, and recovery-point objective where useful.
- Record latest successful backup and backup age through automated monitoring.
- Perform an independent `mon01` restore test.
- Add sanitized Proxmox node placement if additional nodes are introduced.
- Add monitoring and backup status for future infrastructure VMs during onboarding.
- Link VM entries to relevant runbooks, change records, and ADRs.

## Related Documentation

- [Virtualization Architecture](virtualization.md)
- [Network Architecture](network.md)
- [Monitoring and Observability](monitoring.md)
- [Storage Architecture](storage.md)
- [Proxmox Platform](../services/proxmox.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)
- [Pi-hole Service](../services/pihole.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Project 003](../projects/project-003-backup-recovery.md)
- [Hardware Inventory](../hardware/inventory.md)