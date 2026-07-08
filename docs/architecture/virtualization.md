# Virtualization Architecture

This page documents the virtualization design for the homelab.

## Current Status

Status: Planned / baseline documentation pending.

## Goals

- Provide a flexible platform for running infrastructure services and lab workloads.
- Keep stable services separated from experimental systems.
- Practice VM lifecycle management, resource planning, backups, and recovery.
- Document operational decisions in a way that is useful for future troubleshooting.

## Topics to Document

- Hypervisor platform
- Host hardware roles
- VM naming conventions
- Resource allocation strategy
- Storage layout
- Network bridge / VLAN configuration
- Backup and restore process
- Maintenance and update process

## Security Considerations

- Separate attacker/security lab workloads from trusted infrastructure.
- Avoid exposing management interfaces broadly.
- Document management access using placeholders rather than sensitive endpoint details.

## Related Documentation

- [Network Architecture](network.md)
- [Storage Architecture](storage.md)
- [Hardware Inventory](../hardware/inventory.md)
- [VM Provisioning Runbook](../runbooks/vm-provisioning.md)
