# Project 004: Reverse Proxy and Internal HTTPS

## Status

| Area | Details |
| --- | --- |
| Status | Planned — next focus |
| Start date | Pending |
| Owner | Homelab administrator |
| Dependencies | Stable DNS, monitoring, Proxmox backup and recovery |
| Candidate technologies | NGINX Proxy Manager, NGINX, Caddy, or equivalent |

Project 004 begins only after Project 003 backup and recovery closeout. The required recovery foundation is now operational.

## Purpose

Provide friendly internal service names and trusted HTTPS for selected homelab web interfaces without exposing them publicly or turning the reverse proxy into an undocumented dependency.

The project should demonstrate:

- Reverse-proxy architecture.
- Internal DNS integration.
- TLS and certificate lifecycle management.
- Trust distribution.
- Service dependency analysis.
- Monitoring and recovery design.
- Security-conscious public documentation.

## Goals

- Select a reverse-proxy platform based on documented requirements.
- Deploy the proxy as a dedicated, monitored workload.
- Define a safe internal naming pattern.
- Provide HTTPS for selected internal services.
- Select and document an internal certificate-authority model.
- Define how trusted clients receive the CA certificate.
- Document certificate issuance, renewal, revocation, backup, and recovery.
- Monitor proxy availability and certificate expiration.
- Preserve direct administrative access for services where the proxy should not become the only recovery path.
- Keep exact internal names, addresses, private keys, and certificate secrets outside Git.

## Non-Goals

- Public internet exposure.
- Publishing the household domain, SSID, or exact internal namespace.
- Replacing service-native authentication.
- Placing every management interface behind the proxy automatically.
- Treating TLS as a substitute for network segmentation or access control.
- Deploying centralized identity before the new server and UPS projects are complete.

## Current Preconditions

Completed foundations:

- Pi-hole provides internal DNS and local records.
- `mon01` provides Prometheus, Grafana, and Blackbox Exporter.
- `pve01`, `dns01`, and `mon01` have Linux host monitoring.
- Recursive and local DNS probes are active.
- Daily VM backup coverage exists for stable infrastructure VMs.
- A representative Proxmox whole-VM restore has been validated.
- Proxmox management authentication has routine and break-glass recovery paths.

## Open Decisions

### Reverse-Proxy Platform

Evaluate:

- NGINX Proxy Manager.
- Native NGINX.
- Caddy.
- Another platform only when it offers a clear operational advantage.

Decision criteria:

- Ease of configuration and recovery.
- Internal certificate support.
- Automation and configuration portability.
- Security update process.
- Monitoring options.
- Resource requirements.
- Portfolio value and learning depth.
- Avoidance of unnecessary lock-in.

### Deployment Model

Choose between:

- Dedicated VM.
- Dedicated container.
- Another isolated deployment only with documented rationale.

The selected model must define:

- Host and operating system.
- Resource allocation.
- Storage and backup coverage.
- Network placement.
- Administrative access.
- Update and rollback procedure.

### Internal Naming

Define a sanitized public model such as:

```text
<SERVICE>.<PRIVATE_DNS>
```

Operational names must:

- Resolve only where intended.
- Avoid personal or location-based identifiers.
- Be documented privately when exact values matter.
- Avoid `.local` because of multicast DNS ambiguity.

### Certificate Authority and Trust

Evaluate:

- A locally managed private CA.
- A tool-integrated CA workflow.
- A public-domain DNS challenge only if ownership, privacy, and operational complexity justify it.

Document:

- Root and intermediate CA roles if applicable.
- Where private keys are stored.
- How client trust is distributed and removed.
- Certificate lifetime and renewal.
- Revocation or replacement procedure.
- Recovery after CA or proxy loss.
- Which artifacts are backed up and which remain offline.

## Candidate Initial Services

Potential services for internal HTTPS:

- Grafana.
- Prometheus, if browser access through the proxy provides a documented benefit.
- Pi-hole administration.
- Future internal applications.

Proxmox management requires separate risk review. It should not be placed behind the reverse proxy merely for consistency, and direct internal management access must remain available for recovery.

## Proposed Architecture

```text
Trusted client
    |
    | HTTPS to <SERVICE>.<PRIVATE_DNS>
    v
Internal reverse proxy
    |
    | HTTP or HTTPS on trusted internal network
    v
Selected backend service

Pi-hole
    `-- resolves internal proxy names

mon01
    `-- monitors proxy and certificate state
```

The exact backend addresses, names, ports, and trust artifacts remain private.

## Security Requirements

- Keep the proxy internal-only unless a separate future project explicitly changes that boundary.
- Do not publish private keys, certificate requests containing identifying values, tokens, or exact private DNS names.
- Preserve service authentication and authorization.
- Use least privilege for proxy administration and automation.
- Restrict backend access where practical so clients use intended paths without blocking emergency recovery.
- Define update responsibility and vulnerability response.
- Document header, protocol, and TLS settings that materially affect security.
- Protect CA keys more strongly than ordinary service certificates.
- Keep attacker-style workloads away from CA material and proxy administration.

## Backup and Recovery Requirements

Before the proxy becomes a dependency:

- Add the proxy workload to Proxmox backup coverage.
- Document proxy configuration locations and database state.
- Protect CA material and certificate configuration appropriately.
- Keep CA private keys outside the public repository.
- Define a manual rebuild path.
- Test restoration in an isolated environment.
- Preserve direct access to critical backends during proxy failure.
- Record certificate and trust recovery separately from VM recovery.

## Monitoring Requirements

At minimum, monitor:

- Proxy host availability.
- HTTPS endpoint availability for selected services.
- HTTP response status where meaningful.
- Certificate expiration.
- Certificate hostname validation.
- Proxy service state.
- Resource utilization.

Alerts should be added only when a response runbook and notification route exist.

## Validation Plan

### DNS

- Internal names resolve to the intended proxy address.
- Unintended networks do not receive private records where isolation is required.
- Existing recursive and local DNS probes remain healthy.

### HTTPS

- Trusted clients validate the certificate chain without warnings.
- Hostnames match certificate identities.
- Expired, wrong-host, or untrusted certificates fail as expected.
- HTTP behavior redirects or remains disabled according to the design.

### Proxy Routing

- Each hostname routes only to its intended backend.
- Backend authentication remains functional.
- WebSockets, redirects, and application-specific headers work where required.
- Direct recovery access remains available according to the service design.

### Monitoring

- Prometheus sees the proxy host or exporter target.
- Blackbox probes validate selected HTTPS endpoints.
- Certificate-expiration data is visible.
- Grafana displays useful status without exposing private names publicly.

### Recovery

- Proxy configuration can be restored or rebuilt.
- A temporary restored proxy can be tested without conflicting with production.
- Trust and certificate recovery procedures are understandable and complete.
- Backend services remain administrable during proxy failure.

## Documentation Deliverables

Project completion should update:

- Architecture overview.
- Network architecture.
- Security architecture.
- Monitoring architecture.
- VM inventory.
- Storage and backup documentation.
- Reverse-proxy service page.
- Certificate or PKI service page if separate.
- Backup and disaster-recovery runbooks.
- New proxy and certificate troubleshooting runbooks.
- ADR for platform and certificate-authority choices.
- Project changelog and dated change record.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Proxy becomes a single point of failure | Multiple service UIs become unavailable | Preserve direct recovery paths, monitor the proxy, back it up, and test restoration |
| CA private key is lost | New trusted certificates cannot be issued | Protect and back up CA material separately with documented recovery |
| CA private key is exposed | Trust boundary is compromised | Restrict access, rotate or rebuild the CA, and document revocation and re-trust procedures |
| Certificate renewal fails silently | Internal services show warnings or become inaccessible | Monitor expiration and document renewal ownership |
| DNS and proxy records drift | Names resolve to incorrect backends | Maintain a clear source of truth and validate after changes |
| Proxy hides backend problems | Users see proxy errors without root-cause clarity | Monitor proxy and backend layers separately |
| Unnecessary management proxying increases risk | Recovery becomes harder | Review each service individually and retain direct access where appropriate |

## Milestones

- [ ] Define requirements and select the reverse-proxy platform.
- [ ] Select VM or container deployment model.
- [ ] Define internal naming and DNS changes.
- [ ] Select the certificate-authority and trust model.
- [ ] Deploy and harden the proxy workload.
- [ ] Integrate the first backend service.
- [ ] Add HTTPS endpoint and certificate monitoring.
- [ ] Add backup coverage and private recovery assets.
- [ ] Complete isolated restore and certificate recovery testing.
- [ ] Update architecture, service, runbook, ADR, and changelog documentation.

## Related Documentation

- [Projects Index](README.md)
- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [Pi-hole](../services/pihole.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Project 003](project-003-backup-recovery.md)
- [Backup Runbook](../runbooks/backup.md)
- [Disaster Recovery](../runbooks/disaster-recovery.md)
- [Roadmap](../../ROADMAP.md)