# multicortexEXO

Sistema Linux Live/Bootável baseado em **openSUSE Leap 15.6 x86_64**, voltado para execução local de Inteligência Artificial, automação, agentes especializados e orquestração de múltiplos modelos de IA em ambiente controlado.

Este projeto é um **fork/adaptação técnica** do projeto original [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo), criado para permitir evolução independente, customização, manutenção própria, geração local da ISO e adaptação do conceito MultiCortex para um ambiente prático, auditável e executável em máquinas locais, servidores, notebooks, estações de trabalho e ambientes offline.

---

## Índice

- [Sobre o projeto](#sobre-o-projeto)
- [Por que este fork foi criado](#por-que-este-fork-foi-criado)
- [O que foi gerado](#o-que-foi-gerado)
- [Como o sistema funciona](#como-o-sistema-funciona)
- [Arquitetura geral](#arquitetura-geral)
- [Requisitos para rodar a ISO](#requisitos-para-rodar-a-iso)
- [Requisitos para compilar a ISO](#requisitos-para-compilar-a-iso)
- [Como compilar a ISO](#como-compilar-a-iso)
- [Como testar a ISO](#como-testar-a-iso)
- [Usuários e senhas padrão da ISO](#usuários-e-senhas-padrão-da-iso)
- [Como gravar a ISO em pendrive](#como-gravar-a-iso-em-pendrive)
- [Persistência de dados](#persistência-de-dados)
- [Modelos de IA suportados](#modelos-de-ia-suportados)
- [Funcionamento do multicortexEXO](#funcionamento-do-multicortexexo)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Configuração](#configuração)
- [Serviços](#serviços)
- [Logs e diagnóstico](#logs-e-diagnóstico)
- [Publicação no GitHub](#publicação-no-github)
- [Segurança](#segurança)
- [Limitações conhecidas](#limitações-conhecidas)
- [Roadmap](#roadmap)
- [Troubleshooting](#troubleshooting)
- [Licença](#licença)
- [Créditos](#créditos)

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

Estrutura recomendada do fork:

```text
multicortexEXO_fork/
├── README.md
├── .gitignore
├── docs/
│   ├── documentacao_multicortex_exo_bootable_opensuse.md
│   └── documentacao_multicortex_exo_bootable_opensuse.docx
│
├── scripts/
│   └── gerar_iso_multicortex_completo_py36.py
│
├── patches/
│   └── notas-build-opensuse-leap-15.6.md
│
├── releases/
│   └── MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256
│
└── suse/
    └── x86_64/
        └── suse-leap-15.6-JeOS/
            ├── config.xml
            ├── config.sh
            └── demais arquivos KIWI
```

---

## Configuração

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

## Publicação no GitHub

### Criar pasta local do fork

```bash
cd /home/hawk

rm -rf /home/hawk/multicortexEXO_fork
mkdir -p /home/hawk/multicortexEXO_fork
```

Copiar o conteúdo original sem o `.git`:

```bash
rsync -a   --exclude='.git'   /home/hawk/builds/multicortex-exo/   /home/hawk/multicortexEXO_fork/
```

Copiar arquivos corrigidos:

```bash
cp -a /home/hawk/builds/kiwi-desc/config.xml   /home/hawk/multicortexEXO_fork/suse/x86_64/suse-leap-15.6-JeOS/config.xml

cp -a /home/hawk/builds/kiwi-desc/config.sh   /home/hawk/multicortexEXO_fork/suse/x86_64/suse-leap-15.6-JeOS/config.sh
```

Criar estrutura auxiliar:

```bash
mkdir -p /home/hawk/multicortexEXO_fork/scripts
mkdir -p /home/hawk/multicortexEXO_fork/docs
mkdir -p /home/hawk/multicortexEXO_fork/patches
mkdir -p /home/hawk/multicortexEXO_fork/releases
```

Copiar script de build:

```bash
cp -a /home/hawk/gerar_iso_multicortex_completo_py36.py   /home/hawk/multicortexEXO_fork/scripts/
```

Gerar checksum:

```bash
sha256sum /home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso   > /home/hawk/multicortexEXO_fork/releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256
```

### Criar `.gitignore`

```bash
cd /home/hawk/multicortexEXO_fork

cat > .gitignore <<'EOF'
out/
build/
image-root/
*.iso
*.raw
*.qcow2
*.img
*.vmdk
*.log
.cache/
__pycache__/
*.pyc
*.tmp
*.bak
*.bak2
*~
EOF
```

### Inicializar Git

```bash
cd /home/hawk/multicortexEXO_fork

git init
git branch -M main
git config user.name "Aguinaldo"
git config user.email "hawkinf@gmail.com"
```

### Commit inicial

```bash
git add .
git commit -m "Initial MultiCortex EXO fork with KIWI 10 compatibility"
```

### Criar repositório no GitHub

```bash
gh repo create hawkinf/multicortexEXO_fork   --public   --source=.   --remote=origin   --push
```

Para privado:

```bash
gh repo create hawkinf/multicortexEXO_fork   --private   --source=.   --remote=origin   --push
```

### Se o repositório já existir

```bash
cd /home/hawk/multicortexEXO_fork

git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/hawkinf/multicortexEXO_fork.git
git push -u origin main
```

### Publicar ISO em GitHub Release

A ISO não deve ser enviada no commit Git. Ela deve ser publicada como asset de release.

```bash
cd /home/hawk/multicortexEXO_fork

gh release create v1.0.5-leap15.6   /home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso   /home/hawk/multicortexEXO_fork/releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256   --title "MultiCortex EXO 1.0.5 - openSUSE Leap 15.6 x86_64"   --notes "ISO bootável do MultiCortex EXO baseada em openSUSE Leap 15.6, arquitetura x86_64. Gerada com ajustes de compatibilidade para KIWI 10.x."
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

<!-- BEGIN MULTICORTEX EXO GENERATED README SECTION -->

## MultiCortex EXO Fork - operação da ISO Live

Este fork prepara uma ISO Linux Live baseada em openSUSE Leap 15.6 x86_64, gerada com KIWI NG, com foco em IA local, Ollama, Web UI, API HTTP, perfis de modelos e uso em ambiente offline/controlado.

### Usuários e senhas padrão da ISO

- root / linux
- tux / linux

Essas senhas aparecem no `config.xml` em formato de hash Unix `md5-crypt`. Hash não é reversível; ele apenas valida a senha durante o login.

Antes de usar SSH, rede ou publicar uma ISO final, troque as senhas com:

- `passwd root`
- `passwd tux`
- `openssl passwd -1`

### Comandos principais dentro da ISO

- `multicortex-menu`
- `multicortex-status`
- `multicortex-models-light`
- `multicortex-models-medium`
- `multicortex-models-code`
- `multicortex-models-large`
- `multicortex-models-list`

### Arquitetura recomendada

A ISO base deve continuar enxuta. O desenho recomendado é:

1. ISO Base: openSUSE Leap 15.6, Ollama, Web UI/API, scripts, diagnóstico e documentação.
2. Model Pack: scripts para baixar modelos por perfil.
3. Full Offline SSD Edition: SSD/NVMe com `/var/lib/ollama` já populado.

### Build rápido

- `bash scripts/build/check-build-env.sh`
- `bash scripts/build/clean-build.sh`
- `bash scripts/build/build-iso.sh`
- `bash scripts/build/check-result.sh`

### Documentação complementar

- `docs/BUILD.md`
- `docs/API.md`
- `docs/MODELOS.md`
- `docs/FULL_OFFLINE.md`
- `docs/SEGURANCA.md`

<!-- END MULTICORTEX EXO GENERATED README SECTION -->
