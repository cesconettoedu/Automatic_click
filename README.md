run -> python3 main.py

# VPN Loop Automator

Este script automatiza ciclos de conexão VPN e testes de navegação com Firefox (via Selenium).  
Ele conecta a VPN, abre um site de teste, espera alguns segundos, fecha o navegador, desconecta a VPN e repete o processo várias vezes.

---

## Como funciona

1. Verifica o IP público atual.
2. Conecta a VPN usando **OpenVPN** com o arquivo de configuração especificado (`client.ovpn`).
3. Aguarda alguns segundos para a VPN estabelecer a conexão.
4. Obtém o novo IP público e compara com o anterior.
5. Abre o **Firefox em modo headless** via Selenium.
6. Acessa a URL definida (`https://www.siteescolhido.com`).
7. Espera alguns segundos no site.
8. Fecha o navegador.
9. Desconecta da VPN (encerra processos `openvpn`).
10. Espera o tempo configurado.
11. Repete o ciclo até atingir o número definido (`NUM_CICLOS`).

---

## Requisitos

- **Linux** com suporte a `sudo` e `openvpn` instalado
- **Python 3.8+**
- **Bibliotecas Python**:
  - `requests`
  - `selenium`
- **Firefox** instalado
- **geckodriver** compatível com a versão do Firefox e presente no `PATH`

---

## Configuração

- Defina os parâmetros no código:
  - `VPN_CONFIG` → caminho do arquivo `.ovpn`
  - `URL_TESTE` → URL para abrir no navegador
  - `NUM_CICLOS` → número de ciclos que serão executados
  - `TEMPO_ESPERA` → tempo de espera entre ciclos (segundos)
  - `TEMPO_CONEXAO_VPN` → tempo de espera para VPN conectar (segundos)

---

## Execução

```bash
python3 main.py
```
