# Maintenance Runbook

## Purpose

Provide a repeatable baseline for routine maintenance while protecting service availability, administrative access, monitoring, and recovery options.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Draft baseline |
| Validation | Not yet exercised as a complete environment-specific maintenance window |
| Backup dependency | Project 003 VM backups and restore validation pending |
| Last reviewed | 2026-07-12 |

This runbook should be expanded with tested timing, exact validation checks, and rollback details after the next planned Proxmox or core-service maintenance window.

## Maintenance Areas

- Debian guest updates.
- Proxmox host updates.
- Pi-hole updates.
- Prometheus, Grafana, and exporter updates.
- Firmware review.
- Backup and restore validation.
- Authentication and recovery-path review.
- Monitoring and log review.
- Documentation consistency review.
- Hardware and capacity review.

## Preconditions

Before maintenance:

- Confirm the planned scope and affected systems.
- Review vendor or package release notes.
- Confirm no active incident is already in progress.
- Confirm current service health in Prometheus and Grafana.
- Confirm recent protected backups exist when the backup platform is operational.
- Confirm required application exports are current for meaningful service changes.
- Confirm Proxmox routine and break-glass access paths.
- Confirm physical-console access for hypervisor work.
- Record a rollback path for configuration changes.
- Keep secrets and raw outputs outside the repository.

## Procedure

1. Record the maintenance objective and affected systems.
2. Capture current versions and relevant health state.
3. Create protected configuration rollback copies where appropriate.
4. Confirm backup or recovery assets for the affected workload.
5. Apply one logical change at a time.
6. Validate configuration syntax before service reload or restart.
7. Prefer reload over restart when supported and appropriate.
8. Reboot only when required by the update or validation plan.
9. Validate services from the source layer outward.
10. Review logs for new errors.
11. Remove temporary rollback files only after a protected known-good copy exists.
12. Update documentation and the changelog for meaningful changes.

## Validation Order

### Network and Management

- Router and switch connectivity remain available.
- Proxmox management is reachable from a trusted system.
- System time remains synchronized.
- The named routine Proxmox administrator can authenticate.
- The protected break-glass path remains documented and available.

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

### `dns01`

```bash
systemctl is-active pihole-FTL prometheus-node-exporter
systemctl is-enabled pihole-FTL prometheus-node-exporter
pihole status
```

Prometheus:

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

Confirm:

- `prometheus`
- `node_exporter`
- `blackbox_dns`
- `blackbox_dns_local`

Grafana:

- All three hosts display current data.
- Recursive and Local DNS show current state.
- Dashboard timestamps advance normally.

## Rollback

If maintenance causes a failure:

1. Stop making additional changes.
2. Identify whether the failure is configuration, package, network, authentication, or reboot related.
3. Restore the known-good configuration copy when applicable.
4. Revalidate syntax before restarting the affected service.
5. Revert the package or configuration only when a safe method is documented.
6. Use the protected Proxmox break-glass or physical-console path if routine access fails.
7. Restore a validated VM backup when available and appropriate.
8. Record the failure, recovery steps, and permanent corrective action.

Do not improvise destructive rollback commands without confirming the target and recovery impact.

## Documentation Requirements

For meaningful maintenance:

- Update the affected service or hardware page.
- Update version information when operationally relevant.
- Update `CHANGELOG.md`.
- Add or revise a runbook when troubleshooting revealed a reusable process.
- Update ADR follow-up work if a decision was validated or superseded.
- Run the Markdown link validator.

## Future Improvements

- Validate this runbook during a planned maintenance window.
- Add measured maintenance duration and expected downtime.
- Add package-specific rollback procedures where supported.
- Add a dedicated Proxmox maintenance and management-access recovery runbook.
- Integrate backup-age and backup-job checks after Project 003.
- Add UPS state checks after Project 005.

## Related Documentation

- [Backup Runbook](backup.md)
- [Disaster Recovery Runbook](disaster-recovery.md)
- [Prometheus Scrape Target Troubleshooting](prometheus-scrape-target-troubleshooting.md)
- [QEMU Guest Agent Troubleshooting](qemu-guest-agent-troubleshooting.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
