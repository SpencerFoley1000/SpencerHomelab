# Project 004: Reverse Proxy and Internal HTTPS

## Status

| Area | Details |
| --- | --- |
| Status | Completed — operational baseline |
| Completion date | 2026-07-14 |
| Owner | Homelab administrator |
| Dependencies | Pi-hole local DNS, `mon01` monitoring, Proxmox backup and recovery |
| Platform | NGINX Proxy Manager on dedicated Debian VM |
| Certificate model | Private root CA with wildcard internal service certificate |

Project 004 delivered internal reverse proxying, friendly service names, trusted HTTPS, certificate-lifecycle documentation, monitoring, backup coverage, and representative recovery validation.

Follow-up hardening remains documented separately and does not invalidate the completed operational baseline.

## Purpose

Provide memorable internal service names and trusted HTTPS for selected homelab web interfaces without exposing them publicly or making the proxy an undocumented single recovery dependency.

The project demonstrates:

- Reverse-proxy architecture.
- Internal DNS integration.
- TLS and certificate lifecycle management.
- Private trust distribution.
- Service dependency analysis.
- Host and service monitoring.
- Backup and isolated restore testing.
- Security-conscious public documentation.

## Implemented Architecture

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

mon01
    |-- scrapes proxy01 Node Exporter
    `-- probes HTTPS availability and certificate expiration

Proxmox
    `-- protects proxy01 through daily VM backups
```

Exact addresses, VM IDs, credentials, private keys, backup filenames, and protected certificate artifacts remain outside Git.

## Design Decisions

### Reverse-Proxy Platform

Selected NGINX Proxy Manager because it provides:

- Straightforward Docker Compose deployment.
- Understandable persistent state.
- NGINX-based routing behavior.
- Custom certificate support.
- Practical administration for the current service count.
- A manageable manual recovery path.

Native NGINX and Caddy remain valid future alternatives if automation, scale, or configuration portability requirements change.

### Deployment Model

`proxy01` is a dedicated Debian 13 VM with:

- 2 vCPU.
- 2 GB RAM.
- 20 GB virtual disk.
- QEMU Guest Agent.
- Node Exporter.
- Docker Engine and Docker Compose.
- NGINX Proxy Manager persistent state under `/opt/nginx-proxy-manager/`.

A dedicated VM keeps proxy failure, administration, backup, and monitoring separate from DNS and monitoring hosts.

### Internal Naming

The implemented public documentation model uses:

```text
<SERVICE>.lab.home.arpa
```

Initial names:

- `grafana.lab.home.arpa`
- `pihole.lab.home.arpa`

Pi-hole local records point these names to `proxy01`, not directly to backend systems.

### Certificate Authority and Trust

The implemented certificate model uses:

- A private root CA generated on a trusted administrative workstation.
- An encrypted root CA private key kept off `proxy01`.
- A wildcard certificate covering `*.lab.home.arpa` and `lab.home.arpa`.
- Only the wildcard service certificate and private key imported into NGINX Proxy Manager.
- Public root CA certificate installation on trusted Windows and Debian clients.

The initial CA has no online CRL or OCSP service. Compromise response therefore requires CA and certificate replacement plus trust-anchor removal.

### Recovery Boundaries

- Native backend authentication remains enabled.
- Direct backend access remains available for emergency recovery.
- Proxmox management is intentionally not proxied.
- The proxy is internal-only and has no router port forwarding.

See [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md).

## Implemented Services

### Grafana

- Friendly name resolves to `proxy01`.
- NGINX Proxy Manager forwards to Grafana on `mon01`.
- WebSocket support is enabled.
- HTTP redirects to HTTPS.
- Grafana authentication remains active.

### Pi-hole

- Friendly name resolves to `proxy01`.
- NGINX Proxy Manager forwards to Pi-hole on `dns01`.
- HTTP redirects to HTTPS.
- Pi-hole authentication remains active.
- A narrow rewrite redirects only `/` to `/admin/`:

```nginx
rewrite ^/$ /admin/ permanent;
```

## Monitoring

### Host Monitoring

Prometheus scrapes Node Exporter on `proxy01` with:

```text
host="proxy01"
role="reverse-proxy"
```

### HTTPS and Certificate Monitoring

Blackbox Exporter uses the `https_internal` module through the `blackbox_https_internal` Prometheus job.

Monitored signals include:

- HTTPS probe success.
- HTTP status code.
- Earliest certificate expiration.

Grafana includes:

- Internal HTTPS service availability.
- Certificate days remaining.

Alerting remains disabled until notification routing and response runbooks exist.

## Backup and Recovery

`proxy01` is included in the existing daily Proxmox backup job using:

- Snapshot mode.
- Zstandard compression.
- Retention of 7 daily, 4 weekly, and 3 monthly backups.
- Dedicated external storage with mount-point enforcement.

The backup protects:

- Debian guest state.
- Docker deployment.
- Compose definition.
- NGINX Proxy Manager database and proxy-host definitions.
- Imported wildcard certificate and service private key.
- Monitoring agent configuration.

The root CA private key is intentionally outside the VM backup boundary.

## Validation

### DNS

- Grafana and Pi-hole internal names resolve to `proxy01`.
- Existing recursive and local DNS probes remain healthy.

### Proxy Routing

- Grafana login loads through the friendly hostname.
- Pi-hole administration loads through the friendly hostname.
- Each hostname reaches only its intended backend.
- Backend authentication remains functional.
- Direct backend access remains available.

### HTTPS

- HTTP redirects to HTTPS.
- Trusted Windows and Debian clients validate the private CA chain.
- Wildcard SAN values cover the selected names.
- Both HTTPS endpoints load successfully.
- Windows Schannel revocation-status limitations are documented without disabling certificate validation globally.

### Monitoring

- `proxy01` Node Exporter target returns `1` in Prometheus.
- Both HTTPS Blackbox probes return success.
- Certificate expiration is visible in Prometheus and Grafana.
- Grafana availability and certificate-lifetime panels display separate service labels.

### Backup and Recovery

- Initial `proxy01` backup completed successfully.
- Backup was restored under a temporary VM ID.
- Restored VM network adapter was removed before first boot.
- Debian booted.
- Docker, QEMU Guest Agent, and Node Exporter were active.
- NGINX Proxy Manager container was running.
- Expected ports were listening.
- Persistent Compose, application-data, and certificate directories were present.
- Local administration endpoint returned an HTTP response.
- Temporary restore VM was removed after validation.
- Production proxy routes remained healthy after cleanup.

The restore proved local recovery of the proxy workload and imported service certificate state. It did not prove a live network cutover or restoration of the root CA signing key.

## Security Controls

- Proxy is internal-only.
- No edge-router port forwarding is configured.
- NGINX Proxy Manager administration remains on trusted internal access.
- Backend authentication is preserved.
- Proxmox management is not proxied.
- Root CA private key is encrypted, off proxy, and outside Git.
- VM backups are treated as sensitive because they contain the wildcard service private key and proxy database.
- HSTS remains disabled until recovery and compatibility implications are intentionally reviewed.
- Security-lab workloads must not access proxy administration or CA material.

## Lessons Learned

- Verify actual backend addresses before creating proxy routes; assumed addresses caused an avoidable failure.
- A service can be active and listening while a proxy still fails because the wrong address or port is configured.
- PowerShell aliases `curl` to `Invoke-WebRequest`; `curl.exe` avoids ambiguity.
- Copying prompts or continuation markers between shells creates misleading command errors.
- Prometheus configuration syntax validation must be paired with target discovery and PromQL validation.
- Grafana query legends and panel Display name variables use different syntax.
- Private CAs without CRL or OCSP endpoints can trigger Windows revocation-status errors even when chain and hostname validation succeed.
- The proxy must remain a convenience and security layer rather than the only recovery path.
- Isolated VM restoration is effective for testing duplicate infrastructure safely.

## Completion Checklist

- [x] Define requirements and select the reverse-proxy platform.
- [x] Select VM deployment model.
- [x] Define internal naming and DNS changes.
- [x] Select the certificate-authority and trust model.
- [x] Deploy and harden the proxy workload.
- [x] Integrate Grafana and Pi-hole.
- [x] Add host, HTTPS endpoint, and certificate monitoring.
- [x] Add backup coverage.
- [x] Complete isolated proxy restore testing.
- [x] Document certificate issuance, renewal, replacement, and CA-loss procedures.
- [x] Update architecture, service, runbook, ADR, change, roadmap, and changelog documentation.

## Follow-Up Work

- Create a second encrypted or offline root CA private-key copy in a separate failure domain.
- Define a formal certificate-renewal calendar and ownership process.
- Add actionable certificate-expiration alerts after notification routing exists.
- Export and privately validate the updated infrastructure dashboard.
- Restrict proxy administration and monitoring through future segmentation.
- Reconsider wildcard versus per-service certificates as the service count grows.
- Re-test recovery after major Docker, NGINX Proxy Manager, storage, or PKI changes.

## Related Documentation

- [Projects Index](README.md)
- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Virtualization Architecture](../architecture/virtualization.md)
- [VM Inventory](../architecture/vm-inventory.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Prometheus](../services/prometheus.md)
- [Grafana](../services/grafana.md)
- [Blackbox Exporter](../services/blackbox-exporter.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [Proxmox VM Restore](../runbooks/proxmox-vm-restore.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [Completion Change Record](../changes/2026-07-14-project-004-reverse-proxy-internal-https-completion.md)
- [Roadmap](../../ROADMAP.md)
