# Managed Switch

## Purpose

The managed switch provides wired connectivity for the homelab and will become the foundation for future VLAN segmentation.

It is currently part of the baseline network build. The immediate goal is reliable connectivity and management access. The long-term goal is to support management, lab, and security network separation.

## Current Role

| Area | Details |
| --- | --- |
| Device role | Managed access switch |
| Current status | Active / baseline configuration |
| Network role | Connects lab devices to the current private network |
| Management | Internal management address; exact value omitted from public documentation |
| Future role | VLAN-capable switching for segmented lab networks |

## Current Configuration Notes

- The switch is reachable on the current private network.
- Management credentials should be stored in a password manager.
- Exact management IP address should be documented privately or with a placeholder such as `<SWITCH_MGMT_IP>`.
- VLAN design is planned but should not be treated as complete until configured, tested, and documented.

## Design Reasoning

A managed switch was added early because it gives the lab room to grow beyond a flat network.

Benefits:

- Supports future VLAN segmentation.
- Provides a realistic networking component for systems and network administration practice.
- Allows infrastructure devices to be wired instead of relying entirely on wireless connectivity.
- Creates a foundation for management, lab services, and security testing networks.

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
- Review firmware update options and document the update process.

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
