#!/usr/bin/env python3
"""
hookscore.py - dá nota à primeira frase de um Reels nas cinco coisas que os
ganchos fortes têm em comum, e ranqueia um lote deles entre si.

O que isto é:  cinco heurísticas locais, calculadas na sua máquina, só a partir
do texto. Elas medem propriedades que ganchos que seguram a atenção costumam
ter: um tamanho que dá pra falar em menos de três segundos, um marcador
concreto, alguma coisa em jogo, o conteúdo na frente e não no fim, e alguém
do outro lado pra quem a frase é dita.

O que isto NÃO é:  um previsor de views. A versão original, em inglês, foi
testada contra 74 ganchos reais de vídeos curtos. Separar um gancho real de um
escrito pra ser ruim ela fez bem (AUC 0,83). Separar os acertos de um criador
dos fracassos do mesmo criador ela quase não fez (AUC 0,56, onde 0,50 é cara
ou coroa).

Esta versão em português do Brasil usa as mesmas cinco checagens com listas
de palavras em português. Ela ainda NÃO foi medida contra ganchos brasileiros
reais, então os números acima não valem automaticamente pra ela.

Use pro que foi medido: ela pega saudação, preâmbulo, gancho sem nada concreto
e gancho que leva cinco segundos pra ser dito. Ela não diz qual de dois
ganchos bons vai rodar, e nada que lê texto consegue, porque isso depende do
seu rosto, da sua edição, do seu áudio e de pra quem o Instagram mostra.
Confie mais no gráfico de retenção do que neste script.

Cada checagem vai de 0 a 100. Quanto maior, melhor.

Uso
  python3 hookscore.py ganchos.txt            # um gancho por linha, ranqueados
  python3 hookscore.py --hook "Uma cláusula me custou R$ 18 mil."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py ganchos.txt --json
"""

import argparse
import json
import re
import statistics
import sys

# Uma palavra é uma sequência de letras (com acento) ou dígitos. "$", "%",
# apóstrofo e hífen podem aparecer dentro dela: "R$4200", "12%", "guarda-chuva".
WORD_RE = re.compile(r"[$]?[^\W_](?:[^\W_]|[$%'’-])*")
UPPER = "A-ZÀ-ÖØ-Þ"
LOWER = "a-zß-öø-ÿ"
NUMBER_RE = re.compile(
    r"(?:R|US)?\$\s?\d[\d.,]*"                          # dinheiro
    r"|\b\d[\d.,]*\s?"                                   # um número, com
    r"(?:%|k\b|mil\b|mi\b|x\b|h\b|hs\b|horas?\b"        # ou sem unidade
    r"|min\b|minutos?\b|dias?\b|semanas?\b|m[eê]s\b|meses\b|anos?\b)?",
    re.IGNORECASE)
# Nome próprio: maiúscula no meio da frase. A primeira palavra da frase não
# conta, porque toda frase começa com maiúscula.
PROPER_RE = re.compile(rf"(?<![.!?]\s)(?<!^)\b[{UPPER}][{LOWER}]{{2,}}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
PRICE_RE = re.compile(r"(?:R|US)?\$\s?\d")

# Gancho falado diz o número em voz alta. "Dezoito mil reais" é tão concreto
# quanto "R$ 18.000", e contar só dígitos deixava isso passar. "Um", "uma",
# "primeiro" e "zero" ficam de fora de propósito: são artigo, enchimento ou
# expressão ("do zero") muito mais vezes do que são quantidade.
SPOKEN_NUMBERS = {
    "dois", "duas", "três", "tres", "quatro", "cinco", "seis", "sete",
    "oito", "nove", "dez", "onze", "doze", "treze", "catorze", "quatorze",
    "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte",
    "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta",
    "noventa", "cem", "cento", "duzentos", "trezentos", "quinhentos", "mil",
    "milhão", "milhao", "milhões", "milhoes", "bilhão", "bilhões", "dúzia",
    "metade", "dobro", "triplo", "dezenas", "centenas",
}
MONEY_WORDS = {
    "reais", "conto", "contos", "pila", "pilas", "dólar", "dólares",
    "centavos", "porcento", "faturamento", "faturei", "faturou", "lucro",
    "lucrei", "salário", "aluguel", "milionário", "milionária", "prejuízo",
}

# Palavras que colocam alguma coisa em jogo. Um gancho sem nenhuma delas é uma
# afirmação; um gancho com uma é um motivo pra continuar assistindo.
STAKES = {
    "pare", "nunca", "errado", "errada", "erro", "erros", "errei",
    "errando", "perdi", "perdeu", "perder", "perdendo", "perde", "custou",
    "custa", "custava", "custo", "caro", "quebrei", "quebrou", "faliu",
    "falhei", "falhou", "fracasso", "fracassei", "ninguém", "ninguem", "não",
    "nao", "nem", "sem", "parei", "desisti", "demitido", "demitida",
    "apaguei", "apague", "apaga", "matou", "mata", "substituiu", "substitui",
    "troquei", "cortei", "corta", "corte", "grátis", "graça", "paguei",
    "pagava", "cobrei", "cobrava", "contratei", "economizei", "primeiro",
    "primeira", "proibido", "proibida", "ilegal", "pior", "piores", "odeio",
    "odiava", "desperdicei", "desperdício", "jogando", "golpe", "mentira",
    "menti", "mentiram", "verdade", "segredo", "escondido", "escondem",
    "roubei", "roubaram", "antes", "até", "mas", "exceto", "problema",
    "risco", "perigo", "cuidado", "arrependo", "arrependi", "deveria", "devia",
    "ainda", "já", "só", "apenas", "versus", "vs", "dívida", "devolução",
    "devoluções", "cancelou", "cancelaram", "multa", "bloqueado",
    "bloqueada",
}

# Aberturas que gastam o primeiro segundo sem dizer nada. Comparadas palavra
# por palavra com o começo do gancho.
WEAK_OPENERS = [
    "então", "entao", "bom", "ok", "olá", "ola", "oi", "e aí", "eai", "e ai",
    "gente", "galera", "pessoal", "fala", "salve", "bom dia", "boa tarde",
    "boa noite", "hoje", "basicamente", "sinceramente", "olha", "olhe",
    "escuta", "seguinte", "o seguinte", "tipo", "né", "assim", "enfim",
    "deixa eu", "vamos", "bora", "eu queria", "eu quero", "eu vou", "vou",
    "um dos", "uma das", "você sabia", "vocês sabiam", "sabia que",
    "já pensou", "você já", "neste", "nesse", "no vídeo", "no reels",
    "a questão", "o negócio", "muita gente", "existe", "existem", "isso é",
    "esse é", "essa é", "quando se", "se você já", "como vocês",
]

# Imperativos que merecem a primeira posição.
# "Para" sozinho é quase sempre preposição ("para quem vende..."), então só
# "para de" conta como ordem. Ver stop_command().
IMPERATIVES = {
    "pare", "rouba", "roube", "copia", "copie", "apaga", "apague",
    "testa", "teste", "tenta", "tente", "assiste", "assista", "olha", "olhe",
    "lê", "leia", "salva", "salve", "usa", "use", "faz", "faça", "monta",
    "monte", "escreve", "escreva", "manda", "mande", "pega", "pegue",
    "começa", "comece", "larga", "largue", "nunca", "sempre", "não",
    "confere", "confira", "esquece", "esqueça", "troca", "troque", "corta",
    "corte",
}

# Em português o sujeito fica escondido no verbo: "Perdi R$ 18 mil" é
# primeira pessoa sem nenhum "eu". Formas comuns, mais as terminações do
# pretérito ("-ei": comprei, errei) e da primeira do plural ("-amos": cortamos).
FIRST_PERSON_VERBS = {
    "sou", "estou", "tô", "to", "era", "fui", "tenho", "tinha", "tive",
    "vou", "fiz", "faço", "sei", "dei", "vi", "li", "quis", "pude", "perdi",
    "vendi", "decidi", "descobri", "aprendi", "consegui", "abri", "escrevi",
    "recebi", "percebi", "entendi", "resolvi", "devolvi", "vivi", "corri",
    "temos", "somos", "fomos", "vamos", "estamos", "fizemos", "tivemos",
}


def first_person_verb(lw):
    return any(t in FIRST_PERSON_VERBS
               or (len(t) >= 5 and t.endswith("ei"))
               or (len(t) >= 6 and t.endswith(("amos", "emos", "imos")))
               for t in lw)


DEALBREAKERS = [
    (re.compile(r"(?i)^\s*(?:para|pare) de (?:rolar|passar|pular)|^\s*n[aã]o (?:passa|pula|role|rola)\b"),
     "Abre com \"para de rolar o feed\". Pedir atenção prova que você ainda não conquistou."),
    (re.compile(r"(?i)\b(?:neste|nesse|no) (?:v[ií]deo|reels?|post)(?: de hoje)?\b"
                r"|\bvou te (?:mostrar|ensinar|contar)\b|\bhoje (?:eu )?vou\b"),
     "Preâmbulo de vídeo. Apague e abra direto no que importa."),
    (re.compile(r"(?i)^\s*(?:oi|ol[aá]|e a[ií]|eai|fala,? (?:galera|pessoal|gente)|salve|"
                r"bom dia|boa tarde|boa noite|tudo bem)\b"),
     "Saudação. Ninguém abriu o feed pra ser cumprimentado."),
    (HASHTAG_RE,
     "Hashtag no gancho. Hashtag vai no fim da legenda, se for em algum lugar."),
    (EMOJI_RE,
     "Emoji no gancho. Texto na tela no tamanho de gancho tem espaço pra palavra ou pra emoji, não pros dois."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def br(x, nd=1):
    """Número no formato brasileiro: vírgula decimal."""
    return f"{x:.{nd}f}".replace(".", ",")


def words(text):
    # "R$ 18.000" é dito como um valor só, então conta como uma palavra só.
    text = re.sub(r"(?<=\d)[.,](?=\d)", "", text)
    text = re.sub(r"((?:R|US)\$)\s+(?=\d)", r"\1", text)
    return WORD_RE.findall(text)


def lower_words(text):
    return [w.lower().strip("'’") for w in words(text)]


def stop_command(text):
    """"Para de ..." no começo é ordem, não preposição."""
    return bool(re.match(r"(?i)\s*para de\b", text))


def check_length(text):
    """O gancho tem que chegar antes do dedão se mexer. Uns dois segundos."""
    n = len(words(text))
    secs = n / 2.75                      # ~165 palavras por minuto, falado
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # duas linhas de texto grande na tela
        score -= 12
    return clamp(score), (f"{n} palavras, {chars} caracteres, ~{br(secs)}s falado "
                          "(ideal: 5 a 12 palavras)")


def check_specificity(text):
    """Uma coisa concreta vale mais que três abstratas."""
    nums = [n.strip().rstrip(".,") for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = lower_words(text)
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    if re.search(r"(?i)\bpor cento\b", text):
        spoken.append("por cento")
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - nenhum número, nenhum nome, nada verificável"))


def check_stakes(text):
    """Tensão, custo, negação. Alguma coisa que quem assiste pode perder."""
    markers = sorted({w for w in lower_words(text) if w in STAKES})
    if re.search(r"(?i)\bpara de\b", text):
        markers.append("para de")
    if PRICE_RE.search(text):
        markers.append("um preço")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensão" + (f": {', '.join(markers[:4])}" if markers else
                                              " - nada está em jogo nessa frase")
    return clamp(score), detail


def check_frontload(text):
    """A palavra que interessa não pode estar na nona posição."""
    w = words(text)
    if not w:
        return 0.0, "vazio"
    low = [x.lower().strip("'’") for x in w]
    penalty, hit_opener = 0, None
    for weak in WEAK_OPENERS:
        parts = weak.split()
        if low[:len(parts)] == parts:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS
                or (i == 0 and stop_command(text)) or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or PRICE_RE.match(w[i])
                or (i and re.match(rf"[{UPPER}][{LOWER}]{{2,}}$", w[i]))):
            payload = i
            break
    if payload is None:
        base, where = 30.0, "nenhuma palavra de peso na frase"
    elif payload <= 3:
        base, where = 100.0, f"conteúdo na palavra {payload + 1}"
    elif payload <= 6:
        base, where = 70.0, f"conteúdo na palavra {payload + 1}, podia vir antes"
    else:
        base, where = 40.0, f"conteúdo na palavra {payload + 1}, tarde demais"
    detail = where + (f"; abertura fraca \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Dito pra uma pessoa, ou solto no ar."""
    low = text.lower()
    w = lower_words(text)
    if re.search(r"\b(?:você|vocês|voce|vc|vcs|cê|seu|sua|seus|suas|te|teu|tua|contigo|tu)\b", low):
        return 100.0, "fala com quem assiste"
    if w and (w[0] in IMPERATIVES or stop_command(text)):
        return 90.0, f"abre com imperativo (\"{w[0]}\")"
    if (re.search(r"\b(?:eu|meu|minha|meus|minhas|me|mim|comigo|nós|nosso|nossa|a gente)\b", low)
            or first_person_verb(w)):
        return 70.0, "primeira pessoa, sem falar com quem assiste"
    return 35.0, "terceira pessoa, ninguém na sala"


CHECKS = ["TAMANHO", "CONCRETUDE", "TENSÃO", "ABERTURA", "DIRECIONAMENTO"]


def run(text):
    results = {
        "TAMANHO": check_length(text),
        "CONCRETUDE": check_specificity(text),
        "TENSÃO": check_stakes(text),
        "ABERTURA": check_frontload(text),
        "DIRECIONAMENTO": check_address(text),
    }
    flags = [msg for pattern, msg in DEALBREAKERS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # A propriedade mais fraca limita o gancho, mesma lógica do detect.py: uma
    # propriedade ruim basta pro dedão continuar rolando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "FORTE" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "FRACO")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nNOTA DO GANCHO", file=out)
    print("=" * 64, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<15} {bar(score)} {br(score):>5}", file=out)
        print(f"  {'':<15} {detail}", file=out)
    print("-" * 64, file=out)
    print(f"  {'NOTA':<15} {bar(overall)} {br(overall):>5}   {verdict}", file=out)
    for f in flags:
        print(f"\n  ELIMINATÓRIO  {f}", file=out)
    if verdict != "FORTE":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propriedade mais fraca: {weakest}. Corrija essa e rode de novo.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nRANKING DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        print(f"{mark} {br(r['score']):>5} {r['verdict']:<6} {hook}", file=out)
        print(f"        mais fraca: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})",
              file=out)
        for f in r["flags"]:
            print(f"        eliminatório: {f}", file=out)
    print("\nGrave o primeiro. Se o primeiro ficou abaixo de 50, nenhum desses é o gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Dá nota a um gancho de Reels em cinco propriedades.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo com um gancho por linha, ou -")
    ap.add_argument("--hook", help="dá nota a um gancho só, passado na linha de comando")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nada pra avaliar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
