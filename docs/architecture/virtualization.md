# Virtualization Architecture

## Purpose

This document describes the virtualization design for the homelab. It focuses on the role of Proxmox VE, the current workload model, and the operational assumptions that should guide future VM and container decisions.

## Current Status

Proxmox VE is the active virtualization platform. The environment currently runs two production-style infrastructure VMs and is designed to grow gradually without sacrificing recoverability or clarity.

Current priorities:

- Keep the Proxmox host reachable, secure, and documented.
- Track active VMs in the [VM Inventory](vm-inventory.md).
- Keep DNS and monitoring responsibilities on separate systems.
- Install QEMU Guest Agent on stable Linux VMs where supported.
- Document resource, storage, networking, backup, and recovery assumptions.
- Prevent experimental workloads from consuming resources required by core infrastructure.

## Platform

| Area | Current Direction |
| --- | --- |
| Hypervisor | Proxmox VE |
| Hardware | Lenovo ThinkPad E16 Gen 1 |
| Primary role | Run lab infrastructure, services, and test workloads |
| Management access | Internal network only; exact endpoint omitted |
| Current storage | Local 1 TB PCIe SSD |
| Backup status | Not yet implemented or restore-tested |
| Documentation level | Sanitized architecture and operational notes |

The installed Proxmox version, bridge layout, and storage pool details should be recorded during the next maintenance review.

## Current Workloads

| VM | Role | Status | Notes |
| --- | --- | --- | --- |
| `dns01` | Pi-hole DNS server | Active | Provides internal DNS records, DNS-based blocking, Node Exporter metrics, and a monitored DNS endpoint |
| `mon01` | Monitoring and observability | Active | Runs Prometheus, Grafana, Node Exporter, and Blackbox Exporter |

See the [VM Inventory](vm-inventory.md) for current resource allocations and recovery priority.

## Design Goals

- Provide a flexible platform for infrastructure services and lab workloads.
- Practice VM lifecycle management, capacity planning, backups, and recovery.
- Keep core infrastructure separate from experimental systems.
- Avoid making the hypervisor dependent on undocumented manual changes.
- Support future automation without requiring automation before the environment is understood.
- Make workload criticality and restore order explicit.

## Workload Categories

| Category | Examples | Stability Expectation |
| --- | --- | --- |
| Core infrastructure | DNS, monitoring, backup services, management tooling | Stable, monitored, documented, and eventually backed up |
| Lab services | Dashboards, test applications, learning projects | Documented but may change frequently |
| Security lab | Attacker machines, vulnerable VMs, detection engineering projects | Isolated and clearly labeled |
| Temporary experiments | Short-lived tests and proofs of concept | Disposable unless promoted to a documented service |

## Naming Convention

Current pattern:

```text
<role><number>
```

Examples:

- `dns01`
- `mon01`
- `pbs01`
- `proxy01`
- `sec-lab01`

Avoid personal names, family names, locations, or identifying labels in VM names committed to public documentation.

## Resource Allocation Strategy

Resource allocation starts conservative and is adjusted using observed behavior.

Current lessons:

- `mon01` memory was increased from 2 GB to 3 GB after Grafana showed limited headroom.
- Monitoring infrastructure should be sized using observed usage rather than assumptions alone.
- The Proxmox host has 16 GB RAM, so stable services require deliberate capacity planning.

Guidelines:

- Keep enough host memory and CPU available for Proxmox management and emergency access.
- Document unusually large or changed allocations.
- Give core infrastructure priority over experiments.
- Avoid adding persistent workloads without checking host capacity.
- Reassess storage before VM disks and monitoring retention consume most of the local SSD.

## Networking Model

Current model:

- Core infrastructure VMs connect to the homelab LAN.
- Static addressing is used for foundational services.
- Internal DNS records are managed through Pi-hole.
- Exact bridge names, addresses, VM IDs, and MAC addresses are sanitized.
- `mon01` scrapes `dns01` metrics and probes the DNS service over the internal network.

Future documentation should include:

- Proxmox bridge layout.
- VLAN-aware bridge configuration if implemented.
- Management network placement.
- Allowed VM groups on each network segment.
- Security-lab isolation boundaries.

## Guest Integration

QEMU Guest Agent is installed on `dns01` and `mon01`.

The agent depends on both the guest package and the Proxmox-provided virtio serial device. A full Proxmox stop/start may be required after enabling the virtual hardware. The operational procedure is documented in the [QEMU Guest Agent Troubleshooting Runbook](../runbooks/qemu-guest-agent-troubleshooting.md).

## Backup and Recovery

Backups have not yet been implemented or restore-tested.

Until Project 003 is complete, stable services should be considered recoverable only from:

- Service documentation.
- Configuration exports created outside the repository.
- Package installation procedures.
- Sanitized architecture and troubleshooting notes.

Current recovery priority:

1. Proxmox management and network connectivity.
2. `dns01` because internal services may depend on DNS.
3. `mon01` to restore monitoring visibility.
4. Lower-priority lab and experimental workloads.

Project 003 should define backup destination, frequency, retention, encryption, VM coverage, and representative restore testing.

## Security Considerations

- Do not expose Proxmox management directly to the internet.
- Use strong unique credentials stored outside the repository.
- Limit administrative access to trusted devices and future management networks.
- Keep security-lab workloads isolated from trusted infrastructure.
- Document privileged containers, passthrough devices, or unusual VM permissions.
- Apply Proxmox and guest updates through a deliberate maintenance process.
- Avoid publishing VM IDs, exact addresses, MAC addresses, or raw configuration exports.

## Maintenance Notes

Future Proxmox maintenance procedures should document:

- Installed version and update process.
- Backup checks before major changes.
- VM shutdown and startup order.
- Host reboot expectations.
- Service validation after maintenance.
- Recovery steps if the host becomes unreachable.

The [VM Provisioning Runbook](../runbooks/vm-provisioning.md) provides the current baseline checklist for new VMs.

## Future Improvements

- Record the installed Proxmox version.
- Document the sanitized bridge and storage layout.
- Add a tested Proxmox maintenance runbook.
- Add backup and restore validation under Project 003.
- Add monitoring coverage for the Proxmox host.
- Add ADRs for future clustering, storage, networking, or container decisions.

## Related Documentation

- [Architecture Overview](overview.md)
- [Network Architecture](network.md)
- [VM Inventory](vm-inventory.md)
- [Storage Architecture](storage.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Proxmox Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Hardware Inventory](../hardware/inventory.md)
