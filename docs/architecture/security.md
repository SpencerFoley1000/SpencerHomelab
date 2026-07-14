# Security Architecture

## Purpose

Describe the homelab security model at an architecture level, focusing on practical controls, recoverable administration, protected backups, safe public documentation, and separation between trusted infrastructure and experimental security work.

## Current Status

Security architecture is in baseline implementation.

Current posture:

- Public documentation is sanitized.
- Secrets, raw exports, exact private addressing, drive identifiers, and recovery material remain outside Git.
- Management interfaces are internal-only.
- Proxmox routine administration uses a named account documented as `<PROXMOX_ADMIN_ACCOUNT>`.
- `root@pam` remains a TOTP-protected break-glass identity.
- Both Proxmox identities have independent recovery keys.
- System time and NTP were validated before TOTP enrollment.
- Physical console access remains the final hypervisor recovery path.
- Linux host metrics are collected for `pve01`, `dns01`, and `mon01`.
- A dedicated backup target protects `dns01` and `mon01` with daily VM backups.
- Proxmox mount-point enforcement prevents backup fall-through into the host root filesystem.
- An isolated `dns01` VM restore was completed successfully.
- Security-lab isolation is required before attacker-style or intentionally vulnerable systems are used.

## Security Goals

- Apply controls appropriate for a production-style learning environment.
- Reduce unnecessary root and shared-account use.
- Maintain recoverable administration without relying on one password or device.
- Segment experimental workloads from trusted infrastructure.
- Protect management, monitoring, DNS, and backup systems as high-value assets.
- Document decisions without exposing protected implementation details.
- Build practices relevant to professional infrastructure and security roles.

## Public Documentation Boundaries

Do not publish:

- Passwords, tokens, API keys, private keys, SSH keys, or recovery codes.
- TOTP seeds, QR codes, or authenticator exports.
- Exact routine administrative usernames when a placeholder is sufficient.
- Certificates containing private material.
- Public IP addresses.
- Identifying SSIDs, addresses, ISP records, or account identifiers.
- Device serial numbers, asset tags, MAC addresses, filesystem UUIDs, or private drive identifiers.
- Exact backup filenames, storage volume identifiers, or raw task logs.
- Raw VM backups, Pi-hole Teleporter files, Grafana exports, or private hashes.
- Exact firewall exports or unnecessary topology details.

Use placeholders such as:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PRIVATE_DNS>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<BACKUP_MOUNT>`
- `<BACKUP_TARGET>`
- `<BACKUP_VOLUME_ID>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Management Access Model

Management access is limited to trusted administrators and trusted devices.

Management surfaces include:

- Proxmox web interface and SSH.
- Router and switch interfaces.
- Grafana and Prometheus.
- Pi-hole administration.
- Backup storage and future UPS management.
- Future identity, secrets, proxy, and automation systems.

### Proxmox Administrative Identities

| Identity class | Purpose | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine Proxmox administration | Unique password, TOTP, propagated Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass and root-only operations | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path | Physical access to `pve01` |

The routine identity is application-level and does not automatically grant Debian console or SSH access.

Validated controls:

- Synchronized system clock.
- Active NTP service.
- Fresh-session password-and-TOTP login for both identities.
- Routine host and VM administration through the named account.
- Independent recovery-key sets.

A permission boundary was observed: the named Administrator account could not modify `root@pam` TOTP. Root authentication-factor changes required a root-authenticated session.

## Administrative-Access Recovery

If the primary authenticator is lost or replaced:

1. Use an unused recovery key or protected break-glass path.
2. Confirm accurate system time.
3. Remove the lost-device enrollment.
4. Enroll the replacement authenticator.
5. Replace affected recovery material.
6. Validate both routine and break-glass login paths.
7. Document the event without protected values.

Recovery keys should not be consumed merely to prove they exist.

## Network Segmentation Strategy

The current network remains mostly flat behind the GL.iNet Opal boundary.

Planned boundaries:

| Boundary | Purpose |
| --- | --- |
| Management network | Protect hypervisor, network, monitoring, backup, and UPS administration |
| Lab services network | Host DNS, monitoring, proxy, identity, and internal applications |
| Security lab network | Isolate attacker tools, detection systems, and vulnerable targets |
| Guest or untrusted network | Restrict lower-trust and temporary devices |
| Household or upstream network | Separate family and general-use devices from lab experiments |

Segmentation must be documented, tested, and recoverable before being treated as stable architecture.

## Authentication and Secrets

Requirements:

- Use strong unique passwords.
- Prefer named routine identities over root or shared accounts.
- Require MFA for high-value management where supported.
- Retain a controlled break-glass path.
- Store secrets and recovery material outside Git.
- Keep recovery material independent from the primary authenticator device.
- Never commit private SSH keys.
- Rotate credentials after exposure, loss, compromise, or trust changes.
- Use least-privilege identities for future Proxmox API monitoring.

## Monitoring and Detection

Current visibility:

- Linux host metrics for `pve01`, `dns01`, and `mon01`.
- Recursive and local DNS probes.
- Grafana infrastructure and service dashboards.

Future security-relevant monitoring:

- Repeated authentication failures.
- Unexpected administrative logins.
- Administrative identity or MFA changes.
- Management-service exposure changes.
- Backup job failure, age, and capacity.
- UPS and uncontrolled shutdown events.
- Host resource anomalies.
- Security-lab traffic where appropriate.
- Reverse-proxy and certificate events after Project 004.

Monitoring should be added only when a failure condition, response, notification route, and runbook are defined.

## Backup Protection

Backups contain complete system state and must be treated as sensitive.

Implemented controls:

- Dedicated external backup storage separate from the active VM datastore.
- ext4 filesystem and persistent UUID-based mount.
- Proxmox content restriction to backup artifacts.
- Mount-point enforcement so an absent disk fails visibly.
- Daily backups for `dns01` and `mon01`.
- Tiered retention: 7 daily, 4 weekly, and 3 monthly.
- A representative isolated `dns01` restore test.
- Raw backup artifacts and exact identifiers kept outside Git.
- Security-lab workloads excluded from trusted backup control.

Current limitations:

- The disk is normally connected to the same physical host and location.
- It is not immutable, offline, or off-site.
- `mon01` has not been independently restored.
- The isolated `dns01` test did not validate network-facing behavior.

Future stronger protection may include offline rotation, off-site storage, a NAS, or Proxmox Backup Server.

## Restore Security

During testing or uncertain failure conditions:

- Restore under a different VM ID.
- Use a clearly temporary name.
- Remove the network adapter before first boot.
- Validate through the Proxmox console.
- Do not connect a duplicate guest until the original cannot return.
- Delete the temporary VM after testing.

During a suspected compromise, treat restored systems and backups as potentially affected until the incident scope is understood.

## Patch and Maintenance Security

Maintenance should include:

- Release-note review.
- Pre-change backup and mount checks.
- Rollback planning.
- Post-update service and monitoring validation.
- Administrative-login and system-time validation.
- Firmware review where relevant.
- Documentation and changelog updates.

Management interfaces and core infrastructure receive priority.

## Security Lab Boundary

Before running attacker-style workloads, document:

- Network segment.
- Allowed targets.
- Firewall boundaries.
- Monitoring coverage.
- Reset and recovery process.
- Rules preventing impact to household or trusted infrastructure.
- Whether the workload can reach management, monitoring, backup, DNS, proxy, or identity systems.

## Future Improvements

- Review router and switch authentication, exposure, and recovery.
- Add a tested management-access recovery runbook.
- Review Proxmox SSH and root-login policy after console recovery is documented.
- Evaluate authentication-failure monitoring and rate-limiting.
- Restrict management through a dedicated network.
- Add a tested patch-management procedure.
- Add backup age, failure, and capacity monitoring.
- Add a second backup copy in a separate failure domain.
- Document Project 004 reverse-proxy trust and certificate controls.
- Add security-lab isolation before offensive tooling is used.
- Create ADRs for the new-server role, UPS design, and future segmentation.

## Related Documentation

- [Security Policy](../../SECURITY.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Monitoring Architecture](monitoring.md)
- [Storage Architecture](storage.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [ADR-0003](../decisions/ADR-0003-direct-attached-proxmox-backup-storage.md)
- [Authentication Hardening Change Record](../changes/2026-07-12-proxmox-administrative-authentication-hardening.md)
- [Project 003 Completion Change Record](../changes/2026-07-14-project-003-backup-recovery-completion.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Maintenance Runbook](../runbooks/maintenance.md)