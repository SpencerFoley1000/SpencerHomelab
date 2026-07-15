# NGINX Proxy Manager

## Status

Active

## Purpose

NGINX Proxy Manager provides internal reverse proxying and TLS termination for selected homelab web interfaces. It allows trusted clients to use memorable internal names and HTTPS while preserving each backend service's native authentication and direct recovery path.

The proxy is not publicly exposed and is not used as a replacement for network segmentation, application authentication, or administrative access controls.

## Technology Stack

| Component | Value |
| --- | --- |
| Host | `proxy01` |
| Operating system | Debian 13 (Trixie) |
| Deployment | Docker Compose |
| Container image | `jc21/nginx-proxy-manager:2.15.1` |
| Persistent configuration | `/opt/nginx-proxy-manager/data/` |
| Certificate state | `/opt/nginx-proxy-manager/letsencrypt/` |
| Compose definition | `/opt/nginx-proxy-manager/compose.yml` |
| Database | NGINX Proxy Manager embedded SQLite state |
| Public exposure | None |
| Backup maturity | Daily Proxmox backup; isolated whole-VM restore validated 2026-07-14 |

Exact VM IDs, addresses, credentials, certificate private keys, and backup filenames remain outside Git.

## Architecture

```text
Trusted client
    |
    | HTTPS to <SERVICE>.lab.home.arpa
    v
Pi-hole local DNS
    |
    | resolves service name to <PROXY01_IP>
    v
proxy01 / NGINX Proxy Manager
    |
    | internal HTTP to selected backend
    v
Backend service with native authentication
```

Current proxy hosts:

| Publicly documented name | Backend role | TLS | Direct recovery access |
| --- | --- | --- | --- |
| `grafana.lab.home.arpa` | Grafana on `mon01` | Internal wildcard certificate | Retained through the backend address and port |
| `pihole.lab.home.arpa` | Pi-hole administration on `dns01` | Internal wildcard certificate | Retained through the backend address and native administration path |

Proxmox management is intentionally not routed through the proxy. Hypervisor recovery must not depend on an optional application-layer proxy.

## Networking

| Port | Purpose | Exposure |
| --- | --- | --- |
| TCP `80` | Internal HTTP and redirect to HTTPS | Homelab LAN only |
| TCP `443` | Internal HTTPS proxy traffic | Homelab LAN only |
| TCP `81` | NGINX Proxy Manager administration | Trusted administrative clients only |
| TCP `9100` | Node Exporter metrics | `mon01` only where future firewall policy is enforced |

No router port forwarding or public DNS record is configured for the proxy.

## Internal DNS

Pi-hole local records point selected service names to the proxy address, not directly to backend systems.

```text
grafana.lab.home.arpa -> <PROXY01_IP>
pihole.lab.home.arpa  -> <PROXY01_IP>
```

The proxy selects the backend by HTTP `Host` header. This separates client-facing names from backend addresses and ports.

## TLS and Certificate Model

The current design uses a private root certificate authority and a wildcard service certificate covering:

```text
*.lab.home.arpa
lab.home.arpa
```

The root CA private key:

- Was generated on a trusted administrative workstation.
- Is encrypted with a passphrase stored outside Git.
- Is not present on `proxy01`.
- Must never be uploaded to NGINX Proxy Manager.
- Requires a second protected copy in a separate failure domain as a follow-up hardening task.

`proxy01` stores only the wildcard service certificate and its private key. Trusted clients receive the public root CA certificate through an intentional administrative process.

The initial private CA does not publish CRL or OCSP endpoints. Windows Schannel clients may therefore report that revocation status is unavailable even when chain and hostname validation succeed. This limitation is documented rather than bypassed globally.

## Proxy Configuration

### Grafana

- Scheme: HTTP to the backend.
- WebSocket support: enabled for Grafana Live compatibility.
- Backend authentication remains active.
- HTTP redirects to HTTPS.
- Direct backend access remains available for recovery.

### Pi-hole

- Scheme: HTTP to the backend.
- Backend authentication remains active.
- HTTP redirects to HTTPS.
- A narrow NGINX rewrite redirects only `/` to `/admin/`:

```nginx
rewrite ^/$ /admin/ permanent;
```

This avoids the Pi-hole bare-root error page without rewriting application paths generally.

## Monitoring

`proxy01` is monitored at two layers.

### Host

Node Exporter is scraped by Prometheus using:

```text
host="proxy01"
role="reverse-proxy"
```

### Service and Certificate

Blackbox Exporter probes both HTTPS endpoints using the `https_internal` module.

Current signals include:

- `probe_success`
- `probe_http_status_code`
- `probe_ssl_earliest_cert_expiry`

Grafana displays:

- Internal HTTPS service availability.
- Certificate days remaining.

Alerts remain intentionally disabled until notification routing and response runbooks exist.

## Backup Strategy

`proxy01` is included in the daily Proxmox backup job using:

- Snapshot mode.
- Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external backup storage with mount-point enforcement.

The VM backup protects:

- Debian configuration.
- Docker Engine state required by the deployment.
- Compose definition.
- NGINX Proxy Manager database and proxy-host definitions.
- Imported wildcard certificate and service private key.
- Node Exporter configuration.

The VM backup does not protect the root CA signing key because that key is intentionally kept off the proxy.

## Recovery Procedure

### Whole-VM Recovery

1. Restore the latest `proxy01` backup to normal VM storage using a temporary VM ID.
2. Remove the restored VM's network adapter before first boot if production remains online.
3. Validate Debian boot, Docker, Node Exporter, QEMU Guest Agent, the NGINX Proxy Manager container, local ports, and persistent directories.
4. Resolve duplicate identity and addressing risk before reconnecting networking.
5. Validate DNS, HTTPS, backend routing, monitoring, and client trust after production cutover.

### Manual Rebuild

1. Provision a minimal Debian VM named `proxy01`.
2. Install QEMU Guest Agent, Node Exporter, Docker Engine, and Docker Compose.
3. Recreate `/opt/nginx-proxy-manager/compose.yml`.
4. Restore protected NGINX Proxy Manager state or recreate proxy hosts manually.
5. Import the current service certificate and private key from protected storage.
6. Revalidate local DNS records and both backend routes.
7. Re-add monitoring and backup coverage.

### CA Loss

If the root CA private key is lost but not compromised:

- Existing certificates remain usable until expiration.
- New certificates cannot be issued from that CA.
- Create a replacement CA, issue replacement certificates, redistribute trust, and remove the old CA from clients.

If the root CA private key is exposed, treat the trust boundary as compromised and replace the CA and all issued certificates.

## Restore Validation

On 2026-07-14, the production backup was restored to a temporary isolated VM.

Validated:

- VM reconstruction from the Proxmox backup.
- Debian boot.
- Docker active.
- Node Exporter active.
- QEMU Guest Agent active.
- NGINX Proxy Manager container running.
- TCP `80`, `81`, `443`, and `9100` listeners present.
- HTTP response from the local administration endpoint.
- Persistent Compose, application-data, and certificate directories present.

The temporary VM had no network adapter and was deleted after validation. The test proved local recovery of the proxy workload and imported service certificate state; it did not exercise a live network cutover or root CA signing-key restoration.

## Security Considerations

- Keep ports `80`, `81`, and `443` internal-only.
- Restrict port `81` to trusted administrative clients.
- Preserve backend authentication.
- Do not publish proxy exports, databases, certificates with private material, or exact backend addresses.
- Keep the root CA private key off `proxy01` and away from security-lab workloads.
- Keep direct backend access for emergency recovery.
- Review container updates before deployment and verify proxy behavior afterward.
- Treat VM backups as sensitive because they contain service credentials and private certificate material.

## Maintenance Notes

- Review container-image updates and release notes before changing the pinned image version.
- Confirm a recent VM backup before application or certificate changes.
- Validate Compose configuration before recreation.
- Recheck both HTTPS probes and certificate lifetime after changes.
- Renew the wildcard certificate before the monitored threshold becomes actionable.
- Update Pi-hole records and proxy-host definitions together to avoid drift.
- Re-test restoration after major platform, storage, or certificate changes.

## Future Improvements

- Create a second encrypted or offline copy of the root CA private key in a separate failure domain.
- Define a formal certificate renewal and CA rotation calendar.
- Add actionable certificate-expiration alerts after notification routing exists.
- Restrict proxy administration and monitoring flows through future segmentation and firewall policy.
- Evaluate an intermediate CA only if certificate volume and operational requirements justify it.
- Consider configuration automation after the manual lifecycle is well understood.

## Related Documentation

- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Network Architecture](../architecture/network.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
