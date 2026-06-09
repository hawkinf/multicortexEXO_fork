# multicortexEXO

Sistema Linux Live/Instalável voltado para execução local de Inteligência Artificial, automação, agentes especializados e orquestração de múltiplos modelos de IA em ambiente controlado.

> Este projeto é um **fork** criado para permitir evolução independente, customização técnica, manutenção própria e adaptação do conceito MultiCortex para um ambiente mais prático, auditável e executável em máquinas locais, servidores, notebooks, estações de trabalho e ambientes offline.

---

## Índice

* [Sobre o projeto](#sobre-o-projeto)
* [Por que este fork foi criado](#por-que-este-fork-foi-criado)
* [O que é o multicortexEXO](#o-que-é-o-multicortexexo)
* [Como o sistema funciona](#como-o-sistema-funciona)
* [Arquitetura geral](#arquitetura-geral)
* [Requisitos para rodar a ISO](#requisitos-para-rodar-a-iso)
* [Requisitos para compilar a ISO](#requisitos-para-compilar-a-iso)
* [Como compilar](#como-compilar)
* [Como gravar a ISO em pendrive](#como-gravar-a-iso-em-pendrive)
* [Como iniciar o sistema](#como-iniciar-o-sistema)
* [Persistência de dados](#persistência-de-dados)
* [Modelos de IA suportados](#modelos-de-ia-suportados)
* [Funcionamento do multicortexEXO](#funcionamento-do-multicortexexo)
* [Estrutura do repositório](#estrutura-do-repositório)
* [Configuração](#configuração)
* [Logs e diagnóstico](#logs-e-diagnóstico)
* [Segurança](#segurança)
* [Limitações conhecidas](#limitações-conhecidas)
* [Roadmap](#roadmap)
* [Licença](#licença)
* [Créditos](#créditos)

---

## Sobre o projeto

O **multicortexEXO** é uma distribuição Linux Live/Instalável baseada em Debian/Ubuntu, criada para oferecer um ambiente pronto para uso com ferramentas de IA local, agentes, automações e modelos de linguagem executando diretamente na máquina do usuário.

A proposta é permitir que o usuário tenha uma estação de IA independente, com foco em:

* Execução local de modelos LLM.
* Uso em modo Live por pendrive.
* Possibilidade de instalação em disco.
* Operação offline quando os modelos já estiverem baixados.
* Ambiente padronizado para testes, suporte, automação e desenvolvimento.
* Separação de agentes por função.
* Orquestração de tarefas entre diferentes modelos.
* Controle maior sobre privacidade, dados e dependências externas.

Em vez de depender exclusivamente de serviços externos, o projeto busca entregar uma base local, reproduzível e modificável.

---

## Por que este fork foi criado

Este fork foi criado porque o projeto original serviu como inspiração, mas havia necessidade de uma versão com objetivos próprios, mais prática e mais controlada.

Os principais motivos do fork são:

### 1. Evolução independente

O fork permite alterar o sistema sem depender do ritmo, das escolhas técnicas ou das limitações do projeto original.

Isso possibilita:

* Ajustar scripts de build.
* Trocar pacotes.
* Adicionar suporte a novos modelos.
* Modificar a interface.
* Criar instaladores próprios.
* Integrar ferramentas específicas.
* Manter documentação própria.
* Fazer correções sem aguardar upstream.

### 2. Foco em uso real

O multicortexEXO não foi pensado apenas como demonstração. A ideia é ser um sistema utilizável em bancada técnica, laboratório, suporte, desenvolvimento, análise, automação e uso pessoal avançado.

O objetivo é que a ISO possa ser usada em cenários como:

* Boot por pendrive.
* Diagnóstico de máquinas.
* Execução local de IA.
* Ambiente de recuperação.
* Estação temporária de trabalho.
* Testes de modelos LLM.
* Execução offline.
* Demonstrações controladas.

### 3. IA local e soberania de dados

O fork busca permitir que o usuário execute IA localmente, sem enviar arquivos, prompts ou dados sensíveis para serviços externos.

Isso é importante em casos como:

* Documentos privados.
* Dados empresariais.
* Código-fonte.
* Laudos técnicos.
* Logs de clientes.
* Informações financeiras.
* Projetos internos.
* Dados que não devem sair da máquina.

### 4. Controle técnico

Ao gerar a própria ISO, é possível saber exatamente:

* Quais pacotes foram instalados.
* Quais serviços iniciam no boot.
* Quais modelos estão disponíveis.
* Quais portas estão abertas.
* Quais permissões existem.
* Quais scripts são executados.
* Como o ambiente é configurado.

Como diz o velho método: primeiro entenda a máquina, depois deixe a máquina trabalhar.

### 5. Adaptação ao conceito multicortexEXO

O multicortexEXO adiciona uma camada própria de organização, onde diferentes “córtex” ou núcleos especializados podem assumir funções diferentes dentro do sistema.

Exemplo:

* Um córtex para programação.
* Um córtex para análise de documentos.
* Um córtex para automação.
* Um córtex para terminal Linux.
* Um córtex para segurança.
* Um córtex para suporte técnico.
* Um córtex para planejamento.
* Um córtex para execução de tarefas.

---

## O que é o multicortexEXO

O **multicortexEXO** é a camada de orquestração do sistema.

Ele funciona como uma estrutura que organiza ferramentas, modelos e agentes de IA em blocos especializados. Em vez de tratar a IA como um único chatbot genérico, o sistema separa funções em núcleos especializados.

A ideia central é:

> Um problema complexo pode ser resolvido melhor quando dividido entre agentes especializados, cada um com uma função clara.

O multicortexEXO pode operar com diferentes backends de IA, como:

* Ollama.
* llama.cpp.
* vLLM.
* LM Studio.
* Open WebUI.
* Serviços externos opcionais via API.
* Scripts locais em Python.
* Ferramentas de terminal.
* Pipelines de automação.

---

## Como o sistema funciona

O fluxo básico do sistema é:

1. O computador inicia pela ISO.
2. O Linux Live carrega o sistema base.
3. Serviços essenciais são iniciados.
4. O ambiente gráfico ou terminal é carregado.
5. O multicortexEXO inicializa seus módulos.
6. Os modelos locais são detectados.
7. A interface de IA é disponibilizada ao usuário.
8. O usuário escolhe uma tarefa, agente ou modelo.
9. O multicortexEXO encaminha a tarefa para o núcleo adequado.
10. O resultado é exibido, salvo, exportado ou usado em uma automação.

Exemplo prático:

```text
Usuário
  ↓
Interface multicortexEXO
  ↓
Orquestrador
  ↓
Seleciona agente adequado
  ↓
Seleciona modelo local ou remoto
  ↓
Executa tarefa
  ↓
Retorna resposta
  ↓
Gera arquivo, comando, análise ou automação
```

---

## Arquitetura geral

A arquitetura sugerida do projeto é:

```text
multicortexEXO
├── Sistema Live Linux
│   ├── Kernel
│   ├── Initramfs
│   ├── SquashFS
│   ├── Pacotes base
│   └── Camada de persistência opcional
│
├── Camada de IA
│   ├── Ollama
│   ├── llama.cpp
│   ├── Open WebUI
│   ├── Modelos locais
│   └── APIs opcionais
│
├── Orquestrador multicortexEXO
│   ├── Agente programador
│   ├── Agente técnico
│   ├── Agente pesquisador
│   ├── Agente shell
│   ├── Agente documento
│   ├── Agente segurança
│   └── Agente automação
│
├── Ferramentas
│   ├── Python
│   ├── Git
│   ├── Docker opcional
│   ├── Editores
│   ├── Terminal
│   └── Utilitários de diagnóstico
│
└── Interface
    ├── Terminal
    ├── Painel web local
    ├── Atalhos gráficos
    └── Scripts auxiliares
```

---

## Requisitos para rodar a ISO

Os requisitos dependem dos modelos de IA que serão executados.

### Requisitos mínimos

Indicado apenas para boot, testes leves e modelos pequenos.

```text
CPU: x86_64
RAM: 8 GB
Armazenamento: pendrive de 16 GB
GPU: não obrigatória
Boot: UEFI ou Legacy, conforme build da ISO
Internet: necessária apenas para baixar modelos ou atualizações
```

### Requisitos recomendados

Indicado para uso real com modelos pequenos e médios.

```text
CPU: Intel Core i5/i7 ou AMD Ryzen 5/7
RAM: 16 GB ou mais
Armazenamento: pendrive USB 3.0 de 32 GB ou SSD externo
GPU: NVIDIA com 6 GB ou mais de VRAM, opcional
Boot: UEFI recomendado
Internet: recomendada na primeira configuração
```

### Requisitos ideais

Indicado para modelos maiores, uso com interface web e múltiplos agentes.

```text
CPU: Intel Core i7/i9 ou AMD Ryzen 7/9
RAM: 32 GB a 64 GB
Armazenamento: SSD NVMe ou SSD externo de 128 GB ou mais
GPU: NVIDIA com 12 GB ou mais de VRAM
Boot: UEFI
Internet: recomendada para baixar modelos e dependências
```

### Observação sobre GPU

O sistema pode funcionar sem GPU dedicada, usando CPU. Porém, modelos maiores serão lentos.

Para aceleração por GPU, recomenda-se:

* Placa NVIDIA.
* Driver compatível.
* CUDA configurado.
* Backend compatível com GPU.

Em máquinas antigas, o ideal é usar modelos quantizados menores.

---

## Requisitos da ISO

Para que a ISO funcione corretamente, ela deve conter:

### Sistema base

* Kernel Linux compatível com o hardware alvo.
* Initramfs funcional.
* Sistema de arquivos SquashFS.
* Bootloader GRUB ou ISOLINUX.
* Suporte a UEFI.
* Suporte opcional a Legacy BIOS.
* Pacotes essenciais de rede.
* Suporte a teclado ABNT2, se necessário.
* Locale configurado para pt_BR.UTF-8, se desejado.

### Pacotes essenciais

Recomendado incluir:

```text
git
curl
wget
nano
vim
htop
btop
python3
python3-pip
python3-venv
build-essential
ca-certificates
gnupg
lsblk
parted
gparted
rsync
openssh-client
openssh-server opcional
network-manager
```

### Pacotes de IA

Dependendo do objetivo da ISO:

```text
ollama
llama.cpp
open-webui opcional
python3-transformers opcional
python3-torch opcional
docker opcional
docker-compose opcional
```

### Requisitos de boot

A ISO deve ser híbrida, podendo ser gravada em pendrive com ferramentas como:

* Rufus.
* Balena Etcher.
* Ventoy.
* dd no Linux.
* Raspberry Pi Imager, se compatível.

### Persistência

Para salvar modelos, configurações e histórico, recomenda-se criar uma partição de persistência.

Exemplo de label:

```text
persistence
```

Arquivo de configuração típico:

```text
/persistence.conf
```

Conteúdo:

```text
/ union
```

Sem persistência, o sistema volta ao estado original após reiniciar.

---

## Requisitos para compilar a ISO

A compilação deve ser feita preferencialmente em Linux.

### Sistema recomendado para build

```text
Debian 12 ou superior
Ubuntu 22.04 ou superior
Ubuntu 24.04 ou superior
```

### Hardware recomendado para build

```text
CPU: 4 núcleos ou mais
RAM: 8 GB ou mais
Disco livre: 40 GB ou mais
Internet: obrigatória para baixar pacotes
```

### Pacotes necessários

Em Debian/Ubuntu:

```bash
sudo apt update
sudo apt install -y \
  git \
  live-build \
  debootstrap \
  squashfs-tools \
  xorriso \
  isolinux \
  syslinux-common \
  grub-pc-bin \
  grub-efi-amd64-bin \
  mtools \
  dosfstools \
  curl \
  wget \
  ca-certificates
```

---

## Como compilar

Clone o repositório:

```bash
git clone ALTERAR_AQUI_URL_DO_REPOSITORIO multicortexEXO
cd multicortexEXO
```

Atualize submódulos, se existirem:

```bash
git submodule update --init --recursive
```

Dê permissão aos scripts:

```bash
chmod +x scripts/*.sh
```

Execute a preparação do ambiente:

```bash
./scripts/prepare-build.sh
```

Compile a ISO:

```bash
./scripts/build-iso.sh
```

Se o projeto usa `live-build` diretamente, o processo pode ser:

```bash
sudo lb clean
sudo lb config
sudo lb build
```

Ao final, a ISO deve ser gerada em um caminho semelhante a:

```text
build/multicortexEXO.iso
```

ou:

```text
live-image-amd64.hybrid.iso
```

Renomeie a ISO final de forma padronizada:

```bash
mv live-image-amd64.hybrid.iso multicortexEXO-amd64.iso
```

Gere o hash SHA256:

```bash
sha256sum multicortexEXO-amd64.iso > multicortexEXO-amd64.iso.sha256
```

---

## Como gravar a ISO em pendrive

### Opção 1: Rufus no Windows

1. Abra o Rufus.
2. Selecione o pendrive.
3. Selecione a ISO `multicortexEXO-amd64.iso`.
4. Escolha GPT/UEFI, se o computador for moderno.
5. Clique em iniciar.
6. Aguarde a gravação.
7. Reinicie o computador pelo pendrive.

### Opção 2: Balena Etcher

1. Abra o Balena Etcher.
2. Selecione a ISO.
3. Selecione o pendrive.
4. Clique em Flash.
5. Aguarde a conclusão.

### Opção 3: Linux com dd

Atenção: o comando abaixo apaga completamente o disco selecionado.

Liste os discos:

```bash
lsblk
```

Grave a ISO:

```bash
sudo dd if=multicortexEXO-amd64.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

Substitua `/dev/sdX` pelo dispositivo correto.

---

## Como iniciar o sistema

1. Insira o pendrive.
2. Ligue o computador.
3. Acesse o menu de boot.
4. Escolha o pendrive.
5. Selecione uma das opções:

```text
multicortexEXO Live
multicortexEXO Live com persistência
multicortexEXO modo seguro
Instalar multicortexEXO
```

Após o boot, o sistema carregará o ambiente base.

Se houver interface gráfica, acesse o painel do multicortexEXO pelo atalho na área de trabalho ou pelo navegador local.

Exemplo:

```text
http://localhost:3000
http://localhost:8080
http://localhost:11434
```

As portas podem variar conforme a configuração do projeto.

---

## Persistência de dados

Por padrão, uma ISO Live não salva alterações após reiniciar.

Para manter dados, modelos e configurações, use persistência.

Itens que podem ser persistidos:

* Modelos baixados.
* Configuração dos agentes.
* Histórico de conversas.
* Scripts criados.
* Chaves locais.
* Configurações de rede.
* Arquivos do usuário.
* Bancos vetoriais.
* Índices de documentos.

Diretórios recomendados para persistência:

```text
/home
/opt/multicortexEXO
/var/lib/ollama
/var/lib/open-webui
```

A persistência deve ser usada com cuidado. Em ambiente técnico, o velho princípio ainda vale: backup antes, experiência depois.

---

## Modelos de IA suportados

O sistema pode ser adaptado para diversos modelos, dependendo do backend usado.

### Modelos leves

Indicados para máquinas com pouca RAM:

```text
Phi
TinyLlama
Gemma pequeno
Qwen pequeno
Llama quantizado pequeno
Mistral quantizado
```

### Modelos médios

Indicados para máquinas com 16 GB a 32 GB de RAM:

```text
Llama 3.x 8B quantizado
Mistral 7B quantizado
Qwen 7B quantizado
Gemma 7B quantizado
DeepSeek Coder pequeno/médio
```

### Modelos maiores

Indicados para máquinas com bastante RAM ou GPU:

```text
Llama 70B quantizado
Qwen 32B
Mixtral
DeepSeek maior
Modelos especializados em código
```

A disponibilidade depende de licença, tamanho, hardware e backend.

---

## Funcionamento do multicortexEXO

O multicortexEXO é a camada lógica do sistema. Ele organiza a execução da IA em múltiplos núcleos funcionais.

Cada núcleo, ou “córtex”, possui uma função específica.

### Cortex Shell

Responsável por tarefas de terminal e sistema.

Exemplos:

* Gerar comandos Linux.
* Explicar logs.
* Criar scripts Bash.
* Diagnosticar rede.
* Automatizar tarefas.

### Cortex Code

Responsável por programação.

Exemplos:

* Criar código.
* Revisar código.
* Explicar erros.
* Gerar testes.
* Refatorar projetos.
* Criar documentação técnica.

### Cortex Docs

Responsável por documentos.

Exemplos:

* Ler arquivos.
* Resumir PDFs.
* Criar relatórios.
* Gerar README.
* Criar manuais.
* Organizar documentação.

### Cortex Security

Responsável por análise defensiva e segurança.

Exemplos:

* Analisar logs.
* Verificar configurações.
* Sugerir hardening.
* Identificar riscos.
* Avaliar permissões.
* Criar checklist defensivo.

### Cortex Support

Responsável por suporte técnico.

Exemplos:

* Diagnóstico de Windows.
* Diagnóstico de Linux.
* Recuperação de ambiente.
* Checklist de atendimento.
* Geração de laudo técnico.
* Organização de procedimentos.

### Cortex Research

Responsável por pesquisa e comparação.

Exemplos:

* Comparar soluções.
* Avaliar tecnologias.
* Organizar fontes.
* Criar matrizes de decisão.
* Gerar estudos técnicos.

### Cortex Automation

Responsável por automações.

Exemplos:

* Scripts Python.
* Rotinas agendadas.
* Processamento de arquivos.
* Integração com APIs.
* Execução de pipelines.

---

## Fluxo interno do multicortexEXO

O fluxo interno sugerido é:

```text
Entrada do usuário
  ↓
Classificação da tarefa
  ↓
Escolha do córtex adequado
  ↓
Escolha do modelo adequado
  ↓
Execução local ou remota
  ↓
Validação do resultado
  ↓
Entrega ao usuário
  ↓
Registro em log, se habilitado
```

Exemplo:

```text
Pedido: "Crie um script para instalar pacotes no Debian"

Classificação:
  Tipo: programação + shell

Cortex selecionado:
  Cortex Shell
  Cortex Code

Modelo:
  Modelo local de código

Saída:
  Script Bash validado e explicado
```

---

## Estrutura do repositório

Estrutura sugerida:

```text
multicortexEXO/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── docs/
│   ├── arquitetura.md
│   ├── instalacao.md
│   ├── modelos.md
│   └── troubleshooting.md
│
├── scripts/
│   ├── prepare-build.sh
│   ├── build-iso.sh
│   ├── clean-build.sh
│   ├── install-models.sh
│   └── first-boot.sh
│
├── config/
│   ├── packages.list
│   ├── services.list
│   ├── multicortexexo.yaml
│   └── persistence.conf
│
├── live-build/
│   ├── config/
│   ├── includes.chroot/
│   ├── includes.binary/
│   └── hooks/
│
├── multicortexEXO/
│   ├── core/
│   ├── agents/
│   ├── backends/
│   ├── tools/
│   └── ui/
│
└── build/
    └── output/
```

---

## Configuração

Arquivo principal sugerido:

```text
config/multicortexexo.yaml
```

Exemplo:

```yaml
system:
  name: multicortexEXO
  mode: live
  language: pt-BR
  persistence: true

ai:
  default_backend: ollama
  default_model: llama3
  allow_remote_api: false

backends:
  ollama:
    enabled: true
    host: http://localhost:11434

  llama_cpp:
    enabled: false
    models_path: /opt/models

  openai_compatible:
    enabled: false
    base_url: ""
    api_key_env: "OPENAI_API_KEY"

agents:
  shell:
    enabled: true
  code:
    enabled: true
  docs:
    enabled: true
  security:
    enabled: true
  support:
    enabled: true
  research:
    enabled: true
  automation:
    enabled: true

logs:
  enabled: true
  path: /var/log/multicortexEXO
```

---

## Serviços

Serviços comuns que podem ser iniciados com o sistema:

```text
ollama.service
open-webui.service
multicortexexo.service
ssh.service opcional
docker.service opcional
```

Verificar status:

```bash
systemctl status multicortexexo
systemctl status ollama
```

Iniciar manualmente:

```bash
sudo systemctl start multicortexexo
```

Parar:

```bash
sudo systemctl stop multicortexexo
```

---

## Logs e diagnóstico

Logs principais:

```text
/var/log/multicortexEXO/
/var/log/syslog
/var/log/boot.log
~/.multicortexEXO/logs/
```

Comandos úteis:

```bash
journalctl -u multicortexexo -f
journalctl -u ollama -f
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

## Segurança

O multicortexEXO deve ser tratado como um sistema operacional completo.

Recomendações:

* Não incluir chaves privadas dentro da ISO pública.
* Não embutir tokens de API no repositório.
* Não deixar SSH aberto sem senha forte ou chave.
* Não rodar agentes com privilégios root sem necessidade.
* Não executar comandos sugeridos por IA sem revisão.
* Não incluir dados de clientes na ISO.
* Validar hashes de arquivos baixados.
* Manter os pacotes atualizados.
* Separar ambiente de teste e produção.
* Usar persistência criptografada quando houver dados sensíveis.

### Arquivos que não devem ser commitados

```text
.env
*.key
*.pem
*.p12
*.token
secrets.yaml
models/
build/
*.iso
*.img
```

---

## Limitações conhecidas

* Modelos grandes exigem muita RAM ou GPU.
* Boot Live pode ser mais lento em pendrive USB 2.0.
* Algumas GPUs podem exigir drivers proprietários.
* Secure Boot pode impedir o carregamento de alguns módulos.
* Sem persistência, modelos baixados são perdidos ao reiniciar.
* Execução por CPU pode ser lenta.
* Nem todo backend suporta aceleração por GPU em todo hardware.
* Algumas ferramentas podem exigir internet na primeira execução.

---

## Boas práticas de uso

1. Testar primeiro em máquina virtual.
2. Validar boot por Ventoy ou Rufus.
3. Gerar hash SHA256 da ISO.
4. Manter uma ISO limpa e uma ISO experimental.
5. Documentar alterações em `CHANGELOG.md`.
6. Separar modelos pequenos, médios e grandes.
7. Não misturar dados pessoais com builds públicos.
8. Fazer backup da persistência.
9. Testar em hardware real antes de distribuir.
10. Revisar scripts que executam comandos administrativos.

---

## Build em máquina virtual

É possível testar a ISO em:

* VMware Workstation.
* VirtualBox.
* QEMU/KVM.
* Proxmox.
* Hyper-V.

Exemplo com QEMU:

```bash
qemu-system-x86_64 \
  -m 8192 \
  -smp 4 \
  -cdrom multicortexEXO-amd64.iso \
  -boot d \
  -enable-kvm
```

Com disco virtual:

```bash
qemu-img create -f qcow2 multicortexEXO-test.qcow2 64G

qemu-system-x86_64 \
  -m 8192 \
  -smp 4 \
  -cdrom multicortexEXO-amd64.iso \
  -hda multicortexEXO-test.qcow2 \
  -boot d \
  -enable-kvm
```

---

## Como atualizar o fork

Adicionar upstream original, se aplicável:

```bash
git remote add upstream ALTERAR_AQUI_URL_DO_PROJETO_ORIGINAL
```

Buscar atualizações:

```bash
git fetch upstream
```

Mesclar alterações:

```bash
git merge upstream/main
```

Enviar para o fork:

```bash
git push origin main
```

Caso o projeto original use outro branch principal, ajuste `main` para o nome correto.

---

## Versionamento

Sugestão de padrão:

```text
0.1.0
0.2.0
0.3.0
```

Para builds de ISO:

```text
multicortexEXO-amd64-0.1.0-YYYYMMDD.iso
```

Exemplo:

```text
multicortexEXO-amd64-0.1.0-20260609.iso
```

---

## Roadmap

Itens planejados:

* Interface gráfica própria.
* Instalador simplificado.
* Suporte completo a persistência.
* Gerenciador de modelos.
* Seleção de agente por tarefa.
* Painel de logs.
* Integração com RAG local.
* Indexação de documentos.
* Modo técnico para suporte.
* Modo programação.
* Modo segurança defensiva.
* Modo offline completo.
* Build automatizado por GitHub Actions.
* Assinatura e verificação de ISO.
* Documentação avançada.

---

## Troubleshooting

### A ISO não inicia

Verifique:

* Se o pendrive foi gravado corretamente.
* Se o boot UEFI está habilitado.
* Se Secure Boot está desativado.
* Se a ISO foi baixada sem corromper.
* Se o hash SHA256 confere.

### O sistema inicia, mas a IA não responde

Verifique:

```bash
systemctl status ollama
ollama list
curl http://localhost:11434
```

### O modelo está muito lento

Possíveis causas:

* Pouca RAM.
* Modelo grande demais.
* Execução apenas por CPU.
* Pendrive lento.
* Falta de swap.
* GPU não detectada.

### A GPU não aparece

Verifique:

```bash
lspci | grep -i nvidia
nvidia-smi
lsmod | grep nvidia
```

### Sem internet

Verifique:

```bash
ip a
nmcli device
ping 8.8.8.8
ping google.com
```

---

## Licença

ALTERAR_AQUI: informe a licença correta do projeto.

Exemplos comuns:

```text
MIT
GPL-3.0
Apache-2.0
BSD-3-Clause
```

Se este projeto deriva de outro projeto, respeite a licença original.

---

## Créditos

Este projeto é um fork inspirado no conceito MultiCortex, adaptado para uma implementação própria chamada **multicortexEXO**.

Créditos:

* Projeto original: ALTERAR_AQUI
* Fork e adaptações: ALTERAR_AQUI
* Base Linux: Debian/Ubuntu
* Ferramentas de IA: conforme backends utilizados
* Comunidade open source

---

## Aviso

Este projeto está em desenvolvimento.

Use em ambiente de teste antes de aplicar em produção. Revise scripts antes de executar comandos administrativos. Modelos de IA podem errar, sugerir comandos incorretos ou gerar respostas incompletas. O usuário continua responsável por validar qualquer ação executada no sistema.

IA ajuda bastante, mas ainda não substitui o velho e confiável “ler o log com calma”.
