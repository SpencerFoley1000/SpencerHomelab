# Project 001: Pi-hole DNS Service

## Status

Completed

## Purpose

Project 001 established the first production-style service in the homelab by deploying Pi-hole on a dedicated Debian virtual machine.

The project was intended to create useful internal DNS infrastructure while building practical experience with Proxmox VM provisioning, Linux administration, static networking, DNS troubleshooting, and service documentation.

## Objectives

- Deploy a dedicated Debian VM named `dns01`.
- Configure stable network addressing using sanitized public documentation.
- Install Pi-hole as the homelab DNS service.
- Add local DNS records for core infrastructure.
- Validate DNS resolution from another client.
- Document recovery, security, and future backup requirements.

## Architecture Impact

Project 001 introduced:

- The first active infrastructure VM on Proxmox.
- Pi-hole as the internal DNS and local-record service.
- The `lab` internal DNS zone.
- A dependency on the GL.iNet Opal routing boundary and managed switch.
- The initial VM inventory and service documentation pattern.

The service initially supports manually configured clients. Router-provided DNS remains a future change until resilience and recovery procedures are stronger.

## Results

- Deployed `dns01` on Proxmox VE.
- Installed Debian 13.5 as a minimal headless server.
- Configured non-root administration with `sudo`.
- Installed and validated QEMU Guest Agent.
- Configured a static homelab address.
- Installed Pi-hole using the official installer.
- Selected Cloudflare as the initial upstream resolver.
- Added sanitized local DNS records for core infrastructure.
- Confirmed public and local DNS resolution from a separate client.
- Added service, network, virtualization, and VM inventory documentation.

## Validation

Validation included:

- Confirming `dns01` was reachable on the homelab LAN.
- Confirming Pi-hole services were active.
- Confirming the Pi-hole administration interface was reachable internally.
- Resolving public domains through Pi-hole.
- Resolving local records such as `dns01.lab` and `pve01.lab` from another client.

## Troubleshooting and Lessons Learned

- Hardware virtualization had to be enabled in system firmware before Proxmox could run KVM-backed VMs.
- Debian administrator behavior depends on whether a root password is configured during installation; `sudo` membership required correction.
- Minimal Debian installations may omit common troubleshooting tools.
- Static IP configuration can work while DNS fails if `/etc/resolv.conf` is incomplete.
- QEMU Guest Agent depends on both the guest package and Proxmox-side virtual hardware configuration.
- Layered troubleshooting is effective: verify local configuration, gateway reachability, internet connectivity by IP, and DNS resolution separately.

## Security Considerations

- Pi-hole is internal-only and must not be exposed directly to the internet.
- Administrative credentials are stored outside the repository.
- DNS query logs are treated as sensitive operational data.
- Public documentation uses placeholders instead of exact addresses or personally identifying network names.

## Follow-Up Tasks

- [ ] Configure router DHCP to provide Pi-hole as DNS after resilience is improved.
- [ ] Add a secondary DNS service.
- [ ] Export Pi-hole configuration after meaningful changes.
- [x] Add host and service-level monitoring for `dns01`.
- [ ] Add VM backup coverage and complete a restore test.
- [ ] Evaluate Unbound only after the current DNS design is stable.

## Related Documentation

- [Pi-hole Service](../services/pihole.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Project 002: Monitoring and Observability](project-002-monitoring-observability.md)
- [Changelog](../../CHANGELOG.md)
