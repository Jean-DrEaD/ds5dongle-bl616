import os
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------- PARAMETROS (mm) ----------------
# Placa LCTech BL616 (medidas ESTIMADAS pela foto do anuncio; conferir com paquimetro)
L, W, T = 45.5, 22.5, 1.0          # comprimento, largura, espessura da PCB
usb_y = 13.8                        # centro do USB-C a partir da borda de baixo da PCB
usb_h = 3.2                         # altura do conector USB-C acima da PCB
boot_x, boot_y = 6.2, 4.7           # botao BOOT a partir do canto esquerdo/baixo da PCB
sw_h = 1.8                          # altura do botao BOOT acima da PCB
led_x, led_y = 19.9, 21.1           # LEDs a partir do canto esquerdo/baixo da PCB

# Case
c = 0.3          # folga em volta da PCB
wall = 2.0       # parede
usbw = 2.0       # parede do lado USB
floor = 1.0      # fundo
under = 1.0      # espaco sob a PCB (componentes do verso)
ledge = 1.2      # largura do apoio da PCB
zlid = 8.3       # altura onde a tampa assenta
plate = 1.2      # espessura da tampa
step_h = 2.5     # altura do degrau/saia
s = 1.0          # recuo do degrau
tol = 0.15       # folga do encaixe tampa/base
R = 2.0          # raio dos cantos

usb_open_w = 12.8   # abertura para o plug (corpo do plug USB-C ate 12,35 mm)

zb0 = floor + under          # face de baixo da PCB
ztop = zb0 + T               # face de cima da PCB
bx0 = usbw + c               # PCB: x minimo
by0 = wall + c               # PCB: y minimo
Lo = usbw + L + 2 * c + wall
Wo = 2 * wall + W + 2 * c


def rbox(x0, y0, lx, ly, z0, h, r):
    wp = cq.Workplane("XY").workplane(offset=z0).center(x0 + lx / 2, y0 + ly / 2).rect(lx, ly).extrude(h)
    if r > 0:
        wp = wp.edges("|Z").fillet(r)
    return wp


def box(x0, y0, z0, lx, ly, lz):
    return cq.Workplane("XY").box(lx, ly, lz, centered=False).translate((x0, y0, z0))


# ---------------- BASE ----------------
base = rbox(0, 0, Lo, Wo, 0, zlid, R)
# degrau externo (a saia da tampa encaixa aqui)
ring = rbox(0, 0, Lo, Wo, zlid - step_h, step_h, R).cut(
    rbox(s, s, Lo - 2 * s, Wo - 2 * s, zlid - step_h, step_h, R - s))
base = base.cut(ring)
# cavidade da PCB
base = base.cut(rbox(usbw, wall, L + 2 * c, W + 2 * c, zb0, zlid, 0.5))
# cavidade sob a PCB (deixa apoio em volta)
base = base.cut(rbox(bx0 + ledge, by0 + ledge, L - 2 * ledge, W - 2 * ledge, floor, under + 0.01, 0.5))
# abertura USB-C
uy = by0 + usb_y
usb_cut = box(-1, uy - usb_open_w / 2, floor, usbw + 1.3, usb_open_w, zlid + 2).edges("|X and <Z").fillet(1.0)
base = base.cut(usb_cut)

# ---------------- TAMPA ----------------
lid = rbox(0, 0, Lo, Wo, zlid, plate, R)
skirt = rbox(0, 0, Lo, Wo, zlid - step_h, step_h, R).cut(
    rbox(s - tol, s - tol, Lo - 2 * (s - tol), Wo - 2 * (s - tol), zlid - step_h, step_h, R - (s - tol)))
lid = lid.union(skirt)
# recorte da saia na abertura USB e ponto de alavanca na outra ponta
lid = lid.cut(box(-1, uy - usb_open_w / 2, zlid - step_h - 0.1, 2.2, usb_open_w, step_h + 0.1))
lid = lid.cut(box(Lo - 1.5, Wo / 2 - 4, zlid - step_h - 0.1, 2.5, 8, step_h + 0.1))
# janela dos LEDs
lx, ly = bx0 + led_x, by0 + led_y
lid = lid.cut(cq.Workplane("XY").workplane(offset=zlid - 0.1).center(lx, ly).slot2D(5.0, 2.4).extrude(plate + 0.2))
# furo do botao BOOT
kx, ky = bx0 + boot_x, by0 + boot_y
lid = lid.cut(cq.Workplane("XY").workplane(offset=zlid - 0.1).center(kx, ky).circle(1.7).extrude(plate + 0.2))
# 4 batentes que seguram a PCB nos cantos
lug = 1.5
for (px, py) in [(bx0 + 0.2, by0 + 0.2), (bx0 + 0.2, by0 + W - 0.2 - lug),
                 (bx0 + L - 0.2 - lug, by0 + 0.2), (bx0 + L - 0.2 - lug, by0 + W - 0.2 - lug)]:
    lid = lid.union(box(px, py, ztop + 0.2, lug, lug, zlid - (ztop + 0.2) + 0.01))

# ---------------- BOTAO (plunger) ----------------
zsw = ztop + sw_h + 0.2                      # ponta do botao fica 0,2 mm acima do switch
plunger = (cq.Workplane("XY").workplane(offset=zsw).center(kx, ky).circle(1.3).extrude(zlid - 0.8 - zsw)
           .faces(">Z").workplane().circle(2.7).extrude(0.8)
           .faces(">Z").workplane().circle(1.5).extrude(plate + 1.0))
# a flange fica logo abaixo da tampa; o botao sobressai 1 mm acima da tampa

if __name__ == "__main__":
    out = os.path.join(HERE, "saida")
    os.makedirs(out, exist_ok=True)
    cq.exporters.export(base, f"{out}/ds5dongle_case_base.step")
    cq.exporters.export(lid, f"{out}/ds5dongle_case_tampa.step")
    cq.exporters.export(plunger, f"{out}/ds5dongle_case_botao.step")
    asm = cq.Assembly(name="ds5dongle_case")
    asm.add(base, name="base", color=cq.Color(0.15, 0.15, 0.18))
    asm.add(lid, name="tampa", color=cq.Color(0.3, 0.3, 0.35))
    asm.add(plunger, name="botao", color=cq.Color(0.8, 0.2, 0.2))
    asm.save(f"{out}/ds5dongle_case_montada.step")
    for n, o in [("base", base), ("lid", lid), ("plunger", plunger)]:
        s_ = o.val()
        bb = s_.BoundingBox()
        print(n, "valido:", s_.isValid(), "vol: %.1f mm3" % s_.Volume(),
              "bbox: %.1f x %.1f x %.1f" % (bb.xlen, bb.ylen, bb.zlen))
