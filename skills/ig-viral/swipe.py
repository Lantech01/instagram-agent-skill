#!/usr/bin/env python3
"""
swipe.py - ranqueia os Reels que você coletou pelo quanto cada um superou a
própria conta, dá nome à fórmula de gancho que cada um usou e escreve o swipe
file.

Este script existe por uma correção só: view bruta não é evidência. Uma conta
de 2.000.000 de seguidores fazendo 400.000 views teve um dia fraco. Uma conta
de 4.000 seguidores fazendo 400.000 views achou alguma coisa. Aqui o ranking é
pelo múltiplo sobre a base da própria conta, que é a única versão de
"viralizou" que te diz algo que dá pra copiar.

A entrada é um arquivo separado por tabulação que você preenche enquanto
navega, um Reels por linha, com uma linha de cabeçalho dando nome às colunas
(em português ou em inglês):

    conta     seguidores  mediana  views    gancho
    @alguem   48000       11 mil   412.000  ninguém te conta que os primeiros 30 vão flopar

`mediana` são as views típicas recentes daquela conta e é a melhor base. Se
você só tem `seguidores`, deixe a mediana de fora e o script avisa. `gancho` é
a primeira frase do Reels, falada ou na tela, nas palavras da pessoa. Números
podem vir como 412000, 412.000, 412 mil, 48k ou 1,2 mi.

Uso
  python3 swipe.py coletados.tsv
  python3 swipe.py coletados.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py coletados.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[$]?[^\W_](?:[^\W_]|[$%'’-])*")
UNCLASSIFIED = "sem classificação"
# Cabeçalhos aceitos, em português ou inglês.
COLUMNS = {
    "account": "account", "conta": "account", "perfil": "account",
    "followers": "followers", "seguidores": "followers",
    "median": "median", "mediana": "median",
    "views": "views", "visualizações": "views", "visualizacoes": "views",
    "reproduções": "views", "plays": "views",
    "hook": "hook", "gancho": "hook",
}

try:                                              # opcional: dá nota aos ganchos também
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral copiado sozinho
    score_hook = None


def br(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")


def milhar(n):
    return f"{n:,}".replace(",", ".")


def parse_count(raw):
    """412000, 412.000, 412 mil, 48k, 1,2 mi, 1.2M -> inteiro. Vazio -> None."""
    s = (raw or "").strip().lower().replace(" ", "")
    if not s:
        return None
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)(k|mil|mi|m|milh[aã]o|milh[oõ]es|bi)", s)
    if m:
        mult = {"k": 1_000, "mil": 1_000, "mi": 1_000_000, "m": 1_000_000,
                "bi": 1_000_000_000}.get(m.group(2), 1_000_000)
        return int(round(float(m.group(1).replace(",", ".")) * mult))
    digits = re.sub(r"[^\d]", "", s)
    return int(digits) if digits else None


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, UNCLASSIFIED
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, UNCLASSIFIED


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [COLUMNS.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = parse_count(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = parse_count(r.get(k))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["baseline_kind"] = ("mediana" if r.get("median") else
                              "seguidores" if r.get("followers") else None)
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "mediana da conta" if used_median else "número de seguidores",
        # Lote misto: as linhas sem mediana caem pra seguidores, e o múltiplo
        # delas não é comparável com o das outras. Isso tem que aparecer.
        "follower_rows": (sum(1 for r in ranked if r["baseline_kind"] == "seguidores")
                          if used_median else 0),
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == UNCLASSIFIED),
    }


def render(a, out=sys.stdout):
    head = (f"SWIPE FILE  ·  {a['n']} reels  ·  {a['accounts']} contas  ·  "
            f"base: {a['baseline']}"
            + (f" ({a['follower_rows']} por seguidores, com *)" if a["follower_rows"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 80), file=out)
    for r in a["reels"]:
        mark = "*" if a["follower_rows"] and r["baseline_kind"] == "seguidores" else " "
        mult = f"{br(r['outlier'])}x{mark}" if r["outlier"] else "   ? "
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>8}  gancho {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {milhar(r['views']):>10}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 80), file=out)
    if a["follower_rows"]:
        print(f"  * {a['follower_rows']} linha(s) sem mediana: o múltiplo usa o número de "
              "seguidores e não é comparável\n    com o das outras. Pegue a mediana dessas "
              "contas antes de confiar no ranking.", file=out)
    print("O QUE ESTÁ FUNCIONANDO NESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  terço de cima, por múltiplo:  "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  nota mediana do gancho:       cima {a['top_hook_score']:.0f}  "
              f"vs baixo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  tamanho mediano do gancho:    cima {br(a['top_words'])} palavras  "
          f"vs baixo {br(a['bottom_words'])} palavras", file=out)
    print(f"  sem classificação:            {a['unclassified']} de {a['n']}. Leia esses na "
          "mão: é ali que está escondida uma fórmula que você ainda não tem.", file=out)
    print("\n  Um lote coletado na mão é indício, não prova. Doze Reels não mostram "
          "nada;\n  quarenta em seis contas mostram alguma coisa. Colete mais antes de "
          "acreditar.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe file", "",
             f"{a['n']} Reels em {a['accounts']} contas. "
             f"Ranqueados pelo múltiplo sobre a base ({a['baseline']}).", ""]
    for r in a["reels"]:
        mult = f"{br(r['outlier'])}x" if r["outlier"] else "?"
        score = br(r["hook_score"]) if r["hook_score"] is not None else "-"
        lines += [f"## {mult}  {r['formula']}  ({r.get('account', '')})",
                  f"- views: {milhar(r['views'])}  base: {milhar(r['baseline'])}"
                  + (f" ({r['baseline_kind']})" if r["baseline_kind"] else ""),
                  f"- nota do gancho: {score}  palavras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ranqueia Reels coletados pelo múltiplo sobre a base.")
    ap.add_argument("input", nargs="?", default="-", help="arquivo TSV, ou - pra stdin")
    ap.add_argument("--hooks", default=HOOKS, help="caminho do ig-reel/hooks.json")
    ap.add_argument("--out", help="também grava o swipe file em markdown aqui")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("nenhuma linha utilizável. Precisa de um arquivo separado por tabulação com "
              "pelo menos views e gancho.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: hooks.json não encontrado, fórmulas sem nome. Passe --hooks.",
              file=sys.stderr)
    if score_hook is None:
        print("aviso: não deu pra importar o hookscore.py, notas dos ganchos puladas.",
              file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        folder = os.path.dirname(path)
        if folder:                                # "--out swipe.md" não tem pasta
            os.makedirs(folder, exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"gravado em {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
