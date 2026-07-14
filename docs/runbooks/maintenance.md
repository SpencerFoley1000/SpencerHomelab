# Maintenance Runbook

## Purpose

Provide a repeatable baseline for routine maintenance while protecting service availability, administrative access, monitoring, backups, and recovery options.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Draft baseline |
| Validation | Not yet exercised as one complete environment-specific maintenance window |
| Backup dependency | Operational; daily VM backups active and representative restore tested |
| Last reviewed | 2026-07-14 |

This runbook should gain measured timing and rollback details after the next planned Proxmox or core-service maintenance window.

## Maintenance Areas

- Debian guest updates.
- Proxmox host updates.
- Pi-hole updates.
- Prometheus, Grafana, and exporter updates.
- Firmware review.
- Backup and restore validation.
- Authentication and recovery-path review.
- Monitoring and log review.
- Hardware and capacity review.
- Documentation consistency review.

## Preconditions

Before maintenance:

- Define the objective, scope, affected systems, and expected disruption.
- Review relevant release notes.
- Confirm no unrelated incident is active.
- Confirm current health in Prometheus and Grafana.
- Confirm the backup filesystem is actually mounted.
- Confirm Proxmox reports the backup target active.
- Confirm a recent successful backup exists for each affected stable VM.
- Confirm application-level exports are current when relevant.
- Confirm routine and break-glass Proxmox access.
- Confirm physical-console access for hypervisor work.
- Create a rollback plan for configuration changes.
- Keep secrets and raw private output outside Git.

Backup checks:

```bash
findmnt <BACKUP_MOUNT>
df -h <BACKUP_MOUNT>
pvesm status
pvesm list <BACKUP_TARGET>
```

Do not proceed with high-impact maintenance when the only known-good recovery copy is unavailable or unverified.

## Procedure

1. Record the maintenance objective and affected systems.
2. Capture current versions and health state.
3. Create protected configuration rollback copies where appropriate.
4. Confirm backup and recovery assets.
5. Apply one logical change at a time.
6. Validate configuration syntax before reload or restart.
7. Prefer reload over restart when supported.
8. Reboot only when required.
9. Validate from the source layer outward.
10. Review logs for new errors.
11. Confirm monitoring and scheduled backup state.
12. Remove temporary rollback files only after a protected known-good copy exists.
13. Update documentation and the changelog for meaningful changes.

## Validation Order

### Network and Management

- Router and switch connectivity remain available.
- Proxmox is reachable from a trusted system.
- System time remains synchronized.
- The named routine administrator can authenticate.
- The protected break-glass and physical-console paths remain available.

### `pve01`

```bash
pveversion
systemctl is-active pve-firewall
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
timedatectl status
```

Prometheus:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

Backup validation:

```bash
findmnt <BACKUP_MOUNT>
pvesm status
pvesh get /cluster/backup --output-format yaml
```

Confirm the backup storage is active and the scheduled job remains enabled for `dns01` and `mon01`.

### `dns01`

```bash
systemctl is-active pihole-FTL prometheus-node-exporter
systemctl is-enabled pihole-FTL prometheus-node-exporter
pihole status
```

```promql
up{job="node_exporter", host="dns01"}
```

```promql
probe_success{job="blackbox_dns", host="dns01"}
```

```promql
probe_success{job="blackbox_dns_local", host="dns01", scope="local"}
```

### `mon01`

```bash
systemctl is-active prometheus grafana-server prometheus-node-exporter prometheus-blackbox-exporter
systemctl is-enabled prometheus grafana-server prometheus-node-exporter prometheus-blackbox-exporter
sudo promtool check config /etc/prometheus/prometheus.yml
```

Prometheus inventory:

```promql
count by (job, instance) (up)
```

Confirm these jobs exist:

- `prometheus`
- `node_exporter`
- `blackbox_dns`
- `blackbox_dns_local`

Grafana:

- All three hosts display current data.
- Recursive and Local DNS show current state.
- Dashboard timestamps advance normally.

### Post-Maintenance Backup

After a significant guest or hypervisor change:

- Confirm the next scheduled job succeeds, or run a deliberate manual backup when justified.
- Check artifact size and target capacity.
- Re-test restoration after major Proxmox, VM storage, backup storage, or migration changes.

## Rollback

If maintenance causes a failure:

1. Stop making additional changes.
2. Identify whether the issue is configuration, package, network, authentication, storage, or reboot related.
3. Restore the known-good configuration copy when applicable.
4. Revalidate syntax before restarting the service.
5. Revert packages only through a supported, documented method.
6. Use break-glass or physical-console access if routine management fails.
7. Use a validated VM backup when restoration is the safest path.
8. Keep restored copies isolated until duplicate identity risk is eliminated.
9. Record the failure, recovery steps, and permanent corrective action.

Do not improvise destructive rollback commands without confirming the target and recovery impact.

## Documentation Requirements

For meaningful maintenance:

- Update the affected service, architecture, project, or hardware page.
- Update version information when operationally relevant.
- Update `CHANGELOG.md` or create a dated change record.
- Add or revise a runbook when troubleshooting revealed a reusable process.
- Update ADR follow-up work when a decision was validated or superseded.
- Record backup or restore-test changes.
- Run the Markdown link validator.

## Future Improvements

- Validate this runbook during a planned maintenance window.
- Add measured duration and expected downtime.
- Add package-specific rollback procedures where supported.
- Add a dedicated Proxmox management-access recovery runbook.
- Add automated backup-age and task-result checks.
- Add UPS state checks after Project 005.

## Related Documentation

- [Backup Runbook](backup.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [Disaster Recovery](disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](prometheus-scrape-target-troubleshooting.md)
- [QEMU Guest Agent Troubleshooting](qemu-guest-agent-troubleshooting.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Project 003](../projects/project-003-backup-recovery.md)