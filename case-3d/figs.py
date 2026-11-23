import os
HERE = os.path.dirname(os.path.abspath(__file__))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch, Arc, Polygon, Ellipse

LANG = os.environ.get("FIGS_LANG", "pt")   # "pt" (padrao) ou "en"
EN = {
    "Bluetooth\n(sem fio)": "Bluetooth\n(wireless)",
    "Seu controle\nDualSense": "Your DualSense\ncontroller",
    "Dongle\n(placa BL616)": "Dongle\n(BL616 board)",
    "Seu computador": "Your computer",
    "Vista de cima (esquema). A placa real pode ter pequenas diferenças.": "Top view (schematic). The real board may differ slightly.",
    "1. Segure o BOOT": "1. Hold BOOT",
    "2. Plugue no USB do PC": "2. Plug into PC USB",
    "3. Solte o BOOT": "3. Release BOOT",
    "Bouffalo Lab Dev Cube  (esquema ilustrativo, a tela real pode variar)": "Bouffalo Lab Dev Cube  (illustrative mock-up, the real screen may vary)",
    "<- clique aqui para gravar": "<- click here to flash",
    "Segure  PS + Create  por 3 segundos": "Hold  PS + Create  for 3 seconds",
    "A luz do controle pisca = modo de pareamento": "Controller light blinking = pairing mode",
    "Dongle plugado no PC": "Dongle plugged into the PC",
    "LED azul: de piscando para FIXO": "Blue LED: from blinking to SOLID",
    "O que o LED azul faz (3 segundos)": "What the blue LED does (3 seconds)",
    "Estado": "State",
    "Dica: depois de 1 minuto o LED apaga sozinho para não incomodar. Isso é normal (função ligada de fábrica).": "Tip: after 1 minute the LED turns itself off. This is normal (on by default).",
    "Botão BOOT da placa (o mesmo usado na gravação)": "BOOT button on the board (the same one used for flashing)",
    "Tampa (1,2 mm) com 4 batentes\nque seguram a placa nos cantos": "Lid (1.2 mm) with 4 lugs\nthat hold the board at the corners",
    "Botão BOOT\n(peça vermelha)": "BOOT button\n(red part)",
    "Conector\nUSB-C": "USB-C\nconnector",
    "Placa BL616 (1,0 mm)": "BL616 board (1.0 mm)",
    "Apoio nas bordas": "Edge support",
    "Fundo (1,0 mm)": "Floor (1.0 mm)",
    "9,5 mm": "9.5 mm",
    "50,1 mm": "50.1 mm",
    "Porta (COM)": "Port (COM)",
    "a que apareceu na lista (ex.: COM5)": "the one that appeared (e.g. COM5)",
    "Esperando / sem controle": "Waiting / no controller",
    "pisca devagar (1x por segundo)": "slow blink (1x per second)",
    "Procurando o controle": "Searching for controller",
    "pisca rápido (3x por segundo)": "fast blink (3x per second)",
    "aceso fixo": "solid",
    "Conectado": "Connected",
    "Bateria do controle quase no fim (10%)": "Controller battery almost empty (10%)",
    "pisca rápido": "fast blink",
    "Pareamentos apagados": "Pairings cleared",
    "3 piscadas curtas": "3 short flashes",
    "1 clique": "1 click",
    "Troca para o próximo\ncontrole já pareado\n(guarda até 8)": "Switches to the next\npaired controller\n(remembers up to 8)",
    "2 cliques": "2 clicks",
    "Desconecta o controle\natual e procura\num controle novo": "Disconnects the current\ncontroller and scans\nfor a new one",
    "Segurar 3 s": "Hold 3 s",
    "Apaga TODOS os\npareamentos e começa\nde novo (LED pisca 3x)": "Clears ALL pairings\nand starts over\n(LED flashes 3x)",
    "dedo no\nbotão BOOT": "finger on\nBOOT button",
    "cabo USB-C": "USB-C cable",
    "A placa está em modo\nde gravação (pronta)": "Board is in flash mode\n(ready)",
}
if LANG == "en":
    import matplotlib.axes as _ax
    _text, _annot = _ax.Axes.text, _ax.Axes.annotate
    _ax.Axes.text = lambda self, x, y, s, *a, **k: _text(self, x, y, EN.get(s, s), *a, **k)
    _ax.Axes.annotate = lambda self, t, *a, **k: _annot(self, EN.get(t, t), *a, **k)
OUT = os.path.join(HERE, "img_en" if LANG == "en" else "img")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1f3a5f"
TEAL = "#2a9d8f"
RED = "#d6453d"
ORANGE = "#e9892b"
BLUE = "#2563a8"
LIGHT = "#eef3f8"
GREY = "#8a94a3"
GREEN = "#2e9e5b"
plt.rcParams["font.family"] = "DejaVu Sans"


def newfig(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)


def rbox(ax, x, y, w, h, fc, ec="none", r=0.3, lw=1.0, z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    return p


def controller(ax, cx, cy, s=1.0, glow=False):
    # corpo
    rbox(ax, cx - 3.2 * s, cy - 1.0 * s, 6.4 * s, 2.0 * s, "#f4f6fa", "#b9c2d0", 0.9 * s, 1.2, 2)
    for sx in (-1, 1):
        ax.add_patch(Ellipse((cx + sx * 2.7 * s, cy - 1.25 * s), 1.9 * s, 2.8 * s, angle=sx * -12,
                             fc="#f4f6fa", ec="#b9c2d0", lw=1.2, zorder=1))
    # faixa preta central
    rbox(ax, cx - 2.6 * s, cy - 0.9 * s, 5.2 * s, 1.7 * s, "#eceff5", "none", 0.8 * s, 0, 3)
    # touchpad
    rbox(ax, cx - 0.9 * s, cy + 0.05 * s, 1.8 * s, 0.75 * s, "#dde3ec", "#b9c2d0", 0.2 * s, 0.8, 4)
    # light bar
    col = "#3b82f6" if glow else "#9fb3d1"
    for sx in (-1, 1):
        ax.add_patch(Arc((cx + sx * 0.0, cy + 0.2 * s), 6.0 * s, 2.0 * s, theta1=20 if sx > 0 else 160,
                         theta2=70 if sx > 0 else 200, color=col, lw=3.0 if glow else 1.5, zorder=5))
    # analogicos
    for sx in (-0.9, 0.9):
        ax.add_patch(Circle((cx + sx * s, cy - 0.65 * s), 0.38 * s, fc="#cfd6e2", ec="#9aa6b8", lw=1, zorder=5))
    # direcional e botoes
    ax.plot([cx - 2.1 * s, cx - 1.5 * s], [cy + 0.2 * s] * 2, color="#9aa6b8", lw=3 * s, zorder=5, solid_capstyle="round")
    ax.plot([cx - 1.8 * s] * 2, [cy - 0.1 * s, cy + 0.5 * s], color="#9aa6b8", lw=3 * s, zorder=5, solid_capstyle="round")
    for dx, dy in ((1.8, 0.5), (1.8, -0.1), (1.5, 0.2), (2.1, 0.2)):
        ax.add_patch(Circle((cx + dx * s, cy + dy * s), 0.14 * s, fc="#9aa6b8", ec="none", zorder=5))


def dongle(ax, cx, cy, s=1.0, led="#2563eb"):
    # placa
    rbox(ax, cx - 1.2 * s, cy - 0.6 * s, 2.4 * s, 1.2 * s, BLUE, "#143d70", 0.12 * s, 1.0, 3)
    rbox(ax, cx - 1.65 * s, cy - 0.32 * s, 0.6 * s, 0.64 * s, "#cfd4db", "#8a94a3", 0.1 * s, 0.8, 3)
    ax.add_patch(Rectangle((cx + 0.2 * s, cy - 0.15 * s), 0.4 * s, 0.4 * s, fc="#111827", ec="none", zorder=4))
    ax.add_patch(Circle((cx - 0.1 * s, cy + 0.4 * s), 0.08 * s, fc=led, ec="none", zorder=5))


def pc(ax, cx, cy, s=1.0):
    rbox(ax, cx - 1.6 * s, cy - 0.7 * s, 3.2 * s, 2.1 * s, "#e5e9f0", "#9aa6b8", 0.15 * s, 1.2, 2)
    rbox(ax, cx - 1.4 * s, cy - 0.5 * s, 2.8 * s, 1.7 * s, "#223a5e", "none", 0.08 * s, 0, 3)
    ax.add_patch(Rectangle((cx - 0.15 * s, cy - 1.0 * s), 0.3 * s, 0.35 * s, fc="#9aa6b8", ec="none", zorder=2))
    rbox(ax, cx - 0.7 * s, cy - 1.15 * s, 1.4 * s, 0.2 * s, "#9aa6b8", "none", 0.08 * s, 0, 2)
    ax.text(cx, cy + 0.35 * s, "PC", color="white", ha="center", va="center", fontsize=11, fontweight="bold", zorder=5)


def arrow(ax, p0, p1, color=NAVY, lw=2.0, style="-|>", ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=14, color=color, lw=lw, ls=ls,
                                 connectionstyle=f"arc3,rad={rad}", zorder=6))


def waves(ax, x, y, n=3, color=BLUE):
    for i in range(n):
        r = 0.5 + i * 0.35
        ax.add_patch(Arc((x, y), r * 2, r * 2, theta1=-40, theta2=40, color=color, lw=2.2, zorder=6))


def fig_arch():
    fig, ax = newfig(9.4, 2.9)
    ax.set_xlim(-1.4, 20.2)
    ax.set_ylim(-1.6, 3.6)
    controller(ax, 3.0, 1.2, 1.0, glow=True)
    dongle(ax, 10.0, 1.2, 1.15)
    pc(ax, 17.2, 1.1, 1.05)
    waves(ax, 6.7, 1.2)
    arrow(ax, (11.8, 1.2), (15.0, 1.2), color=NAVY, lw=2.4)
    ax.text(8.0, 2.7, "Bluetooth\n(sem fio)", ha="center", va="center", fontsize=9, color=BLUE, fontweight="bold")
    ax.text(13.4, 1.75, "USB", ha="center", va="center", fontsize=9, color=NAVY, fontweight="bold")
    ax.text(3.0, -0.8, "Seu controle\nDualSense", ha="center", va="center", fontsize=9, color=NAVY)
    ax.text(10.0, -0.8, "Dongle\n(placa BL616)", ha="center", va="center", fontsize=9, color=NAVY)
    ax.text(17.2, -0.8, "Seu computador", ha="center", va="center", fontsize=9, color=NAVY)
    save(fig, "arch")


# ---------------------------------------------------------------- placa
def board(ax, ox=0, oy=0, s=1.0, labels=False, hl_boot=False):
    L, W = 45.5, 22.5
    rbox(ax, ox, oy, L * s, W * s, BLUE, "#143d70", 1.2 * s, 1.5, 2)
    # USB-C
    rbox(ax, ox - 0.8 * s, oy + (13.8 - 4.47) * s, 7.0 * s, 8.94 * s, "#d5dae1", "#8a94a3", 1.2 * s, 1.0, 4)
    rbox(ax, ox + 0.6 * s, oy + (13.8 - 3.2) * s, 5.2 * s, 6.4 * s, "#8f98a5", "none", 1.0 * s, 0, 5)
    # chip
    ax.add_patch(Rectangle((ox + 24.0 * s, oy + 10.3 * s), 6.0 * s, 6.0 * s, fc="#161b22", ec="#0b0f14", lw=0.8, zorder=5))
    ax.add_patch(Circle((ox + 25.2 * s, oy + 11.5 * s), 0.35 * s, fc="#444c56", ec="none", zorder=6))
    # botao BOOT
    bx, by = ox + 6.2 * s, oy + 4.7 * s
    ax.add_patch(Rectangle((bx - 2.1 * s, by - 2.1 * s), 4.2 * s, 4.2 * s, fc="#e7eaee", ec="#8a94a3", lw=0.8, zorder=5))
    ax.add_patch(Circle((bx, by), 1.2 * s, fc="#2b2f36", ec="#111", lw=0.5, zorder=6))
    if hl_boot:
        ax.add_patch(Circle((bx, by), 3.2 * s, fc="none", ec=ORANGE, lw=2.4, zorder=7))
    # LEDs
    lx, ly = ox + 19.9 * s, oy + 21.1 * s
    ax.add_patch(Circle((lx - 0.9 * s, ly), 0.55 * s, fc="#ff5a4f", ec="#7a1d18", lw=0.5, zorder=6))
    ax.add_patch(Circle((lx + 0.9 * s, ly), 0.55 * s, fc="#4aa3ff", ec="#16457a", lw=0.5, zorder=6))
    # antena
    ax.add_patch(Rectangle((ox + 25.0 * s, oy + 0.5 * s), 2.2 * s, 1.2 * s, fc="#d9a79f", ec="#8d5148", lw=0.6, zorder=6))
    # furos
    for i in range(8):
        for cxn in (39.9, 42.4):
            ax.add_patch(Circle((ox + cxn * s, oy + (20.6 - i * 2.54) * s), 0.62 * s, fc="#e8c7e8", ec="#7a4a7a", lw=0.5, zorder=5))
    if labels:
        pts = {
            1: (ox + 1.5 * s, oy + 13.8 * s, -6.5, 13.8 + 12, "USB"),
            2: (bx, by, 6.2, -6.5, "BOOT"),
            3: (lx, ly, 19.9, 29.0, "LED"),
            4: (ox + 26.1 * s, oy + 1.1 * s, 31.0, -6.5, "ANT"),
            5: (ox + 41.2 * s, oy + 11.0 * s, 52.5, 11.0, "PINOS"),
            6: (ox + 27.0 * s, oy + 13.3 * s, 27.0, 29.0, "CHIP"),
        }
        for n, (px, py, tx, ty, _) in pts.items():
            tx, ty = ox + tx * s, oy + ty * s
            ax.plot([px, tx], [py, ty], color=NAVY, lw=1.2, zorder=8)
            ax.add_patch(Circle((tx, ty), 1.7 * s, fc=NAVY, ec="white", lw=1.5, zorder=9))
            ax.text(tx, ty, str(n), color="white", ha="center", va="center", fontsize=11, fontweight="bold", zorder=10)


def fig_board():
    fig, ax = newfig(9.0, 4.4)
    ax.set_xlim(-12, 58)
    ax.set_ylim(-11, 36)
    board(ax, 0, 0, 1.0, labels=True)
    ax.text(22.7, -9.5, "Vista de cima (esquema). A placa real pode ter pequenas diferenças.", ha="center",
            fontsize=7.5, color=GREY, style="italic")
    save(fig, "board")


def fig_bootmode():
    fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.0), dpi=200)
    titles = ["1. Segure o BOOT", "2. Plugue no USB do PC", "3. Solte o BOOT"]
    for i, ax in enumerate(axs):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-14, 52)
        ax.set_ylim(-16, 30)
        rbox(ax, -14, -16, 66, 46, LIGHT, "#d3dce8", 2.0, 1.0, 0)
        ax.text(19, 27.0, titles[i], ha="center", va="center", fontsize=10.5, color=NAVY, fontweight="bold")
        board(ax, 0, 0, 0.95, hl_boot=(i < 2))
        if i < 2:
            # dedo
            ax.add_patch(Ellipse((6.0, -5.5), 6.5, 9.0, fc="#f1c9a5", ec="#c9976a", lw=1.2, zorder=12))
            ax.text(6.0, -13.0, "dedo no\nbotão BOOT", ha="center", va="center", fontsize=7.5, color=NAVY)
        if i == 1:
            ax.plot([-1, -11], [13.0, 13.0], color="#334155", lw=5, zorder=3, solid_capstyle="round")
            rbox(ax, -13.6, 10.4, 4.4, 5.2, "#334155", "none", 1.0, 0, 3)
            ax.text(-8.5, 19.5, "cabo USB-C", ha="center", fontsize=7.5, color=NAVY)
        if i == 2:
            ax.add_patch(Circle((22, 11), 6.5, fc=GREEN, ec="none", zorder=13))
            ax.plot([18.8, 21.0, 25.4], [11.0, 8.6, 13.6], color="white", lw=4, zorder=14, solid_capstyle="round")
            ax.text(22, -8.0, "A placa está em modo\nde gravação (pronta)", ha="center", va="center", fontsize=8, color=NAVY)
    fig.subplots_adjust(wspace=0.04, left=0.01, right=0.99, top=0.99, bottom=0.01)
    fig.savefig(f"{OUT}/bootmode.png", facecolor="white", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


def fig_devcube():
    fig, ax = newfig(8.6, 5.0)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 68)
    rbox(ax, 0, 0, 100, 68, "#f3f4f6", "#9aa6b8", 1.5, 1.5, 0)
    ax.add_patch(Rectangle((0, 62), 100, 6, fc="#2b3f5e", ec="none", zorder=1))
    ax.text(2.5, 65, "Bouffalo Lab Dev Cube  (esquema ilustrativo, a tela real pode variar)", color="white", fontsize=7.6, va="center")
    rows = [
        ("Chip Type", "BL616", None),
        ("Interface", "UART", None),
        ("Porta (COM)", "a que apareceu na lista (ex.: COM5)", None),
        ("Partition Table", "partition_cfg_4M_nosec.toml", RED),
        ("Boot2 Bin", "boot2_bl616_isp_release_v8.1.8.bin", None),
        ("Firmware Bin", "ds5dongle-lctech616.bin", None),
    ]
    y = 55
    for i, (k, v, hl) in enumerate(rows):
        ax.text(3, y, k, fontsize=8.4, va="center", color=NAVY, fontweight="bold")
        rbox(ax, 30, y - 3.0, 66, 6.0, "white", hl if hl else "#c3cad5", 0.8, 2.0 if hl else 1.0, 2)
        ax.text(32, y, v, fontsize=8.2, va="center", color="#111827")
        ax.add_patch(Circle((97.5 if False else 27, y), 1.4, fc=NAVY, ec="none", zorder=4))
        ax.text(27, y, str(i + 1), color="white", ha="center", va="center", fontsize=6.8, fontweight="bold", zorder=5)
        y -= 8.2
    rbox(ax, 30, 1.2, 30, 7, TEAL, "none", 1.0, 0, 3)
    ax.text(45, 4.7, "Create & Download", color="white", ha="center", va="center", fontsize=8.6, fontweight="bold", zorder=5)
    ax.add_patch(Circle((27, 4.7), 1.4, fc=NAVY, ec="none", zorder=4))
    ax.text(27, 4.7, "7", color="white", ha="center", va="center", fontsize=6.8, fontweight="bold", zorder=5)
    ax.text(63, 4.7, "<- clique aqui para gravar", fontsize=8, va="center", color=TEAL, fontweight="bold")
    ax.text(97, 41.5, "", fontsize=7)
    save(fig, "devcube")


def fig_pair():
    fig, ax = newfig(9.2, 3.0)
    ax.set_xlim(-1.8, 22)
    ax.set_ylim(-4.0, 4.4)
    controller(ax, 4.2, 1.0, 1.25, glow=True)
    # PS + Create destacados
    ax.add_patch(Circle((4.2, 0.35), 0.5, fc=ORANGE, ec="white", lw=1.5, zorder=8))
    ax.text(4.2, 0.35, "PS", ha="center", va="center", fontsize=6.5, color="white", fontweight="bold", zorder=9)
    ax.add_patch(Circle((1.6, 2.0), 0.5, fc=ORANGE, ec="white", lw=1.5, zorder=8))
    ax.text(1.6, 2.0, "C", ha="center", va="center", fontsize=7, color="white", fontweight="bold", zorder=9)
    ax.text(4.2, 3.6, "Segure  PS + Create  por 3 segundos", ha="center", fontsize=9.5, color=NAVY, fontweight="bold")
    ax.text(4.2, -3.3, "A luz do controle pisca = modo de pareamento", ha="center", fontsize=8.6, color=NAVY)
    waves(ax, 9.0, 1.0, 3)
    dongle(ax, 13.8, 1.0, 1.4, led="#2563eb")
    ax.text(13.8, -0.3, "Dongle plugado no PC", ha="center", fontsize=8.6, color=NAVY)
    ax.text(13.8, -1.2, "LED azul: de piscando para FIXO", ha="center", fontsize=8.6, color=GREEN, fontweight="bold")
    pc(ax, 19.6, 1.0, 0.95)
    arrow(ax, (15.9, 1.0), (17.6, 1.0), lw=2)
    save(fig, "pair")


def fig_leds():
    fig, ax = newfig(8.6, 3.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 46)
    states = [
        ("Esperando / sem controle", "pisca devagar (1x por segundo)", [(0, .5), (1, 1.5), (2, 2.5)]),
        ("Procurando o controle", "pisca rápido (3x por segundo)", [(i / 3, i / 3 + 1 / 6) for i in range(9)]),
        ("Conectado", "aceso fixo", [(0, 3)]),
        ("Bateria do controle quase no fim (10%)", "pisca rápido", [(i / 3, i / 3 + 1 / 6) for i in range(9)]),
        ("Pareamentos apagados", "3 piscadas curtas", [(0.0, .2), (.4, .6), (.8, 1.0)]),
    ]
    y = 40
    ax.text(2, 45, "Estado", fontsize=8.6, fontweight="bold", color=NAVY, va="center")
    ax.text(40, 45, "O que o LED azul faz (3 segundos)", fontsize=8.6, fontweight="bold", color=NAVY, va="center")
    for name, desc, on in states:
        ax.text(2, y, name, fontsize=8.2, va="center", color="#111827")
        ax.add_patch(Rectangle((40, y - 2.2), 30, 4.4, fc="#e5e9f0", ec="none", zorder=1))
        for a, b in on:
            ax.add_patch(Rectangle((40 + a * 10, y - 2.2), (b - a) * 10, 4.4, fc="#2f7bff", ec="none", zorder=2))
        ax.text(72.5, y, desc, fontsize=7.6, va="center", color=GREY)
        y -= 8.0
    ax.text(2, 1.5, "Dica: depois de 1 minuto o LED apaga sozinho para não incomodar. Isso é normal (função ligada de fábrica).",
            fontsize=7.6, color=GREY, va="center", style="italic")
    save(fig, "leds")


def fig_gestures():
    fig, ax = newfig(9.2, 2.9)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 32)
    cards = [
        ("1 clique", "Troca para o próximo\ncontrole já pareado\n(guarda até 8)", [(0, 1)]),
        ("2 cliques", "Desconecta o controle\natual e procura\num controle novo", [(0, 1), (1, 1)]),
        ("Segurar 3 s", "Apaga TODOS os\npareamentos e começa\nde novo (LED pisca 3x)", [(0, 2)]),
    ]
    for i, (t, d, _) in enumerate(cards):
        x0 = 1 + i * 33
        rbox(ax, x0, 1, 31, 30, LIGHT, "#d3dce8", 1.5, 1.0, 0)
        ax.text(x0 + 15.5, 27.2, t, ha="center", va="center", fontsize=10, fontweight="bold", color=NAVY)
        # botao
        n = 2 if i == 1 else 1
        for k in range(n):
            cx = x0 + 15.5 + (k - (n - 1) / 2) * 6
            ax.add_patch(Circle((cx, 19.2), 2.3, fc="#2b2f36", ec="white", lw=1.2, zorder=3))
            ax.add_patch(Circle((cx, 19.2), 3.4, fc="none", ec=ORANGE, lw=1.6, zorder=3))
        if i == 2:
            ax.add_patch(Arc((x0 + 15.5, 19.2), 11, 11, theta1=40, theta2=330, color=TEAL, lw=2.2, zorder=3))
        ax.text(x0 + 15.5, 8.8, d, ha="center", va="center", fontsize=7.8, color="#111827", linespacing=1.35)
    ax.text(50, -1.6, "Botão BOOT da placa (o mesmo usado na gravação)", ha="center", fontsize=7.8, color=GREY, style="italic")
    save(fig, "gestures")


def fig_section():
    """Corte lateral esquematico da case."""
    fig, ax = newfig(9.2, 3.8)
    ax.set_xlim(-6, 62)
    ax.set_ylim(-4, 22)
    k = 1.0
    col_b, col_l = "#4b5b73", "#8aa0bd"
    # base: fundo + paredes
    ax.add_patch(Rectangle((0, 0), 50.1, 1.0, fc=col_b, ec="none"))
    ax.add_patch(Rectangle((0, 0), 2.0, 8.3, fc=col_b, ec="none"))
    ax.add_patch(Rectangle((48.1, 0), 2.0, 8.3, fc=col_b, ec="none"))
    # apoio
    ax.add_patch(Rectangle((2.0, 1.0), 1.5, 1.0, fc=col_b, ec="none"))
    ax.add_patch(Rectangle((46.6, 1.0), 1.5, 1.0, fc=col_b, ec="none"))
    # abertura USB (recorte na parede esquerda)
    ax.add_patch(Rectangle((-0.1, 1.0), 2.2, 7.4, fc="white", ec="none", zorder=3))
    # PCB
    ax.add_patch(Rectangle((2.3, 2.0), 45.5, 1.0, fc=BLUE, ec="none", zorder=4))
    ax.add_patch(Rectangle((1.5, 3.0), 7.0, 3.2, fc="#cfd4db", ec="#8a94a3", lw=0.6, zorder=4))
    ax.add_patch(Rectangle((10.6, 3.0), 4.0, 1.8, fc="#e7eaee", ec="#8a94a3", lw=0.6, zorder=4))
    ax.add_patch(Rectangle((24.5, 3.0), 6.0, 0.9, fc="#161b22", ec="none", zorder=4))
    # tampa
    ax.add_patch(Rectangle((0, 8.3), 50.1, 1.2, fc=col_l, ec="none"))
    ax.add_patch(Rectangle((0, 5.8), 0.85, 2.5, fc=col_l, ec="none"))
    ax.add_patch(Rectangle((49.25, 5.8), 0.85, 2.5, fc=col_l, ec="none"))
    # batentes
    ax.add_patch(Rectangle((2.5, 3.2), 1.5, 5.1, fc=col_l, ec="none"))
    ax.add_patch(Rectangle((46.1, 3.2), 1.5, 5.1, fc=col_l, ec="none"))
    # botao (plunger)
    ax.add_patch(Rectangle((7.2, 5.0), 2.6, 2.5, fc=RED, ec="none", zorder=5))
    ax.add_patch(Rectangle((5.8, 7.5), 5.4, 0.8, fc=RED, ec="none", zorder=5))
    ax.add_patch(Rectangle((7.0, 8.3), 3.0, 2.2, fc=RED, ec="none", zorder=5))
    ax.add_patch(Rectangle((8.0, 3.0), 0.0, 0.0, fc="none"))
    ax.add_patch(Rectangle((6.2, 3.0), 4.0, 1.8, fc="#e7eaee", ec="#8a94a3", lw=0.6, zorder=4))
    # cotas e legendas
    def note(x, y, tx, ty, txt, col=NAVY):
        ax.annotate(txt, xy=(x, y), xytext=(tx, ty), fontsize=7.6, color=col, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color=col, lw=0.9))
    note(25, 9.0, 25, 14.2, "Tampa (1,2 mm) com 4 batentes\nque seguram a placa nos cantos", NAVY)
    note(8.5, 10.4, 8.5, 17.4, "Botão BOOT\n(peça vermelha)", RED)
    note(5.0, 4.5, -2.2, 12.6, "Conector\nUSB-C", NAVY)
    note(28, 2.5, 33, -2.2, "Placa BL616 (1,0 mm)", BLUE)
    note(2.7, 1.5, 8, -2.2, "Apoio nas bordas", NAVY)
    note(25, 0.5, 44, -2.2, "Fundo (1,0 mm)", NAVY)
    ax.annotate("", xy=(52.5, 0), xytext=(52.5, 9.5), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(55.8, 4.7, "9,5 mm", fontsize=8, color=GREY, rotation=90, va="center")
    ax.annotate("", xy=(0, 20.3), xytext=(50.1, 20.3), arrowprops=dict(arrowstyle="<->", color=GREY, lw=1))
    ax.text(25, 21.2, "50,1 mm", fontsize=8, color=GREY, ha="center")
    save(fig, "section")


if __name__ == "__main__":
    for f in (fig_arch, fig_board, fig_bootmode, fig_devcube, fig_pair, fig_leds, fig_gestures, fig_section):
        f()
    print(sorted(os.listdir(OUT)))
