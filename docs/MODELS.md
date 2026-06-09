# Modelos de IA — Perfis e Instalação

A ISO base não inclui modelos. Eles são baixados após o boot via Ollama, por perfil de hardware.

---

## Antes de instalar

Confirmar que o Ollama está ativo:

```bash
systemctl status ollama
curl http://127.0.0.1:11434/api/tags
```

Se estiver parado:

```bash
systemctl start ollama
```

---

## Perfil leve — 8–16 GB RAM

```bash
multicortex-models-light
```

Para VMs, notebooks simples e testes rápidos. Todos rodam bem em CPU sem GPU.

| Modelo | Parâmetros | Tamanho aprox. | Uso |
|--------|-----------|----------------|-----|
| `tinyllama:latest` | 1.1B | ~637 MB | Ultra-leve, respostas rápidas mesmo sem GPU |
| `phi3:mini` | 3.8B | ~2.2 GB | Microsoft Phi-3, bom custo-benefício |
| `gemma3:1b` | 1B | ~815 MB | Google Gemma 3, eficiente |
| `qwen3:0.6b` | 0.6B | ~522 MB | Menor modelo disponível |
| `smollm2:1.7b` | 1.7B | ~1 GB | HuggingFace SmolLM2 |

---

## Perfil médio — 16–32 GB RAM, GPU 8–12 GB VRAM

```bash
multicortex-models-medium
```

PCs com hardware razoável. Com GPU, respostas rápidas. Sem GPU, alguns segundos por resposta.

| Modelo | Parâmetros | Uso |
|--------|-----------|-----|
| `llama3.1:8b` | 8B | Meta LLaMA 3.1 — melhor equilíbrio geral |
| `llama3.2:3b` | 3B | Meta LLaMA 3.2 — mais rápido |
| `mistral:7b` | 7B | Forte em raciocínio e seguimento de instruções |
| `qwen3:8b` | 8B | Alibaba Qwen 3 — bom em multilíngue |
| `gemma3:4b` | 4B | Google Gemma 3 médio |
| `qwen2.5:7b` | 7B | Qwen 2.5 — bom desempenho em português |

---

## Perfil código — 16–32 GB RAM

```bash
multicortex-models-code
```

Especializado em programação, análise técnica e geração de scripts.

| Modelo | Parâmetros | Especialidade |
|--------|-----------|---------------|
| `deepseek-coder:1.3b` | 1.3B | DeepSeek Coder leve |
| `deepseek-coder:6.7b` | 6.7B | DeepSeek Coder completo |
| `qwen2.5-coder:7b` | 7B | Alibaba, múltiplas linguagens |
| `codegemma:7b` | 7B | Google, forte em Python e C++ |
| `starcoder2:7b` | 7B | BigCode, treinado em 600+ linguagens |

---

## Perfil grande — 32–64+ GB RAM, GPU ≥12 GB VRAM

```bash
multicortex-models-large
```

Workstations com SSD NVMe e GPU dedicada. Qualidade próxima a serviços de nuvem.

| Modelo | Parâmetros | Uso |
|--------|-----------|-----|
| `llama3.1:70b` | 70B | Meta LLaMA 3.1 full — qualidade próxima a GPT-4 |
| `llama3.3:70b` | 70B | Meta LLaMA 3.3 — mais recente |
| `qwen2.5:32b` | 32B | Alibaba, forte em multilíngue |
| `qwen3:32b` | 32B | Qwen 3 médio-grande |
| `mixtral:8x7b` | 46.7B MoE | Mistral Mixture of Experts |
| `deepseek-r1:32b` | 32B | DeepSeek R1 — raciocínio avançado |

> Sem GPU: modelos acima de 7B levam de 30 segundos a vários minutos por resposta.

---

## Listar modelos instalados

```bash
multicortex-models-list
# ou:
ollama list
# ou via API:
curl http://127.0.0.1:11434/api/tags
```

---

## Instalar modelos individualmente

```bash
ollama pull tinyllama:latest
ollama pull llama3.1:8b
ollama pull mistral:7b
```

---

## Usar um modelo

```bash
# Interativo:
ollama run tinyllama

# Com prompt direto:
ollama run llama3.1:8b "Resuma em 3 linhas o que é um sistema operacional"

# Via API:
curl http://127.0.0.1:11434/api/generate \
  -d '{"model": "llama3.1:8b", "prompt": "O que é IA local?", "stream": false}'
```

---

## Onde os modelos ficam armazenados

```
/var/lib/ollama/models/
├── blobs/
│   └── sha256-[hash]         ← pesos em formato GGUF
└── manifests/
    └── registry.ollama.ai/library/[modelo]/[tag]
```

Com persistência ativa no pendrive, os modelos sobrevivem ao reinício. Sem persistência, são perdidos ao desligar.

---

## Edição offline com SSD

Para ambientes sem internet:

**1. Em uma máquina com internet, baixar os modelos:**

```bash
ollama pull tinyllama:latest
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull deepseek-coder:6.7b
```

**2. Copiar para SSD externo:**

```bash
rsync -av /var/lib/ollama/ /mnt/ssd-externo/ollama/
```

**3. Gerar manifesto de controle:**

```bash
ollama list > MODELOS.txt
sha256sum MODELOS.txt > MODELOS.txt.sha256
```

**4. No ambiente offline:** inicializar a ISO com o SSD conectado, montar e apontar o Ollama para o diretório de modelos, ou copiar para a camada de persistência.

---

## Requisitos de hardware por perfil

| Perfil | RAM mínima | GPU VRAM | Armazenamento |
|--------|-----------|---------|---------------|
| Leve | 8 GB | opcional | — |
| Médio | 16 GB | 8 GB recomendado | 40 GB+ |
| Código | 16 GB | 8 GB recomendado | 40 GB+ |
| Grande | 32 GB | ≥12 GB | SSD NVMe 128 GB+ |
