# ADR-0005: Migrate `pve01` to the X299 Server

## Status

Accepted — 2026-07-21

## Context

The initial Proxmox platform ran successfully on a Lenovo ThinkPad E16 Gen 1, but its 16 GB memory ceiling and limited internal expansion constrained planned identity and security workloads. A dedicated X299 system was assembled with 32 GB RAM and greater expansion capacity.

The existing Proxmox installation, VM storage, backup scheduling, authentication controls, and monitoring configuration were already stable. Rebuilding them solely because the physical host changed would add migration risk without improving the logical design.

## Decision

Move the existing Proxmox SATA system disk into the X299 server and retain the logical hostname `pve01`.

The X299 server becomes the sole production hypervisor. The ThinkPad leaves the virtualization role and returns to endpoint use. It is not treated as a cluster node or recovery host unless a future decision explicitly assigns that role.

## Consequences

### Positive

- Preserves working VM, backup, authentication, and monitoring configuration.
- Avoids an unnecessary hypervisor rebuild and workload restore.
- Doubles initial host memory from 16 GB to 32 GB.
- Provides greater storage and PCIe expansion capacity.
- Keeps existing service documentation and Prometheus labels stable.

### Negative

- The platform still has a single production hypervisor and no automatic failover.
- One motherboard DIMM slot is nonfunctional, limiting memory topology.
- The desktop-class server lacks the ThinkPad's built-in battery ride-through.
- A dedicated GPU is required for local console access because the CPU lacks integrated graphics.
- Retaining the hostname means operators must not assume old hardware details from the logical name.

## Alternatives Considered

| Alternative | Reason not selected |
| --- | --- |
| Fresh Proxmox installation and VM restores | Added avoidable configuration and recovery risk when the existing disk could boot on the new platform |
| Two-node Proxmox cluster | Two nodes do not provide a clean quorum design, and the ThinkPad was intended to return to endpoint use |
| Keep the ThinkPad as primary | Preserved the memory and expansion constraints that motivated the build |
| Run both hosts independently | Increased power, maintenance, and documentation overhead without a current workload requirement |

## Validation

- The transferred installation booted successfully as `pve01`.
- Internal management access returned.
- Core VMs and services returned to operation.
- Backup storage remained accessible.
- Node Exporter resumed reporting and exposed X299 CPU temperature metrics.

## Follow-up

- Implement UPS-backed graceful shutdown under Project 006.
- Continue monitoring temperature and stability.
- Document any future NVMe or memory-topology change.
- Create a new ADR before adding a second hypervisor or changing the ThinkPad's role again.

