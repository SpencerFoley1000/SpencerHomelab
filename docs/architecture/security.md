# Security Architecture

## Purpose

This document describes the homelab security model at an architecture level. It focuses on practical controls, recoverable administration, safe public documentation, and a clear boundary between trusted infrastructure and experimental security work.

## Current Status

Security architecture is in the baseline implementation phase.

Current posture:

- Public documentation is sanitized.
- Secrets, raw exports, exact private addressing, and recovery material remain outside Git.
- Management interfaces remain internal-only.
- Proxmox routine administration uses a named application account documented publicly as `<PROXMOX_ADMIN_ACCOUNT>`.
- The Proxmox root identity is retained as a TOTP-protected break-glass account.
- Both Proxmox administrative identities have independent recovery keys.
- System time and NTP were validated before TOTP enrollment.
- Physical console access remains the final hypervisor recovery path.
- Linux host metrics are collected for `pve01`, `dns01`, and `mon01`.
- Project 003A documented sensitive recovery assets without committing them.
- Security-lab isolation is required before attacker-style or intentionally vulnerable systems are used.

## Security Goals

- Apply controls appropriate for a production-style learning homelab.
- Reduce unnecessary root and shared-account use.
- Maintain recoverable administrative access without relying on one password or phone.
- Segment experimental and attacker-style workloads from trusted infrastructure.
- Protect monitoring and backup systems as high-value infrastructure.
- Document security decisions without exposing sensitive implementation details.
- Build habits that translate to professional infrastructure and security roles.

## Public Documentation Boundaries

Do not publish:

- Passwords, tokens, API keys, private keys, SSH keys, or recovery codes.
- TOTP seeds, provisioning QR codes, or authenticator exports.
- Exact routine administrative usernames when a placeholder communicates the design.
- Private keys or certificates containing private material.
- Public IP addresses.
- Personally identifying SSIDs or network names.
- Home address, ISP account information, or personal account identifiers.
- Device serial numbers, asset tags, MAC addresses, or private drive identifiers.
- Raw backup archives, Pi-hole Teleporter files, Grafana exports, or private hashes.
- Exact firewall exports or topology details when sanitized architecture is sufficient.

Use placeholders such as:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PRIVATE_DNS>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<BACKUP_TARGET>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Management Access Model

Management access is limited to trusted administrators and trusted devices.

Management interfaces include:

- Proxmox web interface and SSH.
- Router and switch management interfaces.
- Grafana and Prometheus administration.
- Pi-hole administration.
- Backup storage and future UPS administration.
- Future identity, secrets, or automation systems.

### Proxmox Administrative Identities

| Identity class | Purpose | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine Proxmox application administration | Unique password, TOTP, propagated Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass access and root-only Proxmox operations | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path when network management fails | Physical access to `pve01` |

The routine Proxmox identity is an application-level account. It does not automatically create a Debian user or grant Linux console or SSH access.

Implementation validation included:

- Synchronized system clock.
- Active NTP service.
- Fresh-session password-and-TOTP login for both identities.
- Successful routine host and VM administration through the named account.
- Independent recovery-key sets.

A permission boundary was observed: the named Administrator account received a `403` when attempting to change `root@pam` TOTP. Root authentication-factor changes required a root-authenticated session.

## Administrative-Access Recovery

If the primary authenticator device is lost or replaced:

1. Use an unused recovery key or the protected break-glass path.
2. Confirm accurate system time.
3. Remove the enrollment associated with the lost device.
4. Enroll the replacement authenticator.
5. Replace or regenerate recovery material where required.
6. Validate both routine and break-glass login paths.
7. Record the recovery event without publishing protected values.

Recovery keys should not be consumed merely to prove they exist. Their presence and protected storage should be verified without unnecessary use.

## Network Segmentation Strategy

The current network is intentionally simple and remains largely flat behind the GL.iNet Opal routing boundary.

Planned security boundaries:

| Boundary | Purpose |
| --- | --- |
| Management network | Protect hypervisor, router, switch, monitoring, backup, and UPS administration |
| Lab services network | Host internal DNS, monitoring, proxy, identity, and application services |
| Security lab network | Isolate attacker tools, detection systems, and intentionally vulnerable targets |
| Guest / untrusted network | Restrict lower-trust or temporary devices |
| Household / upstream network | Keep family and general-use devices separate from lab experiments |

Segmentation must be documented, tested, and recoverable before being treated as stable architecture.

Security-lab isolation must exist before offensive tooling or intentionally vulnerable workloads are used.

## Authentication and Secrets

Requirements:

- Use strong unique passwords for infrastructure accounts.
- Prefer named routine-administration identities over root or shared accounts.
- Require multifactor authentication for high-value management interfaces where supported.
- Retain a controlled break-glass path.
- Store secrets and recovery material outside Git.
- Keep recovery material independent from the primary authenticator device.
- Use SSH keys where appropriate, but never commit private keys.
- Record secret locations using placeholders only.
- Rotate credentials after exposure, authenticator loss, compromise, or major trust changes.
- Use least-privilege identities for future Proxmox API monitoring.

## Monitoring and Detection

Current monitoring provides:

- Linux host metrics for `pve01`, `dns01`, and `mon01`.
- Recursive and local DNS service checks.
- Grafana infrastructure and service-health dashboards.

Future security-relevant monitoring should include:

- Repeated authentication failures.
- Unexpected administrative logins.
- Changes to administrative identities or MFA enrollment.
- Management-service exposure changes.
- Backup-job failures and backup age.
- UPS and uncontrolled shutdown events.
- Host resource anomalies.
- Security-lab traffic where appropriate.

Monitoring should be added only when the failure condition, response, notification route, and runbook are defined.

Logs may contain sensitive usernames, addresses, query data, and authentication events and must not be committed.

## Backup Protection

Backups are security-sensitive because they may contain credentials, configuration, authentication state, and service data.

Requirements:

- Restrict write access to backup targets.
- Keep backup storage separate from source storage.
- Encrypt sensitive backups where practical.
- Store recovery keys and credentials outside Git.
- Test restores periodically.
- Keep security-lab systems from modifying trusted backups.
- Do not assume VM backups replace administrative-access recovery.
- Do not assume application-export integrity proves successful restoration.
- Treat the 5 TB external drive as unproven until Project 003 integration and restore testing complete.

## Patch and Maintenance Security

Maintenance should eventually include:

- Patch-review frequency.
- Proxmox and Debian update procedures.
- Pre-change backup checks.
- Rollback or recovery planning.
- Post-update monitoring and authentication validation.
- Firmware review for infrastructure hardware.
- Documentation and changelog updates.

Management interfaces, core infrastructure, and internet-reachable dependencies receive priority.

## Security Lab Boundary

Before running attacker-style workloads, document:

- Network segment.
- Allowed targets.
- Firewall boundaries.
- Monitoring coverage.
- Reset and recovery process.
- Rules preventing impact to household or trusted infrastructure.
- Whether the workload can reach monitoring, backup, management, or identity systems.

## Future Improvements

- Review router and managed-switch authentication, management exposure, and recovery options.
- Document a management-access recovery runbook.
- Review Proxmox SSH authentication and root-login policy after console recovery is documented.
- Evaluate authentication-failure monitoring and rate-limiting without unnecessary hypervisor complexity.
- Restrict management interfaces through a dedicated management network.
- Document management VLAN and firewall philosophy after implementation.
- Add a tested patch-management procedure.
- Complete Project 003 backup and restore validation.
- Add security-lab isolation documentation before offensive tooling is used.
- Create ADRs for the new server role, backup design, UPS design, and future segmentation.

## Related Documentation

- [Security Policy](../../SECURITY.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Monitoring Architecture](monitoring.md)
- [Storage Architecture](storage.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Proxmox Authentication Hardening Change Record](../changes/2026-07-12-proxmox-administrative-authentication-hardening.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
- [Maintenance Runbook](../runbooks/maintenance.md)
