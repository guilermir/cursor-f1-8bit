# 🏎️ Cursor F1 8-bit

Um overlay divertido para **Windows** em Python que coloca um carrinho de Fórmula 1 em *pixel art* seguindo o cursor do mouse pela tela (incluindo múltiplos monitores), girando de acordo com o movimento, emitindo fumaça e ativando uma chama de turbo ao segurar o botão esquerdo do mouse.

> **Sem dependências externas:** utiliza apenas a biblioteca padrão do Python (`tkinter`, `ctypes`, `math` e `random`).

## ✨ Funcionalidades

- **Movimento suave e direção:** o carrinho acompanha o cursor com *drag* configurável e rotaciona conforme a direção do deslocamento.
- **Modo Turbo:** ao segurar o botão esquerdo do mouse, a velocidade de perseguição aumenta e uma chama em *pixel art* surge na traseira.
- **Fumaça opcional:** pode ser ativada ou desativada via configuração no código.
- **Janela "fantasma" transparente:** fica sempre no topo (`topmost`) sem bloquear os cliques nos programas que estão por baixo.
- **Suporte a multi-monitor e escala DPI:** calcula a área virtual combinada de monitores e ajusta coordenadas em telas com zoom/DPI.

## 🚀 Como executar

1. Certifique-se de ter o **Python 3** instalado no **Windows**.
2. Baixe ou clone este repositório.
3. Execute o script pelo terminal ou abra no **VS Code** e pressione **F5**:

```bash
python cursor_f1_8bit.py
```

### Como sair
- Pressione **`Ctrl` + `Alt` + `Q`** a qualquer momento, ou
- Use **`Ctrl` + `C`** no terminal.

## ⚙️ Configurações

No topo do arquivo `cursor_f1_8bit.py`, você pode ajustar parâmetros como:

| Variável | Descrição | Valor padrão |
| :--- | :--- | :--- |
| `TAMANHO` | Escala do sprite (`1.0` = original 28×52 px) | `0.50` |
| `DIRECOES` | Quantidade de ângulos pré-renderizados | `16` |
| `FUMACA` | Ativa (`True`) ou desativa (`False`) o rastro de fumaça | `False` |
| `PIXEL_FX` | Tamanho dos blocos de *pixel art* da fumaça e chama | `2` |
| `SEGUIR` | Suavidade/arrasto normal (`0.0` a `1.0`) | `0.14` |
| `SEGUIR_TURBO` | Suavidade/arrasto com o botão esquerdo pressionado | `0.30` |
| `INTERVALO_MS` | Intervalo entre quadros em milissegundos (~60 FPS) | `16` |

## ⚠️ Compatibilidade

Este script utiliza chamadas da API do Windows via `ctypes` (`user32`, `shcore` e estilos estendidos de janela), portanto foi feito especificamente para **Windows**.
