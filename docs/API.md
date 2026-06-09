# API HTTP do MultiCortex EXO

O backend principal de inferência local é o Ollama.

## Endpoint padrão

```text
http://127.0.0.1:11434
```

## Listar modelos instalados

```bash
curl http://127.0.0.1:11434/api/tags
```

## Exemplo de geração

```bash
curl http://127.0.0.1:11434/api/generate \
  -d '{
    "model": "llama3.1:8b",
    "prompt": "Explique o que é o MultiCortex EXO em português.",
    "stream": false
  }'
```

## Exemplo de chat

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

## Segurança

Por padrão, mantenha a API somente em `127.0.0.1`.

Evite expor `0.0.0.0:11434` diretamente na rede. Se precisar acesso remoto, use VPN, túnel SSH, proxy autenticado ou firewall.
