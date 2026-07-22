# Project 005: X299 Virtualization Server

## Status

Completed on 2026-07-21.

## Purpose

Replace the temporary laptop-based Proxmox host with a dedicated, expandable server while preserving the working virtualization platform, production VMs, backup design, and monitoring identity.

## Scope

- Assemble the X299 platform and verify successful POST.
- Install a dedicated display adapter because the Intel Core i7-7800X has no integrated graphics.
- Move the existing Proxmox system SSD from the ThinkPad into the server instead of rebuilding a known-good platform.
- Validate CPU and memory detection, boot, networking, workload recovery, and temperatures.
- Return the ThinkPad to normal endpoint use.
- Update the architecture and operational documentation.

## Implemented Hardware

| Component | Production configuration |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| Cooling | Noctua NH-U12S |
| Graphics | AMD Radeon R7 350 for console access |
| Chassis | NZXT H510 |
| Power supply | Existing 500 W unit |
| System storage | Existing 1 TB SATA SSD containing the Proxmox installation |
| Known limitation | One inner DIMM slot is nonfunctional |

Exact addresses, identifiers, serial numbers, and storage UUIDs remain outside the public repository.

## Design Decisions

### Preserve the Existing Proxmox Installation

The existing SATA system disk was transferred directly from the ThinkPad. This avoided an unnecessary reinstall and preserved:

- The `pve01` hostname and management configuration.
- VM definitions and disks.
- Backup schedules and storage configuration.
- Administrative authentication and TOTP configuration.
- Node Exporter configuration and existing Prometheus labels.

The migration was treated as a hardware-platform change, not a new logical host. This decision is recorded in [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md).

### Use a Low-Power Display Adapter

Neither the i7-7800X nor the primary workstation CPU provides usable integrated graphics for this migration. A Radeon R7 350 was installed to provide reliable local console access without keeping the workstation's primary GPU in the server.

### Retire the ThinkPad Hypervisor Role

After the disk transfer succeeded, the ThinkPad was removed from the production virtualization path and returned to endpoint use. It is not currently a Proxmox node or automatic failover target.

## Migration Summary

1. Shut down the VMs and Proxmox host cleanly.
2. Disconnected the external backup target and system SSD only after shutdown.
3. Completed the X299 assembly and local console setup.
4. Installed the existing Proxmox SATA SSD in the X299 server.
5. Booted the existing `pve01` installation on the new hardware.
6. Verified management access, networking, VM startup, service health, backup-storage visibility, and monitoring.
7. Added and validated hardware temperature telemetry.
8. Returned the ThinkPad to non-server use.

## Validation

Validated successfully:

- System POST and local video output.
- Intel Core i7-7800X detection.
- Expected 32 GB memory detection in the stable slot arrangement.
- Proxmox boot from the transferred SATA SSD.
- Existing `pve01` identity and internal management access.
- Startup of `dns01`, `mon01`, and `proxy01`.
- Pi-hole DNS, Prometheus, Grafana, and NGINX Proxy Manager service availability.
- Node Exporter reachability from Prometheus.
- Linux hardware-monitoring sensor exposure through Node Exporter.
- CPU core-temperature metrics from the `coretemp` hardware-monitoring device.
- Continued access to the dedicated backup target.

The known failed DIMM slot remains a documented capacity constraint. Completion means the installed 32 GB configuration is operational; it does not claim the defective slot was repaired.

## Security Considerations

- Proxmox management remains internal-only.
- The named routine administrator, root break-glass identity, TOTP, and independent recovery keys were preserved.
- No credentials, recovery data, MAC addresses, serial numbers, storage UUIDs, or exact private addresses are published.
- Physical console access remains available through the dedicated display adapter.
- Intentionally vulnerable workloads remain out of scope until network isolation is implemented.

## Lessons Learned

- CPU integrated graphics support must be checked explicitly during server planning; a working CPU and motherboard do not guarantee video output.
- Reusing a working Proxmox system disk can turn a host replacement into a controlled hardware migration rather than a full platform rebuild.
- Preserving the logical hostname kept monitoring, backup, and operational references stable, but every dependency still required post-migration validation.
- Custom hardware should expose temperature telemetry before being left unattended.
- Known hardware faults can be accepted when their impact is understood, tested around, and documented honestly.

## Remaining Improvements

- Complete Project 006 UPS monitoring and graceful shutdown.
- Record idle, normal-load, and higher-load power measurements.
- Continue observing temperatures and stability under real workloads.
- Decide whether and how to use the available NVMe devices.
- Reassess memory capacity when workload demand justifies an upgrade.
- Re-run restore testing after future major storage or hypervisor changes.

## Related Documentation

- [X299 Server Hardware](../hardware/server-build.md)
- [Initial ThinkPad Host](../hardware/server.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Hardware Inventory](../hardware/inventory.md)
- [ADR-0005](../decisions/ADR-0005-migrate-pve01-to-x299-server.md)
- [Completion Record](../changes/2026-07-21-project-005-x299-server-completion.md)

