#!/usr/bin/env python3
"""
Gerador de página de cliente Trustmore.

Pega os dados de um cliente novo, preenche o template (_template/index.html +
_template/admin.html) e escreve a pasta pronta pra subir no repositório.

Uso:
    python3 generate_client.py \
        --slug carol2 \
        --nome "Nome Completo" \
        --servico "Serviço prestado" \
        --cidade "Cidade / região" \
        --whatsapp 31600000000 \
        --sheet-id ID_DA_PLANILHA \
        --review-form-id ID_DO_FORMULARIO_DE_AVALIACAO \
        --foto caminho/para/foto.jpg \
        --fundo caminho/para/fundo.jpg

Não faz nenhum commit/push sozinho -- só gera os arquivos localmente dentro
da pasta <slug>/ na raiz do repositório. Revise e suba manualmente (ou use
o publish_client.sh depois de conferir).
"""
import argparse
import pathlib
import random
import re
import shutil
import string
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_INDEX = REPO_ROOT / "_template" / "index.html"
TEMPLATE_ADMIN = REPO_ROOT / "_template" / "admin.html"


def gen_admin_code(length=8):
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choices(alphabet, k=length))


def only_digits(s):
    return re.sub(r"\D", "", s)


def fill(template_text, mapping):
    out = template_text
    for key, val in mapping.items():
        out = out.replace("{{%s}}" % key, val)
    return out


def check_no_placeholders_left(text, label):
    leftover = set(re.findall(r"\{\{[A-Z_]+\}\}", text))
    if leftover:
        print(f"AVISO: sobraram placeholders não preenchidos em {label}: {leftover}", file=sys.stderr)
        return False
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", required=True, help="nome da pasta do cliente (sem espaços/acentos), ex: carol2")
    p.add_argument("--nome", required=True)
    p.add_argument("--servico", required=True)
    p.add_argument("--cidade", required=True)
    p.add_argument("--whatsapp", required=True, help="código do país + número, com ou sem formatação")
    p.add_argument("--sheet-id", required=True, help="ID da planilha Google (da URL docs.google.com/spreadsheets/d/ESSE_ID/...)")
    p.add_argument("--review-form-id", required=True, help="ID do formulário de avaliação (da URL .../forms/d/e/ESSE_ID/viewform)")
    p.add_argument("--foto", required=True, help="caminho local da foto do cliente")
    p.add_argument("--fundo", required=True, help="caminho local da imagem de fundo")
    p.add_argument("--admin-code", default=None, help="código do admin (8 chars); se omitido, gera um aleatório")
    p.add_argument("--out", default=None, help="pasta de saída; default: <repo>/<slug>")
    args = p.parse_args()

    admin_code = args.admin_code or gen_admin_code()
    whatsapp_digits = only_digits(args.whatsapp)

    mapping = {
        "NOME": args.nome,
        "SERVICO": args.servico,
        "CIDADE": args.cidade,
        "WHATSAPP": whatsapp_digits,
        "SHEET_ID": args.sheet_id,
        "REVIEW_FORM_ID": args.review_form_id,
        "SLUG": args.slug,
        "ADMIN_CODE": admin_code,
    }

    index_text = fill(TEMPLATE_INDEX.read_text(encoding="utf-8"), mapping)
    admin_text = fill(TEMPLATE_ADMIN.read_text(encoding="utf-8"), mapping)

    ok1 = check_no_placeholders_left(index_text, "index.html")
    ok2 = check_no_placeholders_left(admin_text, "admin.html")

    out_dir = pathlib.Path(args.out) if args.out else (REPO_ROOT / args.slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "index.html").write_text(index_text, encoding="utf-8")
    admin_filename = f"admin-{admin_code}.html"
    (out_dir / admin_filename).write_text(admin_text, encoding="utf-8")

    foto_ext = pathlib.Path(args.foto).suffix or ".jpg"
    fundo_ext = pathlib.Path(args.fundo).suffix or ".jpg"
    shutil.copy(args.foto, out_dir / f"foto{foto_ext}")
    shutil.copy(args.fundo, out_dir / f"fundo{fundo_ext}")

    # o template referencia foto.jpg / fundo.jpg diretamente -- se a extensão
    # original não for .jpg, ajusta a referência dentro dos arquivos gerados
    if foto_ext.lower() != ".jpg":
        for fp in (out_dir / "index.html", out_dir / admin_filename):
            fp.write_text(fp.read_text(encoding="utf-8").replace("foto.jpg", f"foto{foto_ext}"), encoding="utf-8")
    if fundo_ext.lower() != ".jpg":
        for fp in (out_dir / "index.html", out_dir / admin_filename):
            fp.write_text(fp.read_text(encoding="utf-8").replace("fundo.jpg", f"fundo{fundo_ext}"), encoding="utf-8")

    print(f"\nPasta gerada em: {out_dir}")
    print(f"  - index.html")
    print(f"  - {admin_filename}")
    print(f"  - foto{foto_ext}")
    print(f"  - fundo{fundo_ext}")
    print(f"\nLink público (depois do push):  https://trustmore.app/{args.slug}/")
    print(f"Link da área privada:            https://trustmore.app/{args.slug}/{admin_filename}")
    if not (ok1 and ok2):
        print("\nATENÇÃO: revise os avisos de placeholder acima antes de publicar.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
