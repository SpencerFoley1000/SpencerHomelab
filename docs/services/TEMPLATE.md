# Service Name

## Purpose

Explain what this service does, why it exists in the homelab, and what operational value it provides.

## Current Status

| Area | Details |
| --- | --- |
| Status | Planned / Experimental / Active / Deprecated / Retired |
| Owner | Homelab administrator |
| Criticality | Low / Medium / High |
| Environment | Homelab |
| Documentation state | Draft / Current / Needs review |

## Technology Stack

| Component | Value |
| --- | --- |
| Application | Service name |
| Version | Version or release channel |
| Host | Hostname or role |
| Operating system | OS name |
| Deployment method | Package / Docker / VM / LXC / Script / Other |
| Data location | Sanitized storage label |

## Dependencies

List anything required for the service to work.

Examples:

- DNS
- DHCP
- Database
- Reverse proxy
- Storage mount
- Authentication provider
- Network segment
- Backup target

## Networking

| Area | Details |
| --- | --- |
| Network segment | Sanitized network label |
| Addressing | Sanitized address or placeholder |
| DNS name | Internal DNS name or placeholder |
| Ports | Required ports |
| External access | None / VPN only / Public / Other |

Avoid publishing sensitive addresses, account details, or full firewall exports.

## Storage

Document where the service stores important data.

| Data Type | Location | Backup Required | Notes |
| --- | --- | --- | --- |
| Configuration | Sanitized config path | Yes / No |  |
| Application data | Sanitized data path | Yes / No |  |
| Logs | Sanitized log path | Optional |  |

## Backup Strategy

Document what must be backed up and how recovery would work.

- Backup scope:
- Backup destination:
- Backup frequency:
- Retention:
- Restore tested: Yes / No / Pending
- Last restore test:

A backup that has never been restored should be treated as unproven.

## Recovery Procedure

High-level recovery steps:

1. Confirm the failure scope.
2. Restore or rebuild the host if required.
3. Restore service configuration.
4. Restore application data.
5. Validate the service is reachable.
6. Confirm dependent services are functioning.
7. Document lessons learned.

Link to a dedicated runbook if the process becomes detailed.

## Monitoring

Document how service health is checked.

- Uptime check:
- Metrics:
- Logs:
- Alerts:
- Dashboard:

## Security Considerations

Document practical controls and risks.

- Authentication method:
- Authorization model:
- Network exposure:
- Sensitive value storage location, using a placeholder only:
- Update process:
- Known risks:

Do not commit sensitive values or sensitive configuration exports.

## Maintenance Notes

Include routine maintenance tasks.

- Update process:
- Configuration review:
- Backup validation:
- Log review:
- Certificate renewal if applicable:

## Validation

Use this section to record how the service was tested.

Examples:

- Confirmed service starts after reboot.
- Confirmed DNS name resolves.
- Confirmed web UI loads internally.
- Confirmed backup job completes.
- Confirmed restore process works.

## Troubleshooting

Common checks:

- Is the host online?
- Is the service process or container running?
- Are required ports listening?
- Is DNS resolving correctly?
- Is storage mounted and writable?
- Are logs showing errors?

## Future Improvements

- Add monitoring.
- Add backup validation.
- Add automation.
- Improve network segmentation.
- Add recovery runbook.

## Related Documentation

- [Services README](README.md)
- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Storage Architecture](../architecture/storage.md)
- [Security Architecture](../architecture/security.md)
