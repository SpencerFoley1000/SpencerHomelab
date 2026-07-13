# VM Provisioning Runbook

## Purpose

Provide a repeatable baseline for creating, validating, monitoring, documenting, and recovering new virtual machines.

## Status

| Area | Details |
| --- | --- |
| Lifecycle | Baseline checklist |
| Validation | Individual steps exercised through `dns01` and `mon01`; full standardized workflow still maturing |
| Last reviewed | 2026-07-12 |

## Preconditions

- The hypervisor is healthy and reachable through a trusted management path.
- The VM purpose, owner, lifecycle state, and expected dependencies are defined.
- Required CPU, memory, disk, and network resources are available.
- Network and storage placement are selected.
- Required ISO images or templates are available and trusted.
- Naming follows the repository convention.
- Secrets are stored outside the repository.
- Backup and recovery expectations are defined before stable service state is created.
- Experimental or intentionally vulnerable systems have an approved isolation plan.

## Planning Record

Before creation, document:

| Item | Required decision |
| --- | --- |
| Hostname | Sanitized role-based name such as `<role><number>` |
| Purpose | Clear service or project role |
| Lifecycle | Planned, experimental, active, or temporary |
| Host placement | Current Proxmox node |
| vCPU and memory | Conservative initial allocation with expected growth |
| Disk | Size, storage pool, and whether state is rebuildable |
| Network | Stable service network, management network, or isolated lab segment |
| Addressing | DHCP, reservation, or static configuration |
| DNS | Required local records |
| Monitoring | Host, service, application, and platform checks |
| Backup | VM backup, application export, rebuild-only, or disposable |
| Recovery priority | High, medium, low, or disposable |
| Security | Access model, exposure, firewall requirements, and isolation |

## Procedure

1. Define the VM purpose and architecture impact.
2. Select a safe role-based hostname.
3. Confirm host capacity in Prometheus and Grafana.
4. Select the appropriate network and storage placement.
5. Allocate CPU, memory, and disk conservatively.
6. Create the VM using sanitized internal notes for VM IDs, MAC addresses, and storage identifiers.
7. Install the operating system from a trusted source.
8. Apply operating-system updates.
9. Configure hostname, time synchronization, and baseline administrative access.
10. Configure network addressing and resolver behavior.
11. Install QEMU Guest Agent when supported.
12. Apply service-specific packages and configuration.
13. Configure host monitoring before the VM is considered stable infrastructure.
14. Add service-level monitoring where the VM exposes a critical network service.
15. Configure backup or explicitly document why the VM is disposable or rebuild-only.
16. Add the VM to the [VM Inventory](../architecture/vm-inventory.md).
17. Create or update service, architecture, project, ADR, and runbook documentation.
18. Add a changelog entry for meaningful infrastructure changes.

## Validation

### Hypervisor and Guest Integration

- VM starts and stops cleanly.
- Allocated CPU, memory, and disk match the plan.
- QEMU Guest Agent reports correctly where installed.
- No unexpected virtual hardware is attached.

### Network

- The VM has the intended address assignment.
- Gateway reachability works.
- Internet-by-IP works when required.
- DNS resolution works.
- Required local DNS records exist.
- Management access is restricted to trusted paths.
- No duplicate address or hostname exists.

### Service

- Required systemd services are active and enabled.
- Intended network endpoints respond.
- Logs show no unresolved startup failure.
- The service survives a reboot when appropriate.

### Monitoring

For Linux hosts using Node Exporter:

```promql
up{job="node_exporter", host="<HOSTNAME>"}
```

Confirm:

- Prometheus target state is `UP`.
- Expected host and role labels exist.
- Grafana displays current data.
- Service probes or application metrics answer a defined operational question.

### Backup and Recovery

- Backup method is documented.
- Application export requirements are documented.
- Recovery priority is recorded.
- Stable workloads are included in Project 003 or a successor backup process.
- A new VM is not described as fully protected until backup and restore validation exists.

### Documentation

- VM inventory entry exists.
- Service or project page exists.
- Network, storage, monitoring, and security implications are reflected where applicable.
- Changelog entry exists for meaningful deployment.
- Sensitive values are sanitized.
- Markdown link validation passes.

## Rollback

If provisioning fails before the VM stores unique state:

1. Preserve relevant logs and lessons learned.
2. Remove or disable incomplete DNS records, monitoring targets, and firewall rules.
3. Delete the failed VM only after confirming no required state exists.
4. Update documentation to record the failed approach when useful.
5. Re-provision from a corrected plan.

If the VM already contains important state:

- Do not delete it as routine cleanup.
- Isolate it if necessary.
- Preserve available configuration or application exports.
- Use the documented backup or recovery path.
- Record the incident and corrective action.

## Security Considerations

- Do not publish exact addresses, VM IDs, MAC addresses, usernames, or secrets.
- Avoid default credentials.
- Use least privilege for service and administrative identities.
- Keep management interfaces internal-only.
- Place intentionally vulnerable workloads on isolated networks.
- Review privileged containers, passthrough, nested virtualization, and unusual device access before enabling them.
- Do not add broad firewall rules before testing the required path.

## Future Improvements

- Create a standard Debian VM template after the baseline is stable and understood.
- Add automated configuration checks without hiding the underlying process.
- Add standardized cloud-init only after manual provisioning assumptions are documented.
- Add tested backup onboarding after Project 003.
- Add explicit VLAN and firewall onboarding after segmentation.
- Add a decommissioning runbook.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Network Architecture](../architecture/network.md)
- [Storage Architecture](../architecture/storage.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Adding a Service](adding-service.md)
- [QEMU Guest Agent Troubleshooting](qemu-guest-agent-troubleshooting.md)
