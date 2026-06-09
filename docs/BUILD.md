# Build da ISO — Walkthrough Completo

Passo a passo de tudo que acontece ao executar o build, do primeiro comando até a ISO inicializar e o modelo responder. Exemplo usado: perfil **light**.

---

## Visão geral do fluxo

```
python3 gerar_iso.py
  └─ verifica root, detecta SO
  └─ zypper install kiwi-ng
  └─ git clone cabelo/multicortex-exo
  └─ copytree → workdir/kiwi-desc/
  └─ patch config.xml (HTTP, repos, bootstrap, NVIDIA G06)
  └─ kiwi-ng --debug system build
       ├─ valida config.xml
       ├─ fase bootstrap: rpm instala 10 pkgs no root tree
       ├─ fase image: chroot + zypper instala ~800 pkgs
       ├─ copia overlay root/ → root tree
       ├─ executa config.sh no chroot
       ├─ dracut: gera initramfs com módulo kiwi-live
       ├─ mksquashfs: comprime com xz → ~1.8 GB
       ├─ monta estrutura ISO (EFI/, LiveOS/, isolinux/)
       └─ xorriso: gera .iso híbrido (UEFI + BIOS + pendrive)

dd → pendrive → UEFI → GRUB2 → kernel + overlay
  └─ systemd → ollama, sshd, gdm
  └─ GNOME → autostart → ollama run llama3.2

multicortex-models-light
  └─ ollama pull: tinyllama, phi3:mini, gemma3:1b, qwen3:0.6b, smollm2:1.7b
```

---

## Pré-requisito

**openSUSE Leap 15.6 x86_64** — em VMware, VirtualBox, Proxmox ou máquina física. O KIWI é dependente do ambiente de build da SUSE; outras distribuições podem funcionar mas não são validadas.

---

## Parte 1 — Script Python

### Passo 1: executar como root

```bash
su -
python3 scripts/gerar_iso_multicortex_completo_py36.py
```

O `su -` é obrigatório — não `sudo`. O KIWI usa `loop devices`, monta sistemas de arquivos e faz `chroot`; com sudo algumas operações falham silenciosamente. O script verifica `os.geteuid() == 0` e encerra imediatamente se não for root.

**Flags disponíveis:**

```bash
--clean           apaga workdir inteiro antes de começar
--no-install      pula instalação de pacotes (kiwi-ng já disponível)
--workdir PATH    pasta de trabalho (padrão: /home/hawk/builds ou ~/builds)
```

### Passo 2: detecção do SO

Lê e parseia `/etc/os-release`. Avisa se `VERSION_ID != "15.6"` mas não aborta.

### Passo 3: instalação de dependências no host

```
zypper --gpg-auto-import-keys refresh
zypper install -y git python3 python3-pip python3-kiwi curl wget nano
                  xz tar gzip cpio rsync which
                  ca-certificates ca-certificates-mozilla openssl
```

`--gpg-auto-import-keys` aceita chaves GPG novas sem interação. O pacote crítico é `python3-kiwi` — traz o `kiwi-ng`. Se não for encontrado após a instalação, o script adiciona automaticamente o repositório KIWI Builder e reinstala:

```
zypper ar -f https://download.opensuse.org/repositories/
              Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/
              kiwi-builder
```

Encerra com `kiwi-ng --version` para confirmar.

### Passo 4: clone ou atualização do upstream

```
git clone https://github.com/cabelo/multicortex-exo.git
# ou, se já existe:
git pull --ff-only
```

`--ff-only` (fast-forward only) rejeita pull se houver commits divergentes — garante que o build é sempre baseado no upstream limpo. Valida que `suse/x86_64/suse-leap-15.6-JeOS` existe no clone.

### Passo 5: cópia do descritor KIWI

```python
shutil.copytree(src, dst, symlinks=True)
```

Copia `multicortex-exo/suse/x86_64/suse-leap-15.6-JeOS` para `workdir/kiwi-desc/`. O original no upstream não é tocado — todas as modificações ficam na cópia.

### Passo 6: patch do `config.xml`

Todas as modificações são feitas em memória e gravadas de volta. O arquivo no upstream não é alterado.

**HTTPS → HTTP:** o prefixo `obs://` é URL interna do OBS (Build Service da SUSE) — só funciona na infraestrutura deles. URLs HTTPS são convertidas para HTTP porque o chroot KIWI é isolado sem CAs configurados; conexões HTTPS falhariam com erro de certificado.

**Repositórios non-oss e NVIDIA** são inseridos antes do bloco `<packages type="image">` se não estiverem presentes. A função verifica idempotência — não duplica se já existirem.

**Bootstrap críticos:** garante `ca-certificates-mozilla` e `openssl` no bloco `<packages type="bootstrap">`. Sem eles, qualquer download HTTPS feito durante a fase de instalação dentro do chroot falha. Usa regex com `re.DOTALL` para localizar o bloco no XML multilinha.

**5 pacotes NVIDIA G06 garantidos:**
```
nvidia-common-G06  nvidia-compute-G06  nvidia-compute-utils-G06
nvidia-utils-G06   nvidia-driver-G06-kmp-default
```
Verifica presença em aspas simples E duplas antes de inserir (o XML usa os dois formatos).

**Compatibilidade KIWI 10:** comenta `baseMount` e `baseCleanMount` no `config.sh` se ainda estiverem presentes — funções removidas no KIWI 10 que causam erro de build.

### Passo 7: execução do KIWI

```bash
kiwi-ng --debug system build \
  --description workdir/kiwi-desc/ \
  --target-dir   workdir/out/
```

O script usa `subprocess.Popen` para ler a saída linha a linha em tempo real, imprimindo na tela e gravando em `builds/build-multicortex.log` simultaneamente. `stderr=STDOUT` une os dois streams para manter ordem cronológica.

---

## Parte 2 — KIWI internamente

### Passo 8: parsing e validação

KIWI valida o `config.xml` contra o schema 6.4. Verifica tipos de imagem, repositórios acessíveis e atributos obrigatórios. XML inválido aborta o build com erro de schema.

### Passo 9: fase bootstrap

KIWI cria o **root tree** — diretório temporário onde a imagem será montada — e instala os pacotes de `<packages type="bootstrap">` **usando `rpm` diretamente no host**, sem zypper dentro do chroot, porque o zypper ainda não existe na imagem:

```xml
<packages type="bootstrap">
    <package name="filesystem"/>           <!-- cria /usr /etc /var etc (FHS) -->
    <package name="glibc-locale"/>         <!-- libs de localização -->
    <package name="udev"/>
    <package name="ca-certificates"/>
    <package name="ca-certificates-mozilla"/>  <!-- CAs para HTTPS no chroot -->
    <package name="openssl"/>
    <package name="openSUSE-release"/>     <!-- define a distro para o zypper -->
    <package name="cracklib-dict-full"/>
    <package name="module-init-tools"/>
</packages>
```

### Passo 10: fase image

Com o bootstrap no lugar, o KIWI entra no chroot e usa o zypper de dentro:

```bash
chroot /tmp/kiwi-root-tree-XXXX zypper install [pacotes do config.xml]
```

Você declara ~120 pacotes no `config.xml`, mas o solver instala ~800 por dependências transitivas. O `solver.onlyRequires = true` (injetado pelo patch e confirmado pelo `config.sh`) evita centenas de pacotes `Recommended` desnecessários.

No terminal você vê:
```
[ 45%] Installing: kernel-default-6.4.0-150600.23.25.1.x86_64
[ 46%] Installing: python312-3.12.4-150600.3.3.1.x86_64
[ 47%] Installing: ollama-0.3.6-lp156.1.x86_64
```

### Passo 11: cópia do overlay `root/`

O KIWI copia `kiwi-desc/root/` para dentro do root tree, **sobrescrevendo** qualquer arquivo instalado por pacote. É o mecanismo de customização — você substitui qualquer arquivo de qualquer pacote colocando a versão modificada no overlay.

Também extrai os `.tar` declarados no `config.xml` (`plymouth.tar`, `gdm.tar`) — os temas visuais entram na imagem aqui.

### Passo 12: execução do `config.sh` no chroot

```bash
chroot /tmp/kiwi-root-tree-XXXX /bin/bash /image/config.sh
```

O KIWI injeta funções utilitárias em `/.kconfig` antes de executar. Em sequência:

- `suseSetupProduct` — cria `/etc/products.d/baseproduct`
- `suseImportBuildKey` — importa GPG da SUSE no banco RPM da imagem
- `sed` ativa `solver.onlyRequires` no `zypp.conf` da imagem
- `baseUpdateSysConfig` — define autologin do `tux`, GDM, GNOME
- `suseInsertService sshd/ollama/multicortex-chat-ui` — cria links em `/etc/systemd/system/multi-user.target.wants/`
- `rm -rf /usr/share/doc/packages/*` — remove documentação
- `/sbin/ldconfig` — reconstrói cache do linker dinâmico
- `baseSetRunlevel 5` — define `graphical.target`
- **`exit 0`** — o script termina aqui

> **Bug conhecido:** o bloco `MULTICORTEX EXO GENERATED CONFIG` está posicionado após o `exit 0` e **nunca executa**. O `multicortex-firstboot.service` (no overlay) supre a criação dos diretórios no boot.

### Passo 13: geração do initramfs

```bash
chroot dracut --force --add "kiwi-live" [...]
```

O módulo `kiwi-live` (do pacote `dracut-kiwi-live`) ensina o initramfs a montar o SquashFS e criar o overlay. Inclui scripts de detecção de mídia, módulos do kernel (squashfs, loop, ext4, usb) e binários mínimos.

### Passo 14: compressão SquashFS

```bash
mksquashfs /tmp/kiwi-root-tree-XXXX LiveOS/squashfs.img -comp xz -b 1M
```

`xz` oferece a melhor compressão. Um root tree de ~8 GB vira ~1.8 GB. Descompressão sob demanda — o kernel descomprime apenas os blocos acessados, não a imagem inteira.

### Passo 15: estrutura da ISO

```
/tmp/kiwi-iso-XXXX/
├── EFI/BOOT/
│   ├── bootx64.efi     ← shim (1º estágio UEFI)
│   └── grub.efi        ← GRUB2 (2º estágio UEFI)
├── LiveOS/
│   └── squashfs.img    ← sistema completo comprimido
├── boot/grub2/themes/studio/
└── isolinux/           ← SYSLINUX para BIOS legacy
```

### Passo 16: ISO híbrida final

```bash
xorriso -as mkisofs \
  -eltorito-boot isolinux/isolinux.bin \  ← boot BIOS
  -eltorito-alt-boot \
  -e EFI/BOOT/bootx64.efi \              ← boot UEFI
  -isohybrid-mbr isohdpfx.bin \          ← MBR para pendrive
  -output MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

Uma única imagem que funciona simultaneamente como ISO 9660 (CD/DVD), disco com MBR (pendrive via BIOS) e GPT com partição ESP (pendrive via UEFI). O `hybridpersistent="true"` do `config.xml` reserva espaço para a partição ext4 de persistência.

```
=== ISO gerada com sucesso ===
 - /home/hawk/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso (1.79 GiB)
```

---

## Parte 3 — Do pendrive ao modelo respondendo

### Passo 17: gravação no pendrive

```bash
sudo dd if=MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
        of=/dev/sdX bs=4M status=progress conv=fsync
```

`conv=fsync` força escrita física antes de retornar — sem ele, dados podem estar apenas no cache do kernel quando o terminal indica término.

### Passo 18: boot UEFI

Firmware escaneia dispositivos em busca de `EFI/BOOT/bootx64.efi`. Encontra no pendrive, carrega o shim, que carrega o GRUB2. Menu "studio" aparece; sem interação, a entrada Live é selecionada automaticamente.

### Passo 19: kernel e Plymouth

GRUB2 carrega o `kernel-default` + initramfs com parâmetro `splash`. Plymouth exibe a animação tema "studio".

### Passo 20: dracut-kiwi-live monta o overlay

O módulo `kiwi-live` localiza a ISO/pendrive via `CDLABEL`:

1. Monta SquashFS como loop read-only → `/run/rootfsbase`
2. Verifica espaço disponível para partição ext4 de persistência
3. Se houver: monta ext4. Se não: usa RAM (tmpfs)
4. Cria o overlay:
```bash
mount -t overlay overlay \
  -o lowerdir=/run/rootfsbase,upperdir=/run/overlay,workdir=/run/work \
  /sysroot
```
5. `pivot_root` para `/sysroot`

Leituras → SquashFS (read-only). Escritas → ext4 (persistente) ou RAM.

### Passo 21: systemd sobe os serviços

**`multicortex-firstboot.service`:**
```bash
mkdir -p /var/lib/ollama /var/log/multicortex
chmod 755 /var/lib/ollama /var/log/multicortex
```
Cria os diretórios que o Ollama precisa (necessário pelo bug do `exit 0` no `config.sh`).

**`ollama.service`:** inicia em `127.0.0.1:11434`. Verifica `/var/lib/ollama/models/` — sem modelos, apenas aguarda.

**`sshd.service`:** porta 22.

### Passo 22: GDM e GNOME

GDM lê `DISPLAYMANAGER_AUTOLOGIN=tux` e faz login sem senha. GNOME carrega.

**Autostart `config_osviacam.sh`** (executa uma vez):
```bash
gsettings set org.gnome.shell favorite-apps "['firefox.desktop', 'org.gnome.Terminal.desktop','Chat.desktop']"
gsettings set org.gnome.desktop.interface gtk-theme Dark
gsettings set org.gnome.desktop.background picture-uri "file:////usr/share/wallpapers/studio_wallpaper.jpg"
rm /home/tux/.config/autostart/config.desktop   # se auto-remove
```

**Autostart `initMulticortex.sh`** (a cada login):
```bash
cat /etc/multicortex.asc    # logo ASCII
echo "Initializing..."
ollama run llama3.2 "Ola!"  # falha se modelo não instalado
```

### Passo 23: instalar o perfil light

```bash
multicortex-models-light
# equivale a:
ollama pull tinyllama:latest   # ~637 MB
ollama pull phi3:mini          # ~2.2 GB
ollama pull gemma3:1b          # ~815 MB
ollama pull qwen3:0.6b         # ~522 MB
ollama pull smollm2:1.7b       # ~1 GB
```

Para cada modelo, o Ollama: consulta o manifesto em `registry.ollama.ai`, baixa os blobs faltantes, verifica SHA256, cria manifests em `/var/lib/ollama/models/`. Com persistência ativa, os modelos sobrevivem ao reinício.

### Passo 24: modelo respondendo

```bash
ollama run tinyllama "Explique o que é um motherboard em 2 linhas"
```

O Ollama tokeniza o prompt, executa o forward pass pela rede neural e retorna os tokens decodificados. Com `tinyllama` em CPU: alguns segundos. Com GPU NVIDIA: quase instantâneo.

---

## Build manual (sem o script Python)

```bash
su -
zypper refresh
zypper install -y git curl wget xz tar gzip cpio rsync which \
    ca-certificates ca-certificates-mozilla openssl

# Se kiwi-ng não estiver disponível:
zypper ar -f \
    https://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/ \
    kiwi-builder
zypper --gpg-auto-import-keys refresh
zypper install -y python311-kiwi
kiwi-ng --version

mkdir -p ~/builds/out
kiwi-ng --debug system build \
  --description $(pwd)/suse/x86_64/suse-leap-15.6-JeOS \
  --target-dir ~/builds/out \
  2>&1 | tee ~/builds/build.log
```

### Verificar resultado

```bash
find ~/builds/out -name "*.iso" -ls
sha256sum ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso
```

---

## Erros comuns no build

| Erro | Causa | Solução |
|------|-------|---------|
| `baseMount() is obsolete` | Função removida no KIWI 10 | Comentar `baseMount`/`baseCleanMount` no `config.sh` |
| `suseConfig() is obsolete` | Função removida no KIWI 10 | Comentar `suseConfig` |
| `suseRemoveYaST() is obsolete` | Função removida no KIWI 10 | Comentar `suseRemoveYaST` |
| `gconftool-2: No such file or directory` | Scripts legados | Já comentados neste fork |
| Avisos `NOKEY` nos RPMs | GPG não importado | São `warning`, não `ERROR` — build prossegue |
| Conflito drivers NVIDIA | Versões 550/580 misturadas | Manter apenas pacotes G06 da mesma linha |
| Mirror BR falhando | `mirrorcache-br-2` instável | Usar `download.opensuse.org` (já configurado) |

---

## Publicar no GitHub Releases

```bash
command -v gh || zypper install -y gh
gh auth login

TAG="v1.0.5-leap15.6"

gh release create "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork \
  --title "MultiCortex EXO 1.0.5 Live ISO" \
  --notes "ISO Linux Live — openSUSE Leap 15.6 x86_64. GNOME, Ollama, NVIDIA G06, Python 3.12, Node.js 20." \
  --latest

# Atualizar assets de release existente
gh release upload "$TAG" \
  ~/builds/out/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso \
  releases/MultiCortex_EXO_1.0.5.x86_64-1.15.6.iso.sha256 \
  --repo hawkinf/multicortexEXO_fork --clobber
```
