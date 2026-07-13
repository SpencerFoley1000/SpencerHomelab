# Proxmox Administrative Authentication Hardening

## Date

2026-07-12

## Status

Implemented and validated.

## Scope

This change hardened access to the Proxmox management plane without introducing new network segmentation or broad firewall-policy changes.

Affected areas:

- Proxmox administrative identities.
- Multifactor authentication.
- Emergency access and recovery.
- Public security and service documentation.

## Changed

- Created a named Proxmox application account, documented publicly as `<PROXMOX_ADMIN_ACCOUNT>`, for routine administration.
- Granted the named account the Administrator role at `/` with propagation.
- Enabled TOTP for both the named account and the `root@pam` break-glass account.
- Generated separate recovery-key sets for both administrative identities.
- Verified synchronized system time and active NTP before relying on TOTP.
- Completed clean password-and-TOTP login tests for both accounts from fresh browser sessions.
- Designated the named account for routine administration and retained `root@pam` for break-glass and root-only operations.
- Updated Proxmox service, security architecture, and repository overview documentation.

The actual routine account name, passwords, TOTP seeds, provisioning QR codes, recovery keys, and exact management endpoints remain outside the repository.

## Why

- The hypervisor management plane is a high-value target because compromise would affect every hosted workload.
- A named routine account improves administrative accountability and reduces unnecessary use of the root identity.
- TOTP reduces the risk posed by password guessing, credential reuse, or disclosure of a password alone.
- Independent recovery keys prevent loss of the authenticator device from becoming permanent administrative lockout.
- Sanitizing the exact routine account name removes unnecessary public attack-surface information without weakening the portfolio value of the design.
- The current flat homelab network makes authentication hardening a safer immediate control than introducing untested segmentation or restrictive firewall policy.

## Validation

- `timedatectl status` reported `System clock synchronized: yes`.
- `timedatectl status` reported `NTP service: active`.
- `<PROXMOX_ADMIN_ACCOUNT>` completed a clean password-and-TOTP login.
- `root@pam` completed a clean password-and-TOTP login.
- The named administrator could access the host and active virtual machines through its assigned role.
- Both identities have separate recovery-key sets.

Recovery keys were not consumed during routine validation.

## Lessons Learned

- A Proxmox application account does not automatically create a matching Debian user or grant Linux console or SSH access.
- TOTP depends on accurate system time, so NTP synchronization should be verified before enrollment.
- The named Administrator account received a `403` when attempting to modify `root@pam` TOTP; root authentication changes required a root-authenticated session.
- A broad application role does not necessarily delegate protected identity-management actions for the root account.
- Multifactor authentication is incomplete without a recovery design independent of the enrolled phone.
- Keeping an existing authenticated root session open during enrollment reduced lockout risk.
- Public documentation can explain the identity model without exposing the exact routine login name.

## Operational Model

| Identity | Use | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine Proxmox administration | Unique password, TOTP, Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass access and root-only actions | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path | Physical access to `pve01` |

## Remaining Work

- Review router and managed-switch authentication, management exposure, and recovery options.
- Document a management-access recovery runbook.
- Review Proxmox SSH authentication and root-login policy after physical-console recovery is documented.
- Evaluate authentication-failure monitoring and rate-limiting options without adding unnecessary hypervisor complexity.
- Restrict management interfaces through a dedicated management network when segmentation is implemented.

## Related Documentation

- [Change Records Index](README.md)
- [Proxmox VE Platform](../services/proxmox.md)
- [Security Architecture](../architecture/security.md)
- [Network Architecture](../architecture/network.md)
- [Repository README](../../README.md)
