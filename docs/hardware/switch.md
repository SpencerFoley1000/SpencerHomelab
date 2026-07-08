# TP-Link TL-SG108E Managed Switch

## Purpose

The TP-Link TL-SG108E Easy Smart Switch provides wired connectivity for the homelab and will become the foundation for future VLAN segmentation.

It is currently part of the baseline network build. The immediate goal is reliable connectivity and management access. The long-term goal is to support management, lab, and security network separation.

## Current Role

| Area | Details |
| --- | --- |
| Device | TP-Link TL-SG108E Easy Smart Switch |
| Device role | Managed access switch |
| Firmware | Stock firmware |
| Current status | Active / baseline configuration |
| Network role | Connects lab devices to the current private network |
| Management | Internal management address; exact value omitted from public documentation |
| Future role | VLAN-capable switching for segmented lab networks |

## Current Configuration Notes

- The switch is reachable on the current private network.
- The switch is running stock firmware.
- Management credentials should be stored in a password manager.
- Exact management IP address should be documented privately or with a placeholder such as `<SWITCH_MGMT_IP>`.
- VLAN design is planned but should not be treated as complete until configured, tested, and documented.

## Design Decision

The homelab uses a TP-Link TL-SG108E as the initial managed switch because it provides a simple, affordable way to introduce managed switching concepts without adding unnecessary enterprise complexity early in the build.

This is useful for:

- Learning basic managed switch administration.
- Preparing for VLAN segmentation.
- Wiring infrastructure devices instead of relying entirely on wireless connectivity.
- Building a realistic network foundation for future services and security labs.

## Management Access

Switch management should be limited to trusted devices and, eventually, a dedicated management network.

Public documentation should not include:

- Real administrator username if it is personally identifying.
- Passwords.
- Exact management IP address if unnecessary.
- Full configuration exports containing sensitive details.

Use placeholders:

- `<SWITCH_MGMT_IP>`
- `<MGMT_NETWORK>`
- `<SECRET_STORED_IN_PASSWORD_MANAGER>`

## VLAN Planning

Future VLANs may include:

| Segment | Purpose |
| --- | --- |
| Management | Switch, router/firewall, Proxmox, and core administration interfaces |
| Lab services | Internal service workloads |
| Security lab | Isolated attacker/defender and vulnerable VM testing |
| Guest / untrusted | Optional low-trust devices |

VLAN IDs, subnet details, and port assignments should be documented after they are implemented and validated.

## Security Considerations

- Change default credentials before treating the switch as stable infrastructure.
- Store credentials outside the repository.
- Restrict switch management access where possible.
- Avoid exposing management interfaces outside the internal network.
- Back up or document the switch configuration once it becomes non-trivial.
- Review stock firmware update options and document the update process.

## Maintenance Notes

Future maintenance documentation should include:

- Firmware version and update process using sanitized values.
- Configuration backup process.
- Management access recovery procedure.
- Port mapping table if the physical topology becomes complex.
- VLAN and trunk/access port assignments after segmentation is implemented.

## Future Improvements

- Add sanitized port map.
- Add VLAN configuration notes.
- Add switch recovery process.
- Add firmware maintenance notes.
- Add network diagram reference once diagrams exist.

## Related Documentation

- [Hardware Inventory](inventory.md)
- [Network Architecture](../architecture/network.md)
- [Security Architecture](../architecture/security.md)
