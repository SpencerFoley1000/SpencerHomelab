# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the homelab.

ADRs document meaningful infrastructure decisions, the context behind them, alternatives considered, and the tradeoffs accepted. They are written for future maintainers and for portfolio readers who want to understand the engineering reasoning behind the lab.

## Purpose

Use ADRs to explain why an important decision was made.

Examples:

- Choosing Proxmox as the virtualization platform.
- Choosing a business laptop as the first virtualization host.
- Choosing a router/firewall platform.
- Introducing VLAN segmentation.
- Selecting a monitoring stack.
- Selecting a backup strategy.
- Changing DNS or DHCP architecture.
- Introducing security lab isolation.

## When to Create an ADR

Create an ADR when a decision:

- Affects architecture or operations long term.
- Introduces a new platform or core dependency.
- Changes networking, storage, backup, monitoring, or security design.
- Has meaningful tradeoffs.
- Would be hard to understand six months later without context.
- Might be interesting to a future employer reviewing the repository.

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

## Template

Use [ADR Template](ADR_TEMPLATE.md) when creating a new decision record.

## Related Documentation

- [Architecture Overview](../architecture/overview.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Hardware Documentation](../hardware/)
- [Services Documentation](../services/)
