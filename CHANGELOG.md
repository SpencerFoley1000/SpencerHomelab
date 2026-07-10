# Changelog

This changelog records meaningful infrastructure, documentation, and process changes in reverse chronological order.

## 2026-07-09 - mon01 Resource Tuning

### Changed

- Increased `mon01` memory allocation from 2 GB to 3 GB.
- Left `mon01` CPU and disk allocation unchanged.
- Updated `docs/architecture/vm-inventory.md` to reflect the new RAM allocation.
- Updated `docs/projects/project-002-monitoring-observability.md` with the sizing rationale and troubleshooting lesson.

### Why

- Grafana showed `mon01` using roughly 1.55 GB of RAM consistently, with occasional spikes near 1.85 GB.
- `mon01` runs Prometheus, Grafana, and Node Exporter, making it the core monitoring system for the homelab.
- Additional headroom is appropriate before adding more monitoring components such as DNS availability checks or Blackbox Exporter.
- 3 GB provides a safer operating margin without overcommitting the current 16 GB Proxmox host.

### Lessons Learned

- Monitoring infrastructure should be monitored and resized based on observed behavior.
- Linux memory graphs should be interpreted carefully, but sustained pressure near the VM limit is still worth addressing.
- Small resource changes should still be documented because they affect capacity planning and future troubleshooting.

## 2026-07-09 - Project 002: Monitoring Baseline, Node Exporter, Prometheus, Grafana, and dns01 Monitoring

### Changed

- Deployed `mon01` as the dedicated monitoring and observability VM.
- Installed Debian 13.5 (Trixie) as a minimal headless server.
- Configured non-root administration with `sudo`.
- Installed baseline administrative tools and QEMU Guest Agent.
- Validated package repositories, networking, and DNS resolution on `mon01`.
- Installed Node Exporter using the Debian package repository.
- Verified Node Exporter locally with `curl localhost:9100/metrics`.
- Installed Prometheus using the Debian package repository.
- Configured Prometheus to scrape itself on `localhost:9090` and Node Exporter on `localhost:9100`.
- Validated Prometheus target health in the web UI, with both initial scrape targets reporting `UP`.
- Ran initial PromQL validation queries including `up`, `node_memory_MemAvailable_bytes`, and root filesystem availability checks.
- Installed Grafana using the Grafana APT repository.
- Started and validated the `grafana-server` service.
- Configured Grafana to use Prometheus as its first data source.
- Imported a Node Exporter dashboard to validate end-to-end visualization.
- Installed Node Exporter on `dns01`.
- Validated the `dns01` Node Exporter endpoint locally with `curl localhost:9100/metrics`.
- Validated remote scrape reachability from `mon01` to `dns01`.
- Added `dns01` as the first remote Prometheus scrape target under the `node_exporter` job.
- Confirmed Prometheus target health showed the `dns01` target as `UP`.
- Confirmed Grafana can display both `mon01` and `dns01` when using the `node_exporter` job selector.
- Added `mon01` to the VM inventory under `docs/architecture/vm-inventory.md`.
- Updated `dns01` in the VM inventory to reflect monitored host metrics.
- Updated monitoring architecture documentation under `docs/architecture/monitoring.md`.
- Added Node Exporter service documentation under `docs/services/node-exporter.md`.
- Added Prometheus service documentation under `docs/services/prometheus.md`.
- Added Grafana service documentation under `docs/services/grafana.md`.
- Updated Project 002 progress documentation under `docs/projects/project-002-monitoring-observability.md`.
- Added a QEMU Guest Agent troubleshooting runbook under `docs/runbooks/qemu-guest-agent-troubleshooting.md`.

### Why

- Establish monitoring as a dedicated infrastructure role instead of combining it with DNS or the Proxmox host.
- Build the observability stack from the bottom up by exposing metrics before installing Prometheus or Grafana.
- Move from one-time metric inspection to time-series metric collection and dashboard visualization.
- Expand monitoring coverage beyond the monitoring VM itself by adding `dns01`, the first production-style service VM.
- Practice enterprise-style separation of responsibilities, validation, troubleshooting, and documentation.
- Create a foundation for future host metrics, DNS health checks, dashboards, alerting, and capacity planning.

### Lessons Learned

- Node Exporter exposes Linux host metrics through a simple HTTP `/metrics` endpoint.
- Metrics are numerical measurements of system state over time.
- Prometheus scrapes configured targets on an interval and stores metric samples as time-series data.
- Grafana connects to Prometheus as a data source and visualizes PromQL-backed metrics.
- Building the stack layer-by-layer makes troubleshooting easier because each dependency can be validated independently.
- Remote scrape targets should be validated with `curl` from the Prometheus host before Prometheus configuration is changed.
- Scraping `dns01` by static IP avoids making DNS monitoring depend on DNS resolution from the same host being monitored.
- Prometheus target health may briefly show `UNKNOWN` until the first scrape completes.
- Imported Grafana dashboards may assume different Prometheus job names; selecting or adjusting the correct job variable may be required.
- A successful `curl -I localhost:3000` response can validate Grafana even when a port listing is unclear.
- If APT cannot locate a package from a third-party repository, verify the repository file, signing key, and `apt-get update` output.
- QEMU Guest Agent depends on both the guest package and the Proxmox-provided virtio serial device.
- If `/dev/virtio-ports/org.qemu.guest_agent.0` is missing despite `agent: 1` being enabled, a full Proxmox stop/start may be required to recreate the VM hardware channel.
- A guest OS reboot is not always equivalent to a hypervisor-level power cycle.

### Remaining Work

- Build a custom Linux host dashboard for learning and portfolio polish.
- Add DNS availability checks and future Pi-hole metrics.
- Add Proxmox monitoring approach.
- Add alerting only after checks are documented and actionable.
- Add backup coverage for `mon01` once backup infrastructure is deployed.

## 2026-07-08 - Project 001: Pi-hole DNS Service

### Changed

- Deployed the first production-style infrastructure VM, `dns01`.
- Installed Debian 13.5 (Trixie) as a minimal headless server.
- Configured non-root administration with `sudo`.
- Installed and verified the QEMU Guest Agent for Proxmox integration.
- Configured a static IP for the DNS VM on the homelab LAN.
- Installed Pi-hole as the homelab DNS service.
- Selected Cloudflare as the initial upstream DNS provider.
- Added local DNS records for core homelab infrastructure.
- Verified DNS resolution from a separate client.
- Added service documentation for Pi-hole under `docs/services/pihole.md`.
- Added VM inventory documentation under `docs/architecture/vm-inventory.md`.
- Updated network architecture documentation to reflect the GL.iNet Opal as the homelab edge router.
- Updated router documentation to clarify that the household network is an upstream dependency, not managed lab infrastructure.

### Why

- Establish DNS as the first foundational homelab service.
- Provide readable internal names for infrastructure systems instead of relying on memorized IP addresses.
- Create a safer isolated lab design behind the GL.iNet Opal router without affecting the household network.
- Build practical skills in Linux administration, Proxmox VM deployment, static networking, DNS, and troubleshooting.
- Start documenting real services in a portfolio-ready format as soon as they become part of the environment.

### Lessons Learned

- Hardware virtualization may need to be explicitly enabled in firmware before Proxmox can start KVM-backed VMs.
- Debian installation behavior differs depending on whether a root password is configured; `sudo` access may need to be added manually.
- Minimal Debian installs may not include convenience tools such as `curl` by default.
- QEMU Guest Agent behavior depends on both the guest package and the Proxmox VM option being enabled.
- Static IP configuration can succeed while DNS resolution fails if resolver configuration is incomplete.
- Troubleshooting by layer is effective: verify gateway reachability, internet-by-IP, then DNS resolution.
- The GL.iNet Opal topology gives the homelab a useful isolation boundary while still depending on upstream Wi-Fi for internet access.

### Remaining Work

- Configure the GL.iNet Opal DHCP settings to hand out Pi-hole as DNS for homelab clients after stability is validated.
- Add a secondary DNS server before relying on Pi-hole for all homelab clients.
- Export Pi-hole configuration after meaningful DNS changes.
- Add monitoring for DNS availability and query health.
- Add VM backup coverage and restore testing once backup infrastructure is deployed.
- Consider Unbound as a future recursive DNS resolver project.

## 2026-07-07 - Architecture Decision Records

### Changed

- Added the Architecture Decision Records index under `docs/decisions/`.
- Added a standard ADR template.
- Added ADR-0001 documenting the decision to use the Lenovo ThinkPad E16 Gen 1 as the initial Proxmox host.
- Defined ADR naming, status values, and usage guidance.

### Why

- Preserve the reasoning behind meaningful infrastructure decisions.
- Make design tradeoffs clear for future maintenance and portfolio review.
- Establish a repeatable process for documenting future platform, networking, storage, monitoring, and security decisions.

### Lessons Learned

- Architecture decisions are more useful when they document context and tradeoffs, not just the final choice.
- The first Proxmox host decision is significant enough to preserve because it affects cost, power, noise, and growth options.
- ADRs help future readers understand why the lab evolved the way it did.

### Remaining Work

- Add ADRs for future router/firewall decisions.
- Add ADRs for VLAN segmentation when implemented.
- Add ADRs for monitoring, backup, and security platform choices.

## 2026-07-07 - Services Documentation Templates

### Changed

- Expanded the services documentation index under `docs/services/`.
- Added a standard service documentation template.
- Added a runbook template for repeatable procedures.
- Added a project template for larger service or infrastructure efforts.
- Defined service lifecycle states for planned, experimental, active, deprecated, and retired services.

### Why

- Create a consistent documentation pattern before deploying production-style homelab services.
- Make future service documentation easier to maintain and compare.
- Support operational practices such as validation, rollback planning, troubleshooting, monitoring, backups, and recovery.

### Lessons Learned

- Service documentation should cover operations and recovery, not just installation notes.
- Templates reduce the chance that future services miss important maintenance details.
- Larger service projects should track design decisions, risks, validation, and lessons learned separately from day-to-day service pages.

### Remaining Work

- Add service-specific runbooks as operational procedures are created.
- Link future service decisions to architecture decision records when appropriate.

## 2026-07-07 - Hardware Model Refinement

### Changed

- Updated hardware documentation to reflect actual deployed device models instead of generic placeholders.
- Documented the Lenovo ThinkPad E16 Gen 1 as the primary Proxmox host.
- Documented the TP-Link TL-SG108E Easy Smart Switch using stock firmware.
- Documented the GL.iNet GL-SFT1200 Opal as the current lab router using stock firmware.
- Reframed the desktop page as an administrative workstation without publishing personal workstation hardware details.

### Why

- Make the repository accurately represent the real homelab infrastructure.
- Keep public documentation specific enough to be useful while still avoiding serial numbers, management IPs, MAC addresses, and personal workstation details.
- Improve portfolio quality by documenting engineering tradeoffs behind hardware choices.

### Lessons Learned

- Real model names are useful and safe to publish when they do not expose personally identifying or secret information.
- Personal workstation specifications should be omitted unless they are directly relevant to the lab architecture.
- Business-class laptops can be a practical first Proxmox platform when power, noise, cost, and simplicity matter.

### Remaining Work

- Add sanitized switch port mapping after physical topology is finalized.
- Add VLAN documentation after segmentation is implemented.
- Revisit router/firewall design if the Opal no longer meets lab requirements.
- Add recovery and maintenance runbooks for core hardware.

## 2026-07-07 - Hardware Documentation

### Changed

- Added the hardware documentation index under `docs/hardware/`.
- Expanded the sanitized hardware inventory.
- Added managed switch documentation covering current role, management access, VLAN planning, and maintenance notes.
- Added router/firewall documentation covering current upstream dependency and future routing responsibilities.
- Added desktop workstation documentation covering administrative use, documentation workflow, and security considerations.
- Added primary virtualization server documentation covering the Proxmox host role, storage, networking, security, and recovery considerations.

### Why

- Establish a hardware baseline before adding more services and complex network changes.
- Make physical infrastructure roles clear enough for future troubleshooting.
- Keep public hardware documentation useful without exposing serial numbers, exact management addresses, or personally identifying details.

### Lessons Learned

- Hardware documentation should focus on operational role and architecture impact rather than raw device identifiers.
- Managed switching and Proxmox hosting are foundational enough to document before advanced services are deployed.
- Router/firewall documentation should distinguish current upstream dependency from future dedicated routing design.

### Remaining Work

- Add sanitized hardware specifications once device details are finalized.
- Document switch port mapping and VLAN assignments after segmentation is implemented.
- Document router/firewall platform decision once selected.
- Add hardware maintenance and recovery runbooks as the lab matures.

## 2026-07-07 - Architecture Documentation

### Changed

- Added the architecture documentation index under `docs/architecture/`.
- Expanded the high-level architecture overview.
- Documented the current network baseline, sanitized addressing model, and future segmentation plan.
- Documented the Proxmox virtualization strategy and workload categories.
- Documented storage assumptions, backup philosophy, and future NAS considerations.
- Documented monitoring goals, scope, alerting philosophy, and future observability direction.
- Documented security architecture, public documentation boundaries, management access, and security lab isolation goals.

### Why

- Create a clear architecture baseline before adding more hardware-specific and service-specific documentation.
- Make the repository more useful as both an operational reference and a public portfolio.
- Preserve the reasoning behind early design decisions while the lab is still simple enough to explain cleanly.

### Lessons Learned

- Architecture documentation should describe the intended operating model, not just list devices.
- Sanitized placeholders allow useful public documentation without exposing sensitive infrastructure details.
- Security lab work should be planned around isolation before offensive or intentionally vulnerable workloads are introduced.

### Remaining Work

- Document the hardware inventory and device roles.
- Add switch, router, desktop, and server documentation.
- Add service documentation templates and runbooks for future workloads.
- Create architecture decision records for major design choices.

## 2026-07-07 - Documentation Foundation

### Changed

- Added the initial public portfolio documentation structure.
- Expanded the repository README into a landing page.
- Added documentation standards, sanitization rules, roadmap, security policy, runbooks, service templates, and architecture decision records.

### Why

- Establish the GitHub repository as the source of truth for the homelab.
- Create a maintainable documentation foundation before starting larger infrastructure projects.
- Ensure public documentation is safe, sanitized, and resume-ready from the beginning.

### Lessons Learned

- Public infrastructure documentation needs explicit sanitization rules before detailed implementation notes are added.
- A strong structure early prevents the repo from becoming a collection of disconnected notes.

### Remaining Work

- Document the initial hardware inventory.
- Document the current network assumptions.
- Add the first real service or infrastructure project once implementation begins.
