# multicortexEXO

Sistema Linux Live/Bootável baseado em **openSUSE Leap 15.6 x86_64**, voltado para execução local de Inteligência Artificial, automação, agentes especializados e orquestração de múltiplos modelos de IA em ambiente controlado.

Este projeto é um **fork/adaptação técnica** do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo), criado para permitir evolução independente, customização, manutenção própria, geração local da ISO e adaptação do conceito MultiCortex para um ambiente prático, auditável e executável em máquinas locais, servidores, notebooks, estações de trabalho e ambientes offline.

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Por que este fork foi criado](#por-que-este-fork-foi-criado)
- [Resumo das atualizações realizadas](#resumo-das-atualizações-realizadas)
- [O que foi gerado](#o-que-foi-gerado)
- [Como o sistema funciona](#como-o-sistema-funciona)
- [Arquitetura geral](#arquitetura-geral)
- [Arquitetura recomendada](#arquitetura-recomendada)
- [Requisitos para rodar a ISO](#requisitos-para-rodar-a-iso)
- [Requisitos para compilar a ISO](#requisitos-para-compilar-a-iso)
- [Como compilar a ISO](#como-compilar-a-iso)
- [Scripts adicionados e funcionamento detalhado](#scripts-adicionados-e-funcionamento-detalhado)
- [Comandos disponíveis dentro da ISO](#comandos-disponíveis-dentro-da-iso)
- [Programas e componentes usados pelos scripts](#programas-e-componentes-usados-pelos-scripts)
- [Serviços da ISO](#serviços-da-iso)
- [API HTTP local](#api-http-local)
- [Como testar a ISO](#como-testar-a-iso)
- [Usuários e senhas padrão da ISO](#usuários-e-senhas-padrão-da-iso)
- [Como gravar a ISO em pendrive](#como-gravar-a-iso-em-pendrive)
- [Persistência de dados](#persistência-de-dados)
- [Modelos de IA suportados](#modelos-de-ia-suportados)
- [Como instalar modelos por perfil](#como-instalar-modelos-por-perfil)
- [Funcionamento do multicortexEXO](#funcionamento-do-multicortexexo)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Configuração KIWI](#configuração-kiwi)
- [Logs e diagnóstico](#logs-e-diagnóstico)
- [Publicação no GitHub Releases](#publicação-no-github-releases)
- [Validações realizadas](#validações-realizadas)
- [Segurança](#segurança)
- [Limitações conhecidas](#limitações-conhecidas)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Licença](#licença)
- [Créditos](#créditos)
- [Aviso](#aviso)

---

## Sobre o projeto

O **multicortexEXO** é uma distribuição Linux Live/Bootável baseada em **openSUSE Leap 15.6**, criada para oferecer um ambiente pronto para uso com ferramentas de IA local, agentes, automações e modelos de linguagem executando diretamente na máquina do usuário.

A proposta é permitir que o usuário tenha uma estação de IA independente, com foco em:

- execução local de modelos LLM;
- uso em modo Live por ISO ou pendrive;
- possibilidade de teste em VM;
- operação offline quando os modelos já estiverem baixados;
- ambiente padronizado para testes, suporte, automação e desenvolvimento;
- separação de agentes por função;
- orquestração de tarefas entre diferentes modelos;
- maior controle sobre privacidade, dados e dependências externas.

Em vez de depender exclusivamente de serviços externos, o projeto busca entregar uma base local, reproduzível e modificável.

---

## Por que este fork foi criado

Este fork foi criado porque o projeto original serviu como inspiração, mas havia necessidade de uma versão com objetivos próprios, mais prática e mais controlada.

Os principais motivos do fork são:

### 1. Evolução independente

O fork permite alterar o sistema sem depender do ritmo, das escolhas técnicas ou das limitações do projeto original.

Isso possibilita:

- ajustar scripts de build;
- trocar pacotes;
- adaptar repositórios;
- adicionar suporte a novos modelos;
- modificar interface e serviços;
- criar instaladores próprios;
- integrar ferramentas específicas;
- manter documentação própria;
- fazer correções sem aguardar upstream.

### 2. Foco em uso real

O multicortexEXO não foi pensado apenas como demonstração. A ideia é ser um sistema utilizável em bancada técnica, laboratório, suporte, desenvolvimento, análise, automação e uso pessoal avançado.

Cenários de uso:

- boot por pendrive;
- diagnóstico de máquinas;
- execução local de IA;
- estação temporária de trabalho;
- testes de modelos LLM;
- execução offline;
- demonstrações controladas;
- laboratório de automação e agentes.

### 3. IA local e soberania de dados

O fork busca permitir que o usuário execute IA localmente, sem enviar arquivos, prompts ou dados sensíveis para serviços externos.

Isso é importante em casos como:

- documentos privados;
- dados empresariais;
- código-fonte;
- laudos técnicos;
- logs de clientes;
- informações financeiras;
- projetos internos;
- dados que não devem sair da máquina.

### 4. Controle técnico

Ao gerar a própria ISO, é possível saber exatamente:

- quais pacotes foram instalados;
- quais serviços iniciam no boot;
- quais modelos estão disponíveis;
- quais portas estão abertas;
- quais permissões existem;
- quais scripts são executados;
- como o ambiente é configurado.

Como diz o velho método: primeiro entenda a máquina, depois deixe a máquina trabalhar.

---


## Resumo das atualizações realizadas

Esta fase do fork transformou a ISO em um projeto mais organizado, auditável e operacional. Antes, o repositório estava focado principalmente na descrição KIWI e na geração da imagem. Agora ele possui scripts próprios para build, diagnóstico, operação dentro da ISO, documentação complementar e preparação para instalação de modelos por perfil.

### Atualizações de repositório

Foram adicionados ou atualizados:

- `VERSION`, com a versão/build do projeto;
- `.gitignore` reforçado para evitar commit de ISO, imagens, logs, chaves e modelos;
- documentação complementar em `docs/`;
- scripts de build em `scripts/build/`;
- scripts de sistema em `scripts/system/`;
- scripts de modelos em `scripts/models/`;
- overlay KIWI em `suse/x86_64/suse-leap-15.6-JeOS/root/`;
- comandos `multicortex-*` dentro da ISO via `/usr/local/bin`;
- arquivo `/etc/multicortex-version` dentro da imagem;
- mensagem `/etc/motd` com instruções rápidas;
- aliases em `/etc/profile.d/multicortex.sh`;
- serviço `multicortex-firstboot.service`;
- bloco no `config.sh` para preparar diretórios, permissões e serviços.

### Atualizações dentro da ISO

A ISO passou a incluir estrutura para os comandos:

```text
multicortex-menu
multicortex-status
multicortex-models-light
multicortex-models-medium
multicortex-models-code
multicortex-models-large
multicortex-models-list
```

Esses comandos foram pensados para reduzir a necessidade de decorar caminhos longos. Em vez de procurar scripts manualmente, o usuário chama o comando direto no terminal. Coisa simples, do jeito que Unix sempre gostou: comando curto, função clara.

### Atualizações de documentação

Foram previstos os seguintes documentos:

```text
docs/BUILD.md
docs/API.md
docs/MODELOS.md
docs/FULL_OFFLINE.md
docs/SEGURANCA.md
docs/build-environment-report.md
```

Cada arquivo tem uma função:

- `BUILD.md`: explica como preparar o ambiente e gerar a ISO;
- `API.md`: documenta o uso da API HTTP local do Ollama;
- `MODELOS.md`: separa modelos por perfil de hardware e uso;
- `FULL_OFFLINE.md`: explica a edição offline com SSD/NVMe;
- `SEGURANCA.md`: reúne cuidados com senhas, SSH, API e dados sensíveis;
- `build-environment-report.md`: registra informações do ambiente de build.

### Commits desta fase

```text
9dc0987 Improve MultiCortex EXO tooling, docs and model profiles
a5f35b8 Document MultiCortex EXO live ISO operation in README
```

### ISO validada nesta fase

```text
MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

SHA256:

```text
03c9de435287e76e602b8b7d6860e0cd46a6e307d54590c24d85735341fb483d
```

---

## O que foi gerado

ISO gerada com sucesso:

```text
MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

Caminho local usado no ambiente de build:

```text
/home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

Arquitetura:

```text
x86_64 / amd64 / x64 / 64 bits
```

Base:

```text
openSUSE Leap 15.6
```

Tipo:

```text
Live ISO bootável
```

Tamanho aproximado:

```text
1,8 GB
```

Build realizado com:

```text
openSUSE Leap 15.6 Server
KIWI NG 10.2.33
Python 3.6.15
VMware
```

---

## Como o sistema funciona

O fluxo básico do sistema é:

1. O computador inicia pela ISO.
2. O bootloader carrega o kernel Linux e o initramfs.
3. O sistema Live baseado em openSUSE é montado.
4. O ambiente base é carregado.
5. Serviços essenciais são iniciados.
6. O ambiente gráfico/terminal é disponibilizado.
7. O Ollama e serviços do MultiCortex podem ser iniciados.
8. O usuário acessa modelos locais, terminal, ferramentas e automações.
9. O sistema executa tarefas de IA local ou integrações configuradas.

Fluxo conceitual:

```text
Usuário
  ↓
Interface / Terminal / Painel local
  ↓
Serviços multicortexEXO
  ↓
Ollama / backends locais / scripts
  ↓
Modelos e ferramentas
  ↓
Resultado, arquivo, comando, análise ou automação
```

---

## Arquitetura geral

```text
multicortexEXO
├── Sistema Live openSUSE
│   ├── Kernel
│   ├── Initramfs
│   ├── SquashFS
│   ├── Pacotes base
│   └── Camada de persistência opcional
│
├── Camada de IA
│   ├── Ollama
│   ├── Modelos locais
│   ├── APIs opcionais
│   └── Scripts auxiliares
│
├── Serviços
│   ├── sshd
│   ├── ollama
│   └── multicortex-chat-ui
│
├── Ferramentas
│   ├── Python
│   ├── Git
│   ├── Shell
│   ├── Utilitários Linux
│   └── Diagnóstico
│
└── Interface
    ├── Terminal
    ├── Ambiente gráfico GNOME
    ├── Painel local
    └── Scripts de automação
```

---


## Arquitetura recomendada

Não é recomendado embutir todos os modelos grandes diretamente na ISO base. Isso deixaria a imagem muito grande, mais lenta para gerar, mais difícil de testar e ruim para distribuir.

A arquitetura recomendada fica dividida em três camadas.

### 1. ISO Base

A ISO Base contém:

- openSUSE Leap 15.6;
- descrição KIWI;
- scripts de build;
- scripts de diagnóstico;
- Ollama, se disponível nos pacotes/configuração;
- Web UI ou preparação para Web UI;
- API local;
- documentação;
- comandos `multicortex-*`;
- estrutura para instalar modelos posteriormente.

Essa é a versão ideal para publicar no GitHub Releases.

### 2. Model Pack

O Model Pack é o conjunto de scripts que baixa modelos por perfil.

Exemplos:

```bash
multicortex-models-light
multicortex-models-medium
multicortex-models-code
multicortex-models-large
```

Assim, cada máquina instala apenas o que consegue rodar. Um notebook simples pode usar modelos leves; uma workstation com GPU pode usar modelos médios ou grandes.

### 3. Full Offline SSD Edition

A Full Offline SSD Edition é a versão pensada para ambiente sem internet.

Nela, os modelos já ficam baixados em SSD/NVMe, normalmente em:

```text
/var/lib/ollama
```

Essa edição é recomendada para bancada técnica, campo, laboratório, cliente, demonstração controlada ou ambiente isolado.

---

## Requisitos para rodar a ISO

### Mínimo para dar boot

```text
CPU: Intel/AMD 64 bits
Arquitetura: x86_64 / amd64 / x64
RAM: 4 GB
Boot: UEFI recomendado
Secure Boot: desligado
Rede: recomendada
GPU: não obrigatória
```

### Recomendado para uso normal

```text
CPU: Intel Core i5/i7 ou AMD Ryzen 5/7
Núcleos: 4 ou mais
RAM: 8 GB ou mais
Armazenamento: 40 GB ou mais se for instalar/testar persistência
GPU: Intel, AMD ou NVIDIA
Boot: UEFI
Secure Boot: OFF
Internet: recomendada na primeira configuração
```

### Recomendado para IA local/Ollama

```text
CPU: 6 a 8 núcleos
RAM: 16 GB ou mais
Disco: 80 GB ou mais
GPU NVIDIA: opcional, mas recomendada
VRAM: 8 GB ou mais para modelos médios
```

### Ideal para modelos maiores

```text
CPU: Intel Core i7/i9 ou AMD Ryzen 7/9
RAM: 32 GB a 64 GB
Armazenamento: SSD NVMe ou SSD externo de 128 GB ou mais
GPU: NVIDIA com 12 GB ou mais de VRAM
Boot: UEFI
```

Sem GPU dedicada, o sistema pode funcionar via CPU, porém modelos maiores serão lentos.

---

## Requisitos para compilar a ISO

### Sistema recomendado para build

```text
openSUSE Leap 15.6 x86_64
```

### Hardware recomendado para build

```text
CPU: 4 núcleos ou mais
RAM: 8 GB ou mais
Disco livre: 100 GB ou mais
Internet: obrigatória para baixar pacotes
VM: VMware, VirtualBox, Proxmox ou máquina física
```

### Pacotes necessários

Como root:

```bash
zypper refresh
zypper install -y git curl wget nano xz tar gzip cpio rsync which ca-certificates ca-certificates-mozilla openssl
```

Verificar o KIWI:

```bash
kiwi-ng --version
```

Se o KIWI não estiver instalado:

```bash
zypper ar -f https://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/ kiwi-builder
zypper --gpg-auto-import-keys refresh
zypper install -y python311-kiwi
```

Se o sistema já tiver `python311-kiwi`, não aceite downgrade para `python3-kiwi`.

---

## Como compilar a ISO

### 1. Clonar o projeto original

```bash
cd /home/hawk
mkdir -p builds
cd builds

git clone https://github.com/cabelo/multicortex-exo.git
```

### 2. Copiar a descrição KIWI

```bash
cd /home/hawk/builds

rm -rf kiwi-desc out
mkdir -p kiwi-desc out

cp -a multicortex-exo/suse/x86_64/suse-leap-15.6-JeOS/. kiwi-desc/
```

### 3. Ajustar `config.xml`

O projeto usa repositórios openSUSE Leap 15.6 e repositórios OBS. Para build local, a versão funcional utilizou:

```text
http://download.opensuse.org/distribution/leap/15.6/repo/oss/
http://download.opensuse.org/update/leap/15.6/oss/
http://download.opensuse.org/distribution/leap/15.6/repo/non-oss/
http://download.opensuse.org/update/leap/15.6/non-oss/
https://download.nvidia.com/opensuse/leap/15.6/
```

Evite o mirror brasileiro `mirrorcache-br-2.opensuse.org` se ele falhar durante o download.

### 4. Ajustar pacotes NVIDIA

O build funcional manteve suporte NVIDIA, evitando mistura de versões 550 e 580.

Pacotes usados/garantidos:

```text
nvidia-common-G06
nvidia-compute-G06
nvidia-compute-utils-G06
nvidia-utils-G06
nvidia-driver-G06-kmp-default
```

Caso o solver do `zypper` reclame de conflitos, remova pacotes extras que puxem uma linha diferente, como:

```text
nvidia-video-G06
nvidia-gl-G06
kernel-firmware-nvidia-gspx-G06
```

### 5. Ajustar `config.sh` para KIWI 10.x

O `config.sh` original usa funções antigas do SUSE Studio/KIWI. No KIWI 10.x, algumas são obsoletas ou inexistentes.

Foram removidas ou comentadas:

```text
baseMount
baseCleanMount
suseConfig
suseRemoveYaST
```

Comandos sensíveis foram protegidos com `|| true` ou checagens de existência:

```bash
[ -f /image/.profile ] && cp /image/.profile /studio/profile || true
[ -f /image/config.xml ] && cp /image/config.xml /studio/config.xml || true
[ -f /etc/vimrc ] && sed -i -e's/^syntax on/" syntax on/' /etc/vimrc || true
```

Também foram desativados scripts legados de tema que dependiam de `gconftool-2`/`dconf` no chroot:

```bash
# sh /studio/configure_gdm_theme.sh removido
# sh /studio/configure_gnome_background.sh removido
```

### 6. Rodar o build

```bash
cd /home/hawk/builds

rm -rf /home/hawk/builds/out
mkdir -p /home/hawk/builds/out

kiwi-ng --debug system build   --description /home/hawk/builds/kiwi-desc   --target-dir /home/hawk/builds/out   2>&1 | tee /home/hawk/builds/build-multicortex.log
```

### 7. Verificar a ISO

```bash
find /home/hawk/builds/out -maxdepth 3 -type f -name "*.iso" -ls
```

Resultado esperado:

```text
/home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

---


## Scripts adicionados e funcionamento detalhado

Esta seção explica cada script adicionado ou previsto nesta fase do fork.

### Visão geral

```text
scripts/
├── build/
│   ├── check-build-env.sh
│   ├── install-build-deps-opensuse.sh
│   ├── clean-build.sh
│   ├── build-iso.sh
│   └── check-result.sh
│
├── system/
│   ├── multicortex-status.sh
│   └── multicortex-menu.sh
│
└── models/
    ├── _ollama_common.sh
    ├── install-light-models.sh
    ├── install-medium-models.sh
    ├── install-code-models.sh
    ├── install-large-models.sh
    └── list-installed-models.sh
```

> Observação: se algum script de `models/` ainda não existir no repositório local, ele deve ser adicionado antes de gerar uma ISO final com os comandos `multicortex-models-*`. Os links dentro da ISO apontam para `/opt/multicortex/scripts/models/`.

---

### `scripts/build/check-build-env.sh`

#### Finalidade

Verifica se o servidor de build está pronto para gerar a ISO com KIWI NG.

#### Como executar

```bash
bash scripts/build/check-build-env.sh
```

#### O que ele verifica

- diretório atual do projeto;
- valor de `DESC_DIR`;
- presença do `config.xml`;
- presença do `config.sh`;
- existência dos comandos essenciais;
- versão do KIWI NG;
- sistema operacional;
- validade do XML;
- sintaxe dos scripts Bash.

#### Programas usados

- `git`: controle de versão;
- `bash`: interpretador dos scripts;
- `curl`: testes HTTP;
- `kiwi-ng`: geração da ISO;
- `zypper`: pacotes openSUSE;
- `xmllint`: validação XML;
- `shellcheck`: análise estática de Bash;
- `sudo`: execução com privilégio;
- `sha256sum`: cálculo de hash;
- `tee`: gravação de logs;
- `find`: localização de arquivos;
- `awk`, `sed`, `grep`: processamento de texto.

#### Saída esperada

```text
KIWI (next generation) version 10.2.33
OK: suse/x86_64/suse-leap-15.6-JeOS/config.xml
OK: suse/x86_64/suse-leap-15.6-JeOS/config.sh
Sintaxe dos scripts:
OK
```

---

### `scripts/build/install-build-deps-opensuse.sh`

#### Finalidade

Instala ou verifica dependências necessárias no openSUSE.

#### Como executar

```bash
bash scripts/build/install-build-deps-opensuse.sh
```

#### O que ele faz

- carrega `/etc/os-release`;
- confirma se o sistema é openSUSE/SUSE;
- executa `zypper refresh`;
- instala dependências básicas;
- verifica se `kiwi-ng` existe;
- tenta instalar KIWI se necessário;
- verifica `shellcheck`;
- tenta instalar `ShellCheck`, quando disponível.

#### Observação sobre KIWI

Em alguns ambientes, o pacote instalado não aparece como `python3-kiwi`, mas o comando existe:

```bash
kiwi-ng --version
command -v kiwi-ng
```

Se esses comandos funcionarem, o KIWI está disponível para o build.

---

### `scripts/build/clean-build.sh`

#### Finalidade

Remove a saída anterior do build e recria os diretórios limpos.

#### Como executar

```bash
bash scripts/build/clean-build.sh
```

#### Variáveis usadas

```bash
TARGET_DIR="${TARGET_DIR:-$HOME/builds/out}"
LOG_DIR="${LOG_DIR:-$HOME/builds/logs}"
```

#### Exemplo com caminhos fixos

```bash
TARGET_DIR=/home/hawk/builds/out \
LOG_DIR=/home/hawk/builds/logs \
bash scripts/build/clean-build.sh
```

---

### `scripts/build/build-iso.sh`

#### Finalidade

Executa o build da ISO usando KIWI NG.

#### Como executar

```bash
bash scripts/build/build-iso.sh
```

#### O que ele faz

- define o diretório KIWI;
- cria diretórios de saída;
- cria diretório de logs;
- monta um nome de log com data e hora;
- detecta se precisa usar `sudo`;
- executa `kiwi-ng --debug system build`;
- salva toda a saída do build com `tee`.

#### Variáveis usadas

```bash
DESC_DIR="${DESC_DIR:-suse/x86_64/suse-leap-15.6-JeOS}"
TARGET_DIR="${TARGET_DIR:-$HOME/builds/out}"
LOG_DIR="${LOG_DIR:-$HOME/builds/logs}"
```

#### Comando principal

```bash
kiwi-ng --debug system build \
  --description "$(pwd)/$DESC_DIR" \
  --target-dir "$TARGET_DIR"
```

---

### `scripts/build/check-result.sh`

#### Finalidade

Localiza artefatos gerados e calcula SHA256 das ISOs.

#### Como executar

```bash
bash scripts/build/check-result.sh
```

#### O que ele faz

- procura arquivos `.iso`, `.img`, `.raw` e `.qcow2`;
- lista os arquivos encontrados;
- calcula o SHA256;
- gera `SHA256SUMS`.

#### Exemplo de resultado

```text
SHA256:
03c9de435287e76e602b8b7d6860e0cd46a6e307d54590c24d85735341fb483d  MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

---

### `scripts/system/multicortex-status.sh`

#### Finalidade

Mostra um diagnóstico geral do sistema dentro da ISO.

#### Como executar dentro da ISO

```bash
multicortex-status
```

Ou diretamente:

```bash
/opt/multicortex/scripts/system/multicortex-status.sh
```

#### O que ele mostra

- versão do MultiCortex;
- hostname;
- kernel;
- arquitetura;
- versão do openSUSE;
- IPs locais;
- URLs prováveis da API e Web UI;
- status dos serviços;
- resposta da API do Ollama;
- modelos instalados;
- CPU;
- RAM;
- disco;
- GPU NVIDIA, se houver;
- logs recentes do Ollama.

#### Programas usados

- `hostname`: nome da máquina;
- `uname`: kernel e arquitetura;
- `ip`: endereços de rede;
- `systemctl`: status dos serviços;
- `curl`: teste da API Ollama;
- `jq`: formatação opcional do JSON;
- `ollama`: listagem de modelos;
- `lscpu`: informações de CPU;
- `free`: uso de memória;
- `df`: uso de disco;
- `nvidia-smi`: GPU NVIDIA;
- `journalctl`: logs dos serviços.

---

### `scripts/system/multicortex-menu.sh`

#### Finalidade

Fornece um menu interativo para operação básica do sistema.

#### Como executar dentro da ISO

```bash
multicortex-menu
```

Ou diretamente:

```bash
/opt/multicortex/scripts/system/multicortex-menu.sh
```

#### Opções do menu

```text
1. Ver status
2. Iniciar Ollama
3. Parar Ollama
4. Reiniciar Ollama
5. Iniciar Web UI
6. Parar Web UI
7. Reiniciar Web UI
8. Listar modelos
9. Instalar modelos leves
10. Instalar modelos médios
11. Instalar modelos de código
12. Instalar modelos grandes
13. Testar API
14. Mostrar IPs e URLs
15. Sair
```

#### O que ele controla

- `ollama.service`;
- `multicortex-chat-ui.service`;
- `open-webui.service`;
- scripts `multicortex-models-*`;
- teste HTTP da API do Ollama.

---

### `scripts/models/_ollama_common.sh`

#### Finalidade

Arquivo auxiliar usado pelos scripts de instalação/listagem de modelos.

Normalmente ele não é executado diretamente. Ele é carregado pelos outros scripts com `source`.

#### Funções principais

```text
log()
warn()
fail()
have()
start_ollama_if_needed()
pull_model()
pull_profile()
list_models()
```

#### Variável principal

```bash
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
```

#### Como ele inicia o Ollama

1. testa `http://127.0.0.1:11434/api/tags`;
2. tenta `systemctl start ollama.service`;
3. se necessário, tenta `nohup ollama serve`.

---

### `scripts/models/install-light-models.sh`

#### Finalidade

Instala modelos leves.

#### Como executar

```bash
multicortex-models-light
```

#### Modelos previstos

```text
tinyllama:latest
phi3:mini
gemma3:1b
qwen3:0.6b
smollm2:1.7b
```

#### Perfil recomendado

```text
RAM: 8 GB a 16 GB
GPU: opcional
Uso: VM, notebook simples, testes rápidos
```

---

### `scripts/models/install-medium-models.sh`

#### Finalidade

Instala modelos médios.

#### Como executar

```bash
multicortex-models-medium
```

#### Modelos previstos

```text
llama3.1:8b
llama3.2:3b
mistral:7b
qwen3:8b
gemma3:4b
qwen2.5:7b
```

#### Perfil recomendado

```text
RAM: 16 GB a 32 GB
GPU: 8 GB a 12 GB de VRAM recomendada
Uso: chat local, análise de texto, suporte e automação
```

---

### `scripts/models/install-code-models.sh`

#### Finalidade

Instala modelos especializados em programação.

#### Como executar

```bash
multicortex-models-code
```

#### Modelos previstos

```text
deepseek-coder:1.3b
deepseek-coder:6.7b
qwen2.5-coder:7b
codegemma:7b
starcoder2:7b
```

---

### `scripts/models/install-large-models.sh`

#### Finalidade

Instala modelos grandes.

#### Como executar

```bash
multicortex-models-large
```

#### Modelos previstos

```text
llama3.1:70b
llama3.3:70b
qwen2.5:32b
qwen3:32b
mixtral:8x7b
deepseek-r1:32b
```

#### Atenção

Este perfil exige muito disco, RAM, tempo de download e, preferencialmente, GPU forte.

---

### `scripts/models/list-installed-models.sh`

#### Finalidade

Lista os modelos instalados no Ollama.

#### Como executar

```bash
multicortex-models-list
```

#### O que ele usa

- `ollama list`;
- `curl http://127.0.0.1:11434/api/tags`.

---

## Comandos disponíveis dentro da ISO

Os comandos são expostos em:

```text
/usr/local/bin/
```

### Comandos principais

```bash
multicortex-menu
multicortex-status
multicortex-models-light
multicortex-models-medium
multicortex-models-code
multicortex-models-large
multicortex-models-list
```

### Atalhos de shell

O arquivo `/etc/profile.d/multicortex.sh` cria aliases:

```bash
mc-status
mc-menu
mc-models
```

Equivalências:

```text
mc-status -> multicortex-status
mc-menu   -> multicortex-menu
mc-models -> multicortex-models-list
```

---

## Programas e componentes usados pelos scripts

### `bash`

Interpretador dos scripts `.sh`.

### `kiwi-ng`

Ferramenta que gera a ISO Live a partir da descrição KIWI.

### `zypper`

Gerenciador de pacotes do openSUSE.

### `xmllint`

Valida o `config.xml`.

### `shellcheck`

Analisa scripts Bash e aponta problemas comuns.

### `git`

Controle de versão do projeto.

### `curl`

Testa endpoints HTTP, especialmente a API do Ollama.

### `jq`

Formata respostas JSON.

### `systemctl`

Inicia, para, reinicia e consulta serviços systemd.

### `journalctl`

Consulta logs de serviços.

### `ollama`

Gerencia e executa modelos locais.

Exemplos:

```bash
ollama list
ollama pull llama3.1:8b
ollama run llama3.1:8b
```

### `nvidia-smi`

Mostra informações de GPU NVIDIA, quando disponível.

### `ip`

Mostra endereços de rede.

### `free`

Mostra uso de RAM.

### `df`

Mostra uso de disco.

---

## Serviços da ISO

### `ollama.service`

Serviço da API e execução local de modelos.

```bash
systemctl status ollama
systemctl start ollama
systemctl restart ollama
systemctl stop ollama
```

### `multicortex-chat-ui.service`

Serviço previsto para a interface Web local do MultiCortex.

```bash
systemctl status multicortex-chat-ui
systemctl start multicortex-chat-ui
systemctl restart multicortex-chat-ui
systemctl stop multicortex-chat-ui
```

URL provável:

```text
http://127.0.0.1:3000
```

### `open-webui.service`

Serviço previsto para Open WebUI, caso esteja instalado/configurado.

```bash
systemctl status open-webui
systemctl start open-webui
systemctl restart open-webui
systemctl stop open-webui
```

URL provável:

```text
http://127.0.0.1:8080
```

### `multicortex-firstboot.service`

Serviço adicionado para preparar diretórios no boot.

Ele cria ou ajusta:

```text
/var/lib/ollama
/var/log/multicortex
```

Verificar:

```bash
systemctl status multicortex-firstboot
```

---

## API HTTP local

O endpoint principal do Ollama é:

```text
http://127.0.0.1:11434
```

### Listar modelos

```bash
curl http://127.0.0.1:11434/api/tags
```

### Gerar texto

```bash
curl http://127.0.0.1:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Explique o que é o MultiCortex EXO em português.",
    "stream": false
  }'
```

### Chat

```bash
curl http://127.0.0.1:11434/api/chat \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "user", "content": "Resuma o sistema em 5 linhas."}
    ],
    "stream": false
  }'
```

### Segurança da API

Mantenha a API em `127.0.0.1`. Para acesso remoto, use VPN, túnel SSH, proxy autenticado ou firewall.

---

## Como testar a ISO

### VMware

Crie uma nova VM:

```text
Sistema: Linux 64-bit / openSUSE 64-bit
Firmware: UEFI
Secure Boot: OFF
CPU: 2 a 4 cores
RAM: 4 GB mínimo, 8 GB recomendado
Disco: 40 GB
Rede: NAT
ISO: MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

Inicie o boot pela ISO.

### QEMU/KVM

```bash
qemu-system-x86_64   -m 8192   -smp 4   -cdrom MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso   -boot d   -enable-kvm
```

---

## Usuários e senhas padrão da ISO

A imagem Live gerada a partir do `config.xml` inclui usuários locais pré-configurados para acesso inicial ao sistema.

### Credenciais padrão

```text
Usuário: root
Senha:   linux

Usuário: tux
Senha:   linux
```

Essas senhas aparecem no `config.xml` em formato de hash Unix `md5-crypt`, por exemplo:

```xml
<user password="$1$wYJUgpM5$RXMMeASDc035eX.NbYWFl0" home="/root" name="root" groups="root"/>
<user password="$1$Ox48k8VQ$PMrwjyY9Yak/sXnWDiq2q1" home="/home/tux" name="tux" groups="users" shell="/bin/bash"/>
```

O hash não deve ser entendido como senha criptografada reversível. Ele serve apenas para validação da senha durante o login. Neste caso, ambos os hashes correspondem à senha padrão `linux`.

### Uso durante testes

Em ambiente Live, VM ou bancada de testes, use:

```text
Login: root
Senha: linux
```

ou:

```text
Login: tux
Senha: linux
```

O usuário `root` deve ser usado apenas para administração do sistema. Para uso comum, testes de interface e execução de ferramentas sem privilégios administrativos, prefira o usuário `tux`.

### Alterar a senha após o boot

Depois de iniciar a ISO, troque as senhas padrão se o sistema for usado em rede, com SSH habilitado ou com persistência:

```bash
passwd root
passwd tux
```

### Alterar a senha antes de gerar a ISO

Para trocar a senha já no build da ISO, gere um novo hash `md5-crypt` e substitua o campo `password` no `config.xml`:

```bash
openssl passwd -1
```

Exemplo de uso:

```bash
openssl passwd -1 'NovaSenhaForteAqui'
```

Depois substitua o hash antigo no arquivo:

```xml
<user password="NOVO_HASH_AQUI" home="/root" name="root" groups="root"/>
```

> Atenção: a senha `linux` é uma senha padrão clássica usada em imagens de teste/openSUSE/KIWI. Ela é adequada para laboratório, mas não deve ser mantida em ambiente exposto, com SSH ativo ou em uma ISO pública de produção.

---

## Como gravar a ISO em pendrive

### Rufus no Windows

1. Abra o Rufus.
2. Selecione o pendrive.
3. Selecione a ISO `MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso`.
4. Escolha GPT/UEFI para computadores modernos.
5. Clique em iniciar.
6. Aguarde a gravação.
7. Reinicie o computador pelo pendrive.

### Balena Etcher

1. Abra o Balena Etcher.
2. Selecione a ISO.
3. Selecione o pendrive.
4. Clique em Flash.
5. Aguarde a conclusão.

### Linux com `dd`

Atenção: o comando abaixo apaga completamente o disco selecionado.

```bash
lsblk
```

```bash
sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

Substitua `/dev/sdX` pelo dispositivo correto.

---

## Persistência de dados

A ISO foi gerada como Live ISO. Dependendo da configuração do KIWI e do modo de boot, pode haver suporte a persistência híbrida.

Itens recomendados para persistência:

```text
/home
/var/lib/ollama
/opt/multicortexEXO
/var/log
```

Sem persistência, alterações feitas durante a sessão Live podem ser perdidas ao reiniciar.

---

## Modelos de IA suportados

A disponibilidade depende do backend usado, da RAM, da GPU e dos modelos instalados.

### Modelos leves

```text
TinyLlama
Phi
Gemma pequeno
Qwen pequeno
Llama quantizado pequeno
Mistral quantizado
```

### Modelos médios

```text
Llama 3.x 8B quantizado
Mistral 7B quantizado
Qwen 7B quantizado
Gemma 7B quantizado
DeepSeek Coder pequeno/médio
```

### Modelos maiores

```text
Llama 70B quantizado
Qwen 32B
Mixtral
DeepSeek maior
Modelos especializados em código
```

---


## Como instalar modelos por perfil

Os modelos são instalados via Ollama. Antes de instalar, confirme se o Ollama está ativo:

```bash
systemctl status ollama
curl http://127.0.0.1:11434/api/tags
```

### Perfil leve

```bash
multicortex-models-light
```

Uso recomendado:

```text
VMs, notebooks simples, testes rápidos, 8 GB a 16 GB de RAM.
```

### Perfil médio

```bash
multicortex-models-medium
```

Uso recomendado:

```text
PCs com 16 GB a 32 GB de RAM, GPU opcional, uso diário local.
```

### Perfil código

```bash
multicortex-models-code
```

Uso recomendado:

```text
Programação, scripts, análise técnica, automação e suporte.
```

### Perfil grande

```bash
multicortex-models-large
```

Uso recomendado:

```text
Workstations, servidores, SSD/NVMe, muita RAM e GPU forte.
```

### Listar modelos

```bash
multicortex-models-list
```

---

## Funcionamento do multicortexEXO

O multicortexEXO é a camada lógica do sistema. Ele organiza a execução da IA em múltiplos núcleos funcionais.

### Cortex Shell

Responsável por terminal e sistema.

Exemplos:

- gerar comandos Linux;
- explicar logs;
- criar scripts Bash;
- diagnosticar rede;
- automatizar tarefas.

### Cortex Code

Responsável por programação.

Exemplos:

- criar código;
- revisar código;
- explicar erros;
- gerar testes;
- refatorar projetos;
- criar documentação técnica.

### Cortex Docs

Responsável por documentos.

Exemplos:

- ler arquivos;
- resumir PDFs;
- criar relatórios;
- gerar README;
- criar manuais;
- organizar documentação.

### Cortex Security

Responsável por análise defensiva e segurança.

Exemplos:

- analisar logs;
- verificar configurações;
- sugerir hardening;
- identificar riscos;
- avaliar permissões;
- criar checklist defensivo.

### Cortex Support

Responsável por suporte técnico.

Exemplos:

- diagnóstico de Windows;
- diagnóstico de Linux;
- recuperação de ambiente;
- checklist de atendimento;
- geração de laudo técnico;
- organização de procedimentos.

### Cortex Automation

Responsável por automações.

Exemplos:

- scripts Python;
- rotinas agendadas;
- processamento de arquivos;
- integração com APIs;
- execução de pipelines.

---

## Estrutura do repositório

Estrutura atual/recomendada do fork:

```text
multicortexEXO_fork/
├── README.md
├── VERSION
├── .gitignore
├── docs/
│   ├── API.md
│   ├── BUILD.md
│   ├── FULL_OFFLINE.md
│   ├── MODELOS.md
│   ├── SEGURANCA.md
│   └── build-environment-report.md
│
├── scripts/
│   ├── build/
│   │   ├── check-build-env.sh
│   │   ├── install-build-deps-opensuse.sh
│   │   ├── clean-build.sh
│   │   ├── build-iso.sh
│   │   └── check-result.sh
│   │
│   ├── system/
│   │   ├── multicortex-status.sh
│   │   └── multicortex-menu.sh
│   │
│   └── models/
│       ├── _ollama_common.sh
│       ├── install-light-models.sh
│       ├── install-medium-models.sh
│       ├── install-code-models.sh
│       ├── install-large-models.sh
│       └── list-installed-models.sh
│
└── suse/
    └── x86_64/
        └── suse-leap-15.6-JeOS/
            ├── config.xml
            ├── config.sh
            └── root/
                ├── etc/
                │   ├── motd
                │   ├── multicortex-version
                │   ├── profile.d/multicortex.sh
                │   └── systemd/system/multicortex-firstboot.service
                ├── opt/multicortex/scripts/
                └── usr/local/bin/multicortex-*
```

---

## Configuração KIWI

Arquivo principal do build:

```text
suse/x86_64/suse-leap-15.6-JeOS/config.xml
```

Script de configuração da imagem:

```text
suse/x86_64/suse-leap-15.6-JeOS/config.sh
```

Serviços ativados no `config.sh`:

```text
sshd
ollama
multicortex-chat-ui
```

---


### Overlay `root/`

O diretório abaixo é usado pelo KIWI para inserir arquivos dentro da ISO:

```text
suse/x86_64/suse-leap-15.6-JeOS/root/
```

Exemplos de arquivos inseridos:

```text
/etc/motd
/etc/multicortex-version
/etc/profile.d/multicortex.sh
/etc/systemd/system/multicortex-firstboot.service
/opt/multicortex/scripts/system/multicortex-status.sh
/opt/multicortex/scripts/system/multicortex-menu.sh
/usr/local/bin/multicortex-status
/usr/local/bin/multicortex-menu
```

### Bloco adicionado ao `config.sh`

O `config.sh` passou a preparar o ambiente MultiCortex durante o build:

- cria `/var/lib/ollama`;
- cria `/var/log/multicortex`;
- ajusta permissões dos scripts;
- habilita `multicortex-firstboot.service`;
- tenta habilitar `ollama.service`;
- tenta habilitar `multicortex-chat-ui.service`;
- tenta habilitar `open-webui.service`;
- ajusta permissão do `/etc/motd`.

### Arquivo de versão

Na raiz do repositório:

```text
VERSION
```

Dentro da ISO:

```text
/etc/multicortex-version
```

### Mensagem de login

Dentro da ISO:

```text
/etc/motd
```

Essa mensagem mostra comandos úteis e lembra as credenciais padrão.

### Aliases

Dentro da ISO:

```text
/etc/profile.d/multicortex.sh
```

Aliases previstos:

```bash
alias mc-status='multicortex-status'
alias mc-menu='multicortex-menu'
alias mc-models='multicortex-models-list'
```

---

## Serviços

Verificar status:

```bash
systemctl status sshd
systemctl status ollama
systemctl status multicortex-chat-ui
```

Iniciar manualmente:

```bash
sudo systemctl start ollama
sudo systemctl start multicortex-chat-ui
```

Parar:

```bash
sudo systemctl stop ollama
sudo systemctl stop multicortex-chat-ui
```

---

## Logs e diagnóstico

Comandos úteis:

```bash
journalctl -u ollama -f
journalctl -u multicortex-chat-ui -f
dmesg
lsblk
free -h
df -h
ip a
systemctl --failed
```

Verificar GPU NVIDIA:

```bash
nvidia-smi
```

Verificar modelos do Ollama:

```bash
ollama list
```

Testar um modelo:

```bash
ollama run llama3
```

---


## Publicação no GitHub Releases

A ISO não deve ser enviada em commit Git. Ela deve ser publicada como asset em uma release.

### Conferir ISO e SHA

```bash
ISO="/root/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso"
SHA="/root/builds/out/SHA256SUMS"

ls -lh "$ISO"
cat "$SHA"
sha256sum "$ISO"
```

### Verificar GitHub CLI

```bash
command -v gh || zypper install -y gh
gh --version
```

### Login

```bash
gh auth login
gh auth status
```

### Criar release

```bash
TAG="v1.0.5-exo-20260609"

gh release create "$TAG" \
  "$ISO" \
  "$SHA" \
  --repo hawkinf/multicortexEXO_fork \
  --title "MultiCortex EXO 1.0.5 Live ISO" \
  --notes "ISO Linux Live baseada em openSUSE Leap 15.6 x86_64, gerada com KIWI NG, com scripts MultiCortex, diagnóstico, menu, API local e perfis de modelos." \
  --latest
```

### Conferir release

```bash
gh release view "$TAG" --repo hawkinf/multicortexEXO_fork
gh release list --repo hawkinf/multicortexEXO_fork
```

### Atualizar assets de uma release existente

```bash
gh release upload "$TAG" \
  "$ISO" \
  "$SHA" \
  --repo hawkinf/multicortexEXO_fork \
  --clobber
```

---


## Validações realizadas

### Ambiente de build

```bash
bash scripts/build/check-build-env.sh
```

Resultado validado:

```text
kiwi-ng: /usr/bin/kiwi-ng
xmllint: /usr/bin/xmllint
shellcheck: /usr/bin/shellcheck
config.xml: OK
config.sh: OK
scripts: OK
```

### Sintaxe Bash

```bash
bash -n scripts/models/*.sh
bash -n scripts/system/*.sh
bash -n scripts/build/*.sh
```

Resultado: sem erros.

### ShellCheck

```bash
shellcheck scripts/models/*.sh scripts/system/*.sh scripts/build/*.sh
```

Resultado: sem avisos após ajustes.

### XML

```bash
xmllint --noout suse/x86_64/suse-leap-15.6-JeOS/config.xml
```

Resultado: sem erros.

### Git

```bash
git diff --check
git status -sb
```

Resultado: sem problemas de whitespace; alterações commitadas e enviadas para `origin/main`.

### Build

```bash
bash scripts/build/build-iso.sh
bash scripts/build/check-result.sh
```

Resultado:

```text
MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
SHA256: 03c9de435287e76e602b8b7d6860e0cd46a6e307d54590c24d85735341fb483d
```

---

## Segurança

O multicortexEXO deve ser tratado como um sistema operacional completo.

Recomendações:

- não incluir chaves privadas dentro da ISO pública;
- não embutir tokens de API no repositório;
- não deixar SSH aberto sem senha forte ou chave;
- trocar as senhas padrão `root/linux` e `tux/linux` antes de usar a ISO em rede, publicar uma versão final ou habilitar SSH;
- não rodar agentes com privilégios root sem necessidade;
- não executar comandos sugeridos por IA sem revisão;
- não incluir dados de clientes na ISO;
- validar hashes de arquivos baixados;
- manter pacotes atualizados;
- separar ambiente de teste e produção;
- usar persistência criptografada quando houver dados sensíveis.

Arquivos que não devem ser commitados:

```text
.env
*.key
*.pem
*.p12
*.token
secrets.yaml
models/
build/
out/
*.iso
*.img
```

---

## Limitações conhecidas

- Modelos grandes exigem muita RAM ou GPU.
- Boot Live pode ser mais lento em pendrive USB 2.0.
- Algumas GPUs podem exigir drivers proprietários.
- Secure Boot pode impedir o carregamento de alguns módulos.
- Sem persistência, modelos baixados podem ser perdidos ao reiniciar.
- Execução por CPU pode ser lenta.
- Nem todo backend suporta aceleração por GPU em todo hardware.
- Algumas ferramentas podem exigir internet na primeira execução.
- Esta ISO é x86_64; não roda em ARM/Raspberry Pi/Mac Apple Silicon.

---

## Roadmap

Itens planejados:

- interface gráfica própria;
- instalador simplificado;
- suporte completo a persistência;
- gerenciador de modelos;
- seleção de agente por tarefa;
- painel de logs;
- integração com RAG local;
- indexação de documentos;
- modo técnico para suporte;
- modo programação;
- modo segurança defensiva;
- modo offline completo;
- build automatizado por GitHub Actions;
- assinatura e verificação de ISO;
- documentação avançada.

---

## Troubleshooting

### A ISO não inicia

Verifique:

- se o pendrive foi gravado corretamente;
- se o boot UEFI está habilitado;
- se Secure Boot está desativado;
- se a ISO foi baixada sem corromper;
- se o hash SHA256 confere.

### O sistema inicia, mas a IA não responde

```bash
systemctl status ollama
systemctl status multicortex-chat-ui
ollama list
curl http://localhost:11434
```

### O modelo está lento

Possíveis causas:

- pouca RAM;
- modelo grande demais;
- execução apenas por CPU;
- pendrive lento;
- falta de swap;
- GPU não detectada.

### A GPU não aparece

```bash
lspci | grep -i nvidia
nvidia-smi
lsmod | grep nvidia
```

### Sem internet

```bash
ip a
nmcli device
ping 8.8.8.8
ping google.com
```

### Erro `NOKEY` durante build

Durante o build podem aparecer avisos:

```text
Header V3 RSA/SHA256 Signature ... NOKEY
```

No build realizado, esses avisos apareceram como `warning`, não como `ERROR`, e não impediram a geração da ISO.

Mesmo assim, antes de distribuir publicamente, valide a origem dos repositórios e as chaves GPG.

### Erro `baseMount() is obsolete`

Comente ou remova:

```bash
baseMount
baseCleanMount
```

### Erro `suseConfig() is obsolete`

Comente ou remova:

```bash
suseConfig
```

### Erro `suseRemoveYaST() is obsolete`

Comente ou remova:

```bash
suseRemoveYaST
```

### Erro `gconftool-2: No such file or directory`

Comente os scripts legados:

```bash
sh /studio/configure_gdm_theme.sh
sh /studio/configure_gnome_background.sh
```

---

## Licença

Este fork deve respeitar a licença do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo) e as licenças dos componentes utilizados, incluindo openSUSE, KIWI, Ollama, drivers NVIDIA e demais pacotes de terceiros.

Antes de distribuir publicamente a ISO, revise as licenças dos pacotes incluídos e confirme se redistribuição de componentes proprietários está permitida no formato pretendido.

---

## Créditos

- Projeto original: [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo)
- Fork e adaptações: **Aguinaldo Liesack Baptistini**
- Base Linux: **openSUSE Leap 15.6**
- Build da imagem: **KIWI NG**
- IA local: **Ollama**
- Drivers e componentes: respectivos autores, projetos e mantenedores

---

## Aviso

Este projeto está em desenvolvimento.

Use em ambiente de teste antes de aplicar em produção. Revise scripts antes de executar comandos administrativos. Modelos de IA podem errar, sugerir comandos incorretos ou gerar respostas incompletas. O usuário continua responsável por validar qualquer ação executada no sistema.

IA ajuda bastante, mas ainda não substitui o velho e confiável hábito de ler o log com calma.

