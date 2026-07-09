# Services

This directory documents homelab services and service-like infrastructure components.

A service should receive documentation when it becomes part of the environment, supports another system, stores data, requires maintenance, exposes a network endpoint, or represents a meaningful experiment worth preserving.

## Purpose

Service documentation exists to answer practical operational questions:

- What does the service do?
- Where does it run?
- How was it deployed?
- What does it depend on?
- How is it secured?
- How is it backed up?
- How would it be restored?
- What should be checked when it breaks?

## Documentation Standard

Use [Service Template](TEMPLATE.md) when adding a new service.

Each service should document, when applicable:

- Purpose
- Technology stack
- Host
- Operating system
- Deployment method
- Dependencies
- Networking
- Storage
- Backup strategy
- Recovery procedure
- Monitoring
- Security considerations
- Maintenance notes
- Future improvements

## Service Lifecycle

| State | Meaning |
| --- | --- |
| Planned | Service is being considered but is not deployed |
| Experimental | Service is deployed for testing and may be rebuilt or removed |
| Active | Service is intentionally part of the lab environment |
| Deprecated | Service is still present but planned for replacement or removal |
| Retired | Service has been removed and retained only for historical reference |

Experimental services should be clearly labeled so future readers do not confuse temporary work with stable infrastructure.

## Naming Guidance

Service pages should use clear, lowercase filenames:

```text
<service-name>.md
```

Examples:

- `dns.md`
- `monitoring.md`
- `docker.md`
- `backup.md`
- `pihole.md`

Avoid filenames that include secrets, internal-only names, personal identifiers, or exact hostnames that should not be public.

## Current Services

| Service | State | Host | Purpose | Documentation |
| --- | --- | --- | --- | --- |
| Pi-hole | Active | `dns01` | Internal DNS, local DNS records, and DNS-based blocking for the homelab LAN | [pihole.md](pihole.md) |
| Node Exporter | Active | `mon01`, `dns01` | Linux host metrics exporter for Prometheus | [node-exporter.md](node-exporter.md) |
| Prometheus | Active | `mon01` | Metrics scraping, storage, and PromQL querying | [prometheus.md](prometheus.md) |
| Grafana | Active | `mon01` | Dashboarding and visualization for Prometheus metrics | [grafana.md](grafana.md) |

## Planned Candidates

Future service candidates may include:

- DNS availability monitoring
- Pi-hole metrics integration
- Backup tooling
- Container hosting
- Reverse proxy and internal TLS
- Security lab services
- Automation tooling

## Templates

- [Service Template](TEMPLATE.md)
- [Runbook Template](RUNBOOK_TEMPLATE.md)
- [Project Template](PROJECT_TEMPLATE.md)

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
