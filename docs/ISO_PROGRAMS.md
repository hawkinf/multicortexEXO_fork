# Programas da ISO — Inventário Completo

Documentação de todos os programas, scripts, arquivos de configuração e componentes presentes na ISO multicortexEXO. Dividida em desenvolvimentos próprios do fork, programas de terceiros incluídos, e infraestrutura de sistema.

---

## Desenvolvimentos próprios do fork

São os arquivos criados ou modificados diretamente neste repositório. Tudo que está em `suse/x86_64/suse-leap-15.6-JeOS/root/` é copiado pelo KIWI para dentro da ISO.

---

### `multicortex-status.sh`

**Localização na ISO:** `/opt/multicortex/scripts/system/multicortex-status.sh`  
**Fonte no repo:** `scripts/system/multicortex-status.sh`  
**Chamado por:** comando `multicortex-status` ou alias `mc-status`

Script de diagnóstico completo do sistema. Exibe seções formatadas em azul ciano com `\033[1;36m`:

- **Versão:** lê `/etc/multicortex-version` ou `./VERSION`
- **Sistema:** hostname, versão do kernel (`uname -r`), arquitetura (`uname -m`), `PRETTY_NAME` e `VERSION_ID` do `/etc/os-release`
- **Rede:** IPs globais via `ip -4 addr show scope global` formatado com `awk`; URLs prováveis de todos os serviços (Ollama API em 11434, Web UI em 3000, Open WebUI em 8080)
- **Serviços:** estado de `ollama.service`, `multicortex-chat-ui.service`, `open-webui.service` via `systemctl is-active`
- **Ollama API:** `curl -fsS http://127.0.0.1:11434/api/tags` → lista modelos com `jq` ou JSON bruto
- **Modelos:** `ollama list` em formato tabular
- **Hardware:** model name da CPU via `lscpu | awk`; RAM via `free -h`; disco via `df -h /`; saída completa do `nvidia-smi` se disponível
- **Logs:** `journalctl -u ollama.service -n 20 --no-pager`

Usa `set -Eeuo pipefail` e `|| true` em todos os comandos opcionais — não aborta se alguma ferramenta não estiver disponível.

---

### `multicortex-menu.sh`

**Localização na ISO:** `/opt/multicortex/scripts/system/multicortex-menu.sh`  
**Fonte no repo:** `scripts/system/multicortex-menu.sh`  
**Chamado por:** comando `multicortex-menu` ou alias `mc-menu`

Menu interativo de controle do sistema. Loop `while true` com `clear` antes de cada iteração. Menu via heredoc `cat <<'MENU'`.

| Opção | Ação |
|-------|------|
| 1 | `multicortex-status` |
| 2 / 3 / 4 | start / stop / restart `ollama.service` |
| 5 / 6 / 7 | start / stop / restart `multicortex-chat-ui` + `open-webui` |
| 8 | `multicortex-models-list` |
| 9 / 10 / 11 / 12 | instalar modelos light / medium / code / large |
| 13 | teste da API Ollama via `curl` |
| 14 | IPs e URLs do sistema |
| 15 | sair |

Funções internas: `run()` pausa com Enter após cada comando. `service_cmd()` tenta `sudo systemctl` com fallback sem sudo. `show_urls()` exibe URLs hardcoded + IPs reais. `test_api()` chama `curl` na porta 11434.

---

### `initMulticortex.sh`

**Localização na ISO:** `/usr/bin/initMulticortex.sh`  
**Fonte no repo:** `suse/.../root/usr/bin/initMulticortex.sh`  
**Chamado por:** autostart `init.desktop` no login do GNOME do usuário `tux`

```bash
cat /etc/multicortex.asc
echo "Initializing..."
ollama run llama3.2 "Ola!"
```

Exibe o logo ASCII (arquivo `/etc/multicortex.asc` — pendência: não está no overlay) e inicia uma conversa com o modelo `llama3.2`. Se o modelo não estiver instalado, tenta download ou falha. O terminal fica aberto para uso interativo após a resposta.

---

### `config_osviacam.sh`

**Localização na ISO:** `/usr/bin/config_osviacam.sh`  
**Fonte no repo:** `suse/.../root/usr/bin/config_osviacam.sh`  
**Chamado por:** autostart `config.desktop` — executa **uma única vez** no primeiro login

```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface monospace-font-name 'Monospace 12'
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"
rm /home/tux/.config/autostart/config.desktop
```

Configura a aparência do GNOME via `gsettings` e se auto-remove do autostart. O nome do script é herança do projeto VICAM (visão computacional com câmera) do upstream; a funcionalidade atual não tem relação com câmera.

---

### `exo` (wrapper do usuário tux)

**Localização na ISO:** `/home/tux/bin/exo`  
**Fonte no repo:** `suse/.../root/home/tux/bin/exo`  
**Chamado por:** usuário manualmente

```bash
cd ~/exo
source .venv/bin/activate
exo
```

Wrapper de conveniência para o framework de inferência distribuída exo. Pressupõe instalação manual de `~/exo/.venv`. Ver [EXO_CLUSTER.md](EXO_CLUSTER.md) para instalação e uso completo.

---

### `gerar_iso_multicortex_completo_py36.py`

**Localização no repo:** `scripts/gerar_iso_multicortex_completo_py36.py`  
**Não está dentro da ISO** — é executado no host para gerar a ISO

Script Python 3.6+ que automatiza o build completo:

1. Verifica root (`os.geteuid() == 0`)
2. Detecta SO via `/etc/os-release`
3. Instala `kiwi-ng` e dependências via zypper (com fallback para o repositório KIWI Builder)
4. Clona ou atualiza `cabelo/multicortex-exo` via `git pull --ff-only`
5. Copia o descritor KIWI para `workdir/kiwi-desc/`
6. Patcha o `config.xml`: HTTPS→HTTP, adiciona repos non-oss e NVIDIA, garante pacotes bootstrap críticos, garante os 5 pacotes NVIDIA G06
7. Patcha o `config.sh`: comenta `baseMount`/`baseCleanMount` para compatibilidade com KIWI 10
8. Executa `kiwi-ng --debug system build` com output em tempo real via `subprocess.Popen`

Argumentos: `--clean` (apaga workdir), `--no-install` (pula zypper), `--workdir PATH`.

---

### `/etc/motd`

**Localização na ISO:** `/etc/motd`  
**Fonte no repo:** `suse/.../root/etc/motd`

Mensagem exibida no terminal após login SSH ou console:

```
MultiCortex EXO Live

Comandos úteis:
  multicortex-menu
  multicortex-status
  multicortex-models-light
  multicortex-models-medium
  multicortex-models-code
  multicortex-models-large
  multicortex-models-list

Usuários padrão desta imagem, se mantidos no config.xml:
  root / linux
  tux  / linux

Troque as senhas antes de usar em rede ou publicar ISO final.
```

---

### `/etc/multicortex-version`

**Localização na ISO:** `/etc/multicortex-version`  
**Fonte no repo:** `suse/.../root/etc/multicortex-version`

Arquivo de uma linha com a string de versão da ISO:

```
0.99 Build 20260609 11:17
```

Lido pelo `multicortex-status.sh`. Deve ser atualizado a cada novo build antes de gerar a ISO.

---

### `/etc/profile.d/multicortex.sh`

**Localização na ISO:** `/etc/profile.d/multicortex.sh`  
**Fonte no repo:** `suse/.../root/etc/profile.d/multicortex.sh`

Carregado automaticamente para todos os usuários em qualquer shell de login:

```bash
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

Define o endereço do Ollama (sobrescrevível via variável de ambiente) e os aliases curtos para os comandos multicortex.

---

### `multicortex-firstboot.service`

**Localização na ISO:** `/etc/systemd/system/multicortex-firstboot.service`  
**Fonte no repo:** `suse/.../root/etc/systemd/system/multicortex-firstboot.service`

```ini
[Unit]
Description=MultiCortex EXO first boot preparation
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/bin/bash -lc 'mkdir -p /var/lib/ollama /var/log/multicortex; chmod 755 /var/lib/ollama /var/log/multicortex || true'
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Cria `/var/lib/ollama` (onde o Ollama armazena modelos) e `/var/log/multicortex` com permissão 755 na primeira inicialização. Existe porque o bloco do `config.sh` que criaria esses diretórios está após o `exit 0` e nunca executa.

---

### `Chat.desktop`

**Localização na ISO:** `/usr/share/applications/Chat.desktop`  
**Fonte no repo:** `suse/.../root/usr/share/applications/Chat.desktop`

Atalho GNOME que abre o Firefox diretamente em `http://localhost:7001`:

```ini
Exec=/usr/bin/firefox http://localhost:7001
Icon=/usr/share/pixmaps/chat.png
Name=Chat
```

Aparece na dock do GNOME ao lado do Firefox e do Terminal. Serve como ponto de entrada para qualquer interface web de chat (Open WebUI, multicortex-chat-ui, ou similar) configurada na porta 7001.

---

### Autostart `init.desktop`

**Localização na ISO:** `/home/tux/.config/autostart/init.desktop`  
**Fonte no repo:** `suse/.../root/home/tux/.config/autostart/init.desktop`

```ini
Type=Application
Terminal=true
Exec=/usr/bin/initMulticortex.sh
```

Chama `initMulticortex.sh` em um terminal no login do GNOME do usuário `tux`. Executa a cada login.

---

### Autostart `config.desktop`

**Localização na ISO:** `/home/tux/.config/autostart/config.desktop`  
**Fonte no repo:** `suse/.../root/home/tux/.config/autostart/config.desktop`

```ini
Type=Application
Terminal=true
Exec=/usr/bin/config_osviacam.sh
```

Chama `config_osviacam.sh` no primeiro login. O script se auto-remove ao terminar — não executa mais nas inicializações seguintes.

---

### `/etc/ld.so.conf.d/cuda.conf`

**Localização na ISO:** `/etc/ld.so.conf.d/cuda.conf`  
**Fonte no repo:** `suse/.../root/etc/ld.so.conf.d/cuda.conf`

```
/usr/local/cuda-12.6/targets/x86_64-linux/lib
```

Configura o linker dinâmico para encontrar as bibliotecas CUDA em `/usr/local/cuda-12.6/`. As libs devem ser instaladas manualmente nesse diretório — a ISO inclui apenas os drivers de runtime NVIDIA G06, não o CUDA Toolkit completo. Ver `/usr/local/cuda/readme.txt` dentro da ISO.

---

### `/etc/sysconfig/network/ifcfg-lan0`

**Localização na ISO:** `/etc/sysconfig/network/ifcfg-lan0`  
**Fonte no repo:** `suse/.../root/etc/sysconfig/network/ifcfg-lan0`

```
BOOTPROTO='dhcp'
MTU=''
REMOTE_IPADDR=''
STARTMODE='onboot'
```

Configura a interface de rede `lan0` para DHCP automático. A regra udev `70-persistent-net.rules` nomeia a primeira interface Ethernet como `lan0`.

---

### `/etc/udev/rules.d/70-persistent-net.rules`

**Localização na ISO:** `/etc/udev/rules.d/70-persistent-net.rules`  
**Fonte no repo:** `suse/.../root/etc/udev/rules.d/70-persistent-net.rules`

```
SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", ATTR{address}=="?*", ATTR{dev_id}=="0x0", ATTR{type}=="1", KERNEL=="?*", NAME="lan0"
```

Nomeia qualquer interface Ethernet como `lan0` independente do hardware. Garante que a configuração em `ifcfg-lan0` sempre se aplique à interface cabeada, independente do nome que o kernel atribuiria (eth0, enp3s0, etc.).

---

### Repositórios pré-configurados

**Localização na ISO:** `/etc/zypp/repos.d/`  
**Fonte no repo:** `suse/.../root/etc/zypp/repos.d/`

Três repositórios disponíveis para uso após o boot sem configuração adicional:

**`jax_15.6.repo`** — repositório `home:cabelo:jax`:
```ini
[JAX_15.6]
baseurl=http://download.opensuse.org/repositories/home:cabelo:jax/15.6/
enabled=1
gpgcheck=1
```
Repositório do autor do projeto original (Alessandro Faria/CABELO). Contém pacotes de IA: Ollama, OpenVINO, OpenCV com módulo DNN, e outras bibliotecas. É daqui que o Ollama é instalado durante o build.

**`openSUSE_Leap_15.6_OSS.repo`** — repositório base do openSUSE Leap 15.6.

**`openSUSE_Leap_15.6_Updates.repo`** — atualizações de segurança do openSUSE Leap 15.6.

---

### Temas visuais

**Localização no repo:** `suse/x86_64/suse-leap-15.6-JeOS/usr/share/`  
**Empacotados como:** `gdm.tar` e `plymouth.tar` no `config.xml`

#### Tema GRUB2 (`grub2/themes/studio/`)

Define a aparência do menu de boot:

- `background.png` — fundo do menu de boot
- `theme.txt` — configuração do layout:
  - Menu centralizado (18% da esquerda, 64% de largura, 33% do topo)
  - Fonte DejaVu Sans Bold 14pt para itens
  - Barra de progresso de timeout em verde (`#63a63d`) sobre preto
  - Item selecionado: pixmap `select_*.png`, texto preto
  - Scrollbar de 20px com thumb em pixmap `slider_*.png`
- Fontes `.pf2` (DejaVu 10/12/14pt, ascii)
- Script `activate-theme` — aplica o tema ao GRUB2

#### Tema Plymouth (`plymouth/themes/studio/`)

Splash screen durante o boot (kernel → systemd):

- `background.png` — fundo (1.1 MB — imagem em resolução alta)
- `logo.png` — logotipo exibido no centro (25 KB)
- `openSUSE.script` — script de animação Plymouth em linguagem própria
- `studio.plymouth` — arquivo de definição do tema
- `progress-0/1/2.png` — quadros da animação da barra de progresso
- `progress_bar.png`, `progress_box.png`, `progress_box_background.png`, `progress_box_edge.png` — componentes visuais da barra
- `box.png`, `entry.png` — caixas de entrada de senha (unlock screen)
- `bullet.png` — indicador de caractere digitado
- `lock.png`, `hibernate.png` — ícones de estado
- `/etc/plymouth/plymouthd.conf` — aponta para o tema: `Theme=studio`

#### Tema GDM (`gdm/themes/studio/`)

Tela de login gráfico:

- `background.jpg` (281 KB) e `background.png` (1.1 MB) — fundo da tela de login
- `logo.png` — logotipo (27 KB)
- `dots.png` — elemento decorativo
- `preview.png` (39 KB) — thumbnail usado pelo seletor de tema GDM
- `studio.xml` — XML de definição do tema GDM (cores, posicionamento)
- `GdmGreeterTheme.desktop` — metadados do tema

#### Tema GFXBOOT (`gfxboot/themes/studio/`)

Tela de boot para BIOS legacy (antes do GRUB2 no modo UEFI):

- `data-boot/` — assets para o modo de boot
- `data-install/` — assets para o modo de instalação
- `config` — configuração do tema
- `Makefile` — symlink para `../openSUSE/Makefile` (herda o processo de build do tema openSUSE)

#### Wallpaper (`wallpapers/`)

- `studio_wallpaper.jpg` (281 KB) — wallpaper padrão do GNOME Desktop
- `studio-wallpaper.xml` — arquivo de definição para o sistema de wallpapers do GNOME (permite troca automática e ajuste por resolução)

---

### `backup-pasta`

**Localização na ISO:** `studio/overlay-tmp/files/backup-pasta` (não instalado como comando)  
**Fonte no repo:** `suse/.../root/studio/overlay-tmp/files/backup-pasta`

```bash
tar -zcvf $1.$(date +%y%m%d-%H%M%S).tar.gz $1
```

Script de backup compactado com timestamp. Cria um `.tar.gz` do caminho passado como argumento, nomeado com data e hora no formato `AAMMDD-HHMMSS`. Exemplo de uso:

```bash
backup-pasta /home/tux/projetos
# gera: /home/tux/projetos.260609-143022.tar.gz
```

O script está em `overlay-tmp/files/` e a linha que o instalaria em `/usr/local/bin/` está **comentada** no `config.sh`:

```bash
# mv /studio/overlay-tmp/files/backup-pasta /usr/local/bin/backup-pasta
# chown root:users /usr/local/bin/backup-pasta
# chmod 755 /usr/local/bin/backup-pasta
```

Para ativar: descomente essas linhas no `config.sh` antes de gerar a ISO.

---

### `runMonero`

**Localização na ISO:** `studio/overlay-tmp/files/runMonero`  
**Fonte no repo:** `suse/.../root/studio/overlay-tmp/files/runMonero`

```bash
#/usr/bin/gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Shell.desktop','google-chrome.desktop']"
#/usr/bin/gsettings set org.gnome.desktop.interface monospace-font-name 'Monospace 12'
#/usr/bin/gsettings set org.gnome.desktop.interface gtk-theme Dark
```

Arquivo com apenas comentários — todo o conteúdo está comentado com `#`. É um resquício do projeto original que provavelmente incluía mineração de Monero (XMR) numa versão anterior. Não tem efeito nenhum na ISO atual.

---

### `manifesto.xml`

**Localização na ISO:** `studio/manifesto.xml`  
**Fonte no repo:** `suse/.../root/studio/manifesto.xml`

Manifesto legado do **SUSE Studio** (plataforma descontinuada de criação de appliances online). Contém a definição original do projeto `OSAR_OpenSUSE_Augmented_Reality` em openSUSE Leap 42.1, criado por Alessandro Faria (CABELO) em 2017 (UUID `8c7f385c-19b7-11e7-f0b0-4fbb28ae4d82`).

Mostra a origem do projeto: era uma ISO de realidade aumentada com OpenSceneGraph, osgART, GIMP, Blender e câmera (Cheese). O multicortexEXO é a evolução dessa ISO para IA generativa. Não tem efeito funcional — é documentação histórica.

---

### `config.sh` (script de build KIWI)

**Localização no repo:** `suse/x86_64/suse-leap-15.6-JeOS/config.sh`  
**Executado por:** KIWI NG dentro do chroot durante o build — não está na ISO final

Configura a imagem durante o build: autologin do `tux`, GDM, GNOME, habilita serviços (sshd, ollama, multicortex-chat-ui), remove docs, ldconfig, runlevel 5.

**Bug crítico:** o bloco `MULTICORTEX EXO GENERATED CONFIG` está após o `exit 0` e nunca executa.

---

## Programas de terceiros incluídos na ISO

### Ollama

**Pacote:** `ollama` (do repositório `home:cabelo:jax`)  
**Porta:** `127.0.0.1:11434`  
**Serviço:** `ollama.service` — habilitado no boot

Motor de inferência LLM local. Gerencia download, carregamento e execução de modelos. Expõe API REST compatível com OpenAI.

```bash
ollama list                          # listar modelos instalados
ollama pull llama3.1:8b              # baixar modelo
ollama run llama3.1:8b "pergunta"    # rodar modelo
```

Modelos armazenados em `/var/lib/ollama/models/`. Ver [MODELS.md](MODELS.md) para os perfis de instalação.

---

### Firefox

**Pacote:** `MozillaFirefox`

Browser. Usado como interface para serviços web locais:
- Atalho `Chat` na dock → `http://localhost:7001`
- Acesso direto à API Ollama → `http://127.0.0.1:11434`

---

### GNOME Desktop

**Pacotes:** `patterns-gnome-gnome_basis`, `gnome_basis_opt`, `gnome_x11`, `gnome_utilities`, `gnome_internet`, `gnome_imaging`, `gnome_basic`, `gnome_yast`, `sw_management_gnome`

Ambiente desktop completo. Sobe automaticamente via GDM com autologin do usuário `tux`. Inclui: GNOME Shell, Nautilus, GNOME Terminal, GNOME Settings, Calculadora, Monitor do Sistema, visualizador de imagens.

---

### GDM

**Incluído via:** `patterns-gnome-gnome_basis`

Gerenciador de display. Configurado para autologin do `tux` via `DISPLAYMANAGER_AUTOLOGIN=tux` no sysconfig.

---

### GNOME Terminal

**Pacote:** `gnome-terminal`, `gnome-terminal-lang`

Terminal emulador. É onde os comandos `multicortex-*` são executados. O autostart `init.desktop` abre um terminal ao logar.

---

### Cheese

**Pacote:** `cheese`, `cheese-lang`

Aplicativo de câmera. Herdado do projeto original VICAM/OSAR (visão computacional). Permite captura de imagem e vídeo pela câmera.

---

### NetworkManager

**Pacote:** `NetworkManager-gnome`, `NetworkManager-gnome-lang`

Gerenciamento de rede com interface gráfica. Permite configurar Wi-Fi e redes cabeadas sem editar arquivos de configuração. O applet aparece na barra de sistema do GNOME.

---

### wpa_supplicant-gui

**Pacote:** `wpa_supplicant-gui`

Interface gráfica para autenticação em redes Wi-Fi WPA/WPA2/WPA3 empresariais. Complementa o NetworkManager para redes corporativas.

---

### YaST2

**Pacotes:** `yast2-control-center-gnome`, `yast2-x11`

Painel de controle do openSUSE. Configuração gráfica do sistema: usuários, partições, serviços, firewall, rede. Disponível no menu de aplicativos.

---

### OpenSSH

**Pacote:** `openssh`  
**Serviço:** `sshd.service` — habilitado no boot  
**Porta:** 22

Servidor SSH. Acesso remoto: `ssh tux@<ip>` ou `ssh root@<ip>`. Credenciais padrão: `linux`.

---

### Python 3.12

**Pacotes:** `python312`, `python312-pip`, `python312-setuptools`, `python312-base`

Python 3.12 com pip e setuptools. Adicionado explicitamente porque o Leap 15.6 tem Python 3.6 por padrão — incompatível com a maioria das bibliotecas modernas de IA (LangChain, transformers, etc. requerem ≥ 3.9).

Também presentes: `python3-base`, `python3-devel`, `python3-pip` — versão do sistema para compatibilidade com ferramentas openSUSE.

---

### Node.js 20 + npm

**Pacotes:** `nodejs20`, `npm20`, `nodejs-common`

Runtime JavaScript e gerenciador de pacotes. Necessário para Open WebUI, interfaces web de chat baseadas em Next.js/React, e outras ferramentas de frontend para IA.

---

### Compiladores e ferramentas de build

| Pacote | Função |
|--------|--------|
| `gcc`, `gcc-c++` | Compiladores C e C++ |
| `cmake` | Sistema de build (usado por OpenCV, llama.cpp) |
| `make` | Build clássico via Makefile |
| `ninja` | Backend rápido do cmake |
| `scons` | Build alternativo (usado por OpenVINO) |
| `pkg-config` | Localiza bibliotecas de desenvolvimento |
| `git`, `git-lfs` | Controle de versão; git-lfs para repositórios Hugging Face com modelos grandes |
| `ccache` | Cache de compilação — reduz recompilações de projetos C/C++ |
| `patchelf` | Modifica RPATH de binários ELF |
| `fdupes` | Remove arquivos duplicados |
| `ShellCheck` | Análise estática de scripts Shell |

---

### Bibliotecas de computação e visão

| Pacote | Função |
|--------|--------|
| `opencv-devel` | OpenCV — visão computacional, DNN module |
| `opencl-headers`, `opencl-cpp-headers`, `ocl-icd-devel` | OpenCL — computação paralela em GPU genérica |
| `tbb-devel` | Intel TBB — paralelismo em CPU para OpenCV e frameworks de IA |
| `libva-devel`, `vaapi-intel-driver` | VA-API Intel — aceleração de vídeo por hardware |
| `libvdpau_nouveau` | VDPAU — aceleração de vídeo para GPUs Nouveau |
| `protobuf-devel` | Serialização usada por TensorFlow, ONNX |
| `nlohmann_json-devel` | JSON header-only para C++ (usado por llama.cpp) |
| `snappy-devel` | Compressão rápida usada por TensorFlow e RocksDB |
| `zlib-devel` | Compressão base |
| `gflags-devel-static` | Flags de linha de comando para C++ (Caffe, TensorFlow) |
| `pugixml-devel` | Parser XML leve para C++ (OpenVINO) |
| `ade-devel` | Grafos de computação para OpenCV DNN |

---

### Drivers NVIDIA G06

| Pacote | Função |
|--------|--------|
| `nvidia-drivers-insync-latest` | Meta-pacote do driver mais recente sincronizado com o kernel |
| `nvidia-common-G06` | Arquivos comuns compartilhados entre os componentes G06 |
| `nvidia-compute-G06` | Bibliotecas CUDA runtime — necessário para Ollama usar GPU |
| `nvidia-compute-utils-G06` | `nvidia-persistenced` e utilitários de compute |
| `nvidia-utils-G06` | `nvidia-smi` para monitoramento |
| `nvidia-driver-G06-kmp-default` | Módulo do kernel (`.ko`) compilado para o `kernel-default` |

Os drivers são instalados pelo repositório `https://download.nvidia.com/opensuse/leap/15.6/`.

---

### Hardware Intel e firmware

| Pacote | Função |
|--------|--------|
| `ucode-intel` | Microcódigo para processadores Intel (corrige bugs via firmware) |
| `libdrm_intel1` | DRM Intel para renderização acelerada |
| `libdrm_nouveau2` | DRM Nouveau (NVIDIA open source) |
| `libvdpau_nouveau` | VDPAU para GPUs Nouveau |
| `xf86-video-intel` | Driver Xorg para Intel HD/UHD Graphics |
| `vaapi-intel-driver` | VA-API para decodificação de vídeo hardware Intel |
| `kernel-firmware` | Firmwares genéricos de hardware |
| `atmel-firmware` | Wi-Fi Atmel |
| `adaptec-firmware` | Controladoras RAID Adaptec |
| `bluez-firmware` | Bluetooth BlueZ |
| `alsa-firmware` | Áudio ALSA |
| `ipw-firmware` | Wi-Fi Intel IPW |
| `mpt-firmware` | Controladoras MPT/LSI |
| `FirmwareUpdateKit` | Ferramenta de atualização de firmware UEFI |
| `iw` | Ferramenta de configuração de interfaces Wi-Fi |
| `wpa_supplicant-gui` | Wi-Fi WPA empresarial GUI |

---

### Kernel e bootloader

| Pacote | Função |
|--------|--------|
| `kernel-default` | Kernel Linux do openSUSE Leap 15.6 |
| `grub2` | Bootloader principal |
| `grub2-x86_64-efi` | GRUB2 para UEFI |
| `grub2-i386-pc` | GRUB2 para BIOS legacy |
| `grub2-branding-openSUSE` | Branding do GRUB2 |
| `shim` | Shim para UEFI Secure Boot |
| `syslinux` | Bootloader BIOS legacy alternativo (ISO híbrida) |
| `gfxboot-branding-openSUSE`, `gfxboot-devel` | Tela de boot gráfica BIOS |
| `plymouth`, `plymouth-branding-openSUSE`, `plymouth-dracut`, `plymouth-plugin-script` | Splash screen animado |
| `dracut-kiwi-live` | Módulo dracut para boot Live com overlay SquashFS |
| `dracut-kiwi-oem-repart`, `dracut-kiwi-oem-dump` | Módulos para instalação em disco (builds OEM) |

---

### Utilitários de sistema

| Pacote | Função |
|--------|--------|
| `openssh` | Servidor SSH |
| `iproute2` | Ferramentas modernas de rede (`ip`, `ss`) |
| `dhcp-client` | Cliente DHCP |
| `iputils` | `ping`, `tracepath` |
| `ifplugd` | Detecta conexão/desconexão de cabo de rede |
| `lvm2` | Gerenciador de volumes lógicos |
| `e2fsprogs` | Ferramentas ext2/3/4 (necessário para a partição de persistência) |
| `parted` | Particionamento de disco |
| `zypper` | Gerenciador de pacotes openSUSE |
| `vim` | Editor de texto (syntax off na ISO — sem plugin de sintaxe) |
| `bash-completion` | Auto-completar de comandos no bash |
| `less` | Paginador de texto |
| `tar` | Compactação/descompactação |
| `which` | Localiza executáveis no PATH |
| `openssl` | SSL/TLS e ferramentas criptográficas |
| `ca-certificates`, `ca-certificates-mozilla` | Certificados CA raiz |
| `jeos-firstboot` | Assistente de primeira inicialização JeOS |
| `checkmedia` | Verificação de integridade da mídia (mediacheck no boot) |
| `timezone` | Dados de fuso horário |
| `glibc-locale` | Localizações do sistema |
| `fontconfig`, `fonts-config` | Configuração de fontes |
| `xorg-x11`, `xorg-x11-driver-input`, `xorg-x11-driver-video`, `xorg-x11-fonts` | Xorg e drivers de entrada/vídeo |
| `x11-tools` | Utilitários X11 |
| `sax3` | Ferramenta de configuração do servidor X |
| `gsettings-backend-dconf` | Backend dconf para gsettings (configuração do GNOME) |
| `gvfs-backends` | Backends de sistema de arquivos virtual (rede, MTP, etc.) |
| `libgnomesu` | Escalonamento de privilégios para aplicativos GNOME |
| `gnote` | Editor de notas GNOME |
| `wallpaper-branding-openSUSE` | Wallpapers padrão do openSUSE |
| `module-init-tools` | Ferramentas para módulos do kernel |
| `filesystem` | Estrutura de diretórios FHS |
| `cracklib-dict-full` | Dicionário para validação de senhas |
| `openSUSE-release` | Identificação da distribuição |

---

## Infraestrutura legada (não executada)

Arquivos herdados do projeto original que permanecem na ISO mas não têm efeito.

### `studio/configure_gdm_theme.sh`

Configurava o tema GDM com `gconftool-2` (GNOME 2). **Não executa** — comentado no `config.sh` porque `gconftool-2` não existe no GNOME 3.

### `studio/configure_gnome_background.sh`

Configurava wallpaper e dock com `gsettings`. **Não executa** — desabilitado junto com o anterior.

### `studio/runMonero`

Arquivo com todo o conteúdo comentado. Resquício de uma versão anterior do upstream.

### `studio/manifesto.xml`

Manifesto do SUSE Studio datado de 2017, projeto `OSAR_OpenSUSE_Augmented_Reality`. Documentação histórica da origem do projeto.

### `suse-studio-firstboot.service` e `suse-studio-custom.service`

Serviços legados do SUSE Studio. O `firstboot` executa `/etc/init.d/suse_studio_firstboot` (configura rede DHCP e GNOME) e se auto-deleta. O `custom` executaria `/studio/suse-studio-custom` se existir.

### `grub_config.service`

```ini
ConditionPathExists=/.kiwi_grub_config.trigger
ExecStart=/bin/bash -c 'grub2-mkconfig -o /boot/grub2/grub.cfg'
```

Reconstrói o `grub.cfg` após instalação em disco. Só dispara se `.kiwi_grub_config.trigger` existir — criado pelo KIWI em builds OEM, nunca presente na Live ISO.

### `usr/share/firstboot/scripts/config.sh`

Versão legada do script de firstboot. Configura GNOME via `gsettings` e chama `c_rehash`. Não executado no build atual.

---

## Arquivos pendentes (referenciados mas ausentes)

| Arquivo | Referenciado por | Status |
|---------|-----------------|--------|
| `/etc/multicortex.asc` | `initMulticortex.sh` | Não está no overlay — logo ASCII não é exibido |
| `/usr/local/bin/multicortex-status` | aliases em `profile.d` e `multicortex-menu.sh` | Não criado — comandos não funcionam |
| `/usr/local/bin/multicortex-menu` | aliases em `profile.d` e `multicortex-menu.sh` | Não criado |
| `/usr/local/bin/multicortex-models-*` | aliases em `profile.d` e opções 9–12 do menu | Não criado |
| `multicortex-chat-ui.service` | habilitado no `config.sh` | Arquivo `.service` não está no overlay |
| `scripts/models/install-light-models.sh` | `MODELS.md`, menu opção 9 | Não commitado |
| `scripts/models/install-medium-models.sh` | `MODELS.md`, menu opção 10 | Não commitado |
| `scripts/models/install-code-models.sh` | `MODELS.md`, menu opção 11 | Não commitado |
| `scripts/models/install-large-models.sh` | `MODELS.md`, menu opção 12 | Não commitado |
| `scripts/models/list-installed-models.sh` | aliases e menu opção 8 | Não commitado |
| `scripts/build/build-iso.sh` | `BUILD.md` | Não commitado |
