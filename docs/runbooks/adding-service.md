# Adding a Service Runbook

## Purpose

Provide a repeatable process for deploying and documenting a new homelab service.

## Procedure

1. Define the service purpose and expected users.
2. Decide whether the service is production-like or experimental.
3. Choose deployment method.
4. Identify dependencies.
5. Define networking and exposure.
6. Define storage and backup needs.
7. Configure authentication and access controls.
8. Deploy the service.
9. Validate functionality.
10. Create or update the service documentation page.
11. Add a changelog entry.
12. Update the roadmap if the service completes a planned item.
13. Create an ADR if the service choice represents a major architectural decision.

## Documentation Checklist

- [ ] Service page created from template.
- [ ] Ports and exposure documented using sanitized values.
- [ ] Backup strategy documented.
- [ ] Recovery steps documented.
- [ ] Security considerations documented.
- [ ] Changelog updated.

## Related Documentation

- [Service Template](../services/templates/service-template.md)
- [Security Architecture](../architecture/security.md)
