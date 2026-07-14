# Project 003: Backup and Recovery

## Status

| Area | Details |
| --- | --- |
| Status | Completed |
| Start date | 2026-07-09 |
| Completion date | 2026-07-14 |
| Owner | Homelab administrator |
| Related services | Proxmox VE, Pi-hole, Prometheus, Grafana, Node Exporter, Blackbox Exporter |

Project 003 established the homelab's first operational VM backup system and proved a representative whole-VM restore path.

## Purpose

Establish a documented, scheduled, and testable backup and recovery process for the stable infrastructure VMs.

The project combined:

- Whole-VM Proxmox backups for rapid recovery.
- Application-level exports for portability.
- Configuration and dependency inventories for manual reconstruction.
- A representative isolated restore test.
- Public, sanitized recovery documentation.

The guiding question was:

> If this VM failed tonight, what information and service state would be required to recover it safely?

## Objectives

- Identify critical service state and dependencies on `dns01` and `mon01`.
- Assign recovery priority based on operational impact.
- Create protected Pi-hole and Grafana recovery exports.
- Deploy backup storage separate from the Proxmox VM datastore.
- Configure automatic VM backup scheduling and retention.
- Complete initial backups for both stable VMs.
- Restore at least one representative VM without overwriting production.
- Document the proven recovery process and its remaining boundaries.

## Scope Completed

### Backup Readiness

- Inventoried `dns01` and `mon01` services, packages, configuration locations, state, and dependencies.
- Created and privately inspected a Pi-hole Teleporter export.
- Created and privately inspected the existing Grafana dashboard exports.
- Documented Prometheus and Blackbox Exporter configuration requirements.
- Documented the Grafana Prometheus data-source recovery mapping.
- Classified replaceable content separately from essential configuration and service state.
- Added the service configuration export and inspection runbook.

### Backup Storage

- Acquired and identified a dedicated 5 TB external hard drive.
- Confirmed expected capacity before destructive operations.
- Confirmed SMART overall health passed.
- Completed an extended SMART self-test without error.
- Replaced the factory NTFS filesystem with ext4.
- Configured persistent mounting by private filesystem UUID.
- Registered the target as Proxmox directory storage.
- Restricted the target to backup content.
- Enabled mount-point enforcement to prevent backups from falling through to the host root filesystem when the external disk is absent.

### Backup Jobs

- Completed initial manual backups of `dns01` and `mon01`.
- Configured daily snapshot-mode backups.
- Configured Zstandard compression.
- Configured retention for:
  - 7 daily backups.
  - 4 weekly backups.
  - 3 monthly backups.
- Kept exact storage identifiers, volume names, drive UUIDs, and artifact filenames outside the public repository.

### Restore Validation

- Restored the `dns01` backup to a temporary VM on normal VM storage.
- Used a different VM ID so the active production guest was not overwritten.
- Renamed the restored copy clearly as a restore-test guest.
- Removed the restored VM's network adapter before boot.
- Confirmed the restored Debian operating system reached a normal login prompt.
- Confirmed the expected root filesystem and disk were present.
- Confirmed `pihole-FTL` was active.
- Confirmed `prometheus-node-exporter` was active.
- Reviewed failed units and identified `openipmi.service` as nonblocking in the QEMU VM environment.
- Shut down and deleted the temporary restored VM after validation.

## Architecture Impact

| Area | Impact |
| --- | --- |
| Network | No permanent topology change. Restore testing used a network-isolated temporary VM. |
| Virtualization | `dns01` and `mon01` now receive automatic full-VM backups through Proxmox. |
| Storage | Added a dedicated 5 TB external ext4 backup destination separate from the active VM datastore. |
| Monitoring | Monitoring configuration, Grafana state, dashboard exports, and both DNS probe definitions are recovery assets. |
| Security | Backup artifacts and raw exports remain private; mount-point enforcement reduces accidental host-root writes. |
| Operations | Daily backups, tiered retention, tested restore steps, and recovery order are now documented. |

## Design Decisions

| Decision | Reason | Tradeoff |
| --- | --- | --- |
| Inventory service state before backup implementation | A backup file does not explain service dependencies or validation requirements. | Implementation took longer but produced a more complete recovery design. |
| Use a dedicated direct-attached external disk | Separates backups from the VM datastore without adding another server. | The copy remains in the same physical location and is not immutable or off-site. |
| Use ext4 | Native Linux filesystem behavior is appropriate for a dedicated Proxmox target. | The drive is less convenient for direct Windows use. |
| Mount by UUID | Avoids unstable `/dev/sdX` device naming. | The exact UUID must be retained privately. |
| Enforce the mount point in Proxmox | Prevents a missing external disk from causing backups to consume the host root filesystem. | Backup jobs fail visibly when the target is unavailable. |
| Use snapshot mode and Zstandard | Minimizes service interruption and provides practical compression. | Full backups still consume more capacity than a deduplicating platform. |
| Retain daily, weekly, and monthly generations | Balances recent recovery points with limited historical depth. | Capacity and pruning must be reviewed over time. |
| Use VM backups plus application exports | Supports both fast whole-system recovery and portable service recovery. | Multiple recovery layers require maintenance. |
| Restore `dns01` before `mon01` | DNS is foundational to normal service access and troubleshooting. | Monitoring visibility returns after DNS. |
| Test the restore without networking | Eliminates duplicate IP and service-conflict risk while production remains online. | End-to-end DNS and monitoring behavior were outside the isolated test boundary. |

The long-term design decision is recorded in [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md).

## Backup Inventory

| System | Role | Protection | Restore priority | Current maturity |
| --- | --- | --- | --- | --- |
| `dns01` | Pi-hole DNS and local records | Daily Proxmox VM backup, protected Teleporter export, and rebuild documentation | High | Backup successful; isolated whole-VM restore, boot, filesystem, Pi-hole, and Node Exporter validation complete |
| `mon01` | Monitoring and observability | Daily Proxmox VM backup, reviewed configuration inventory, protected dashboard exports, and rebuild documentation | Medium | Backup successful; independent whole-VM restore not yet performed |

## Backup Job Baseline

| Setting | Implemented value |
| --- | --- |
| Protected guests | `dns01`, `mon01` |
| Frequency | Daily |
| Local schedule | 10:00 |
| Mode | Snapshot |
| Compression | Zstandard |
| Daily retention | 7 |
| Weekly retention | 4 |
| Monthly retention | 3 |
| Missed-run repetition | Disabled in the initial configuration |
| Target type | Proxmox directory storage on a dedicated external ext4 filesystem |
| Content restriction | Backup artifacts only |
| Missing-mount protection | Enabled |

## Recovery Assets

### `dns01`

- Proxmox VM backup.
- Protected Pi-hole Teleporter archive.
- Pi-hole service, package, and configuration inventory.
- Static networking notes using private operational values.
- Node Exporter service-state inventory.
- Recursive and local DNS post-recovery validation requirements.

### `mon01`

- Proxmox VM backup.
- Prometheus and Blackbox Exporter configuration inventory.
- Grafana SQLite and data-source recovery mapping.
- Protected dashboard exports available at project completion.
- Required Prometheus jobs:
  - `prometheus`
  - `node_exporter`
  - `blackbox_dns`
  - `blackbox_dns_local`
- Required Blackbox modules:
  - `dns_udp`
  - `dns_udp_local`

The Homelab Infrastructure Overview remains operational but still requires a separate protected Classic JSON export. That export is useful follow-up work but is not a blocker for the proven full-VM backup and restore scope completed here.

## Validation Results

### Backup Target

- Expected 5 TB device identified before destructive operations.
- SMART overall-health result passed.
- Extended SMART self-test completed without error.
- No reallocated, pending, or uncorrectable sectors were reported during initial inspection.
- ext4 filesystem mounted with expected multi-terabyte usable capacity.
- Proxmox reported the backup storage active.
- Backup content restriction and mount-point enforcement were present in the storage configuration.

### Initial Backups

- `dns01` backup completed successfully and produced a plausible compressed artifact.
- `mon01` backup completed successfully.
- The scheduled job includes both stable infrastructure VMs.
- Retention settings were visible through the Proxmox cluster backup configuration.

### `dns01` Isolated Restore

Proven:

- Backup artifact readability.
- Proxmox VM reconstruction.
- Restoration to separate VM storage and ID.
- Safe network isolation before boot.
- Debian boot to a login prompt.
- Root filesystem availability.
- `pihole-FTL` active.
- Node Exporter active.
- Safe cleanup of the temporary restored VM.

Not proven by the isolated test:

- Client DNS queries.
- Local-record responses over the network.
- Remote Node Exporter reachability.
- Prometheus target state.
- Recursive and local Blackbox probe success.

Those checks require a controlled network-connected restore or an actual replacement recovery after the original guest is confirmed offline.

## Recovery Order

1. Restore physical power and network connectivity.
2. Restore Proxmox management access and confirm storage state.
3. Restore `dns01` and validate public and local DNS.
4. Restore `mon01` and validate Prometheus, exporters, Grafana, and all intended targets.
5. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
6. Restore lower-priority or experimental workloads.
7. Review logs and update documentation with any deviations.

## Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| External target is absent | Backup job cannot write to intended storage | UUID mount plus Proxmox mount-point enforcement causes visible failure instead of root-filesystem fallback |
| Backup artifact contains secrets and private state | Sensitive data exposure | Keep artifacts, raw exports, hashes, identifiers, and logs outside Git |
| Backup completes but restore fails | False confidence in recovery | Require representative restore testing and document its exact boundary |
| Duplicate restored VM reaches the LAN | Address, hostname, or service conflict | Restore under a temporary ID and remove the network adapter before boot |
| Single connected disk is damaged with the host | Loss of first recovery copy | Evaluate offline, rotated, off-site, NAS, or Proxmox Backup Server copies later |
| Scheduled run is missed | Recovery point becomes older than expected | Review job history and reconsider missed-run behavior if host uptime changes |
| `mon01` backup is untested | Monitoring recovery remains less proven | Perform an independent restore after major changes or before migration |
| Application exports become stale | Manual or selective recovery loses recent state | Refresh private exports after meaningful service changes |

## Lessons Learned

- Destructive disk work must begin with positive identification by capacity and hardware identity.
- Manufacturer decimal terabytes and Linux binary capacity reporting produce different but expected values.
- SMART health plus an extended self-test provides stronger evidence than a quick filesystem check.
- UUID-based mounting is safer than relying on device names.
- Removable Proxmox storage needs explicit mount-point enforcement.
- A backup system is not complete until a restore has succeeded.
- Temporary restore VMs should be isolated before their first boot.
- Local service state and end-to-end network service behavior are different validation layers.
- A failed virtual-hardware service does not automatically indicate a failed restore; the service's relevance must be assessed.
- Backup maturity should be documented per VM rather than generalized across every protected workload.
- Whole-VM backups, portable exports, and rebuild documentation solve different recovery problems and work best together.

## Follow-Up Work

Project 003 is complete. The following are operational improvements rather than completion blockers:

- [ ] Observe scheduled executions and pruning over time.
- [ ] Add backup job, backup age, storage capacity, and failure monitoring through a least-privilege Proxmox integration.
- [ ] Define an actionable failure-notification path.
- [ ] Perform an independent `mon01` restore test.
- [ ] Perform a controlled network-connected `dns01` validation when duplicate identity risk can be eliminated.
- [ ] Export and privately validate the Homelab Infrastructure Overview.
- [ ] Remove obsolete installer ISO attachments from stable VMs after confirming they are unnecessary.
- [ ] Evaluate a second copy in a separate failure domain.
- [ ] Re-test restoration after major Proxmox upgrades, storage changes, or service migrations.

## Related Documentation

- [Projects README](README.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Project Completion Change Record](../changes/2026-07-14-project-003-backup-recovery-completion.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Service Configuration Export and Inspection](../runbooks/service-config-export.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Hardware Inventory](../hardware/inventory.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)