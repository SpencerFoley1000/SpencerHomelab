# Proxmox VE Platform

## Purpose

Proxmox VE is the active virtualization platform for the homelab. It provides the management plane and compute environment for infrastructure virtual machines, including `dns01` and `mon01`.

This page documents Proxmox as an operational platform. Hardware-specific details are documented separately, while design decisions belong in architecture and ADR documentation.

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
| Administrative authentication | Named routine administrator and protected root break-glass identity; TOTP and independent recovery keys enabled |
| Host monitoring | Active through Node Exporter, Prometheus, and Grafana |
| Backup maturity | Project 003A readiness complete; 5 TB target integration, VM backups, and restore testing pending |
| Future platform | X299 server hardware acquired; assembly and validation pending |

The exact management endpoint, internal address, routine administrator name, VM IDs, MAC addresses, storage identifiers, authentication seeds, recovery keys, and sensitive configuration values are intentionally omitted.

## Current Workloads

| VM | Role | Status |
| --- | --- | --- |
| `dns01` | Pi-hole DNS, local records, and Node Exporter | Active |
| `mon01` | Prometheus, Grafana, Node Exporter, and Blackbox Exporter | Active |

The [VM Inventory](../architecture/vm-inventory.md) is the source of truth for VM resources, monitoring, backup maturity, and recovery priority.

## Platform Responsibilities

Proxmox currently provides:

- VM lifecycle management.
- Virtual CPU, memory, storage, and network allocation.
- Internal management access.
- QEMU Guest Agent integration for stable Linux VMs.
- Local virtualization storage.
- The current foundation for Project 003 VM backups and restore testing.
- A platform for future proxy, identity, security, and automation workloads.

## Dependencies

Proxmox operations depend on:

- The Lenovo ThinkPad E16 Gen 1 active host.
- The TP-Link managed switch for wired connectivity.
- The GL.iNet Opal routing boundary.
- Existing upstream household connectivity for package updates and public DNS.
- Local host storage.
- Private credential and recovery-material storage outside Git.
- Accurate system time for TOTP.
- Future 5 TB external backup storage for protected VM recovery.

The VMs can continue running during an upstream internet outage, but package updates and public recursive DNS may be affected.

## Networking

Current network model:

- The management interface is reachable only from the internal homelab network.
- Core infrastructure VMs connect to the homelab LAN.
- Foundational services use static addressing.
- Exact bridge names, addresses, MAC addresses, and VM IDs are not published.
- VLAN-aware bridges and isolated workload networks remain planned.

Future networking documentation must record:

- Sanitized bridge roles.
- VLAN-aware configuration.
- Management-network placement.
- Allowed workload networks.
- Security-lab isolation boundaries.
- The network relationship between the ThinkPad and future server.

## Firewall

The Proxmox firewall service is active.

During Node Exporter deployment, `mon01` successfully reached `<PVE01_IP>:9100` while the firewall was enabled. Because existing policy already permitted the trusted monitoring connection, no broad inbound rule was added.

Firewall-change sequence:

1. Test the required path from the intended source.
2. Confirm whether existing policy already permits it.
3. Add the narrowest required source, destination, protocol, and port rule only when needed.
4. Revalidate management access and monitoring afterward.
5. Document permanent policy changes.

## Administrative Authentication

Proxmox administrative access uses separate routine and emergency identities:

| Identity | Intended use | Controls |
| --- | --- | --- |
| `<PROXMOX_ADMIN_ACCOUNT>` | Routine web-interface administration | Unique password, TOTP, propagated Administrator role, dedicated recovery keys |
| `root@pam` | Break-glass and root-only Proxmox actions | Unique password, TOTP, separate recovery keys, restricted routine use |
| Physical console | Final recovery path | Physical access to `pve01` |

Operational rules:

- Use `<PROXMOX_ADMIN_ACCOUNT>` for routine Proxmox administration.
- Reserve `root@pam` for emergencies and operations that require the root identity.
- Keep the actual account name, passwords, TOTP seeds, QR codes, and recovery keys outside Git.
- Keep recovery material separate from the enrolled authenticator device.
- Do not consume recovery keys during routine testing.
- Re-enroll TOTP and rotate affected recovery material after authenticator loss or replacement.

Validation completed during implementation:

- `System clock synchronized: yes`.
- `NTP service: active`.
- Both identities completed clean password-and-TOTP logins from fresh browser sessions.
- Each identity has a separate recovery-key set.
- The named routine administrator can manage the host and active VMs through its propagated role.
- Root authentication-factor changes require a root-authenticated session; the named administrator received a `403` when attempting to modify `root@pam` TOTP.

The routine Proxmox identity is application-level. It does not create a Debian user or automatically grant console or SSH access.

## Storage

The active platform currently uses the ThinkPad's local 1 TB PCIe SSD.

Project 003 will add a dedicated 5 TB external backup target. Before it is considered operational, document and validate:

- Drive inspection and expected capacity.
- Filesystem and stable mount method.
- Proxmox storage registration.
- Protected VM coverage.
- Backup schedule, retention, and pruning.
- Capacity thresholds.
- Representative restore results.

The future X299 server has two existing 1 TB NVMe devices, but their final storage layout is not yet approved.

Until VM backups and restore tests succeed, stable workloads remain recoverable only through service documentation, private application exports, and manual reconstruction—not proven whole-VM restoration.

## QEMU Guest Agent

QEMU Guest Agent is installed on stable Debian VMs where supported.

The agent depends on:

- The guest package and service.
- The Proxmox-provided virtio serial device.

A full Proxmox stop/start may be required after enabling virtual hardware. See [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md).

## Monitoring

### Current Baseline

Node Exporter `1.9.0-1+b4` is installed directly on `pve01`.

Validated state:

- `prometheus-node-exporter` is active and enabled.
- `/metrics` responds on TCP `9100`.
- `mon01` can reach the endpoint.
- Prometheus scrapes it under the shared `node_exporter` job.
- Labels are `host="pve01"` and `role="hypervisor"`.
- Target-specific PromQL returns `1`.
- Grafana displays CPU, memory, filesystem, network, and uptime metrics.

```promql
up{job="node_exporter", host="pve01", role="hypervisor"}
```

Expected result: `1`.

### Monitoring Boundary

Node Exporter provides Linux operating-system metrics. It does not provide authoritative:

- VM or container state.
- Cluster or quorum status.
- Proxmox task results.
- Storage-pool state.
- Backup-job health.
- Replication or migration state.

A future Proxmox exporter or API integration must use a dedicated least-privilege identity. Credentials must remain outside Git.

## Security Considerations

- Do not expose Proxmox management publicly.
- Use `<PROXMOX_ADMIN_ACCOUNT>` for routine management and reserve `root@pam` for break-glass work.
- Maintain independent recovery keys.
- Keep account names, passwords, TOTP seeds, QR codes, and recovery keys outside the repository.
- Limit management access to trusted devices and future management networks.
- Keep experimental and attacker-style workloads isolated.
- Do not publish exact management addresses, VM IDs, MAC addresses, storage identifiers, or sensitive exports.
- Treat the hypervisor as high-value infrastructure because all active VMs depend on it.
- Review privileged containers, passthrough devices, nested virtualization, and unusual permissions.
- Keep Node Exporter internal-only.
- Introduce API monitoring credentials only through a documented least-privilege design.

## Backup and Recovery

Project 003A completed the service-state and recovery inventory. VM backup infrastructure is not yet implemented or restore-tested.

Current recovery order:

1. Restore physical network connectivity and Proxmox management access.
2. Restore `dns01` and validate public and local DNS.
3. Restore `mon01` and validate Prometheus, all Node Exporter targets, both Blackbox jobs, and Grafana.
4. Confirm monitoring observes `pve01`, `dns01`, and `mon01`.
5. Restore lower-priority workloads.

Administrative-access recovery must preserve:

- The protected root break-glass identity.
- Recovery keys independent of the authenticator device.
- Accurate system time.
- Physical-console access as the final path.

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
timedatectl status
```

Expected TOTP time state:

```text
System clock synchronized: yes
NTP service: active
```

From `mon01`:

```bash
curl --connect-timeout 5 --fail --silent --show-error \
  http://<PVE01_IP>:9100/metrics | head
```

Grafana validation:

- Confirm `pve01` appears in the detailed Node Exporter dashboard.
- Confirm it appears in the Homelab Infrastructure Overview.
- Confirm CPU, memory, filesystem, network, and uptime panels update.

## Maintenance Notes

After Proxmox upgrades:

- Record the new version and kernel.
- Confirm the firewall service.
- Confirm Node Exporter remains active and reachable.
- Confirm Prometheus reports `pve01` as `UP`.
- Confirm Grafana panels resume.
- Confirm system time remains synchronized.
- Complete a fresh TOTP login with the routine administrator.
- Validate `dns01` and `mon01` after host reboot.

After authenticator loss or replacement:

- Use a recovery key or protected break-glass path.
- Remove the old enrollment.
- Enroll the replacement authenticator.
- Generate and store replacement recovery material when required.
- Verify routine and break-glass paths.

## Future Improvements

- Document sanitized bridge and storage layout.
- Add Proxmox-specific VM, storage, task, and backup metrics.
- Complete Project 003 backups and restore testing.
- Create a tested Proxmox maintenance and management-access recovery runbook.
- Review SSH authentication and root-login policy after console recovery is documented.
- Evaluate authentication-failure monitoring and rate limiting without unnecessary complexity.
- Restrict management through a dedicated management network when segmentation is implemented.
- Assemble and validate the future X299 server.
- Create an ADR defining whether the new server replaces or supplements `pve01`.
- Integrate UPS monitoring and graceful shutdown under Project 005.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [Node Exporter](node-exporter.md)
- [Prometheus](prometheus.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Current Proxmox Host Hardware](../hardware/server.md)
- [Future Virtualization Server Build](../hardware/server-build.md)
- [Network Architecture](../architecture/network.md)
- [Project 002: Monitoring](../projects/project-002-monitoring-observability.md)
- [Project 003: Backup and Recovery](../projects/project-003-backup-recovery.md)
- [ADR-0001: Initial Proxmox Host](../decisions/ADR-0001-proxmox-on-thinkpad-e16.md)
- [Authentication Hardening Change Record](../changes/2026-07-12-proxmox-administrative-authentication-hardening.md)
- [QEMU Guest Agent Troubleshooting](../runbooks/qemu-guest-agent-troubleshooting.md)
