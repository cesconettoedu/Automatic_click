# VPN Loop Automator

This script automates VPN connection cycles and website testing with Firefox (via Selenium).  
It connects to the VPN, opens a test website, waits a few seconds, closes the browser, disconnects from the VPN, and repeats the process multiple times.

---

## How it works

1. Checks the current public IP.
2. Connects to the VPN using **OpenVPN** with the specified configuration file (`client.ovpn`).
3. Waits a few seconds for the VPN to establish the connection.
4. Retrieves the new public IP and compares it with the previous one.
5. Launches **Firefox in headless mode** via Selenium.
6. Opens the specified URL (`https://www.siteescolhido.com`).
7. Waits a few seconds on the website.
8. Closes the browser.
9. Disconnects from the VPN (kills `openvpn` processes).
10. Waits for the configured delay.
11. Repeats the cycle until the defined number (`NUM_CICLOS`) is reached.

---

## Requirements

- **Linux** with `sudo` support and `openvpn` installed
- **Python 3.8+**
- **Python libraries**:
  - `requests`
  - `selenium`
- **Firefox** installed
- **geckodriver** compatible with your Firefox version and available in the `PATH`

---

## Configuration

Set the following parameters inside the script:

- `VPN_CONFIG` → path to the `.ovpn` configuration file
- `URL_TESTE` → URL to open in the browser
- `NUM_CICLOS` → number of cycles to execute
- `TEMPO_ESPERA` → waiting time between cycles (seconds)
- `TEMPO_CONEXAO_VPN` → waiting time for VPN to connect (seconds)

---

## Execution

```bash
python3 main.py


Example output:
[2025-08-28 10:00:00] === Starting VPN Loop Automator ===
[2025-08-28 10:00:00] Connecting to VPN via openvpn...
[2025-08-28 10:00:10] ✓ VPN connected
[2025-08-28 10:00:10] Initializing Firefox (headless)...
[2025-08-28 10:00:15] ✓ Page loaded: Free Online Image Resizer Tool
[2025-08-28 10:00:20] ✓ Firefox closed
[2025-08-28 10:00:20] Disconnecting VPN...
[2025-08-28 10:00:20] ✓ OpenVPN processes terminated

```
