# VM Provisioning Runbook

## Purpose

Provide a repeatable process for creating and documenting new virtual machines.

## Preconditions

- Hypervisor is installed and reachable through a safe management path.
- Network and storage targets are defined.
- Required ISO images or templates are available.
- Secrets are stored outside this repository.

## Procedure

1. Define the VM purpose.
2. Select the appropriate network segment.
3. Allocate CPU, memory, and disk based on workload needs.
4. Install the operating system.
5. Apply updates.
6. Configure hostname and baseline access.
7. Configure monitoring and backups, if applicable.
8. Document the VM in the relevant service, project, or architecture page.
9. Add a changelog entry for meaningful infrastructure changes.

## Validation

- VM boots successfully.
- Network connectivity works as expected.
- Management access is restricted appropriately.
- Backups are configured if the VM stores important state.
- Documentation has been updated.

## Related Documentation

- [Virtualization Architecture](../architecture/virtualization.md)
- [Network Architecture](../architecture/network.md)
