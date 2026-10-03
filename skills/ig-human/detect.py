#!/usr/bin/env python3
"""
detect.py - um painel de cinco checagens que dá nota a quanto um texto parece
escrito por máquina.

O que isto é:  cinco heurísticas locais, modeladas nos sinais que os
detectores públicos de IA medem: variação no tamanho das frases, concretude,
vocabulário de clichê, marcas tipográficas e voz. Toda nota é calculada na
sua máquina, só a partir do texto. Nada é enviado pra lugar nenhum.

O que isto NÃO é:  GPTZero, Originality, Copyleaks, Winston ou Turnitin. Não
chama a API deles e não tem como prometer o veredito deles. Ele pega as coisas
que todos eles observam, e é por isso que corrigir essas coisas costuma mexer
nos números deles também. A única afirmação honesta é a desta linha.

Esta versão é pra português do Brasil. Os limites de cada checagem vêm da
versão original em inglês e ainda não foram calibrados com textos
brasileiros: trate a nota como orientação, não como medida.

Cada checagem devolve uma nota HUMANA de 0 a 100. Quanto maior, melhor.

Uso
  python3 detect.py rascunho.txt
  pbpaste | python3 detect.py -
  python3 detect.py rascunho.txt --json
  python3 detect.py antes.txt depois.txt      # compara dois rascunhos
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

UPPER = "A-ZÀ-ÖØ-Þ"
LOWER = "a-zß-öø-ÿ"
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")
WORD_RE = re.compile(r"[^\W\d_]+(?:[-'’][^\W\d_]+)*")
# Fala informal brasileira. Texto de modelo escreve "para", "nós" e "está";
# gente escreve "pra", "a gente" e "tá".
INFORMAL = re.compile(
    r"\b(?:pra|pro|pras|pros|tá|tô|tava|tavam|tamo|né|cê|vc|vcs|tb|tbm|pq|"
    r"a gente|daí)\b", re.IGNORECASE)
PRONOUNS = re.compile(
    r"\b(?:eu|me|mim|meu|minha|meus|minhas|comigo|nós|nosso|nossa|nossos|nossas|"
    r"a gente|você|vocês|vc|vcs|cê|seu|sua|seus|suas|te|teu|tua|contigo)\b",
    re.IGNORECASE)
NUMBERS = re.compile(
    r"(?:R|US)?\$\s?\d|\b\d[\d.,]*%?"
    r"|(?i:\b(?:dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|"
    r"quinze|vinte|trinta|quarenta|cinquenta|cem|mil|milh[aã]o|milh[oõ]es|reais)\b)")
PROPER = re.compile(rf"(?<![.!?]\s)(?<!^)\b[{UPPER}][{LOWER}]{{2,}}\b", re.MULTILINE)
# O mesmo que o humanize.py protege: link, e-mail, hashtag e menção não são
# texto corrido, então clichê dentro deles não conta.
PROTECTED = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|(?<!\w)[#@][\w.]*\w")


def clamp(n):
    return max(0.0, min(100.0, n))


def br(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def scale(value, human, machine):
    """Leva o valor pra 0-100, com `human` -> 100 e `machine` -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def sentences(text):
    return [s.strip() for s in SENT_RE.findall(text) if len(s.split()) > 2]


def words(text):
    return WORD_RE.findall(text)


def lexicon_pattern(find):
    return re.compile(r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b", re.IGNORECASE)


def check_burstiness(text):
    """Gente varia muito o tamanho das frases. Modelo escreve tudo igual."""
    lens = [len(s.split()) for s in sentences(text)]
    if len(lens) < 4:
        return 50.0, "curto demais pra julgar"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"variação {br(cv, 2)} em {len(lens)} frases (ideal: 0,55 ou mais)"


def check_specificity(text):
    """Números, nomes e coisas concretas. Clichê é abstrato."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais pra julgar"
    per100 = 100 / len(w)
    hits = len(NUMBERS.findall(text)) + len(set(PROPER.findall(text)))
    density = hits * per100
    score = scale(density, human=6.0, machine=0.5)
    return score, (f"{hits} marcadores concretos, {br(density)} a cada 100 palavras "
                   "(ideal: 4 ou mais)")


def check_slop(text, lex):
    """Densidade de vocabulário de clichê, contra o léxico."""
    w = words(text)
    if not w:
        return 50.0, "vazio"
    # Do termo mais longo pro mais curto, apagando o que já foi contado, pra
    # "mergulhar de cabeça" não contar de novo como "mergulhar".
    work, hits, found = PROTECTED.sub(" ", text), 0, []
    for entry in sorted(lex["words"] + lex["phrases"], key=lambda e: -len(e["find"])):
        pattern = lexicon_pattern(entry["find"])
        n = len(pattern.findall(work))
        if n:
            hits += n
            found.append(entry["find"])
            work = pattern.sub(" ", work)
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} termos de clichê, {br(density)} a cada 100 palavras"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerprint(text):
    """Caracteres que um teclado de celular não produz."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—")
    curly = sum(text.count(c) for c in "‘’“”«»")
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "\u00a0\u202f\u2009")
    total = invisible * 4 + em * 2 + curly + ellip + nbsp
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} invisível, {em} travessão, {curly} aspa curva, "
              f"{ellip} reticências, {nbsp} espaço rígido")
    return score, detail


def check_voice(text, lex):
    """Fala informal, pessoa do discurso e os formatos que modelo usa por padrão."""
    w = words(text)
    if len(w) < 25:
        return 50.0, "curto demais pra julgar"
    per100 = 100 / len(w)
    informal = len(INFORMAL.findall(text)) * per100
    person = len(PRONOUNS.findall(text)) * per100
    tells = 0
    names = []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(informal, human=3.0, machine=0.0) * 0.35
             + scale(person, human=8.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("topicos-iguais")
    detail = (f"{br(informal)} marcas de fala informal, {br(person)} pronomes pessoais "
              f"a cada 100 palavras, {tells} vício(s) de estrutura")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["RITMO", "CONCRETUDE", "CLICHÊS", "DIGITAIS", "VOZ"]


def run(text, lex):
    results = {}
    results["RITMO"] = check_burstiness(text)
    results["CONCRETUDE"] = check_specificity(text)
    results["CLICHÊS"] = check_slop(text, lex)
    results["DIGITAIS"] = check_fingerprint(text)
    results["VOZ"] = check_voice(text, lex)
    scores = [results[c][0] for c in CHECKS]
    # A checagem mais fraca puxa o veredito: um detector só precisa de um sinal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "APROVADO" if overall >= 70 and min(scores) >= 55 else (
        "REVISAR" if overall >= 50 else "SINALIZADO")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "PAINEL DE DETECÇÃO DE IA" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {br(score):>5}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'NOTA HUMANA':<13} {bar(overall)} {br(overall):>5}   {verdict}", file=out)
    if verdict != "APROVADO":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Sinal mais fraco: {weakest}. Corrija esse primeiro.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota a quanto um texto parece escrito por máquina.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - pra stdin")
    ap.add_argument("compare", nargs="?", help="segundo arquivo, pra mostrar antes/depois")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        sign = "+" if delta >= 0 else "-"
        print(f"  {br(a['human_score'])} {a['verdict']}  ->  "
              f"{br(b['human_score'])} {b['verdict']}   ({sign}{br(abs(delta))})\n")

    sys.exit(0 if payload[-1]["verdict"] == "APROVADO" else 1)


if __name__ == "__main__":
    main()
