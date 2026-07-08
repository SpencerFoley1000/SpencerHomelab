# Architecture Overview

## Purpose

This document describes the overall homelab architecture at a high level. It is intended to help future maintainers understand what the lab is, why it exists, and how the major infrastructure pieces relate to each other.

The homelab is designed as a production-style learning environment for systems administration, networking, virtualization, automation, monitoring, and security engineering.

## Current Architecture Summary

The current environment is built around:

- A primary Proxmox virtualization host.
- A managed switch for wired lab connectivity.
- Existing upstream home internet connectivity.
- A staged plan for routing, segmentation, monitoring, services, and security tooling.

Sensitive implementation details are intentionally generalized. Exact IP addresses, public IP information, SSIDs, serial numbers, and account-specific information should not be committed to this repository.

## Design Goals

- Provide a realistic environment for entry-level IT, systems administration, and security practice.
- Keep infrastructure understandable enough to troubleshoot without relying on memory.
- Document decisions in a way that demonstrates engineering thought process.
- Build gradually, starting with a stable hardware and network foundation.
- Support future projects such as monitoring, backup validation, service hosting, and security lab work.

## Operating Model

The homelab should be treated like a small production environment:

- Changes should be documented before they are considered complete.
- Permanent infrastructure changes should be reflected in GitHub.
- Secrets and personally identifying information must be stored outside the repository.
- Experimental services should be clearly labeled as experimental.
- Recovery steps should be documented for important systems.

## Major Components

| Component | Role | Documentation |
| --- | --- | --- |
| Network | Provides connectivity, addressing, and future segmentation | [Network](network.md) |
| Virtualization | Runs lab workloads using Proxmox | [Virtualization](virtualization.md) |
| Storage | Provides local VM storage and future backup targets | [Storage](storage.md) |
| Monitoring | Tracks health, availability, and performance | [Monitoring](monitoring.md) |
| Security | Defines baseline controls and safe public documentation practices | [Security](security.md) |

## Current Assumptions

- The lab currently depends on existing home internet connectivity.
- Early network design prioritizes simplicity while leaving room for VLANs and dedicated routing later.
- Proxmox is the primary virtualization platform.
- Documentation is sanitized because the repository is public.
- Hardware and service documentation will be expanded as each component is configured.

## Future Improvements

- Add a detailed logical network diagram.
- Document VLANs after segmentation is implemented.
- Add service dependency maps as services come online.
- Add recovery procedures for core infrastructure.
- Add architecture decision records for major design choices.

## Related Documentation

- [Network Architecture](network.md)
- [Virtualization Architecture](virtualization.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Architecture Decision Records](../decisions/)
