# NK2 Arbeidskrav 2 – Automatisering

Dette prosjektet er laget til Arbeidskrav 2 i Nettverk 2 ved Fagskolen Innlandet.

Målet med oppgaven er å bruke to metoder for å automatisere Cisco-utstyr:

1. **Python og pySerial** via konsollkabel for å sette opp SSH.
2. **Ansible** via SSH for videre konfigurasjon av nettverket.

Jeg jobber med STUD2, altså den grønne delen av topologien.

Tanken er at jeg først skal kunne sette opp en Cisco-enhet med Python, slik at den får IP-adresse, SSH-bruker og SSH-tilgang. Etter dette kan jeg bruke Ansible til å konfigurere blant annet routing, VLAN, trunk og DHCP.

---

## STUD2 – Nettverksoppsett

I dette arbeidskravet har jeg jobbet med et oppsett bestående av CORE-switch, rutere og access-switcher.

### Enheter konfigurert og testet

| Enhet | Modell | IP-adresse | Hva som er testet |
|---|---|---|---|
| CORE | Cisco 3650 | 172.16.2.2 | SSH, Ansible og routing |
| R1 | Cisco 2901 | 172.16.21.2 | SSH, Ansible, routing og DHCP |
| SW1 | Cisco 2960 | 192.168.10.10 | SSH, Ansible, VLAN og trunk |

### Nettverk og adresser

| Nettverk | Adresse | Bruksområde |
|---|---|---|
| Management | 172.16.2.0/24 | PC til CORE |
| CORE–R1 | 172.16.21.0/30 | Forbindelse mellom CORE og R1 |
| VLAN 10 | 192.168.10.0/24 | Klientnettverk og management for SW1 |
| VLAN 20 | 192.168.20.0/24 | Planlagt nettverk for R2-siden |

Den fysiske koblingen som ble testet var:

PC → CORE → R1 → SW1

CORE har `172.16.21.1` mot R1, mens R1 har `172.16.21.2`. På R1 ble VLAN 10 satt opp med gateway `192.168.10.1`.

SW1 er koblet til R1 med en trunk-forbindelse som tillater VLAN 10 og 20.

### Status på resten av oppsettet

Jeg har også laget konfigurasjonsfiler for R2 og SW2, men disse ble ikke testet fysisk i den siste labøkten. EtherChannel mot STUD1 ble heller ikke testet siden partnerens utstyr ikke var tilgjengelig.

---

## Del 1 – Python via konsoll

En Cisco-enhet som er nullstilt, har ikke nødvendigvis SSH konfigurert. Derfor brukte jeg Python og pySerial via konsollkabel for å gjøre den første konfigurasjonen.

Python-scriptet setter blant annet opp hostname, IP-adresse, domenenavn, SSH-bruker og RSA-nøkler.

Python-filene ligger i mappen `python/`:

- `serial_test.py` – testing av konsollforbindelsen
- `test_console.py` – enkel test mot Cisco-console
- `setup_ssh.py` – oppsett av SSH på rutere
- `setup_ssh_switch.py` – oppsett av SSH på switcher

Etter at Python hadde konfigurert enhetene, kontrollerte jeg at de svarte på ping og at jeg kunne logge inn med SSH.

---

## Del 2 – Ansible via SSH

Etter at SSH fungerte, brukte jeg Ansible fra WSL på Windows-PC-en.

Ansible bruker `inventory.yml` til å finne enhetene og `host_vars/` til å hente forskjellige innstillinger for hver enhet.

Jeg har laget egne playbooks for blant annet:

- Routing og IP-adresser
- VLAN og trunk-porter
- DHCP-pooler
- EtherChannel
- Verifisering og lagring av konfigurasjon

Konfigurasjonen bruker variabler slik at den kan gjenbrukes på flere Cisco-enheter uten å måtte skrive hele oppsettet på nytt.

---

## Testing og feilsøking

Underveis testet jeg forbindelsene med ping, SSH og Ansible.

På R1 fikk jeg konfigurert routing og DHCP for VLAN 10. DHCP-poolen bruker nettverket `192.168.10.0/24`, med gateway `192.168.10.1`. Adressene fra `.1` til `.20` er ekskludert fra DHCP-utdeling.

På SW1 fikk jeg konfigurert VLAN 10 og 20 og kontrollert at trunk-porten `Fa0/1` fungerte med 802.1Q.

Jeg møtte også noen problemer:

- Først var konsollporten opptatt av PuTTY.
- R1 sto i initial configuration dialog, slik at Python-kommandoene ikke ble kjørt som forventet.
- Eldre Cisco IOS brukte SSH-algoritmer som nyere OpenSSH ikke godtok automatisk.
- Nettverkskabelen på SW1 sto først i feil port.
- Jeg måtte rette interface-navnene i `host_vars/R1.yml` fra et annet rutermodellformat til de faktiske portene på Cisco 2901.

Etter feilsøkingen fikk jeg testet at Python-bootstrap fungerte, og at Ansible kunne nå og konfigurere de tre enhetene.

---

## Resultat

Jeg fikk testet hele arbeidsflyten fra Python via konsoll til Ansible over SSH på deler av STUD2-nettverket.

CORE, R1 og SW1 fungerte med riktig IP-adressering, og jeg fikk verifisert routing, DHCP og trunk/VLAN-konfigurasjon.

Resten av topologien er forberedt med konfigurasjonsfiler, men ikke fullstendig testet på fysisk utstyr.
