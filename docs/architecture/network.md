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
- `proxy01`, providing NGINX Proxy Manager, internal TLS termination, and Node Exporter.
- Node Exporter on `pve01`, `dns01`, `mon01`, and `proxy01`.
- Recursive and local DNS probes from `mon01` to `dns01` over UDP `53`.
- Internal HTTPS probes from `mon01` through `proxy01` to selected backends.

Dedicated VLANs, management networks, inter-segment firewall policy, and security-lab isolation remain planned rather than stable architecture.

Exact IP addresses, SSIDs, public addresses, ISP details, MAC addresses, certificate private keys, and other identifying values must not be published.

## Goals

- Support reliable DNS, monitoring, backups, internal HTTPS, and future services.
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
| `<PROXY01_IP>` | Reverse-proxy VM address |
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
  |-- mon01: Prometheus, Grafana, Node Exporter, Blackbox Exporter
  `-- proxy01: NGINX Proxy Manager, Docker, Node Exporter
```

The household network is an upstream dependency, not managed homelab infrastructure. The Opal creates a separate routing boundary so DNS, DHCP, monitoring, proxying, and future segmentation work do not directly modify the household network.

## Current DNS Design

| Area | Current design |
| --- | --- |
| DNS server | `dns01` running Pi-hole |
| Internal service namespace | `lab.home.arpa` |
| Upstream resolver | Cloudflare DNS selected during initial deployment |
| Client rollout | Selected clients configured manually |
| Future rollout | Router DHCP option after resilience improves |
| Recursive monitoring | `blackbox_dns` from `mon01` |
| Local-record monitoring | `blackbox_dns_local` from `mon01` |

Current friendly service records include:

- `grafana.lab.home.arpa`
- `pihole.lab.home.arpa`

These records resolve to `<PROXY01_IP>`. NGINX Proxy Manager selects the correct backend using the requested hostname.

The `home.arpa` namespace avoids `.local` multicast-DNS ambiguity and does not claim public DNS validity.

## Reverse-Proxy Flow

```text
Trusted client
    |
    | DNS query
    v
dns01 / Pi-hole
    |
    | service name -> <PROXY01_IP>
    v
proxy01 / NGINX Proxy Manager
    |
    | internal HTTP
    v
Selected backend
```

Current design rules:

- No public DNS records are required.
- No edge-router port forwarding is configured.
- Port `81` remains an internal administration interface.
- Backend authentication remains active.
- Direct backend access remains available for recovery.
- Proxmox management is not placed behind the proxy.

## Required Traffic Flows

| Source | Destination | Protocol | Purpose |
| --- | --- | --- | --- |
| Prometheus on `mon01` | `localhost:9090` | TCP | Prometheus self-monitoring |
| Prometheus on `mon01` | `localhost:9100` | TCP | `mon01` Node Exporter metrics |
| Prometheus on `mon01` | `<DNS01_IP>:9100` | TCP | `dns01` Node Exporter metrics |
| Prometheus on `mon01` | `<PVE01_IP>:9100` | TCP | `pve01` Node Exporter metrics |
| Prometheus on `mon01` | `<PROXY01_IP>:9100` | TCP | `proxy01` Node Exporter metrics |
| Prometheus on `mon01` | `localhost:9115` | TCP | Blackbox Exporter probe endpoint |
| Blackbox Exporter on `mon01` | `<DNS01_IP>:53` | UDP | Recursive and local DNS probes |
| Blackbox Exporter on `mon01` | `<PROXY01_IP>:443` | TCP/TLS | Internal HTTPS and certificate probes |
| Trusted browser | `<PROXY01_IP>:443` | TCP/TLS | Friendly HTTPS service access |
| Trusted administrator | `<PROXY01_IP>:81` | TCP | NGINX Proxy Manager administration |
| `proxy01` | `<MON01_IP>:3000` | TCP | Grafana backend traffic |
| `proxy01` | `<DNS01_IP>:80` | TCP | Pi-hole administration backend traffic |
| Trusted administrator | Direct backend addresses | TCP | Emergency recovery access |

All management, monitoring, proxy, and backend interfaces are internal-only.

## DNS and Proxy Failure Domains

| Observation | Likely investigation area |
| --- | --- |
| DNS probes down, direct IP access works | `dns01`, Pi-hole, local records, or DNS path |
| Friendly name resolves but HTTPS probe fails | `proxy01`, NGINX Proxy Manager, certificate, or proxy route |
| HTTPS probe succeeds but application login fails | Backend application or authentication |
| Proxy route fails but direct backend works | NGINX Proxy Manager configuration or proxy-to-backend path |
| Both proxy and direct backend fail | Backend VM, application, routing, or shared infrastructure |
| Certificate days missing while HTTPS works | Blackbox module, Prometheus job, or metric query |

## DHCP Strategy

The Opal currently provides DHCP.

Current approach:

- Keep DHCP on the router.
- Use reservations or stable assignments for foundational VMs.
- Configure selected clients to use Pi-hole during validation.
- Avoid making every device dependent on one DNS VM before secondary DNS and recovery are tested.

Future approach:

- Provide `<DNS01_IP>` through DHCP.
- Add secondary DNS first.
- Document scopes, reservations, and DNS options with placeholders.

## Future Segmentation

| Segment | Purpose | Policy direction |
| --- | --- | --- |
| Management | Hypervisor, router, switch, proxy administration, monitoring administration | Trusted administrative devices only |
| Lab Services | DNS, monitoring, proxy traffic, internal applications | Permit documented service flows |
| Security Lab | Attacker, defender, and intentionally vulnerable systems | Isolate from household and stable infrastructure |
| Guest / Untrusted | Temporary or lower-trust devices | Restrict access to internal services |

Segmentation should be implemented only when it can be documented, tested, and recovered. VLAN IDs and firewall rules should not be treated as stable until verified.

## Security Considerations

- Do not expose management, monitoring, proxy administration, or internal HTTPS services directly to the internet.
- Treat the household network as upstream only.
- Restrict administrative access to trusted devices.
- Store router, switch, hypervisor, Grafana, Prometheus, Pi-hole, proxy, and PKI secrets outside Git.
- Do not publish exact addresses, SSIDs, MAC addresses, or personal usernames.
- Treat DNS query logs, proxy configuration, certificate state, and monitoring data as sensitive.
- Keep TCP `81`, `3000`, `9090`, `9100`, and `9115` off untrusted networks.
- Isolate offensive and intentionally vulnerable workloads before use.
- Prefer narrowly scoped firewall policy over broad convenience rules.

## Open Questions

- Is the Opal sufficient as the medium-term edge router?
- When should Pi-hole become the DHCP-provided resolver for all lab clients?
- Which secondary DNS design best fits the lab?
- Which VLANs are needed for the first stable segmentation milestone?
- Should monitoring and proxy administration move to a dedicated management network?
- When should wildcard certificates be replaced with per-service certificates?

## Future Improvements

- Add a sanitized logical network diagram.
- Document VLAN IDs after intentional assignment.
- Document firewall-rule philosophy with sanitized examples.
- Document DHCP scopes and DNS options.
- Add switch, gateway, DHCP, DNS, and proxy troubleshooting procedures.
- Add secondary DNS for resilience.
- Restrict proxy administration and monitoring paths after segmentation.

## Related Documentation

- [Architecture Overview](overview.md)
- [Virtualization Architecture](virtualization.md)
- [VM Inventory](vm-inventory.md)
- [Monitoring Architecture](monitoring.md)
- [Security Architecture](security.md)
- [Pi-hole Service](../services/pihole.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Blackbox Exporter Service](../services/blackbox-exporter.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Router Documentation](../hardware/router.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
