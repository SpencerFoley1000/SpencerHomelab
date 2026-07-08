# GL.iNet GL-SFT1200 Opal Router

## Purpose

The GL.iNet GL-SFT1200 Opal currently serves as the regular router for the homelab. It provides the routing boundary for lab systems and supports the early network foundation while the environment is still being built.

This page documents the router's current role and the future direction for more advanced routing, firewalling, and segmentation.

## Current Role

| Area | Details |
| --- | --- |
| Device | GL.iNet GL-SFT1200 Opal |
| Device role | Lab router |
| Firmware | Stock firmware |
| Current status | Active |
| Internet access | Provides regular routing for the lab environment |
| Lab routing | Currently simple; future segmentation planned |
| Public documentation | Exact WAN/public details omitted |

## Current State

The GL.iNet GL-SFT1200 Opal is currently used as the lab's regular router. This keeps the first build simple while the hardware, switch, Proxmox host, and documentation foundation are established.

This is acceptable for the early phase because the lab is not yet hosting public services or complex segmented networks.

## Design Decision

The homelab uses the GL.iNet GL-SFT1200 Opal as the initial router because it is simple, compact, and sufficient for the current stage of the lab.

This choice supports the current goals:

- Establish a dedicated lab routing device.
- Keep the early network build understandable.
- Avoid introducing a full firewall platform before VLANs and service requirements are clearly defined.
- Leave room to repurpose or replace the router later if the lab needs more advanced firewalling, routing, or monitoring capabilities.

## Future Router / Firewall Responsibilities

A future dedicated router/firewall platform may eventually provide:

- Inter-VLAN routing.
- DHCP services for lab networks.
- DNS forwarding or internal DNS integration.
- Firewall policies between management, lab, and security networks.
- VPN or remote access if needed.
- Network logging and visibility.

## Public Documentation Boundaries

Do not publish:

- Public WAN IP addresses.
- ISP account details.
- Full firewall exports containing sensitive topology.
- Exact port forwards.
- VPN keys, pre-shared keys, or certificates containing private material.
- Personally identifying network names.

Use placeholders:

- `<ROUTER_IP>`
- `<WAN_IP_REDACTED>`
- `<LAN_SUBNET>`
- `<MGMT_NETWORK>`
- `<LAB_NETWORK>`
- `<VPN_ENDPOINT_REDACTED>`

## Security Considerations

- Do not expose management interfaces to the internet.
- Avoid port forwarding unless there is a documented reason.
- Document firewall rule intent before adding complex rules.
- Keep management access restricted to trusted networks.
- Store administrative credentials in a password manager.
- Treat VPN and remote access credentials as secrets.
- Revisit the router/firewall design before adding isolated security lab workloads.

## Open Questions

- Is the GL.iNet GL-SFT1200 Opal sufficient for the long-term routing role?
- When should the lab move to a more advanced router/firewall platform?
- Which VLANs need routing first?
- Which services, if any, will ever be reachable remotely?
- What logging is needed for future security projects?

## Future Improvements

- Decide whether the Opal remains the long-term lab router or becomes a temporary/secondary device.
- Add sanitized interface and VLAN layout after segmentation is implemented.
- Document DHCP and DNS responsibilities.
- Add firewall policy philosophy using placeholders.
- Add recovery process for routing failure.
- Add architecture decision record for the routing platform choice.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Switch](switch.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
