# Network Architecture

## Purpose

This document describes the homelab network design using sanitized values suitable for a public repository. It explains the current baseline, the intended direction, and the assumptions that should guide future network changes.

## Current Status

The network is currently in an early baseline phase:

- A managed switch is available for lab connectivity.
- The switch has been placed on the existing private IP range.
- The lab currently depends on existing home internet connectivity.
- Dedicated VLANs, routing boundaries, and firewall policies are planned but not fully documented as implemented.

Exact IP addresses, SSIDs, public IP addresses, ISP details, and other identifying information must not be published.

## Goals

- Build a network that supports learning, experimentation, and safe service hosting.
- Separate management, lab, security testing, and general-use traffic where appropriate.
- Keep the initial design simple enough to troubleshoot while leaving room for segmentation.
- Document architecture and reasoning without exposing unnecessary operational details.
- Create a foundation for future monitoring, DNS, firewall, and security projects.

## Sanitized Addressing Model

Public documentation should use placeholders instead of exact values.

| Placeholder | Meaning |
| --- | --- |
| `<LAN_SUBNET>` | Existing general-purpose private network |
| `<MGMT_NETWORK>` | Future management network for infrastructure access |
| `<LAB_NETWORK>` | Future lab workload network |
| `<SECURITY_LAB_NETWORK>` | Future isolated network for security testing |
| `<ROUTER_IP>` | Router or default gateway address |
| `<SWITCH_MGMT_IP>` | Managed switch administrative address |
| `<PROXMOX_HOST_IP>` | Proxmox host management address |
| `<REDACTED_SSID>` | Sanitized wireless network name |

## Current Logical Design

```text
Internet
  |
Existing upstream router / household network
  |
Managed switch
  |
Proxmox host and lab devices
```

This design is intentionally simple for the initial build. It allows the hardware and virtualization foundation to come online before adding routing complexity.

## Future Segmentation Plan

Planned network segments may include:

| Segment | Purpose | Notes |
| --- | --- | --- |
| Management | Hypervisor, switch, router, and administrative interfaces | Restrict access to trusted admin devices |
| Lab Services | Internal services such as DNS, monitoring, dashboards, and documentation tooling | Should be reachable only where needed |
| Security Lab | Attacker/defender testing, intentionally vulnerable systems, and cyber engineering projects | Should be isolated from household devices |
| Guest / Untrusted | Temporary or low-trust devices | Optional future segment |

Segmentation should be implemented only when it is understood well enough to troubleshoot. VLANs and firewall rules should be documented before they are treated as stable.

## DNS and DHCP Strategy

Current DNS and DHCP details are still being finalized. Future documentation should record:

- Which system provides DHCP for each segment.
- Which system provides internal DNS resolution.
- Whether local records are managed manually or through automation.
- Naming conventions for infrastructure hosts and services.

Avoid publishing internal hostnames if they reveal personally identifying information.

## Security Considerations

- Do not expose management interfaces directly to the internet.
- Restrict administrative access to trusted devices and networks.
- Keep switch, router, hypervisor, and service credentials in a password manager.
- Avoid reusing household Wi-Fi names, personal usernames, or exact addresses in public documentation.
- Isolate security testing networks before running offensive or intentionally vulnerable workloads.

## Open Questions

- Which device will act as the long-term router/firewall?
- When should the lab stop relying on the existing household network?
- Which VLANs are required for the first stable segmentation milestone?
- Which services require internal-only DNS records?
- What firewall rules are required for security lab isolation?

## Future Improvements

- Add a sanitized logical network diagram.
- Document VLAN IDs after they are intentionally assigned.
- Document firewall rule philosophy and examples using placeholders.
- Document DHCP scopes and DNS zones in sanitized form.
- Add troubleshooting steps for switch, DHCP, DNS, and gateway issues.

## Related Documentation

- [Architecture Overview](overview.md)
- [Security Architecture](security.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
