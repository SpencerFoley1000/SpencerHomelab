# ADR-0001: Use Lenovo ThinkPad E16 Gen 1 as Initial Proxmox Host

## Status

Accepted

## Date

2026-07-07

## Context

The homelab needed an initial virtualization platform capable of running infrastructure services, test workloads, and future security lab systems.

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

The system will serve as the primary virtualization host during the first phase of the lab.

## Rationale

A business-class laptop is a practical first virtualization host for this stage of the homelab.

Reasons:

- It provides enough compute capacity for early VMs, containers, and infrastructure services.
- It is quieter and more power-efficient than typical rack server hardware.
- It avoids the cost and complexity of enterprise server hardware before the lab requires it.
- It keeps the initial environment physically simple while networking and documentation foundations are still being built.
- The integrated battery provides limited ride-through during brief power interruptions, although it should not be treated as a long-term substitute for a proper UPS.
- Proxmox VE provides practical experience with virtualization concepts used in systems administration and infrastructure roles.

## Alternatives Considered

| Alternative | Reason Not Chosen |
| --- | --- |
| Enterprise rack server | Higher cost, more noise, more power usage, and unnecessary complexity for the first phase |
| Desktop-based virtualization | Would blur the line between personal workstation and lab infrastructure |
| Multiple mini PCs | Useful later, but unnecessary before the initial architecture and services are stable |
| Cloud-only lab | Good for future Azure learning, but does not provide the same hands-on networking and hardware experience |

## Consequences

### Positive

- Provides a dedicated compute platform for the homelab.
- Keeps the lab quiet and power-efficient.
- Makes the environment easier to maintain during the early build.
- Supports practical Proxmox, VM, container, storage, and backup learning.
- Leaves room to grow into additional nodes or dedicated server hardware later.

### Negative / Tradeoffs

- Limited memory compared to larger servers.
- Limited internal storage expansion.
- Fewer network interfaces than a dedicated firewall or server platform.
- Laptop hardware is not ideal for every production-style server scenario.
- Future workloads may require memory, storage, or host expansion.

### Follow-Up Work

- [ ] Document Proxmox host maintenance procedures.
- [ ] Add VM inventory once workloads are deployed.
- [ ] Add monitoring for host health.
- [ ] Add backup and restore validation.
- [ ] Reassess host capacity after core services are deployed.

## Validation

This decision should be validated over time by tracking:

- Host stability.
- Resource utilization.
- VM and container performance.
- Ease of maintenance.
- Backup and restore reliability.
- Whether future workloads exceed the hardware limits.

If the host becomes a bottleneck, a future ADR should document whether to upgrade memory, add storage, add another Proxmox node, or move to dedicated server hardware.

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Lenovo ThinkPad E16 Gen 1 Proxmox Host](../hardware/server.md)
