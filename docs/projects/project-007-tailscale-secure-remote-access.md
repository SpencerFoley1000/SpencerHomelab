# Project 007: Tailscale Secure Remote Access

## Status

Planned

## Purpose

Provide authenticated remote access to selected homelab monitoring and management services without exposing administrative interfaces directly to the public internet.

## Goals

- Enroll only approved administrative endpoints and homelab systems.
- Reach Grafana and selected management interfaces while away from the local network.
- Use explicit, least-privilege access policy instead of granting unrestricted tailnet connectivity.
- Preserve local access and recovery paths if Tailscale or its control plane is unavailable.
- Produce repeatable deployment, validation, maintenance, and revocation documentation.

## Planned Scope

- Select the minimum systems that require Tailscale connectivity.
- Define the administrator and device enrollment model.
- Configure access controls for approved users, devices, and services.
- Decide whether direct node access, subnet routing, or a combination is justified by the final requirements.
- Validate connectivity from an external network.
- Confirm that unapproved services and paths remain inaccessible.
- Document updates, key expiration, device removal, access revocation, troubleshooting, and recovery.
- Add monitoring for the remote-access path only where it produces an actionable operational signal.

## Security Considerations

- Do not expose Proxmox, Grafana, Pi-hole, SSH, or other management interfaces through public router port forwarding.
- Treat tailnet membership as privileged access and remove unused devices promptly.
- Require strong identity-provider authentication and multifactor authentication where supported.
- Grant access by service and role rather than treating the tailnet as a fully trusted flat network.
- Keep secrets, reusable authentication material, device identifiers, and private network details out of this public repository.

## Dependencies

- Project 006 UPS monitoring and graceful shutdown completed and validated.
- Existing local management access remains functional.
- Recovery access is documented before remote access becomes operationally important.

## Completion Criteria

- Approved remote endpoint can reach each explicitly authorized service from outside the local network.
- Unauthorized service paths are tested and remain blocked.
- No management port is forwarded publicly for this implementation.
- Device enrollment, removal, key lifecycle, update, troubleshooting, and recovery procedures are documented.
- Architecture, service, runbook, change, and roadmap documentation reflects the deployed design.

## Follow-Up

- Reassess access policy after Project 008 introduces centralized identity.
- Evaluate whether future network segmentation requires narrower routes or additional policy boundaries.
