# Adding a Service Runbook

## Purpose

Provide a repeatable process for deploying and documenting a new homelab service.

## Status

Operational checklist

## Preconditions

- The service has a defined purpose and intended users.
- Required network, storage, and host capacity are understood.
- Credentials and sensitive values will be stored outside the repository.
- The impact on existing services has been considered.

## Procedure

1. Define the service purpose and expected users.
2. Decide whether the service is production-like or experimental.
3. Choose the deployment method.
4. Identify dependencies.
5. Define networking and exposure.
6. Define storage and backup needs.
7. Configure authentication and access controls.
8. Deploy the service.
9. Validate functionality and expected failure behavior.
10. Create or update the service documentation page.
11. Add or update monitoring where the service is operationally important.
12. Add a changelog entry.
13. Update the roadmap if the service completes or advances a planned item.
14. Create an ADR if the service choice represents a major architectural decision.

## Validation

- The service starts successfully after deployment.
- Required ports or endpoints are reachable only from intended networks.
- Dependencies continue to function.
- Monitoring confirms the expected service state where applicable.
- Backup and recovery expectations are documented.
- Public documentation contains no sensitive values.

## Rollback

- Stop or remove the new service if it creates instability.
- Restore any changed configuration from a known-good backup.
- Confirm dependent services return to their previous state.
- Document the failed approach and lessons learned if the attempt produced useful information.

## Documentation Checklist

- [ ] Service page created from the service template.
- [ ] Ports and exposure documented using sanitized values.
- [ ] Dependencies documented.
- [ ] Backup strategy documented.
- [ ] Recovery steps documented.
- [ ] Monitoring approach documented.
- [ ] Security considerations documented.
- [ ] Changelog updated.
- [ ] Roadmap updated if applicable.
- [ ] ADR created if the choice has long-term architectural impact.

## Related Documentation

- [Service Template](../services/TEMPLATE.md)
- [Runbook Template](TEMPLATE.md)
- [Security Architecture](../architecture/security.md)
- [Documentation Standard](../../DOCS_STYLE.md)
