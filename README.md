# multicortexEXO

**ISO Linux Live bootável** baseada em **openSUSE Leap 15.6 x86_64**, com ambiente GNOME, suporte a GPU NVIDIA e infraestrutura para execução local de modelos de linguagem (LLM) via **Ollama**.

Fork independente de [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo), com scripts próprios de build, overlay de sistema, documentação e estrutura de evolução autônoma.

---

## Índice

- [O que este projeto entrega](#o-que-este-projeto-entrega)
- [Versão e release](#versão-e-release)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Descrição técnica da ISO](#descrição-técnica-da-iso)
- [Descritor KIWI — config.xml](#descritor-kiwi--configxml)
- [Script de build — config.sh](#script-de-build--configsh)
- [Overlay root — arquivos copiados na ISO](#overlay-root--arquivos-copiados-na-iso)
- [Fluxo de boot](#fluxo-de-boot)
- [Serviços systemd](#serviços-systemd)
- [Credenciais padrão](#credenciais-padrão)
- [Como compilar a ISO](#como-compilar-a-iso)
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

## O que este projeto entrega

Uma ISO de aproximadamente 1,8 GB que, ao inicializar em qualquer PC x86_64, oferece:

- Ambiente GNOME completo com autologin do usuário `tux`
- Ollama rodando localmente na porta 11434 — backend de inferência LLM
- Atalho de desktop abrindo Firefox em `localhost:7001` (interface de chat)
- Terminal com aliases e comandos de diagnóstico e controle MultiCortex
- Suporte a GPU NVIDIA (drivers G06 — compute, utils, kernel module)
- Python 3.12, Node.js 20, compiladores e bibliotecas de desenvolvimento e IA
- SSH habilitado
- Estrutura para instalar modelos LLM por perfil de hardware após o boot

A ISO é híbrida UEFI + BIOS Legacy, suporta persistência de dados em ext4, e pode ser testada em VM.

Casos de uso diretos: bancada técnica, laboratório de IA, demonstração controlada, suporte offline, estação temporária de trabalho, testes de modelos LLM.

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
│   ├── functions.sh                     Funções Shell de boot do KIWI
│   ├── locale/                          Internacionalização do KIWI (40+ idiomas, .po e .mo)
│   ├── helper/kiwi-boot-packages        Lista de pacotes de boot
│   ├── package/                         Metadados RPM do kiwi-boot-descriptions
│   └── arch/                            Descritores de boot por arquitetura
│       ├── arm/oemboot/                 ARM: SLES12, SLES15, Leap 15.0, Leap 42.x, Tumbleweed
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
│   ├── gerar_iso_multicortex_completo_py36.py   Script Python de build automático (Python 3.6+)
│   └── system/
│       ├── multicortex-menu.sh          Menu interativo de controle do sistema
│       └── multicortex-status.sh        Diagnóstico completo do sistema
│
└── suse/x86_64/suse-leap-15.6-JeOS/    Descrição KIWI — núcleo da ISO
    ├── config.xml                       Pacotes, repositórios, usuários, tipo de imagem
    ├── config-1.0.0.xml                 Versão anterior do config.xml (referência)
    ├── configBUB.xml                    Variante experimental
    ├── config.sh                        Script de pós-build executado pelo KIWI no chroot
    ├── Dicefile                         Manifesto KIWI alternativo (formato Dice)
    ├── firstboot_scripts/config.sh      Script de firstboot legado
    ├── gdm.tar                          Tema GDM empacotado para boot
    ├── plymouth.tar                     Tema Plymouth empacotado para boot
    │
    ├── root/                            Overlay: tudo aqui é copiado diretamente na ISO
    │   ├── etc/
    │   │   ├── motd                     Mensagem exibida no login
    │   │   ├── multicortex-version      Versão do sistema (lida pelo multicortex-status)
    │   │   ├── profile.d/multicortex.sh Aliases (mc-status, mc-menu, mc-models) e OLLAMA_HOST
    │   │   ├── ld.so.conf.d/cuda.conf   Configuração do linker para CUDA
    │   │   ├── plymouth/plymouthd.conf  Configuração do Plymouth
    │   │   ├── sysconfig/network/ifcfg-lan0   Rede: DHCP automático no boot
    │   │   ├── systemd/system/
    │   │   │   ├── multicortex-firstboot.service   Cria /var/lib/ollama no primeiro boot
    │   │   │   ├── suse-studio-custom.service      Legado SUSE Studio
    │   │   │   └── suse-studio-firstboot.service   Legado SUSE Studio
    │   │   ├── udev/rules.d/70-persistent-net.rules
    │   │   └── zypp/repos.d/
    │   │       ├── jax_15.6.repo               Repositório JAX pré-configurado na ISO
    │   │       ├── openSUSE_Leap_15.6_OSS.repo
    │   │       └── openSUSE_Leap_15.6_Updates.repo
    │   │
    │   ├── home/tux/
    │   │   ├── bin/exo                  Ativa venv e executa framework exo (requer instalação manual)
    │   │   └── .config/autostart/
    │   │       └── init.desktop         Executa initMulticortex.sh no login do tux
    │   │
    │   ├── opt/multicortex/scripts/system/
    │   │   ├── multicortex-menu.sh      Cópia idêntica à de scripts/system/
    │   │   └── multicortex-status.sh    Cópia idêntica à de scripts/system/
    │   │
    │   └── usr/
    │       ├── bin/initMulticortex.sh   Autostart: exibe ASCII e tenta ollama run llama3.2
    │       ├── lib/systemd/system/grub_config.service   Só ativo em builds OEM/VMX
    │       ├── local/cuda/readme.txt    Placeholder para libs CUDA (instalação manual)
    │       └── share/
    │           ├── applications/Chat.desktop   Atalho GNOME → Firefox localhost:7001
    │           └── pixmaps/chat.png
    │
    └── usr/share/                       Assets visuais do descritor KIWI
        ├── gdm/themes/studio/           Tema GDM (fundo de login, logo, preview)
        ├── gfxboot/themes/studio/       Tema GFXBOOT (telas de boot/instalação)
        ├── grub2/themes/studio/         Tema GRUB2 (fontes DejaVu, backgrounds, sliders)
        ├── plymouth/themes/studio/      Tema Plymouth (splash de boot)
        └── wallpapers/                  Wallpaper padrão do sistema
```

> **Sobre `custom_boot/`:** Herdado integralmente do upstream (`kiwi-boot-descriptions`). Contém suporte de boot para ARM, PPC, IBM Z e x86_64 em diversas distribuições. Não foi modificado pelo fork — serve de referência para builds em outros ambientes.

---

## Descrição técnica da ISO

| Propriedade | Valor |
|-------------|-------|
| Nome da imagem | `MultiCortex_EXO_1.0.5` |
| Base | openSUSE Leap 15.6 x86_64 |
| Schema KIWI | 6.4 |
| Tipo | ISO Live híbrida (UEFI + BIOS Legacy) |
| Flags | overlay, hybrid, hybridpersistent (ext4), mediacheck |
| Kernel cmdline | `splash` |
| Locale | `pt_BR` |
| Teclado | `br` |
| Timezone | `UTC` |
| Gerenciador de pacotes | zypper |
| Bootloader tema | studio |
| Plymouth tema | studio |

### Pacotes incluídos — grupos principais

**Ambiente gráfico:** GNOME completo (`patterns-gnome-gnome_basis`, `gnome_utilities`, `gnome_internet`, `gnome_x11`, `gnome_imaging`), GDM com autologin do usuário `tux`, Firefox, terminal GNOME, NetworkManager GUI, Cheese.

**IA e desenvolvimento:** Python 3.12 + pip + setuptools, Python 3.x base, Node.js 20 + npm, gcc/g++, cmake, make, ninja, scons, git + git-lfs, OpenCV (`opencv-devel`), OpenCL (`opencl-headers`, `ocl-icd-devel`), protobuf, TBB (`tbb-devel`), libva, snappy, nlohmann_json, ShellCheck, ccache, patchelf, fdupes.

**NVIDIA:** `nvidia-drivers-insync-latest`, `nvidia-common-G06`, `nvidia-compute-G06`, `nvidia-compute-utils-G06`, `nvidia-utils-G06`, `nvidia-driver-G06-kmp-default`.

**Sistema:** `kernel-default`, GRUB2 + `grub2-x86_64-efi` + `shim` (UEFI), `syslinux` (BIOS), Plymouth, `openssh`, `iproute2`, `dhcp-client`, firmware de rede e dispositivos (intel, atmel, adaptec, bluez, alsa, ipw), `e2fsprogs`, `lvm2`, `parted`, `wpa_supplicant-gui`.

**ISO Live e OEM:** `dracut-kiwi-live`, `gfxboot-branding-openSUSE`, `dracut-kiwi-oem-repart`, `dracut-kiwi-oem-dump`.

### Repositórios configurados no build

| Repositório | Propósito |
|-------------|-----------|
| Virtualization:Appliances:Builder / Leap 15.6 | KIWI NG |
| openSUSE Leap 15.6 OSS + Updates | Base do sistema |
| openSUSE Leap 15.6 Non-OSS + Updates | Pacotes não-livres |
| home:cabelo:jax / 15.6 | Pacotes IA/OpenVINO do autor original |
| home:cabelo:innovators / 15.6 | Pacotes adicionais |
| download.nvidia.com/opensuse/leap/15.6 | Drivers NVIDIA |

---

## Descritor KIWI — config.xml

O `config.xml` define a imagem inteira. Os pontos críticos para customização:

**Tipo da imagem:** ISO híbrida com overlay e persistência ext4. Para mudar para OEM/instalável: alterar `image="iso"` para `image="oem"`.

**Usuários:** senhas em hash `md5-crypt`. Para gerar novo hash: `openssl passwd -1 'NovaSenha'`.

**Locale/teclado/timezone:** configurados como `pt_BR` / `br` / `UTC`. Ajustar conforme necessário antes do build.

**Repositórios:** URLs HTTP são usadas intencionalmente (não HTTPS) para evitar problemas de validação de certificado no chroot KIWI. O script Python de build converte HTTPS→HTTP automaticamente ao copiar o descritor.

**Pacotes NVIDIA:** para trocar de versão de driver, garantir que todos os pacotes G06 sejam da mesma linha (não misturar 550 e 580). Se o solver reclamar de conflitos, remover `nvidia-video-G06`, `nvidia-gl-G06` ou `kernel-firmware-nvidia-gspx-G06` do `config.xml`.

---

## Script de build — config.sh

Executado pelo KIWI dentro do chroot durante o build. Faz:

1. `suseSetupProduct` + `suseImportBuildKey` — setup básico do produto openSUSE
2. `solver.onlyRequires = true` no zypper — resolve apenas dependências estritas
3. Sysconfig: autologin de `tux` via GDM, NetworkManager ativo, GNOME como WM
4. Overlay: copia `.profile` e `config.xml` para `/studio/`, ajusta permissões de `/var/lib/ollama`
5. Scripts legados de tema GDM/GNOME **comentados** — incompatíveis com KIWI 10 (usam `gconftool-2`/`dconf`)
6. Habilita serviços: `sshd`, `ollama`, `multicortex-chat-ui`
7. Habilita `grub_config.service` apenas para builds OEM/VMX
8. Runlevel 5 (gráfico)
9. Remove `/usr/share/doc/`, `/opt/kde*`
10. `ldconfig`

> **Bug conhecido:** o bloco `# BEGIN MULTICORTEX EXO GENERATED CONFIG` está posicionado **após o `exit 0` final** do script, portanto nunca é executado pelo KIWI. Os comandos `mkdir /var/lib/ollama`, `chmod` nos scripts e `systemctl enable` para os serviços MultiCortex precisam ser movidos para **antes** do `exit 0`, ou os serviços não serão habilitados durante o build. Por ora, o `multicortex-firstboot.service` (que está no overlay `root/`) garante a criação dos diretórios na primeira inicialização.

---

## Overlay root — arquivos copiados na ISO

Tudo em `suse/x86_64/suse-leap-15.6-JeOS/root/` é copiado diretamente para dentro da ISO pelo KIWI.

### `/etc/motd`

Exibido no login do terminal. Lista os comandos disponíveis e informa as credenciais padrão.

### `/etc/multicortex-version`

String `0.99 Build 20260609 11:17`. Lida pelo `multicortex-status.sh` para exibição.

### `/etc/profile.d/multicortex.sh`

Carregado para todos os usuários em login de shell:

```bash
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

### `/etc/systemd/system/multicortex-firstboot.service`

Serviço `oneshot` executado após `network-online.target`. Cria `/var/lib/ollama` e `/var/log/multicortex` com permissão 755. Garante a estrutura mesmo que o `config.sh` não tenha criado durante o build.

### `/etc/sysconfig/network/ifcfg-lan0`

`BOOTPROTO=dhcp`, `STARTMODE=onboot` — DHCP automático na inicialização.

### `/etc/zypp/repos.d/`

Três repositórios pré-configurados dentro da ISO: OSS, Updates e JAX (`home:cabelo:jax`). Permitem instalar pacotes adicionais de IA/OpenVINO sem configuração manual.

### `/usr/bin/initMulticortex.sh`

Chamado pelo autostart no login do `tux`. Exibe o logo ASCII e tenta:

```bash
ollama run llama3.2 "Ola!"
```

Falha silenciosamente se o modelo não estiver instalado. Para funcionar, instalar previamente: `ollama pull llama3.2`.

### `/usr/share/applications/Chat.desktop`

Atalho GNOME que abre Firefox em `http://localhost:7001`. Sugere uma interface web de chat local nessa porta (Open WebUI ou similar).

### `/home/tux/bin/exo`

Ativa um virtualenv Python e executa o framework `exo` (para LLMs distribuídos entre dispositivos). O diretório `~/exo/.venv` não está na ISO — precisa ser criado manualmente após o boot:

```bash
cd ~/exo && python3 -m venv .venv && source .venv/bin/activate && pip install exo-inference
```

### `/opt/multicortex/scripts/system/`

Cópias idênticas dos scripts `multicortex-status.sh` e `multicortex-menu.sh` instaladas em `/opt/multicortex/`. Os comandos curtos `multicortex-status` e `multicortex-menu` em `/usr/local/bin/` devem ser criados como links para esses arquivos (pendência — ver seção de estado atual).

---

## Fluxo de boot

```
UEFI/BIOS → GRUB2 (tema studio)
  → kernel-default + initramfs (Plymouth splash)
  → dracut-kiwi-live monta SquashFS como overlay
     └── persistência ext4 ativada se espaço disponível no pendrive
  → systemd
     ├── multicortex-firstboot.service → mkdir /var/lib/ollama /var/log/multicortex
     ├── ollama.service → API em 127.0.0.1:11434
     ├── sshd.service → SSH na porta 22
     └── gdm.service → autologin tux
  → GNOME Desktop
     ├── autostart: initMulticortex.sh em terminal → tenta ollama run llama3.2
     └── atalho Chat.desktop → Firefox em localhost:7001
```

---

## Serviços systemd

| Serviço | Estado | Porta | Função |
|---------|--------|-------|--------|
| `sshd.service` | Habilitado | 22 | Acesso SSH remoto |
| `ollama.service` | Habilitado | 11434 | Backend LLM local |
| `multicortex-chat-ui.service` | Habilitado* | 3000 | Interface web local (planejada) |
| `open-webui.service` | Habilitado* | 8080 | Open WebUI alternativa |
| `multicortex-firstboot.service` | Habilitado | — | Cria diretórios na primeira inicialização |
| `grub_config.service` | Condicional | — | Só ativo em builds OEM/VMX |

\* *Habilitados no `config.sh`, mas o arquivo `.service` de `multicortex-chat-ui` não está no overlay. Requer instalação do pacote ou criação manual do arquivo de serviço.*

```bash
# Controle manual
systemctl status ollama
systemctl start|stop|restart ollama
journalctl -u ollama -f
```

---

## Credenciais padrão

```
Usuário  Senha    Grupo
root     linux    root
tux      linux    users
```

> **Trocar antes de usar em rede ou publicar ISO:**

```bash
passwd root
passwd tux
```

Para gerar novo hash no `config.xml` antes do build:

```bash
openssl passwd -1 'NovaSenhaAqui'
# Substituir o campo password= no config.xml com o hash gerado
```

---

## Como compilar a ISO

### Requisito: openSUSE Leap 15.6 x86_64

Build validado neste ambiente. VMware, VirtualBox, Proxmox ou máquina física funcionam.

### Opção 1: script Python (recomendado)

Compatível com Python 3.6+. Automatiza todas as etapas: instalação de dependências, clone do repo original, ajuste do `config.xml`, execução do KIWI.

```bash
# Como root:
python3 scripts/gerar_iso_multicortex_completo_py36.py

# Limpando build anterior:
python3 scripts/gerar_iso_multicortex_completo_py36.py --clean
```

A ISO é gerada em `/home/hawk/builds/out/` (ou `~/builds/out/` se `/home/hawk` não existir).

O script faz automaticamente:

- Instala `python3-kiwi`, `git`, `curl` e demais dependências via zypper
- Adiciona o repositório KIWI Builder se `kiwi-ng` não estiver disponível
- Clona `cabelo/multicortex-exo` ou atualiza via `git pull`
- Copia o descritor KIWI para diretório de trabalho limpo
- Converte URLs HTTPS → HTTP no `config.xml` (compatibilidade no chroot)
- Executa `kiwi-ng --debug system build` com log completo

### Opção 2: build manual

```bash
# Instalar KIWI NG
zypper refresh
zypper install -y git curl wget nano xz tar gzip cpio rsync which \
    ca-certificates ca-certificates-mozilla openssl

# Se kiwi-ng não estiver disponível:
zypper ar -f \
    https://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/ \
    kiwi-builder
zypper --gpg-auto-import-keys refresh
zypper install -y python311-kiwi

# Verificar versão
kiwi-ng --version

# Executar build
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
| `suseConfig() is obsolete` | Função removida no KIWI 10 | Comentar `suseConfig` no `config.sh` |
| `suseRemoveYaST() is obsolete` | Função removida no KIWI 10 | Comentar `suseRemoveYaST` no `config.sh` |
| `gconftool-2: No such file or directory` | Scripts legados de tema | Já comentados neste fork |
| Avisos `NOKEY` nos RPMs | GPG do pacote não importado | São `warning`, não `ERROR` — não impedem o build |
| Conflito de drivers NVIDIA | Versões 550 e 580 misturadas | Manter apenas drivers G06 da mesma linha |
| Mirror BR falhando | `mirrorcache-br-2.opensuse.org` instável | Usar mirrors diretos `download.opensuse.org` já configurados |

---

## Como testar a ISO

### VMware

```
Sistema operacional: Linux 64-bit / openSUSE 64-bit
Firmware: UEFI
Secure Boot: OFF
CPU: 4 cores
RAM: 8 GB (mínimo 4 GB para dar boot)
Disco: 40 GB
Rede: NAT
ISO: MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

### QEMU/KVM

```bash
qemu-system-x86_64 \
  -m 8192 \
  -smp 4 \
  -cdrom MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  -boot d \
  -enable-kvm
```

---

## Como gravar em pendrive

**Linux:**

```bash
# Identificar o dispositivo
lsblk

# Gravar (substituir /dev/sdX pelo dispositivo correto — APAGA TUDO)
sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
        of=/dev/sdX bs=4M status=progress conv=fsync
```

**Windows:** Rufus — selecionar GPT/UEFI para PCs modernos.

**macOS e outros:** Balena Etcher.

---

## Comandos disponíveis na ISO

### No terminal

```bash
multicortex-status        # diagnóstico completo: versão, rede, serviços, ollama, hardware, GPU, logs
multicortex-menu          # menu interativo de controle (15 opções)
multicortex-models-light  # instala modelos leves via Ollama
multicortex-models-medium # instala modelos médios via Ollama
multicortex-models-code   # instala modelos de código via Ollama
multicortex-models-large  # instala modelos grandes via Ollama
multicortex-models-list   # lista modelos instalados no Ollama
```

### Aliases disponíveis em qualquer shell

```bash
mc-status   # → multicortex-status
mc-menu     # → multicortex-menu
mc-models   # → multicortex-models-list
```

### Variável de ambiente

```bash
OLLAMA_HOST   # padrão: 127.0.0.1:11434  (definida em /etc/profile.d/multicortex.sh)
```

### O que faz `multicortex-status`

Exibe seções formatadas cobrindo: versão da ISO, hostname, kernel, arquitetura, IPs locais, URLs dos serviços, estado dos serviços systemd, teste live da API Ollama, lista de modelos instalados, CPU, RAM, uso de disco, saída do `nvidia-smi`, últimas 20 linhas do log do Ollama.

### O que faz `multicortex-menu`

Menu interativo (`while true`) com 15 opções:

| Opção | Ação |
|-------|------|
| 1 | `multicortex-status` |
| 2 / 3 / 4 | start / stop / restart `ollama.service` |
| 5 / 6 / 7 | start / stop / restart `multicortex-chat-ui` e `open-webui` |
| 8 | `multicortex-models-list` |
| 9 / 10 / 11 / 12 | instalar modelos light / medium / code / large |
| 13 | teste da API Ollama via curl |
| 14 | exibir IPs e URLs do sistema |
| 15 | sair |

---

## API HTTP local do Ollama

Endpoint base: `http://127.0.0.1:11434`

```bash
# Listar modelos instalados
curl http://127.0.0.1:11434/api/tags

# Geração de texto
curl http://127.0.0.1:11434/api/generate \
  -d '{"model": "llama3.1:8b", "prompt": "Olá!", "stream": false}'

# Chat multi-turno
curl http://127.0.0.1:11434/api/chat \
  -d '{
    "model": "llama3.1:8b",
    "messages": [{"role": "user", "content": "Resuma em 3 linhas o que é o MultiCortex EXO."}],
    "stream": false
  }'
```

Manter a API **apenas em `127.0.0.1`**. Para acesso remoto: túnel SSH, VPN ou proxy autenticado. Nunca expor `0.0.0.0:11434` diretamente na rede.

---

## Perfis de modelos de IA

Antes de instalar, confirmar que o Ollama está ativo:

```bash
systemctl status ollama
curl http://127.0.0.1:11434/api/tags
```

### Perfil leve — VMs, notebooks simples, 8–16 GB RAM

```bash
multicortex-models-light
```

Modelos: `tinyllama:latest` · `phi3:mini` · `gemma3:1b` · `qwen3:0.6b` · `smollm2:1.7b`

### Perfil médio — PCs com 16–32 GB RAM, GPU 8–12 GB VRAM

```bash
multicortex-models-medium
```

Modelos: `llama3.1:8b` · `llama3.2:3b` · `mistral:7b` · `qwen3:8b` · `gemma3:4b` · `qwen2.5:7b`

### Perfil código — programação, scripts, análise técnica

```bash
multicortex-models-code
```

Modelos: `deepseek-coder:1.3b` · `deepseek-coder:6.7b` · `qwen2.5-coder:7b` · `codegemma:7b` · `starcoder2:7b`

### Perfil grande — workstation com SSD NVMe e GPU ≥12 GB VRAM

```bash
multicortex-models-large
```

Modelos: `llama3.1:70b` · `llama3.3:70b` · `qwen2.5:32b` · `qwen3:32b` · `mixtral:8x7b` · `deepseek-r1:32b`

> Sem GPU dedicada, todos os perfis rodam via CPU. Modelos acima de 7B serão lentos em CPU.

---

## Persistência de dados

A ISO usa overlay ext4 híbrido. Em pendrive com espaço disponível, dados são salvos entre sessões.

Diretórios importantes para persistência:

```
/var/lib/ollama       modelos baixados
/home/tux             arquivos do usuário
/var/log/multicortex  logs do sistema
```

Sem persistência ativa (ex: boot por CD ou ISO em RAM), modelos baixados durante a sessão são perdidos ao reiniciar.

---

## Edição offline com SSD

Para ambientes sem internet:

1. Em uma máquina com internet, baixar modelos: `ollama pull llama3.1:8b mistral:7b ...`
2. Copiar `/var/lib/ollama` para um SSD/NVMe externo
3. No ambiente offline: iniciar a ISO, montar o SSD, copiar os modelos para `/var/lib/ollama` com persistência ativa

Gerar manifesto para controle e auditoria:

```bash
ollama list > MODELOS.txt
sha256sum MODELOS.txt > MODELOS.txt.sha256
```

---

## Requisitos de hardware

A ISO é **exclusivamente x86_64**. Não funciona em ARM, Raspberry Pi ou Apple Silicon.

### Mínimo para dar boot

- CPU x86_64 64 bits
- RAM: 4 GB
- Firmware: UEFI recomendado (suporta BIOS legacy)
- **Secure Boot: desligado**

### Por perfil de uso

| Uso | CPU | RAM | Armazenamento | GPU |
|-----|-----|-----|---------------|-----|
| VM / testes rápidos | qualquer quad-core | 8 GB | — | opcional |
| Modelos leves (≤3B) | i5 / Ryzen 5 | 16 GB | — | opcional |
| Modelos médios (7B) | i5 / Ryzen 5 | 16–32 GB | 80 GB+ | 8 GB VRAM recomendado |
| Modelos grandes (32–70B) | i7 / Ryzen 7+ | 32–64+ GB | SSD NVMe 128 GB+ | ≥12 GB VRAM |

---

## Diagnóstico e troubleshooting

### Status geral

```bash
multicortex-status
systemctl --failed
```

### Serviços individuais

```bash
systemctl status ollama
journalctl -u ollama -f
journalctl -u multicortex-chat-ui -f
```

### GPU

```bash
lspci | grep -i nvidia
nvidia-smi
lsmod | grep nvidia
```

### Rede

```bash
ip a
nmcli device status
ping 8.8.8.8
```

### Ollama não responde

```bash
systemctl status ollama
curl http://localhost:11434
ollama list
# Se o serviço não iniciou:
systemctl start ollama
# Se o modelo pedido não existe:
ollama pull llama3.2
```

### Modelo lento

Causas comuns: pouca RAM, modelo grande demais para o hardware, execução apenas por CPU, pendrive USB 2.0, falta de swap, GPU não detectada. Verificar com `multicortex-status` e `nvidia-smi`.

### ISO não inicia

Verificar: gravação correta do pendrive (SHA256), UEFI habilitado, Secure Boot desligado. Testar em VM antes de usar em hardware.

---

## Segurança

- Trocar `root/linux` e `tux/linux` antes de usar em rede, habilitar SSH ou publicar ISO
- Manter Ollama em `127.0.0.1:11434` — nunca expor `0.0.0.0` diretamente
- SSH: usar chaves, desativar login root por senha, configurar firewall
- Não incluir na ISO pública: dados de clientes, chaves privadas, tokens, arquivos `.env`
- Validar SHA256 de arquivos baixados antes de usar

O `.gitignore` já exclui: `*.iso`, `*.key`, `*.pem`, `*.token`, `*.env`, `secrets.yaml`, `models/`, `out/`, `build/`.

---

## Estado atual e pendências conhecidas

### O que funciona

- `config.xml` completo: pacotes, repositórios, usuários e tipo de imagem definidos
- `config.sh` com configurações de sistema, serviços e compatibilidade com KIWI 10
- Overlay `root/` com: MOTD, arquivo de versão, aliases de shell, serviço de firstboot, configuração de rede, repositórios pré-configurados, scripts de sistema
- `multicortex-status.sh` e `multicortex-menu.sh` funcionais
- Script Python de build automático (`gerar_iso_multicortex_completo_py36.py`)
- Documentação em `docs/`
- Temas visuais: GRUB2, Plymouth, GDM, GFXBOOT, wallpaper
- ISO `MultiCortex_EXO_1.0.5` gerada e publicada no GitHub Releases

### Pendências

**Bug no `config.sh`:** o bloco `MULTICORTEX EXO GENERATED CONFIG` está após o `exit 0` e nunca é executado. Mover para antes do `exit 0`.

**Scripts não commitados** — referenciados na documentação mas ausentes no repositório:

```
scripts/build/check-build-env.sh
scripts/build/install-build-deps-opensuse.sh
scripts/build/clean-build.sh
scripts/build/build-iso.sh
scripts/build/check-result.sh
scripts/models/_ollama_common.sh
scripts/models/install-light-models.sh
scripts/models/install-medium-models.sh
scripts/models/install-code-models.sh
scripts/models/install-large-models.sh
scripts/models/list-installed-models.sh
```

**Binários ausentes no overlay:** os comandos `multicortex-status`, `multicortex-menu` e `multicortex-models-*` precisam existir em `/usr/local/bin/` dentro da ISO — os links simbólicos ou scripts não estão no `root/`.

**`multicortex-chat-ui.service`:** habilitado no `config.sh`, mas o arquivo `.service` não está no overlay.

**Framework `exo`:** `/home/tux/bin/exo` pressupõe `~/exo/.venv` instalado manualmente após o boot.

---

## Publicar no GitHub Releases

A ISO não deve ser commitada — publicar como asset de release:

```bash
# Verificar CLI
command -v gh || zypper install -y gh
gh auth login

# Criar release
TAG="v1.0.5-leap15.6"

gh release create "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork \
  --title "MultiCortex EXO 1.0.5 Live ISO" \
  --notes "ISO Linux Live baseada em openSUSE Leap 15.6 x86_64. GNOME, Ollama, NVIDIA G06, Python 3.12, Node.js 20." \
  --latest

# Verificar
gh release view "$TAG" --repo hawkinf/multicortexEXO_fork

# Atualizar assets de uma release existente
gh release upload "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork \
  --clobber
```

---

## Licença e créditos

Este fork respeita a licença do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo) e as licenças de todos os componentes incluídos: openSUSE, KIWI NG, Ollama, drivers NVIDIA e demais pacotes de terceiros. Antes de redistribuir a ISO publicamente, revisar as licenças dos pacotes — especialmente drivers proprietários NVIDIA.

**Projeto original:** Alessandro de Oliveira Faria (CABELO) — `cabelo@opensuse.org`

**Fork e adaptações:** Aguinaldo Liesack Baptistini — Hawk Informática

> Este projeto está em desenvolvimento ativo. Usar em ambiente de teste antes de aplicar em produção. Revisar scripts antes de executar comandos administrativos. Modelos de IA podem produzir respostas incorretas — a validação de qualquer ação é responsabilidade do usuário.
