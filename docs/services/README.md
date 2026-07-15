# Services

This directory documents homelab services and service-like infrastructure components.

A service receives documentation when it becomes part of the environment, supports another system, stores important state, requires maintenance, exposes a network endpoint, or represents an experiment worth preserving.

## Purpose

Service documentation should answer:

- What does the service do?
- Where does it run?
- How was it deployed?
- What does it depend on?
- How is it secured?
- How is it monitored?
- How is it backed up?
- How would it be recovered?
- What should be checked when it fails?

## Documentation Standard

Use the [Service Template](TEMPLATE.md) for new services.

Each page should cover, when applicable:

- Purpose
- Technology stack
- Host and operating system
- Deployment method
- Dependencies
- Networking
- Storage and state
- Monitoring
- Security considerations
- Backup strategy
- Recovery procedure
- Maintenance notes
- Future improvements

## Service Lifecycle

| State | Meaning |
| --- | --- |
| Planned | Under consideration but not deployed |
| Experimental | Deployed for testing and may be rebuilt or removed |
| Active | Intentionally part of the environment |
| Deprecated | Present but planned for replacement or removal |
| Retired | Removed and retained only for historical reference |

Experimental services must be labeled clearly so temporary work is not mistaken for stable infrastructure.

## Current Services and Platforms

| Service / Platform | State | Host or scope | Purpose | Documentation |
| --- | --- | --- | --- | --- |
| Proxmox VE | Active | `pve01` | Virtualization platform for homelab workloads | [proxmox.md](proxmox.md) |
| Pi-hole | Active | `dns01` | Internal DNS, local records, and DNS filtering | [pihole.md](pihole.md) |
| Node Exporter | Active | `mon01`, `dns01`, `pve01`, `proxy01` | Linux host and hypervisor-OS metrics | [node-exporter.md](node-exporter.md) |
| Prometheus | Active | `mon01` | Metrics scraping, storage, target health, and PromQL | [prometheus.md](prometheus.md) |
| Grafana | Active | `mon01` | Detailed and summary dashboards for host, DNS, HTTPS, and certificate metrics | [grafana.md](grafana.md) |
| Blackbox Exporter | Active | `mon01` | Recursive DNS, local DNS, internal HTTPS, and certificate-expiration probes | [blackbox-exporter.md](blackbox-exporter.md) |
| NGINX Proxy Manager | Active | `proxy01` | Internal reverse proxy and TLS termination for selected services | [nginx-proxy-manager.md](nginx-proxy-manager.md) |

## Current Monitoring Coverage

- Host metrics for `mon01`, `dns01`, `pve01`, and `proxy01`.
- Recursive public-name DNS probe through `dns01`.
- Local-record DNS probe independent of upstream recursion.
- Internal HTTPS probes for Grafana and Pi-hole.
- Certificate-expiration metrics for proxied services.
- Detailed imported Node Exporter dashboard.
- Homelab Service Health dashboard.
- Homelab Infrastructure Overview dashboard.

## Planned Candidates

- Pi-hole application metrics.
- Proxmox platform-specific metrics.
- Backup-health monitoring.
- Alertmanager and notification routing.
- Identity services.
- Container hosting beyond the dedicated proxy workload.
- Security monitoring and detection services.
- Automation tooling.

## Naming Guidance

Use clear lowercase filenames:

```text
<service-name>.md
```

Avoid filenames containing secrets, personal identifiers, exact addresses, or internal-only names that should not be public.

## Templates

- [Service Template](TEMPLATE.md)
- [Runbook Template](../runbooks/TEMPLATE.md)
- [Project Template](../projects/TEMPLATE.md)

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
