# Virtualization Architecture

## Purpose

This document describes the virtualization design for the homelab. It focuses on the role of Proxmox VE, the current workload model, platform security, monitoring boundaries, and the operational assumptions that should guide future VM, container, and host decisions.

## Current Status

Proxmox VE is the active virtualization platform. The environment currently runs two production-style infrastructure VMs and is preparing for a future dedicated virtualization server.

Current priorities:

- Keep the active Proxmox host reachable, secure, monitored, and documented.
- Track active VMs in the [VM Inventory](vm-inventory.md).
- Keep DNS and monitoring responsibilities on separate systems.
- Install QEMU Guest Agent on stable Linux VMs where supported.
- Complete Project 003 VM backup and restore validation.
- Assemble and validate the future server before assigning it a production role.
- Prevent experimental workloads from consuming resources required by core infrastructure.

## Active Platform

| Area | Current State |
| --- | --- |
| Hypervisor | Proxmox VE `9.2.2` |
| Debian base | Debian 13 Trixie |
| Running kernel | `7.0.2-6-pve` |
| Active host | Lenovo ThinkPad E16 Gen 1, documented as `pve01` |
| Primary role | Run stable infrastructure VMs and future lab workloads |
| Management access | Internal network only; exact endpoint omitted |
| Administrative model | Named routine administrator plus root break-glass identity, both protected by TOTP and independent recovery keys |
| Current storage | Local 1 TB PCIe SSD |
| Host monitoring | Active through Node Exporter, Prometheus, and Grafana |
| Backup status | Project 003A readiness complete; VM backups and restore testing pending |

The exact bridge names, addresses, storage identifiers, VM IDs, authentication seeds, and recovery material remain private.

## Planned Dedicated Server

Hardware has been acquired for a future dedicated virtualization server.

Current known configuration:

| Component | Sanitized specification |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| Cooling | Noctua NH-U12S |
| Power supply | Existing 500 W unit |
| Chassis | Existing NZXT H510 |
| Planned local storage | Two existing 1 TB NVMe devices |
| Known limitation | One inner DIMM slot is nonfunctional; CPU and 32 GB memory were detected in seller validation |
| Current status | Acquired; assembly and local validation pending |

The future server is not considered production infrastructure until it passes:

- Visual inspection and assembly validation.
- CPU and memory detection checks.
- Stability and temperature testing.
- Storage-health validation.
- Network validation.
- Hypervisor installation and management-access validation.
- Monitoring and backup integration.

A future ADR should decide whether this server replaces the ThinkPad, supplements it as another node, or changes the ThinkPad to a secondary role.

## Current Workloads

| VM | Role | Status | Notes |
| --- | --- | --- | --- |
| `dns01` | Pi-hole DNS server | Active | Provides internal DNS records, DNS filtering, Node Exporter metrics, and recursive/local DNS probe targets |
| `mon01` | Monitoring and observability | Active | Runs Prometheus, Grafana, Node Exporter, and Blackbox Exporter |

See the [VM Inventory](vm-inventory.md) for current resource allocations, backup maturity, monitoring coverage, and recovery priority.

## Design Goals

- Provide a flexible platform for infrastructure services and lab workloads.
- Practice VM lifecycle management, capacity planning, backups, and recovery.
- Keep core infrastructure separate from experimental systems.
- Avoid making the hypervisor dependent on undocumented manual changes.
- Support future automation without requiring automation before the environment is understood.
- Make workload criticality and restore order explicit.
- Treat host transitions as documented migrations rather than informal hardware swaps.

## Workload Categories

| Category | Examples | Stability expectation |
| --- | --- | --- |
| Core infrastructure | DNS, monitoring, backup services, management tooling | Stable, monitored, documented, and backed up after Project 003 |
| Lab services | Reverse proxy, internal applications, dashboards | Documented but may change frequently |
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
- The active Proxmox host has 16 GB RAM, so stable services require deliberate capacity planning.
- The future server's 32 GB baseline provides additional capacity but does not eliminate the need for workload prioritization.
- The failed DIMM slot reduces maximum memory flexibility and must be documented during future expansion.

Guidelines:

- Keep enough host memory and CPU available for Proxmox management and emergency access.
- Document unusually large or changed allocations.
- Give core infrastructure priority over experiments.
- Avoid adding persistent workloads without checking host capacity.
- Reassess storage before VM disks and monitoring retention consume most local capacity.
- Validate hardware limits before purchasing upgrades.

## Networking Model

Current model:

- Core infrastructure VMs connect to the homelab LAN.
- Static addressing is used for foundational services.
- Internal DNS records are managed through Pi-hole.
- Exact bridge names, addresses, VM IDs, and MAC addresses are sanitized.
- `mon01` scrapes Node Exporter on `dns01` and `pve01`.
- `mon01` probes both recursive and local DNS behavior on `dns01`.

Future documentation should include:

- Sanitized Proxmox bridge roles.
- VLAN-aware bridge configuration if implemented.
- Management-network placement.
- Allowed VM groups on each network segment.
- Security-lab isolation boundaries.
- Network placement for the future dedicated server.

## Guest Integration

QEMU Guest Agent is installed on `dns01` and `mon01`.

The agent depends on both:

- The guest package and systemd service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling virtual hardware. The operational procedure is documented in the [QEMU Guest Agent Troubleshooting Runbook](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

Current monitoring includes:

- Node Exporter on `pve01`, `dns01`, and `mon01`.
- Prometheus target health for all three systems.
- Grafana CPU, memory, filesystem, network, and uptime views.
- Recursive and local DNS service probes for `dns01`.

Node Exporter on `pve01` provides Linux operating-system metrics. It does not provide authoritative:

- VM or container state.
- Storage-pool health.
- Proxmox task results.
- Backup-job status.
- Cluster or quorum state.
- Replication or migration state.

Proxmox platform metrics remain a separate future integration requiring a documented least-privilege identity.

## Backup and Recovery

Project 003A completed:

- Recovery inventories for `dns01` and `mon01`.
- Private Pi-hole Teleporter export creation and inspection.
- Private Grafana dashboard export creation and inspection.
- Prometheus, Blackbox Exporter, Grafana, and Node Exporter state classification.
- Preliminary manual recovery notes.

The 5 TB external drive has been acquired but is not yet integrated as Proxmox backup storage.

Current recovery priority:

1. Restore physical networking and Proxmox management access.
2. Restore `dns01` and validate public and local DNS.
3. Restore `mon01` and validate Prometheus, both Blackbox jobs, and Grafana.
4. Confirm monitoring observes all restored systems.
5. Restore lower-priority lab and experimental workloads.

Project 003 must still define backup scheduling, retention, protected VM coverage, backup-health validation, and a representative isolated restore test.

## Security Considerations

- Do not expose Proxmox management directly to the internet.
- Use a named routine administrator and reserve the root identity for break-glass and root-only work.
- Store passwords, TOTP seeds, recovery keys, API credentials, and private keys outside the repository.
- Limit administrative access to trusted devices and future management networks.
- Keep security-lab workloads isolated from trusted infrastructure.
- Document privileged containers, passthrough devices, or unusual VM permissions.
- Apply Proxmox and guest updates through a deliberate maintenance process.
- Avoid publishing VM IDs, exact addresses, MAC addresses, storage identifiers, or raw configuration exports.
- Introduce platform-monitoring credentials only through a least-privilege design.

## Maintenance Notes

Proxmox maintenance procedures should document:

- Installed version and update process.
- Backup checks before major changes.
- VM shutdown and startup order.
- Host reboot expectations.
- Validation of `dns01`, `mon01`, and `pve01` monitoring after maintenance.
- TOTP and system-time validation.
- Recovery steps if management access is lost.

The [VM Provisioning Runbook](../runbooks/vm-provisioning.md) provides the current baseline checklist for new VMs.

## Future Improvements

- Document the sanitized bridge and storage layout.
- Add a tested Proxmox maintenance and management-access recovery runbook.
- Complete backup and restore validation under Project 003.
- Add Proxmox-specific platform metrics through least-privilege integration.
- Assemble and validate the future dedicated server.
- Create an ADR defining the future relationship between the ThinkPad and dedicated server.
- Integrate power measurement, UPS monitoring, and graceful shutdown.
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
- [Current Proxmox Host Hardware](../hardware/server.md)
- [Future Virtualization Server Hardware](../hardware/server-build.md)
- [Hardware Inventory](../hardware/inventory.md)
