# Network Architecture

This page documents the homelab network design using sanitized values suitable for a public repository.

## Current Status

Status: Planned / baseline documentation pending.

## Goals

- Build a network that supports learning, experimentation, and safe service hosting.
- Separate trusted, management, lab, and guest-style traffic where appropriate.
- Keep sensitive network details out of public documentation.
- Document enough architecture for future troubleshooting without exposing unnecessary attack surface.

## Sanitization Rules

Do not publish:

- Exact personally identifying SSIDs.
- Public WAN IP addresses.
- ISP account details.
- Complete internal addressing details unless generalized.

Use placeholders such as:

- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<LAB_NETWORK>`
- `<REDACTED_SSID>`
- `<ROUTER_IP>`

## Planned Sections

- Physical topology
- VLAN / subnet strategy
- Routing boundaries
- DNS strategy
- DHCP strategy
- Firewall rules
- Remote access approach
- Security considerations

## Open Questions

- Which device will act as the primary router/firewall long term?
- When should the lab stop relying on the existing household network?
- Which services need internal-only DNS records?
- What segmentation is needed for security lab work?
