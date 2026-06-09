#!/usr/bin/env bash
set -Eeuo pipefail

TITLE="MultiCortex EXO Status"
VERSION_FILE="/etc/multicortex-version"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"

section() {
  printf '\n\033[1;36m## %s\033[0m\n' "$*"
}

cmd_or_na() {
  local label="$1"
  shift
  printf '%-28s ' "$label"
  "$@" 2>/dev/null || printf 'N/A\n'
}

echo "============================================================"
echo "$TITLE"
echo "============================================================"

section "Versão"
if [[ -f "$VERSION_FILE" ]]; then
  cat "$VERSION_FILE"
elif [[ -f "./VERSION" ]]; then
  cat "./VERSION"
else
  echo "Versão não encontrada"
fi

section "Sistema"
cmd_or_na "Hostname:" hostname
cmd_or_na "Kernel:" uname -r
cmd_or_na "Arquitetura:" uname -m
if [[ -f /etc/os-release ]]; then
  grep -E '^(PRETTY_NAME|VERSION_ID)=' /etc/os-release | sed 's/^/  /'
fi

section "Rede"
if command -v ip >/dev/null 2>&1; then
  ip -4 addr show scope global | awk '/inet / {print "  " $2 "  " $NF}'
else
  hostname -I 2>/dev/null || true
fi

echo
echo "URLs prováveis:"
echo "  Ollama API:       ${OLLAMA_BASE_URL}"
echo "  Ollama tags:      ${OLLAMA_BASE_URL}/api/tags"
echo "  Web UI local:     http://127.0.0.1:3000"
echo "  Open WebUI:       http://127.0.0.1:8080"

section "Serviços"
if command -v systemctl >/dev/null 2>&1; then
  for svc in ollama.service multicortex-chat-ui.service open-webui.service; do
    printf '%-30s ' "$svc"
    systemctl is-active "$svc" 2>/dev/null || true
  done
else
  echo "systemctl indisponível"
fi

section "Ollama API"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS "${OLLAMA_BASE_URL}/api/tags" >/tmp/multicortex-tags.json 2>/dev/null; then
    echo "OK: ${OLLAMA_BASE_URL}/api/tags respondeu."
    if command -v jq >/dev/null 2>&1; then
      jq -r '.models[]?.name // empty' /tmp/multicortex-tags.json | sed 's/^/  - /' || true
    else
      cat /tmp/multicortex-tags.json
      echo
    fi
  else
    echo "Falhou: API não respondeu em ${OLLAMA_BASE_URL}."
  fi
else
  echo "curl não instalado"
fi

section "Modelos via ollama list"
if command -v ollama >/dev/null 2>&1; then
  ollama list || true
else
  echo "ollama não instalado"
fi

section "Hardware"
cmd_or_na "CPU:" bash -c "lscpu | awk -F: '/Model name/ {gsub(/^[ \t]+/,\"\",\$2); print \$2; exit}'"
cmd_or_na "RAM:" free -h
cmd_or_na "Disco:" df -h /
if command -v nvidia-smi >/dev/null 2>&1; then
  echo
  echo "NVIDIA:"
  nvidia-smi || true
else
  echo
  echo "NVIDIA: nvidia-smi não encontrado"
fi

section "Logs recentes"
if command -v journalctl >/dev/null 2>&1; then
  journalctl -u ollama.service -n 20 --no-pager 2>/dev/null || true
else
  echo "journalctl indisponível"
fi
