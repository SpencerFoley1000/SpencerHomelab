# Internal Certificate Lifecycle

## Status

Operational baseline

## Last Validated

2026-07-14

## Purpose

Document the safe issuance, deployment, trust distribution, renewal, replacement, and recovery process for the homelab private certificate authority and internal service certificates.

This runbook uses sanitized paths and names. Private keys, passphrases, exact workstation paths, and certificate files containing private material must remain outside Git.

## Current Model

- Private root CA created on a trusted administrative workstation.
- Root CA private key encrypted with a strong passphrase.
- Root CA private key kept off `proxy01`.
- Public root CA certificate distributed to trusted clients and `mon01`.
- Wildcard service certificate covers `*.lab.home.arpa` and `lab.home.arpa`.
- NGINX Proxy Manager terminates TLS for selected internal services.
- No public internet exposure.
- No online CRL or OCSP service in the initial design.

## Protected Artifacts

| Artifact | Sensitivity | Required handling |
| --- | --- | --- |
| Root CA private key | Critical secret | Encrypted, off proxy, outside Git, second protected copy required |
| Root CA passphrase | Critical secret | Password manager or equivalent protected store |
| Root CA public certificate | Public trust artifact | Distribute only through trusted administrative channels |
| Service private key | Secret | Upload only to the intended proxy; protected by VM backup and private storage |
| Service certificate | Public certificate | May be distributed with the service key kept separate |
| CSR and extension file | Potentially topology-revealing | Keep private when exact internal names are present |
| NGINX Proxy Manager database | Sensitive operational state | Protect through VM backup; never commit raw state |

## Preconditions

- Trusted administrative workstation.
- OpenSSL available.
- Protected private storage outside the repository.
- Root CA passphrase available.
- Current service names confirmed.
- Recent `proxy01` backup confirmed before certificate replacement.
- Trusted access to NGINX Proxy Manager.

## Issue or Renew the Wildcard Certificate

### 1. Confirm working directory

Use a private directory represented publicly as:

```text
<PRIVATE_PKI_DIRECTORY>
```

Confirm the existing root CA certificate and encrypted private key are present.

### 2. Generate a new service private key

```bash
openssl genpkey \
  -algorithm RSA \
  -pkeyopt rsa_keygen_bits:2048 \
  -out lab-home-arpa.key.pem
```

### 3. Create the extension file

```ini
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:*.lab.home.arpa,DNS:lab.home.arpa
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer
```

### 4. Create the certificate-signing request

```bash
openssl req \
  -new \
  -sha256 \
  -key lab-home-arpa.key.pem \
  -out lab-home-arpa.csr.pem \
  -subj "/CN=*.lab.home.arpa/O=Homelab"
```

### 5. Sign the certificate

```bash
openssl x509 \
  -req \
  -sha256 \
  -days 365 \
  -in lab-home-arpa.csr.pem \
  -CA homelab-root-ca.crt.pem \
  -CAkey homelab-root-ca.key.pem \
  -CAcreateserial \
  -out lab-home-arpa.crt.pem \
  -extfile lab-home-arpa.ext
```

Enter the root CA passphrase only through the local OpenSSL prompt. Do not place the passphrase in shell history, scripts, Git, or screenshots.

### 6. Validate before deployment

```bash
openssl verify \
  -CAfile homelab-root-ca.crt.pem \
  lab-home-arpa.crt.pem

openssl x509 \
  -in lab-home-arpa.crt.pem \
  -noout \
  -subject \
  -issuer \
  -dates \
  -ext subjectAltName
```

Confirm:

- Chain verification returns `OK`.
- Issuer is the expected homelab root CA.
- Validity dates are correct.
- SAN includes both wildcard and zone-apex names.

## Deploy to NGINX Proxy Manager

1. Confirm a recent `proxy01` backup.
2. Open NGINX Proxy Manager from a trusted administrative client.
3. Add a custom certificate using:
   - Service private key.
   - Signed service certificate.
   - No intermediate certificate in the current single-root model.
4. Use a descriptive name such as `lab.home.arpa wildcard`.
5. Assign the certificate to each intended proxy host.
6. Enable Force SSL and HTTP/2 where tested.
7. Leave HSTS disabled until the recovery and client-compatibility implications are intentionally accepted.
8. Save and test each route.

Never upload the root CA private key to NGINX Proxy Manager.

## Distribute Client Trust

Only the public root CA certificate is distributed.

### Windows

From an elevated PowerShell or command prompt:

```powershell
certutil.exe -addstore -f Root "<PATH_TO_ROOT_CA_PUBLIC_CERTIFICATE>"
```

Validate through the browser and a certificate-aware client.

### Debian or Ubuntu

```bash
sudo install -m 0644 \
  <ROOT_CA_PUBLIC_CERTIFICATE> \
  /usr/local/share/ca-certificates/homelab-root-ca.crt

sudo update-ca-certificates
```

Remove temporary transfer copies after installation.

## Validate Deployed HTTPS

From a trusted client:

```bash
curl -I https://grafana.lab.home.arpa
curl -I https://pihole.lab.home.arpa
```

Windows Schannel may report unavailable revocation status because the initial private CA has no CRL or OCSP endpoint. A narrower validation command is:

```powershell
curl.exe --ssl-revoke-best-effort -I https://grafana.lab.home.arpa
```

Do not use `-k` or `--insecure` for acceptance testing because those options disable certificate validation.

Confirm:

- HTTP redirects to HTTPS.
- Certificate chain is trusted.
- Hostname matches.
- Backend login remains functional.
- Blackbox `probe_success` returns `1`.
- Certificate days remaining appears in Grafana.

## Renewal Procedure

1. Review the Grafana certificate-days panel.
2. Begin renewal before the operational warning threshold.
3. Generate a new service private key rather than reusing the old key by default.
4. Issue and validate the replacement certificate.
5. Confirm a current `proxy01` backup.
6. Import the replacement certificate into NGINX Proxy Manager.
7. Reassign proxy hosts.
8. Validate both internal HTTPS endpoints.
9. Confirm Blackbox probes and certificate-expiration metrics reflect the new certificate.
10. Retain the previous certificate and key only for a short rollback window in protected storage, then remove them intentionally.
11. Update documentation and the changelog.

## Root CA Public Certificate Removal

When retiring or replacing a CA:

- Remove the old trust anchor from managed clients after all services have migrated.
- Validate that no active service certificate chains to the retired CA.
- Preserve only the records required for audit or historical recovery.
- Destroy retired private key copies according to the protected-storage process.

## Root CA Loss

If the private key is lost but not exposed:

1. Existing service certificates remain valid until expiration.
2. New certificates cannot be issued from the lost CA.
3. Create a replacement root CA.
4. Issue replacement service certificates.
5. Distribute the replacement public root certificate.
6. Migrate proxy hosts.
7. Remove the old trust anchor after migration.
8. Document the event and lessons learned without publishing protected material.

## Root CA Compromise

If exposure is suspected or confirmed:

1. Treat every certificate issued by the CA as untrusted.
2. Disconnect or restrict affected administrative surfaces where appropriate.
3. Create a new CA using a trusted system.
4. Issue new service certificates and private keys.
5. Replace certificates on all services.
6. Remove the compromised CA from every trusted client.
7. Review backups and systems that contained affected private material.
8. Document scope, remediation, and remaining risk without publishing secrets.

The current design has no online revocation infrastructure, so replacement of the trust anchor is the authoritative compromise response.

## Backup and Recovery

### Root CA

Required:

- Encrypted primary private key copy.
- Strong passphrase stored separately.
- Second encrypted or offline copy in a separate failure domain.
- Public certificate retained with recovery documentation.
- Periodic verification that protected copies remain readable.

Do not place the only root CA copy on the same workstation, Proxmox host, or backup disk as the services it protects.

### Service Certificate and Proxy State

Protected by:

- Private certificate and key storage on the administrative workstation.
- `proxy01` whole-VM backups.
- NGINX Proxy Manager persistent state.
- Manual rebuild documentation.

The 2026-07-14 isolated restore validated that the imported certificate state and NGINX Proxy Manager data were present in the restored VM. It did not validate root CA private-key restoration or a live proxy cutover.

## Rollback

If a replacement certificate breaks service access:

1. Reassign the previous known-good certificate in NGINX Proxy Manager.
2. Confirm HTTPS and backend access.
3. Check certificate SAN, validity, issuer, and private-key pairing.
4. Correct the replacement certificate offline.
5. Retry only after validation.

Do not delete the previous certificate until the rollback window has passed.

## Documentation Requirements

Record:

- Issuance or renewal date.
- Certificate purpose and covered sanitized names.
- Expiration date or lifetime.
- Validation performed.
- Proxy hosts changed.
- Monitoring result.
- Whether rollback material was removed.
- Any CA trust-distribution changes.

Never record private keys, passphrases, serial numbers when unnecessary, exact private storage paths, or screenshots containing protected values.

## Related Documentation

- [NGINX Proxy Manager](../services/nginx-proxy-manager.md)
- [Project 004](../projects/project-004-reverse-proxy-internal-https.md)
- [Security Architecture](../architecture/security.md)
- [Monitoring Architecture](../architecture/monitoring.md)
- [Proxmox VM Restore](proxmox-vm-restore.md)
- [ADR-0004](../decisions/ADR-0004-internal-reverse-proxy-and-private-ca.md)
