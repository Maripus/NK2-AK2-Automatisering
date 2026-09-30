# NK2 Arbeidskrav 2 – Automatisering

Dette prosjektet er laget til Arbeidskrav 2 i Nettverk 2.

Målet med oppgaven er å bruke to metoder for å automatisere Cisco-utstyr:

1. Python via konsollkabel
2. Ansible via SSH

Jeg jobber med STUD2-oppsettet, altså den grønne delen av topologien.

Python brukes først for å sette opp SSH på Cisco-enhetene via konsoll. Når SSH fungerer brukes Ansible til videre konfigurasjon over Ethernet.

---

# STUD2-oppsett

STUD2 består av flere Cisco-enheter og klienter.

Planen er at hele den grønne siden skal konfigureres og automatiseres.

Foreløpig er følgende enheter satt opp og testet:

| Enhet | IP | Status |
|---|---|---|
| R2 | 172.16.2.1/24 | Python, SSH og Ansible testet |
| SW2 | 172.16.2.2/24 | Python, SSH og Ansible testet |

R2 og SW2 ble brukt som første del av oppsettet for å teste hele arbeidsflyten fra konsoll til Ansible.

Resten av STUD2-topologien skal også legges inn med egne host_vars og inventory-verdier når alle enhetene er identifisert og har fått management-IP.

---

# Del 1 – Python via konsoll

En ny eller slettet Cisco-enhet har ikke nødvendigvis SSH konfigurert.

Derfor brukes Python og pySerial via konsollkabel for å gjøre den første konfigurasjonen.

Python-script ligger i:

```text
python/
├── serial_test.py
├── test_console.py
├── setup_ssh.py
└── setup_ssh_switch.py
