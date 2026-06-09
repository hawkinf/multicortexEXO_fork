# Build da ISO MultiCortex EXO

## Diretório do projeto

```bash
cd /home/hawk/multicortexEXO_fork
```

## Instalar dependências no openSUSE

```bash
bash scripts/build/install-build-deps-opensuse.sh
```

## Diagnóstico

```bash
bash scripts/build/check-build-env.sh
```

## Limpar build anterior

```bash
bash scripts/build/clean-build.sh
```

## Gerar ISO

```bash
bash scripts/build/build-iso.sh
```

## Conferir resultado

```bash
bash scripts/build/check-result.sh
```

A saída padrão fica em:

```text
/home/hawk/builds/out
```

Os logs ficam em:

```text
/home/hawk/builds/logs
```

## Build direto, sem script

```bash
kiwi-ng --debug system build \
  --description /home/hawk/multicortexEXO_fork/suse/x86_64/suse-leap-15.6-JeOS \
  --target-dir /home/hawk/builds/out
```

## O que não commitar

Não commite arquivos `.iso`, `.raw`, `.qcow2`, `.img`, modelos baixados, chaves, tokens ou `.env`.
