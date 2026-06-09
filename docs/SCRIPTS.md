# Scripts — Funcionamento Detalhado

---

## `multicortex-status.sh`

**Localização:** `scripts/system/multicortex-status.sh`  
(cópia idêntica em `suse/.../root/opt/multicortex/scripts/system/`)

**Chamado por:** comando `multicortex-status` ou alias `mc-status`

Define `set -Eeuo pipefail` — qualquer erro não tratado aborta. `OLLAMA_BASE_URL` usa `$OLLAMA_HOST` se definido, senão `http://127.0.0.1:11434`.

`section()` imprime títulos em azul ciano (`\033[1;36m`). `cmd_or_na()` executa um comando e imprime `N/A` se falhar, sem abortar.

**Seção Versão:** lê `/etc/multicortex-version` ou `./VERSION`.

**Seção Sistema:** `hostname`, `uname -r` (kernel), `uname -m` (arquitetura), `PRETTY_NAME` e `VERSION_ID` do `/etc/os-release`.

**Seção Rede:** `ip -4 addr show scope global` lista IPs globais (não loopback), formatados com `awk`. Imprime URLs de todos os serviços: Ollama API, tags, Web UI, Open WebUI.

**Seção Serviços:** itera sobre `ollama.service`, `multicortex-chat-ui.service`, `open-webui.service` e chama `systemctl is-active` para cada um. Exibe `active`, `inactive` ou `failed`.

**Seção Ollama API:** `curl -fsS http://127.0.0.1:11434/api/tags` salvo em `/tmp/multicortex-tags.json`. Se responder, lista modelos com `jq -r '.models[]?.name'` ou imprime JSON bruto se `jq` não estiver disponível.

**Seção Modelos:** `ollama list` em formato tabular.

**Seção Hardware:** `lscpu | awk` para o model name da CPU; `free -h` para RAM; `df -h /` para disco; `nvidia-smi` completo se disponível.

**Seção Logs:** `journalctl -u ollama.service -n 20 --no-pager`.

Todos os comandos opcionais usam `|| true` — não aborta se a ferramenta não estiver disponível.

---

## `multicortex-menu.sh`

**Localização:** `scripts/system/multicortex-menu.sh`  
(cópia em `suse/.../root/opt/multicortex/scripts/system/`)

**Chamado por:** comando `multicortex-menu` ou alias `mc-menu`

Loop `while true` com `clear` antes de cada iteração. Menu via heredoc `cat <<'MENU'`. O `read` aguarda a opção.

**`run()`:** imprime `>>> comando`, executa, depois pausa com `read -r -p "Enter para voltar..."` — evita que a saída desapareça imediatamente ao limpar a tela.

**`service_cmd()`:** tenta `sudo systemctl action svc`; se falhar, tenta sem sudo. Usa `|| true` para não abortar.

**`show_urls()`:** URLs hardcoded (11434, 3000, 8080) + IPs reais via `ip -4 addr show scope global`.

**`test_api()`:** `curl -fsS http://127.0.0.1:11434/api/tags` — JSON bruto para diagnóstico rápido sem sair do menu.

| Opção | Execução |
|-------|---------|
| 1 | `multicortex-status` |
| 2 / 3 / 4 | start / stop / restart `ollama.service` |
| 5 / 6 / 7 | start / stop / restart `multicortex-chat-ui` + `open-webui` |
| 8 | `multicortex-models-list` |
| 9 / 10 / 11 / 12 | modelos light / medium / code / large |
| 13 | `curl` na API Ollama |
| 14 | IPs e URLs |
| 15 | `exit 0` |

---

## `initMulticortex.sh`

**Localização:** `suse/.../root/usr/bin/initMulticortex.sh`  
**Chamado por:** `init.desktop` no autostart do GNOME (a cada login do `tux`)

```bash
cat /etc/multicortex.asc    # logo ASCII (arquivo não está no overlay — pendência)
echo "Initializing..."
ollama run llama3.2 "Ola!"
```

Dispara no login gráfico em um terminal. Se `llama3.2` não estiver instalado, o Ollama tenta baixar da internet ou falha com mensagem de erro. O terminal fica aberto para uso interativo após a resposta inicial.

---

## `config_osviacam.sh`

**Localização:** `suse/.../root/usr/bin/config_osviacam.sh`  
**Chamado por:** `config.desktop` no autostart (executa **apenas uma vez**)

```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface monospace-font-name 'Monospace 12'
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"
rm /home/tux/.config/autostart/config.desktop
```

Configura dock (Firefox, Terminal, Chat), fonte monoespaçada, tema Dark e wallpaper via `gsettings`. Por fim **remove o próprio arquivo de autostart** — na inicialização seguinte esse script não roda mais.

---

## `exo` (script do usuário tux)

**Localização:** `suse/.../root/home/tux/bin/exo`  
**Chamado por:** usuário manualmente

```bash
cd ~/exo
source .venv/bin/activate
exo
```

Ativa um virtualenv Python e executa o framework [exo](https://github.com/exo-explore/exo), que distribui a execução de um LLM entre múltiplos dispositivos na rede local. O diretório `~/exo` e o venv **não estão na ISO** — instalar manualmente:

```bash
mkdir ~/exo && cd ~/exo
python3.12 -m venv .venv
source .venv/bin/activate
pip install exo-inference
```

---

## `config.sh` — script de build KIWI

**Localização:** `suse/x86_64/suse-leap-15.6-JeOS/config.sh`  
**Executado por:** KIWI NG dentro do chroot da imagem durante o build. Roda como root com acesso ao sistema de arquivos não comprimido.

### Sequência de execução

**1. Carrega funções do KIWI:**
```bash
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile
```
Importa `suseSetupProduct`, `suseInsertService`, `baseUpdateSysConfig`, etc.

**2. Setup do produto:**
```bash
suseSetupProduct      # cria /etc/products.d/baseproduct symlink
suseImportBuildKey    # importa chaves GPG da SUSE no banco RPM
```

**3. Otimização do zypper:**
```bash
sed -i -e 's/# solver.onlyRequires.*/solver.onlyRequires = true/' /etc/zypp/zypp.conf
```
Instala apenas dependências `Requires`, ignorando `Recommends`. Evita centenas de pacotes desnecessários.

**4. Sysconfig:**
```bash
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER_AUTOLOGIN tux
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER gdm
baseUpdateSysConfig /etc/sysconfig/windowmanager DEFAULT_WM gnome
```
Define autologin do `tux`, GDM e GNOME dentro da imagem em construção.

**5. Preparação do overlay:**
- Cria `/studio/`, copia `.profile` e `config.xml` para lá
- Remove `/studio/overlay-tmp`
- Comenta os scripts legados de tema GDM/GNOME (usavam `gconftool-2` inexistente no GNOME 3)

**6. Ativação de serviços:**
```bash
suseInsertService sshd
suseInsertService ollama
suseInsertService multicortex-chat-ui
```
Equivalente a `systemctl enable` dentro do chroot. Cria links em `/etc/systemd/system/multi-user.target.wants/`.

**7. Limpeza e finalização:**
```bash
rm -rf /usr/share/doc/packages/*
rm -rf /opt/kde*
/sbin/ldconfig          # reconstrói cache do linker dinâmico
baseSetRunlevel 5       # graphical.target
exit 0
```

> **Bug conhecido:** o bloco `# BEGIN MULTICORTEX EXO GENERATED CONFIG` está posicionado **após o `exit 0`** e nunca executa. Os `mkdir /var/lib/ollama`, `chmod` nos scripts e `systemctl enable` do bloco são código morto. O `multicortex-firstboot.service` (overlay) supre a criação dos diretórios no boot.

---

## `gerar_iso_multicortex_completo_py36.py`

**Localização:** `scripts/gerar_iso_multicortex_completo_py36.py`  
**Executado por:** root no host openSUSE Leap 15.6  
**Compatibilidade:** Python 3.6+ (stdlib apenas)

### Funções internas

**`is_root()`** — verifica `os.geteuid() == 0`.

**`read_os_release()`** — parseia `/etc/os-release` linha a linha, retorna dicionário.

**`default_workdir()`** — retorna `/home/hawk/builds` se existir, senão `~/builds`.

**`ensure_host_packages()`** — `zypper refresh` + instala dependências. Se `kiwi-ng` não for encontrado, adiciona o repositório KIWI Builder e reinstala. Valida com `kiwi-ng --version`.

**`clone_or_update(workdir)`** — `git clone` ou `git pull --ff-only` do repositório `cabelo/multicortex-exo`. Valida existência do descritor KIWI.

**`copy_kiwi_descriptor(repo_dir, workdir)`** — `shutil.copytree` com `symlinks=True`. Apaga destino anterior se existir.

**`add_package_to_bootstrap(xml, package)`** — localiza `<packages type="bootstrap">` via regex `re.DOTALL`, insere o pacote se ainda não estiver. Idempotente.

**`add_repository_before_packages(xml, repo_xml, unique_text)`** — verifica se `unique_text` já está no XML antes de inserir. Idempotente.

**`patch_config_xml(kiwi_desc)`** — orquestra todas as modificações:
  - Substituições de URL via `str.replace` (dicionário de `old → new`)
  - Adiciona repositórios non-oss e NVIDIA
  - Garante `ca-certificates-mozilla` e `openssl` no bootstrap
  - Garante os 5 pacotes NVIDIA G06 no bloco image
  - Comenta `baseMount`/`baseCleanMount` no `config.sh`
  - Imprime relatório de repositórios, pacotes NVIDIA e bootstrap

**`build_iso(workdir, kiwi_desc)`** — apaga e recria `workdir/out/`. Executa `kiwi-ng` via `subprocess.Popen` com saída em tempo real gravada em log. Verifica código de retorno e presença de `.iso` na saída.

**`main()`** — parseia argumentos, chama as funções em ordem, reporta resultado.

---

## Scripts legados (`studio/`)

Herdados do SUSE Studio. Todos comentados ou não executados no build atual.

**`configure_gdm_theme.sh`** — configura tema GDM com `gconftool-2`. **Não executa** — comentado no `config.sh` porque `gconftool-2` não existe no GNOME 3.

**`configure_gnome_background.sh`** — configura wallpaper e dock via `gsettings`. **Não executa** — desabilitado junto com o anterior para evitar falha na linha `gconftool-2`.

**`firstboot_scripts/config.sh`** — configura GNOME via `gsettings` e faz `c_rehash` (reconstrói hashes de certificados SSL). **Não executa** no build atual.

---

## `suse_studio_firstboot`

**Localização:** `suse/.../root/etc/init.d/suse_studio_firstboot`  
**Chamado por:** `suse-studio-firstboot.service` na primeira inicialização

Detecta todas as interfaces Ethernet em `/sys/class/net/` e configura DHCP para cada uma. Em modo "Testdrive" (VM do SUSE Studio), desativa efeitos visuais do KDE e vmtoolsd.

Configura GNOME: dock, fonte monoespaçada, tema Dark, wallpaper.

Ao final **se auto-desativa e se auto-deleta**:
```bash
systemctl disable suse-studio-firstboot
rm -f /etc/systemd/system/suse-studio-firstboot.service
rm -f /etc/init.d/suse_studio_firstboot
```

Executa uma única vez.
