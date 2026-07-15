# ADR-0004: Use NGINX Proxy Manager with a Private Internal Certificate Authority

## Status

Accepted

## Date

2026-07-14

## Context

The homelab needed memorable internal service names and trusted HTTPS for selected browser-based services without exposing those services publicly.

Requirements:

- Keep the reverse proxy internal-only.
- Preserve native backend authentication.
- Keep direct administrative access available during proxy failure.
- Avoid making Proxmox management depend on the proxy.
- Use a naming model that is safe for a private home network and public documentation.
- Support trusted HTTPS without purchasing a public domain or exposing DNS challenges.
- Separate the root certificate-authority key from the proxy workload.
- Monitor both service availability and certificate expiration.
- Protect proxy state through the existing Proxmox backup architecture.
- Provide a documented manual rebuild and CA replacement path.

The lab already had Pi-hole local DNS, Prometheus, Grafana, Blackbox Exporter, and tested Proxmox backup and restore procedures. A dedicated proxy VM could therefore be integrated as another monitored and recoverable infrastructure workload.

## Decision

Deploy NGINX Proxy Manager on a dedicated Debian VM named `proxy01` using Docker Compose.

Use:

- `lab.home.arpa` as the generic internal namespace.
- Pi-hole local DNS records pointing selected service names to `<PROXY01_IP>`.
- A private root CA generated on a trusted administrative workstation.
- A wildcard service certificate for `*.lab.home.arpa` and `lab.home.arpa`.
- The root CA private key stored off `proxy01` and encrypted with a passphrase.
- Only the wildcard service certificate and its private key imported into NGINX Proxy Manager.
- HTTPS proxying for Grafana and Pi-hole administration as the first services.
- Native backend authentication with no additional NGINX Proxy Manager access-list authentication layer.
- Direct backend access retained for emergency recovery.
- No reverse proxying of Proxmox management.
- Node Exporter for `proxy01` host monitoring.
- Blackbox Exporter HTTPS probes for endpoint availability and certificate expiration.
- Daily Proxmox VM backup coverage and isolated restore validation.

The NGINX Proxy Manager administration interface remains internal and is not forwarded through the edge router.

## Rationale

### Dedicated VM

A dedicated VM provides a clear security, monitoring, backup, and recovery boundary. It avoids placing the proxy on `dns01` or `mon01` and keeps application failure from directly sharing an operating-system role with DNS or monitoring.

### NGINX Proxy Manager

NGINX Proxy Manager provides a practical interface for learning reverse-proxy concepts while retaining visible NGINX behavior, persistent configuration, and a straightforward Docker Compose recovery model.

It reduces manual configuration overhead for the first implementation without preventing later migration to native NGINX, Caddy, or configuration-as-code.

### `home.arpa` Namespace

`home.arpa` is intended for non-unique private home-network naming. Using `lab.home.arpa` avoids multicast-DNS ambiguity associated with `.local` and avoids presenting an invented public domain as globally valid.

### Private CA

A private CA provides trusted HTTPS without public exposure, public DNS ownership, or ACME DNS challenge credentials.

Keeping the root CA private key off the proxy limits the impact of proxy compromise. The proxy can serve certificates but cannot issue arbitrary new certificates.

### Wildcard Service Certificate

A wildcard certificate simplifies initial deployment across a small number of internal services while preserving hostname validation.

The tradeoff is a shared private key across the proxied names. The design should move to per-service certificates if service count, isolation requirements, or automation maturity justify the additional lifecycle work.

### Preserve Direct Access

The proxy is a convenience and security layer, not the only recovery path. Direct backend access reduces the chance that one proxy failure blocks troubleshooting of DNS or monitoring.

Proxmox management remains outside the proxy because recovery of the virtualization platform must not depend on an optional guest workload.

## Alternatives Considered

| Alternative | Reason not chosen |
| --- | --- |
| Native NGINX configuration | Greater manual control but more configuration and certificate-lifecycle work than needed for the first implementation |
| Caddy | Strong automatic HTTPS workflow, but the project prioritized the NGINX ecosystem and a visible administrative interface for the initial deployment |
| Public domain with DNS-01 ACME | Requires domain ownership, external DNS integration, API credentials, and additional privacy and recovery considerations |
| Self-signed certificate per service | Does not provide a reusable trust hierarchy and increases client trust-management work |
| Root CA key stored on `proxy01` | A proxy compromise could become a certificate-issuing compromise |
| Proxy every management interface | Increases dependency and recovery complexity without a clear benefit |
| Host the proxy on `dns01` | Combines unrelated DNS and proxy failure domains |
| Host the proxy on `mon01` | Monitoring should observe the proxy from a separate system rather than share its operating-system failure domain |
| Public exposure with router port forwarding | Outside current project scope and inconsistent with the internal-only security boundary |

## Consequences

### Positive

- Selected services now use memorable internal names.
- Trusted clients can validate HTTPS without browser warnings.
- TLS termination and backend routing are centralized.
- DNS, proxy, backend, and monitoring responsibilities remain separated.
- The root CA signing key is not stored on the proxy.
- Service and certificate state are monitored independently of host metrics.
- `proxy01` is included in scheduled backups.
- An isolated whole-VM restore has validated local proxy-state recovery.
- Direct backend access remains available for troubleshooting and recovery.

### Negative / Tradeoffs

- The proxy is a shared dependency for friendly HTTPS access to multiple services.
- The wildcard private key is shared by the proxied names.
- Trusted clients require intentional root CA installation.
- The initial CA has no online CRL or OCSP service.
- Windows Schannel may report unavailable revocation status even when chain and hostname validation succeed.
- NGINX Proxy Manager introduces container-image and application-database maintenance.
- A second protected copy of the root CA private key remains required in a separate failure domain.
- The isolated restore did not exercise a live network cutover or root CA private-key recovery.

## Security Decisions

- No public port forwarding is configured.
- NGINX Proxy Manager port `81` is restricted to trusted internal administration.
- Backend authentication remains enabled.
- Proxmox management is not proxied.
- Root CA private key and passphrase remain outside Git and off `proxy01`.
- VM backups are treated as sensitive because they contain the wildcard service private key and proxy database.
- Offensive and intentionally vulnerable workloads must not access CA material or proxy administration.
- HSTS remains disabled until recovery and compatibility implications are intentionally reviewed.
- `curl --insecure` is not accepted as certificate validation.

## Validation

The decision was validated through:

- Debian 13 VM deployment as `proxy01`.
- QEMU Guest Agent and Node Exporter activation.
- Docker Engine and Docker Compose installation.
- NGINX Proxy Manager container deployment with persistent storage.
- Pi-hole local DNS records resolving the first service names to the proxy.
- Successful HTTP proxying to Grafana.
- Creation of an encrypted private root CA key on a trusted workstation.
- Issuance and SAN verification of the wildcard certificate.
- Root CA trust installation on Windows and `mon01`.
- Successful HTTPS access to Grafana and Pi-hole.
- HTTP-to-HTTPS redirects.
- Pi-hole root-path redirect to `/admin/`.
- Node Exporter target health for `proxy01`.
- Blackbox HTTPS probes returning success for both services.
- Grafana panels for HTTPS availability and certificate days remaining.
- Successful full-VM backup of `proxy01`.
- Isolated restore to a temporary VM without a network adapter.
- Validation of Debian, Docker, Node Exporter, QEMU Guest Agent, NGINX Proxy Manager, expected listeners, and persistent state.
- Removal of the temporary restore VM after testing.

## Follow-Up Work

- [ ] Create a second encrypted or offline root CA private-key copy in a separate failure domain.
- [ ] Define a formal renewal calendar and ownership process.
- [ ] Add certificate-expiration alerts after notification routing and response procedures exist.
- [ ] Restrict proxy administration and monitoring through future network segmentation.
- [ ] Re-evaluate wildcard versus per-service certificates as the service count grows.
- [ ] Re-test restoration after major NGINX Proxy Manager, Docker, storage, or PKI changes.
- [ ] Evaluate configuration automation only after the manual lifecycle remains well understood.

## Related Documentation

- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Network Architecture](../architecture/network.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
