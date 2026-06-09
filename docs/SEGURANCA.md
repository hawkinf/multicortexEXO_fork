# Segurança do MultiCortex EXO

## Usuários padrão

A imagem original usa:

```text
root / linux
tux  / linux
```

Essas senhas vêm do `config.xml` em hash Unix `md5-crypt`. Hash não é reversível; ele apenas valida a senha digitada.

## Trocar senhas

Dentro do sistema:

```bash
passwd root
passwd tux
```

Para gerar novo hash para o `config.xml`:

```bash
openssl passwd -1
```

## API Ollama

Mantenha o Ollama em localhost:

```text
127.0.0.1:11434
```

Não exponha diretamente na internet.

## SSH

Se ativar SSH:

1. Troque as senhas.
2. Desative login root por senha se possível.
3. Use chave SSH.
4. Use firewall.
5. Não publique ISO final com senha padrão.

## O que nunca commitar

- `.env`
- tokens
- chaves privadas
- arquivos `.pem`, `.key`, `.p12`
- modelos baixados
- ISOs grandes
