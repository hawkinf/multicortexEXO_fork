# multicortexEXO

**ISO Linux Live bootável** baseada em **openSUSE Leap 15.6 x86_64**, com ambiente GNOME, suporte a GPU NVIDIA e infraestrutura completa para execução local de modelos de linguagem (LLM) via **Ollama** — sem depender de nuvem, sem enviar dados para fora da máquina.

Fork independente de [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo), com scripts próprios de build, overlay de sistema, documentação técnica e estrutura de evolução autônoma.

---

## Índice

- [O que é e por que usar](#o-que-é-e-por-que-usar)
- [Diferenças em relação a um Linux normal](#diferenças-em-relação-a-um-linux-normal)
- [Programas incluídos e para que servem](#programas-incluídos-e-para-que-servem)
- [Versão e release](#versão-e-release)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Descrição técnica da ISO](#descrição-técnica-da-iso)
- [Scripts — funcionamento detalhado](#scripts--funcionamento-detalhado)
  - [multicortex-status.sh](#multicortex-statussh)
  - [multicortex-menu.sh](#multicortex-menush)
  - [initMulticortex.sh](#initmulticortexsh)
  - [config_osviacam.sh](#config_osvicamsh)
  - [exo (script do usuário tux)](#exo-script-do-usuário-tux)
  - [config.sh — script de build KIWI](#configsh--script-de-build-kiwi)
  - [gerar_iso_multicortex_completo_py36.py](#gerar_iso_multicortex_completo_py36py)
  - [Scripts legados (studio/)](#scripts-legados-studio)
  - [suse_studio_firstboot](#suse_studio_firstboot)
- [Serviços systemd — o que faz cada um](#serviços-systemd--o-que-faz-cada-um)
- [Overlay root — arquivos copiados na ISO](#overlay-root--arquivos-copiados-na-iso)
- [Credenciais padrão](#credenciais-padrão)
- [Walkthrough completo: do comando à ISO rodando](#walkthrough-completo-do-comando-à-iso-rodando)
  - [Visão geral do fluxo](#visão-geral-do-fluxo)
  - [Parte 1 — Execução do script Python](#parte-1--execução-do-script-python)
  - [Parte 2 — O que o KIWI NG faz internamente](#parte-2--o-que-o-kiwi-ng-faz-internamente)
  - [Parte 3 — Do pendrive ao modelo respondendo](#parte-3--do-pendrive-ao-modelo-respondendo)
- [Como compilar a ISO — referência rápida](#como-compilar-a-iso--referência-rápida)
- [Como testar a ISO](#como-testar-a-iso)
- [Como gravar em pendrive](#como-gravar-em-pendrive)
- [Comandos disponíveis na ISO](#comandos-disponíveis-na-iso)
- [API HTTP local do Ollama](#api-http-local-do-ollama)
- [Perfis de modelos de IA](#perfis-de-modelos-de-ia)
- [Persistência de dados](#persistência-de-dados)
- [Edição offline com SSD](#edição-offline-com-ssd)
- [Requisitos de hardware](#requisitos-de-hardware)
- [Diagnóstico e troubleshooting](#diagnóstico-e-troubleshooting)
- [Segurança](#segurança)
- [Estado atual e pendências conhecidas](#estado-atual-e-pendências-conhecidas)
- [Publicar no GitHub Releases](#publicar-no-github-releases)
- [Licença e créditos](#licença-e-créditos)

---

## O que é e por que usar

O multicortexEXO é uma **distribuição Linux especializada** montada para uma finalidade específica: ter um ambiente completo de IA local pronto para uso em questão de minutos, sem instalação, sem configuração manual, sem dependência de internet após o primeiro download dos modelos.

Você inicializa o computador pela ISO — seja em pendrive, VM ou rede — e o sistema já sobe com Ollama rodando, GNOME disponível, drivers NVIDIA carregados e os comandos de controle funcionando no terminal.

**Casos de uso práticos:**

- Bancada técnica de suporte: boot rápido em qualquer máquina, IA local disponível para auxiliar diagnósticos sem enviar dados do cliente para nenhum servidor externo
- Laboratório de modelos: testar diferentes LLMs sem poluir o sistema principal
- Demonstração controlada: mostrar IA local para cliente sem precisar de internet
- Ambiente offline: campo, indústria, local sem conectividade — os modelos ficam no SSD junto com a ISO
- Desenvolvimento: ambiente reproduzível com Python 3.12, Node.js 20, compiladores e bibliotecas de IA já instalados

---

## Diferenças em relação a um Linux normal

Uma ISO genérica do openSUSE Leap 15.6 é uma distribuição de propósito geral. Você baixa, instala, e depois passa horas configurando. O multicortexEXO parte da mesma base, mas é uma **distribuição de propósito específico** — montada para IA local já funcionar no boot.

| Aspecto | openSUSE Leap 15.6 padrão | multicortexEXO |
|---------|--------------------------|----------------|
| **Modo de uso** | Instalação em disco | Live ISO + overlay (persistência opcional) |
| **Ollama** | Não incluso | Instalado, configurado, habilitado no boot |
| **API de IA** | Não existe | `http://127.0.0.1:11434` disponível no boot |
| **Drivers NVIDIA** | Configuração manual | G06 incluídos no build |
| **Python** | 3.6 (padrão do Leap 15.6) | 3.12 + pip + setuptools |
| **Node.js** | Não incluso | 20 + npm incluídos |
| **Libs de build IA** | Não inclusas | OpenCV, OpenCL, TBB, protobuf, nlohmann_json, libva |
| **Comandos de controle** | Nenhum | `multicortex-status`, `multicortex-menu`, perfis de modelos |
| **Login automático** | Requer senha | Autologin do usuário `tux` |
| **Repositório JAX** | Não configurado | Pré-configurado dentro da ISO |
| **Ambiente pronto** | Após instalação e configuração | No boot |

### O overlay persistente

Um Live CD genérico descarta tudo ao reiniciar. O multicortexEXO usa **overlay persistente em ext4** — se gravado em pendrive com espaço livre, os modelos baixados, arquivos criados e pacotes instalados sobrevivem ao reinício. Isso transforma o pendrive numa estação de trabalho portátil completa: pluga em qualquer PC x86_64 e você tem seu ambiente de IA exatamente como deixou.

---

## Programas incluídos e para que servem

### Infraestrutura de IA

**Ollama** — motor central. Gerencia download, carregamento em memória e execução de modelos LLM. Expõe API REST compatível com OpenAI em `127.0.0.1:11434`. Iniciado como serviço systemd no boot.

**Firefox** — browser. Atalho na dock aponta para `localhost:7001` (interface web de chat local).

### Ambiente de desenvolvimento

**Python 3.12** (`python312`, `python312-pip`, `python312-setuptools`, `python312-base`) — o Leap 15.6 vem com Python 3.6 por padrão. O 3.12 foi adicionado explicitamente porque a maioria das bibliotecas modernas de IA (LangChain, transformers, etc.) requer Python ≥ 3.9.

**Python 3.x base** (`python3-base`, `python3-devel`, `python3-pip`) — versão de compatibilidade para ferramentas do sistema.

**Node.js 20 + npm** (`nodejs20`, `npm20`, `nodejs-common`) — runtime necessário para Open WebUI e outras interfaces web de chat.

**gcc / g++** (`gcc`, `gcc-c++`) — compiladores C/C++ para extensões nativas de Python, llama.cpp e código customizado.

**cmake / make / ninja / scons** (`cmake`, `make`, `ninja`, `scons`) — sistemas de build. cmake é usado pelo OpenCV e llama.cpp. ninja é o backend rápido do cmake.

**git / git-lfs** (`git`, `git-lfs`) — controle de versão. git-lfs necessário para repositórios do Hugging Face que armazenam pesos de modelos em arquivos grandes.

**pkg-config** — localiza bibliotecas de desenvolvimento durante compilação.

### Bibliotecas de computação e visão

**OpenCV** (`opencv-devel`) — visão computacional. Necessária para processamento de imagem, vídeo e modelos multimodais.

**OpenCL** (`opencl-headers`, `opencl-cpp-headers`, `ocl-icd-devel`) — computação paralela em GPU via OpenCL quando CUDA não está disponível.

**Intel VA-API** (`libva-devel`, `vaapi-intel-driver`) — aceleração de vídeo por hardware Intel.

**TBB** (`tbb-devel`) — Intel Threading Building Blocks. Paralelismo em CPU usado pelo OpenCV e frameworks de IA.

**libVDPAU** (`libvdpau_nouveau`) — aceleração de vídeo via VDPAU para GPUs NVIDIA/Nouveau.

**protobuf** (`protobuf-devel`) — serialização de dados usada pelo TensorFlow, ONNX e outros frameworks.

**nlohmann/json** (`nlohmann_json-devel`) — biblioteca header-only de JSON para C++. Usada por llama.cpp.

**snappy** (`snappy-devel`) — compressão rápida usada pelo TensorFlow e RocksDB.

**zlib** (`zlib-devel`) — compressão base, necessária para dezenas de bibliotecas.

**gflags** (`gflags-devel-static`) — flags de linha de comando para C++, usada por Caffe e backends do TensorFlow.

**pugixml** (`pugixml-devel`) — parser XML leve para C++, usado pelo OpenVINO.

**ade-devel** — framework de grafos de computação usado pelo OpenCV DNN module.

### Suporte a NVIDIA (GPU)

**`nvidia-drivers-insync-latest`** — meta-pacote que instala o driver NVIDIA mais recente sincronizado com o kernel.

**`nvidia-common-G06`** — arquivos comuns compartilhados entre os componentes do driver G06.

**`nvidia-compute-G06`** — bibliotecas CUDA para computação em GPU. Necessário para o Ollama usar a GPU para inferência.

**`nvidia-compute-utils-G06`** — `nvidia-persistenced` e ferramentas auxiliares de computação.

**`nvidia-utils-G06`** — `nvidia-smi` e utilitários de monitoramento. O `multicortex-status` chama `nvidia-smi` para exibir temperatura e uso de VRAM.

**`nvidia-driver-G06-kmp-default`** — módulo do kernel NVIDIA (`.ko`) compilado para o `kernel-default` do openSUSE.

**`ucode-intel`** — microcódigo para processadores Intel. Corrige bugs de hardware via firmware.

**`libdrm_intel1` / `libdrm_nouveau2`** — bibliotecas DRM para Intel e Nouveau. Renderização acelerada mesmo sem driver NVIDIA proprietário.

**`xf86-video-intel`** — driver Xorg para Intel HD/UHD Graphics.

### Ferramentas de qualidade de código

**ShellCheck** — analisador estático de scripts Shell. Detecta erros comuns e quoting incorreto.

**ccache** — cache de compilação. Reduz drasticamente recompilações de projetos C/C++ como OpenCV ou llama.cpp.

**patchelf** — modifica binários ELF para ajustar caminhos de biblioteca (`RPATH`). Necessário para redistribuir binários compilados.

**fdupes** — encontra e remove arquivos duplicados.

### Ambiente gráfico

**GNOME** (via `patterns-gnome-*`) — desktop completo. `gnome_basis` é o núcleo; `gnome_internet` adiciona Firefox; `gnome_utilities` adiciona calculadora e monitor; `gnome_imaging` adiciona Cheese.

**GDM** — gerenciador de display com autologin do `tux`.

**GNOME Terminal** — onde os comandos `multicortex-*` são executados.

**Cheese** — câmera. Herdado do projeto original com foco em visão computacional.

**NetworkManager** (`NetworkManager-gnome`) — gerenciamento de rede com GUI.

**YaST2** (`yast2-control-center-gnome`, `yast2-x11`) — painel de controle do openSUSE para configuração gráfica do sistema.

### Sistema e bootloader

**kernel-default** — kernel Linux padrão do openSUSE com módulos para a maioria dos hardwares.

**kernel-firmware** — firmwares de hardware: Wi-Fi, áudio, controladores de armazenamento.

**Firmwares específicos** (`atmel-firmware`, `adaptec-firmware`, `bluez-firmware`, `alsa-firmware`, `ipw-firmware`, `mpt-firmware`) — chipsets específicos de Wi-Fi, RAID, Bluetooth e áudio.

**GRUB2 + shim + grub2-x86_64-efi** — bootloader UEFI. O `shim` é necessário para UEFI moderno.

**syslinux** — bootloader BIOS legacy.

**Plymouth + tema studio** — splash screen animado durante o boot.

**dracut-kiwi-live** — monta o SquashFS como overlay no boot Live. Essencial.

**openssh** — SSH para acesso remoto.

**iproute2** — ferramentas de rede (`ip`, `ss`). Usadas pelo `multicortex-status`.

**dhcp-client** — DHCP automático.

**lvm2** / **e2fsprogs** — LVM e ferramentas ext4. Necessários para a partição de persistência.

**zypper** — gerenciador de pacotes. Permite instalar pacotes adicionais dentro da ISO com persistência ativa.

---

## Versão e release

```
Versão:  0.99 Build 20260609 11:17
ISO:     MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
SHA256:  93ec2e21ffb2d041eed5b06433f1f08104d6e9bcae27ebaab2399874bcdd80a2
```

Download: [GitHub Releases](https://github.com/hawkinf/multicortexEXO_fork/releases)

---

## Estrutura do repositório

```
multicortexEXO_fork/
├── VERSION                              Versão atual do projeto
├── .gitignore
│
├── custom_boot/                         Biblioteca KIWI legada (herdada do upstream, não modificada)
│   ├── functions.sh                     Centenas de funções Shell para boot: LVM, iSCSI, PXE, rede, particionamento
│   ├── locale/                          Internacionalização do KIWI (40+ idiomas)
│   ├── helper/kiwi-boot-packages        Lista de pacotes de boot
│   ├── package/                         Metadados RPM do kiwi-boot-descriptions
│   └── arch/                            Descritores de boot por arquitetura
│       ├── arm/oemboot/                 ARM: SLES12, SLES15, Leap 15.0, 42.x, Tumbleweed
│       ├── ppc/netboot/ e oemboot/      PowerPC: SLES12, SLES15
│       ├── s390/netboot/ e oemboot/     IBM Z: SLES12, SLES15, Tumbleweed
│       └── x86_64/netboot/ e oemboot/  x86_64: SLES12, SLES15, RHEL7, Leap, Tumbleweed, Ubuntu Xenial
│
├── docs/
│   ├── API.md                           Endpoints da API Ollama
│   ├── BUILD.md                         Fluxo de build da ISO
│   ├── FULL_OFFLINE.md                  Edição offline com SSD/NVMe
│   ├── MODELOS.md                       Perfis de modelos por hardware
│   ├── SEGURANCA.md                     Credenciais e boas práticas
│   └── build-environment-report.md      Relatório do último build
│
├── layout/
│   ├── logo.png                         Logotipo do projeto
│   ├── wallpaper.png                    Wallpaper da distro
│   └── wallpaper.xcf                    Arquivo-fonte GIMP
│
├── releases/
│   └── MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256
│
├── scripts/
│   ├── gerar_iso_multicortex_completo_py36.py   Script Python de build automático
│   └── system/
│       ├── multicortex-menu.sh          Menu interativo de controle
│       └── multicortex-status.sh        Diagnóstico completo do sistema
│
└── suse/x86_64/suse-leap-15.6-JeOS/    Descrição KIWI — núcleo da ISO
    ├── config.xml                       Pacotes, repositórios, usuários, tipo de imagem
    ├── config-1.0.0.xml                 Versão anterior do config.xml (referência)
    ├── configBUB.xml                    Variante experimental
    ├── config.sh                        Script de pós-build executado pelo KIWI no chroot
    ├── Dicefile                         Manifesto KIWI para Docker (config.buildhost = :DOCKER)
    ├── firstboot_scripts/config.sh      Script de firstboot legado (gsettings + certificados SSL)
    ├── gdm.tar / plymouth.tar           Temas de boot empacotados
    │
    ├── root/                            Overlay: arquivos copiados diretamente na ISO
    │   ├── etc/motd                     Mensagem no login
    │   ├── etc/multicortex-version      Versão lida pelo multicortex-status
    │   ├── etc/profile.d/multicortex.sh Aliases e OLLAMA_HOST para todos os shells
    │   ├── etc/ld.so.conf.d/cuda.conf   Linker para bibliotecas CUDA
    │   ├── etc/sysconfig/network/ifcfg-lan0   DHCP automático
    │   ├── etc/systemd/system/
    │   │   ├── multicortex-firstboot.service   Cria /var/lib/ollama no boot
    │   │   ├── suse-studio-custom.service      Legado SUSE Studio
    │   │   └── suse-studio-firstboot.service   Legado SUSE Studio
    │   ├── etc/zypp/repos.d/            OSS, Updates, JAX pré-configurados
    │   ├── home/tux/.config/autostart/
    │   │   ├── config.desktop           Autostart: chama config_osviacam.sh (executa 1x)
    │   │   └── init.desktop             Autostart: chama initMulticortex.sh no login
    │   ├── home/tux/bin/exo             Ativa venv e executa framework exo
    │   ├── opt/multicortex/scripts/system/   Cópias de multicortex-status e multicortex-menu
    │   ├── studio/                      Scripts legados SUSE Studio (comentados no config.sh)
    │   ├── usr/bin/config_osviacam.sh   Configura GNOME e se auto-remove do autostart
    │   ├── usr/bin/initMulticortex.sh   Exibe logo ASCII e tenta ollama run llama3.2
    │   ├── usr/lib/systemd/system/grub_config.service   Só para builds OEM
    │   ├── usr/local/cuda/readme.txt    Placeholder — CUDA libs instaladas manualmente aqui
    │   └── usr/share/applications/Chat.desktop   Atalho GNOME → Firefox localhost:7001
    │
    └── usr/share/                       Temas visuais do descritor KIWI
        ├── gdm/themes/studio/           Tema GDM (fundo de login, logo)
        ├── gfxboot/themes/studio/       Tela de boot GFXBOOT
        ├── grub2/themes/studio/         Tema GRUB2 (fontes DejaVu, backgrounds, sliders)
        ├── plymouth/themes/studio/      Splash screen de boot
        └── wallpapers/                  Wallpaper padrão
```

---

## Descrição técnica da ISO

| Propriedade | Valor |
|-------------|-------|
| Nome | `MultiCortex_EXO_1.0.5` |
| Base | openSUSE Leap 15.6 x86_64 |
| Tipo | ISO Live híbrida (UEFI + BIOS Legacy) |
| Sistema de arquivos | SquashFS + overlay ext4 |
| Persistência | Sim (hybridpersistent=true, ext4) |
| Verificação de mídia | Sim (mediacheck=true) |
| Kernel cmdline | `splash` |
| Locale | `pt_BR` |
| Teclado | `br` |
| Timezone | `UTC` |
| Autologin | `tux` via GDM |

---

## Scripts — funcionamento detalhado

### `multicortex-status.sh`

**Localização:** `scripts/system/multicortex-status.sh` (cópia idêntica em `suse/.../root/opt/multicortex/scripts/system/`)

**Chamado por:** comando `multicortex-status` ou alias `mc-status`

O script define `set -Eeuo pipefail` — qualquer erro não tratado aborta. `OLLAMA_BASE_URL` usa `$OLLAMA_HOST` se definido, senão `http://127.0.0.1:11434`. A função `section()` imprime títulos em azul ciano (`\033[1;36m`). A função `cmd_or_na()` executa um comando e imprime `N/A` se falhar, sem abortar.

**Seção Versão:** lê `/etc/multicortex-version` ou `./VERSION`.

**Seção Sistema:** exibe `hostname`, `uname -r`, `uname -m`. Filtra `PRETTY_NAME` e `VERSION_ID` do `/etc/os-release`.

**Seção Rede:** `ip -4 addr show scope global` lista IPs globais (não loopback), formatados com `awk`. Imprime URLs prováveis de todos os serviços.

**Seção Serviços:** itera sobre `ollama.service`, `multicortex-chat-ui.service`, `open-webui.service` e chama `systemctl is-active` para cada um.

**Seção Ollama API:** `curl -fsS http://127.0.0.1:11434/api/tags` salvo em `/tmp/multicortex-tags.json`. Se responder, lista modelos com `jq -r '.models[]?.name'` ou imprime JSON bruto se `jq` não estiver disponível.

**Seção Modelos:** `ollama list` diretamente (formato tabular).

**Seção Hardware:** `lscpu | awk` para o model name da CPU; `free -h` para RAM; `df -h /` para disco; `nvidia-smi` se disponível — exibe temperatura, VRAM e processos.

**Seção Logs:** `journalctl -u ollama.service -n 20 --no-pager`.

Todos os comandos opcionais usam `|| true` para não abortar em ambientes sem todas as ferramentas.

---

### `multicortex-menu.sh`

**Localização:** `scripts/system/multicortex-menu.sh` (cópia em `root/opt/multicortex/scripts/system/`)

**Chamado por:** comando `multicortex-menu` ou alias `mc-menu`

Loop `while true` com `clear` antes de cada iteração. Menu exibido via heredoc `cat <<'MENU'`. O `read` aguarda opção.

**Função `run()`:** imprime `>>> comando`, executa, depois `read -r -p "Enter para voltar..."` — pausa antes de limpar a tela para o resultado não desaparecer imediatamente.

**Função `service_cmd()`:** tenta `sudo systemctl action svc`; se falhar, tenta sem sudo. Usa `|| true` para não abortar.

**Função `show_urls()`:** imprime URLs hardcoded (11434, 3000, 8080) e IPs reais via `ip -4 addr show scope global`.

**Função `test_api()`:** `curl -fsS http://127.0.0.1:11434/api/tags` — JSON bruto para diagnóstico rápido.

| Opção | Execução real |
|-------|--------------|
| 1 | `run multicortex-status` |
| 2 / 3 / 4 | start / stop / restart `ollama.service` |
| 5 / 6 / 7 | start / stop / restart `multicortex-chat-ui` + `open-webui` |
| 8 | `run multicortex-models-list` |
| 9 / 10 / 11 / 12 | instalar modelos light / medium / code / large |
| 13 | `run test_api` |
| 14 | `run show_urls` |
| 15 | `exit 0` |

---

### `initMulticortex.sh`

**Localização:** `suse/.../root/usr/bin/initMulticortex.sh`

**Chamado por:** `init.desktop` no autostart do GNOME do usuário `tux`

```bash
cat /etc/multicortex.asc   # exibe logo ASCII (arquivo não está no overlay — pendência)
echo "Initializing..."
ollama run llama3.2 "Ola!"
```

Dispara no login gráfico. Se `llama3.2` não estiver instalado, o Ollama tenta baixar da internet ou falha. O terminal fica aberto para uso interativo.

---

### `config_osviacam.sh`

**Localização:** `suse/.../root/usr/bin/config_osviacam.sh`

**Chamado por:** `config.desktop` no autostart (executa apenas uma vez)

```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface monospace-font-name 'Monospace 12'
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"
rm /home/tux/.config/autostart/config.desktop
```

Configura a aparência do GNOME (dock, fonte, tema Dark, wallpaper) e depois **se auto-remove do autostart**. Nas inicializações seguintes o arquivo não existe e o script não roda.

---

### `exo` (script do usuário tux)

**Localização:** `suse/.../root/home/tux/bin/exo`

```bash
cd ~/exo
source .venv/bin/activate
exo
```

Ativa um virtualenv Python e executa o framework [exo](https://github.com/exo-explore/exo), que distribui a execução de um LLM entre múltiplos dispositivos na rede local. O diretório `~/exo` e o venv não estão na ISO — precisam ser criados manualmente:

```bash
mkdir ~/exo && cd ~/exo
python3.12 -m venv .venv
source .venv/bin/activate
pip install exo-inference
```

---

### `config.sh` — script de build KIWI

**Localização:** `suse/x86_64/suse-leap-15.6-JeOS/config.sh`

**Executado por:** KIWI NG durante o build, dentro do chroot da imagem. Roda como root com acesso ao sistema de arquivos ainda não comprimido.

**Em sequência:**

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
Faz o zypper instalar apenas dependências `Requires`, ignorando `Recommends`. Evita centenas de pacotes desnecessários.

**4. Sysconfig:**
```bash
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER_AUTOLOGIN tux
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER gdm
baseUpdateSysConfig /etc/sysconfig/windowmanager DEFAULT_WM gnome
```
Define autologin do `tux`, GDM e GNOME dentro da imagem.

**5. Preparação do overlay:**
Cria `/studio/`, copia `.profile` e `config.xml` para lá, remove `/studio/overlay-tmp`. Comenta os scripts legados de tema GDM/GNOME — usavam `gconftool-2` que não existe no GNOME 3.

**6. Ativação de serviços:**
```bash
suseInsertService sshd
suseInsertService ollama
suseInsertService multicortex-chat-ui
```
Equivalente a `systemctl enable` dentro do chroot. Cria links em `/etc/systemd/system/multi-user.target.wants/`.

**7. Limpeza:**
```bash
rm -rf /usr/share/doc/packages/*
rm -rf /opt/kde*
/sbin/ldconfig          # reconstrói cache do linker dinâmico
baseSetRunlevel 5       # modo gráfico (graphical.target)
```

**8. `exit 0`**

O script termina aqui. O bloco `MULTICORTEX EXO GENERATED CONFIG` logo abaixo **nunca executa** — está após o `exit 0`. É o principal bug conhecido do repositório.

---

### `gerar_iso_multicortex_completo_py36.py`

**Localização:** `scripts/gerar_iso_multicortex_completo_py36.py`

**Executado por:** root no host openSUSE Leap 15.6

**Compatibilidade:** Python 3.6+ (stdlib apenas: `argparse`, `os`, `re`, `shutil`, `subprocess`, `sys`, `pathlib`)

**Argumentos:**

```
--workdir PATH    pasta de trabalho (padrão: /home/hawk/builds ou ~/builds)
--clean           apaga a pasta de trabalho antes de começar
--no-install      pula instalação de pacotes (assume kiwi-ng disponível)
```

**Em sequência:**

1. Verifica `os.geteuid() == 0`
2. Lê `/etc/os-release`, avisa se não for Leap 15.6
3. `ensure_host_packages()`: `zypper refresh` + instala `git`, `python3-kiwi`, `curl`, `ca-certificates`, `openssl` etc. Se `kiwi-ng` não for encontrado, adiciona o repositório KIWI Builder e reinstala
4. `clone_or_update()`: `git clone cabelo/multicortex-exo` ou `git pull --ff-only`
5. `copy_kiwi_descriptor()`: `shutil.copytree` de `suse/x86_64/suse-leap-15.6-JeOS` para `workdir/kiwi-desc/`
6. `patch_config_xml()`: HTTPS→HTTP, adiciona repos non-oss e NVIDIA, adiciona `ca-certificates-mozilla`/`openssl` no bootstrap, garante os 5 pacotes NVIDIA G06, comenta `baseMount`/`baseCleanMount` no `config.sh`
7. `build_iso()`: `kiwi-ng --debug system build --description kiwi-desc --target-dir out`. Log em tempo real via `subprocess.Popen` gravado em `build-multicortex.log`

---

### Scripts legados (`studio/`)

**`configure_gdm_theme.sh`** — configura tema GDM com `gconftool-2`. **Não executa** — comentado no `config.sh` porque o `gconftool-2` não existe no GNOME 3.

**`configure_gnome_background.sh`** — configura wallpaper e dock via `gsettings`. **Não executa** — desabilitado junto com o anterior.

**`firstboot_scripts/config.sh`** — configura GNOME via `gsettings` e faz `c_rehash`. **Não executa** no build atual.

---

### `suse_studio_firstboot`

**Localização:** `root/etc/init.d/suse_studio_firstboot`

**Chamado por:** `suse-studio-firstboot.service` na primeira inicialização

Detecta todas as interfaces Ethernet e configura DHCP. Em modo Testdrive (SUSE Studio), desativa efeitos do KDE e vmtoolsd. Configura GNOME: dock, fonte, tema Dark, wallpaper. Ao final **se auto-desativa e se auto-deleta** — executa apenas uma vez.

---

## Serviços systemd — o que faz cada um

### `multicortex-firstboot.service`

```ini
[Service]
Type=oneshot
ExecStart=/usr/bin/bash -lc 'mkdir -p /var/lib/ollama /var/log/multicortex; chmod 755 /var/lib/ollama /var/log/multicortex || true'
RemainAfterExit=yes
```

`Type=oneshot` executa uma vez e termina. `RemainAfterExit=yes` mantém o serviço como "ativo" para que outros possam depender dele. Cria `/var/lib/ollama` (onde o Ollama armazena modelos) e `/var/log/multicortex`. Existe porque o bloco do `config.sh` que criaria esses diretórios nunca executa (bug do `exit 0`).

### `ollama.service`

Instalado pelo pacote `ollama` (repositório JAX). Inicia em `127.0.0.1:11434`. Gerencia carregamento de modelos em RAM ou VRAM. Reinicia automaticamente em caso de falha.

### `sshd.service`

SSH na porta 22. Permite acesso remoto: `ssh tux@<ip>` ou `ssh root@<ip>`.

### `multicortex-chat-ui.service`

Habilitado no `config.sh`, mas **sem arquivo `.service` no overlay**. Deveria iniciar uma interface web de chat na porta 3000. Pendência.

### `open-webui.service`

Referenciado no menu e status, sem arquivo `.service` no overlay. Seria o [Open WebUI](https://github.com/open-webui/open-webui) na porta 8080.

### `grub_config.service`

```ini
ConditionPathExists=/.kiwi_grub_config.trigger
ExecStart=/bin/bash -c 'grub2-mkconfig -o /boot/grub2/grub.cfg'
ExecStartPost=/bin/bash -c 'rm -f /.kiwi_grub_config.trigger'
```

Reconstrói o `grub.cfg` após instalação em disco (builds OEM). Só dispara quando o arquivo trigger existe — criado pelo KIWI em builds OEM.

### `suse-studio-firstboot.service` e `suse-studio-custom.service`

Legados do SUSE Studio. O `firstboot` executa `/etc/init.d/suse_studio_firstboot` e se auto-deleta. O `custom` executaria `/studio/suse-studio-custom` se existir.

---

## Overlay root — arquivos copiados na ISO

Tudo em `suse/x86_64/suse-leap-15.6-JeOS/root/` é copiado pelo KIWI para dentro da ISO. O caminho é preservado — `root/etc/motd` vira `/etc/motd`.

**`/etc/motd`** — exibido no login. Lista comandos disponíveis e credenciais padrão.

**`/etc/multicortex-version`** — string de versão lida pelo `multicortex-status.sh`.

**`/etc/profile.d/multicortex.sh`** — carregado em todo shell de login:
```bash
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

**`/etc/ld.so.conf.d/cuda.conf`** — linker para `/usr/local/cuda/lib64`. As libs CUDA precisam ser instaladas manualmente — o diretório existe mas tem apenas um `readme.txt`.

**`/etc/sysconfig/network/ifcfg-lan0`** — `BOOTPROTO=dhcp`, `STARTMODE=onboot`. DHCP automático no boot.

**`/etc/zypp/repos.d/jax_15.6.repo`** — repositório `home:cabelo:jax` pré-configurado. Permite `zypper install` de pacotes de IA após o boot sem configuração adicional.

---

## Credenciais padrão

```
Usuário   Senha    Grupo
root      linux    root
tux       linux    users
```

> Trocar antes de usar em rede ou publicar ISO:

```bash
passwd root
passwd tux
```

Para gerar hash para o `config.xml` antes de um novo build:

```bash
openssl passwd -1 'NovaSenhaAqui'
```

---

## Walkthrough completo: do comando à ISO rodando

Fluxo detalhado de tudo que acontece ao executar o build, usando o perfil **light** como exemplo — o mais simples de observar de ponta a ponta.

### Visão geral do fluxo

```
VOCÊ                 SCRIPT PYTHON              KIWI NG                ISO GERADA
  │                       │                        │                       │
  │ python3               │                        │                       │
  │ gerar_iso.py ────────>│                        │                       │
  │                       │ verifica root          │                       │
  │                       │ lê /etc/os-release     │                       │
  │                       │ zypper install kiwi-ng │                       │
  │                       │ git clone/pull         │                       │
  │                       │ copia kiwi-desc/       │                       │
  │                       │ patcha config.xml      │                       │
  │                       │ kiwi-ng build ────────>│                       │
  │                       │                        │ valida config.xml     │
  │                       │                        │ fase bootstrap        │
  │                       │                        │ fase image (~800 pkgs)│
  │                       │                        │ copia overlay root/   │
  │                       │                        │ executa config.sh     │
  │                       │                        │ gera initramfs        │
  │                       │                        │ comprime SquashFS     │
  │                       │                        │ monta bootloaders     │
  │                       │                        │ xorriso → .iso ──────>│
  │                       │<───────────────────────│                       │
  │<──────────────────────│                        │                       │
  │                       │                        │              dd → pendrive
  │                       │                        │              UEFI → GRUB2
  │                       │                        │              kernel + overlay
  │                       │                        │              systemd
  │                       │                        │              GNOME → autostart
  │                       │                        │              ollama run llama3.2
```

---

### Parte 1 — Execução do script Python

#### Passo 1: você digita o comando

```bash
su -
python3 /caminho/para/scripts/gerar_iso_multicortex_completo_py36.py
```

O `su -` é obrigatório — não `sudo`. O KIWI precisa de root real para usar `loop devices`, montar sistemas de arquivos e fazer `chroot`. Com `sudo` algumas operações de mount falham silenciosamente.

```python
if not is_root():      # checa os.geteuid() == 0
    print("ERRO: rode como root.")
    sys.exit(1)
```

#### Passo 2: detecção do SO

Lê e parseia `/etc/os-release`. Emite aviso se `VERSION_ID != "15.6"` mas não aborta.

```
Sistema detectado:
  NAME=openSUSE Leap
  VERSION_ID=15.6
```

#### Passo 3: definição do diretório de trabalho

```python
def default_workdir():
    if Path("/home/hawk").exists():
        return Path("/home/hawk/builds")
    return Path.home() / "builds"
```

Se `--clean` foi passado: `shutil.rmtree(workdir)` apaga tudo antes de começar.

#### Passo 4: instalação de dependências no host

```
zypper --gpg-auto-import-keys refresh
```

O `--gpg-auto-import-keys` aceita chaves GPG novas sem interação. Depois instala:

```
git  python3  python3-pip  python3-kiwi  curl  wget  nano
xz  tar  gzip  cpio  rsync  which
ca-certificates  ca-certificates-mozilla  openssl
```

Se `kiwi-ng` não for encontrado no PATH após a instalação, adiciona o repositório KIWI Builder automaticamente:

```
zypper ar -f https://download.opensuse.org/repositories/
              Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/
              kiwi-builder
```

E tenta instalar novamente. Encerra com `kiwi-ng --version` para confirmar.

#### Passo 5: clone ou atualização do upstream

```python
repo_dir = workdir / "multicortex-exo"
```

Se `.git` existe: `git pull --ff-only` — fast-forward only, sem merge commits. Garante build sempre baseado no upstream limpo.

Se não existe: `git clone https://github.com/cabelo/multicortex-exo.git`.

Valida que `suse/x86_64/suse-leap-15.6-JeOS` existe dentro do clone.

#### Passo 6: cópia do descritor KIWI

```python
shutil.copytree(str(src), str(dst), symlinks=True)
```

Copia `multicortex-exo/suse/x86_64/suse-leap-15.6-JeOS` para `workdir/kiwi-desc/`. Apaga destino anterior se existir. `symlinks=True` preserva links simbólicos.

#### Passo 7: patch do `config.xml`

Lê o XML inteiro como string. Todas as modificações são feitas em memória e gravadas de volta.

**HTTPS → HTTP:** o prefixo `obs://` é URL interna do OBS (Build Service da SUSE) — só funciona dentro da infraestrutura deles. Fora, precisa virar URL HTTP real. HTTPS é convertido para HTTP porque o chroot KIWI é isolado sem CAs configurados.

```python
replacements = {
    'obs://Virtualization:Appliances:Builder/openSUSE_Leap_15.6':
        'http://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/',
    'https://download.opensuse.org/...': 'http://download.opensuse.org/...',
    # ...
}
```

**Adiciona repos non-oss e NVIDIA** antes do bloco `<packages type="image">` se não estiverem presentes — usa `str.replace` com verificação de idempotência.

**Bootstrap críticos:** garante `ca-certificates-mozilla` e `openssl` no bloco `<packages type="bootstrap">` via regex com `re.DOTALL` (para casar newlines). Sem eles, qualquer download HTTPS feito durante a fase de instalação falha.

**Garante os 5 pacotes NVIDIA G06:**
```
nvidia-common-G06  nvidia-compute-G06  nvidia-compute-utils-G06
nvidia-utils-G06   nvidia-driver-G06-kmp-default
```
Verifica presença em aspas simples E duplas antes de inserir.

**Compatibilidade KIWI 10:** comenta `baseMount` e `baseCleanMount` no `config.sh` se ainda estiverem lá.

Grava o `config.xml` modificado. O original no upstream não é tocado.

#### Passo 8: execução do build KIWI

```python
cmd = ["kiwi-ng", "--debug", "system", "build",
       "--description", str(kiwi_desc),
       "--target-dir",  str(out_dir)]

proc = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT,
                        universal_newlines=True, bufsize=1)
with log_file.open("w") as log:
    for line in proc.stdout:
        print(line, end="")   # tempo real na tela
        log.write(line)       # e no arquivo de log
code = proc.wait()
```

`stderr=STDOUT` une os dois streams para manter ordem cronológica. O log completo fica em `builds/build-multicortex.log`.

---

### Parte 2 — O que o KIWI NG faz internamente

A partir daqui o controle passa inteiramente para o KIWI.

#### Passo 9: parsing e validação do `config.xml`

KIWI valida o XML contra o schema 6.4: tipos de imagem, pacotes duplicados, repositórios acessíveis. Se o XML for inválido, aborta com erro de schema.

#### Passo 10: fase bootstrap

KIWI cria o **root tree** — diretório temporário onde a imagem será montada. Instala os pacotes do bloco `<packages type="bootstrap">` **usando `rpm` direto no host**, sem zypper dentro do chroot, porque o zypper ainda não existe na imagem:

```xml
<packages type="bootstrap">
    <package name="filesystem"/>      <!-- cria /usr /etc /var etc -->
    <package name="glibc-locale"/>    <!-- libs de localização -->
    <package name="udev"/>
    <package name="ca-certificates"/>
    <package name="ca-certificates-mozilla"/>  <!-- CAs para HTTPS -->
    <package name="openssl"/>
    <package name="openSUSE-release"/>  <!-- define a distro para o zypper -->
    <package name="cracklib-dict-full"/>
    <package name="module-init-tools"/>
</packages>
```

`filesystem` cria a estrutura de diretórios FHS. `ca-certificates-mozilla` + `openssl` são os adicionados pelo patch Python — sem eles, o zypper dentro do chroot falha em downloads HTTPS.

#### Passo 11: fase image

Com o bootstrap, o KIWI entra no chroot e executa o zypper de dentro:

```bash
chroot /tmp/kiwi-root-tree-XXXX zypper install [lista de pacotes do config.xml]
```

Você lista ~120 pacotes no `config.xml`, mas o solver do zypper instala ~800 por causa das dependências transitivas. O `solver.onlyRequires = true` já estava no `config.xml` original, mas o patch do Python garante que está presente mesmo em builds do upstream. Sem isso, o zypper traria centenas de pacotes `Recommended`.

Para o perfil light, os pacotes-chave nessa fase são: `python312`, `nodejs20`, `opencv-devel`, `tbb-devel`, `ollama` (do repositório JAX), toda a pilha GNOME, drivers NVIDIA G06.

No terminal você vê:

```
[ 45%] Installing: kernel-default-6.4.0-150600.23.25.1.x86_64
[ 46%] Installing: python312-3.12.4-150600.3.3.1.x86_64
[ 47%] Installing: ollama-0.3.6-lp156.1.x86_64
```

#### Passo 12: cópia do overlay `root/`

O KIWI copia recursivamente `kiwi-desc/root/` para dentro do root tree, **sobrescrevendo** qualquer arquivo que um pacote tenha instalado. É o mecanismo de customização: você substitui qualquer arquivo de qualquer pacote colocando a versão modificada no overlay.

Também extrai os arquivos `.tar` declarados no `config.xml`:

```xml
<archive name='plymouth.tar' bootinclude='true'/>
<archive name='gdm.tar' bootinclude='true'/>
```

Os temas visuais entram na imagem nesse momento.

#### Passo 13: execução do `config.sh` dentro do chroot

```bash
chroot /tmp/kiwi-root-tree-XXXX /bin/bash /image/config.sh
```

O arquivo `/image/config.sh` dentro do chroot é o `kiwi-desc/config.sh`. O KIWI injeta funções utilitárias em `/.kconfig` antes de executar.

Em sequência dentro do chroot:
- `suseSetupProduct` cria o link `/etc/products.d/baseproduct`
- `suseImportBuildKey` importa GPG no banco RPM da imagem
- `sed` ativa `solver.onlyRequires` no `zypp.conf` da imagem
- `baseUpdateSysConfig` define autologin do `tux`, GDM, GNOME
- `suseInsertService sshd/ollama/multicortex-chat-ui` cria links em `/etc/systemd/system/multi-user.target.wants/`
- `rm -rf /usr/share/doc/packages/*` remove documentação
- `/sbin/ldconfig` reconstrói o cache do linker dinâmico
- `baseSetRunlevel 5` define `graphical.target` como padrão
- `exit 0` — o script termina. O bloco MULTICORTEX abaixo **nunca executa**.

#### Passo 14: geração do initramfs

```bash
chroot /tmp/kiwi-root-tree-XXXX dracut --force --add "kiwi-live" [...]
```

O módulo `kiwi-live` (do pacote `dracut-kiwi-live`) ensina o initramfs a montar o SquashFS e criar o overlay no boot. O initramfs contém scripts de detecção de mídia, montagem, módulos do kernel (squashfs, loop, ext4, usb) e binários mínimos.

#### Passo 15: compressão em SquashFS

```bash
mksquashfs /tmp/kiwi-root-tree-XXXX /tmp/.../LiveOS/squashfs.img -comp xz -b 1M
```

`xz` oferece a melhor compressão — um root tree de ~8GB vira ~1.8GB. A descompressão é sob demanda: o kernel descomprime apenas os blocos acessados, não a imagem inteira.

#### Passo 16: montagem da estrutura da ISO

```
/tmp/kiwi-iso-XXXX/
├── boot/grub2/themes/studio/    ← tema GRUB2
├── EFI/BOOT/
│   ├── bootx64.efi              ← shim (1º estágio UEFI)
│   └── grub.efi                 ← GRUB2 (2º estágio UEFI)
├── LiveOS/squashfs.img          ← sistema completo comprimido
└── isolinux/                    ← SYSLINUX para BIOS legacy
```

#### Passo 17: instalação dos bootloaders

**UEFI:** `shim` + `grub.efi` copiados para `EFI/BOOT/`. O shim valida o GRUB2 para Secure Boot, ou carrega diretamente com Secure Boot desligado. GRUB2 recebe `grub.cfg` com as entradas de boot.

**BIOS legacy:** `isolinux.bin` + `isolinux.cfg` configurados para carregar o mesmo kernel.

#### Passo 18: geração do arquivo ISO híbrido

```bash
xorriso -as mkisofs \
  -eltorito-boot isolinux/isolinux.bin \   ← boot BIOS
  -eltorito-alt-boot \
  -e EFI/BOOT/bootx64.efi \               ← boot UEFI
  -isohybrid-mbr isohdpfx.bin \           ← MBR para pendrive
  -output MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  /tmp/kiwi-iso-XXXX/
```

`xorriso` gera uma imagem que é simultaneamente ISO 9660 (CD/DVD), disco com MBR (pendrive via BIOS) e GPT com partição ESP (pendrive via UEFI). O `isohdpfx.bin` são os 432 bytes gravados no início que funcionam como MBR.

`hybridpersistent="true"` do `config.xml` faz o KIWI reservar espaço no final da imagem para a partição de persistência ext4 quando gravada em pendrive.

#### Passo 19: resultado

```
=== ISO gerada com sucesso ===
 - /home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso (1.79 GiB)
```

---

### Parte 3 — Do pendrive ao modelo respondendo

#### Passo 20: gravação no pendrive

```bash
dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

`dd` copia byte a byte, incluindo o MBR híbrido nos primeiros 446 bytes. `conv=fsync` força escrita para o hardware antes de retornar — sem ele o terminal pode indicar término com dados ainda no cache do kernel.

#### Passo 21: UEFI detecta e inicializa

O firmware escaneia dispositivos em busca de `EFI/BOOT/bootx64.efi`. Encontra no pendrive, carrega o shim, que carrega o GRUB2. O menu "studio" aparece:

```
  Boot Live System
  Check Installation Media
```

Sem tecla pressionada, a primeira entrada é selecionada após alguns segundos.

#### Passo 22: kernel e Plymouth

GRUB2 carrega o `kernel-default` e o initramfs com o parâmetro `splash`. Plymouth exibe a animação com o tema "studio".

#### Passo 23: dracut-kiwi-live monta o overlay

O initramfs localiza a ISO/pendrive via `CDLABEL=MultiCortex_EXO_1.0.5`. O módulo `kiwi-live`:

1. Monta o SquashFS como loop read-only: `/dev/loop0` → `/run/rootfsbase`
2. Verifica se há espaço no pendrive para a partição ext4 de persistência
3. Se sim: cria ou monta a partição ext4. Se não: usa RAM (tmpfs)
4. Cria o overlay:
```bash
mount -t overlay overlay \
  -o lowerdir=/run/rootfsbase,upperdir=/run/overlay,workdir=/run/work \
  /sysroot
```
5. `pivot_root` para `/sysroot`

A partir daqui, leituras vão ao SquashFS (read-only), escritas vão ao ext4 (persistência) ou RAM.

#### Passo 24: systemd inicia os serviços

O systemd inicia em paralelo respeitando dependências:

**`multicortex-firstboot.service`** dispara:
```bash
mkdir -p /var/lib/ollama /var/log/multicortex
chmod 755 /var/lib/ollama /var/log/multicortex
```
Cria os diretórios que o Ollama precisa — necessário porque o bloco do `config.sh` nunca executa.

**`ollama.service`** inicia:
```
Ollama version 0.3.6
listening on 127.0.0.1:11434
```
Verifica `/var/lib/ollama/models/` — sem modelos instalados, apenas aguarda requisições.

**`sshd.service`** inicia na porta 22.

#### Passo 25: GDM e autologin do tux

GDM lê `DISPLAYMANAGER_AUTOLOGIN=tux` do sysconfig e faz login sem senha. GNOME Shell carrega com o wallpaper do projeto.

#### Passo 26: `config_osviacam.sh` — executa uma vez

O `config.desktop` no autostart chama `config_osviacam.sh`:

```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"
rm /home/tux/.config/autostart/config.desktop   # se auto-remove
```

Define dock, tema Dark e wallpaper. Se deleta — não roda nas próximas inicializações.

#### Passo 27: `initMulticortex.sh` — terminal de IA

O `init.desktop` abre um terminal e executa:

```bash
cat /etc/multicortex.asc    # logo ASCII (se existir)
echo "Initializing..."
ollama run llama3.2 "Ola!"
```

`ollama run llama3.2`:
1. Conecta em `127.0.0.1:11434`
2. Verifica `/var/lib/ollama/models/`
3. Se modelo não instalado: tenta download (requer internet) ou falha
4. Se instalado: carrega na RAM/VRAM e responde

#### Passo 28: instalando o perfil light

Com o sistema rodando:

```bash
multicortex-models-light
```

Que executa `ollama pull` para cada modelo:

| Modelo | Tamanho aproximado |
|--------|--------------------|
| `tinyllama:latest` | ~637 MB |
| `phi3:mini` | ~2.2 GB |
| `gemma3:1b` | ~815 MB |
| `qwen3:0.6b` | ~522 MB |
| `smollm2:1.7b` | ~1 GB |

Para cada modelo o Ollama: consulta o manifesto em `registry.ollama.ai`, baixa os blobs faltantes, verifica SHA256, cria os manifests em `/var/lib/ollama/models/manifests/`.

Com persistência ativa no pendrive, os modelos sobrevivem ao reinício.

#### Passo 29: modelo respondendo

```bash
ollama run tinyllama "Explique o que é um motherboard em 2 linhas"
```

O Ollama tokeniza o prompt, executa o forward pass pela rede neural e retorna os tokens decodificados. Com `tinyllama` em CPU: alguns segundos. Com GPU NVIDIA: quase instantâneo.

#### Resumo do fluxo completo

```
python3 gerar_iso.py
  └─ is_root() ✓
  └─ zypper install kiwi-ng
  └─ git clone cabelo/multicortex-exo
  └─ copytree → workdir/kiwi-desc/
  └─ patch config.xml (HTTP, repos, bootstrap, NVIDIA G06)
  └─ kiwi-ng --debug system build
       ├─ valida config.xml
       ├─ bootstrap: rpm instala 10 pkgs no root tree
       ├─ image: chroot + zypper instala ~800 pkgs
       ├─ copia overlay root/ → root tree
       ├─ executa config.sh no chroot
       │    ├─ autologin tux, GDM, GNOME
       │    ├─ enable: sshd, ollama, multicortex-chat-ui
       │    └─ ldconfig + runlevel 5 + exit 0
       ├─ dracut: gera initramfs com módulo kiwi-live
       ├─ mksquashfs: comprime com xz → ~1.8 GB
       ├─ monta estrutura ISO (EFI/, LiveOS/, isolinux/)
       └─ xorriso: gera .iso híbrido (UEFI + BIOS + pendrive)

dd → pendrive

UEFI → shim → GRUB2 → kernel + splash
  └─ initramfs: monta SquashFS + overlay ext4
  └─ systemd
       ├─ multicortex-firstboot → mkdir /var/lib/ollama
       ├─ ollama → listen :11434
       ├─ sshd → listen :22
       └─ gdm → autologin tux
  └─ GNOME Desktop
       ├─ config_osviacam.sh → gsettings + rm autostart (1x)
       └─ initMulticortex.sh → ollama run llama3.2

multicortex-models-light
  └─ ollama pull: tinyllama, phi3:mini, gemma3:1b, qwen3:0.6b, smollm2:1.7b
  └─ /var/lib/ollama/models/blobs/ (persistidos no pendrive)

ollama run tinyllama "pergunta"
  └─ carrega modelo → inferência → resposta
```

---

## Como compilar a ISO — referência rápida

### Requisito: openSUSE Leap 15.6 x86_64

VMware, VirtualBox, Proxmox ou máquina física.

### Opção 1: script Python (recomendado)

```bash
su -
python3 scripts/gerar_iso_multicortex_completo_py36.py

# Com limpeza total:
python3 scripts/gerar_iso_multicortex_completo_py36.py --clean

# Sem reinstalar pacotes:
python3 scripts/gerar_iso_multicortex_completo_py36.py --no-install

# Diretório customizado:
python3 scripts/gerar_iso_multicortex_completo_py36.py --workdir /mnt/builds
```

ISO em `/home/hawk/builds/out/`. Log em `builds/build-multicortex.log`.

### Opção 2: build manual

```bash
zypper refresh
zypper install -y git curl wget xz tar gzip cpio rsync which \
    ca-certificates ca-certificates-mozilla openssl

# Se kiwi-ng não estiver disponível:
zypper ar -f \
    https://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/ \
    kiwi-builder
zypper --gpg-auto-import-keys refresh
zypper install -y python311-kiwi
kiwi-ng --version

mkdir -p ~/builds/out
kiwi-ng --debug system build \
  --description $(pwd)/suse/x86_64/suse-leap-15.6-JeOS \
  --target-dir ~/builds/out \
  2>&1 | tee ~/builds/build.log
```

### Verificar resultado

```bash
find ~/builds/out -name "*.iso" -ls
sha256sum ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

### Erros comuns no build

| Erro | Causa | Solução |
|------|-------|---------|
| `baseMount() is obsolete` | Função removida no KIWI 10 | Comentar `baseMount`/`baseCleanMount` no `config.sh` |
| `suseConfig() is obsolete` | Função removida no KIWI 10 | Comentar `suseConfig` |
| `suseRemoveYaST() is obsolete` | Função removida no KIWI 10 | Comentar `suseRemoveYaST` |
| `gconftool-2: No such file or directory` | Scripts legados de tema | Já comentados neste fork |
| Avisos `NOKEY` nos RPMs | GPG não importado | `warning`, não `ERROR` — build prossegue |
| Conflito drivers NVIDIA | Versões 550 e 580 misturadas | Manter apenas pacotes G06 da mesma linha |
| Mirror BR falhando | `mirrorcache-br-2` instável | Usar `download.opensuse.org` (já configurado) |

---

## Como testar a ISO

### VMware

```
Sistema: Linux 64-bit / openSUSE 64-bit
Firmware: UEFI  |  Secure Boot: OFF
CPU: 4 cores  |  RAM: 8 GB  |  Disco: 40 GB  |  Rede: NAT
```

### QEMU/KVM

```bash
qemu-system-x86_64 -m 8192 -smp 4 \
  -cdrom MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  -boot d -enable-kvm
```

---

## Como gravar em pendrive

```bash
lsblk    # identificar /dev/sdX

sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
        of=/dev/sdX bs=4M status=progress conv=fsync
```

**Windows:** Rufus (GPT/UEFI para PCs modernos). **macOS/outros:** Balena Etcher.

---

## Comandos disponíveis na ISO

```bash
multicortex-status        # diagnóstico completo
multicortex-menu          # menu interativo (15 opções)
multicortex-models-light  # instala modelos leves
multicortex-models-medium # instala modelos médios
multicortex-models-code   # instala modelos de código
multicortex-models-large  # instala modelos grandes
multicortex-models-list   # lista modelos instalados
```

Aliases:

```bash
mc-status   mc-menu   mc-models
```

---

## API HTTP local do Ollama

Endpoint: `http://127.0.0.1:11434`

```bash
# Listar modelos
curl http://127.0.0.1:11434/api/tags

# Geração de texto
curl http://127.0.0.1:11434/api/generate \
  -d '{"model": "llama3.1:8b", "prompt": "Olá!", "stream": false}'

# Chat
curl http://127.0.0.1:11434/api/chat \
  -d '{"model": "llama3.1:8b",
       "messages": [{"role": "user", "content": "O que é IA local?"}],
       "stream": false}'
```

Manter em `127.0.0.1`. Para acesso remoto: `ssh -L 11434:localhost:11434 tux@<ip>`.

---

## Perfis de modelos de IA

### Leve — 8–16 GB RAM

```bash
multicortex-models-light
```

| Modelo | Params | Uso |
|--------|--------|-----|
| `tinyllama:latest` | 1.1B | Ultra-leve, rápido sem GPU |
| `phi3:mini` | 3.8B | Microsoft Phi-3, bom custo-benefício |
| `gemma3:1b` | 1B | Google Gemma 3 |
| `qwen3:0.6b` | 0.6B | Menor modelo disponível |
| `smollm2:1.7b` | 1.7B | HuggingFace SmolLM2 |

### Médio — 16–32 GB RAM, GPU 8–12 GB VRAM

```bash
multicortex-models-medium
```

| Modelo | Params | Uso |
|--------|--------|-----|
| `llama3.1:8b` | 8B | Meta LLaMA 3.1, equilíbrio ideal |
| `llama3.2:3b` | 3B | Meta LLaMA 3.2, rápido |
| `mistral:7b` | 7B | Forte em raciocínio |
| `qwen3:8b` | 8B | Alibaba, multilíngue |
| `gemma3:4b` | 4B | Google Gemma 3 médio |
| `qwen2.5:7b` | 7B | Bom em português |

### Código — 16–32 GB RAM

```bash
multicortex-models-code
```

| Modelo | Params | Especialidade |
|--------|--------|---------------|
| `deepseek-coder:1.3b` | 1.3B | DeepSeek leve |
| `deepseek-coder:6.7b` | 6.7B | DeepSeek completo |
| `qwen2.5-coder:7b` | 7B | Múltiplas linguagens |
| `codegemma:7b` | 7B | Python e C++ |
| `starcoder2:7b` | 7B | 600+ linguagens |

### Grande — 32–64+ GB RAM, GPU ≥12 GB VRAM

```bash
multicortex-models-large
```

| Modelo | Params | Uso |
|--------|--------|-----|
| `llama3.1:70b` | 70B | Qualidade próxima a GPT-4 |
| `llama3.3:70b` | 70B | Mais recente |
| `qwen2.5:32b` | 32B | Multilíngue forte |
| `qwen3:32b` | 32B | Qwen 3 médio-grande |
| `mixtral:8x7b` | 46.7B MoE | Mixture of Experts |
| `deepseek-r1:32b` | 32B | Raciocínio avançado |

> Sem GPU: modelos acima de 7B podem levar de 30 segundos a vários minutos por resposta.

---

## Persistência de dados

Com pendrive e espaço disponível, dados sobrevivem ao reinício:

```
/var/lib/ollama       modelos (podem ser GBs)
/home/tux             arquivos do usuário
/var/log/multicortex  logs
/opt/multicortex      scripts e configurações
```

Sem persistência, modelos baixados são perdidos ao reiniciar. Para uso repetido, pendrive com ≥80 GB para modelos médios.

---

## Edição offline com SSD

Para ambientes sem internet:

```bash
# 1. Com internet: baixar modelos
ollama pull tinyllama:latest
ollama pull llama3.1:8b

# 2. Copiar para SSD externo
rsync -av /var/lib/ollama /mnt/ssd-externo/

# 3. Manifesto de controle
ollama list > MODELOS.txt
sha256sum MODELOS.txt > MODELOS.txt.sha256
```

No ambiente offline: inicializar ISO + SSD, montar e usar.

---

## Requisitos de hardware

A ISO é **exclusivamente x86_64**. Não funciona em ARM, Raspberry Pi ou Apple Silicon.

**Mínimo para boot:** CPU x86_64, 4 GB RAM, UEFI recomendado, **Secure Boot desligado**.

| Uso | CPU | RAM | Armazenamento | GPU |
|-----|-----|-----|---------------|-----|
| VM / testes | qualquer quad-core | 8 GB | — | opcional |
| Modelos leves (≤3B) | i5 / Ryzen 5 | 16 GB | — | opcional |
| Modelos médios (7–8B) | i5 / Ryzen 5 | 16–32 GB | 80 GB+ | 8 GB VRAM recomendado |
| Modelos grandes (32–70B) | i7/i9 / Ryzen 7/9 | 32–64+ GB | SSD NVMe 128 GB+ | ≥12 GB VRAM |

---

## Diagnóstico e troubleshooting

```bash
# Status geral
multicortex-status
systemctl --failed

# Serviços
systemctl status ollama
journalctl -u ollama -f

# GPU
lspci | grep -i nvidia
nvidia-smi
lsmod | grep nvidia

# Rede
ip a
nmcli device status

# Ollama não responde
systemctl status ollama
curl http://localhost:11434
systemctl start ollama
ollama pull llama3.2   # se modelo não instalado
```

**Modelo lento:** verificar com `nvidia-smi` se GPU está sendo usada. Tentar modelo menor.

**ISO não inicia:** verificar SHA256, gravação correta, UEFI habilitado, Secure Boot desligado. Testar em VM primeiro.

---

## Segurança

- Trocar `root/linux` e `tux/linux` antes de usar em rede ou publicar ISO
- Manter Ollama em `127.0.0.1:11434` — nunca expor `0.0.0.0`
- SSH: autenticação por chave, desativar login root por senha, configurar firewall
- Não incluir dados de clientes, chaves ou tokens na ISO publicada

O `.gitignore` já exclui `*.iso`, `*.key`, `*.pem`, `*.token`, `*.env`, `models/`, `out/`, `build/`.

---

## Estado atual e pendências conhecidas

### O que funciona

- `config.xml` com todos os pacotes, repositórios e configurações
- `config.sh` com configurações de sistema e compatibilidade com KIWI 10
- Overlay `root/` com MOTD, versão, aliases, firstboot, rede, repositórios
- `multicortex-status.sh` e `multicortex-menu.sh` funcionais
- Script Python de build automático com patch do `config.xml`
- Temas visuais completos (GRUB2, Plymouth, GDM, GFXBOOT)
- ISO `MultiCortex_EXO_1.0.5` gerada e publicada

### Pendências

**Bug no `config.sh`:** o bloco `MULTICORTEX EXO GENERATED CONFIG` está após o `exit 0` e nunca executa. Mover para antes do `exit 0`.

**Scripts não commitados:**
```
scripts/build/check-build-env.sh      scripts/build/build-iso.sh
scripts/build/install-build-deps-opensuse.sh
scripts/models/install-light-models.sh
scripts/models/install-medium-models.sh
scripts/models/install-code-models.sh
scripts/models/install-large-models.sh
scripts/models/list-installed-models.sh
```

**Binários ausentes no overlay:** `multicortex-status`, `multicortex-menu` e `multicortex-models-*` precisam estar em `/usr/local/bin/` dentro da ISO.

**`/etc/multicortex.asc`** — logo ASCII referenciado pelo `initMulticortex.sh` mas não presente no overlay.

**`multicortex-chat-ui.service`** — habilitado mas sem arquivo `.service` no overlay.

**Framework `exo`** — `~/bin/exo` pressupõe virtualenv instalado manualmente.

---

## Publicar no GitHub Releases

```bash
command -v gh || zypper install -y gh
gh auth login

TAG="v1.0.5-leap15.6"

gh release create "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork \
  --title "MultiCortex EXO 1.0.5 Live ISO" \
  --notes "ISO Linux Live — openSUSE Leap 15.6 x86_64. GNOME, Ollama, NVIDIA G06, Python 3.12, Node.js 20." \
  --latest

# Atualizar assets de release existente
gh release upload "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork --clobber
```

---

## Licença e créditos

Este fork respeita a licença do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo) e as licenças de todos os componentes incluídos: openSUSE, KIWI NG, Ollama, drivers NVIDIA e demais pacotes. Antes de redistribuir a ISO publicamente, revisar as licenças dos pacotes proprietários NVIDIA.

**Projeto original:** Alessandro de Oliveira Faria (CABELO) — `cabelo@opensuse.org`

**Fork e adaptações:** Aguinaldo Liesack Baptistini — Hawk Informática

> Este projeto está em desenvolvimento ativo. Usar em ambiente de teste antes de aplicar em produção. Revisar scripts antes de executar comandos administrativos. Modelos de IA podem produzir respostas incorretas — a validação de qualquer ação é responsabilidade do usuário.
