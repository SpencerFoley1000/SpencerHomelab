# GL.iNet GL-SFT1200 Opal Router

## Purpose

The GL.iNet GL-SFT1200 Opal currently serves as the homelab edge router. It provides the routing boundary for lab systems and supports the early network foundation while the environment is still being built.

This page documents the router's current role and the future direction for more advanced routing, firewalling, DNS, DHCP, and segmentation.

## Current Role

| Area | Details |
| --- | --- |
| Device | GL.iNet GL-SFT1200 Opal |
| Device role | Homelab edge router |
| Firmware | Stock firmware |
| Current status | Active |
| Upstream connectivity | Existing household network over Wi-Fi |
| Downstream connectivity | Homelab LAN and managed switch |
| Lab routing | Currently simple; future segmentation planned |
| Public documentation | Exact WAN, SSID, and addressing details omitted |

## Current State

The GL.iNet GL-SFT1200 Opal is currently used as the lab's edge router. It receives upstream connectivity from the existing household network and provides a separate homelab environment behind it.

This is acceptable for the early phase because:

- The lab can be built without requiring an Ethernet run to the upstream router.
- DNS and DHCP experiments can be isolated from the rest of the household network.
- Mistakes in the homelab are less likely to affect non-lab users.
- The network remains simple enough to troubleshoot while core services are being deployed.

## Design Decision

The homelab uses the GL.iNet GL-SFT1200 Opal as the initial router because it is simple, compact, and sufficient for the current stage of the lab.

This choice supports the current goals:

- Establish a dedicated lab routing boundary.
- Keep the early network build understandable.
- Avoid introducing a full firewall platform before VLANs and service requirements are clearly defined.
- Allow the lab to operate using upstream Wi-Fi where wired upstream connectivity is not feasible.
- Leave room to repurpose or replace the router later if the lab needs more advanced firewalling, routing, or monitoring capabilities.

## DNS and DHCP Responsibilities

Current state:

- The Opal provides the homelab routing boundary.
- Pi-hole on `dns01` provides internal DNS for manually configured clients.
- DHCP remains simple while Pi-hole stability is validated.

Future state:

- Configure the Opal DHCP service to hand out Pi-hole as the DNS server for homelab clients.
- Add a secondary DNS server before making DNS fully dependent on a single VM.
- Document DHCP scopes, reservations, and DNS options using sanitized placeholders.

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
- Household SSIDs or personally identifying network names.
- Full firewall exports containing sensitive topology.
- Exact port forwards.
- VPN keys, pre-shared keys, or certificates containing private material.
- Personally identifying network names.

Use placeholders:

- `<ROUTER_IP>`
- `<WAN_IP_REDACTED>`
- `<HOMELAB_LAN>`
- `<UPSTREAM_NETWORK>`
- `<MGMT_NETWORK>`
- `<LAB_NETWORK>`
- `<DNS01_IP>`
- `<VPN_ENDPOINT_REDACTED>`

## Security Considerations

- Do not expose management interfaces to the internet.
- Avoid port forwarding unless there is a documented reason.
- Document firewall rule intent before adding complex rules.
- Keep management access restricted to trusted networks.
- Store administrative credentials in a password manager.
- Treat VPN and remote access credentials as secrets.
- Revisit the router/firewall design before adding isolated security lab workloads.
- Treat the household network as upstream only, not as a managed or trusted security boundary for lab design.

## Open Questions

- Is the GL.iNet GL-SFT1200 Opal sufficient for the medium-term routing role?
- When should the lab move to a more advanced router/firewall platform?
- When should DHCP be updated to hand out Pi-hole as the default DNS server?
- Should a secondary DNS server be deployed before router-wide DNS changes are made?
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
- [Pi-hole Service](../services/pihole.md)
- [Security Architecture](../architecture/security.md)
