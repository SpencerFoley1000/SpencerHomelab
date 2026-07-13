# ADR-0001: Use Lenovo ThinkPad E16 Gen 1 as Initial Proxmox Host

## Status

Accepted

## Date

2026-07-07

## Context

The homelab needed an initial virtualization platform capable of running infrastructure services, test workloads, and future security-lab systems.

The first host needed to balance:

- Cost.
- Power consumption.
- Noise.
- Simplicity.
- Available compute resources.
- Ease of administration.
- Learning value.

The available hardware was a Lenovo ThinkPad E16 Gen 1 business laptop with a 13th Gen Intel Core i5-1335U, 16 GB RAM, and a 1 TB PCIe SSD.

## Decision

Use the Lenovo ThinkPad E16 Gen 1 as the initial Proxmox VE host for the homelab.

The system serves as the active virtualization host during the first phase of the lab. A future ADR will determine its long-term role after the acquired X299 server is assembled and validated.

## Rationale

A business-class laptop was a practical first virtualization host for this stage of the homelab.

Reasons:

- It provides enough compute capacity for early VMs, containers, and infrastructure services.
- It is quieter and more power-efficient than typical rack server hardware.
- It avoided the cost and complexity of enterprise server hardware before the lab required it.
- It kept the initial environment physically simple while networking, monitoring, documentation, and recovery foundations were built.
- The integrated battery provides limited ride-through during brief power interruptions, although it is not a replacement for a proper UPS.
- Proxmox VE provides practical experience with virtualization, management-plane security, monitoring, capacity planning, and recovery.

## Alternatives Considered

| Alternative | Reason not chosen initially |
| --- | --- |
| Enterprise rack server | Higher cost, more noise, more power usage, and unnecessary complexity for the first phase |
| Desktop-based virtualization | Would blur the line between personal workstation and lab infrastructure |
| Multiple mini PCs | Useful later, but unnecessary before the initial architecture and services were stable |
| Cloud-only lab | Valuable for future Azure learning but does not provide the same hands-on hardware and local networking experience |

## Consequences

### Positive

- Provides a dedicated compute platform for the homelab.
- Keeps the initial lab quiet and power-efficient.
- Makes the early environment easier to maintain.
- Supports practical Proxmox, VM, storage, monitoring, and backup learning.
- Successfully hosts the DNS and monitoring foundation.
- Leaves room to add or transition to dedicated server hardware later.

### Negative / Tradeoffs

- Limited memory compared with dedicated server hardware.
- Limited internal storage expansion.
- Fewer network interfaces than a dedicated server or firewall platform.
- Laptop hardware is not ideal for every production-style server scenario.
- Future workloads require either careful capacity management or host expansion.
- The integrated battery protects only the laptop, not the switch, router, external backup drive, or future server.

### Follow-Up Work

- [ ] Document and test Proxmox host maintenance procedures.
- [x] Add a VM inventory once workloads are deployed.
- [x] Add Linux host monitoring for `pve01`.
- [ ] Add Proxmox platform-specific VM, storage, task, and backup metrics.
- [ ] Complete protected VM backup and restore validation.
- [x] Reassess host capacity after core services are deployed.
- [ ] Create a future ADR defining the relationship between the ThinkPad and X299 server.
- [ ] Integrate the host into UPS monitoring and graceful shutdown design.

The first capacity review resulted in increasing `mon01` from 2 GB to 3 GB RAM after monitoring showed limited headroom. The current host remains suitable for the deployed DNS and monitoring workloads, but memory and local storage remain the primary growth constraints.

## Validation

This decision is validated over time by tracking:

- Host stability.
- Resource utilization.
- VM performance.
- Ease of maintenance.
- Backup and restore reliability.
- Management-access security and recoverability.
- Whether future workloads exceed the hardware limits.

Current validation evidence:

- `dns01` and `mon01` are active on the host.
- Node Exporter exposes `pve01` Linux host metrics to Prometheus and Grafana.
- Monitoring identified and justified a resource adjustment for `mon01`.
- The host has sufficient capacity for the current foundation while retaining limited headroom.
- Proxmox management uses named routine administration, a protected root break-glass path, TOTP, and independent recovery keys.
- Project 003A documented service recovery state and protected application-level exports.

Remaining validation gaps:

- Protected VM backups are not yet operational.
- No representative VM restore has been completed.
- Proxmox platform-specific monitoring is not yet implemented.
- The host's role after the future server is validated has not been decided.
- Coordinated UPS-backed shutdown is not yet implemented.

If the active host becomes a bottleneck or changes role, a future ADR must document whether to retain it as primary, add another Proxmox node, migrate stable workloads, or repurpose it.

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Current Proxmox Host](../hardware/server.md)
- [Future Virtualization Server Build](../hardware/server-build.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Project 003](../projects/project-003-backup-recovery.md)
