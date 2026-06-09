# Segurança

---

## Credenciais padrão

```
Usuário   Senha    Grupo
root      linux    root
tux       linux    users
```

As senhas vêm do `config.xml` em hash Unix `md5-crypt`. O hash não é reversível — apenas valida a senha digitada durante o boot.

**Trocar imediatamente antes de usar em rede ou publicar ISO:**

```bash
passwd root
passwd tux
```

Para gerar novo hash para o `config.xml` antes de um novo build:

```bash
openssl passwd -1 'NovaSenhaAqui'
# Copiar o hash gerado para o campo password= no config.xml
```

---

## API Ollama

Manter o Ollama em `127.0.0.1:11434`. Nunca expor `0.0.0.0:11434` diretamente na rede.

Para acesso remoto seguro: túnel SSH, VPN ou proxy autenticado.

```bash
# Túnel SSH
ssh -L 11434:localhost:11434 tux@<ip>
```

---

## SSH

Se usar a ISO em rede com SSH ativo:

1. Trocar as senhas de `root` e `tux`
2. Desativar login root por senha: `PermitRootLogin no` em `/etc/ssh/sshd_config`
3. Usar autenticação por chave em vez de senha
4. Configurar firewall — a ISO sobe sem firewall por padrão
5. Não publicar ISO com senha padrão

```bash
# Adicionar chave pública para o usuário tux
mkdir -p /home/tux/.ssh
echo "sua-chave-publica" >> /home/tux/.ssh/authorized_keys
chmod 600 /home/tux/.ssh/authorized_keys
chmod 700 /home/tux/.ssh
```

---

## O que nunca commitar

O `.gitignore` já exclui os tipos abaixo, mas vale reforçar:

```
*.iso         ← ISOs geradas
*.raw
*.img
*.key         ← chaves privadas
*.pem
*.p12
*.token       ← tokens de API
.env          ← variáveis de ambiente com segredos
secrets.yaml
models/       ← modelos baixados
out/          ← saída do build
build/
```

---

## ISO para distribuição pública

Antes de publicar uma ISO:

- Trocar todas as senhas padrão ou remover o autologin
- Revisar se há dados de clientes em `/home/tux/` ou `/root/`
- Revisar licenças dos pacotes incluídos — drivers NVIDIA são proprietários
- Gerar o SHA256 e publicar junto com a ISO para verificação de integridade

```bash
sha256sum MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso > MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256
```
