# NK2 Arbeidskrav 2 – Automatisering

## Beskrivelse

Dette prosjektet automatiserer konfigurasjon av Cisco-utstyr med Python og Ansible.

Python brukes først via konsollkabel for å klargjøre enhetene og sette opp SSH.
Etter at SSH er tilgjengelig brukes Ansible til videre konfigurasjon over Ethernet.

## Utstyr

- Windows laptop
- WSL
- Ansible
- Cisco IOS / IOS XE
- R2
- SW2

## IP-adresser

| Enhet | IP-adresse |
|---|---|
| R2 | 172.16.2.1 |
| SW2 | 172.16.2.2 |

## Python

Python-script brukes via serial console for å sette opp:

- hostname
- management-IP
- lokal bruker
- RSA-nøkler
- SSH version 2
- VTY-konfigurasjon

## Ansible

Ansible bruker SSH for å koble til Cisco-enhetene.

Prosjektet bruker Cisco IOS collection:

cisco.ios

## Struktur

AK2-ansible/
├── ansible.cfg
├── inventory.yml
├── group_vars/
├── host_vars/
├── playbooks/
└── README.md

## Playbooks

- show_status.yml – kontrollerer status
- basic_config.yml – grunnkonfigurasjon
- vlans.yml – VLAN-konfigurasjon
- dhcp.yml – DHCP-konfigurasjon

## Testing

Før Ansible kjøres skal det kontrolleres at R2 og SW2 kan nås med ping og SSH.
