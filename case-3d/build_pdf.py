import os
HERE = os.path.dirname(os.path.abspath(__file__))
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle,
                                PageBreak, KeepTogether, Flowable, Preformatted)
from PIL import Image as PILImage

IMG = os.path.join(HERE, "img")
os.makedirs(os.path.join(HERE, "saida"), exist_ok=True)
OUT = os.path.join(HERE, "saida", "LEIA-ME_Dongle_DualSense_BL616.pdf")

NAVY = colors.HexColor("#1f3a5f")
TEAL = colors.HexColor("#2a9d8f")
RED = colors.HexColor("#d6453d")
ORANGE = colors.HexColor("#e9892b")
BLUE = colors.HexColor("#2563a8")
LIGHT = colors.HexColor("#eef3f8")
GREY = colors.HexColor("#6b7686")
GREEN = colors.HexColor("#2e9e5b")

W, H = A4
M = 17 * mm
CW = W - 2 * M

st = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=NAVY, spaceAfter=2),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=12, leading=16, textColor=GREY, spaceAfter=10),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=6, spaceAfter=5),
    "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=BLUE, spaceBefore=6, spaceAfter=3),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.2, textColor=colors.HexColor("#1b2430"), spaceAfter=5),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=GREY, spaceAfter=3),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=9.4, leading=12.6, textColor=colors.HexColor("#1b2430")),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=9.4, leading=12.6, textColor=NAVY),
    "bul": ParagraphStyle("bul", fontName="Helvetica", fontSize=10, leading=14, leftIndent=14, bulletIndent=3,
                          textColor=colors.HexColor("#1b2430"), spaceAfter=2.5),
    "num": ParagraphStyle("num", fontName="Helvetica", fontSize=10, leading=14, leftIndent=18, bulletIndent=0,
                          textColor=colors.HexColor("#1b2430"), spaceAfter=3),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=6.7, leading=8.6, textColor=colors.HexColor("#0f172a")),
    "url": ParagraphStyle("url", fontName="Courier", fontSize=6.9, leading=9, textColor=BLUE, spaceAfter=4, leftIndent=18),
    "cap": ParagraphStyle("cap", fontName="Helvetica-Oblique", fontSize=8.2, leading=11, textColor=GREY, alignment=TA_CENTER,
                          spaceBefore=2, spaceAfter=6),
}


def P(t, s="body"):
    return Paragraph(t, st[s])


def bullets(items, style="bul"):
    return [Paragraph(i, st[style], bulletText="\u2022") for i in items]


def numbered(items):
    return [Paragraph(t, st["num"], bulletText=f"{i}.") for i, t in enumerate(items, 1)]


def img(name, width=None, maxh=None):
    path = f"{IMG}/{name}.png"
    w0, h0 = PILImage.open(path).size
    width = width or CW
    h = width * h0 / w0
    if maxh and h > maxh:
        width = width * maxh / h
        h = maxh
    i = Image(path, width=width, height=h)
    i.hAlign = "CENTER"
    return i


class StepHeader(Flowable):
    def __init__(self, num, title, color=BLUE):
        super().__init__()
        self.num, self.title, self.color = num, title, color
        self.height = 11 * mm

    def wrap(self, aw, ah):
        self.width = aw
        return aw, self.height + 3 * mm

    def draw(self):
        c = self.canv
        c.setFillColor(LIGHT)
        c.roundRect(0, 1.5 * mm, self.width, self.height, 3 * mm, stroke=0, fill=1)
        c.setFillColor(self.color)
        c.circle(6.5 * mm, 1.5 * mm + self.height / 2, 4.4 * mm, stroke=0, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(6.5 * mm, 1.5 * mm + self.height / 2 - 1.6 * mm, str(self.num))
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(13.5 * mm, 1.5 * mm + self.height / 2 - 1.8 * mm, self.title)


def box(flowables, kind="info"):
    col = {"info": BLUE, "warn": ORANGE, "ok": GREEN, "bad": RED}[kind]
    bg = {"info": "#eef4fb", "warn": "#fff4e6", "ok": "#eaf7f0", "bad": "#fdeceb"}[kind]
    t = Table([[flowables]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, col),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def code(text):
    t = Table([[Preformatted(text, st["code"])]], colWidths=[CW])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#cbd5e1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def table(rows, widths, header=True, zebra=True):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    sty = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#d3dce8")),
    ]
    if header:
        sty += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if r % 2 == 0:
                sty.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f6f8fb")))
    t.setStyle(TableStyle(sty))
    return t


def hdr(txt):
    return Paragraph(f'<font color="white"><b>{txt}</b></font>', st["cell"])


def link(url, text=None):
    return f'<link href="{url}" color="#2563a8"><u>{text or url}</u></link>'


def footer(canv, doc):
    canv.saveState()
    canv.setStrokeColor(colors.HexColor("#d3dce8"))
    canv.line(M, 13 * mm, W - M, 13 * mm)
    canv.setFont("Helvetica", 8)
    canv.setFillColor(GREY)
    canv.drawString(M, 8.5 * mm, "Dongle DualSense sem fio  |  placa BL616 (LCTech)  |  firmware DS5Dongle v3.22")
    canv.drawRightString(W - M, 8.5 * mm, f"p\u00e1gina {doc.page}")
    canv.restoreState()


story = []

# ------------------------------------------------------------------ PAGINA 1
story += [
    P("Dongle DualSense sem fio para PC", "title"),
    P("Guia passo a passo: placa BL616 (LCTech) + firmware DS5Dongle v3.22", "sub"),
    P("Depois de gravada, esta placa vira um <b>adaptador USB</b>: voc\u00ea liga no PC e o computador passa a enxergar o seu "
      "controle <b>DualSense</b> (PS5), conectado por Bluetooth, como se ele estivesse com cabo. Assim o controle funciona "
      "sem fio com os recursos completos, segundo o projeto: vibra\u00e7\u00e3o, gatilhos adaptativos, girosc\u00f3pio, touchpad, "
      "alto-falante, microfone e h\u00e1ptica HD."),
    Spacer(1, 3),
    img("arch", CW * 0.97),
    Spacer(1, 2),
    P("Voc\u00ea vai precisar de", "h2"),
]
story += bullets([
    "A <b>placa BL616</b> (azul, com entrada USB-C e um bot\u00e3o escrito BOOT).",
    "Um <b>cabo USB-C de dados</b> (cabo s\u00f3 de carga n\u00e3o funciona) e uma porta USB livre no PC.",
    "Um PC com <b>Windows</b> e internet (s\u00f3 para baixar os arquivos).",
    "Um controle <b>DualSense</b> (PS5) ou DualSense Edge.",
    "Cerca de 10 minutos. <b>N\u00e3o precisa soldar nada</b> e n\u00e3o precisa saber programar.",
])
story += [Spacer(1, 4), P("O caminho em 5 passos", "h2")]
steps = [("1", "Baixar os\narquivos"), ("2", "Colocar a placa\nem modo gravar"), ("3", "Configurar o\nDev Cube"),
         ("4", "Gravar o\nfirmware"), ("5", "Parear o\ncontrole")]
cells = []
for n, t in steps:
    cells.append([Paragraph(f'<font size="20" color="#2563a8"><b>{n}</b></font>', ParagraphStyle("c", alignment=TA_CENTER, leading=24)),
                  Paragraph(t.replace("\n", "<br/>"), ParagraphStyle("c2", fontName="Helvetica-Bold", fontSize=9, leading=12,
                                                                    alignment=TA_CENTER, textColor=NAVY))])
rowtab = Table([[c[0] for c in cells], [c[1] for c in cells]], colWidths=[CW / 5] * 5)
rowtab.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#d3dce8")),
    ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.white), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, 0), 6), ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
]))
story += [rowtab, Spacer(1, 8)]
story += [box([P("<b>Aviso:</b> este \u00e9 um projeto de terceiros (sqlCRT/ds5dongle-bl618-opensource, baseado em awalol/DS5Dongle), "
                 "sem v\u00ednculo com a Sony. O firmware emula um controle DualSense com fio. Use por sua conta e risco.", "small")], "warn")]
story.append(PageBreak())

# ------------------------------------------------------------------ PAGINA 2
story += [P("Conhe\u00e7a a placa", "h2"), img("board", CW * 0.92, maxh=88 * mm), Spacer(1, 2)]
legend = [
    [hdr("N\u00ba"), hdr("Pe\u00e7a"), hdr("Para que serve")],
    [P("<b>1</b>", "cellb"), P("Entrada USB-C", "cellb"), P("Aqui entra o cabo que vai ao PC. Use um cabo curto de dados (USB-C para USB, ou com adaptador).", "cell")],
    [P("<b>2</b>", "cellb"), P("Bot\u00e3o BOOT", "cellb"), P("Usado para gravar o firmware e, depois, para trocar ou apagar pareamentos de controles.", "cell")],
    [P("<b>3</b>", "cellb"), P("LEDs", "cellb"), P("Vermelho = energia. Azul = status do dongle (veja a p\u00e1gina 4).", "cell")],
    [P("<b>4</b>", "cellb"), P("Antena de cer\u00e2mica", "cellb"), P("\u00c9 o Bluetooth. N\u00e3o cubra com metal nem papel alum\u00ednio.", "cell")],
    [P("<b>5</b>", "cellb"), P("Furos para pinos", "cellb"), P("<b>N\u00e3o s\u00e3o usados.</b> O conector de 8 pinos que vem junto pode ficar guardado.", "cell")],
    [P("<b>6</b>", "cellb"), P("Chip BL616", "cellb"), P("O c\u00e9rebro: cuida do Bluetooth e do USB.", "cell")],
]
story += [table(legend, [12 * mm, 38 * mm, CW - 50 * mm]), Spacer(1, 8)]

story += [StepHeader(1, "Baixar os arquivos")]
story += [P("Fa\u00e7a isto no PC onde a placa ser\u00e1 gravada.")]
story += numbered([
    "Baixe o pacote do firmware (ZIP, cerca de 1 MB): " + link("https://github.com/sqlCRT/ds5dongle-bl618-opensource/releases/download/v3.22/ds5dongle-bl618-lctech616-v3.22.zip", "clique aqui para baixar o ZIP v3.22") + ".",
    "Clique com o bot\u00e3o direito no ZIP e escolha <b>Extrair tudo...</b>. Sugest\u00e3o de pasta: <font name='Courier'>C:\\DS5Dongle</font> (anote onde ficou).",
    "Baixe e instale o <b>Bouffalo Lab Dev Cube</b> (programa oficial do fabricante do chip, usado para gravar): " + link("https://dev.bouffalolab.com/download") + ".",
])
story += [Paragraph("Endere\u00e7o do ZIP, caso o clique n\u00e3o funcione:", st["small"]),
          Paragraph("https://github.com/sqlCRT/ds5dongle-bl618-opensource/releases/download/v3.22/ds5dongle-bl618-lctech616-v3.22.zip", st["url"])]
files = [
    [hdr("Arquivo (na pasta extra\u00edda)"), hdr("O que \u00e9")],
    [P("ds5dongle-lctech616.bin", "cellb"), P("Firmware <b>FS</b> (Full-Speed): <b>use este para come\u00e7ar</b>. Melhor compatibilidade com cabos e portas.", "cell")],
    [P("ds5dongle-lctech616-hs.bin", "cellb"), P("Firmware <b>HS</b> (High-Speed): leitura mais r\u00e1pida, mas exige cabo e porta bons. Opcional.", "cell")],
    [P("boot2_bl616_isp_release_v8.1.8.bin", "cellb"), P("Programa de inicializa\u00e7\u00e3o da placa (obrigat\u00f3rio na grava\u00e7\u00e3o).", "cell")],
    [P("partition_cfg_4M_nosec.toml", "cellb"), P("Tabela de parti\u00e7\u00f5es: <b>sempre a vers\u00e3o \"nosec\"</b>.", "cell")],
]
story += [Spacer(1, 3), table(files, [62 * mm, CW - 62 * mm])]

# ------------------------------------------------------------------ PAGINA 3
story += [StepHeader(2, "Colocar a placa em modo de grava\u00e7\u00e3o")]
story += [P("Para receber um firmware novo, a placa precisa ligar de um jeito especial. \u00c9 s\u00f3 uma pegadinha de ordem:")]
story += [img("bootmode", CW)]
story += numbered([
    "Com a placa <b>desconectada</b> do PC, <b>aperte e segure</b> o bot\u00e3o BOOT (se for dif\u00edcil, use a ponta de um clipe ou palito).",
    "Sem soltar, ligue o cabo USB-C no PC.",
    "S\u00f3 agora solte o bot\u00e3o. Pronto.",
])
story += [box([P("<b>Como saber que deu certo?</b> No Dev Cube (pr\u00f3ximo passo) vai aparecer uma <b>porta COM</b> nova na lista "
                 "(por exemplo COM5). Se n\u00e3o aparecer: tente outro cabo (cabo s\u00f3 de carga n\u00e3o serve), outra porta USB do PC, "
                 "ou desligue e repita desde o in\u00edcio.", "cell")], "info"), Spacer(1, 8)]

story += [StepHeader(3, "Configurar o Dev Cube")]
story += [P("Abra o <b>Bouffalo Lab Dev Cube</b>, escolha o chip e preencha como no esquema abaixo. Os arquivos est\u00e3o na pasta "
            "que voc\u00ea extraiu no Passo 1.")]
story += [img("devcube", CW * 0.80, maxh=108 * mm)]
story += [P("Os nomes dos campos podem variar um pouco conforme a vers\u00e3o do programa; o importante s\u00e3o os valores.", "cap")]
story += [box([P("<b>Aten\u00e7\u00e3o ao item 4:</b> escolha <font name='Courier'>partition_cfg_4M_<b>nosec</b>.toml</font>. "
                 "Existe outro arquivo parecido, sem \"nosec\" no nome: <b>n\u00e3o use</b>.", "cell")], "bad")]
story.append(PageBreak())

# ------------------------------------------------------------------ PAGINA 4
story += [StepHeader(4, "Gravar o firmware")]
story += numbered([
    "Confira se os 6 campos est\u00e3o preenchidos e clique em <b>Create &amp; Download</b>.",
    "Espere a barra de progresso chegar ao fim e aparecer a mensagem de sucesso. <b>N\u00e3o desligue o cabo durante a grava\u00e7\u00e3o.</b>",
    "Desconecte o cabo e conecte de novo, <b>sem apertar o BOOT</b>.",
    "O LED azul deve ficar <b>piscando devagar</b>: o dongle est\u00e1 pronto e esperando um controle.",
])
story += [Spacer(1, 4), StepHeader(5, "Parear o controle")]
story += [img("pair", CW * 0.95, maxh=62 * mm)]
story += numbered([
    "Com o dongle plugado no PC (LED piscando devagar) e o controle <b>desligado</b>, segure <b>PS + Create</b> por 3 segundos, "
    "at\u00e9 a luz do controle come\u00e7ar a piscar.",
    "Em poucos segundos o LED do dongle pisca r\u00e1pido (procurando) e depois fica <b>aceso fixo</b>: conectado.",
    "O Windows passa a enxergar um <b>\"DualSense Wireless Controller\"</b>, como se estivesse com cabo. Abra um jogo ou o Steam e teste.",
])
story += [box([P("<b>Dicas:</b> n\u00e3o pareie o controle pelo Bluetooth do Windows (o dongle faz isso sozinho). Se o controle estava conectado "
                 "a outro aparelho (PS5, celular), desligue o Bluetooth dele antes. Nas pr\u00f3ximas vezes basta ligar o controle com o "
                 "bot\u00e3o PS: ele reconecta sozinho.", "cell")], "ok"), Spacer(1, 6)]
story += [P("O que o LED azul da placa est\u00e1 dizendo", "h3"), img("leds", CW * 0.88, maxh=75 * mm)]
story.append(PageBreak())

# ------------------------------------------------------------------ PAGINA 5
story += [P("Usando no dia a dia", "h2"), P("O bot\u00e3o BOOT da placa tem tr\u00eas fun\u00e7\u00f5es depois de pronta:"), img("gestures", CW * 0.92, maxh=62 * mm)]
story += [P("Atalhos no controle", "h3")]
story += bullets([
    "<b>Create + Options por 3 segundos:</b> alterna entre o modo DualSense e o modo <b>Xbox 360</b> (compat\u00edvel com jogos XInput). "
    "O controle vibra e o dongle reinicia sozinho.",
    "<b>Bot\u00e3o PS:</b> pode acordar o PC do repouso (fun\u00e7\u00e3o ligada de f\u00e1brica). Depois de acordar, aperte PS de novo para reconectar.",
])
story += [P("P\u00e1gina de configura\u00e7\u00e3o (opcional)", "h3")]
story += [P("Com o dongle plugado, abra " + link("https://ps5.ds5678.top") + " no <b>Chrome ou Edge</b> e permita o acesso ao dispositivo quando o "
            "navegador pedir. L\u00e1 d\u00e1 para mudar a taxa de leitura, a for\u00e7a da h\u00e1ptica, remapear bot\u00f5es, escolher a cor da luz do "
            "controle, ligar o modo Xbox, ajustar a economia de energia e mais. A atualiza\u00e7\u00e3o online (OTA) n\u00e3o funciona nesta "
            "vers\u00e3o aberta: para atualizar, grave de novo pelo Dev Cube.")]
story += [P("Se algo n\u00e3o funcionar", "h2")]
prob = [
    [hdr("Sintoma"), hdr("O que fazer")],
    [P("O Dev Cube n\u00e3o mostra nenhuma porta COM", "cellb"), P("Cabo s\u00f3 de carga ou porta ruim. Troque o cabo/porta e refa\u00e7a o Passo 2 (BOOT apertado <b>antes</b> de ligar o cabo).", "cell")],
    [P("Gravou, mas o LED azul n\u00e3o acende", "cellb"), P("Desplugue e plugue de novo. Se persistir, refa\u00e7a a grava\u00e7\u00e3o conferindo se usou a parti\u00e7\u00e3o <b>nosec</b>.", "cell")],
    [P("O controle n\u00e3o conecta", "cellb"), P("Controle desligado? Segure PS + Create at\u00e9 piscar. Se j\u00e1 tinha conectado antes, segure o BOOT do dongle por 3 s (apaga pareamentos) e pareie de novo.", "cell")],
    [P("Depois de um tempo parado, n\u00e3o reconecta", "cellb"), P("Na p\u00e1gina de configura\u00e7\u00e3o, desligue a \"economia de energia por inatividade\".", "cell")],
    [P("Som cortando, travadinhas ou desconex\u00f5es", "cellb"), P("Use uma porta USB traseira (direto na placa-m\u00e3e) e um cabo bom e curto. Prefira o firmware FS (normal) ao HS.", "cell")],
    [P("O LED apagou sozinho", "cellb"), P("Normal: ele apaga ap\u00f3s 1 minuto. Se conectar o controle, o PC o reconhece mesmo assim.", "cell")],
]
story += [table(prob, [58 * mm, CW - 58 * mm]), Spacer(1, 6)]
story += [box([P("<b>Importante:</b> depois de gravar a v3.18 ou mais nova, <b>n\u00e3o d\u00e1 para voltar</b> a uma vers\u00e3o anterior \u00e0 3.18 "
                 "(a placa deixa de ligar; s\u00f3 recupera regravando uma vers\u00e3o nova pela porta serial).", "cell")], "warn")]
story.append(PageBreak())

# ------------------------------------------------------------------ PAGINA 6
story += [P("Case impressa em 3D", "h2")]
story += [P("Arquivos: <font name='Courier'>ds5dongle_case_base.step</font>, <font name='Courier'>ds5dongle_case_tampa.step</font> e "
            "<font name='Courier'>ds5dongle_case_botao.step</font> (o <font name='Courier'>_montada.step</font> serve s\u00f3 para visualizar). "
            "Tamanho externo: <b>50,1 x 27,1 x 9,5 mm</b>, sem pinheader, tampa por press\u00e3o (sem parafusos).")]
story += [img("section", CW * 0.92, maxh=78 * mm)]
story += [P("Corte esquem\u00e1tico. Na placa real, o conector USB-C e o bot\u00e3o BOOT ficam lado a lado, n\u00e3o um sobre o outro.", "cap")]
story += [box([P("<b>Medidas estimadas pela foto.</b> O an\u00fancio diz 25 x 20 mm, mas pelas fotos a placa tem cerca de <b>45 x 22 mm</b>. "
                 "O modelo foi feito com as medidas abaixo; <b>confira com um paqu\u00edmetro quando a placa chegar</b> e, se alguma diferir mais "
                 "de 0,5 mm, ajuste no CAD (ou refa\u00e7a o modelo).", "cell")], "warn"), Spacer(1, 4)]
meas = [
    [hdr("Medida usada no modelo"), hdr("Valor (mm)"), hdr("Medida real (preencher)")],
    [P("Comprimento da placa", "cell"), P("45,5", "cell"), P("", "cell")],
    [P("Largura da placa", "cell"), P("22,5", "cell"), P("", "cell")],
    [P("Espessura da placa", "cell"), P("1,0", "cell"), P("", "cell")],
    [P("Centro do USB-C, a partir da borda de baixo", "cell"), P("13,8", "cell"), P("", "cell")],
    [P("Altura do conector USB-C acima da placa", "cell"), P("3,2", "cell"), P("", "cell")],
    [P("Bot\u00e3o BOOT: dist\u00e2ncia do lado esquerdo / da borda de baixo", "cell"), P("6,2 / 4,7", "cell"), P("", "cell")],
    [P("Altura do bot\u00e3o BOOT acima da placa", "cell"), P("1,8", "cell"), P("", "cell")],
]
story += [table(meas, [90 * mm, 30 * mm, CW - 120 * mm]), Spacer(1, 4)]
story += [P("Impress\u00e3o e montagem", "h3")]
story += bullets([
    "<b>Teste primeiro s\u00f3 a base</b> e veja se a placa entra sem for\u00e7ar, antes de imprimir o resto.",
    "PLA ou PETG, bico 0,4 mm, camada 0,2 mm, sem suportes. Base: fundo para baixo. Tampa: de cabe\u00e7a para baixo (face externa na mesa). "
    "Bot\u00e3o: com a ponta fina (topo) para baixo.",
    "Monte assim: placa na base (USB-C no lado da abertura grande) -> bot\u00e3o vermelho encaixado por baixo da tampa, com a ponta passando pelo furo -> "
    "feche a tampa apertando. Para abrir, use o entalhe na ponta oposta ao USB.",
    "A abertura do USB-C tem 12,8 mm para caber o plug de cabos comuns. A janela da tampa mostra os LEDs.",
])

story += [Spacer(1, 4), P("Anexo: baixar tudo automaticamente (opcional, PowerShell)", "h3")]
story += [P("Alternativa ao Passo 1 para quem prefere o PowerShell. Cole o bloco inteiro: ele baixa o ZIP v3.22, extrai em "
            "<font name='Courier'>C:\\DS5Dongle</font>, confere a integridade dos arquivos e abre a pasta.", "small")]
SCRIPT = r"""& {
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $pasta = 'C:\DS5Dongle'
  $base = 'https://github.com/sqlCRT/ds5dongle-bl618-opensource/releases/download/v3.22'
  $url = "$base/ds5dongle-bl618-lctech616-v3.22.zip"
  $zip = "$pasta\fw-v3.22.zip"
  New-Item -ItemType Directory -Force -Path $pasta | Out-Null
  Invoke-WebRequest -Uri $url -OutFile $zip
  Expand-Archive -Path $zip -DestinationPath $pasta -Force
  $fw = "$pasta\ds5dongle-bl618-lctech616-v3.22"
  $esperado = [ordered]@{
    'ds5dongle-lctech616.bin' = '167e7aecaeeda52656af556485b6eeee4d7d07141cc09754dcf4e82b954655b6'
    'ds5dongle-lctech616-hs.bin' = '4c92de6a9dda8a96714bfc752bd526b9d3b63cd6b1c3d978250d718ce3ec7236'
    'boot2_bl616_isp_release_v8.1.8.bin' = '92a329c660e23f1b488a21779cebb6d5fe0ae61fd25dc00d3df7e4334192ace6'
    'partition.bin' = '99c055a2a7279c04d989a2a270106d2e2584a2d5773b57e40b3af0d87f623d12'
  }
  $ok = $true
  foreach ($nome in $esperado.Keys) {
    $h = (Get-FileHash -Algorithm SHA256 -LiteralPath "$fw\$nome").Hash.ToLower()
    if ($h -eq $esperado[$nome]) {
      Write-Host "OK         $nome" -ForegroundColor Green
    } else {
      Write-Host "DIFERENTE  $nome" -ForegroundColor Red; $ok = $false
    }
  }
  if ($ok) {
    Write-Host "Tudo certo. Arquivos em: $fw" -ForegroundColor Cyan
    Start-Process explorer.exe $fw
  } else {
    Write-Host "Algum arquivo difere do esperado. Nao grave na placa." -ForegroundColor Yellow
  }
}"""
story += [code(SCRIPT)]
story += [Spacer(1, 5), P("Projeto original: github.com/sqlCRT/ds5dongle-bl618-opensource (GPL-3.0). Base: github.com/awalol/DS5Dongle. "
                          "Se existir uma vers\u00e3o mais nova na p\u00e1gina de Releases, leia as notas antes de atualizar.", "small")]


doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=15 * mm, bottomMargin=18 * mm,
                      title="Dongle DualSense sem fio - guia passo a passo (BL616, v3.22)", author="Guia")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(M, 18 * mm, CW, H - 33 * mm, id="f", leftPadding=0,
                                                         rightPadding=0, topPadding=0, bottomPadding=0)], onPage=footer)])
doc.build(story)
print("ok")
