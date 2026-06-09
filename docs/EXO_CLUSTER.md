# EXO — Inferência Distribuída em Cluster

O script `~/bin/exo` presente na ISO aponta para o framework **exo** (`exo-explore/exo`) — um sistema de inferência distribuída P2P que permite rodar modelos LLM grandes dividindo as camadas entre várias máquinas na rede local.

Caso de uso direto: você tem três PCs com 16 GB de RAM cada. Nenhum deles roda `llama3.1:70b` sozinho. Com o exo, os três formam um cluster de 48 GB e o modelo roda distribuído entre eles.

---

## Como funciona

### Particionamento em anel

O exo usa por padrão a estratégia **ring memory weighted partitioning** — particionamento em anel ponderado por memória:

1. Cada nó anuncia quanta memória tem disponível
2. O exo calcula quantas camadas do modelo cabem em cada nó, proporcionalmente
3. Durante a inferência, as ativações passam de nó em nó em sequência

```
Modelo llama3.1:70b — 80 camadas

[  Máquina 1  ] → [  Máquina 2  ] → [  Máquina 3  ]
 camadas 0–27       camadas 28–55      camadas 56–79
  16 GB VRAM          16 GB RAM           8 GB RAM
 NVIDIA RTX          PC comum           Notebook/Pi
 tinygrad CUDA       tinygrad CPU       tinygrad CPU
        └─────────────────────────────────┘
                  retorno em anel
```

O requisito mínimo é que a soma da memória de todos os nós seja suficiente para carregar o modelo inteiro. Para llama3.1:70b em FP16 são necessários ~140 GB; com quantização 4-bit, ~40 GB bastam.

### Descoberta automática

O exo descobre outros dispositivos via **UDP broadcast** — zero configuração manual. Basta que todas as máquinas estejam na mesma rede local. Não há nó master ou worker: todos os dispositivos conectam P2P. Qualquer máquina conectada à rede pode participar do cluster.

### Arquitetura P2P

```
                    rede local
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   [nó 1: exo]     [nó 2: exo]     [nó 3: exo]
   camadas 0–27    camadas 28–55   camadas 56–79
        │               │               │
        └───────────────┴───────────────┘
                        │
              API ChatGPT-compatível
              http://<ip-qualquer>:52415
```

Qualquer nó do cluster expõe a API. Você pode mandar a requisição para qualquer máquina — o cluster processa distribuído internamente.

### API e interface web

O exo expõe dois endpoints ao iniciar:

```
Interface web:    http://<ip>:52415
API de chat:      http://<ip>:52415/v1/chat/completions
```

A API é compatível com o formato da OpenAI — uma mudança de uma linha na aplicação troca a API da nuvem pelo cluster local. Clientes que já usam `OPENAI_BASE_URL` funcionam sem alteração.

---

## Diferença entre exo e Ollama

| Aspecto | Ollama | exo |
|---------|--------|-----|
| Execução | Uma máquina | Cluster de máquinas |
| Propósito | Gerenciar e rodar modelos localmente | Distribuir inferência entre nós |
| Modelos | `ollama pull <modelo>` | Download do Hugging Face em `~/.cache/exo/downloads` |
| API | `127.0.0.1:11434` | `<ip>:52415` (compatível com OpenAI) |
| GPU Linux/NVIDIA | CUDA nativo, estável | Via tinygrad — ver seção de compatibilidade |
| Python | Qualquer | **≥3.12 obrigatório** |
| Descoberta de nós | Não se aplica | UDP broadcast automático |
| Caso de uso | Máquina única com RAM/VRAM suficiente | Várias máquinas fracas somando memória |

Os dois não competem — o Ollama é o backend da ISO para uso normal. O exo entra quando nenhuma máquina individual tem memória suficiente para o modelo desejado.

---

## Compatibilidade NVIDIA no Linux — ponto crítico

O exo foi criado com foco principal em **Apple Silicon (MLX)**. No Linux o backend disponível é o **tinygrad**, que suporta NVIDIA via CUDA. Porém o backend tinygrad foi removido na preparação da versão 1.0 do exo oficial.

**Consequência:** o `pip install exo-inference` do repositório oficial (`exo-explore/exo`) **não funciona com NVIDIA no Linux** na versão atual.

### Fork com suporte NVIDIA restaurado

O fork [`Scottcjn/exo-cuda`](https://github.com/Scottcjn/exo-cuda) restaura o suporte tinygrad/CUDA e foi testado com sucesso em GPUs Tesla V100 e M40.

Requisitos para Linux com NVIDIA:

| Componente | Requisito |
|-----------|-----------|
| SO | Ubuntu 22.04/24.04, Debian 12+, openSUSE Leap 15.6 |
| Python | 3.12 (obrigatório — versões anteriores quebram com asyncio) |
| Driver NVIDIA | 525+ |
| CUDA Toolkit | 12.0+ (`nvcc` disponível) |
| VRAM por nó | 8 GB+ recomendado |

**Atenção para a ISO multicortexEXO:** os drivers NVIDIA G06 estão instalados, mas apenas as libs de runtime — o `nvcc` (compilador CUDA) não está incluso. É necessário instalar o `nvidia-cuda-toolkit` via zypper após o boot antes de usar o exo com GPU.

---

## Instalação na ISO multicortexEXO

### Nó com GPU NVIDIA (Máquina 1)

```bash
# 1. Instalar o compilador CUDA (não incluso nos drivers G06)
sudo zypper install -y nvidia-cuda-toolkit

# Verificar:
nvcc --version
nvidia-smi

# 2. Clonar o fork com suporte NVIDIA
cd ~
git clone https://github.com/Scottcjn/exo-cuda.git exo
cd exo

# 3. Criar virtualenv com Python 3.12 (obrigatório)
python3.12 -m venv .venv
source .venv/bin/activate

# 4. Instalar o exo e atualizar o tinygrad para versão corrigida
pip install -e .
pip install --upgrade git+https://github.com/tinygrad/tinygrad.git

# 5. Verificar instalação
exo --version
```

### Nó sem GPU (CPU only — Máquinas 2, 3...)

```bash
# Sem necessidade de CUDA
cd ~
git clone https://github.com/Scottcjn/exo-cuda.git exo
cd exo
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Usando o script wrapper da ISO

Após a instalação, o script `~/bin/exo` já funciona corretamente:

```bash
# ~/bin/exo contém:
# cd ~/exo
# source .venv/bin/activate
# exo

# Executar:
~/bin/exo
```

---

## Iniciando o cluster

### Em cada máquina

```bash
cd ~/exo
source .venv/bin/activate

# Nó com GPU NVIDIA:
exo --inference-engine tinygrad --chatgpt-api-port 52415 --disable-tui

# Nó CPU only (tinygrad detecta automaticamente):
exo --chatgpt-api-port 52415 --disable-tui
```

O `--disable-tui` evita problemas de terminal no GNOME Terminal. Sem ele, o exo tenta exibir uma interface interativa que pode travar dependendo do emulador de terminal.

Ao iniciar, cada nó imprime algo como:

```
Node ID: abc123
Starting exo...
Peer discovery: UDP broadcast
Chat interface started:
  http://192.168.1.10:52415
ChatGPT API endpoint:
  http://192.168.1.10:52415/v1/chat/completions
```

Os nós se descobrem automaticamente em alguns segundos. Não é necessário informar o IP dos outros nós.

### Verificar que os nós se encontraram

```bash
curl http://127.0.0.1:52415/v1/models
```

A resposta deve listar os modelos disponíveis no cluster.

---

## Baixar modelos para o cluster

O exo baixa modelos do Hugging Face, não do registro do Ollama. Os modelos ficam em `~/.cache/exo/downloads/`.

```bash
# Via interface web: acesse http://<ip>:52415 e selecione o modelo

# Via API (dispara o download automaticamente ao primeiro uso):
curl http://127.0.0.1:52415/v1/chat/completions \
  -d '{"model": "llama-3.1-8b", "messages": [{"role": "user", "content": "Oi"}]}'

# Os modelos precisam estar em todos os nós que vão processar os shards correspondentes.
# O exo baixa automaticamente a parte que cada nó precisa.
```

### Modelos suportados pelo exo

| Família | Exemplos |
|---------|---------|
| LLaMA | llama-3.1-8b, llama-3.1-70b, llama-3.2-3b |
| Mistral | mistral-7b |
| LLaVA | llava-1.5-7b (multimodal) |
| Qwen | qwen-2.5-7b |
| DeepSeek | deepseek-r1-7b |

Identificadores no formato `llama-3.1-8b` (hífens, sem dois pontos) — diferente do formato do Ollama (`llama3.1:8b`).

### Onde os modelos ficam

```
~/.cache/exo/downloads/
└── [nome-do-modelo]/
    ├── config.json
    ├── tokenizer.json
    └── model-*.safetensors    ← pesos — podem ser vários GBs
```

Para mudar o diretório de armazenamento:

```bash
export EXO_HOME=/mnt/ssd-externo/exo
exo --chatgpt-api-port 52415 --disable-tui
```

Útil para uso offline: baixar os modelos numa máquina com internet, copiar a pasta para um SSD e usar `EXO_HOME` apontando para o SSD em campo.

---

## Usando a API

### Chat

```bash
curl http://192.168.1.10:52415/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-8b",
    "messages": [
      {"role": "system", "content": "Você é um assistente técnico de TI."},
      {"role": "user",   "content": "O que pode causar superaquecimento num notebook?"}
    ],
    "stream": false
  }'
```

### Trocar da API OpenAI para o cluster exo

Em qualquer aplicação que usa a SDK da OpenAI:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://192.168.1.10:52415/v1",
    api_key="não-necessário"
)

response = client.chat.completions.create(
    model="llama-3.1-8b",
    messages=[{"role": "user", "content": "Olá!"}]
)
print(response.choices[0].message.content)
```

Uma linha muda (`base_url`) — o resto do código não precisa de alteração.

---

## Configuração recomendada para a ISO

### Cluster mínimo para modelos grandes

Para rodar `llama-3.1-70b` com quantização 4-bit (~40 GB):

| Máquina | Papel | Memória | GPU |
|---------|-------|---------|-----|
| Máquina 1 (ISO multicortexEXO) | nó principal | 16 GB VRAM | NVIDIA RTX |
| Máquina 2 | nó secundário | 16 GB RAM | CPU |
| Máquina 3 | nó auxiliar | 8 GB RAM | CPU |

Todos na mesma rede local (switch, não Wi-Fi — latência importa).

### Cluster para modelos médios (7–8B)

Uma única máquina com 16 GB RAM é suficiente para modelos 7B em CPU com o exo. Neste caso o exo não distribui — roda como nó único. O Ollama é mais prático para esse cenário.

### Quando usar exo vs Ollama

Use o **Ollama** quando:
- A máquina tem RAM/VRAM suficiente para o modelo
- Você quer simplicidade — `ollama run modelo`
- Precisa de estabilidade em produção

Use o **exo** quando:
- Nenhuma máquina individual tem memória suficiente
- Você tem várias máquinas disponíveis na mesma rede
- Quer usar hardware heterogêneo (misturar GPU e CPU)
- Precisa da API compatível com OpenAI para integração em aplicações

---

## Variáveis de ambiente

| Variável | Padrão | Uso |
|----------|--------|-----|
| `EXO_HOME` | `~/.cache/exo` | Diretório de modelos |
| `HF_ENDPOINT` | `https://huggingface.co` | Mirror do Hugging Face |
| `DEBUG` | `0` | Nível de log (0–9) |
| `TINYGRAD_DEBUG` | `0` | Log do backend tinygrad (1–6) |
| `CLANG=1` | — | Força CPU no tinygrad (desativa GPU) |

---

## Diagnóstico

### Verificar que o nó está rodando

```bash
curl http://127.0.0.1:52415/v1/models
```

### Ver logs em tempo real

```bash
DEBUG=2 exo --inference-engine tinygrad --chatgpt-api-port 52415 --disable-tui
```

### GPU não está sendo usada

```bash
# Verificar se CUDA está disponível para o tinygrad:
python3.12 -c "import tinygrad; from tinygrad.runtime.ops_cuda import CUDADevice; print('CUDA OK')"

# Se falhar: nvcc não instalado ou driver desatualizado
nvcc --version
nvidia-smi
```

### Nós não se descobrem

- Confirmar que todas as máquinas estão na mesma rede (não VLANs separadas)
- Confirmar que UDP broadcast não está bloqueado pelo firewall
- Testar conectividade: `ping <ip-do-outro-nó>`
- Verificar se a porta 52415 está aberta: `ss -tulpn | grep 52415`

### Download de modelo travado

```bash
# Definir mirror se huggingface.co estiver inacessível:
export HF_ENDPOINT=https://hf-mirror.com
exo --chatgpt-api-port 52415 --disable-tui
```

---

## Estado atual e limitações conhecidas

| Item | Status |
|------|--------|
| Suporte Apple Silicon (MLX) | Estável — foco principal do projeto |
| Suporte Linux CPU (tinygrad) | Funcional com limitações de velocidade |
| Suporte Linux NVIDIA (tinygrad CUDA) | Removido do v1 oficial — usar fork `exo-cuda` |
| Suporte AMD (ROCm) | Experimental |
| Windows | Não suportado oficialmente |
| Raspberry Pi (ARM CPU) | Funcional via tinygrad CPU |
| Velocidade no Linux vs Apple Silicon | 3–5x mais lento no tinygrad CPU vs MLX |

O projeto está em desenvolvimento ativo. O suporte NVIDIA para Linux é a principal limitação para o caso de uso da ISO multicortexEXO. Acompanhar o issue [#1039](https://github.com/exo-explore/exo/issues/1039) no repositório oficial para atualizações.

---

## Referências

- Repositório oficial: https://github.com/exo-explore/exo
- Fork com suporte NVIDIA: https://github.com/Scottcjn/exo-cuda
- Issue de suporte NVIDIA: https://github.com/exo-explore/exo/issues/1039
- Documentação tinygrad: https://github.com/tinygrad/tinygrad
