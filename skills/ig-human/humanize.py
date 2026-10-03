#!/usr/bin/env python3
"""
humanize.py - tira a digital de máquina de um rascunho.

Três passadas, nesta ordem:

  1. INVISÍVEIS  apaga ou normaliza os caracteres que um teclado de gente
                 nunca produz: separadores de largura zero, word joiners,
                 hífens suaves, BOMs, caracteres de tag Unicode, espaços
                 rígidos e estreitos. Eles sobrevivem ao copiar e colar e são
                 a marca mais mecânica de qualquer texto gerado.
  2. TIPOGRAFIA  travessão -> vírgula, meia-risca -> hífen, aspas curvas ->
                 retas, reticências de um caractere -> três pontos,
                 marcador -> hífen.
  3. LÉXICO      troca os clichês do slop.json por palavras simples,
                 preservando maiúsculas e sem mexer em links, hashtags e
                 menções. Termo com "replace": null só é sinalizado, não
                 trocado: em português, conjugação e concordância deixam
                 muita troca automática errada, e frase quebrada é pior que
                 clichê.

Vícios de estrutura ("não é só X, é Y", trios, paredão de hashtag) são
APONTADOS, nunca reescritos automaticamente. Mudar o formato de uma frase
exige julgamento, então isso é trabalho do modelo, não de uma regex.

Uso
  python3 humanize.py rascunho.txt
  python3 humanize.py rascunho.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py rascunho.txt --json
  python3 humanize.py rascunho.txt -o limpo.txt
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "slop.json")

# Links, e-mails, hashtags e menções passam intactos: trocar "#mindset" por
# "#mentalidade" muda a tag, não o texto.
URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+|(?<!\w)[#@][\w.]*\w")
SENT_RE = re.compile(r"[^.!?\n]+[.!?]*")


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> '\\u200b';  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """Troca links por marcadores pra nenhuma passada reescrever dentro deles."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Apaga ou troca por espaço os caracteres invisíveis. Devolve (texto, ocorrências)."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n,
                         "action": entry["action"]})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    # Qualquer caractere Cf (formatação) que sobrou é invisível por definição.
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "outros caracteres invisíveis de formatação", "count": len(stray),
                     "action": "delete"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex):
    hits = []
    for entry in lex["typographic"]:
        ch = entry["from"]
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n, "to": entry["to"].strip() or "(espaço)"})
        if ch == "—":
            # " palavra — palavra " e "palavra—palavra" viram vírgula + espaço.
            text = re.sub(r"\s*—\s*", ", ", text)
        elif ch == "–":
            text = re.sub(r"\s*–\s*(?=\d)", "-", text)      # 5–10  -> 5-10
            text = re.sub(r"\s+–\s+", ", ", text)            # usada como travessão
            text = text.replace("–", "-")
        else:
            text = text.replace(ch, entry["to"])
    # Vírgula inserida antes de uma pontuação que já existia fica errada.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def pass_lexical(text, lex):
    """Troca palavras e expressões de clichê. Das mais longas pras mais curtas,
    pra expressão ganhar da palavra que está dentro dela.

    Devolve (texto, trocados, sinalizados). Termo com "replace": null entra em
    sinalizados e o texto fica como estava.
    """
    hits, flagged, held = [], [], []

    def hold(m):
        held.append(m.group(0))
        return f"\x03{len(held) - 1}\x03"

    entries = sorted(lex["phrases"] + lex["words"],
                     key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        find = entry["find"]
        pattern = re.compile(r"\b" + re.escape(find).replace(r"\ ", r"\s+") + r"\b",
                             re.IGNORECASE)
        found = pattern.findall(text)
        if not found:
            continue
        if entry.get("replace") is None:
            flagged.append({"find": find, "count": len(found), "family": entry["family"]})
            # Guarda fora do texto até o fim da passada, pra uma palavra menor
            # dentro dele não ser trocada e deixar a expressão pela metade.
            text = pattern.sub(hold, text)
            continue
        hits.append({"find": find, "replace": entry["replace"] or "(apagado)",
                     "count": len(found), "family": entry["family"]})
        text = pattern.sub(lambda m: _match_case(m.group(0), entry["replace"]), text)
    text = re.sub(r"\x03(\d+)\x03", lambda m: held[int(m.group(1))], text)
    # Arruma o que sobrou das exclusões. Apagar uma oração inteira deixa
    # pontuação órfã pra trás ("sistema. ." ou uma linha que agora começa com
    # vírgula), e isso fica pior que o clichê.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)       # um espaço que sobrou de uma exclusão.
                                                      # Recuo maior é de propósito.
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)      # um travessão virou vírgula e
                                                      # depois a oração seguinte sumiu
    text = text.replace("...", "\x00ELL\x00")          # protege reticências de verdade
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Um travessão que virou vírgula, seguido de um conectivo, emenda duas
    # frases ("é importante, também, é prova"). Vira ponto final.
    text = re.sub(r",\s*(também|então|ainda|basicamente|no fim)\s*,\s*",
                  lambda m: ". " + m.group(1)[0].upper() + m.group(1)[1:] + ", ", text)
    return text, hits, flagged


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    # Frases todas do mesmo tamanho também é vício de estrutura.
    lens = [len(s.split()) for s in SENT_RE.findall(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Frases do mesmo tamanho (variação {cv:.2f})".replace(".", ","),
                "count": len(lens),
                "fix": "Quebre uma frase no meio. Deixe outra correr comprida. Máquina escreve tudo igual.",
            })
    return flags


def restore_capitals(original, text):
    """Apagar uma abertura deixa a palavra seguinte em minúscula.

    Só corrige pra quem já começa as frases com maiúscula: escrever tudo em
    minúscula de propósito é estilo, não defeito, e atropelar isso seria
    exatamente o tipo de coisa que este script existe pra evitar.
    """
    starts = re.findall(r"(?:^|[.!?]\s+|\n)\s*([A-Za-zÀ-ÖØ-öø-ÿ])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(r"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([a-zß-öø-ÿ])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex)
    text, lexi, flagged = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "flagged": flagged,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    flagged = sum(h["count"] for h in report["flagged"])
    head("RELATÓRIO DO HUMANIZADOR")
    print(f"{total} marcas de máquina removidas, {flagged} clichês sinalizados pra reescrever, "
          f"{len(report['structures'])} vícios de estrutura apontados", file=out)

    actions = {"delete": "apagado", "space": "virou espaço"}
    if report["invisible"]:
        head("1. CARACTERES INVISÍVEIS")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {actions.get(h['action'], h['action'])}",
                  file=out)
    if report["typographic"]:
        head("2. TIPOGRAFIA")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"] or report["flagged"]:
        head("3. LÉXICO DE CLICHÊS")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
        for h in report["flagged"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> (reescreva você)   [{h['family']}]",
                  file=out)
    if report["structures"]:
        head("4. VÍCIOS DE ESTRUTURA  (não corrigidos automaticamente: reescreva você)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("LIMPO")
        print("  Nada pra tirar.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Tira a digital de máquina de um rascunho.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo, ou - pra stdin")
    ap.add_argument("-o", "--out", help="grava o texto limpo aqui em vez de imprimir")
    ap.add_argument("--report", action="store_true", help="mostra o que mudou, no stderr")
    ap.add_argument("--json", action="store_true", help="devolve {text, report} em JSON")
    ap.add_argument("--lexicon", default=LEX, help="caminho do slop.json")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"gravado em {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
