# Arquitetura — Como a ISO funciona

---

## Visão geral

O multicortexEXO é uma **ISO Linux Live híbrida** baseada em openSUSE Leap 15.6. "Híbrida" significa que um único arquivo `.iso` funciona em três contextos diferentes: boot em CD/DVD, boot em pendrive via BIOS legacy e boot em pendrive via UEFI moderno.

A principal diferença em relação a uma ISO Live genérica é o **sistema de camadas (overlay)** e a **infraestrutura de IA pré-configurada** que sobe automaticamente no boot.

---

## Como funciona o sistema de arquivos em camadas

O sistema não está instalado num disco. Ele vive comprimido dentro da ISO num formato chamado **SquashFS** — uma imagem somente-leitura que o kernel descomprime sob demanda, bloco a bloco.

Ao inicializar, o `dracut-kiwi-live` monta o SquashFS como camada inferior (read-only) e cria por cima uma **camada de escrita**:

- Em pendrive com espaço disponível: camada em **ext4 persistente** — dados sobrevivem ao reinício
- Sem espaço disponível: camada em **RAM (tmpfs)** — dados são perdidos ao desligar

Esse sistema de camadas se chama **overlay filesystem**. Qualquer arquivo que você crie ou modifique vai para a camada de escrita. O SquashFS original nunca é tocado. O sistema em execução enxerga os dois como um único sistema de arquivos normal.

```
┌─────────────────────────────────────┐
│  camada de escrita (ext4 ou tmpfs)  │  ← suas modificações
├─────────────────────────────────────┤
│  SquashFS (read-only)               │  ← sistema base, imutável
└─────────────────────────────────────┘
         ↕ kernel enxerga como /
```

---

## Diferenças em relação a um Linux normal

| Aspecto | openSUSE Leap 15.6 padrão | multicortexEXO |
|---------|--------------------------|----------------|
| **Modo de uso** | Instalação em disco | Live ISO + overlay persistente |
| **Ollama** | Não incluso | Instalado, configurado e habilitado no boot |
| **API de IA** | Não existe | `http://127.0.0.1:11434` disponível no boot |
| **Drivers NVIDIA** | Configuração manual | G06 incluídos no build |
| **Python** | 3.6 (padrão do Leap 15.6) | 3.12 + pip + setuptools |
| **Node.js** | Não incluso | 20 + npm |
| **Libs de IA** | Não inclusas | OpenCV, OpenCL, TBB, protobuf, nlohmann_json |
| **Comandos de controle** | Nenhum | `multicortex-status`, `multicortex-menu`, perfis de modelos |
| **Login automático** | Requer senha | Autologin do usuário `tux` |
| **Repositório JAX** | Não configurado | Pré-configurado dentro da ISO |

---

## Fluxo de boot completo

```
UEFI/BIOS
  └─ GRUB2 (UEFI) ou SYSLINUX (BIOS legacy)
       └─ kernel-default + initramfs (Plymouth splash)
            └─ dracut-kiwi-live
                 ├─ monta SquashFS read-only
                 ├─ cria camada ext4 (persistência) ou tmpfs
                 └─ pivot_root → sistema em overlay
  └─ systemd
       ├─ multicortex-firstboot.service → mkdir /var/lib/ollama /var/log/multicortex
       ├─ ollama.service              → escuta em 127.0.0.1:11434
       ├─ sshd.service                → escuta na porta 22
       └─ gdm.service                 → autologin tux
  └─ GNOME Desktop
       ├─ config_osviacam.sh (1x)    → configura aparência + se auto-remove
       └─ initMulticortex.sh          → exibe logo + tenta ollama run llama3.2
```

---

## Serviços systemd

### `multicortex-firstboot.service`

```ini
[Service]
Type=oneshot
ExecStart=/usr/bin/bash -lc 'mkdir -p /var/lib/ollama /var/log/multicortex; chmod 755 /var/lib/ollama /var/log/multicortex || true'
RemainAfterExit=yes
```

`Type=oneshot` executa uma vez e termina. `RemainAfterExit=yes` mantém o serviço como "ativo" para que outros possam depender dele. Cria `/var/lib/ollama` (onde os modelos ficam) e `/var/log/multicortex`. Existe porque o bloco do `config.sh` que criaria esses diretórios está após o `exit 0` e nunca executa.

### `ollama.service`

Instalado pelo pacote `ollama` (repositório JAX). Escuta em `127.0.0.1:11434`. Gerencia carregamento de modelos em RAM ou VRAM. Reinicia automaticamente em falha.

### `sshd.service`

SSH na porta 22. Acesso: `ssh tux@<ip>` ou `ssh root@<ip>`.

### `multicortex-chat-ui.service`

Habilitado no `config.sh`, mas sem arquivo `.service` no overlay. Deveria iniciar uma interface web de chat na porta 3000. **Pendência — não funciona ainda.**

### `open-webui.service`

Referenciado no menu e status, sem arquivo `.service` no overlay. Seria o [Open WebUI](https://github.com/open-webui/open-webui) na porta 8080. **Pendência.**

### `grub_config.service`

```ini
ConditionPathExists=/.kiwi_grub_config.trigger
ExecStart=/bin/bash -c 'grub2-mkconfig -o /boot/grub2/grub.cfg'
```

Só dispara em builds OEM (instalação em disco). O KIWI cria o arquivo trigger em builds OEM; na Live ISO ele nunca existe.

### `suse-studio-firstboot.service`

Legado do SUSE Studio. Configura rede DHCP, GNOME e se auto-deleta na primeira inicialização.

---

## Overlay root — arquivos copiados na ISO

Tudo em `suse/x86_64/suse-leap-15.6-JeOS/root/` é copiado pelo KIWI para dentro da ISO. Caminho preservado: `root/etc/motd` vira `/etc/motd`.

**`/etc/motd`** — exibido no terminal após o login. Lista comandos disponíveis e credenciais padrão.

**`/etc/multicortex-version`** — string de versão lida pelo `multicortex-status.sh`.

**`/etc/profile.d/multicortex.sh`** — carregado em todo shell de login:
```bash
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

**`/etc/ld.so.conf.d/cuda.conf`** — configura o linker para `/usr/local/cuda/lib64`. As libs CUDA devem ser instaladas manualmente nesse diretório.

**`/etc/sysconfig/network/ifcfg-lan0`** — `BOOTPROTO=dhcp`, `STARTMODE=onboot`. DHCP automático no boot.

**`/etc/zypp/repos.d/jax_15.6.repo`** — repositório `home:cabelo:jax` pré-configurado. Contém pacotes de IA (OpenVINO, OpenCV DNN). Permite `zypper install` após o boot sem configuração adicional.

**`/usr/local/cuda/readme.txt`** — placeholder com instrução para instalar libs CUDA manualmente.

**`/home/tux/.config/autostart/config.desktop`** — chama `config_osviacam.sh` no login (executa uma vez, depois se auto-remove).

**`/home/tux/.config/autostart/init.desktop`** — chama `initMulticortex.sh` em cada login.

**`/usr/share/applications/Chat.desktop`** — atalho GNOME que abre Firefox em `http://localhost:7001`.

---

## Programas incluídos e para que servem

### Infraestrutura de IA

**Ollama** — motor central. Gerencia modelos LLM. API REST em `127.0.0.1:11434`. Compatível com clientes da API OpenAI.

### Desenvolvimento

**Python 3.12** (`python312`, `python312-pip`, `python312-setuptools`) — o Leap 15.6 tem Python 3.6 por padrão. O 3.12 foi adicionado porque LangChain, transformers e a maioria das libs modernas de IA requerem Python ≥ 3.9.

**Node.js 20 + npm** (`nodejs20`, `npm20`) — para Open WebUI e outras interfaces web de chat.

**gcc / g++** — compiladores C/C++ para extensões nativas de Python, llama.cpp e código customizado.

**cmake / make / ninja / scons** — sistemas de build. cmake + ninja é a combinação padrão do llama.cpp e OpenCV.

**git / git-lfs** — git-lfs necessário para clonar repositórios do Hugging Face (pesos de modelos em arquivos grandes).

### Bibliotecas de computação

**OpenCV** (`opencv-devel`) — visão computacional. Necessária para modelos multimodais e processamento de imagem.

**OpenCL** (`opencl-headers`, `opencl-cpp-headers`, `ocl-icd-devel`) — computação paralela em GPU sem depender de CUDA.

**TBB** (`tbb-devel`) — Intel Threading Building Blocks. Paralelismo em CPU usado pelo OpenCV e frameworks de IA.

**Intel VA-API** (`libva-devel`, `vaapi-intel-driver`) — aceleração de vídeo por hardware Intel.

**protobuf** (`protobuf-devel`) — serialização usada pelo TensorFlow, ONNX e outros frameworks para salvar/carregar modelos.

**nlohmann/json** (`nlohmann_json-devel`) — JSON header-only para C++, usado pelo llama.cpp.

**snappy** (`snappy-devel`) — compressão rápida usada pelo TensorFlow e RocksDB.

**pugixml** (`pugixml-devel`) — parser XML leve para C++, usado pelo OpenVINO.

**ade-devel** — grafos de computação para o módulo DNN do OpenCV.

### Suporte NVIDIA

**`nvidia-drivers-insync-latest`** — meta-pacote do driver mais recente sincronizado com o kernel.

**`nvidia-common-G06`** — arquivos comuns do driver G06.

**`nvidia-compute-G06`** — bibliotecas CUDA. Necessário para o Ollama usar GPU para inferência.

**`nvidia-compute-utils-G06`** — `nvidia-persistenced` e utilitários auxiliares.

**`nvidia-utils-G06`** — `nvidia-smi` para monitoramento (usado pelo `multicortex-status`).

**`nvidia-driver-G06-kmp-default`** — módulo do kernel (`.ko`) compilado para o `kernel-default`.

**`ucode-intel`** — microcódigo Intel. Corrige bugs de hardware via firmware.

**`libdrm_intel1` / `libdrm_nouveau2`** — DRM para Intel e Nouveau. Renderização acelerada sem driver proprietário.

**`xf86-video-intel`** — driver Xorg para Intel HD/UHD Graphics.

### Ferramentas de qualidade

**ShellCheck** — analisador estático de scripts Shell.

**ccache** — cache de compilação. Reduz recompilações de projetos C/C++ como llama.cpp.

**patchelf** — modifica binários ELF para ajustar `RPATH`. Para redistribuir binários compilados.

**fdupes** — encontra e remove arquivos duplicados.

### Ambiente gráfico

**GNOME** (via `patterns-gnome-*`) — desktop completo. `gnome_basis` é o núcleo; `gnome_internet` adiciona Firefox; `gnome_utilities` adiciona ferramentas diversas; `gnome_imaging` adiciona Cheese.

**GDM** — gerenciador de display com autologin do `tux`.

**Firefox** — interface para o chat web local (`localhost:7001`).

**NetworkManager** (`NetworkManager-gnome`) — gerenciamento de rede com GUI.

**YaST2** (`yast2-control-center-gnome`) — painel de controle do openSUSE.

### Sistema e bootloader

**kernel-default** + **kernel-firmware** — kernel e firmwares de hardware.

**Firmwares específicos** (`atmel-firmware`, `adaptec-firmware`, `bluez-firmware`, `alsa-firmware`, `ipw-firmware`, `mpt-firmware`) — chipsets de Wi-Fi, RAID, Bluetooth e áudio.

**GRUB2 + shim + grub2-x86_64-efi** — bootloader UEFI com Secure Boot.

**syslinux** — bootloader BIOS legacy.

**Plymouth + tema studio** — splash screen animado.

**dracut-kiwi-live** — monta SquashFS como overlay. **Essencial para o Live ISO funcionar.**

**e2fsprogs** + **lvm2** — ferramentas ext4 e LVM para a partição de persistência.

**zypper** — gerenciador de pacotes. Permite instalar dentro da ISO com persistência ativa.

---

## Descrição técnica da imagem KIWI

| Propriedade | Valor |
|-------------|-------|
| Nome | `MultiCortex_EXO_1.0.5` |
| Base | openSUSE Leap 15.6 x86_64 |
| Schema KIWI | 6.4 |
| Tipo | `image="iso"` híbrida |
| Flags | `overlay`, `hybrid`, `hybridpersistent` |
| Sistema de persistência | ext4 |
| Verificação de mídia | `mediacheck=true` |
| Kernel cmdline | `splash` |
| Locale | `pt_BR` |
| Teclado | `br` |
| Timezone | `UTC` |
| Autologin | `tux` via GDM |
| Bootloader tema | studio |
| Plymouth tema | studio |
