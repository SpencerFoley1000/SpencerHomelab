# Security Architecture

## Purpose

Describe the homelab security model at an architecture level, focusing on practical controls, recoverable administration, protected backups, private PKI, safe public documentation, and separation between trusted infrastructure and experimental security work.

## Current Status

Security architecture is in baseline implementation.

Current posture:

- Public documentation is sanitized.
- Secrets, raw exports, exact private addressing, drive identifiers, certificate private keys, and recovery material remain outside Git.
- Management interfaces are internal-only.
- Proxmox routine administration uses a named account documented as `<PROXMOX_ADMIN_ACCOUNT>`.
- `root@pam` remains a TOTP-protected break-glass identity.
- Both Proxmox identities have independent recovery keys.
- System time and NTP were validated before TOTP enrollment.
- Physical console access remains the final hypervisor recovery path.
- Linux host metrics are collected for `pve01`, `dns01`, `mon01`, and `proxy01`.
- Recursive DNS, local DNS, internal HTTPS, and certificate expiration are monitored from `mon01`.
- A dedicated backup target protects `dns01`, `mon01`, and `proxy01` with daily VM backups.
- Proxmox mount-point enforcement prevents backup fall-through into the host root filesystem.
- Isolated `dns01` and `proxy01` VM restores were completed successfully.
- A private root CA provides internal trust while its encrypted private key remains off `proxy01`.
- Security-lab isolation is required before attacker-style or intentionally vulnerable systems are used.

## Security Goals

- Apply controls appropriate for a production-style learning environment.
- Reduce unnecessary root and shared-account use.
- Maintain recoverable administration without relying on one password or device.
- Segment experimental workloads from trusted infrastructure.
- Protect management, monitoring, DNS, proxy, PKI, and backup systems as high-value assets.
- Document decisions without exposing protected implementation details.
- Build practices relevant to professional infrastructure and security roles.

## Public Documentation Boundaries

Do not publish:

- Passwords, tokens, API keys, private keys, SSH keys, or recovery codes.
- TOTP seeds, QR codes, or authenticator exports.
- Exact routine administrative usernames when a placeholder is sufficient.
- Certificates containing private material.
- Root CA or service private keys.
- Public IP addresses.
- Identifying SSIDs, addresses, ISP records, or account identifiers.
- Device serial numbers, asset tags, MAC addresses, filesystem UUIDs, or private drive identifiers.
- Exact backup filenames, storage volume identifiers, or raw task logs.
- Raw VM backups, Pi-hole Teleporter files, Grafana exports, proxy databases, or private hashes.
- Exact firewall exports or unnecessary topology details.

Use placeholders such as:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<HOST_IP>`
- `<PROXY01_IP>`
- `<PRIVATE_DNS>`
- `<PROXMOX_ADMIN_ACCOUNT>`
- `<PROMETHEUS_DATASOURCE_UID>`
- `<BACKUP_MOUNT>`
- `<BACKUP_TARGET>`
- `<REDACTED_SSID>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`
- `<PRIVATE_PKI_DIRECTORY>`

## Management Access Model

Management access is limited to trusted administrators and trusted devices.

Management surfaces include:

- Proxmox web interface and SSH.
- Router and switch interfaces.
- Grafana and Prometheus.
- Pi-hole administration.
- NGINX Proxy Manager port `81`.
- Backup storage and future UPS management.
- Future identity, secrets, and automation systems.

### Proxmox Administrative Identities

| Identity class | Purpose | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine Proxmox administration | Unique password, TOTP, propagated Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass and root-only operations | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path | Physical access to `pve01` |

The routine identity is application-level and does not automatically grant Debian console or SSH access.

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

## Reverse Proxy Security Boundary

The reverse proxy is an internal convenience and TLS layer, not the only administrative path.

Implemented controls:

- No edge-router port forwarding.
- NGINX Proxy Manager administration remains internal.
- Backend application authentication remains enabled.
- Direct backend access remains available for recovery.
- Proxmox management is intentionally not proxied.
- Proxy host, backend, and monitoring roles remain on separate VMs.
- HTTP redirects to HTTPS for selected friendly names.
- HSTS remains disabled until recovery and compatibility implications are intentionally accepted.
- VM backups are treated as sensitive because they contain the wildcard service private key and proxy database.

## Private PKI Trust Model

The current model uses:

- A private root CA generated on a trusted administrative workstation.
- A 4096-bit encrypted root CA private key.
- A wildcard service certificate for `*.lab.home.arpa` and `lab.home.arpa`.
- Root CA public certificate distribution to trusted clients and `mon01`.
- Only the service certificate and service private key stored on `proxy01`.

The root CA private key:

- Must remain outside Git.
- Must remain off `proxy01`, `mon01`, and security-lab systems.
- Uses a passphrase stored separately.
- Requires a second encrypted or offline copy in a separate failure domain.

The initial CA has no online CRL or OCSP service. Loss and compromise are handled differently:

- Lost but uncompromised key: existing certificates work until expiration, but a replacement CA is required for future issuance.
- Exposed key: replace the CA, all issued certificates, and trusted root installations.

## Network Segmentation Strategy

The current network remains mostly flat behind the GL.iNet Opal boundary.

Planned boundaries:

| Boundary | Purpose |
| --- | --- |
| Management network | Protect hypervisor, network, proxy administration, monitoring, backup, and UPS administration |
| Lab services network | Host DNS, monitoring, proxy traffic, identity, and internal applications |
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
- Store secrets, CA passphrases, and recovery material outside Git.
- Keep recovery material independent from the primary authenticator device.
- Never commit private SSH or certificate keys.
- Rotate credentials and certificates after exposure, loss, compromise, or trust changes.
- Use least-privilege identities for future Proxmox API monitoring.

## Monitoring and Detection

Current visibility:

- Linux host metrics for `pve01`, `dns01`, `mon01`, and `proxy01`.
- Recursive and local DNS probes.
- Internal HTTPS service probes.
- Certificate-expiration metrics.
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
- Certificate-expiration and proxy failures with actionable notification routing.

Monitoring should be added only when a failure condition, response, notification route, and runbook are defined.

## Backup Protection

Backups contain complete system state and must be treated as sensitive.

Implemented controls:

- Dedicated external backup storage separate from the active VM datastore.
- ext4 filesystem and persistent UUID-based mount.
- Proxmox content restriction to backup artifacts.
- Mount-point enforcement so an absent disk fails visibly.
- Daily backups for `dns01`, `mon01`, and `proxy01`.
- Tiered retention: 7 daily, 4 weekly, and 3 monthly.
- Representative isolated `dns01` and `proxy01` restore tests.
- Raw backup artifacts and exact identifiers kept outside Git.
- Security-lab workloads excluded from trusted backup control.

Current limitations:

- The disk is normally connected to the same physical host and location.
- It is not immutable, offline, or off-site.
- `mon01` has not been independently restored.
- Isolated restore tests did not validate live network cutover.
- The root CA private key is outside VM backup coverage and still requires a second protected copy.

## Restore Security

During testing or uncertain failure conditions:

- Restore under a different VM ID.
- Use a clearly temporary name.
- Remove the network adapter before first boot.
- Validate through the Proxmox console.
- Do not connect a duplicate guest until the original cannot return.
- Delete the temporary VM after testing.

During a suspected compromise, treat restored systems, service certificates, and backups as potentially affected until the incident scope is understood.

## Patch and Maintenance Security

Maintenance should include:

- Release-note review.
- Pre-change backup and mount checks.
- Rollback planning.
- Post-update service and monitoring validation.
- Administrative-login and system-time validation.
- Certificate and proxy-route validation where applicable.
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
- Whether the workload can reach management, monitoring, backup, DNS, proxy, PKI, or identity systems.

## Future Improvements

- Create a second encrypted or offline root CA key copy in a separate failure domain.
- Define certificate renewal, rotation, and compromise response ownership.
- Review router and switch authentication, exposure, and recovery.
- Add a tested management-access recovery runbook.
- Review Proxmox SSH and root-login policy after console recovery is documented.
- Evaluate authentication-failure monitoring and rate-limiting.
- Restrict management through a dedicated network.
- Add a tested patch-management procedure.
- Add backup age, failure, and capacity monitoring.
- Add a second backup copy in a separate failure domain.
- Add security-lab isolation before offensive tooling is used.
- Create ADRs for the new-server role, UPS design, and future segmentation.

## Related Documentation

- [Security Policy](../../SECURITY.md)
- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Monitoring Architecture](monitoring.md)
- [Storage Architecture](storage.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [Project 004 Completion Change Record](../changes/2026-07-14-project-004-reverse-proxy-internal-https-completion.md)
- [Backup Runbook](../runbooks/backup.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Maintenance Runbook](../runbooks/maintenance.md)
