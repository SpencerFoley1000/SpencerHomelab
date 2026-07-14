# Proxmox VM Restore Runbook

## Purpose

Provide a repeatable and safe process for restoring a Proxmox VM backup without overwriting the active guest or creating a duplicate network identity.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational / tested |
| Project | Project 003: Backup and Recovery |
| Last validated | 2026-07-14 |
| Validated guest | `dns01` |
| Validation boundary | Whole-VM restore, isolated boot, filesystem, and local service state |

The procedure was exercised successfully by restoring `dns01` to a temporary VM, removing its virtual network adapter before boot, validating the guest through the Proxmox console, and deleting the temporary VM afterward.

## Preconditions

- The intended backup artifact exists on `<BACKUP_TARGET>`.
- `<BACKUP_TARGET>` is mounted and reports active in Proxmox.
- The source VM remains intact unless this is an actual replacement recovery.
- An unused temporary VM ID is available.
- The target VM storage has enough free capacity.
- Proxmox root shell or equivalent authorized administrative access is available.
- Private recovery credentials and exact network values are available outside Git.

## Safety Rules

- Never restore over the active production VM during a test.
- Keep the restored guest disconnected until duplicate IP, hostname, MAC, and service risks are understood.
- Confirm the backup volume and destination VM ID before running `qmrestore`.
- Do not publish backup filenames, storage identifiers, drive UUIDs, serial numbers, or internal addresses.
- Delete only the temporary restored VM after validation; do not destroy the source VM.

## Identify the Backup

List backup artifacts:

```bash
pvesm list <BACKUP_TARGET>
```

Record the intended backup volume privately as:

```text
<BACKUP_VOLUME_ID>
```

Confirm the temporary VM ID is unused:

```bash
qm status <TEMP_VM_ID>
```

An error indicating that the VM does not exist is expected.

## Restore to an Isolated Temporary VM

Restore the backup to normal VM storage under the unused ID:

```bash
qmrestore <BACKUP_VOLUME_ID> <TEMP_VM_ID> \
  --storage <VM_STORAGE> \
  --unique 1
```

Rename the restored guest clearly:

```bash
qm set <TEMP_VM_ID> --name <GUEST>-restore-test
```

Inspect the configuration before boot:

```bash
qm config <TEMP_VM_ID>
```

Remove the virtual network adapter for the test:

```bash
qm set <TEMP_VM_ID> --delete net0
```

Verify that no network adapter remains:

```bash
qm config <TEMP_VM_ID> | grep -E '^(name|net|scsi|sata|virtio|ide|boot)'
```

The output must not contain a `net0` line.

## Boot and Validate

Start the temporary VM:

```bash
qm start <TEMP_VM_ID>
qm status <TEMP_VM_ID>
```

Open the Proxmox console and confirm the guest reaches its normal login prompt.

General guest checks:

```bash
hostnamectl
df -h
lsblk
systemctl --failed
```

Validate service-specific units. For `dns01`:

```bash
systemctl is-active pihole-FTL
systemctl is-active prometheus-node-exporter
```

Expected result for both units:

```text
active
```

During the 2026-07-14 validation, `openipmi.service` was the only failed unit. The restored guest is a QEMU VM without physical BMC/IPMI hardware, so this failure did not block recovery validation. Future failures must be assessed individually rather than ignored automatically.

## Validation Boundary

The isolated restore proves that:

- The backup artifact is readable.
- Proxmox can reconstruct the VM disk and configuration.
- The restored operating system boots.
- The expected filesystem is present.
- Local application services can start.
- A restored copy can be tested without overwriting production.

Because the network adapter is removed, this test does not prove:

- Client DNS resolution.
- Local DNS record responses.
- Remote Node Exporter reachability.
- Blackbox probe success.
- Production routing or firewall behavior.

Those checks belong to a controlled network recovery test or an actual replacement recovery after the original guest is confirmed offline.

## Cleanup

Shut down from inside the restored guest:

```bash
sudo poweroff
```

From the Proxmox host, confirm it is stopped:

```bash
qm status <TEMP_VM_ID>
```

Delete the temporary restored VM:

```bash
qm destroy <TEMP_VM_ID> --purge
```

Confirm the temporary VM no longer exists:

```bash
qm status <TEMP_VM_ID>
```

## Actual Recovery Differences

For a real replacement recovery:

1. Confirm the failed or old VM cannot return to the network unexpectedly.
2. Restore using an approved production VM ID and storage location.
3. Review the restored network adapter, bridge, MAC, and static guest configuration.
4. Reconnect networking only after duplicate identities are ruled out.
5. Validate the complete service path from trusted clients and monitoring systems.
6. Record the incident, artifact used, recovery duration, deviations, and permanent fixes.

## Post-Restore Validation

For `dns01` after reconnecting it in a controlled recovery:

- Confirm `pihole-FTL` and Node Exporter are active and enabled.
- Confirm public recursive DNS works.
- Confirm required local records return expected answers.
- Confirm Prometheus reports the `dns01` Node Exporter target as up.
- Confirm both recursive and local Blackbox DNS probes return success.

For `mon01`:

- Confirm Prometheus, Grafana, Node Exporter, and Blackbox Exporter are active and enabled.
- Validate Prometheus configuration and expected jobs.
- Confirm both Blackbox modules and DNS jobs exist.
- Confirm the Grafana data source and protected dashboards display current data.

## Documentation Requirements

After every restore test or real recovery, update:

- The affected VM entry in [VM Inventory](../architecture/vm-inventory.md).
- [Backup Runbook](backup.md).
- [Disaster Recovery Runbook](disaster-recovery.md).
- The related project page.
- The repository changelog or a dated change record.

Record what was proven and what remained outside the validation boundary.

## Related Documentation

- [Backup Runbook](backup.md)
- [Disaster Recovery Runbook](disaster-recovery.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Proxmox VE Platform](../services/proxmox.md)