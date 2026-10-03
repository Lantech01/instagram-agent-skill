#!/usr/bin/env python3
"""
beats.py - transforma um roteiro de Reels num roteiro cronometrado antes de
você gravar.

Estima quanto tempo cada frase leva pra ser dita, empilha tudo em minutagem e
aponta as quatro coisas que matam um Reels na edição: um gancho que passa da
marca de três segundos, uma batida longa o bastante pra pessoa ir embora, uma
sequência de frases sem nada concreto, e uma duração que não bate com o que
você disse que ia fazer.

Os tempos são uma estimativa pela contagem de palavras num ritmo de palavras
por minuto (ppm). Servem pra planejar a edição, não substituem gravar. O
padrão é 165 ppm. Calibre com --ppm depois de cronometrar você mesmo lendo um
roteiro em voz alta: palavra em português costuma ser mais comprida que em
inglês, e o seu ritmo é o que vale.

Uso
  python3 beats.py roteiro.txt
  python3 beats.py roteiro.txt --target 30
  python3 beats.py roteiro.txt --ppm 150 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py roteiro.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[$]?[^\W_](?:[^\W_]|[$%'’-])*")
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
UPPER = "A-ZÀ-ÖØ-Þ"
LOWER = "a-zß-öø-ÿ"
# Concreto: dinheiro, um número com dígitos, ou um nome próprio no meio da
# frase (a primeira palavra de cada frase não conta).
CONCRETE_RE = re.compile(
    rf"(?:R|US)?\$\s?\d|\b\d[\d.,]*\b|(?<![.!?]\s)(?<!^)\b[{UPPER}][{LOWER}]{{2,}}\b",
    re.MULTILINE)
# Número falado também é concreto: "cinco horas" é tão checável quanto "5h".
SPOKEN_NUMBERS = {
    "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "treze", "catorze", "quatorze",
    "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte",
    "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta",
    "noventa", "cem", "cento", "duzentos", "duzentas", "trezentos", "trezentas",
    "quatrocentos", "quatrocentas", "quinhentos", "quinhentas", "seiscentos",
    "seiscentas", "setecentos", "setecentas", "oitocentos", "oitocentas",
    "novecentos", "novecentas", "mil",
    "milhão", "milhões", "bilhão", "bilhões", "dúzia", "metade", "dobro",
    "triplo", "reais",
}
# Palavras que não contam como eco entre o gancho e o final.
STOPWORDS = {
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "e", "ou", "mas", "se",
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "num",
    "numa", "por", "pelo", "pela", "pelos", "pelas", "para", "pra", "pro",
    "pras", "pros", "com", "sem", "sobre", "que", "quem", "qual", "como",
    "quando", "onde", "porque", "isso", "isto", "esse", "essa", "este",
    "esta", "aquele", "aquela", "ele", "ela", "eles", "elas", "eu", "me",
    "mim", "meu", "minha", "meus", "minhas", "você", "vc", "te", "seu", "sua",
    "seus", "suas", "nós", "nosso", "nossa", "gente", "é", "era", "foi",
    "ser", "são", "está", "tá", "tô", "estou", "tem", "ter", "tinha", "vai",
    "vou", "já", "só", "não", "sim", "também", "mais", "muito", "muita", "aí",
    "lá", "aqui", "então", "né", "tipo", "ao", "aos", "à", "às", "lhe",
}

HOOK_WINDOW = 3.0        # segundos. Depois disso, o dedão já decidiu.
MAX_BEAT = 4.0           # segundos numa ideia só, sem nada mudar na tela.
ABSTRACT_RUN = 3         # batidas seguidas sem nada checável.


def br(x, nd=1):
    """Número no formato brasileiro: vírgula decimal."""
    return f"{x:.{nd}f}".replace(".", ",")


def words(text):
    # "R$ 18.000" é dito como um valor só, então conta como uma palavra só.
    text = re.sub(r"(?<=\d)[.,](?=\d)", "", text)
    text = re.sub(r"((?:R|US)\$)\s+(?=\d)", r"\1", text)
    return WORD_RE.findall(text)


def pretty(token):
    """Devolve o separador de milhar pra exibição."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1.", token)


def concrete(text):
    spoken = sum(1 for w in words(text) if w.lower() in SPOKEN_NUMBERS)
    return len(CONCRETE_RE.findall(text)) + spoken


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{br(s).zfill(4)}"


def split_beats(raw, wps):
    """Uma linha é uma batida, a não ser que a linha seja longa demais pra isso."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Parágrafo longo: quebra no fim das frases pra minutagem fazer
        # sentido, e o relatório mostra que foi quebrado.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": concrete(text),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Marca as posições em torno das quais um Reels é construído.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "GANCHO"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "GANCHO" else "GANCHO/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MEIO"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"o gancho leva {br(rows[0]['dur'])}s, passa da marca de "
                                f"{HOOK_WINDOW:.0f}s")
        notes.append(f"A batida 1 leva {br(rows[0]['dur'])}s pra ser dita. Corte pra "
                     f"{int(HOOK_WINDOW * wps)} palavras ou menos, ou o gancho chega depois "
                     "que a decisão já foi tomada.")
    if rows[0]["concrete"] == 0:
        notes.append("A batida 1 não tem número nem nome. Gancho sem nada verificável é o "
                     "que a pessoa passa.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{br(r['dur'])}s numa batida só")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Batida(s) {', '.join(map(str, long_beats))} passam de "
                     f"{MAX_BEAT:.0f}s. Divida a frase ou mude o que está na tela no meio "
                     "dela. Quadro parado é onde as pessoas saem.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"As batidas {start}-{r['n']} não têm nada concreto. Coloque "
                             "um número, um nome ou um preço em uma delas.")
        else:
            run, start = 0, None

    # A última frase devolve a pessoa pra primeira?
    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Loop: a última batida repete \"{', '.join(loop[:3])}\" do gancho. "
                     "Segunda visualização é alcance de graça.")
    else:
        notes.append("Sem loop. A última batida não repete nenhuma palavra do gancho, então "
                     "o vídeo termina seco. Repetir uma palavra da batida 1 é o replay mais "
                     "barato que existe.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Duração dentro da meta ({br(total)}s para {target:g}s).")
        elif delta > 0:
            notes.append(f"{br(delta)}s acima da meta. Corte umas {int(delta * wps)} palavras.")
        else:
            notes.append(f"{br(-delta)}s abaixo da meta. Acrescente {int(-delta * wps)} "
                         "palavras ou grave mais curto. Mais curto costuma ser o certo.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"ROTEIRO CRONOMETRADO  ·  {a['total_words']} palavras  ·  "
            f"~{br(a['total_seconds'])}s a {a['wpm']:g} ppm"
            + (f"  ·  meta {a['target']:g}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 76), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<11}" if r["label"] else " " * 11
        print(f"  {tc(r['start'])}  {br(r['dur']):>4}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<11}^ {f}", file=out)
    print("-" * max(len(head), 76), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Cronometra um roteiro de Reels batida por batida.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo do roteiro, ou - pra stdin")
    ap.add_argument("--ppm", "--wpm", dest="wpm", type=float, default=165,
                    help="ritmo de fala em palavras por minuto (padrão 165)")
    ap.add_argument("--target", "--meta", dest="target", type=float,
                    help="duração alvo em segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("roteiro vazio", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
