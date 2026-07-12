# Security Architecture

## Purpose

This document describes the security model for the homelab at an architecture level. It focuses on practical controls, safe public documentation, and a clear boundary between trusted infrastructure and experimental security work.

## Current Status

Security architecture is in the baseline implementation phase. The immediate priority is to replace unsafe management defaults with recoverable controls while the lab remains simple enough to troubleshoot.

Current security posture:

- Public documentation is sanitized.
- Secrets and recovery material are not stored in the repository.
- Management interfaces remain internal-only.
- Proxmox routine administration uses a named account protected by TOTP.
- The Proxmox root identity is retained as a TOTP-protected break-glass account.
- Both Proxmox administrative identities have separate recovery keys stored outside Git.
- Security lab isolation is planned before attacker-style or intentionally vulnerable systems are used.

## Security Goals

- Apply security best practices appropriate for a learning homelab.
- Segment experimental and attacker-style workloads from trusted infrastructure.
- Document security decisions without exposing sensitive implementation details.
- Build habits that translate to professional infrastructure and security roles.
- Treat backups, monitoring, and management interfaces as high-value systems.
- Maintain recoverable administrative access without relying on a single password or mobile device.

## Public Documentation Boundaries

Do not publish:

- Passwords, tokens, API keys, SSH keys, or recovery codes.
- TOTP seeds, provisioning QR codes, or authenticator exports.
- Private keys or certificates containing private material.
- Public IP addresses.
- Exact firewall exports if they expose sensitive topology.
- Personally identifying SSIDs.
- Home address, ISP account information, or personal account identifiers.
- Device serial numbers or asset tags.
- Sensitive internal topology details that are not needed to explain the design.

Use placeholders such as:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PRIVATE_DNS>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## Management Access Model

Management access should be limited to trusted administrators and trusted devices.

Management interfaces include:

- Proxmox web interface and SSH.
- Switch management interface.
- Router/firewall management interface.
- Monitoring and backup administration panels.
- Any future password manager, secrets manager, or identity tooling.

Current Proxmox access model:

| Identity class | Purpose | Controls |
| --- | --- | --- |
| Named administrator | Routine management and attributable administrative activity | Unique password, TOTP, propagated administrative role, and dedicated recovery keys |
| Root break-glass identity | Emergency recovery and root-only operations | Unique password, TOTP, separate recovery keys, and restricted routine use |
| Physical console | Final recovery path when normal management access fails | Physical access to the host |

The named Proxmox identity is an application-level account and does not automatically create a Debian user or grant Linux console or SSH access.

Future management network design should restrict access to these systems instead of allowing broad access from every lab segment. Router and switch administration should receive comparable authentication and exposure reviews where platform capabilities permit.

## Network Segmentation Strategy

Segmentation should be used to reduce blast radius and support security learning.

Planned security boundaries:

| Boundary | Purpose |
| --- | --- |
| Management network | Protect infrastructure administration interfaces |
| Lab services network | Host internal services without exposing management interfaces |
| Security lab network | Isolate attacker tools and vulnerable systems |
| Household / upstream network | Keep family or general-use devices separate from lab experiments |

Security lab isolation should be implemented before running offensive tooling against intentionally vulnerable systems.

## Authentication and Secrets

General requirements:

- Use strong unique passwords for infrastructure accounts.
- Prefer named routine-administration identities over shared or root accounts.
- Require multifactor authentication for high-value management interfaces where supported.
- Retain a controlled break-glass path for tasks that require elevated or root identity.
- Store secrets and recovery material outside Git.
- Keep recovery material independent from the primary authenticator device.
- Use SSH keys where appropriate, but never commit private keys.
- Document where secrets are stored using placeholders only.
- Rotate credentials after accidental exposure, authenticator loss, or major trust changes.

### Proxmox Authentication Baseline

The implemented Proxmox baseline includes:

- A named `adminops@pve` account for routine administration.
- An Administrator role applied at `/` with propagation for the named account.
- TOTP enabled for both the named account and `root@pam`.
- Separate recovery-key sets for each account.
- Clean password-and-TOTP login validation for both identities.
- System clock synchronization and active NTP validation before TOTP enrollment.
- `root@pam` retained for break-glass use rather than routine administration.

Authentication seeds, QR codes, passwords, and recovery keys are intentionally excluded from the repository.

A permission boundary was observed during implementation: the named administrator received a `403` when attempting to configure TOTP for `root@pam`. Root's authentication factor had to be configured from a root-authenticated session. This behavior reinforces that a broad administrative role does not make every root identity operation delegable.

### Administrative-Access Recovery

If the primary authenticator device is lost or replaced:

1. Use an unused recovery key or the protected break-glass path.
2. Remove the enrollment associated with the lost device.
3. Enroll the replacement authenticator.
4. Replace or regenerate recovery material where required.
5. Validate both routine and break-glass login paths.

Recovery keys should not be consumed merely to demonstrate that they exist. Their presence and storage should be verified without publishing or unnecessarily using them.

## Patch Management

A patch process should eventually document:

- Which systems require manual updates.
- Which systems can update automatically.
- How often updates are reviewed.
- Whether snapshots or backups are taken before major updates.
- How failed updates are rolled back.

Security updates should be prioritized for internet-facing systems, management interfaces, and core infrastructure.

## Logging and Monitoring

Security-relevant monitoring should eventually include:

- Authentication failures.
- Repeated password attempts.
- Unexpected administrative logins.
- Changes to administrative identities or MFA enrollment.
- Service exposure changes.
- Backup failures.
- Host resource anomalies.
- Security lab traffic where appropriate.

Logs may contain sensitive details and should not be committed to the repository.

## Backup Protection

Backups are security-sensitive because they may contain credentials, configuration, or service data.

Guidelines:

- Restrict write access to backup targets.
- Encrypt sensitive backups where practical.
- Store recovery material outside the repository.
- Test restores periodically.
- Keep security lab systems from modifying trusted backups.
- Do not assume VM backups replace independent administrative-access recovery.

## Security Lab Boundary

The long-term goal includes security engineering projects. Those projects should be isolated from stable infrastructure.

Before running attacker-style workloads, document:

- Network segment used.
- Allowed targets.
- Firewall boundaries.
- Reset/recovery process.
- Rules for preventing accidental impact to household or trusted devices.

## Future Improvements

- Review router and managed-switch authentication, management exposure, and recovery options.
- Restrict management interfaces through a dedicated management network after segmentation is implemented.
- Document management VLAN design after implementation.
- Add firewall rule philosophy using sanitized examples.
- Review Proxmox SSH authentication and root-login policy after console recovery is documented.
- Evaluate authentication-failure monitoring and rate-limiting options without introducing unnecessary hypervisor complexity.
- Add a management-access recovery runbook.
- Add patch management runbook.
- Add backup recovery validation runbook.
- Add security lab isolation documentation before offensive tooling is used.
- Add architecture decision records for major security decisions.

## Related Documentation

- [Security Policy](../../SECURITY.md)
- [Network Architecture](network.md)
- [Monitoring Architecture](monitoring.md)
- [Storage Architecture](storage.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
