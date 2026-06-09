# Troubleshooting — Diagnóstico e Estado do Projeto

---

## Diagnóstico rápido

```bash
multicortex-status      # visão completa: versão, rede, serviços, GPU, modelos, logs
systemctl --failed      # serviços que falharam
journalctl -b -p err    # erros do boot atual
```

---

## Serviços

```bash
systemctl status ollama
journalctl -u ollama -f          # log em tempo real
journalctl -u ollama -n 50       # últimas 50 linhas

systemctl start ollama           # iniciar manualmente
systemctl restart ollama         # reiniciar
```

---

## Ollama não responde

```bash
# 1. verificar estado
systemctl status ollama

# 2. testar direto
curl http://localhost:11434

# 3. listar modelos
ollama list

# 4. iniciar se parado
systemctl start ollama

# 5. se modelo não instalado
ollama pull llama3.2
```

---

## GPU não detectada

```bash
lspci | grep -i nvidia     # verificar se a GPU aparece no PCI
nvidia-smi                 # informações detalhadas (temperatura, VRAM, processos)
lsmod | grep nvidia        # verificar se o módulo do kernel está carregado
```

Se o módulo não estiver carregado:
```bash
modprobe nvidia
```

---

## Rede sem IP

```bash
ip a                       # listar interfaces e IPs
nmcli device status        # estado do NetworkManager
ping 8.8.8.8               # testar conectividade

# Forçar DHCP na interface:
nmcli device connect eth0
```

---

## Modelo lento

Verificar se a GPU está sendo usada:
```bash
nvidia-smi    # deve mostrar o processo ollama com uso de VRAM
```

Se a GPU não aparecer, o Ollama está rodando em CPU. Causas comuns:
- Modelo maior que a VRAM disponível (Ollama usa CPU como fallback)
- Driver NVIDIA não carregado (`lsmod | grep nvidia`)
- VRAM insuficiente para o modelo selecionado

Solução imediata: tentar um modelo menor do perfil light.

---

## ISO não inicializa

1. Verificar integridade: `sha256sum MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso` e comparar com o hash publicado
2. Regravar o pendrive — a gravação pode ter corrompido
3. Confirmar UEFI habilitado no firmware
4. Confirmar **Secure Boot desligado**
5. Testar em VM antes de usar em hardware

---

## Erros no build da ISO

| Erro | Causa | Solução |
|------|-------|---------|
| `baseMount() is obsolete` | Função removida no KIWI 10 | Comentar `baseMount`/`baseCleanMount` no `config.sh` |
| `suseConfig() is obsolete` | Função removida no KIWI 10 | Comentar `suseConfig` |
| `suseRemoveYaST() is obsolete` | Função removida no KIWI 10 | Comentar `suseRemoveYaST` |
| `gconftool-2: No such file or directory` | Scripts legados de tema | Já comentados neste fork |
| Avisos `NOKEY` nos RPMs | GPG não importado | São `warning`, não `ERROR` — build prossegue normalmente |
| Conflito drivers NVIDIA | Versões 550 e 580 misturadas | Manter apenas pacotes G06 da mesma linha |
| Mirror BR falhando | `mirrorcache-br-2` instável | Usar `download.opensuse.org` (já configurado no `config.xml` deste fork) |
| Erro de certificado HTTPS no chroot | CAs não presentes no bootstrap | Garantir `ca-certificates-mozilla` e `openssl` no bloco `<packages type="bootstrap">` |

---

## Estado atual do projeto

### O que funciona

- `config.xml` com todos os pacotes, repositórios e configurações
- `config.sh` com compatibilidade com KIWI 10 (funções obsoletas comentadas)
- Overlay `root/` com MOTD, versão, aliases de shell, firstboot service, rede, repositórios JAX
- `multicortex-status.sh` e `multicortex-menu.sh` funcionais e completos
- Script Python de build automático com patch do `config.xml`
- Temas visuais: GRUB2, Plymouth, GDM, GFXBOOT, wallpaper
- ISO `MultiCortex_EXO_1.0.5` gerada e publicada no GitHub Releases

### Pendências conhecidas

**Bug crítico — `config.sh`:** o bloco `# BEGIN MULTICORTEX EXO GENERATED CONFIG` está posicionado após o `exit 0` e **nunca executa** durante o build KIWI. Os `mkdir /var/lib/ollama`, `chmod` nos scripts e `systemctl enable` do bloco são código morto. Correção: mover o bloco para antes do `exit 0`.

**Scripts referenciados mas não commitados:**

```
scripts/build/check-build-env.sh
scripts/build/install-build-deps-opensuse.sh
scripts/build/clean-build.sh
scripts/build/build-iso.sh
scripts/build/check-result.sh
scripts/models/_ollama_common.sh
scripts/models/install-light-models.sh
scripts/models/install-medium-models.sh
scripts/models/install-code-models.sh
scripts/models/install-large-models.sh
scripts/models/list-installed-models.sh
```

**Binários ausentes no overlay:** os comandos `multicortex-status`, `multicortex-menu` e `multicortex-models-*` precisam existir em `/usr/local/bin/` dentro da ISO. Os links simbólicos ou scripts não estão em `root/usr/local/bin/`.

**`/etc/multicortex.asc`** — arquivo de logo ASCII referenciado pelo `initMulticortex.sh` mas ausente do overlay.

**`multicortex-chat-ui.service`** — habilitado no `config.sh` mas sem arquivo `.service` correspondente no overlay.

**Framework `exo`** — o script `~/bin/exo` pressupõe `~/exo/.venv` instalado manualmente após o boot.

---

## Verificar integridade da ISO

```bash
sha256sum MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
# Resultado esperado:
# 93ec2e21ffb2d041eed5b06433f1f08104d6e9bcae27ebaab2399874bcdd80a2
```

O hash também está em `releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256`.
