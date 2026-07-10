# Proxmox VE Platform

## Purpose

Proxmox VE is the active virtualization platform for the homelab. It provides the management plane and compute environment for infrastructure virtual machines, including `dns01` and `mon01`.

This page documents Proxmox as an operational platform. Hardware-specific details are documented separately on the server page, while design decisions belong in the virtualization architecture and ADR documentation.

## Status

| Area | Details |
| --- | --- |
| Lifecycle state | Active |
| Platform role | Primary hypervisor and VM management platform |
| Hostname | `pve01` |
| Hardware | Lenovo ThinkPad E16 Gen 1 |
| Proxmox VE version | `9.2.2` |
| Debian base | Debian 13 Trixie |
| Running kernel | `7.0.2-6-pve` |
| Management exposure | Internal homelab only |
| Public access | None |
| Host monitoring | Active through Node Exporter and Prometheus |
| Backup maturity | Readiness inventory complete; VM backup and restore testing pending |

The exact management endpoint, internal address, VM IDs, MAC addresses, storage identifiers, and sensitive configuration values are intentionally omitted.

## Current Workloads

| VM | Role | Status |
| --- | --- | --- |
| `dns01` | Pi-hole DNS and local records | Active |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active |

The [VM Inventory](../architecture/vm-inventory.md) is the source of truth for virtual machines and resource allocations.

## Platform Responsibilities

Proxmox currently provides:

- VM lifecycle management.
- Virtual CPU, memory, storage, and network allocation.
- Internal management access for the homelab administrator.
- QEMU Guest Agent integration for stable Linux VMs.
- Local virtualization storage.
- A foundation for future snapshots, backups, templates, containers, and isolated security workloads.

## Dependencies

Proxmox operations depend on:

- The Lenovo ThinkPad E16 Gen 1 virtualization host.
- The TP-Link managed switch for wired connectivity.
- The GL.iNet Opal routing boundary.
- Existing upstream household connectivity for internet access and package updates.
- Local storage on the Proxmox host.
- Private credential storage outside the repository.

The VMs can continue running during an upstream internet outage, but package updates and public DNS resolution may be affected.

## Networking

The current network model is intentionally simple:

- The Proxmox management interface is reachable only from the internal homelab network.
- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use static addressing.
- Exact bridge names, addresses, MAC addresses, and VM IDs are not published.
- VLAN-aware bridges and isolated workload networks are planned but not yet stable architecture.

Future networking documentation should record:

- Bridge roles.
- VLAN-aware configuration.
- Management network placement.
- Allowed workload networks.
- Security-lab isolation boundaries.

## Firewall

The Proxmox firewall service is active.

During Node Exporter deployment, `mon01` successfully reached `<PVE01_IP>:9100` while the firewall was enabled. Because the existing policy already permitted the trusted monitoring connection, no broad inbound rule was added.

Firewall changes should follow this sequence:

1. Test the required path from the intended source.
2. Confirm whether an existing rule already permits it.
3. Add the narrowest source-, destination-, protocol-, and port-specific rule only when required.
4. Revalidate management access and monitoring afterward.

## Storage

The platform currently uses the host's local 1 TB PCIe SSD.

Public documentation does not yet record the exact Proxmox storage layout. Before storage becomes more complex, document:

- Storage-pool roles.
- VM disk placement.
- ISO and template storage.
- Available-capacity thresholds.
- Backup destination and retention.
- Restore-test results.

Until backup infrastructure is deployed and tested, workloads should be considered recoverable through service documentation, protected application exports, and manual reconstruction rather than proven VM restoration.

## QEMU Guest Agent

QEMU Guest Agent is installed on stable Debian VMs where supported.

The agent depends on both:

- The guest package and systemd service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling virtual hardware. See the [QEMU Guest Agent Troubleshooting Runbook](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

### Current Baseline

Node Exporter package version `1.9.0-1+b4` is installed directly on `pve01`.

Validated state:

- `prometheus-node-exporter` is active and enabled.
- The local `/metrics` endpoint responds on TCP `9100`.
- `mon01` can reach the endpoint.
- Prometheus scrapes the target under the shared `node_exporter` job.
- Target labels are `host="pve01"` and `role="hypervisor"`.
- The target-specific PromQL query returns `1`.
- Grafana displays CPU, memory, filesystem, network, and uptime metrics.

Sanitized validation query:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

### Monitoring Boundary

Node Exporter provides Linux operating-system metrics. It does not provide authoritative Proxmox platform state such as:

- VM or container status.
- Cluster or quorum status.
- Proxmox task results.
- Storage-pool state.
- Backup-job health.
- Replication or migration state.

A future Proxmox-specific exporter or API integration should use a dedicated least-privilege identity. API credentials must remain outside Git.

## Security Considerations

- Do not expose the Proxmox management interface directly to the internet.
- Use strong, unique administrative credentials stored outside the repository.
- Limit management access to trusted devices and future management networks.
- Keep experimental and attacker-style workloads isolated from trusted infrastructure.
- Do not publish exact management addresses, VM IDs, MAC addresses, storage identifiers, or sensitive exports.
- Treat the Proxmox host as high-value infrastructure because every active VM depends on it.
- Review privileged containers, passthrough devices, and unusual VM permissions before use.
- Keep Node Exporter internal-only and restrict port `9100` to trusted monitoring paths where practical.
- Introduce API monitoring credentials only through a documented least-privilege design.

## Backup and Recovery

Project 003 Phase 003A completed the backup-readiness and configuration inventory, but VM backup infrastructure is not yet implemented or restore-tested.

The implementation phase must define:

- Backup destination.
- Protected VMs.
- Backup frequency and retention.
- Credential handling.
- Restore order and recovery priorities.
- Representative restore testing.

Current recovery order:

1. Restore Proxmox management and networking.
2. Restore `dns01` because other services may depend on DNS.
3. Restore `mon01` to regain monitoring visibility.
4. Restore lower-priority or experimental workloads.

## Validation

Useful platform checks:

```bash
pveversion
. /etc/os-release && echo "$PRETTY_NAME"
systemctl is-active pve-firewall
systemctl is-active prometheus-node-exporter
systemctl is-enabled prometheus-node-exporter
curl -s http://localhost:9100/metrics | head
ss -ltnp | grep 9100
```

From `mon01`:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  http://<PVE01_IP>:9100/metrics | head
```

Prometheus:

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Grafana:

- Select the `node_exporter` job.
- Select `pve01` or its sanitized instance equivalent.
- Confirm CPU, memory, filesystem, network, and uptime panels populate.

## Maintenance Notes

Routine Proxmox maintenance should eventually have a tested runbook covering:

- Update review and package installation.
- Backup checks before major changes.
- VM shutdown and startup order.
- Host reboot expectations.
- Validation of `dns01`, `mon01`, and `pve01` monitoring after maintenance.
- Recovery steps if management access is lost.

After Proxmox upgrades:

- Record the new version and kernel.
- Confirm Node Exporter remains active.
- Confirm Prometheus still reports `pve01` as `UP`.
- Confirm Grafana panels resume after the host returns.

## Future Improvements

- Document the sanitized bridge and storage layout.
- Add Proxmox-specific VM, storage, task, and backup metrics.
- Implement and test VM backups under Project 003.
- Create a Proxmox maintenance runbook.
- Document VLAN-aware networking after segmentation is implemented.
- Build a custom hypervisor dashboard and actionable capacity alerts.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Node Exporter](node-exporter.md)
- [Prometheus](prometheus.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Proxmox Host Hardware](../hardware/server.md)
- [Storage Architecture](../architecture/storage.md)
- [Network Architecture](../architecture/network.md)
- [Project 002: Monitoring](../projects/project-002-monitoring-observability.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0001: Initial Proxmox Host](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md)
