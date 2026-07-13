# Disaster Recovery Runbook

## Purpose

Define the current recovery order, required information, service-validation expectations, and documentation process after hardware failure, configuration loss, or a major infrastructure outage.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Planned / unvalidated recovery baseline |
| Project | Project 003: Backup and Recovery |
| Recovery inventory | Complete for `dns01` and `mon01` |
| VM backup recovery | Not yet implemented or restore-tested |
| Application exports | Pi-hole and existing Grafana exports privately inspected; imports untested |
| Last reviewed | 2026-07-12 |

This document is not a proven disaster-recovery procedure. It records the current intended sequence and must be revised after a controlled restore test.

## Recovery Principles

- Protect people and hardware before restoring services.
- Identify the failure domain before making changes.
- Restore foundational dependencies before dependent services.
- Keep failed systems isolated when corruption, compromise, or address conflict is possible.
- Prefer a validated VM restore when available, but retain manual rebuild paths.
- Never publish credentials, recovery keys, private addresses, drive identifiers, or raw backup artifacts.
- Document deviations from the expected recovery process.

## Recovery Priorities

Current order:

1. Restore electrical power and physical network connectivity.
2. Restore the homelab routing boundary and managed switching.
3. Restore Proxmox management access on the active virtualization host.
4. Restore `dns01` and validate recursive and local DNS.
5. Restore `mon01` and validate Prometheus, exporters, and Grafana.
6. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
7. Restore lower-priority or experimental workloads.
8. Review logs, backup state, and documentation after recovery.

Future identity or reverse-proxy services must be inserted into this order only after their dependencies and recovery requirements are documented.

## Required Private Information

Sensitive values must remain outside this repository.

Private recovery records should contain:

- Router and switch access details.
- Proxmox management endpoint and protected administrative identities.
- TOTP recovery material and physical-console instructions.
- Exact VM network values.
- External backup-drive identity and mount details.
- Proxmox backup storage identifier.
- Application-export locations and hashes.
- Grafana data-source UID.
- Any encryption keys or backup credentials.

Public placeholders include:

- `<ROUTER_RECOVERY_NOTES>`
- `<SWITCH_RECOVERY_NOTES>`
- `<PROXMOX_MANAGEMENT_ENDPOINT>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<HYPERVISOR_BACKUP_LOCATION>`
- `<BACKUP_TARGET>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Initial Assessment

1. Determine whether the issue is power, hardware, network, hypervisor, VM, application, storage, or authentication related.
2. Confirm whether data corruption or compromise is suspected.
3. Preserve relevant logs and failed-state evidence where practical.
4. Confirm the last known-good backup or application export without modifying it.
5. Decide whether recovery will use:
   - a Proxmox VM backup,
   - a portable application export,
   - manual service reconstruction,
   - or a combination.
6. Prevent duplicate addresses by isolating restored guests until the active instance is confirmed offline.

## Network and Proxmox Recovery

1. Confirm the router and managed switch have power and expected link state.
2. Restore the homelab routing boundary using protected private records.
3. Confirm a trusted administrative system can reach the Proxmox management plane.
4. Use the named routine administrator when available.
5. Use the protected root break-glass path only for emergencies or root-only operations.
6. Confirm system time is accurate before relying on TOTP.
7. Use physical-console access if network authentication cannot be recovered safely.
8. Confirm Proxmox storage and VM inventory before starting guests.
9. Confirm the external backup target is present before attempting a VM restore.

## `dns01` Recovery

Preferred method:

1. Restore the latest validated Proxmox VM backup when available.
2. Keep the restored guest isolated until address conflicts are ruled out.
3. Start the VM and confirm Debian networking.
4. Confirm `pihole-FTL` and Node Exporter are active and enabled.
5. Validate required local records.
6. Validate public recursive resolution.
7. Reconnect the VM to the intended network only after validation.

Manual rebuild path:

1. Deploy a supported Debian VM.
2. Recreate static networking using protected operational values.
3. Install Pi-hole and Node Exporter.
4. Import the protected Pi-hole Teleporter archive.
5. Confirm upstream resolver settings and local records.
6. Validate services and monitoring.

Required validation:

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

All expected results should return `1`.

## `mon01` Recovery

Preferred method:

1. Restore the latest validated Proxmox VM backup when available.
2. Start the VM in a controlled state.
3. Confirm Prometheus, Grafana, Node Exporter, and Blackbox Exporter are active and enabled.
4. Validate Prometheus configuration.
5. Confirm all required jobs and targets exist.
6. Confirm both Blackbox modules and DNS jobs work.
7. Confirm the Grafana data source and dashboards display current data.

Manual rebuild path:

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
7. Import all available protected dashboard JSON.
8. Verify data-source mappings, panels, and variables.

Required monitoring validation:

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
- Proxmox management authentication works through the routine and protected recovery model.
- `dns01` answers public and local DNS queries.
- `mon01` observes all intended host and service targets.
- Grafana dashboards show current data.
- Backup storage is mounted and protected as intended.
- No duplicate VMs, hostnames, or addresses remain.
- Temporary recovery access or firewall exceptions are removed.
- Logs show no unresolved recurring failure.

## Post-Recovery Review

After an incident or restore test, document:

- Failure scope.
- Root cause, if known.
- Recovery method and artifact used.
- Start and completion time.
- Validation performed.
- What worked well.
- What differed from the runbook.
- What needs improvement.
- Whether backup, monitoring, security, or architecture controls should change.

Update:

- Relevant service pages.
- [Project 003](../projects/project-003-backup-recovery.md).
- [Storage Architecture](../architecture/storage.md).
- [VM Inventory](../architecture/vm-inventory.md).
- `CHANGELOG.md`.
- The roadmap if a milestone completed.

## Security Considerations

- Do not publish recovery keys, TOTP seeds, backup credentials, or exact private paths.
- Treat restored systems as untrusted until their source and integrity are understood.
- Do not connect duplicate restored guests to the production network.
- Remove temporary credentials and emergency access after recovery.
- Keep security-lab workloads away from trusted backup storage.
- Rotate affected credentials after suspected compromise.

## Remaining Work

- Integrate the 5 TB backup target.
- Run initial backups for `dns01` and `mon01`.
- Add a dedicated Proxmox VM restore runbook.
- Perform a representative isolated restore.
- Replace assumptions in this page with tested commands and timing.
- Add recovery-time and recovery-point objectives after measured experience exists.
- Add future reverse-proxy and identity dependencies when deployed.

## Related Documentation

- [Backup Runbook](backup.md)
- [Service Configuration Export and Inspection](service-config-export.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [Storage Architecture](../architecture/storage.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Security Architecture](../architecture/security.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Pi-hole Service](../services/pihole.md)
- [Prometheus Service](../services/prometheus.md)
- [Grafana Service](../services/grafana.md)
