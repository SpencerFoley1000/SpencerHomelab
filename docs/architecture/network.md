# Network Architecture

## Purpose

This document describes the homelab network design using sanitized values suitable for a public repository. It explains the current baseline, the intended direction, and the assumptions that should guide future network changes.

## Current Status

The network currently includes:

- A GL.iNet Opal travel router providing the homelab routing boundary.
- Upstream internet connectivity from the existing household network over Wi-Fi.
- A TP-Link managed switch providing wired connectivity for lab infrastructure.
- A Proxmox VE host connected through the managed switch.
- `dns01`, providing Pi-hole DNS, local records, and DNS-based blocking for configured clients.
- `mon01`, providing Prometheus, Grafana, and service monitoring.
- Node Exporter traffic from `dns01` to `mon01` over the internal homelab network.
- Blackbox Exporter DNS probes from `mon01` to `dns01` on UDP port 53.

Dedicated VLANs, management networks, inter-segment firewall policies, and security-lab isolation are planned but not yet implemented as stable architecture.

Exact IP addresses, SSIDs, public IP addresses, ISP details, and other identifying information must not be published.

## Goals

- Build a network that supports learning, experimentation, and safe service hosting.
- Keep the homelab isolated from the rest of the household network wherever practical.
- Separate management, lab, security testing, and general-use traffic where appropriate.
- Keep the initial design simple enough to troubleshoot while leaving room for segmentation.
- Document architecture and reasoning without exposing unnecessary operational details.
- Support reliable DNS, monitoring, backups, and future security projects.

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
| `<MON01_IP>` | Monitoring server address |
| `<REDACTED_SSID>` | Sanitized wireless network name |

## Current Logical Design

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal travel router
  |
TP-Link managed switch
  |
Proxmox VE host
  |-- dns01: Pi-hole DNS and Node Exporter
  `-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter
```

The household network is an upstream dependency, not part of the managed homelab environment. This design allows the lab to experiment with DNS, DHCP, routing, and future segmentation without directly changing the household network.

## Current DNS Design

Pi-hole is deployed as the internal DNS service for the homelab.

| Area | Current Design |
| --- | --- |
| DNS server | `dns01` running Pi-hole |
| Internal DNS zone | `lab` |
| Upstream resolver | Cloudflare DNS selected during initial deployment |
| Current client rollout | Manual client DNS configuration |
| Future client rollout | DHCP option from the homelab router after resilience improves |
| Availability monitoring | Blackbox Exporter DNS probe from `mon01` |

Local DNS records include sanitized infrastructure names such as:

- `dns01.lab`
- `pve01.lab`
- `switch01.lab`

These names are intentionally generic and suitable for public documentation. Avoid committing hostnames that expose personal information.

## Monitoring Traffic

Current monitoring paths include:

| Source | Destination | Purpose |
| --- | --- | --- |
| Prometheus on `mon01` | `mon01:9100` | Local Node Exporter metrics |
| Prometheus on `mon01` | `<DNS01_IP>:9100` | Remote Node Exporter metrics from `dns01` |
| Blackbox Exporter on `mon01` | `<DNS01_IP>:53/udp` | DNS resolution availability probe |
| Browser on trusted network | `<MON01_IP>:3000` | Grafana dashboard access |
| Browser on trusted network | `<MON01_IP>:9090` | Prometheus administration and queries |

All monitoring interfaces are intended for trusted internal access only.

## DHCP Strategy

The GL.iNet Opal currently provides DHCP for the homelab network.

Current approach:

- Keep DHCP on the homelab router.
- Configure selected clients to use Pi-hole while stability is validated.
- Avoid making every client dependent on a single DNS VM before fallback and recovery procedures are tested.

Future approach:

- Configure the router to provide `<DNS01_IP>` as the DNS server for homelab clients.
- Add a secondary DNS server before depending on Pi-hole for every device.
- Document DHCP scope, reservations, and DNS options using placeholders.

## Future Segmentation Plan

| Segment | Purpose | Notes |
| --- | --- | --- |
| Management | Hypervisor, switch, router, and administration interfaces | Restrict access to trusted admin devices |
| Lab Services | DNS, monitoring, dashboards, backups, and internal applications | Permit only required service flows |
| Security Lab | Attacker/defender testing and intentionally vulnerable systems | Isolate from household devices and stable infrastructure |
| Guest / Untrusted | Temporary or low-trust devices | Optional future segment |

Segmentation should be implemented only when it is understood well enough to troubleshoot and recover. VLANs and firewall rules should be documented before they are treated as stable.

## Security Considerations

- Do not expose management interfaces directly to the internet.
- Treat the household network as upstream only, not as managed lab infrastructure.
- Restrict administrative and monitoring access to trusted devices and networks.
- Keep switch, router, hypervisor, Grafana, Prometheus, and Pi-hole credentials in a password manager.
- Avoid reusing household Wi-Fi names, personal usernames, or exact addresses in public documentation.
- Isolate security testing networks before running offensive or intentionally vulnerable workloads.
- Treat DNS query logs and monitoring data as sensitive operational information.
- Do not open Node Exporter, Prometheus, Grafana, or Blackbox Exporter ports to untrusted networks.

## Open Questions

- Is the GL.iNet Opal sufficient as the medium-term homelab edge router?
- When should Pi-hole become the DHCP-provided DNS server for all homelab clients?
- Should a secondary DNS server be deployed before Pi-hole is made network-wide?
- Which VLANs are required for the first stable segmentation milestone?
- What firewall rules are required for management and security-lab isolation?
- Which services require internal-only DNS records?
- Should monitoring interfaces eventually move to a dedicated management network?

## Future Improvements

- Add a sanitized logical network diagram.
- Document VLAN IDs after they are intentionally assigned.
- Document firewall rule philosophy and examples using placeholders.
- Document DHCP scopes and DNS options in sanitized form.
- Add troubleshooting procedures for switch, DHCP, DNS, and gateway failures.
- Add secondary DNS for resilience.
- Add a local-record DNS probe to distinguish internal DNS health from upstream recursive resolution.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Pi-hole Service](../services/pihole.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Router Documentation](../hardware/router.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
