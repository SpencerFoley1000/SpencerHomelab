# Infrastructure Change Records

## Purpose

This directory records meaningful infrastructure changes in a concise, reviewable format. Change records complement current-state architecture and service documentation by preserving what changed, why it changed, lessons learned, and remaining work.

These records must remain safe for a public repository. Do not include passwords, tokens, TOTP seeds, provisioning QR codes, recovery keys, private addresses, or identifying network details.

## Records

| Date | Change | Areas affected |
| --- | --- | --- |
| 2026-07-12 | [Proxmox Administrative Authentication Hardening](2026-07-12-proxmox-administrative-authentication-hardening.md) | Proxmox, identity, management-plane security, recovery |

## Related Documentation

- [Repository Changelog](../../CHANGELOG.md)
- [Security Architecture](../architecture/security.md)
- [Proxmox VE Platform](../services/proxmox.md)
