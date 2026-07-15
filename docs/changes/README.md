# Infrastructure Change Records

## Purpose

This directory records meaningful infrastructure changes in a concise, reviewable format. Change records complement current-state architecture and service documentation by preserving what changed, why it changed, lessons learned, and remaining work.

These records must remain safe for a public repository. Do not include passwords, tokens, TOTP seeds, provisioning QR codes, recovery keys, private addresses, serial numbers, drive UUIDs, or identifying network details.

## Records

| Date | Change | Areas affected |
| --- | --- | --- |
| 2026-07-14 | [Project 004 Reverse Proxy and Internal HTTPS Completion](2026-07-14-project-004-reverse-proxy-internal-https-completion.md) | DNS, reverse proxy, private PKI, HTTPS, monitoring, backup, restore testing |
| 2026-07-14 | [Project 003 Backup and Recovery Completion](2026-07-14-project-003-backup-recovery-completion.md) | Proxmox, storage, VM backup, retention, restore testing, recovery documentation |
| 2026-07-12 | [Proxmox Administrative Authentication Hardening](2026-07-12-proxmox-administrative-authentication-hardening.md) | Proxmox, identity, management-plane security, recovery |

## Related Documentation

- [Repository Changelog](../../CHANGELOG.md)
- [Architecture Decision Records](../decisions/)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../architecture/security.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Projects](../projects/)
