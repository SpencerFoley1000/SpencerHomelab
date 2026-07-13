# Projects

This directory tracks meaningful homelab projects from planning through implementation and follow-up work.

Projects are stored as numbered Markdown files in this directory. Each project page records its own lifecycle status so the repository remains simple to navigate as it grows.

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
| [Project 002: Monitoring and Observability Stack](project-002-monitoring-observability.md) | Active — foundation complete | Three-host metrics, recursive and local DNS probes, and operational dashboards are active; application/platform metrics and alerting remain follow-up work. |
| [Project 003: Backup and Recovery](project-003-backup-recovery.md) | Active | Phase 003A recovery inventory is complete; the 5 TB backup target, VM backups, retention, and restore testing remain. |
| Project 004: Reverse Proxy and Internal HTTPS | Planned | Add friendly internal names, reverse proxying, and internal TLS after Project 003 backup implementation. |
| Infrastructure Milestone: Future Virtualization Server | Acquired / pre-deployment | Assemble and validate the X299 server before deciding its production role. |
| Project 005: Power Resilience and Graceful Shutdown | Planned | Measure power, select a UPS, monitor it, and implement orderly shutdown before centralized identity services. |
| Project 006: Active Directory and Centralized Identity | Planned | Deploy identity services only after the new server and power-protection controls are operational. |

## Project Status Values

| Status | Meaning |
| --- | --- |
| Planned | Approved future work that has not started |
| Active | Work is currently being implemented or validated |
| Completed | Intended project scope is complete; follow-up improvements may remain |
| Paused | Work is intentionally deferred |
| Blocked | Work is approved but cannot proceed until a documented dependency is available |
| Retired | The project or resulting infrastructure is no longer active |

## Related Documentation

- [Project Template](TEMPLATE.md)
- [Architecture Documentation](../architecture/)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Runbooks](../runbooks/)
- [Architecture Decision Records](../decisions/)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
