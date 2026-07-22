# Storage Architecture

## Purpose

Describe the current storage design, backup layers, recovery assets, operational controls, and future storage direction for the homelab.

The goal is to make storage changes understandable, recoverable, and safe to operate without publishing private device identifiers, certificate keys, or recovery artifacts.

## Current Status

Projects 003 and 004 established the current backup and recovery baseline.

Current state:

- The active Proxmox host uses a local 1 TB PCIe SSD for the hypervisor and VM storage.
- A dedicated 5 TB external hard drive provides Proxmox VM backup storage.
- The external target uses ext4 and a persistent UUID-based mount.
- Proxmox registers the target as backup-only directory storage.
- Mount-point enforcement prevents backup data from silently falling through to the host root filesystem when the external disk is absent.
- `dns01`, `mon01`, and `proxy01` receive daily snapshot-mode, Zstandard-compressed backups.
- Retention keeps 7 daily, 4 weekly, and 3 monthly backups.
- `dns01` and `proxy01` completed representative isolated restore tests.
- `mon01` has successful backup coverage but has not been independently restore-tested.
- Portable application exports, private PKI material, and rebuild documentation remain additional recovery layers.

## Design Goals

- Keep active workload storage separate from backup storage.
- Use stable identifiers instead of volatile device names.
- Fail visibly when the intended backup filesystem is unavailable.
- Define what must be preserved versus what can be rebuilt.
- Combine whole-VM backups with portable exports, protected keys, and documentation.
- Test restoration rather than treating backup completion as sufficient evidence.
- Protect backup storage and PKI material from untrusted or experimental workloads.
- Keep public documentation specific enough to demonstrate engineering decisions without exposing private operational data.

## Current Storage Components

| Component | Role | Current status | Public documentation boundary |
| --- | --- | --- | --- |
| Proxmox host 1 TB PCIe SSD | Hypervisor, local VM disks, ISOs, and active service state | Active | Exact device and storage identifiers omitted |
| 5 TB external HDD | Dedicated Proxmox backup destination for core VMs | Active and restore-tested through `dns01` and `proxy01` | Model, serial, UUID, exact backup names, and private identifiers omitted |
| Private administrative-workstation storage | Protected location for application exports, certificate material, and hashes | Active supporting recovery layer | Exact paths, usernames, hashes, passphrases, and keys omitted |
| GitHub repository | Sanitized architecture, service, project, runbook, ADR, and change documentation | Active | No raw secrets, private exports, keys, or backup artifacts |
| Two 1 TB NVMe devices | Available expansion storage for the X299 server | Available; production role pending | Exact serial numbers and final pool names omitted |

## Logical Storage Layout

```text
Proxmox host: pve01
|
|-- Local system and VM storage
|   |-- Proxmox operating system
|   |-- dns01 virtual disk
|   |-- mon01 virtual disk
|   `-- proxy01 virtual disk
|
`-- Dedicated external backup storage
    |-- dns01 full-VM backups
    |-- mon01 full-VM backups
    `-- proxy01 full-VM backups

Separate protected recovery assets
|-- Pi-hole Teleporter export
|-- Grafana dashboard exports
|-- Prometheus and Blackbox configuration inventories
|-- Encrypted root CA private key and service certificate material
|-- Private PKI passphrase record stored separately
`-- Sanitized rebuild and restore documentation
```

The backup disk is separate from the active VM datastore but remains directly attached to the same physical host. It improves recovery from local datastore or VM failure but does not create an off-site or immutable copy.

## Backup Target Implementation

| Setting | Implemented design |
| --- | --- |
| Physical capacity | 5 TB marketed capacity |
| Filesystem | ext4 |
| Stable mount | Filesystem UUID retained privately |
| Public mount placeholder | `<BACKUP_MOUNT>` |
| Proxmox storage placeholder | `<BACKUP_TARGET>` |
| Storage type | Directory |
| Allowed content | Backup artifacts only |
| Mount safety | Proxmox mount-point enforcement enabled |
| Backup mode | Snapshot |
| Compression | Zstandard |
| Schedule | Daily at 10:00 local time |
| Retention | 7 daily, 4 weekly, 3 monthly |
| Protected VMs | `dns01`, `mon01`, `proxy01` |

Initial device validation included SMART health, an extended self-test, expected usable capacity, and verification that no reallocated, pending, or uncorrectable sectors were reported.

## Storage Categories

| Category | Purpose | Recovery expectation |
| --- | --- | --- |
| Hypervisor system storage | Proxmox operating system and host configuration | Rebuildable from documentation and protected private records |
| VM disks | Workload operating systems and application state | Protected by scheduled full-VM backups |
| Service configuration | Pi-hole, Prometheus, Blackbox Exporter, Grafana, NGINX Proxy Manager, and future service configuration | Protected through VM backup, reviewed inventory, or application export |
| Application exports | Pi-hole Teleporter and Grafana dashboard JSON | Portable recovery layer; private and independently maintained |
| PKI material | Root CA key, root certificate, service keys, certificates, and issuance records | Protected private storage; root key requires a second failure-domain copy |
| Metrics history | Prometheus local time-series data | Preserved by VM backup but lower priority than configuration for manual rebuild |
| Replaceable content | Package files, plugins, ISOs, images, and caches | Reinstall or redownload unless custom requirements exist |
| Backup storage | Dedicated external destination | Separate from source storage, backup-only, mount-protected, and restore-tested |
| Documentation | Sanitized architecture and operational knowledge | Version-controlled in GitHub; not a substitute for protected service state |

## Recovery Layers

### `dns01`

1. Daily Proxmox VM backup.
2. Protected Pi-hole Teleporter export.
3. Sanitized Pi-hole, networking, and monitoring documentation.
4. Package and service-state inventory.
5. Tested isolated whole-VM restore procedure.

The restore test proved VM reconstruction, Debian boot, filesystem availability, Pi-hole FTL startup, and Node Exporter startup. Network-facing DNS validation was intentionally outside the isolated test boundary.

### `mon01`

1. Daily Proxmox VM backup.
2. Prometheus and Blackbox Exporter configuration inventory.
3. Grafana database and data-source recovery mapping.
4. Protected dashboard exports.
5. Sanitized service and troubleshooting documentation.

The Infrastructure Overview requires a refreshed private export after the Project 004 panel additions. The VM is backed up, but an independent `mon01` restore test remains future work.

### `proxy01`

1. Daily Proxmox VM backup.
2. Compose definition under `/opt/nginx-proxy-manager/`.
3. NGINX Proxy Manager database, route definitions, and imported service-certificate state.
4. Protected service certificate and key copy outside the VM.
5. NGINX Proxy Manager service documentation and certificate lifecycle runbook.
6. Tested isolated whole-VM restore procedure.

The restore test proved Debian boot, Docker, QEMU Guest Agent, Node Exporter, NGINX Proxy Manager, expected listeners, and persistent data and certificate directories. It did not prove a live network cutover or root CA private-key recovery.

### Private Root CA

Required layers:

1. Encrypted primary root CA private key.
2. Passphrase stored separately.
3. Public root CA certificate.
4. Certificate issuance and recovery runbook.
5. Second encrypted or offline private-key copy in a separate failure domain.

The fifth layer remains a documented follow-up. The root CA private key is intentionally excluded from `proxy01` and its VM backups.

## Backup Philosophy

Backups are designed around restore requirements rather than only scheduled copies.

For each stable service, documentation should identify:

- Critical state.
- Backup method.
- Destination.
- Frequency.
- Retention.
- Restore order.
- Post-restore validation.
- Last successful restore-test date.
- Known validation boundaries.

A successful backup that has never been restored should be treated as less mature than a tested recovery path.

Application exports do not replace VM backups. VM backups do not replace dependency knowledge, certificate-key protection, configuration inventories, or manual rebuild documentation.

## Mount-Point Safety

Removable backup storage creates a specific operational risk: the intended mount directory may still exist when the disk is absent.

The implemented mitigation is:

- Persistent UUID mounting.
- A dedicated mount path.
- Proxmox `is_mountpoint` enforcement.
- Routine verification with `findmnt`, `df`, and `pvesm status`.

The correct failure mode is for the backup storage to become unavailable and the job to fail visibly.

## Recovery Priority

1. Restore physical network and Proxmox management access.
2. Confirm local VM storage and the external backup target.
3. Restore `dns01` and validate public plus local DNS.
4. Restore `proxy01` if friendly HTTPS access is operationally required; direct backend paths remain available during proxy outage.
5. Restore `mon01` and validate Prometheus, exporters, Grafana, and dashboard state.
6. Confirm host, DNS, HTTPS, and certificate monitoring.
7. Restore lower-priority or experimental workloads.

## Public Documentation Rules

Do not publish:

- Disk serial numbers.
- Filesystem or partition UUIDs.
- Exact backup volume names or filenames.
- Raw task logs containing private identifiers.
- Personal mount, export, or PKI paths.
- Private hashes when they add no public value.
- Backup encryption keys, CA private keys, service private keys, or passphrases.
- Raw application exports, proxy databases, or VM backup artifacts.

Use placeholders:

- `<PRIMARY_DATASTORE>`
- `<VM_STORAGE>`
- `<BACKUP_TARGET>`
- `<BACKUP_MOUNT>`
- `<BACKUP_DEVICE>`
- `<BACKUP_VOLUME_ID>`
- `<PRIVATE_EXPORT_ROOT>`
- `<PRIVATE_PKI_DIRECTORY>`
- `<ENCRYPTION_KEY_STORED_IN_PASSWORD_MANAGER>`

## Security Considerations

- Backup targets should not be writable from every workload.
- Backup artifacts contain complete VM state and must be treated as sensitive.
- `proxy01` backups contain service private-key material.
- Security-lab workloads must not control trusted backup storage or access PKI material.
- Administrative storage interfaces remain internal-only.
- Raw Pi-hole, Grafana, and proxy exports remain outside Git.
- Future encryption keys must be stored separately from the media.
- A single connected disk does not protect against every physical, electrical, malware, or operator failure.

## Maintenance Notes

- Review scheduled backup results rather than assuming the job ran.
- Review free capacity and pruning behavior.
- Check that new stable VMs are added to backup coverage.
- Remove retired VM backups only through an intentional retention decision.
- Review SMART health periodically and after unusual I/O behavior.
- Re-test restoration after major Proxmox upgrades, storage changes, migrations, proxy upgrades, or PKI changes.
- Refresh application exports after meaningful service changes.
- Verify protected PKI copies remain readable without exposing their contents.
- Document drive replacement, filesystem changes, schedule changes, retention changes, and certificate-storage changes.

## Known Limitations

- The backup drive is normally connected to the same host and physical location.
- It is not immutable, offline, or off-site.
- Backup task, age, and capacity alerting are not yet implemented.
- `mon01` has not been independently restored.
- Isolated restore tests did not exercise production network behavior.
- The root CA private key still requires a second protected copy in a separate failure domain.

## Future Improvements

- Add backup job, age, failure, and capacity monitoring.
- Define an actionable notification and response process.
- Perform an independent `mon01` restore test.
- Refresh and privately validate the Homelab Infrastructure Overview export.
- Create a second encrypted or offline root CA private-key copy.
- Document the future server's validated storage layout.
- Evaluate an offline rotation, off-site copy, NAS, or Proxmox Backup Server when justified.
- Create recovery-time and recovery-point objectives after more measured experience.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Security Architecture](security.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Project 004: Reverse Proxy and Internal HTTPS](../projects/project-004-reverse-proxy-internal-https.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore Runbook](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Service Configuration Export and Inspection](../runbooks/service-config-export.md)
- [Hardware Inventory](../hardware/inventory.md)
