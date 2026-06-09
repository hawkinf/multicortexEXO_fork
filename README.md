# multicortexEXO

**ISO Linux Live bootável** baseada em **openSUSE Leap 15.6 x86_64** com ambiente GNOME, suporte a GPU NVIDIA e IA local via **Ollama** — sem nuvem, sem internet obrigatória após o primeiro setup.

Fork independente de [`cabelo/multicortex-exo`](https://github.com/cabelo/multicortex-exo).

---

## O que é

Uma distribuição Linux especializada que inicializa em qualquer PC x86_64 (pendrive, VM ou rede) com Ollama já rodando, GNOME pronto e drivers NVIDIA carregados. Sem instalação, sem configuração manual.

**Casos de uso:**

- Bancada técnica: IA local para diagnósticos sem enviar dados do cliente para fora
- Laboratório de modelos: testar LLMs sem poluir o sistema principal
- Demonstração offline: IA funcionando sem internet para o cliente
- Desenvolvimento: Python 3.12, Node.js 20, compiladores e bibliotecas de IA prontos no boot

## Versão atual

```
ISO:     MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
SHA256:  93ec2e21ffb2d041eed5b06433f1f08104d6e9bcae27ebaab2399874bcdd80a2
```

Download: [Releases](https://github.com/hawkinf/multicortexEXO_fork/releases)

---

## Quickstart

### 1. Gerar a ISO

```bash
su -
python3 scripts/gerar_iso_multicortex_completo_py36.py
```

Requer openSUSE Leap 15.6 x86_64. O script instala dependências, clona o upstream, patcha o `config.xml` e chama o KIWI. ISO em `/home/hawk/builds/out/`.

→ Passo a passo completo: [docs/BUILD.md](docs/BUILD.md)

### 2. Gravar no pendrive

```bash
sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
        of=/dev/sdX bs=4M status=progress conv=fsync
```

Windows: Rufus (GPT/UEFI). macOS/outros: Balena Etcher.

### 3. Inicializar

UEFI habilitado, Secure Boot **desligado**. Autologin do usuário `tux`. Ollama disponível em `http://127.0.0.1:11434`.

### 4. Instalar modelos

```bash
multicortex-models-light    # tinyllama, phi3:mini, gemma3:1b — para VMs e notebooks
multicortex-models-medium   # llama3.1:8b, mistral:7b — para PCs com 16+ GB RAM
multicortex-models-code     # deepseek-coder, qwen2.5-coder — para programação
multicortex-models-large    # llama3.1:70b, mixtral — para workstations
```

→ Detalhes de cada perfil: [docs/MODELS.md](docs/MODELS.md)

### 5. Verificar tudo

```bash
multicortex-status    # versão, rede, serviços, GPU, modelos, logs
multicortex-menu      # menu interativo com todas as opções
```

---

## Credenciais padrão

```
root / linux
tux  / linux
```

Trocar antes de usar em rede: `passwd root && passwd tux`

---

## Requisitos de hardware

A ISO é **exclusivamente x86_64**. Não funciona em ARM ou Apple Silicon.

| Uso | RAM | GPU | Armazenamento |
|-----|-----|-----|---------------|
| Boot / VM / modelos leves | 4–16 GB | opcional | — |
| Modelos médios (7–8B) | 16–32 GB | 8 GB VRAM recomendado | 80 GB+ |
| Modelos grandes (32–70B) | 32–64+ GB | ≥12 GB VRAM | SSD NVMe 128 GB+ |

---

## Estrutura do repositório

```
multicortexEXO_fork/
├── scripts/
│   ├── gerar_iso_multicortex_completo_py36.py   script de build automático
│   └── system/
│       ├── multicortex-status.sh                diagnóstico do sistema
│       └── multicortex-menu.sh                  menu interativo
├── suse/x86_64/suse-leap-15.6-JeOS/
│   ├── config.xml                               definição da imagem KIWI
│   ├── config.sh                                script de pós-build (chroot)
│   └── root/                                    overlay copiado na ISO
├── docs/                                        documentação técnica
├── layout/                                      logo e wallpaper
├── releases/                                    hashes SHA256
└── custom_boot/                                 biblioteca KIWI legada (upstream)
```

---

## Documentação

| Arquivo | Conteúdo |
|---------|----------|
| [docs/BUILD.md](docs/BUILD.md) | Walkthrough completo: do comando à ISO rodando |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Como a ISO funciona, overlay, serviços, programas incluídos |
| [docs/SCRIPTS.md](docs/SCRIPTS.md) | Funcionamento detalhado de cada script |
| [docs/MODELS.md](docs/MODELS.md) | Perfis de modelos, tabelas de hardware, uso offline |
| [docs/API.md](docs/API.md) | Endpoints da API HTTP do Ollama |
| [docs/SECURITY.md](docs/SECURITY.md) | Credenciais, segurança, o que nunca commitar |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Diagnóstico, erros comuns, estado atual e pendências |

---

## Serviços ativos no boot

| Serviço | Porta | Função |
|---------|-------|--------|
| `ollama` | 11434 | Backend LLM local |
| `sshd` | 22 | Acesso remoto |
| `multicortex-firstboot` | — | Cria `/var/lib/ollama` na primeira inicialização |

---

## Licença e créditos

Projeto original: **Alessandro de Oliveira Faria (CABELO)** — `cabelo@opensuse.org`

Fork e adaptações: **Aguinaldo Liesack Baptistini** — Hawk Informática

Este fork respeita a licença do projeto original e as licenças de todos os componentes incluídos. Antes de redistribuir a ISO publicamente, revisar as licenças dos pacotes NVIDIA.
