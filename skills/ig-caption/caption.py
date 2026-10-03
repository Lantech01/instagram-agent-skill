#!/usr/bin/env python3
"""
caption.py - revisa uma legenda de Instagram e mostra exatamente o que o feed
mostra antes do "... mais".

O Instagram mostra uns 125 caracteres da legenda no feed e esconde o resto
atrás de um toque. Quase toda legenda que falha, falha ali: o gancho está na
terceira frase, ou a primeira linha é um "oi, gente", ou a legenda inteira
abre com hashtag. Este script imprime a janela visível numa caixa, pra você
ler como um estranho rolando o feed lê, e depois faz as checagens que valem a
pena fazer.

O corte em 125 caracteres é uma aproximação. O número real muda com o
aparelho, o tamanho da fonte e onde caem as quebras de linha, e é exatamente
por isso que você quer uma margem, e não uma legenda calculada pra terminar
no 125. Mude com --truncate se quiser testar um corte mais apertado.

Publi: se o post é publicidade, passe --publi. O Código do CONAR (art. 28)
diz que anúncio tem que ser claramente identificado como anúncio. Este script
só confere se a marcação ("publi", "publicidade", "parceria paga"...) aparece
antes do "... mais". Não é parecer jurídico.

Uso
  python3 caption.py legenda.txt
  python3 caption.py legenda.txt --keywords "contrato de prestação de serviço,precificação"
  python3 caption.py legenda.txt --publi
  pbpaste | python3 caption.py -
  python3 caption.py legenda.txt --json
"""

import argparse
import json
import re
import sys
import textwrap

LIMIT = 2200             # Limite de caracteres de legenda do Instagram.
TRUNCATE = 125           # Mais ou menos onde o feed corta pro "... mais".
HASHTAG_LIMIT = 5        # Limite de hashtags por post ou Reels desde 18 de
                         # dezembro de 2025 (era 30). Anunciado pela conta
                         # @Creators: menos hashtags (até 5) e mais
                         # específicas, em vez de muitas genéricas.

UPPER = "A-ZÀ-ÖØ-Þ"
LOWER = "a-zß-öø-ÿ"
HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[\w.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+"
                     r"|\b[a-z0-9-]+\.(?:com\.br|com|co|io|net|org|ai|app|br)/\S*"
                     r"|\b[a-z0-9-]+\.com\.br\b",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(
    rf"(?:R|US)?\$\s?\d|\b\d[\d.,]*\b|(?<![.!?]\s)(?<!^)\b[{UPPER}][{LOWER}]{{2,}}\b",
    re.MULTILINE)
SPOKEN_NUMBERS_RE = re.compile(
    r"(?i)\b(?:dois|duas|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|"
    r"treze|catorze|quatorze|quinze|dezesseis|dezessete|dezoito|dezenove|vinte|"
    r"trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa|cem|cento|mil|"
    r"milh[aã]o|milh[oõ]es|reais)\b")
PUBLI_RE = re.compile(
    r"(?i)#?\bpubli\b|#?\bpublicidade\b|#?\bpublipost\b|\bparceria paga\b|#parceriapaga\b"
    r"|\bpatrocinad[oa]\b|\bconte[uú]do pago\b|#ad\b")

# Pedidos (CTAs). A palavra-chave de "comenta X" tem que estar em maiúsculas,
# que é como ela aparece de verdade: "comenta EU QUERO", "comenta TABELA".
ASKS = [
    (re.compile(rf"(?i:\bcomenta(?:r|e)?)\s+(?:(?i:a palavra)\s+|\")?[{UPPER}0-9]{{2,}}\b"),
     "comentar uma palavra-chave"),
    (re.compile(r"(?i)\bme (?:chama|manda|chame|mande)\b(?: (?:uma|um))?"
                r"(?: (?:dm|direct|mensagem|msg|inbox))?|\b(?:manda|mande|chama) (?:uma )?"
                r"(?:dm|direct|mensagem|msg)\b|\bno direct\b|\bna dm\b"),
     "chamar na DM"),
    (re.compile(r"(?i)\bsalv(?:a|e|ar) (?:esse|este|o|a|pra|para|já)\b"), "salvar"),
    (re.compile(r"(?i)\bcompartilh(?:a|e|ar)\b|\bmanda (?:pra|para) (?:algu[eé]m|aquele|aquela|"
                r"um amigo|uma amiga|quem)\b|\bmarca (?:algu[eé]m|aquele|aquela|um amigo|"
                r"uma amiga|quem)\b"),
     "compartilhar ou marcar"),
    (re.compile(r"(?i)\bsegue (?:pra|para) mais\b|\bme segue\b|\bsiga (?:o perfil|a gente|@|"
                r"pra|para)|\bsegue o perfil\b|\bsegue a gente\b|\bsegue @"),
     "seguir"),
    (re.compile(r"(?i)\blink (?:na|da) bio\b"), "link na bio"),
    (re.compile(r"(?i)\barrast(?:a|e) (?:pro|para o|pra) (?:lado|direita|esquerda)\b"
                r"|\bdesliz(?:a|e)\b"),
     "arrastar pro lado"),
    (re.compile(r"(?i)\bme (?:conta|diz|fala)\b|\bo que voc[eê] (?:faria|acha)\b"
                r"|\bqual (?:voc[eê]|deles|delas|desses|dessas)\b"),
     "responder uma pergunta"),
]

FILLER_TAGS = {
    "#viral", "#fyp", "#explore", "#explorepage", "#explorar", "#foryou",
    "#foryoupage", "#paravoce", "#pravoce", "#trending", "#trend",
    "#instagood", "#love", "#amor", "#follow", "#like4like", "#reels",
    "#reelsinstagram", "#viralreels", "#instadaily", "#brasil",
    "#instabrasil", "#seguidores", "#curtidas", "#sigoevolto", "#sdv",
    "#viralizou", "#viralizar", "#foto", "#instagram",
}


def br(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def concrete_count(text):
    return len(CONCRETE_RE.findall(text)) + len(SPOKEN_NUMBERS_RE.findall(text))


def visible_window(text, cut):
    """O que o feed mostra. O Instagram corta no meio da palavra, então aqui também."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  O QUE O FEED MOSTRA", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... mais" if truncated else "(a legenda inteira aparece)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None, publi=False):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("TAMANHO", "FALHA" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} caracteres" + (f", {chars - LIMIT} acima do limite"
                                           if chars > LIMIT else ""))

    if not first_line:
        add("PRIMEIRA LINHA", "FALHA", "a legenda abre com uma linha em branco")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("PRIMEIRA LINHA", "FALHA",
            "abre com hashtag ou menção, na única posição que vale uma frase")
    elif len(first_line) > cut:
        add("PRIMEIRA LINHA", "AVISO",
            f"{len(first_line)} caracteres, então é cortada no {cut} no meio da ideia. "
            "Tudo bem se o corte for um suspense, ruim se for uma oração subordinada")
    else:
        add("PRIMEIRA LINHA", "OK", f"{len(first_line)} caracteres, aparece inteira")

    n_concrete = concrete_count(window)
    add("GANCHO CONCRETO", "OK" if n_concrete else "AVISO",
        f"{n_concrete} número(s) ou nome(s) na janela visível"
        + ("" if n_concrete else " - nada verificável antes do toque"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FALHA", f"{len(tags)} tags, acima do limite de {HASHTAG_LIMIT} do "
                                 "Instagram. Tag depois da quinta não conta e o bloco "
                                 "parece velho")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} tags, no limite, e {len(filler)} delas "
                                 "genéricas. Gaste as cinco em assunto")
    elif filler:
        add("HASHTAGS", "AVISO", f"{len(tags)} tags, {len(filler)} delas genéricas "
                                 f"({', '.join(filler[:3])}). Essas não descrevem nada")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} tag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("LUGAR DAS TAGS", "OK", "nenhuma tag pra posicionar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("LUGAR DAS TAGS", "AVISO", "tem hashtag dentro da janela visível, gastando "
                                       "espaço do feed com etiqueta")
    else:
        add("LUGAR DAS TAGS", "OK", "as tags estão depois do corte")

    add("LINKS", "AVISO" if links else "OK",
        f"{len(links)} link(s) na legenda, e link em legenda não é clicável. "
        f"Leve pra bio ou pra DM" if links else "nenhum link morto no texto")

    if len(asks) == 1:
        add("UM PEDIDO", "OK", f"uma chamada pra ação: {asks[0]}")
    elif not asks:
        add("UM PEDIDO", "AVISO", "nenhuma chamada pra ação. Decida pra que serve esse post")
    else:
        add("UM PEDIDO", "AVISO", f"{len(asks)} pedidos ({', '.join(asks)}). "
                                  "Dois pedidos é o mesmo que nenhum")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "AVISO" if density > 4 else "OK",
        f"{len(emoji)} emoji, {br(density)} por 100 caracteres"
        + (" - vira decoração" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("AVISO" if found else "FALHA")
        add("BUSCA", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} na janela visível" if found else "")
            + (f". Faltando: {', '.join(missing)}" if missing else ""))

    disclosed_anywhere = bool(PUBLI_RE.search(stripped))
    disclosed_visible = bool(PUBLI_RE.search(window))
    if publi or disclosed_anywhere:
        if disclosed_visible:
            add("PUBLI", "OK", "a marcação de publicidade aparece antes do \"... mais\"")
        elif disclosed_anywhere:
            add("PUBLI", "AVISO", "a marcação de publicidade só aparece depois do \"... mais\". "
                                  "Publicidade tem que ser identificada com clareza (CONAR, "
                                  "art. 28): suba pra primeira linha")
        else:
            add("PUBLI", "FALHA", "o post é publi, mas a legenda não diz. Escreva \"publi\" ou "
                                  "\"publicidade\" na primeira linha e use a marcação de "
                                  "parceria paga do Instagram")

    fails = sum(1 for c in checks if c["status"] == "FALHA")
    warns = sum(1 for c in checks if c["status"] == "AVISO")
    verdict = "CORRIGIR" if fails else ("REVISAR" if warns else "PRONTA")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"LEGENDA  ·  {a['characters']} / {a['limit']} caracteres  ·  "
            f"{len(a['hashtags'])} hashtags  ·  {len(a['asks'])} pedido(s)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<5} {c['check']:<16} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  VEREDITO  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisa uma legenda de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo da legenda, ou - pra stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"caracteres mostrados antes do '... mais' (padrão {TRUNCATE})")
    ap.add_argument("--keywords", default="",
                    help="termos separados por vírgula pelos quais você quer ser encontrado")
    ap.add_argument("--publi", action="store_true",
                    help="o post é publicidade: confere se isso está dito antes do '... mais'")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","), publi=args.publi)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "PRONTA" else 1)


if __name__ == "__main__":
    main()
