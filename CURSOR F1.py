"""
Cursor F1 8-bit  (Windows)

Um carrinho de F1 em pixel art segue o mouse por toda a tela, vira conforme a
direcao, solta fumaca e ganha chama de turbo quando voce segura o botao esquerdo.

Como rodar: abra no VS Code e aperte F5  (ou: python cursor_f1_8bit.py)
Como sair:  Ctrl + Alt + Q  (ou Ctrl+C no terminal)
Nao precisa instalar nada alem do Python.
"""
import ctypes
import math
import random
import tkinter as tk

# ---------------- configuracoes ----------------
TAMANHO = 0.50         # tamanho do carro: 1.0 = desenho original (28x52 px), 0.5 = metade, 0.35 = bem pequeno
DIRECOES = 16         # em quantos angulos o carro pode apontar
FUMACA = False         # False = sem fumaca saindo do carro
PIXEL_FX = 2          # tamanho dos quadradinhos da fumaca e da chama
SEGUIR = 0.14         # quanto o carro "arrasta" atras do mouse (0 a 1)
SEGUIR_TURBO = 0.30   # idem, com o botao esquerdo pressionado
INTERVALO_MS = 16     # ~60 quadros por segundo
FUNDO = "#010101"     # cor que vira transparente (nao use no carro)

# ---------------- sprite (28x52), carro olhando para CIMA ----------------
SPRITE = [
    "............DBBG............",
    ".........GBBFKKFBBE.........",
    "......GBBEKKFFFFKKKBBD......",
    "..IAABEKJJJHCCFCHKJJKFBBBI..",
    "LAEJJJJJJKGBEJJEBFKJJJJJKKAL",
    "LBKJJJJHGIIAEJJGAILGKJJJJJBL",
    "LBKJJKGILIIIEJJGIIDLIGKKJJBL",
    "LBKFFG.IAL.CFJJFC..AI.GFFHBL",
    "LBGBGDAI..ICKJJJCI..IACGBGBL",
    "LBCAB.....IEKKKKEI.....DABAL",
    "LAAL......IELLLKEI......LAAL",
    "..LL......IEKLLKEI.......L..",
    ".DAAAAA..IAGJJJJGAD..AAAAAD.",
    "LADDDDDI.DAGJJKJEAD.IADDDDAL",
    "LADIIIDAAAAEJEEHEAAAADIIIIAL",
    "LAIIIIIADDAEJKKKEADDADIIIIAL",
    "LAIIIIIAAAAEHEEHEAAAADIIIIAL",
    "LADDDDDADDAEJJJJEADDAADDDDAL",
    "LADDDDDAAABFKFFKFBAAAADDDDAL",
    ".DDAAAD.LACKCCCCKCAL.AAAAAD.",
    "..AAAAL.LAKGBCDBGFB..LAAAA..",
    "........IEKCAAAACKGI........",
    "......LIDGGAAAAAAGKDD.......",
    "....DDBDGGCAAAAAACGGDAAD....",
    "...GCGGGKGBBAAAABCCKGGGCD...",
    "..LBGJJKHFEEAAAAEEEKHKJGBI..",
    "..LBHJJHKFEEAAAAEEEKKJJHBI..",
    "..LBHJJHKFEEAAAAEEEKFJJHBI..",
    "..LBKKJJKFEHBAABHEEKKJKKBI..",
    "..LBLLKKHFEJKCCKJEEJKKLLBI..",
    "..LB.LLJJFEJKKKJJEEJJKL.BI..",
    "..LAGLLJJFEJECCEJEEJJKLEAI..",
    "..LACGKKJFEKFKKFKEEKKKGCAI..",
    "..LADBCEKHFFFJJFFFFKCCCIAI..",
    "...DDDECCHHFGJJFEHHBCEDDD...",
    "....DDDABHHEFJJFFHHBBDDD....",
    ".....DAABFHKEKKEKHFBAAD.....",
    "......DABFHJECFEJHFBAD......",
    "...IIIDABFHJECGEJHFBADIII...",
    "..IAAAAAAEFJECGEJHFAAAAAAA..",
    ".DADDDAAABEHHFGHFGBAAADDDDD.",
    "LAIIIIDAAABGFFFFEBBAADIIIIAL",
    "LAIIIIIAAAABFFHFBAAAADIIIIAL",
    "LAIIIIDAAAAAEFFCAAAAADIIIIAL",
    "LADDDDDAAAAABCCBAABBADDDDDAL",
    "LADDDDDACGBBGGGGCBGBAADDDDAL",
    "LADDDDBBBHFFHHHHFFKBBCDDDDAL",
    ".DAAAACECJHHHHHHJHJCCGAAAAD.",
    ".....BBECKHHHHHFFFKBCEA.....",
    ".....LBEACCCCCCCCCCBCEL.....",
    ".....LAGIIIIIIIIIIIIGBI.....",
    "......L....................."
]
PALETA = {
    "A": "#0f0c0f",
    "B": "#330f07",
    "C": "#592415",
    "D": "#393744",
    "E": "#7e341a",
    "F": "#aa4722",
    "G": "#914f37",
    "H": "#c8511f",
    "I": "#6e6b77",
    "J": "#e86425",
    "K": "#d16d39",
    "L": "#0f0c0f"
}
FRENTE = -math.pi / 2  # o desenho aponta para CIMA
LARG, ALT = len(SPRITE[0]), len(SPRITE)
RGB = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in PALETA.items()}


def renderizar(ang, tam=TAMANHO, ss=3):
    """Gira e reduz o sprite para o angulo `ang`.
    Devolve (lado, matriz de cores '#rrggbb' ou None para transparente)."""
    lado = int(math.ceil(math.hypot(LARG, ALT) * tam)) + 2
    if lado % 2:
        lado += 1
    fi = ang - FRENTE
    c, s = math.cos(fi), math.sin(fi)
    mat = []
    for j in range(lado):
        linha = []
        for i in range(lado):
            r = g = b = n = 0
            for a in range(ss):
                for e in range(ss):
                    u = (i + (a + 0.5) / ss - lado / 2) / tam
                    v = (j + (e + 0.5) / ss - lado / 2) / tam
                    sx = u * c + v * s
                    sy = -u * s + v * c
                    col = math.floor(sx + LARG / 2)
                    lin = math.floor(sy + ALT / 2)
                    if 0 <= col < LARG and 0 <= lin < ALT:
                        ch = SPRITE[lin][col]
                        if ch != ".":
                            cr, cg, cb = RGB[ch]
                            r += cr
                            g += cg
                            b += cb
                            n += 1
            if n * 2 >= ss * ss:  # pelo menos metade do pixel coberto
                linha.append("#%02x%02x%02x" % (r // n, g // n, b // n))
            else:
                linha.append(None)
        mat.append(linha)
    return lado, mat


def para_imagem(lado, mat):
    img = tk.PhotoImage(width=lado, height=lado)
    linhas = ["{" + " ".join(cor or FUNDO for cor in lin) + "}" for lin in mat]
    img.put(" ".join(linhas))
    return img


CORES_FUMACA = ["#f2f2f2", "#c4c4c4", "#8c8c8c", "#585858"]
CORES_CHAMA = ["#ffd400", "#ff8a00", "#e10600"]

# ---------------- Windows: mouse global e janela transparente ----------------
user32 = ctypes.windll.user32
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # coordenadas reais em telas com zoom
except Exception:
    user32.SetProcessDPIAware()


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def posicao_mouse():
    p = POINT()
    user32.GetCursorPos(ctypes.byref(p))
    return p.x, p.y


def tecla(vk):
    return user32.GetAsyncKeyState(vk) & 0x8000 != 0


# area de todos os monitores juntos
vx, vy = user32.GetSystemMetrics(76), user32.GetSystemMetrics(77)
vw, vh = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

root = tk.Tk()
root.title("Cursor F1")
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-transparentcolor", FUNDO)
root.geometry(f"{vw}x{vh}{vx:+d}{vy:+d}")
cv = tk.Canvas(root, width=vw, height=vh, bg=FUNDO, highlightthickness=0)
cv.pack()
root.update()

# deixa a janela "fantasma": cliques passam direto para os outros programas
hwnd = user32.GetParent(root.winfo_id()) or root.winfo_id()
estilo = user32.GetWindowLongW(hwnd, -20)
user32.SetWindowLongW(hwnd, -20, estilo | 0x80000 | 0x20 | 0x80)

# pre-calcula o carro em todas as direcoes
IMAGENS = [para_imagem(*renderizar(k * 2 * math.pi / DIRECOES)) for k in range(DIRECOES)]

# ---------------- animacao ----------------
mx0, my0 = posicao_mouse()
x, y = mx0 - vx, my0 - vy
ang = 0.0
fumaca = []  # cada item: [x, y, idade]
F = PIXEL_FX
META = ALT * TAMANHO / 2  # metade do comprimento do carro, em pixels da tela


def quadrado(px, py, cor, tam=F):
    gx = round(px / F) * F  # encaixa na grade de pixels
    gy = round(py / F) * F
    cv.create_rectangle(gx, gy, gx + tam, gy + tam, fill=cor, width=0)


def tick():
    global x, y, ang

    # Ctrl + Alt + Q fecha o programa
    if tecla(0x11) and tecla(0x12) and tecla(0x51):
        root.destroy()
        return

    mx, my = posicao_mouse()
    mx -= vx
    my -= vy
    turbo = tecla(0x01)  # botao esquerdo

    k = SEGUIR_TURBO if turbo else SEGUIR
    dx, dy = mx - x, my - y
    x += dx * k
    y += dy * k
    vel = math.hypot(dx * k, dy * k)

    if vel > 0.8:  # so vira quando esta andando
        alvo = math.atan2(dy, dx)
        d = math.atan2(math.sin(alvo - ang), math.cos(alvo - ang))
        ang += d * 0.2

    cv.delete("all")

    # fumaca saindo da traseira
    if FUMACA and vel > 1.5:
        for _ in range(2 if turbo else 1):
            fumaca.append([
                x - math.cos(ang) * (META + 2) + random.uniform(-2, 2),
                y - math.sin(ang) * (META + 2) + random.uniform(-2, 2),
                0,
            ])
    vivas = []
    for p in fumaca:
        p[2] += 1
        if p[2] < 22:
            vivas.append(p)
            cor = CORES_FUMACA[p[2] * len(CORES_FUMACA) // 22]
            quadrado(p[0], p[1], cor, F * (1 + p[2] // 8))
    fumaca[:] = vivas

    # chama do turbo
    if turbo and vel > 1:
        for n, cor in enumerate(CORES_CHAMA):
            dist = META + 3 + n * F * 2
            quadrado(
                x - math.cos(ang) * dist + random.uniform(-1, 1),
                y - math.sin(ang) * dist + random.uniform(-1, 1),
                cor,
            )

    # carro
    idx = round(ang / (2 * math.pi / DIRECOES)) % DIRECOES
    cv.create_image(round(x), round(y), image=IMAGENS[idx])

    root.after(INTERVALO_MS, tick)


tick()
root.mainloop()
