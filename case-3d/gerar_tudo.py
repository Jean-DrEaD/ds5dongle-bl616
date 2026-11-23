"""Gera a case 3D (STEP) e o LEIA-ME em PDF. Uso:  py gerar_tudo.py
Tudo sai na pasta 'saida'. Instala sozinho o que faltar."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def pip(*pacotes):
    base = [sys.executable, "-m", "pip", "install", "-q", *pacotes]
    if subprocess.call(base) != 0:  # alguns Linux exigem esta opcao
        subprocess.call(base + ["--break-system-packages"])

def etapa(nome, arq):
    print(f"\n=== {nome} ===")
    ok = subprocess.call([sys.executable, arq]) == 0
    print("OK" if ok else "FALHOU (veja a mensagem acima)")
    return ok

print("Instalando dependencias (so demora na 1a vez)...")
pip("reportlab", "matplotlib", "numpy", "pillow")
pip("cadquery")
os.makedirs("saida", exist_ok=True)
r = [etapa("1/3 Case 3D (arquivos STEP)", "case.py"),
     etapa("2/3 Ilustracoes", "figs.py"),
     etapa("3/3 LEIA-ME em PDF", "build_pdf.py")]
print("\nPronto! Arquivos em:", os.path.join(HERE, "saida"))
if not r[0]:
    print("Aviso: o CadQuery nao instalou (precisa de Python 3.9 a 3.12). O PDF foi gerado mesmo assim.")
