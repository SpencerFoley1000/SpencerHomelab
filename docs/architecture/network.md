# Network Architecture

## Purpose

This document describes the homelab network design using sanitized values suitable for a public repository. It explains the current baseline, the intended direction, and the assumptions that should guide future network changes.

## Current Status

The network is currently in an early baseline phase:

- A GL.iNet Opal travel router provides the current homelab routing boundary.
- The Opal receives upstream connectivity from the existing household network over Wi-Fi.
- A managed switch provides wired connectivity for lab infrastructure.
- Proxmox hosts the first infrastructure VM, `dns01`.
- Pi-hole on `dns01` provides internal DNS records and DNS-based blocking for configured homelab clients.
- Dedicated VLANs, routing boundaries, and firewall policies are planned but not fully documented as implemented.

Exact IP addresses, SSIDs, public IP addresses, ISP details, and other identifying information must not be published.

## Goals

- Build a network that supports learning, experimentation, and safe service hosting.
- Keep the homelab isolated from the rest of the household network wherever practical.
- Separate management, lab, security testing, and general-use traffic where appropriate.
- Keep the initial design simple enough to troubleshoot while leaving room for segmentation.
- Document architecture and reasoning without exposing unnecessary operational details.
- Create a foundation for future monitoring, DNS, firewall, and security projects.

## Sanitized Addressing Model

Public documentation should use placeholders instead of exact values.

| Placeholder | Meaning |
| --- | --- |
| `<HOMELAB_LAN>` | Current private network behind the GL.iNet Opal router |
| `<UPSTREAM_NETWORK>` | Existing household network used only for internet connectivity |
| `<MGMT_NETWORK>` | Future management network for infrastructure access |
| `<LAB_NETWORK>` | Future lab workload network |
| `<SECURITY_LAB_NETWORK>` | Future isolated network for security testing |
| `<ROUTER_IP>` | Homelab router or default gateway address |
| `<SWITCH_MGMT_IP>` | Managed switch administrative address |
| `<PROXMOX_HOST_IP>` | Proxmox host management address |
| `<DNS01_IP>` | Pi-hole DNS server address |
| `<REDACTED_SSID>` | Sanitized wireless network name |

## Current Logical Design

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal travel router
  |
Managed switch
  |
Proxmox host
  |
dns01 - Pi-hole DNS
```

The household network is an upstream dependency, not part of the managed homelab environment. This design allows the lab to experiment with DNS, DHCP, routing, and future segmentation without impacting other household users.

## Current DNS Design

Pi-hole is deployed as the current internal DNS service for the homelab.

| Area | Current Design |
| --- | --- |
| DNS server | `dns01` running Pi-hole |
| Internal DNS zone | `lab` |
| Upstream resolver | Cloudflare DNS selected during initial deployment |
| Current client rollout | Manual client DNS configuration |
| Future client rollout | DHCP option from the homelab router |

Local DNS records are used for infrastructure names such as:

- `dns01.lab`
- `pve01.lab`
- `switch01.lab`

These names are intentionally generic and suitable for public documentation. Avoid committing hostnames that expose personal information.

## DHCP Strategy

The GL.iNet Opal currently provides the homelab routing boundary. DHCP responsibilities should remain simple until the network is more mature.

Current approach:

- Keep DHCP on the homelab router.
- Configure only selected clients to use Pi-hole while stability is validated.
- Avoid pushing Pi-hole network-wide until recovery steps and fallback DNS behavior are understood.

Future approach:

- Configure the homelab router to hand out `<DNS01_IP>` as the DNS server for homelab clients.
- Add a secondary DNS server before depending on Pi-hole for every device.
- Document DHCP scope, reservations, and DNS options using placeholders.

## Future Segmentation Plan

Planned network segments may include:

| Segment | Purpose | Notes |
| --- | --- | --- |
| Management | Hypervisor, switch, router, and administrative interfaces | Restrict access to trusted admin devices |
| Lab Services | Internal services such as DNS, monitoring, dashboards, and documentation tooling | Should be reachable only where needed |
| Security Lab | Attacker/defender testing, intentionally vulnerable systems, and cyber engineering projects | Should be isolated from household devices and stable infrastructure |
| Guest / Untrusted | Temporary or low-trust devices | Optional future segment |

Segmentation should be implemented only when it is understood well enough to troubleshoot. VLANs and firewall rules should be documented before they are treated as stable.

## Security Considerations

- Do not expose management interfaces directly to the internet.
- Treat the household network as upstream only, not as managed lab infrastructure.
- Restrict administrative access to trusted devices and networks.
- Keep switch, router, hypervisor, and service credentials in a password manager.
- Avoid reusing household Wi-Fi names, personal usernames, or exact addresses in public documentation.
- Isolate security testing networks before running offensive or intentionally vulnerable workloads.
- Treat DNS query logs as sensitive operational data because they can reveal browsing behavior.

## Open Questions

- Is the GL.iNet Opal sufficient as the medium-term homelab edge router?
- When should Pi-hole become the DHCP-provided DNS server for all homelab clients?
- Should a secondary DNS server be deployed before Pi-hole is made network-wide?
- Which VLANs are required for the first stable segmentation milestone?
- Which services require internal-only DNS records?
- What firewall rules are required for security lab isolation?

## Future Improvements

- Add a sanitized logical network diagram.
- Document VLAN IDs after they are intentionally assigned.
- Document firewall rule philosophy and examples using placeholders.
- Document DHCP scopes and DNS options in sanitized form.
- Add troubleshooting steps for switch, DHCP, DNS, and gateway issues.
- Add secondary DNS for resilience.
- Add monitoring for DNS availability and query health.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Security Architecture](security.md)
- [Pi-hole Service](../services/pihole.md)
- [Router Documentation](../hardware/router.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
