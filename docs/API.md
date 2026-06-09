# API HTTP do Ollama

O backend de inferência local é o Ollama, acessível via HTTP em `127.0.0.1:11434`.

---

## Endpoint base

```
http://127.0.0.1:11434
```

---

## Listar modelos instalados

```bash
curl http://127.0.0.1:11434/api/tags
```

Retorna JSON com os modelos presentes em `/var/lib/ollama/models/`.

---

## Geração de texto

```bash
curl http://127.0.0.1:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Explique o que é um motherboard em 2 linhas.",
    "stream": false
  }'
```

Com `"stream": true` (padrão), a resposta chega em chunks JSON linha a linha.

---

## Chat multi-turno

```bash
curl http://127.0.0.1:11434/api/chat \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {"role": "system",    "content": "Você é um assistente técnico de TI."},
      {"role": "user",      "content": "O que pode causar superaquecimento em um notebook?"}
    ],
    "stream": false
  }'
```

---

## Exemplos práticos

**Diagnóstico técnico:**
```bash
curl http://127.0.0.1:11434/api/generate \
  -d '{"model": "deepseek-coder:6.7b",
       "prompt": "Explique o erro: KERNEL PANIC - not syncing: VFS: Unable to mount root fs",
       "stream": false}'
```

**Análise de código:**
```bash
curl http://127.0.0.1:11434/api/generate \
  -d '{"model": "qwen2.5-coder:7b",
       "prompt": "Revise este script bash e aponte problemas:\n#!/bin/bash\nrm -rf $PASTA/*",
       "stream": false}'
```

**Verificar se está respondendo:**
```bash
curl -fsS http://127.0.0.1:11434/api/tags | jq '.models[].name'
```

---

## Acesso remoto

Por padrão, o Ollama escuta apenas em `127.0.0.1`. Para acesso de outra máquina:

**Túnel SSH (recomendado):**
```bash
ssh -L 11434:localhost:11434 tux@<ip-da-maquina>
# Em seguida, no cliente:
curl http://127.0.0.1:11434/api/tags
```

**Nunca expor `0.0.0.0:11434` diretamente** — use VPN, proxy autenticado ou firewall com regras restritas.

---

## Variável de ambiente

```bash
export OLLAMA_HOST="127.0.0.1:11434"    # padrão — definida em /etc/profile.d/multicortex.sh
```

Para mudar o host em tempo de execução:

```bash
OLLAMA_HOST="192.168.1.10:11434" ollama run llama3.1:8b
```
