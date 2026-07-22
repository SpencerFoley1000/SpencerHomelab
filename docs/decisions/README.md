# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the homelab.

ADRs document meaningful infrastructure decisions, the context behind them, alternatives considered, and the tradeoffs accepted. They are written for future maintainers and portfolio readers who want to understand the engineering reasoning behind the lab.

## Purpose

Use ADRs to explain why an important decision was made.

Examples:

- Choosing Proxmox as the virtualization platform.
- Choosing the initial virtualization host.
- Choosing a router or firewall platform.
- Introducing VLAN segmentation.
- Selecting a monitoring stack.
- Selecting a backup strategy.
- Changing DNS or DHCP architecture.
- Introducing security-lab isolation.

## When to Create an ADR

Create an ADR when a decision:

- Affects architecture or operations long term.
- Introduces a new platform or core dependency.
- Changes networking, storage, backup, monitoring, or security design.
- Has meaningful tradeoffs.
- Would be hard to understand six months later without context.
- Demonstrates useful engineering reasoning to a portfolio reviewer.

Do not create ADRs for minor edits, temporary experiments, typo fixes, or routine maintenance unless they reveal an important design lesson.

## Naming Convention

Use sequential numbering:

```text
ADR-0001-short-decision-title.md
ADR-0002-short-decision-title.md
ADR-0003-short-decision-title.md
```

Keep filenames lowercase after the ADR number and use hyphens between words.

## ADR Status Values

| Status | Meaning |
| --- | --- |
| Proposed | Decision is being considered but not finalized |
| Accepted | Decision is currently in effect |
| Superseded | Decision was replaced by a newer ADR |
| Deprecated | Decision remains documented but should not be used for new work |
| Retired | Decision applied to infrastructure that no longer exists |

## Current ADRs

| ADR | Status | Topic |
| --- | --- | --- |
| [ADR-0001](ADR-0001-proxmox-on-thinkpad-e16.md) | Accepted | Use Lenovo ThinkPad E16 Gen 1 as the initial Proxmox host |
| [ADR-0005](ADR-0005-migrate-pve01-to-x299-server.md) | Accepted | Migrate `pve01` from the ThinkPad to the dedicated X299 server |
| [ADR-0002](ADR-0002-prometheus-grafana-monitoring-stack.md) | Accepted | Use Prometheus, Grafana, Node Exporter, and Blackbox Exporter for monitoring |
| [ADR-0003](ADR-0003-direct-attached-proxmox-backup-storage.md) | Accepted | Use direct-attached ext4 Proxmox backup storage with layered recovery assets |
| [ADR-0004](ADR-0004-internal-reverse-proxy-and-private-ca.md) | Accepted | Use NGINX Proxy Manager with a private internal certificate authority |

## Template

Use [ADR Template](ADR_TEMPLATE.md) when creating a new decision record.

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
- [Projects](../projects/)
- [Infrastructure Change Records](../changes/)
