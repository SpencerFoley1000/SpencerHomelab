# Network Architecture

## Purpose

This document describes the homelab network using sanitized values suitable for a public portfolio. It records the current design, required service flows, security boundaries, and planned segmentation without exposing exact addresses or personally identifying details.

## Current Status

The network currently includes:

- A GL.iNet Opal travel router providing the homelab routing boundary.
- Upstream internet connectivity from the existing household network over Wi-Fi.
- A TP-Link managed switch providing wired connectivity.
- A Proxmox VE host connected through the managed switch.
- `dns01`, providing Pi-hole DNS, local records, and DNS filtering.
- `mon01`, providing Prometheus, Grafana, Node Exporter, and Blackbox Exporter.
- Node Exporter on `pve01`, `dns01`, and `mon01`.
- Recursive and local DNS probes from `mon01` to `dns01` over UDP `53`.

Dedicated VLANs, management networks, inter-segment firewall policy, and security-lab isolation remain planned rather than stable architecture.

Exact IP addresses, SSIDs, public addresses, ISP details, MAC addresses, and other identifying values must not be published.

## Goals

- Support reliable DNS, monitoring, backups, and future services.
- Isolate the homelab from the household network wherever practical.
- Keep the current design simple enough to troubleshoot.
- Prepare for management, service, security-lab, and untrusted segmentation.
- Document required traffic flows before enforcing restrictive policy.
- Preserve useful public architecture detail without exposing operational secrets.

## Sanitized Addressing Model

| Placeholder | Meaning |
| --- | --- |
| `<HOMELAB_LAN>` | Current private network behind the homelab router |
| `<UPSTREAM_NETWORK>` | Household network used only for upstream connectivity |
| `<MGMT_NETWORK>` | Future management network |
| `<LAB_NETWORK>` | Future stable service network |
| `<SECURITY_LAB_NETWORK>` | Future isolated security-testing network |
| `<ROUTER_IP>` | Homelab gateway |
| `<SWITCH_MGMT_IP>` | Managed-switch address |
| `<PVE01_IP>` | Proxmox host address |
| `<DNS01_IP>` | Pi-hole DNS address |
| `<MON01_IP>` | Monitoring VM address |
| `<REDACTED_SSID>` | Sanitized wireless network name |

## Current Logical Design

```text
Internet
  |
Existing household network / upstream Wi-Fi
  |
GL.iNet Opal router
  |
TP-Link managed switch
  |
Proxmox VE host: pve01
  |-- dns01: Pi-hole DNS and Node Exporter
  `-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter
```

The household network is an upstream dependency, not managed homelab infrastructure. The Opal creates a separate routing boundary so DNS, DHCP, monitoring, and future segmentation work do not directly modify the household network.

## Current DNS Design

| Area | Current design |
| --- | --- |
| DNS server | `dns01` running Pi-hole |
| Internal DNS zone | `lab` |
| Upstream resolver | Cloudflare DNS selected during initial deployment |
| Client rollout | Selected clients configured manually |
| Future rollout | Router DHCP option after resilience improves |
| Recursive monitoring | `blackbox_dns` from `mon01` |
| Local-record monitoring | `blackbox_dns_local` from `mon01` |

Sanitized local records include:

- `dns01.lab`
- `pve01.lab`
- `switch01.lab`

These generic names are suitable for public documentation. Records containing personal names or identifying context must remain private.

## Required Monitoring Flows

| Source | Destination | Protocol | Purpose |
| --- | --- | --- | --- |
| Prometheus on `mon01` | `localhost:9090` | TCP | Prometheus self-monitoring |
| Prometheus on `mon01` | `localhost:9100` | TCP | `mon01` Node Exporter metrics |
| Prometheus on `mon01` | `<DNS01_IP>:9100` | TCP | `dns01` Node Exporter metrics |
| Prometheus on `mon01` | `<PVE01_IP>:9100` | TCP | `pve01` Node Exporter metrics |
| Prometheus on `mon01` | `localhost:9115` | TCP | Blackbox Exporter probe endpoint |
| Blackbox Exporter on `mon01` | `<DNS01_IP>:53` | UDP | Recursive and local DNS probes |
| Trusted browser | `<MON01_IP>:3000` | TCP | Grafana access |
| Trusted browser | `<MON01_IP>:9090` | TCP | Prometheus queries and administration |

All monitoring interfaces are internal-only.

The Proxmox firewall was active when `pve01` monitoring was added. Testing from `mon01` confirmed the required TCP `9100` flow already worked, so no broad allow rule was introduced.

## DNS Probe Failure Domains

Recursive probe path:

```text
mon01 -> dns01/Pi-hole -> upstream resolver -> public answer
```

Local probe path:

```text
mon01 -> dns01/Pi-hole -> internal record answer
```

Interpretation:

- Recursive down, local up: investigate upstream resolver or internet path.
- Recursive up, local down: investigate Pi-hole local-record state.
- Both down: investigate `dns01`, Pi-hole, routing, firewall, or the monitoring path.

## DHCP Strategy

The Opal currently provides DHCP.

Current approach:

- Keep DHCP on the router.
- Configure selected clients to use Pi-hole during validation.
- Avoid making every device dependent on one DNS VM before secondary DNS and recovery are tested.

Future approach:

- Provide `<DNS01_IP>` through DHCP.
- Add secondary DNS first.
- Document scopes, reservations, and DNS options with placeholders.

## Future Segmentation

| Segment | Purpose | Policy direction |
| --- | --- | --- |
| Management | Hypervisor, router, switch, administration interfaces | Trusted administrative devices only |
| Lab Services | DNS, monitoring, dashboards, backups, internal applications | Permit documented service flows |
| Security Lab | Attacker, defender, and intentionally vulnerable systems | Isolate from household and stable infrastructure |
| Guest / Untrusted | Temporary or lower-trust devices | Restrict access to internal services |

Segmentation should be implemented only when it can be documented, tested, and recovered. VLAN IDs and firewall rules should not be treated as stable until verified.

## Security Considerations

- Do not expose management or monitoring interfaces directly to the internet.
- Treat the household network as upstream only.
- Restrict administrative access to trusted devices.
- Store router, switch, hypervisor, Grafana, Prometheus, and Pi-hole credentials outside Git.
- Do not publish exact addresses, SSIDs, MAC addresses, or personal usernames.
- Treat DNS query logs and monitoring data as sensitive.
- Keep TCP `3000`, `9090`, `9100`, and `9115` off untrusted networks.
- Isolate offensive and intentionally vulnerable workloads before use.
- Prefer narrowly scoped firewall policy over broad convenience rules.

## Open Questions

- Is the Opal sufficient as the medium-term edge router?
- When should Pi-hole become the DHCP-provided resolver for all lab clients?
- Which secondary DNS design best fits the lab?
- Which VLANs are needed for the first stable segmentation milestone?
- Should monitoring interfaces move to a dedicated management network?
- Which services require internal DNS and HTTPS?

## Future Improvements

- Add a sanitized logical network diagram.
- Document VLAN IDs after intentional assignment.
- Document firewall-rule philosophy with sanitized examples.
- Document DHCP scopes and DNS options.
- Add switch, gateway, DHCP, and DNS troubleshooting procedures.
- Add secondary DNS for resilience.
- Revisit monitoring flows after segmentation is implemented.

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
