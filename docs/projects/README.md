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
| [Project 002: Monitoring and Observability Stack](project-002-monitoring-observability.md) | Active | Deployed `mon01`, Prometheus, Grafana, Node Exporter, Blackbox Exporter, host metrics, and DNS availability monitoring. |
| Project 003: Backup and Recovery | Planned | Define backup targets, retention, recovery priorities, and tested restore procedures. |

## Project Status Values

| Status | Meaning |
| --- | --- |
| Planned | Approved future work that has not started |
| Active | Work is currently being implemented or validated |
| Completed | Intended project scope is complete; follow-up improvements may remain |
| Paused | Work is intentionally deferred |
| Retired | The project or resulting infrastructure is no longer active |

## Related Documentation

- [Project Template](TEMPLATE.md)
- [Architecture Documentation](../architecture/)
- [Services Documentation](../services/)
- [Runbooks](../runbooks/)
- [Architecture Decision Records](../decisions/)
- [Roadmap](../../ROADMAP.md)
- [Changelog](../../CHANGELOG.md)
