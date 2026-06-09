# Full Offline SSD Edition

A versão Full Offline SSD Edition é uma edição especial para rodar sem internet.

## Ideia correta

1. Gerar ISO base pequena.
2. Preparar um SSD/NVMe com modelos já baixados.
3. Copiar ou montar `/var/lib/ollama`.
4. Usar a ISO para iniciar a máquina e apontar o Ollama para o diretório de modelos.

## Por que não colocar tudo na ISO base?

Modelos grandes deixam a ISO enorme, lenta para gerar, lenta para copiar e ruim para testar. Uma ISO base enxuta é mais fácil de manter.

## Preparar modelos em uma máquina com internet

```bash
ollama pull tinyllama:latest
ollama pull llama3.1:8b
ollama pull mistral:7b
ollama pull qwen3:8b
ollama pull deepseek-coder:6.7b
```

## Diretório padrão

```text
/var/lib/ollama
```

## Recomendação

Para edição offline real, use SSD externo ou NVMe dedicado. Grave também um arquivo de manifesto:

```bash
ollama list > MODELOS-INSTALADOS.txt
sha256sum MODELOS-INSTALADOS.txt > MODELOS-INSTALADOS.txt.sha256
```
