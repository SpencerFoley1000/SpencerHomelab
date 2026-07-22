# Projects

This directory tracks meaningful homelab projects from planning through implementation and follow-up work.

Projects are stored as numbered Markdown files. Each page records its lifecycle status so the repository remains simple to navigate as it grows.

## Project Documentation Standard

Each project should include:

- Purpose
- Status
- Goals and scope
- Architecture impact
- Design decisions
- Implementation notes
- Testing and validation
- Security considerations
- Lessons learned
- Follow-up tasks

Use the [Project Template](TEMPLATE.md) when starting a new project.

## Current Projects

| Project | Status | Summary |
| --- | --- | --- |
| [Project 001: Pi-hole DNS Service](project-001-pihole-dns.md) | Completed | Deployed `dns01` and established Pi-hole as the first production-style homelab service. |
| [Project 002: Monitoring and Observability Stack](project-002-monitoring-observability.md) | Active — foundation complete | Four-host metrics, DNS and internal HTTPS probes, and operational dashboards are active; application/platform metrics and alerting remain follow-up work. |
| [Project 003: Backup and Recovery](project-003-backup-recovery.md) | Completed | Added dedicated backup storage, daily VM backups, tiered retention, and validated isolated restore paths. |
| [Project 004: Reverse Proxy and Internal HTTPS](project-004-reverse-proxy-internal-https.md) | Completed | Deployed `proxy01`, friendly internal names, private-CA HTTPS, endpoint and certificate monitoring, backup coverage, and isolated restore validation. |
| [Project 005: X299 Virtualization Server](project-005-x299-virtualization-server.md) | Completed | Built the dedicated server, transferred the existing Proxmox installation, restored production services, and added host thermal monitoring. |
| Project 006: Power Resilience and Graceful Shutdown | Planned | Install the UPS, monitor it, and implement orderly shutdown before centralized identity services. |
| Project 007: Active Directory and Centralized Identity | Planned | Deploy identity services only after power-protection controls are operational. |

## Project Status Values

| Status | Meaning |
| --- | --- |
| Planned | Approved future work that has not started |
| Active | Work is currently being implemented or validated |
| Completed | Intended scope is complete; follow-up improvements may remain |
| Paused | Work is intentionally deferred |
| Blocked | Work cannot proceed until a documented dependency is available |
| Retired | The project or resulting infrastructure is no longer active |

A project may be completed while clearly documented operational improvements remain. Follow-up work must not be mislabeled as completed validation.

## Related Documentation

- [Project Template](TEMPLATE.md)
- [Architecture Documentation](../architecture/)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Runbooks](../runbooks/)
- [Architecture Decision Records](../decisions/)
- [Infrastructure Change Records](../changes/)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
