# Project 004 Reverse Proxy and Internal HTTPS Completion

## Date

2026-07-14

## Summary

Completed the first internal reverse-proxy and private-PKI implementation for the homelab.

The project introduced a dedicated `proxy01` VM running NGINX Proxy Manager, friendly `lab.home.arpa` service names through Pi-hole, trusted internal HTTPS for Grafana and Pi-hole, host and endpoint monitoring, certificate-expiration visibility, scheduled VM backup coverage, and an isolated restore test.

## What Changed

### Reverse Proxy

- Provisioned `proxy01` as a dedicated Debian 13 VM.
- Installed QEMU Guest Agent and Node Exporter.
- Installed Docker Engine from the vendor-supported Debian repository.
- Deployed NGINX Proxy Manager with Docker Compose.
- Persisted application state, proxy definitions, and certificate state under `/opt/nginx-proxy-manager/`.
- Kept the proxy and its administration interface internal-only.

### Internal DNS and Routing

- Standardized the public documentation model on `lab.home.arpa`.
- Added Pi-hole local records for Grafana and Pi-hole administration.
- Pointed those records to `proxy01` rather than directly to backend systems.
- Configured NGINX Proxy Manager to route requests by hostname to the correct backend.
- Preserved direct backend access for recovery.
- Intentionally left Proxmox management outside the proxy dependency.

### Internal PKI and HTTPS

- Generated an encrypted private root CA key on a trusted administrative workstation.
- Kept the root CA private key off `proxy01`.
- Issued a wildcard service certificate for `*.lab.home.arpa` and `lab.home.arpa`.
- Installed the public root CA certificate on trusted Windows and Debian clients.
- Imported only the wildcard service certificate and private key into NGINX Proxy Manager.
- Enabled HTTPS and HTTP-to-HTTPS redirects for Grafana and Pi-hole.
- Added a narrow root-path rewrite so the Pi-hole friendly URL lands on `/admin/`.
- Documented the initial design's lack of online CRL or OCSP services.

### Monitoring

- Added `proxy01` to the shared Prometheus Node Exporter job using `host="proxy01"` and `role="reverse-proxy"` labels.
- Added an `https_internal` Blackbox Exporter module.
- Added a `blackbox_https_internal` Prometheus job for Grafana and Pi-hole.
- Confirmed both HTTPS probes return success.
- Added Grafana panels for internal HTTPS service availability and certificate days remaining.
- Kept alerting disabled until notification routing and response runbooks exist.

### Backup and Recovery

- Added `proxy01` to the existing daily Proxmox backup job.
- Completed an initial snapshot-mode, Zstandard-compressed VM backup.
- Restored the VM to a temporary ID on normal VM storage.
- Removed the restored VM's network adapter before boot.
- Validated Debian, Docker, QEMU Guest Agent, Node Exporter, NGINX Proxy Manager, expected listeners, and persistent application and certificate directories.
- Deleted the temporary restore VM after validation.

### Documentation

- Completed the Project 004 project page.
- Added NGINX Proxy Manager service documentation.
- Added an internal certificate lifecycle runbook.
- Added ADR-0004 documenting the proxy and private-CA decision.
- Synchronized architecture, inventory, monitoring, storage, security, roadmap, indexes, and changelog documentation.

## Why

- Direct IP addresses and ports become difficult to operate and explain as the service count grows.
- Internal HTTPS protects administrative sessions and provides realistic certificate-lifecycle experience.
- Keeping the proxy separate from DNS and monitoring preserves clear failure domains.
- Keeping the root CA key off the proxy reduces the impact of a proxy compromise.
- Host metrics alone do not prove that HTTPS routing or certificate validation works.
- Backup completion alone does not prove that NGINX Proxy Manager state can be recovered.
- Public portfolio documentation should show both the implemented design and the operational tradeoffs accepted.

## Validation

Validated successfully:

- `proxy01` Debian networking and hostname.
- QEMU Guest Agent.
- Node Exporter endpoint and Prometheus target state.
- Docker Engine and Docker Compose.
- NGINX Proxy Manager container and persistent storage.
- Pi-hole local DNS resolution to the proxy.
- Grafana backend reachability from `proxy01`.
- Grafana HTTP proxy routing.
- Wildcard certificate chain and SAN values.
- Windows and Debian root CA trust.
- Grafana and Pi-hole HTTPS access.
- HTTP-to-HTTPS redirects.
- Pi-hole `/` to `/admin/` redirect.
- Blackbox HTTPS probe success.
- Certificate-expiration metric visibility.
- Grafana availability and certificate-lifetime panels.
- Initial `proxy01` VM backup.
- Isolated whole-VM restore and local service validation.
- Production proxy health after restore-test cleanup.

## Lessons Learned

- Backend addresses should be verified from the actual guest before creating proxy routes; assumed addresses created an avoidable troubleshooting detour.
- A healthy backend service can still be unreachable when the wrong address or port is used.
- PowerShell aliases `curl` to `Invoke-WebRequest`; `curl.exe` avoids ambiguity during Windows testing.
- Copying shell prompts and continuation markers into another shell produces misleading command-not-found errors.
- YAML indentation can pass casual visual review while preventing Prometheus from discovering a target; direct target inventory validation is required.
- Grafana's query legend syntax and panel Display name syntax are different.
- Private CAs without CRL or OCSP endpoints can trigger Windows Schannel revocation-status errors even when chain and hostname validation are correct.
- `--ssl-revoke-best-effort` is a narrower diagnostic choice than disabling certificate validation.
- The proxy should remain a convenience and security layer, not the only administrative recovery path.
- Restoring with the network adapter removed is a repeatable way to validate duplicate infrastructure safely.

## Remaining Work

- Create a second encrypted or offline copy of the root CA private key in a separate failure domain.
- Define a formal certificate-renewal calendar and ownership process.
- Add actionable certificate-expiration alerts after notification routing exists.
- Export and privately validate the updated infrastructure dashboard.
- Restrict proxy administration and monitoring through future segmentation.
- Re-evaluate wildcard certificates if service count or isolation requirements grow.
- Re-test recovery after major Docker, NGINX Proxy Manager, storage, or PKI changes.

## Related Documentation

- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Internal Certificate Lifecycle](../runbooks/internal-certificate-lifecycle.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
- [Architecture Overview](../architecture/overview.md)
- [Network Architecture](../architecture/network.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Security Architecture](../architecture/security.md)
- [Storage Architecture](../architecture/storage.md)
- [VM Inventory](../architecture/vm-inventory.md)
