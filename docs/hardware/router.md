# Router / Firewall

## Purpose

The router or firewall defines the routing boundary for the homelab. It controls how lab systems reach upstream networks and, eventually, how internal lab segments communicate with each other.

This page documents the current dependency on existing upstream connectivity and the future direction for dedicated routing and firewalling.

## Current Role

| Area | Details |
| --- | --- |
| Device role | Upstream gateway / future router-firewall platform |
| Current status | Existing dependency / long-term design pending |
| Internet access | Provided through existing home network connectivity |
| Lab routing | Currently simple; future segmentation planned |
| Public documentation | Exact WAN/public details omitted |

## Current State

The homelab currently relies on existing upstream internet connectivity. This keeps the first build simple while the hardware, switch, Proxmox host, and documentation foundation are established.

This is acceptable for the early phase because the lab is not yet hosting public services or complex segmented networks.

## Design Reasoning

Starting with the existing upstream network reduces initial complexity. A dedicated router/firewall should be introduced when there is a clear need, such as:

- VLAN routing.
- Firewall policy enforcement between lab segments.
- Isolated security lab networks.
- Internal DNS and DHCP control.
- Remote access design.
- More realistic network administration practice.

## Future Router / Firewall Responsibilities

A future dedicated router/firewall may provide:

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

## Open Questions

- Which platform will become the long-term router/firewall?
- When should the lab move away from reliance on the existing household network?
- Which VLANs need routing first?
- Which services, if any, will ever be reachable remotely?
- What logging is needed for future security projects?

## Future Improvements

- Select and document the long-term router/firewall platform.
- Add sanitized interface and VLAN layout.
- Document DHCP and DNS responsibilities.
- Add firewall policy philosophy using placeholders.
- Add recovery process for routing failure.
- Add architecture decision record for the routing platform choice.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Switch](switch.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
