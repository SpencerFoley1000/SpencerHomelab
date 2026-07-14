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

Available hardware was a Lenovo ThinkPad E16 Gen 1 with an Intel Core i5-1335U, 16 GB RAM, and a 1 TB PCIe SSD.

## Decision

Use the Lenovo ThinkPad E16 Gen 1 as the initial Proxmox VE host.

It remains the active host during the first phase of the lab. A future ADR will determine its long-term role after the X299 server is assembled and validated.

## Rationale

A business-class laptop was practical for the initial phase.

Reasons:

- Enough compute for early infrastructure VMs.
- Quieter and more efficient than typical rack hardware.
- Avoided unnecessary cost and complexity.
- Kept the environment simple while networking, monitoring, backup, security, and documentation foundations were built.
- Integrated battery provides limited ride-through for brief interruptions.
- Proxmox provides hands-on experience with virtualization, capacity, monitoring, management security, and recovery.

## Alternatives Considered

| Alternative | Reason not chosen initially |
| --- | --- |
| Enterprise rack server | Higher cost, noise, power use, and unnecessary complexity |
| Desktop-based virtualization | Would mix personal workstation and infrastructure roles |
| Multiple mini PCs | Useful later but unnecessary before the architecture stabilized |
| Cloud-only lab | Valuable for future Azure work but lacks the same local hardware and networking practice |

## Consequences

### Positive

- Dedicated compute platform for the homelab.
- Quiet and power-efficient initial environment.
- Simple physical footprint.
- Supports practical Proxmox, VM, storage, monitoring, backup, and recovery work.
- Successfully hosts the DNS and monitoring foundation.
- Allows a later transition to dedicated server hardware.

### Negative / Tradeoffs

- Limited memory and internal storage expansion.
- Fewer network interfaces than dedicated server hardware.
- Laptop hardware is not ideal for every production-style scenario.
- Future workload growth requires capacity discipline or migration.
- The integrated battery does not protect the router, switch, external backup drive, or future server.

## Follow-Up Work

- [ ] Validate a complete Proxmox maintenance window.
- [x] Add a VM inventory.
- [x] Add Linux host monitoring for `pve01`.
- [ ] Add Proxmox platform-specific VM, storage, task, and backup metrics.
- [x] Complete protected VM backup and representative restore validation.
- [x] Reassess host capacity after core services were deployed.
- [ ] Create an ADR defining the ThinkPad and X299 server relationship.
- [ ] Integrate the host into UPS monitoring and graceful-shutdown design.

The first capacity review increased `mon01` from 2 GB to 3 GB RAM after monitoring showed limited headroom. The host remains suitable for the current DNS and monitoring workloads, but memory and local storage remain the main growth constraints.

## Validation

Current evidence:

- `dns01` and `mon01` are active.
- Node Exporter exposes `pve01` Linux metrics to Prometheus and Grafana.
- Monitoring identified and justified the `mon01` memory increase.
- Proxmox management uses named routine administration, a protected root break-glass path, TOTP, and independent recovery keys.
- A dedicated 5 TB external backup target is active.
- Daily backups protect `dns01` and `mon01`.
- `dns01` was restored to an isolated temporary VM and locally validated.
- The temporary restore VM was removed after testing.

Remaining validation gaps:

- Proxmox platform-specific monitoring is not implemented.
- `mon01` has not been independently restored.
- The host's role after future-server validation is undecided.
- Coordinated UPS-backed shutdown is not implemented.

A future ADR must document whether to retain the ThinkPad as primary, add another node, migrate stable workloads, or repurpose it.

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
- [ADR-0003](ADR-0003-direct-attached-proxmox-backup-storage.md)