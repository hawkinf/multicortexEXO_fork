#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador COMPLETO da ISO MultiCortex EXO para openSUSE Leap 15.6.

Compatível com Python antigo do openSUSE, inclusive Python 3.6.
Mantém o pacote completo, incluindo NVIDIA/proprietários.

Uso como root:
    python3 gerar_iso_multicortex_completo_py36.py

Uso limpando tudo:
    python3 gerar_iso_multicortex_completo_py36.py --clean

ISO esperada em:
    /home/hawk/builds/out/
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


MULTICORTEX_REPO = "https://github.com/cabelo/multicortex-exo.git"
KIWI_DESC_RELATIVE = "suse/x86_64/suse-leap-15.6-JeOS"
KIWI_BUILDER_REPO = (
    "https://download.opensuse.org/repositories/"
    "Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/"
)


def run(cmd, cwd=None, check=True):
    print("\n>>> " + " ".join(cmd))
    sys.stdout.flush()
    return subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=check)


def run_capture(cmd, cwd=None, check=False):
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        universal_newlines=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def is_root():
    return hasattr(os, "geteuid") and os.geteuid() == 0


def default_workdir():
    if Path("/home/hawk").exists():
        return Path("/home/hawk/builds")
    return Path.home() / "builds"


def read_os_release():
    data = {}
    p = Path("/etc/os-release")
    if not p.exists():
        return data
    for line in p.read_text(errors="ignore").splitlines():
        if "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k] = v.strip().strip('"')
    return data


def ensure_host_packages():
    print("\n=== Atualizando repositórios do host ===")
    run(["zypper", "--gpg-auto-import-keys", "refresh"])

    pkgs = [
        "git",
        "python3",
        "python3-pip",
        "python3-kiwi",
        "curl",
        "wget",
        "nano",
        "xz",
        "tar",
        "gzip",
        "cpio",
        "rsync",
        "which",
        "ca-certificates",
        "ca-certificates-mozilla",
        "openssl",
    ]

    print("\n=== Instalando ferramentas no host ===")
    result = run_capture(["zypper", "install", "-y"] + pkgs)
    print(result.stdout)

    if result.returncode != 0 or shutil.which("kiwi-ng") is None:
        print("\npython3-kiwi não instalou pelos repositórios atuais. Adicionando KIWI Builder...")
        run(["zypper", "ar", "-f", KIWI_BUILDER_REPO, "kiwi-builder"], check=False)
        run(["zypper", "--gpg-auto-import-keys", "refresh"])
        run(["zypper", "install", "-y"] + pkgs)

    run(["kiwi-ng", "--version"])


def clone_or_update(workdir):
    repo_dir = workdir / "multicortex-exo"

    if repo_dir.exists() and (repo_dir / ".git").exists():
        print("\n=== Atualizando repositório existente ===")
        run(["git", "pull", "--ff-only"], cwd=repo_dir)
    elif repo_dir.exists():
        raise RuntimeError("A pasta %s existe, mas não é um repositório git." % repo_dir)
    else:
        print("\n=== Clonando MultiCortex EXO ===")
        run(["git", "clone", MULTICORTEX_REPO, str(repo_dir)])

    desc = repo_dir / KIWI_DESC_RELATIVE
    if not desc.exists():
        raise RuntimeError("Descritor KIWI não encontrado: %s" % desc)

    return repo_dir


def copy_kiwi_descriptor(repo_dir, workdir):
    src = repo_dir / KIWI_DESC_RELATIVE
    dst = workdir / "kiwi-desc"

    print("\n=== Copiando descritor KIWI ===")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(str(src), str(dst), symlinks=True)

    if not (dst / "config.xml").exists():
        raise RuntimeError("config.xml não encontrado na cópia do descritor KIWI.")

    return dst


def add_package_to_bootstrap(xml, package):
    if ("name=\"%s\"" % package) in xml or ("name='%s'" % package) in xml:
        return xml

    pattern = re.compile(
        r"(<packages\s+type=[\"']bootstrap[\"'][^>]*>)(.*?)(\n\s*</packages>)",
        re.DOTALL,
    )

    def repl(match):
        start, body, end = match.group(1), match.group(2), match.group(3)
        insertion = "\n        <package name='%s'/>" % package
        return start + body + insertion + end

    new_xml, count = pattern.subn(repl, xml, count=1)
    if count == 0:
        raise RuntimeError('Não encontrei o bloco <packages type="bootstrap"> no config.xml.')

    return new_xml


def add_repository_before_packages(xml, repo_xml, unique_text):
    if unique_text in xml:
        return xml
    return xml.replace('    <packages type="image"', repo_xml + '\n    <packages type="image"')


def patch_config_xml(kiwi_desc):
    config_xml = kiwi_desc / "config.xml"
    s = config_xml.read_text(errors="ignore")

    print("\n=== Ajustando config.xml para build COMPLETO com NVIDIA ===")

    replacements = {
        '<source path="obs://Virtualization:Appliances:Builder/openSUSE_Leap_15.6"/>':
        '<source path="http://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/"/>',

        "https://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/":
        "http://download.opensuse.org/repositories/Virtualization:/Appliances:/Builder/openSUSE_Leap_15.6/",

        "https://download.opensuse.org/distribution/leap/15.6/repo/oss/":
        "http://download.opensuse.org/distribution/leap/15.6/repo/oss/",

        "https://download.opensuse.org/update/leap/15.6/oss/":
        "http://download.opensuse.org/update/leap/15.6/oss/",

        "https://download.opensuse.org/distribution/leap/15.6/repo/non-oss/":
        "http://download.opensuse.org/distribution/leap/15.6/repo/non-oss/",

        "https://download.opensuse.org/update/leap/15.6/non-oss/":
        "http://download.opensuse.org/update/leap/15.6/non-oss/",

        "https://download.opensuse.org/repositories/home:/cabelo:/jax/15.6/":
        "http://download.opensuse.org/repositories/home:/cabelo:/jax/15.6/",

        "https://download.opensuse.org/repositories/home:/cabelo:/innovators/15.6/":
        "http://download.opensuse.org/repositories/home:/cabelo:/innovators/15.6/",
    }

    for old, new in replacements.items():
        s = s.replace(old, new)

    non_oss_repos = """
    <repository type='rpm-md'>
        <source path='http://download.opensuse.org/distribution/leap/15.6/repo/non-oss/'/>
    </repository>
    <repository type='rpm-md'>
        <source path='http://download.opensuse.org/update/leap/15.6/non-oss/'/>
    </repository>
"""
    s = add_repository_before_packages(s, non_oss_repos, "distribution/leap/15.6/repo/non-oss")

    nvidia_repo = """
    <repository type='rpm-md'>
        <source path='https://download.nvidia.com/opensuse/leap/15.6/'/>
    </repository>
"""
    s = add_repository_before_packages(s, nvidia_repo, "download.nvidia.com/opensuse/leap/15.6")

    # Corrige erro de certificado dentro do rootfs/chroot do KIWI.
    s = add_package_to_bootstrap(s, "ca-certificates-mozilla")
    s = add_package_to_bootstrap(s, "openssl")

    image_packages_match = re.search(
        r"(<packages\s+type=[\"']image[\"'][^>]*>)(.*?)(\n\s*</packages>)",
        s,
        flags=re.DOTALL,
    )
    if not image_packages_match:
        raise RuntimeError('Não encontrei o bloco <packages type="image">.')

    required_nvidia = [
        "nvidia-common-G06",
        "nvidia-compute-G06",
        "nvidia-compute-utils-G06",
        "nvidia-utils-G06",
        "nvidia-driver-G06-kmp-default",
    ]

    for pkg in required_nvidia:
        if ("name='%s'" % pkg) not in s and ('name="%s"' % pkg) not in s:
            s = s.replace(
                image_packages_match.group(1),
                image_packages_match.group(1) + "\n        <package name='%s'/>" % pkg,
                1,
            )

    config_xml.write_text(s)

    # Compatibilidade com KIWI 10.x: funções antigas do config.sh.
    config_sh = kiwi_desc / "config.sh"
    if config_sh.exists():
        c = config_sh.read_text(errors="ignore")
        c = c.replace("baseMount\\n", "# baseMount removido: KIWI 10 já gerencia mounts\\n")
        c = c.replace("baseCleanMount\\n", "# baseCleanMount removido: KIWI 10 já gerencia mounts\\n")
        config_sh.write_text(c)
        print("config.sh ajustado para KIWI 10.x")

    print("\nPacotes NVIDIA mantidos/garantidos:")
    for pkg in required_nvidia:
        print(" - " + pkg)

    print("\nRepositórios do config.xml:")
    for n, line in enumerate(s.splitlines(), start=1):
        if "source path" in line:
            print("%s: %s" % (n, line.strip()))

    print("\nPacotes bootstrap importantes:")
    for pkg in ["ca-certificates", "ca-certificates-mozilla", "openssl"]:
        print(" - %s: %s" % (pkg, "OK" if pkg in s else "AUSENTE"))


def build_iso(workdir, kiwi_desc):
    out_dir = workdir / "out"
    log_file = workdir / "build-multicortex.log"

    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== Iniciando build COMPLETO da ISO ===")
    print("Descritor: %s" % kiwi_desc)
    print("Saída:     %s" % out_dir)
    print("Log:       %s" % log_file)

    cmd = [
        "kiwi-ng",
        "--debug",
        "system",
        "build",
        "--description",
        str(kiwi_desc),
        "--target-dir",
        str(out_dir),
    ]

    with log_file.open("w", encoding="utf-8", errors="replace") as log:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
        )

        for line in proc.stdout:
            print(line, end="")
            log.write(line)

        code = proc.wait()

    if code != 0:
        print("\nERRO: build falhou.")
        print("Veja o final do log com:")
        print("  tail -150 %s" % log_file)
        raise SystemExit(code)

    iso_files = sorted(out_dir.glob("*.iso"))
    if not iso_files:
        print("\nBuild terminou, mas não encontrei .iso em: %s" % out_dir)
        print("Arquivos encontrados:")
        for p in sorted(out_dir.iterdir()):
            print(" - " + p.name)
        raise SystemExit(2)

    print("\n=== ISO gerada com sucesso ===")
    for iso in iso_files:
        gib = iso.stat().st_size / (1024.0 ** 3)
        print(" - %s (%.2f GiB)" % (iso, gib))


def main():
    parser = argparse.ArgumentParser(description="Gera a ISO completa do MultiCortex EXO com NVIDIA.")
    parser.add_argument("--workdir", default=str(default_workdir()), help="Pasta de trabalho. Padrão: /home/hawk/builds se existir.")
    parser.add_argument("--clean", action="store_true", help="Apaga a pasta de trabalho antes de começar.")
    parser.add_argument("--no-install", action="store_true", help="Não instala pacotes no host; assume que tudo já está instalado.")
    args = parser.parse_args()

    if not is_root():
        print("ERRO: rode como root.")
        print("Exemplo:")
        print("  su -")
        print("  python3 /home/hawk/gerar_iso_multicortex_completo_py36.py")
        sys.exit(1)

    osr = read_os_release()
    print("Sistema detectado:")
    print("  NAME=%s" % osr.get("NAME", "?"))
    print("  VERSION_ID=%s" % osr.get("VERSION_ID", "?"))

    if osr.get("VERSION_ID") != "15.6":
        print("\nAVISO: recomendado openSUSE Leap 15.6 para este projeto.")

    workdir = Path(args.workdir).expanduser().resolve()

    if args.clean and workdir.exists():
        print("\n=== Limpando %s ===" % workdir)
        shutil.rmtree(str(workdir))

    workdir.mkdir(parents=True, exist_ok=True)

    if not args.no_install:
        ensure_host_packages()
    else:
        run(["kiwi-ng", "--version"])

    repo_dir = clone_or_update(workdir)
    kiwi_desc = copy_kiwi_descriptor(repo_dir, workdir)
    patch_config_xml(kiwi_desc)
    build_iso(workdir, kiwi_desc)


if __name__ == "__main__":
    main()
