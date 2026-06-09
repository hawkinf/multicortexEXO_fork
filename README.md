# multicortexEXO

**ISO Linux Live bootável** baseada em **openSUSE Leap 15.6 x86_64**, com ambiente GNOME, suporte a GPU NVIDIA e infraestrutura completa para execução local de modelos de linguagem (LLM) via **Ollama** — sem depender de nuvem, sem enviar dados para fora da máquina.

Fork independente de [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo), com scripts próprios de build, overlay de sistema, documentação técnica e estrutura de evolução autônoma.

---

## Índice

- [O que é e por que usar](#o-que-é-e-por-que-usar)
- [Como a ISO funciona — do boot ao modelo rodando](#como-a-iso-funciona--do-boot-ao-modelo-rodando)
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

## Como a ISO funciona — do boot ao modelo rodando

Entender o fluxo completo ajuda a saber onde mexer quando algo não funciona.

### 1. Boot — o que acontece antes do desktop aparecer

A ISO é uma imagem híbrida: funciona tanto em UEFI moderno quanto em BIOS legacy. O arquivo ISO contém dois bootloaders gravados em regiões específicas — GRUB2 para UEFI e SYSLINUX para BIOS. Quando você inicializa, o firmware do computador detecta o modo correto automaticamente.

O GRUB2 carrega o kernel (`kernel-default`) e o initramfs (imagem inicial compacta de sistema de arquivos). O Plymouth exibe o splash screen com o tema "studio" enquanto isso acontece. O kernel recebe o parâmetro `splash` que mantém esse visual até o desktop aparecer.

### 2. Montagem do sistema de arquivos em camadas (overlay)

Este é o mecanismo central que faz a ISO funcionar como Live. O sistema não está instalado num disco — ele vive comprimido dentro da ISO num formato chamado **SquashFS**, uma imagem somente-leitura.

O `dracut-kiwi-live` monta esse SquashFS e cria por cima uma **camada de escrita em RAM** (ou em ext4 no pendrive, se houver espaço). Esse sistema de camadas se chama overlay. Qualquer arquivo que você crie ou modifique vai para a camada de escrita — o SquashFS original nunca é tocado.

Resultado: a ISO é imutável, mas o sistema em execução se comporta como um Linux normal onde você pode criar arquivos, instalar pacotes, baixar modelos. Com persistência ativada (pendrive com espaço livre), essas mudanças sobrevivem ao reinício.

### 3. systemd sobe os serviços

Com o sistema de arquivos montado, o systemd inicia os serviços pela ordem de dependências:

- `multicortex-firstboot.service` é um dos primeiros — cria `/var/lib/ollama` e `/var/log/multicortex` com permissão 755, garantindo que os diretórios existam antes do Ollama tentar usá-los
- `ollama.service` inicia o servidor Ollama, que fica escutando em `127.0.0.1:11434`
- `sshd.service` inicia, permitindo acesso remoto pela porta 22
- `gdm.service` inicia o GDM (gerenciador de display)

### 4. Login automático e desktop

O GDM está configurado para fazer autologin do usuário `tux` sem pedir senha. O GNOME carrega com o wallpaper da distro e dois atalhos na área de trabalho.

### 5. Autostart — o que executa no primeiro segundo do desktop

Assim que o GNOME termina de carregar, dois processos de autostart disparam:

**`init.desktop`** — chama `/usr/bin/initMulticortex.sh` em um terminal. Esse script exibe o logo ASCII do MultiCortex (lido de `/etc/multicortex.asc`) e em seguida executa `ollama run llama3.2 "Ola!"`. Se o modelo `llama3.2` não estiver instalado, o Ollama tenta baixá-lo (requer internet) ou falha com mensagem de erro.

**`config.desktop`** — chama `/usr/bin/config_osviacam.sh`, que configura a aparência do GNOME via `gsettings`: define os apps favoritos da dock (Firefox, Terminal, Chat), fonte monoespaçada, tema Dark e wallpaper. Ao terminar, se deleta do autostart — executa apenas uma vez.

### 6. Sistema pronto

Neste ponto o sistema está operacional:

- Terminal com aliases `mc-status`, `mc-menu`, `mc-models`
- Ollama respondendo em `http://127.0.0.1:11434`
- Atalho `Chat` na dock do GNOME abrindo Firefox em `localhost:7001`
- Variável `OLLAMA_HOST` exportada para todos os shells
- SSH disponível na porta 22

---

## Diferenças em relação a um Linux normal

Uma ISO genérica do openSUSE Leap 15.6 é uma distribuição de propósito geral. Você baixa, instala, e depois passa horas configurando o que precisa. O multicortexEXO parte do mesmo base, mas é uma **distribuição de propósito específico** — foi montada para IA local já funcionar no boot.

### O que muda concretamente

| Aspecto | openSUSE Leap 15.6 padrão | multicortexEXO |
|---------|--------------------------|----------------|
| **Modo de uso** | Instalação em disco | Live ISO + overlay (opcional persistência) |
| **Ollama** | Não incluso | Instalado, configurado, habilitado no boot |
| **API de IA** | Não existe | `http://127.0.0.1:11434` disponível no boot |
| **Drivers NVIDIA** | Requer configuração manual | G06 incluídos no build |
| **Python** | 3.6 (padrão do Leap 15.6) | 3.12 + pip + setuptools adicionados |
| **Node.js** | Não incluso | 20 + npm incluídos |
| **Ferramentas de build IA** | Não inclusas | OpenCV, OpenCL, TBB, protobuf, nlohmann_json, libva já instalados |
| **Comandos de controle** | Nenhum | `multicortex-status`, `multicortex-menu`, perfis de modelos |
| **Login automático** | Requer senha | Autologin do usuário `tux` |
| **Repositório JAX** | Não configurado | Pré-configurado dentro da ISO |
| **Ambiente pronto** | Após instalação e configuração | No boot |

### O que o overlay adiciona que o Live normal não tem

Um Live CD genérico descarta tudo ao reiniciar. O multicortexEXO usa **overlay persistente em ext4** — se gravado em pendrive com espaço livre, os modelos baixados, arquivos criados e pacotes instalados sobrevivem ao reinício. Isso transforma o pendrive numa estação de trabalho portátil completa: pluga em qualquer PC x86_64, e você tem seu ambiente de IA exatamente como deixou.

---

## Programas incluídos e para que servem

### Infraestrutura de IA

**Ollama** — o motor central de toda a IA local. Gerencia download, carregamento em memória e execução de modelos LLM. Expõe uma API REST compatível com OpenAI em `127.0.0.1:11434`. Sem o Ollama nada funciona. Iniciado como serviço systemd no boot.

**Firefox** → `localhost:7001` — atalho na dock que abre o browser apontado para a porta onde uma interface web de chat pode estar rodando (Open WebUI ou similar). A interface em si precisa ser instalada separadamente.

### Ambiente de desenvolvimento

**Python 3.12** (`python312`, `python312-pip`, `python312-setuptools`, `python312-base`) — a versão mais recente disponível no Leap 15.6. O openSUSE Leap vem com Python 3.6 como padrão; o 3.12 foi explicitamente adicionado porque a maioria das bibliotecas modernas de IA (LangChain, transformers, etc.) requer Python ≥ 3.9. `pip` e `setuptools` incluídos para poder instalar qualquer pacote Python sem configuração adicional.

**Python 3.x base** (`python3-base`, `python3-devel`, `python3-pip`) — versão de compatibilidade mantida para ferramentas do sistema que dependem do Python padrão do openSUSE.

**Node.js 20 + npm** (`nodejs20`, `npm20`, `nodejs-common`) — runtime JavaScript necessário para Open WebUI e outras interfaces web de chat baseadas em Next.js ou similar.

**gcc / g++** (`gcc`, `gcc-c++`) — compiladores C e C++ para compilar extensões nativas de Python, bibliotecas de IA com código C++ (como llama.cpp) e qualquer código customizado.

**cmake / make / ninja / scons** (`cmake`, `make`, `ninja`, `scons`) — sistemas de build. cmake é usado pelo OpenCV e llama.cpp. ninja é o backend rápido do cmake. scons é alternativa usada por alguns projetos OpenVINO.

**git / git-lfs** (`git`, `git-lfs`) — controle de versão. git-lfs (Large File Storage) necessário para clonar repositórios de modelos do Hugging Face que armazenam pesos em arquivos grandes.

**pkg-config** — utilitário para localizar bibliotecas de desenvolvimento durante compilação.

### Bibliotecas de computação e visão

**OpenCV** (`opencv-devel`) — biblioteca de visão computacional. Necessária para processamento de imagem, vídeo e para modelos multimodais que trabalham com imagens junto com texto.

**OpenCL** (`opencl-headers`, `opencl-cpp-headers`, `ocl-icd-devel`) — interface para computação paralela em GPU. Permite que modelos usem a GPU via OpenCL quando CUDA não está disponível ou não é necessário.

**Intel VA-API** (`libva-devel`, `vaapi-intel-driver`) — aceleração de vídeo por hardware Intel. Útil para decodificação eficiente de vídeo em modelos multimodais.

**TBB** (`tbb-devel`) — Intel Threading Building Blocks. Biblioteca de paralelismo em CPU usada pelo OpenCV e por vários frameworks de IA para otimizar execução em múltiplos cores.

**libVDPAU** (`libvdpau_nouveau`) — aceleração de vídeo por hardware via VDPAU, usado por GPUs NVIDIA/Nouveau.

**protobuf** (`protobuf-devel`) — serialização de dados usada pelo TensorFlow, ONNX e outros frameworks de IA para salvar e carregar modelos.

**nlohmann/json** (`nlohmann_json-devel`) — biblioteca header-only de JSON para C++. Usada por llama.cpp e outros projetos nativos.

**snappy** (`snappy-devel`) — compressão rápida usada pelo TensorFlow e RocksDB.

**zlib** (`zlib-devel`) — compressão base, necessária para dezenas de bibliotecas.

**gflags** (`gflags-devel-static`) — biblioteca de flags de linha de comando para C++, usada por projetos como Caffe e alguns backends do TensorFlow.

**pugixml** (`pugixml-devel`) — parser XML leve para C++, usado pelo OpenVINO.

**ade-devel** — framework de grafos de computação usado pelo OpenCV DNN module.

### Suporte a NVIDIA (GPU)

**`nvidia-drivers-insync-latest`** — meta-pacote que instala o driver NVIDIA mais recente sincronizado com o kernel. Ponto de entrada principal.

**`nvidia-common-G06`** — arquivos comuns compartilhados entre todos os componentes do driver G06.

**`nvidia-compute-G06`** — bibliotecas CUDA para computação em GPU. Necessário para que o Ollama use a GPU NVIDIA para inferência.

**`nvidia-compute-utils-G06`** — utilitários de computação: `nvidia-persistenced` (mantém o driver carregado) e ferramentas auxiliares.

**`nvidia-utils-G06`** — `nvidia-smi` e outros utilitários de monitoramento da GPU. O `multicortex-status` chama `nvidia-smi` para exibir temperatura, uso de memória VRAM e outros dados.

**`nvidia-driver-G06-kmp-default`** — módulo do kernel NVIDIA compilado para o `kernel-default` do openSUSE. É o arquivo `.ko` que o kernel carrega para ter acesso à GPU.

**`ucode-intel`** — microcódigo para processadores Intel. Corrige bugs de hardware via firmware sem precisar de BIOS update.

**`libdrm_intel1` / `libdrm_nouveau2`** — bibliotecas DRM (Direct Rendering Manager) para Intel e Nouveau. Permitem renderização acelerada mesmo sem driver NVIDIA proprietário.

**`xf86-video-intel`** — driver Xorg para Intel HD/UHD Graphics. Necessário para exibição gráfica em sistemas com Intel integrado.

### Ferramentas de qualidade de código

**ShellCheck** (`ShellCheck`) — analisador estático de scripts Shell. Detecta erros comuns, variáveis não declaradas, quoting incorreto. Usado nos scripts de build para validação automática.

**ccache** (`ccache`) — cache de compilação. Armazena resultados de compilações anteriores. Reduz drasticamente o tempo de recompilação de projetos C/C++ como OpenCV ou llama.cpp.

**patchelf** (`patchelf`) — modifica binários ELF para ajustar caminhos de biblioteca (`RPATH`). Necessário para redistribuir binários compilados que precisam encontrar libs em locais não-padrão.

**fdupes** (`fdupes`) — encontra e remove arquivos duplicados. Útil para manter o overlay limpo.

### Ambiente gráfico

**GNOME** (via `patterns-gnome-*`) — ambiente desktop completo. O padrão `patterns-gnome-gnome_basis` puxa o núcleo do GNOME. `gnome_internet` adiciona Firefox e ferramentas de rede. `gnome_utilities` adiciona calculadora, monitor de sistema, etc. `gnome_imaging` adiciona Cheese (câmera) e ferramentas de imagem.

**GDM** — gerenciador de display. Configurado com autologin do `tux` para que o desktop apareça sem interação do usuário.

**GNOME Terminal** (`gnome-terminal`) — terminal emulador. É onde os comandos `multicortex-*` são executados.

**Cheese** (`cheese`) — aplicativo de câmera. Herdado do projeto original (que tinha foco em visão computacional com câmera). Permite usar câmera diretamente no ambiente.

**Firefox** (`MozillaFirefox`) — browser. Usado como interface para acessar o chat web local (`localhost:7001`) e outros serviços locais.

**NetworkManager** (`NetworkManager-gnome`) — gerenciamento de rede com interface gráfica. Permite configurar Wi-Fi e redes cabeadas via GUI sem precisar editar arquivos de configuração.

**wpa_supplicant-gui** — interface gráfica para redes Wi-Fi protegidas.

**YaST2** (`yast2-control-center-gnome`, `yast2-x11`) — painel de controle do openSUSE. Permite configurar o sistema graficamente: adicionar usuários, gerenciar partições, configurar firewall, etc.

### Sistema e bootloader

**kernel-default** — kernel Linux padrão do openSUSE. Compilado com módulos para a grande maioria dos hardwares.

**kernel-firmware** — firmwares de hardware: adaptadores Wi-Fi, placas de som, controladores de armazenamento. Sem isso, vários dispositivos não funcionam.

**Firmwares específicos** (`atmel-firmware`, `adaptec-firmware`, `bluez-firmware`, `alsa-firmware`, `ipw-firmware`, `mpt-firmware`) — firmwares para chipsets específicos de Wi-Fi (Atmel, Intel IPW), controladores RAID (Adaptec, MPT), Bluetooth (BlueZ) e áudio (ALSA).

**GRUB2** + **shim** + **grub2-x86_64-efi** — bootloader para UEFI. O `shim` é necessário para funcionar com Secure Boot desligado em sistemas UEFI modernos. `grub2-x86_64-efi` é o arquivo EFI que o firmware carrega.

**syslinux** — bootloader para BIOS legacy. Faz a ISO funcionar em PCs mais antigos.

**Plymouth** + tema studio — splash screen animado durante o boot.

**dracut-kiwi-live** — componente que monta o SquashFS como overlay no boot Live. Essencial para o funcionamento da ISO.

**dracut-kiwi-oem-repart** / **dracut-kiwi-oem-dump** — para builds OEM (instalação em disco). Não usados no modo Live.

**openssh** — servidor SSH. Permite acesso remoto ao sistema via terminal.

**iproute2** — ferramentas modernas de rede (`ip`, `ss`). Usadas pelo `multicortex-status` para listar IPs.

**dhcp-client** — cliente DHCP para obter IP automaticamente na rede.

**lvm2** — gerenciador de volumes lógicos. Necessário para sistemas com LVM.

**e2fsprogs** — ferramentas para sistema de arquivos ext2/3/4. Necessário para criar e verificar a partição de persistência.

**jeos-firstboot** — assistente de primeira inicialização do JeOS (Just Enough OS). Pode aparecer na primeira inicialização para configurações básicas.

**vim** — editor de texto via terminal.

**bash-completion** — auto-completar de comandos no bash.

**less** / **tar** / **which** / **parted** — utilitários básicos do sistema.

**zypper** — gerenciador de pacotes do openSUSE. Permite instalar pacotes adicionais dentro da ISO com persistência.

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

**Chamado por:** comando `multicortex-status` (ou alias `mc-status`) no terminal da ISO

**O que faz, linha a linha:**

O script define `set -Eeuo pipefail` — qualquer erro não tratado aborta a execução. A variável `OLLAMA_BASE_URL` usa o valor de `$OLLAMA_HOST` se definido, senão `http://127.0.0.1:11434`.

A função `section()` imprime um título formatado em azul ciano (`\033[1;36m`). A função `cmd_or_na()` executa um comando e imprime `N/A` se falhar, sem abortar o script.

**Seção Versão:** lê `/etc/multicortex-version` se existir, senão tenta `./VERSION`. Exibe a string de versão da ISO.

**Seção Sistema:** exibe `hostname`, `uname -r` (versão do kernel), `uname -m` (arquitetura). Lê `/etc/os-release` e filtra `PRETTY_NAME` e `VERSION_ID`.

**Seção Rede:** usa `ip -4 addr show scope global` para listar apenas IPs com escopo global (não loopback). Formata com `awk` para mostrar IP/máscara e nome da interface. Imprime as URLs prováveis de todos os serviços (Ollama API, tags endpoint, Web UI, Open WebUI).

**Seção Serviços:** itera sobre `ollama.service`, `multicortex-chat-ui.service`, `open-webui.service` e chama `systemctl is-active` para cada um. Exibe `active`, `inactive` ou `failed`.

**Seção Ollama API:** chama `curl -fsS http://127.0.0.1:11434/api/tags` e salva em `/tmp/multicortex-tags.json`. Se a chamada funcionar, imprime "OK" e lista os modelos usando `jq -r '.models[]?.name'`. Se `jq` não estiver disponível, imprime o JSON bruto.

**Seção Modelos via ollama list:** executa `ollama list` diretamente (formato tabular diferente do JSON da API).

**Seção Hardware:** usa `lscpu | awk` para extrair o campo "Model name" do processador. Executa `free -h` (uso de RAM) e `df -h /` (espaço em disco na raiz). Verifica se `nvidia-smi` existe: se sim, executa e exibe a saída completa (temperatura, uso de VRAM, processos usando GPU).

**Seção Logs recentes:** `journalctl -u ollama.service -n 20 --no-pager` — últimas 20 linhas do log do Ollama.

Todas as seções usam `|| true` nos comandos opcionais para não abortar se uma ferramenta não estiver disponível.

---

### `multicortex-menu.sh`

**Localização:** `scripts/system/multicortex-menu.sh` (cópia em `root/opt/multicortex/scripts/system/`)

**Chamado por:** comando `multicortex-menu` (ou alias `mc-menu`)

**O que faz:**

Loop `while true` com `clear` antes de cada iteração — a tela é sempre limpa antes de mostrar o menu. O menu é exibido via `cat <<'MENU'` (heredoc). O `read` aguarda o usuário digitar uma opção.

**Função `run()`:** recebe um comando como argumento, imprime `>>> comando` e executa. Depois do comando terminar, exibe `read -r -p "Enter para voltar..."` para pausar antes de limpar a tela. Isso evita que a saída de um comando desapareça imediatamente.

**Função `service_cmd()`:** recebe `action` (start/stop/restart) e `svc` (nome do serviço). Tenta `sudo systemctl action svc` primeiro; se falhar (ex: sudo não disponível), tenta `systemctl action svc` sem sudo. Usa `|| true` para não abortar se ambos falharem.

**Função `show_urls()`:** imprime as URLs hardcoded de todos os serviços (11434, 3000, 8080) e lista os IPs reais da máquina via `ip -4 addr show scope global`.

**Função `test_api()`:** executa `curl -fsS http://127.0.0.1:11434/api/tags` e imprime o resultado JSON bruto. Rápido para verificar se o Ollama está respondendo sem precisar sair do menu.

**Mapeamento de opções:**

| Opção | Execução real |
|-------|--------------|
| 1 | `run multicortex-status` |
| 2 | `service_cmd start ollama.service` |
| 3 | `service_cmd stop ollama.service` |
| 4 | `service_cmd restart ollama.service` |
| 5 | `service_cmd start multicortex-chat-ui.service` + `service_cmd start open-webui.service` |
| 6 | stop em ambos os serviços de UI |
| 7 | restart em ambos os serviços de UI |
| 8 | `run multicortex-models-list` |
| 9 | `run multicortex-models-light` |
| 10 | `run multicortex-models-medium` |
| 11 | `run multicortex-models-code` |
| 12 | `run multicortex-models-large` |
| 13 | `run test_api` (curl no Ollama) |
| 14 | `run show_urls` |
| 15 | `exit 0` |

Opção inválida: imprime "Opção inválida." e aguarda 1 segundo antes de redesenhar o menu.

---

### `initMulticortex.sh`

**Localização:** `suse/.../root/usr/bin/initMulticortex.sh`

**Chamado por:** `init.desktop` no autostart do GNOME do usuário `tux`

**O que faz:**

```bash
cat /etc/multicortex.asc   # exibe logo ASCII do MultiCortex
echo " "
echo "Initializing..."
echo " "
ollama run llama3.2 "Ola!"
```

Esse é o script que dispara no login gráfico. O arquivo `/etc/multicortex.asc` não está no overlay — é um arquivo que deveria estar na ISO mas não foi adicionado ainda. Se não existir, `cat` retorna erro mas o script continua.

A linha `ollama run llama3.2 "Ola!"` envia a mensagem "Ola!" para o modelo `llama3.2`. Se o modelo não estiver instalado, o Ollama tenta baixá-lo (requer internet). Se não houver internet e o modelo não estiver no disco, falha com erro.

O terminal onde isso roda fica aberto — o usuário pode continuar usando o Ollama interativamente após a mensagem inicial.

---

### `config_osviacam.sh`

**Localização:** `suse/.../root/usr/bin/config_osviacam.sh`

**Chamado por:** `config.desktop` no autostart do GNOME (executa apenas uma vez)

**O que faz:**

```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface monospace-font-name 'Monospace 12'
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"

rm /home/tux/.config/autostart/config.desktop
```

Configura a aparência do GNOME para o usuário `tux` via `gsettings`:

- **Dock (favorites):** define os três apps na dock do GNOME — Firefox, Terminal e Chat (o atalho para localhost:7001)
- **Fonte monoespaçada:** Monospace 12pt (para terminais e editores)
- **Tema:** Dark (tema escuro do GNOME)
- **Wallpaper:** aponta para `/usr/share/wallpapers/studio_wallpaper.jpg` (o wallpaper do projeto)

Por fim, **remove o próprio arquivo de autostart** (`/home/tux/.config/autostart/config.desktop`). Isso garante que essas configurações sejam aplicadas apenas uma vez, no primeiro login — nas inicializações seguintes o arquivo não existe mais e o script não é chamado.

---

### `exo` (script do usuário tux)

**Localização:** `suse/.../root/home/tux/bin/exo`

**Chamado por:** usuário manualmente (`~/bin/exo` ou simplesmente `exo` se `~/bin` estiver no PATH)

**O que faz:**

```bash
cd ~/exo
source .venv/bin/activate
exo
```

Navega para o diretório `~/exo`, ativa o virtualenv Python em `.venv/` e executa o binário `exo`. O framework [exo](https://github.com/exo-explore/exo) permite distribuir a execução de um LLM entre múltiplos dispositivos na rede local — cada máquina processa parte do modelo, viabilizando rodar modelos grandes sem uma única GPU potente.

O diretório `~/exo` e o virtualenv **não estão na ISO** — precisam ser criados manualmente:

```bash
mkdir ~/exo && cd ~/exo
python3.12 -m venv .venv
source .venv/bin/activate
pip install exo-inference
```

---

### `config.sh` — script de build KIWI

**Localização:** `suse/x86_64/suse-leap-15.6-JeOS/config.sh`

**Executado por:** KIWI NG durante o build da ISO, dentro do chroot (sistema de arquivos isolado da imagem em construção). Roda como root. Tem acesso à imagem ainda não comprimida.

**O que faz em sequência:**

**1. Carrega funções e perfil do KIWI:**
```bash
test -f /.kconfig && . /.kconfig
test -f /.profile && . /.profile
```
Importa as funções utilitárias do KIWI (`suseSetupProduct`, `suseInsertService`, etc.) se disponíveis.

**2. Setup do produto openSUSE:**
```bash
suseSetupProduct      # cria /etc/products.d/baseproduct symlink
suseImportBuildKey    # importa chaves GPG da SUSE para o banco de chaves RPM
```

**3. Otimização do zypper:**
```bash
sed --in-place -e 's/# solver.onlyRequires.*/solver.onlyRequires = true/' /etc/zypp/zypp.conf
```
Faz o zypper resolver apenas dependências `Requires`, ignorando `Recommends` e `Suggests`. Reduz o número de pacotes instalados e evita que pacotes recomendados mas não necessários entrem na imagem.

**4. Configurações de sysconfig:**
```bash
baseUpdateSysConfig /etc/sysconfig/keyboard KEYTABLE us.map.gz
baseUpdateSysConfig /etc/init.d/suse_studio_firstboot NETWORKMANAGER yes
baseUpdateSysConfig /etc/sysconfig/console CONSOLE_FONT lat9w-16.psfu
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER_AUTOLOGIN tux
baseUpdateSysConfig /etc/sysconfig/displaymanager DISPLAYMANAGER gdm
baseUpdateSysConfig /etc/sysconfig/windowmanager DEFAULT_WM gnome
```
Define: teclado US durante o build (o `keytable br` do config.xml ajusta no boot), NetworkManager ativo, autologin do `tux` via GDM, GNOME como WM padrão.

**5. Preparação do overlay:**
- Cria `/studio/` se não existir
- Copia `.profile` e `config.xml` para `/studio/` (usado pelo firstboot legado)
- Remove `/studio/overlay-tmp` (limpeza de arquivos temporários)
- Se o usuário `ollama` existir e `/var/lib/ollama` existir, ajusta proprietário para `ollama:ollama`
- **Comenta os scripts legados** de tema GDM/GNOME — `configure_gdm_theme.sh` e `configure_gnome_background.sh` usavam `gconftool-2` que não existe no KIWI 10

**6. Ativação de serviços:**
```bash
suseInsertService sshd
suseInsertService ollama
suseInsertService multicortex-chat-ui
```
Equivalente a `systemctl enable` mas usando a API do KIWI. Habilita `sshd`, `ollama` e `multicortex-chat-ui` para iniciar no boot.

Para builds OEM/VMX habilita `grub_config`; para ISO Live remove esse serviço.

**7. Runlevel 3 e limpeza:**
```bash
baseSetRunlevel 3          # modo multi-user sem gráfico (temporário durante o build)
rm -rf /usr/share/doc/packages/*    # remove documentação dos pacotes
rm -rf /usr/share/doc/manual/*
rm -rf /opt/kde*                    # remove resquícios de KDE se houver
sed -i -e's/^syntax on/" syntax on/' /etc/vimrc   # desativa syntax highlighting no vim
```

**8. ldconfig e runlevel 5:**
```bash
/sbin/ldconfig      # reconstrói cache de bibliotecas dinâmicas
baseSetRunlevel 5   # modo gráfico (final)
```

**9. exit 0**

O script termina aqui. O bloco `MULTICORTEX EXO GENERATED CONFIG` abaixo do `exit 0` **nunca é executado** — é código morto que precisa ser movido para antes do `exit 0`.

---

### `gerar_iso_multicortex_completo_py36.py`

**Localização:** `scripts/gerar_iso_multicortex_completo_py36.py`

**Executado por:** usuário root no host openSUSE Leap 15.6, antes de qualquer build

**Compatibilidade:** Python 3.6+ (usa apenas stdlib: `argparse`, `os`, `re`, `shutil`, `subprocess`, `sys`, `pathlib`)

**Argumentos de linha de comando:**

```
--workdir PATH    pasta de trabalho (padrão: /home/hawk/builds se existir, senão ~/builds)
--clean           apaga a pasta de trabalho inteira antes de começar
--no-install      pula a instalação de pacotes no host (assume que kiwi-ng já está disponível)
```

**O que faz em sequência:**

**1. Verificação de root:**
```python
if not is_root():
    print("ERRO: rode como root.")
    sys.exit(1)
```
KIWI precisa de root para montar sistemas de arquivos, usar loop devices e fazer chroot.

**2. Detecção do sistema operacional:**
Lê `/etc/os-release` e verifica se `VERSION_ID == "15.6"`. Emite aviso se não for, mas não aborta — permite build experimental em outras versões.

**3. Instalação de dependências no host (`ensure_host_packages`):**
Executa `zypper --gpg-auto-import-keys refresh` para atualizar os repositórios. Instala:
```
git, python3, python3-pip, python3-kiwi, curl, wget, nano,
xz, tar, gzip, cpio, rsync, which, ca-certificates,
ca-certificates-mozilla, openssl
```
Se `kiwi-ng` não estiver disponível após a instalação, adiciona o repositório KIWI Builder (`Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/`) e tenta instalar novamente. Verifica o resultado com `kiwi-ng --version`.

**4. Clone ou atualização do repositório (`clone_or_update`):**
Verifica se `workdir/multicortex-exo/.git` existe. Se sim: `git pull --ff-only` (atualização rápida sem merge). Se não: `git clone https://github.com/cabelo/multicortex-exo.git`. Valida que o diretório `suse/x86_64/suse-leap-15.6-JeOS` existe dentro do clone.

**5. Cópia do descritor KIWI (`copy_kiwi_descriptor`):**
Copia `multicortex-exo/suse/x86_64/suse-leap-15.6-JeOS` para `workdir/kiwi-desc` usando `shutil.copytree`. Remove o destino antes se existir. Valida que `config.xml` existe na cópia.

**6. Patch do `config.xml` (`patch_config_xml`):**

*Substituições de URL (HTTPS → HTTP):*
```
obs://Virtualization:Appliances:Builder/... → http://download.opensuse.org/.../
https://download.opensuse.org/... → http://download.opensuse.org/...
https://download.opensuse.org/repositories/home:/cabelo:/jax/... → http://...
```
Necessário porque o chroot KIWI pode ter problemas de certificado HTTPS. HTTP funciona de forma mais confiável em ambientes isolados.

*Adição de repositórios faltantes:*
Verifica se os repositórios non-oss e NVIDIA já estão no XML. Se não estiverem, os insere antes do bloco `<packages type="image">` usando regex.

*Adição de pacotes bootstrap:*
Garante que `ca-certificates-mozilla` e `openssl` estejam no bloco `<packages type="bootstrap">` (pacotes instalados primeiro, antes de tudo). Resolve problemas de certificado durante o build.

*Garantia dos pacotes NVIDIA G06:*
Verifica se cada pacote da lista está presente no XML:
```
nvidia-common-G06, nvidia-compute-G06, nvidia-compute-utils-G06,
nvidia-utils-G06, nvidia-driver-G06-kmp-default
```
Se algum estiver faltando, insere no bloco `<packages type="image">`.

*Compatibilidade com KIWI 10:*
Comenta `baseMount` e `baseCleanMount` no `config.sh` se ainda estiverem presentes (funções removidas no KIWI 10 que causam erro).

Ao final, imprime um relatório mostrando: pacotes NVIDIA garantidos, todas as URLs de repositório, pacotes bootstrap críticos.

**7. Build da ISO (`build_iso`):**
Apaga e recria `workdir/out/`. Executa:
```
kiwi-ng --debug system build \
  --description workdir/kiwi-desc \
  --target-dir workdir/out
```
Usa `subprocess.Popen` com `stdout=PIPE` para ler a saída linha a linha — imprime em tempo real na tela E grava em `workdir/build-multicortex.log`. Se o código de retorno for diferente de zero, informa o erro e a localização do log. Se nenhum `.iso` for encontrado em `workdir/out/`, reporta os arquivos presentes e encerra com erro 2. Em caso de sucesso, lista os arquivos `.iso` gerados com tamanho em GiB.

---

### Scripts legados (`studio/`)

**`configure_gdm_theme.sh`** — configura o tema visual do GDM (login screen). Usa `gconftool-2` para GNOME 2/SLED 10 e comandos diretos para openSUSE 11.4. Também habilita acesso remoto via `gconftool-2`. **Não é executado** no build atual — foi comentado no `config.sh` porque o `gconftool-2` não existe em GNOME 3 (presente no Leap 15.6).

**`configure_gnome_background.sh`** — configura o wallpaper do GNOME. Tenta três abordagens: gconftool para GNOME 2, gconftool para openSUSE 11.4, e gsettings moderno. Ao final, define favoritos da dock e tema via `gsettings` — essa parte seria útil, mas o script inteiro foi desabilitado para evitar falha no `gconftool-2`. **Não é executado.**

**`firstboot_scripts/config.sh`** — versão legada do script de firstboot. Configura GNOME via `gsettings` (favoritos, fonte, tema, wallpaper) e faz `c_rehash` (reconstrói hashes de certificados SSL). Ativa `sshd` e outros serviços. **Não é executado** no build atual — substituído pelo `config.sh` principal.

---

### `suse_studio_firstboot`

**Localização:** `root/etc/init.d/suse_studio_firstboot`

**Chamado por:** `suse-studio-firstboot.service` na primeira inicialização

**O que faz:**

Script complexo de configuração de primeira inicialização, herdado do SUSE Studio. Detecta automaticamente todas as interfaces de rede Ethernet (`ls /sys/class/net/`) e configura DHCP para cada uma. Em modo "Testdrive" (máquina virtual da plataforma SUSE Studio), desativa efeitos visuais do KDE e a ferramenta vmtoolsd.

Configura o GNOME: define apps favoritos na dock, fonte monoespaçada, tema Dark, wallpaper do projeto.

Ao final, **se auto-desativa e se auto-deleta**:
```bash
systemctl disable suse-studio-firstboot
rm -f /etc/systemd/system/suse-studio-firstboot.service
rm -f /etc/init.d/suse_studio_firstboot
```
Executa apenas uma vez.

---

## Serviços systemd — o que faz cada um

### `multicortex-firstboot.service`

```ini
[Service]
Type=oneshot
ExecStart=/usr/bin/bash -lc 'mkdir -p /var/lib/ollama /var/log/multicortex; chmod 755 /var/lib/ollama /var/log/multicortex || true'
RemainAfterExit=yes
```

`Type=oneshot` — executa uma vez e termina. `RemainAfterExit=yes` — o systemd considera o serviço "ativo" mesmo após o processo terminar, o que permite que outros serviços dependam dele com `After=multicortex-firstboot.service`.

Cria `/var/lib/ollama` (onde o Ollama armazena modelos, manifests e blobs) e `/var/log/multicortex` (logs do sistema MultiCortex). Ambos com permissão 755. Necessário porque o build KIWI não executa o bloco MultiCortex do `config.sh` (bug do `exit 0` antecipado).

### `ollama.service`

Instalado pelo pacote `ollama` (do repositório JAX). Inicia o servidor Ollama em `127.0.0.1:11434`. Gerencia o carregamento de modelos em memória (RAM ou VRAM da GPU). Reinicia automaticamente em caso de falha.

### `sshd.service`

Servidor OpenSSH. Permite acesso remoto à ISO via `ssh tux@<ip>` ou `ssh root@<ip>`. Útil para gerenciar a máquina remotamente sem precisar de teclado/monitor.

### `multicortex-chat-ui.service`

Habilitado no `config.sh` (`suseInsertService multicortex-chat-ui`), mas **o arquivo `.service` não está no overlay**. O serviço não tem definição — provavelmente seria instalado por um pacote ou criado manualmente. Deveria iniciar uma interface web de chat na porta 3000.

### `open-webui.service`

Referenciado no menu e no status, mas também sem arquivo `.service` no overlay. Seria o [Open WebUI](https://github.com/open-webui/open-webui) — interface web para Ollama — na porta 8080.

### `grub_config.service`

```ini
[Service]
ExecStart=/bin/bash -c 'grub2-mkconfig -o /boot/grub2/grub.cfg'
ExecStartPost=/bin/bash -c 'rm -f /.kiwi_grub_config.trigger'
ConditionPathExists=/.kiwi_grub_config.trigger
```

Reconstrói o `grub.cfg` após a instalação em disco (builds OEM). Ativado apenas quando o arquivo `.kiwi_grub_config.trigger` existe — o KIWI cria esse arquivo em builds OEM para sinalizar que o GRUB precisa ser reconfigurado após o primeiro boot.

### `suse-studio-firstboot.service` e `suse-studio-custom.service`

Serviços legados do SUSE Studio. O `firstboot` executa `/etc/init.d/suse_studio_firstboot` (visto acima) e depois se auto-deleta. O `custom` executaria `/studio/suse-studio-custom` se esse arquivo existir — permite scripts de customização pós-boot. Ambos são herança da plataforma SUSE Studio.

---

## Overlay root — arquivos copiados na ISO

Tudo em `suse/x86_64/suse-leap-15.6-JeOS/root/` é copiado pelo KIWI para dentro da ISO durante o build. O caminho é preservado — `root/etc/motd` vira `/etc/motd` na ISO.

**`/etc/motd`** — exibido no terminal após o login SSH ou console. Lista todos os comandos disponíveis e informa as credenciais padrão.

**`/etc/multicortex-version`** — string `0.99 Build 20260609 11:17`. Lida pelo `multicortex-status.sh` para exibir a versão da ISO.

**`/etc/profile.d/multicortex.sh`** — carregado automaticamente para todos os usuários em qualquer shell de login:
```bash
export OLLAMA_HOST="${OLLAMA_HOST:-127.0.0.1:11434}"
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

**`/etc/ld.so.conf.d/cuda.conf`** — configura o linker dinâmico para procurar bibliotecas em `/usr/local/cuda/lib64`. As bibliotecas CUDA em si precisam ser copiadas manualmente para `/usr/local/cuda/` — o diretório existe mas tem apenas um `readme.txt`.

**`/etc/sysconfig/network/ifcfg-lan0`** — configura a interface `lan0` para DHCP automático (`BOOTPROTO=dhcp`, `STARTMODE=onboot`). A interface Ethernet principal ganha IP automaticamente no boot.

**`/etc/zypp/repos.d/jax_15.6.repo`** — repositório `home:cabelo:jax` pré-configurado dentro da ISO. Contém pacotes de IA como OpenVINO, OpenCV com DNN, e outras bibliotecas do projeto original. Permite instalar esses pacotes com `zypper install` após o boot sem precisar adicionar o repositório manualmente.

**`/usr/local/cuda/readme.txt`** — instrução: "Place all CUDA library files here." É um placeholder para instalação manual das libs CUDA, caso o usuário queira usar CUDA além do que os drivers NVIDIA já fornecem.

---

## Credenciais padrão

```
Usuário   Senha    Grupo
root      linux    root
tux       linux    users
```

> **Trocar imediatamente antes de usar em rede ou publicar ISO:**

```bash
passwd root
passwd tux
```

Para gerar hash para o `config.xml` antes de um novo build:

```bash
openssl passwd -1 'NovaSenhaAqui'
# Copiar o hash gerado para o campo password= no config.xml
```

---

## Como compilar a ISO

### Requisito: openSUSE Leap 15.6 x86_64

O build foi validado neste ambiente. VMware, VirtualBox, Proxmox ou máquina física funcionam.

### Opção 1: script Python (recomendado)

O script `gerar_iso_multicortex_completo_py36.py` automatiza todas as etapas — instala dependências, clona o repo upstream, aplica patches no `config.xml` e executa o KIWI.

```bash
# Como root:
python3 scripts/gerar_iso_multicortex_completo_py36.py

# Com limpeza total do build anterior:
python3 scripts/gerar_iso_multicortex_completo_py36.py --clean

# Pulando instalação de pacotes (kiwi-ng já instalado):
python3 scripts/gerar_iso_multicortex_completo_py36.py --no-install

# Em diretório customizado:
python3 scripts/gerar_iso_multicortex_completo_py36.py --workdir /mnt/builds
```

A ISO é gerada em `/home/hawk/builds/out/` ou `~/builds/out/`. O log completo fica em `builds/build-multicortex.log`.

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
| `suseConfig() is obsolete` | Função removida no KIWI 10 | Comentar `suseConfig` |
| `suseRemoveYaST() is obsolete` | Função removida no KIWI 10 | Comentar `suseRemoveYaST` |
| `gconftool-2: No such file or directory` | Scripts legados de tema | Já comentados neste fork |
| Avisos `NOKEY` nos RPMs | GPG não importado | São `warning`, não `ERROR` — build prossegue normalmente |
| Conflito de drivers NVIDIA | Versões 550 e 580 misturadas | Manter apenas pacotes G06 da mesma linha; remover `nvidia-video-G06`, `nvidia-gl-G06` se causar conflito |
| Mirror BR falhando | `mirrorcache-br-2.opensuse.org` instável | Usar `download.opensuse.org` diretamente (já configurado no `config.xml` deste fork) |

---

## Como testar a ISO

### VMware

```
Sistema operacional: Linux 64-bit / openSUSE 64-bit
Firmware: UEFI
Secure Boot: OFF
CPU: 4 cores
RAM: 8 GB (mínimo 4 GB)
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
lsblk   # identificar o dispositivo — ex: /dev/sdb

# Cuidado: apaga tudo no dispositivo selecionado
sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
        of=/dev/sdX bs=4M status=progress conv=fsync
```

**Windows:** Rufus — selecionar GPT/UEFI para PCs modernos.

**macOS e outros:** Balena Etcher.

---

## Comandos disponíveis na ISO

```bash
multicortex-status        # diagnóstico completo do sistema
multicortex-menu          # menu interativo de controle
multicortex-models-light  # instala modelos leves via Ollama
multicortex-models-medium # instala modelos médios via Ollama
multicortex-models-code   # instala modelos de código via Ollama
multicortex-models-large  # instala modelos grandes via Ollama
multicortex-models-list   # lista modelos instalados
```

Aliases:

```bash
mc-status   # → multicortex-status
mc-menu     # → multicortex-menu
mc-models   # → multicortex-models-list
```

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
    "messages": [{"role": "user", "content": "Explique o que é o multicortexEXO em 3 linhas."}],
    "stream": false
  }'
```

Manter sempre em `127.0.0.1`. Para acesso remoto: túnel SSH (`ssh -L 11434:localhost:11434 tux@<ip>`), VPN ou proxy autenticado.

---

## Perfis de modelos de IA

Confirmar que o Ollama está ativo antes de instalar:

```bash
systemctl status ollama
curl http://127.0.0.1:11434/api/tags
```

### Leve — VMs, notebooks simples, 8–16 GB RAM

```bash
multicortex-models-light
```

Modelos instalados via `ollama pull`:

| Modelo | Parâmetros | Uso |
|--------|-----------|-----|
| `tinyllama:latest` | 1.1B | Ultra-leve, respostas rápidas mesmo sem GPU |
| `phi3:mini` | 3.8B | Microsoft Phi-3, ótimo custo-benefício |
| `gemma3:1b` | 1B | Google Gemma 3, eficiente |
| `qwen3:0.6b` | 0.6B | Alibaba Qwen, menor modelo disponível |
| `smollm2:1.7b` | 1.7B | HuggingFace SmolLM2, bom raciocínio para o tamanho |

### Médio — 16–32 GB RAM, GPU 8–12 GB VRAM

```bash
multicortex-models-medium
```

| Modelo | Parâmetros | Uso |
|--------|-----------|-----|
| `llama3.1:8b` | 8B | Meta LLaMA 3.1, excelente equilíbrio |
| `llama3.2:3b` | 3B | Meta LLaMA 3.2, rápido e capaz |
| `mistral:7b` | 7B | Mistral AI, forte em raciocínio |
| `qwen3:8b` | 8B | Alibaba Qwen 3, multilíngue |
| `gemma3:4b` | 4B | Google Gemma 3 médio |
| `qwen2.5:7b` | 7B | Qwen 2.5, bom em português |

### Código — programação e análise técnica

```bash
multicortex-models-code
```

| Modelo | Parâmetros | Especialidade |
|--------|-----------|---------------|
| `deepseek-coder:1.3b` | 1.3B | DeepSeek Coder leve |
| `deepseek-coder:6.7b` | 6.7B | DeepSeek Coder completo |
| `qwen2.5-coder:7b` | 7B | Alibaba, forte em múltiplas linguagens |
| `codegemma:7b` | 7B | Google, bom em Python e C++ |
| `starcoder2:7b` | 7B | BigCode, treinado em 600+ linguagens |

### Grande — workstation com SSD NVMe e GPU ≥12 GB VRAM

```bash
multicortex-models-large
```

| Modelo | Parâmetros | Uso |
|--------|-----------|-----|
| `llama3.1:70b` | 70B | Meta LLaMA 3.1 full, qualidade próxima a GPT-4 |
| `llama3.3:70b` | 70B | Meta LLaMA 3.3, mais recente |
| `qwen2.5:32b` | 32B | Alibaba, forte em multilíngue |
| `qwen3:32b` | 32B | Qwen 3 médio-grande |
| `mixtral:8x7b` | 46.7B (MoE) | Mistral Mixture of Experts |
| `deepseek-r1:32b` | 32B | DeepSeek R1, raciocínio avançado |

> Sem GPU dedicada todos os perfis executam via CPU. Modelos acima de 7B serão lentos em CPU — calcule ~30s a vários minutos por resposta dependendo do hardware.

---

## Persistência de dados

A ISO usa overlay ext4. Em pendrive com espaço disponível, dados são preservados entre sessões.

Diretórios críticos para persistir:

```
/var/lib/ollama       modelos baixados (podem ser GBs)
/home/tux             arquivos do usuário tux
/var/log/multicortex  logs
/opt/multicortex      scripts e configurações
```

Sem persistência, modelos baixados durante a sessão são perdidos ao reiniciar. Para uso repetido, gravar em pendrive com espaço suficiente (80 GB+ para modelos médios).

---

## Edição offline com SSD

Para ambientes sem internet (campo, indústria, cliente isolado):

1. Em uma máquina com internet, baixar os modelos desejados:
```bash
ollama pull tinyllama:latest
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull deepseek-coder:6.7b
```

2. Copiar `/var/lib/ollama` para um SSD/NVMe externo

3. No ambiente offline: inicializar a ISO com pendrive + SSD, montar o SSD e usar os modelos diretamente ou copiar para a camada persistente

Gerar manifesto para controle e auditoria:

```bash
ollama list > MODELOS.txt
sha256sum MODELOS.txt > MODELOS.txt.sha256
```

---

## Requisitos de hardware

A ISO é **exclusivamente x86_64**. Não funciona em ARM, Raspberry Pi ou Apple Silicon.

**Mínimo para boot:**
- CPU x86_64 64 bits
- RAM: 4 GB
- Firmware: UEFI recomendado (BIOS legacy suportado)
- **Secure Boot: desligado**

**Por perfil de uso:**

| Uso | CPU | RAM | Armazenamento | GPU |
|-----|-----|-----|---------------|-----|
| VM / testes | qualquer quad-core | 8 GB | — | opcional |
| Modelos leves (≤3B) | i5 / Ryzen 5 | 16 GB | — | opcional |
| Modelos médios (7–8B) | i5 / Ryzen 5 | 16–32 GB | 80 GB+ | 8 GB VRAM recomendado |
| Modelos grandes (32–70B) | i7/i9 / Ryzen 7/9 | 32–64+ GB | SSD NVMe 128 GB+ | ≥12 GB VRAM |

---

## Diagnóstico e troubleshooting

### Status completo

```bash
multicortex-status
systemctl --failed
```

### Serviços

```bash
systemctl status ollama
journalctl -u ollama -f
journalctl -u multicortex-chat-ui -f
```

### GPU não detectada

```bash
lspci | grep -i nvidia
nvidia-smi
lsmod | grep nvidia
```

### Rede sem IP

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
systemctl start ollama      # se estiver parado
ollama pull llama3.2        # se o modelo não estiver instalado
```

### Modelo lento

CPU sem GPU: 30s a vários minutos por resposta em modelos >7B. Verificar com `nvidia-smi` se a GPU está sendo usada. Tentar modelo menor do perfil leve.

### ISO não inicia

Verificar hash SHA256 da ISO, gravação correta no pendrive, UEFI habilitado, Secure Boot desligado. Testar em VM antes de usar em hardware.

---

## Segurança

- Trocar `root/linux` e `tux/linux` antes de usar em rede, habilitar SSH ou publicar ISO
- Manter Ollama em `127.0.0.1:11434` — nunca expor `0.0.0.0` diretamente
- SSH: usar autenticação por chave, desativar login root por senha, configurar firewall
- Não incluir dados de clientes, chaves, tokens ou arquivos sensíveis na ISO publicada

O `.gitignore` já exclui: `*.iso`, `*.key`, `*.pem`, `*.token`, `*.env`, `secrets.yaml`, `models/`, `out/`, `build/`.

---

## Estado atual e pendências conhecidas

### O que funciona

- `config.xml` com todos os pacotes, repositórios e configurações para gerar a ISO
- `config.sh` com configurações de sistema e compatibilidade com KIWI 10
- Overlay `root/` com MOTD, versão, aliases, serviço de firstboot, rede, repositórios, scripts de sistema
- `multicortex-status.sh` e `multicortex-menu.sh` funcionais e completos
- Script Python de build automático com patch automático do `config.xml`
- Documentação em `docs/`
- Temas visuais completos (GRUB2, Plymouth, GDM, GFXBOOT)
- ISO `MultiCortex_EXO_1.0.5` gerada e publicada

### Pendências

**Bug no `config.sh`:** o bloco `MULTICORTEX EXO GENERATED CONFIG` está após o `exit 0` e nunca executa. Corrigir movendo o bloco para antes do `exit 0`.

**Scripts não commitados — referenciados mas ausentes:**

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

**Binários ausentes no overlay:** `multicortex-status`, `multicortex-menu` e `multicortex-models-*` precisam existir em `/usr/local/bin/` dentro da ISO. Os links ou scripts não estão em `root/usr/local/bin/`.

**`/etc/multicortex.asc`** — arquivo de logo ASCII referenciado pelo `initMulticortex.sh` mas não presente no overlay.

**`multicortex-chat-ui.service`** — habilitado no `config.sh` mas sem arquivo `.service` no overlay.

**Framework `exo`** — o script `~/bin/exo` pressupõe virtualenv instalado manualmente.

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
  --repo hawkinf/multicortexEXO_fork \
  --clobber
```

---

## Licença e créditos

Este fork respeita a licença do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo) e as licenças de todos os componentes incluídos: openSUSE, KIWI NG, Ollama, drivers NVIDIA e demais pacotes. Antes de redistribuir a ISO publicamente, revisar as licenças dos pacotes proprietários NVIDIA.

**Projeto original:** Alessandro de Oliveira Faria (CABELO) — `cabelo@opensuse.org`

**Fork e adaptações:** Aguinaldo Liesack Baptistini

> Este projeto está em desenvolvimento ativo. Usar em ambiente de teste antes de aplicar em produção. Revisar scripts antes de executar comandos administrativos. Modelos de IA podem produzir respostas incorretas — a validação de qualquer ação é responsabilidade do usuário.
