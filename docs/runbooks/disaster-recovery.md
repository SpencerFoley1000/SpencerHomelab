# Disaster Recovery Runbook

## Purpose

Define the recovery order, decision points, service-validation requirements, and documentation process after hardware failure, configuration loss, or a major infrastructure outage.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Operational baseline with representative restore validation |
| Project | Project 003: Backup and Recovery |
| Recovery inventory | Complete for `dns01` and `mon01` |
| VM backup recovery | Implemented for both VMs; isolated `dns01` restore tested |
| Application exports | Pi-hole and existing Grafana exports privately inspected; imports not independently tested |
| Last reviewed | 2026-07-14 |

The whole-VM restore path is proven for `dns01` through an isolated boot and local service validation. End-to-end network behavior remains a required step during a controlled connected test or actual replacement recovery.

## Recovery Principles

- Protect people and hardware before restoring services.
- Identify the failure domain before changing systems.
- Restore foundational dependencies before dependent services.
- Preserve failed-state evidence where practical.
- Keep restored systems isolated when corruption, compromise, or duplicate identity is possible.
- Prefer a validated VM restore when available, while retaining manual rebuild paths.
- Treat backup artifacts and recovery exports as sensitive.
- Document deviations and permanent fixes.

## Recovery Priorities

1. Restore electrical power and physical network connectivity.
2. Restore the homelab routing boundary and managed switching.
3. Restore Proxmox management access on the active virtualization host.
4. Confirm the external backup target is mounted and active.
5. Restore `dns01` and validate public plus local DNS.
6. Restore `mon01` and validate Prometheus, exporters, and Grafana.
7. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
8. Restore lower-priority or experimental workloads.
9. Review logs, backup state, and documentation after recovery.

Future reverse proxy, certificate, identity, and security services must be inserted according to documented dependencies.

## Required Private Information

Keep outside this repository:

- Router and switch access details.
- Proxmox management endpoint and administrative identities.
- TOTP recovery material and physical-console instructions.
- Exact VM network values and VM IDs.
- Backup drive identity, filesystem UUID, and mount details.
- Proxmox backup storage and volume identifiers.
- Application-export locations and hashes.
- Grafana data-source UID.
- Encryption keys or backup credentials.

Public placeholders include:

- `<ROUTER_RECOVERY_NOTES>`
- `<SWITCH_RECOVERY_NOTES>`
- `<PROXMOX_MANAGEMENT_ENDPOINT>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<BACKUP_MOUNT>`
- `<BACKUP_TARGET>`
- `<BACKUP_VOLUME_ID>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Initial Assessment

1. Determine whether the issue is power, hardware, network, hypervisor, VM, application, storage, authentication, or compromise related.
2. Confirm whether corruption or malicious activity is suspected.
3. Preserve logs, task results, hardware errors, and failed-state evidence where practical.
4. Confirm the latest known-good backup without modifying it.
5. Confirm `<BACKUP_MOUNT>` is the actual mounted backup filesystem.
6. Decide whether recovery will use:
   - a Proxmox VM backup,
   - a portable application export,
   - manual reconstruction,
   - or a combination.
7. Prevent duplicate addresses and hostnames by isolating restored guests until the original instance is confirmed offline.
8. Define the validation boundary before starting so local boot success is not mistaken for complete service recovery.

## Network and Proxmox Recovery

1. Confirm the router and managed switch have power and expected link state.
2. Restore the homelab routing boundary using protected records.
3. Confirm a trusted administrative system can reach the Proxmox management plane.
4. Use `<PROXMOX_ADMIN_ACCOUNT>` for routine administration when available.
5. Use the protected `root@pam` break-glass path only when required.
6. Confirm system time before relying on TOTP.
7. Use physical-console access if network administration cannot be recovered safely.
8. Confirm Proxmox storage and VM inventory before starting guests.
9. Verify the backup mount and storage state:

   ```bash
   findmnt <BACKUP_MOUNT>
   df -h <BACKUP_MOUNT>
   pvesm status
   ```

10. Confirm the intended backup artifact exists:

    ```bash
    pvesm list <BACKUP_TARGET>
    ```

Do not bypass mount-point enforcement or write recovery data into the Proxmox root filesystem.

## VM Restore Safety

For a test or when the original VM may still return:

- Restore to a different VM ID.
- Use a clearly temporary name.
- Remove the virtual network adapter before boot.
- Validate through the Proxmox console.
- Delete the temporary VM after testing.

Use the tested [Proxmox VM Restore Runbook](proxmox-vm-restore.md).

For an actual replacement recovery:

- Confirm the failed or old VM cannot reconnect unexpectedly.
- Review restored networking before connection.
- Reconnect only after duplicate identity risk is eliminated.
- Perform complete network and monitoring validation.

## `dns01` Recovery

### Preferred VM Restore

1. Select the latest appropriate `dns01` backup.
2. Restore without overwriting a potentially recoverable source VM unless replacement is intentional.
3. Keep the restored VM network-isolated during initial boot validation.
4. Confirm Debian reaches a login prompt.
5. Confirm the expected filesystem is mounted.
6. Confirm local service state:

   ```bash
   systemctl is-active pihole-FTL
   systemctl is-active prometheus-node-exporter
   systemctl --failed
   ```

7. Assess every failed unit. During the Project 003 test, `openipmi.service` was nonblocking because the guest had no physical BMC/IPMI hardware.
8. Confirm the original VM cannot conflict with the restored copy.
9. Review the intended network adapter, bridge, and private static configuration.
10. Reconnect networking.
11. Validate local and recursive DNS from a trusted client.
12. Confirm remote monitoring recovers.

### Manual Rebuild

1. Deploy a supported Debian VM.
2. Recreate static networking using protected operational values.
3. Install Pi-hole and Node Exporter.
4. Import the protected Pi-hole Teleporter archive.
5. Confirm upstream resolver settings and local records.
6. Validate services and monitoring.

### Required Validation

Local service state:

```bash
systemctl is-active pihole-FTL
systemctl is-active prometheus-node-exporter
```

Prometheus and probe validation:

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

Expected results are `1` after networking is restored.

Also confirm:

- A trusted client resolves a public name through Pi-hole.
- Required local records return expected answers.
- No duplicate address or hostname exists.

## `mon01` Recovery

### Preferred VM Restore

1. Select the latest appropriate `mon01` backup.
2. Restore in an isolated or controlled state.
3. Confirm Debian and the expected filesystem boot normally.
4. Confirm service state:

   ```bash
   systemctl is-active prometheus
   systemctl is-active grafana-server
   systemctl is-active prometheus-node-exporter
   systemctl is-active prometheus-blackbox-exporter
   ```

5. Validate Prometheus configuration.
6. Confirm required jobs and targets exist.
7. Confirm both Blackbox modules and DNS jobs work.
8. Confirm the Grafana Prometheus data source is healthy.
9. Confirm protected dashboards display current data.

`mon01` has successful backup coverage but was not independently restore-tested during Project 003. Treat its VM restore path as less mature than `dns01` until exercised.

### Manual Rebuild

1. Deploy a supported Debian VM.
2. Install Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
3. Restore or recreate `/etc/prometheus/prometheus.yml` and `/etc/prometheus/blackbox.yml`.
4. Confirm Prometheus jobs:
   - `prometheus`
   - `node_exporter`
   - `blackbox_dns`
   - `blackbox_dns_local`
5. Confirm Blackbox modules:
   - `dns_udp`
   - `dns_udp_local`
6. Restore Grafana consistently or recreate its Prometheus data source.
7. Import available protected dashboard JSON.
8. Verify data-source mappings, panels, and variables.

### Required Monitoring Validation

```promql
count by (job, instance) (up)
```

```promql
up{job="node_exporter"}
```

```promql
probe_success{job=~"blackbox_dns.*", host="dns01"}
```

Expected host targets are `mon01`, `dns01`, and `pve01`. Both DNS probe series should return `1`.

## Post-Recovery Validation

Confirm:

- Trusted clients have expected network connectivity.
- Proxmox routine and break-glass management paths work.
- Backup storage is mounted and active.
- `dns01` answers public and local DNS queries.
- `mon01` observes all intended host and service targets.
- Grafana dashboards show current data.
- No duplicate VMs, hostnames, MAC addresses, or IP addresses remain.
- Temporary recovery adapters, credentials, or firewall exceptions are removed.
- Logs show no unresolved recurring failure.
- A new backup is created after stable production recovery when appropriate.

## Restore-Test Evidence

The 2026-07-14 `dns01` test proved:

- Backup artifact readability.
- VM reconstruction on normal Proxmox storage.
- Safe restoration under a different VM ID.
- Network isolation before startup.
- Debian boot and filesystem availability.
- Pi-hole FTL and Node Exporter local service startup.
- Safe destruction of the temporary restore VM.

It did not prove network-facing DNS or monitoring behavior because the virtual NIC was removed. Public documentation must preserve that distinction.

## Post-Recovery Review

Document:

- Failure scope and likely root cause.
- Recovery method and artifact used.
- Recovery start and completion time.
- Validation performed.
- What worked well.
- Deviations from the runbook.
- Temporary actions removed.
- Permanent fixes or architecture changes.
- Whether backup, monitoring, security, storage, or documentation controls should change.

Update:

- Relevant service pages.
- [Project 003](../projects/project-003-backup-recovery.md).
- [Storage Architecture](../architecture/storage.md).
- [VM Inventory](../architecture/vm-inventory.md).
- The repository changelog or a dated change record.
- The roadmap if priorities changed.

## Security Considerations

- Do not publish recovery keys, TOTP seeds, backup credentials, private paths, or backup identifiers.
- Treat restored systems as untrusted until the source and incident scope are understood.
- Never connect duplicate restored guests to production.
- Remove temporary credentials and emergency access after recovery.
- Keep attacker-style workloads away from trusted backup storage.
- Rotate affected credentials after suspected compromise.
- Do not rely on the directly attached drive as the only future copy for high-value data.

## Remaining Improvements

- Perform an independent `mon01` restore test.
- Perform a controlled network-connected `dns01` test when the original guest can be safely isolated.
- Add measured recovery-time and recovery-point objectives.
- Add backup task, age, capacity, and failure monitoring.
- Add future reverse proxy, certificate, and identity dependencies after deployment.
- Create a second backup copy in a separate failure domain when justified.

## Related Documentation

- [Backup Runbook](backup.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0003: Direct-Attached Proxmox Backup Storage](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Storage Architecture](../architecture/storage.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Security Architecture](../architecture/security.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)