#!/usr/bin/env bash
set -Eeuo pipefail

run() {
  echo
  echo ">>> $*"
  "$@"
  echo
  read -r -p "Enter para voltar ao menu..."
}

service_cmd() {
  local action="$1"
  local svc="$2"
  if command -v systemctl >/dev/null 2>&1; then
    sudo systemctl "$action" "$svc" || systemctl "$action" "$svc" || true
  else
    echo "systemctl não disponível."
  fi
}

show_urls() {
  echo "URLs locais:"
  echo "  Ollama API:       http://127.0.0.1:11434"
  echo "  Tags:             http://127.0.0.1:11434/api/tags"
  echo "  Web UI local:     http://127.0.0.1:3000"
  echo "  Open WebUI:       http://127.0.0.1:8080"
  echo
  echo "IPs da máquina:"
  ip -4 addr show scope global 2>/dev/null | awk '/inet / {print "  " $2 "  " $NF}' || hostname -I || true
}

test_api() {
  curl -fsS http://127.0.0.1:11434/api/tags || true
  echo
}

while true; do
  clear
  cat <<'MENU'
============================================================
 MultiCortex EXO - Menu de Controle
============================================================

 1. Ver status
 2. Iniciar Ollama
 3. Parar Ollama
 4. Reiniciar Ollama
 5. Iniciar Web UI
 6. Parar Web UI
 7. Reiniciar Web UI
 8. Listar modelos
 9. Instalar modelos leves
10. Instalar modelos médios
11. Instalar modelos de código
12. Instalar modelos grandes
13. Testar API
14. Mostrar IPs e URLs
15. Sair

MENU
  read -r -p "Escolha: " opt
  case "$opt" in
    1) run multicortex-status ;;
    2) service_cmd start ollama.service; read -r -p "Enter..." ;;
    3) service_cmd stop ollama.service; read -r -p "Enter..." ;;
    4) service_cmd restart ollama.service; read -r -p "Enter..." ;;
    5) service_cmd start multicortex-chat-ui.service; service_cmd start open-webui.service; read -r -p "Enter..." ;;
    6) service_cmd stop multicortex-chat-ui.service; service_cmd stop open-webui.service; read -r -p "Enter..." ;;
    7) service_cmd restart multicortex-chat-ui.service; service_cmd restart open-webui.service; read -r -p "Enter..." ;;
    8) run multicortex-models-list ;;
    9) run multicortex-models-light ;;
    10) run multicortex-models-medium ;;
    11) run multicortex-models-code ;;
    12) run multicortex-models-large ;;
    13) run test_api ;;
    14) run show_urls ;;
    15) exit 0 ;;
    *) echo "Opção inválida."; sleep 1 ;;
  esac
done
