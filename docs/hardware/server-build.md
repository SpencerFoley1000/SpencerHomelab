# Future Virtualization Server Build

## Purpose

This page documents the acquired hardware, known limitation, validation plan, and intended architecture role for the future dedicated virtualization server.

The system is not yet production infrastructure. It must be assembled, tested, monitored, and integrated into backup and recovery workflows before hosting stable workloads.

## Status

| Area | Details |
| --- | --- |
| Lifecycle state | Acquired / pre-deployment |
| Intended role | Future dedicated virtualization server |
| Current role | None; hardware is awaiting assembly and validation |
| Production approval | Not granted |
| Final hostname | Pending; use `<FUTURE_PVE_HOST>` publicly until selected |
| Hypervisor | Expected to use Proxmox VE; final design decision pending validation |
| Network placement | Pending |
| Backup coverage | Pending |
| Monitoring coverage | Pending |

## Acquired Components

| Component | Specification |
| --- | --- |
| Motherboard | ASRock X299M Extreme4 |
| Processor | Intel Core i7-7800X |
| Memory | 32 GB Crucial DDR4-2133 |
| CPU cooler | Noctua NH-U12S |
| TPM | ASRock TPM 2.0 module |
| Chassis | Existing NZXT H510 |
| Power supply | Existing 500 W unit |
| Planned local storage | Two existing 1 TB NVMe devices |
| Additional included item | Motherboard I/O shield |

The build is expected to remain below approximately $200 in newly purchased server components because the chassis, power supply, and NVMe storage are reused. Thermal paste is required during assembly.

## Known Hardware Limitation

One inner DIMM slot is reported as nonfunctional.

Current evidence supplied with the hardware:

- BIOS detected the Intel Core i7-7800X.
- BIOS detected 32 GB of installed memory.
- Dual-channel operation was shown.

The motherboard has four DIMM slots. If the reported defect is confirmed, three usable slots remain.

Operational consequences:

- The initial 32 GB configuration may be acceptable if it passes local testing.
- Future memory upgrades must follow a topology supported by the remaining slots.
- The defect reduces memory-layout flexibility and must be included in capacity planning.
- Memory stability must be tested before workload migration.
- The failure should not be represented as resolved unless the slot is independently retested and works reliably.

## Intended Architecture Value

The future server is expected to provide:

- More memory capacity than the current 16 GB ThinkPad host.
- More internal storage flexibility.
- A platform better suited to persistent infrastructure growth.
- Additional capacity for reverse proxy, identity, security, and future platform services.
- A useful hardware-validation, migration, monitoring, backup, and power-management project.

It is not yet decided whether the server will:

- Replace the ThinkPad as the primary Proxmox host.
- Join it as an additional Proxmox node.
- Run independently while the ThinkPad retains a secondary or recovery role.

That decision requires an ADR after validation and before workload migration.

## Assembly Plan

1. Inspect the motherboard, socket, DIMM slots, cooler, and included components for shipping damage.
2. Verify the reported failed DIMM slot location.
3. Install the CPU cooler using fresh thermal paste.
4. Install the known-good memory configuration.
5. Install the two NVMe devices only after the board passes initial POST validation.
6. Connect the existing 500 W power supply and verify all required power connectors.
7. Complete an initial bench or open-case POST before final cable management.
8. Record BIOS-detected CPU, memory, storage, and firmware state using sanitized notes.

## Validation Requirements

### Hardware Detection

- CPU model is correctly detected.
- Expected 32 GB memory is detected.
- Memory channels and slot population match the intended layout.
- Both NVMe devices are detected.
- Fans and temperature sensors report plausible values.

### Memory Stability

- Confirm the reported failed slot behavior.
- Run an extended memory test.
- Record errors, slot placement, and final stable topology.
- Do not migrate stable workloads if any unexplained memory errors remain.

### Thermal and Power Validation

- Record idle temperatures.
- Record sustained-load temperatures.
- Verify the Noctua cooler remains securely mounted.
- Observe startup and load power consumption before UPS selection.
- Confirm the existing 500 W power supply is stable under the intended load.

### Storage Validation

- Review SMART or NVMe health data.
- Run non-destructive read and performance checks.
- Select a documented storage layout.
- Decide which data is local, backed up, replaceable, or portable.
- Avoid treating redundancy as a substitute for backup.

### Network and Hypervisor Validation

- Confirm stable wired network connectivity.
- Install and update the selected hypervisor.
- Configure internal-only management access.
- Apply a named-administrator and break-glass authentication model.
- Add Node Exporter or equivalent baseline host monitoring.
- Confirm Prometheus and Grafana visibility.
- Integrate the host into Project 003 backup and restore design before stable workload migration.

## Migration Gate

No stable VM should move to this server until:

- Hardware and memory tests pass.
- Thermals are acceptable.
- Storage health and layout are documented.
- Network and management access are validated.
- Monitoring is active.
- Backup destination and restore process are available.
- The target role is recorded in an ADR.
- A rollback plan exists for each migrated workload.

## Security Considerations

- Do not publish serial numbers, MAC addresses, BIOS identifiers, or exact management addresses.
- Do not reuse default hypervisor credentials.
- Keep management internal-only.
- Use named routine administration and preserve a protected break-glass path.
- Keep recovery keys and TOTP material outside Git.
- Review firmware and update requirements before production use.
- Do not host intentionally vulnerable workloads until network isolation is implemented.

## Power and UPS Dependencies

Project 005 should follow server validation because UPS sizing depends on measured rather than assumed load.

Required measurements:

- Idle power.
- Normal infrastructure workload power.
- Startup power.
- Sustained higher-load power.
- Combined load if both virtualization hosts remain active.

The UPS design must include:

- Adequate load capacity and runtime.
- Monitoring support where practical.
- Orderly guest shutdown.
- Orderly hypervisor shutdown.
- Documented recovery after utility power returns.
- Battery-health and replacement procedures.

## Future Improvements

- Complete physical assembly.
- Record validated BIOS and firmware state.
- Confirm final memory topology and failed-slot behavior.
- Select and document the NVMe storage layout.
- Measure thermals and power consumption.
- Install and harden the hypervisor.
- Integrate host monitoring.
- Integrate backup and restore coverage.
- Create an ADR for the server's production role.
- Update architecture diagrams and workload placement after the role is approved.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Current Proxmox Host](server.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Roadmap](../../ROADMAP.md)
