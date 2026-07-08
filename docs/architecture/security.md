# Security Architecture

## Purpose

This document describes the security model for the homelab at an architecture level. It focuses on practical controls, safe public documentation, and a clear boundary between trusted infrastructure and experimental security work.

## Current Status

Security architecture is in the baseline planning phase. The immediate priority is to avoid unsafe defaults while the lab is still being built.

Current security posture:

- Public documentation is sanitized.
- Secrets are not stored in the repository.
- Management interfaces should remain internal-only.
- Security lab isolation is planned before attacker-style or intentionally vulnerable systems are used.

## Security Goals

- Apply security best practices appropriate for a learning homelab.
- Segment experimental and attacker-style workloads from trusted infrastructure.
- Document security decisions without exposing sensitive implementation details.
- Build habits that translate to professional infrastructure and security roles.
- Treat backups, monitoring, and management interfaces as high-value systems.

## Public Documentation Boundaries

Do not publish:

- Passwords, tokens, API keys, SSH keys, or recovery codes.
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

Future management network design should restrict access to these systems instead of allowing broad access from every lab segment.

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

- Use strong unique passwords for infrastructure accounts.
- Store secrets in a password manager, not in GitHub.
- Use SSH keys where appropriate, but never commit private keys.
- Document where secrets are stored using placeholders only.
- Rotate credentials after accidental exposure or major trust changes.

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
- Unexpected administrative logins.
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

## Security Lab Boundary

The long-term goal includes security engineering projects. Those projects should be isolated from stable infrastructure.

Before running attacker-style workloads, document:

- Network segment used.
- Allowed targets.
- Firewall boundaries.
- Reset/recovery process.
- Rules for preventing accidental impact to household or trusted devices.

## Future Improvements

- Document management VLAN design after implementation.
- Add firewall rule philosophy using sanitized examples.
- Add patch management runbook.
- Add backup recovery validation runbook.
- Add security lab isolation documentation before offensive tooling is used.
- Add architecture decision records for major security decisions.

## Related Documentation

- [Security Policy](../../SECURITY.md)
- [Network Architecture](network.md)
- [Monitoring Architecture](monitoring.md)
- [Storage Architecture](storage.md)
- [Disaster Recovery Runbook](../runbooks/disaster-recovery.md)
