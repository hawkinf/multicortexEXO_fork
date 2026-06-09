# Perfis de modelos do MultiCortex EXO

A ISO base não deve carregar todos os modelos grandes. O correto é entregar a base leve, com scripts para instalar por perfil.

## Perfil leve

Comando:

```bash
multicortex-models-light
```

Modelos configurados:

- tinyllama:latest
- phi3:mini
- gemma3:1b
- qwen3:0.6b
- smollm2:1.7b

Uso: máquinas simples, testes rápidos, Live ISO em VM, 8 GB a 16 GB de RAM.

## Perfil médio

Comando:

```bash
multicortex-models-medium
```

Modelos configurados:

- llama3.1:8b
- llama3.2:3b
- mistral:7b
- qwen3:8b
- gemma3:4b
- qwen2.5:7b

Uso: PCs com 16 GB a 32 GB de RAM ou GPU de 8 GB a 12 GB.

## Perfil código

Comando:

```bash
multicortex-models-code
```

Modelos configurados:

- deepseek-coder:1.3b
- deepseek-coder:6.7b
- qwen2.5-coder:7b
- codegemma:7b
- starcoder2:7b

Uso: programação, scripts, análise técnica e manutenção.

## Perfil grande

Comando:

```bash
multicortex-models-large
```

Modelos configurados:

- llama3.1:70b
- llama3.3:70b
- qwen2.5:32b
- qwen3:32b
- mixtral:8x7b
- deepseek-r1:32b

Uso: SSD/NVMe, bastante RAM/VRAM, estação de trabalho ou servidor.

## Listar modelos instalados

```bash
multicortex-models-list
```
