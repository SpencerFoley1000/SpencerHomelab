# Changelog

This changelog records meaningful infrastructure, documentation, and process changes in reverse chronological order.

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
