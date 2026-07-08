# Desktop Workstation

## Purpose

The desktop workstation is the primary administrative and learning endpoint for the homelab. It is used to manage documentation, access infrastructure tools, interact with GitHub, and run local lab tasks when appropriate.

## Current Role

| Area | Details |
| --- | --- |
| Device role | Administrative workstation and general lab endpoint |
| Current status | Active |
| Primary use | Documentation, GitHub, management access, troubleshooting, and learning workflows |
| Future use | Possible local VM testing, security tooling, or cloud/security learning tasks |
| Public documentation | Personal usernames, exact hostnames, and sensitive paths omitted |

## Responsibilities

The desktop workstation may be used for:

- Editing and maintaining the GitHub documentation repository.
- Accessing Proxmox and other internal management interfaces.
- Running SSH, browser-based administration, and troubleshooting tools.
- Creating diagrams, notes, and project documentation.
- Testing client-side access to internal services.
- Supporting future Azure, security, or automation learning workflows.

## Design Reasoning

Keeping a dedicated administrative workstation role helps separate daily lab management from server workloads.

Benefits:

- Easier documentation workflow through VS Code and Git.
- More realistic administration pattern than configuring everything directly on servers.
- Provides a trusted endpoint for managing infrastructure.
- Can support future security and cloud learning without making the Proxmox host a general-purpose desktop.

## Security Considerations

- Treat the workstation as a trusted management device.
- Avoid storing secrets directly in project files.
- Use a password manager for infrastructure credentials.
- Keep GitHub authentication tokens and SSH private keys out of the repository.
- Avoid committing personal usernames, local Windows paths, or screenshots that reveal sensitive details.
- Keep the system patched, especially if it is used to access management interfaces.

## Documentation Boundaries

Do not publish:

- Personal Windows username if not intentionally public.
- Local filesystem paths containing personal names.
- Browser screenshots containing private tabs, account names, or internal IPs.
- SSH private keys.
- GitHub tokens.
- Password manager exports.

Use placeholders:

- `<ADMIN_WORKSTATION>`
- `<LOCAL_USER>`
- `<REPO_PATH>`
- `<SSH_KEY_STORED_PRIVATELY>`

## Maintenance Notes

Future notes may include:

- Required administration tools.
- Git and VS Code setup notes.
- SSH key management approach.
- Backup expectations for local documentation work.
- Security tooling installed for lab use.

## Future Improvements

- Document a sanitized administration toolchain.
- Add a local Git workflow note if needed.
- Add SSH key management guidance.
- Add a workstation hardening checklist.
- Decide whether local VMs should run here or stay on the Proxmox host.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Server](server.md)
- [Security Architecture](../architecture/security.md)
- [Architecture Overview](../architecture/overview.md)
