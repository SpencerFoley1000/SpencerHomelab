# Administrative Workstation

## Purpose

The administrative workstation is the personal endpoint used to manage the homelab. It is used to maintain documentation, access infrastructure tools, interact with GitHub, and perform management tasks.

This system is intentionally documented by role rather than hardware specifications because it is not core lab infrastructure.

## Current Role

| Area | Details |
| --- | --- |
| Device role | Administrative workstation and general lab endpoint |
| Current status | Active |
| Primary use | Documentation, GitHub, management access, troubleshooting, and learning workflows |
| Future use | Possible security tooling, cloud tooling, or client-side testing |
| Public documentation | Personal usernames, exact hostnames, local paths, and hardware specs omitted |

## Responsibilities

The administrative workstation may be used for:

- Editing and maintaining the GitHub documentation repository.
- Accessing Proxmox and other internal management interfaces.
- Running SSH, browser-based administration, and troubleshooting tools.
- Creating diagrams, notes, and project documentation.
- Testing client-side access to internal services.
- Supporting future Azure, security, or automation learning workflows.

## Design Decision

The workstation is documented as an administrative endpoint instead of a lab infrastructure device.

This avoids unnecessary personal hardware detail in the public repository while still documenting the operational role the workstation plays in managing the environment.

Benefits:

- Keeps the repository focused on infrastructure.
- Avoids publishing personal workstation specifications that do not materially affect the lab design.
- Reduces maintenance when the personal workstation changes.
- Still documents the management path used to operate the homelab.

## Security Considerations

- Treat the workstation as a trusted management device.
- Avoid storing secrets directly in project files.
- Use a password manager for infrastructure credentials.
- Keep GitHub authentication tokens and SSH private keys out of the repository.
- Avoid committing personal usernames, local paths, or screenshots that reveal sensitive details.
- Keep the system patched, especially if it is used to access management interfaces.

## Documentation Boundaries

Do not publish:

- Personal operating system username if not intentionally public.
- Local filesystem paths containing personal names.
- Browser screenshots containing private tabs, account names, or internal IPs.
- SSH private keys.
- GitHub tokens.
- Password manager exports.
- Personal hardware specifications unless they become relevant to the lab design.

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
