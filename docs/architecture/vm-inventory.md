# VM Inventory

## Purpose

This inventory tracks virtual machines that are intentionally part of the homelab environment.

The goal is to document what exists, why it exists, where it runs, and how important it is to the rest of the lab. Exact IP addresses and sensitive implementation details are intentionally sanitized for public documentation.

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
- Backup status
- Recovery priority
- Monitoring coverage
- Documentation links

Avoid publishing:

- Exact internal IPs unless necessary and intentionally sanitized.
- MAC addresses.
- VM IDs unless there is a documented reason.
- Personal usernames.
- Secrets, tokens, keys, or passwords.
- Hostnames that reveal personally identifying information.

## Active Virtual Machines

| Hostname | Purpose | Platform | OS | vCPU | RAM | Disk | Network | IP Model | Lifecycle | Backup Status | Monitoring | Documentation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and DNS-based blocking | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 2 GB | 20 GB | Homelab LAN | Static, sanitized as `<DNS01_IP>` | Active | Not yet backed up | Node Exporter host metrics and Blackbox DNS availability probe | [Pi-hole](../services/pihole.md), [Node Exporter](../services/node-exporter.md), [Blackbox Exporter](../services/blackbox-exporter.md) |
| `mon01` | Monitoring and observability stack | Proxmox VE VM | Debian 13.5 (Trixie) | 2 | 3 GB | 32 GB | Homelab LAN | Static, sanitized as `<MON01_IP>` | Active | Not yet backed up | Prometheus self-monitoring and local Node Exporter metrics | [Project 002](../projects/project-002-monitoring-observability.md), [Node Exporter](../services/node-exporter.md), [Prometheus](../services/prometheus.md), [Grafana](../services/grafana.md), [Blackbox Exporter](../services/blackbox-exporter.md) |

Project status and VM lifecycle are tracked separately. Project 002 remains active while `mon01` itself is an active infrastructure VM.

## Recovery Priority

| Priority | VM | Reason |
| --- | --- | --- |
| High | `dns01` | Provides internal DNS for homelab services and local records |
| Medium | `mon01` | Provides monitoring visibility; important for troubleshooting but not required for core connectivity |

Recovery priority should be revisited after additional services depend on monitoring, authentication, reverse proxying, or backup infrastructure.

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
- Future infrastructure VMs should be added here before their deployment is considered complete.
- Experimental VMs should be clearly labeled as experimental or temporary.
- Backup status must be updated after Project 003 implements and validates a backup target.

## Future Improvements

- Add service tier and restore-time expectations for critical VMs.
- Add backup schedule, retention, and last restore-test date.
- Add sanitized Proxmox node placement if additional nodes are introduced.
- Add monitoring status for future infrastructure VMs during onboarding.
- Link VM entries to relevant runbooks and ADRs.

## Related Documentation

- [Virtualization Architecture](virtualization.md)
- [Network Architecture](network.md)
- [Monitoring and Observability](monitoring.md)
- [Proxmox Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Node Exporter Service](../services/node-exporter.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
- [Hardware Inventory](../hardware/inventory.md)
