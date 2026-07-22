# X299 Virtualization Server

## Purpose

This page documents the physical platform now running the production Proxmox host `pve01`, including its migration history, known hardware limitation, monitoring, and maintenance requirements.

## Status

| Area | Details |
| --- | --- |
| Lifecycle state | Active production infrastructure |
| Role | Primary and sole Proxmox virtualization server |
| Hostname | `pve01` |
| Hypervisor | Existing Proxmox VE installation migrated from the initial ThinkPad host |
| Management | Internal-only |
| Monitoring | Node Exporter, Prometheus, Grafana, and CPU hardware-sensor metrics |
| Backup integration | Existing VM backup configuration and dedicated external target preserved |
| Production date | 2026-07-21 |

## Hardware

| Component | Specification |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| CPU cooler | Noctua NH-U12S |
| Display adapter | AMD Radeon R7 350 |
| TPM | ASRock TPM 2.0 module |
| Chassis | NZXT H510 |
| Power supply | Existing 500 W unit |
| System storage | Existing 1 TB SATA SSD containing Proxmox and VM state |
| Available expansion storage | Two 1 TB NVMe devices; production role not yet assigned |

The display adapter exists for physical-console access because the i7-7800X has no integrated graphics. It is not used for compute workloads.

## Known Hardware Limitation

One inner DIMM slot is nonfunctional. The server operates with 32 GB in the validated working-slot arrangement.

Operational consequences:

- The fault is accepted, not repaired.
- Memory expansion must account for the remaining usable slots and supported topology.
- The current capacity is sufficient for the deployed workload baseline.
- Any memory change requires detection, stability, and temperature validation before production use.

## Migration

The Proxmox SATA SSD was moved from the Lenovo ThinkPad E16 Gen 1 into this server. Retaining the disk preserved the logical `pve01` identity, VM state, backup schedule, administrator configuration, TOTP controls, and monitoring labels.

Validated after migration:

- POST and local video output.
- Expected CPU and 32 GB memory detection.
- Boot from the transferred system disk.
- Internal Proxmox management access.
- Startup of `dns01`, `mon01`, and `proxy01`.
- DNS, monitoring, and reverse-proxy service availability.
- Dedicated backup-target access.
- Node Exporter scrape health.
- `coretemp` CPU temperature metrics through the hardware-monitoring collector.

See [Project 005](../projects/project-005-x299-virtualization-server.md) and [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md).

## Monitoring

Node Exporter provides the existing Linux host baseline plus hardware-monitoring sensor data.

Current host visibility includes:

- CPU utilization and load.
- Memory availability.
- Filesystem, disk, and network activity.
- Uptime and exporter reachability.
- CPU core temperatures exposed by the `coretemp` device.

Temperature telemetry should be reviewed after cooler maintenance, memory changes, airflow changes, or sustained high-load testing. Node Exporter does not replace Proxmox-specific API monitoring for VM, task, storage-pool, or backup-job state.

## Security Considerations

- Keep Proxmox management and Node Exporter internal-only.
- Use the named routine administrator and reserve root for break-glass operations.
- Keep passwords, TOTP seeds, recovery keys, exact addresses, MAC addresses, UUIDs, and hardware identifiers outside Git.
- Preserve physical-console access for recovery.
- Do not place attacker-style workloads on trusted networks or near backup storage.

## Power and UPS Dependency

Unlike the initial laptop host, this server has no integrated battery. Project 006 must provide:

- UPS-backed runtime for the server and required network path.
- UPS state monitoring where supported.
- Ordered VM and host shutdown.
- Documented recovery after utility power returns.
- Battery testing and replacement procedures.

## Maintenance Notes

Before hardware maintenance:

- Confirm recent successful backups and mounted backup storage.
- Shut down VMs and the host cleanly.
- Preserve the stable DIMM layout unless memory work is intentional.
- Record cable and storage placement privately when needed for reassembly.

After hardware maintenance:

- Confirm CPU and expected memory detection.
- Confirm cooler mounting, fan operation, and temperatures.
- Validate Proxmox management and all core VMs.
- Confirm Node Exporter and hardware-sensor metrics.
- Confirm the backup target and next scheduled backup.

## Future Improvements

- Complete Project 006 UPS integration and graceful shutdown testing.
- Record idle, normal, startup, and higher-load power measurements.
- Select a documented role for the NVMe devices when a storage requirement exists.
- Add Proxmox platform and backup-job metrics through least privilege.
- Reassess memory capacity as identity and security workloads are introduced.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Initial ThinkPad Host](server.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Project 005](../projects/project-005-x299-virtualization-server.md)
- [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md)
