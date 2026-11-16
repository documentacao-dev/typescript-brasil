#!/usr/bin/env python3
"""Confere as páginas traduzidas da documentação do TypeScript contra o inglês.

Para cada .md em packages/documentation/copy/en/ com `ia-translate: true`:

- front matter com as mesmas chaves do inglês (mais `ia-translate`);
- blocos de código idênticos (são compilados pelo twoslash no build);
- links (`](...)` e `href`) idênticos e na mesma ordem;
- mesmo número de títulos; título traduzido com `{#id}` em inglês;
- pouca prosa sobrando em inglês.

O inglês vem do commit em tool/traducao/ultimo-sync-upstream.txt.
Uso: python3 tool/traducao/verificar.py [caminhos...]   (código 1 se houver erro)
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = (ROOT / 'tool' / 'traducao' / 'ultimo-sync-upstream.txt').read_text().strip()
CONTEUDO = ROOT / 'packages' / 'documentation' / 'copy' / 'en'
FLAG = re.compile(r'^ia-translate:\s*true\s*$', re.M)
FM = re.compile(r'\A---\n(.*?)\n---\n', re.S)
CHAVE = re.compile(r'^([A-Za-z_][\w-]*):', re.M)
CERCA = re.compile(r'^```.*?^```', re.S | re.M)
LINK = re.compile(r'\]\(([^)\s]+)|href=["\']([^"\']+)')
TITULO = re.compile(r'^#{1,6}\s+(.*)$', re.M)
EN = set('the and of to is are you your this that with for in it be can when '
         'will from have which an by on as at or'.split())


def corpo(texto):
    m = FM.match(texto)
    return (m.group(1) if m else ''), (texto[m.end():] if m else texto)


def titulos(texto):
    return TITULO.findall(CERCA.sub('', texto))


def conferir(caminho):
    erros = []
    pt = (ROOT / caminho).read_text()
    r = subprocess.run(['git', 'show', f'{BASE}:{caminho}'], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        return [f'{caminho}: não existe no upstream ({BASE[:9]})']
    en = r.stdout
    fm_en, c_en = corpo(en)
    fm_pt, c_pt = corpo(pt)
    k_en, k_pt = set(CHAVE.findall(fm_en)), set(CHAVE.findall(fm_pt)) - {'ia-translate'}
    if k_en != k_pt:
        erros.append(f'chaves do front matter mudaram: {sorted(k_en ^ k_pt)}')
    b_en, b_pt = CERCA.findall(c_en), CERCA.findall(c_pt)
    if b_en != b_pt:
        dif = sum(a != b for a, b in zip(b_en, b_pt))
        erros.append(f'blocos de código: {len(b_en)} no inglês, {len(b_pt)} na tradução, {dif} diferente(s)')
    l_en = [a or b for a, b in LINK.findall(c_en)]
    l_pt = [a or b for a, b in LINK.findall(c_pt)]
    if l_en != l_pt:
        erros.append(f'links: {len(l_en)} no inglês, {len(l_pt)} na tradução'
                     + ('' if len(l_en) != len(l_pt) else ' (destinos diferentes)'))
    t_en, t_pt = titulos(c_en), titulos(c_pt)
    if len(t_en) != len(t_pt):
        erros.append(f'títulos: {len(t_en)} no inglês, {len(t_pt)} na tradução')
    else:
        sem = [t for a, t in zip(t_en, t_pt) if a != t and '{#' not in t]
        if sem:
            erros.append(f'{len(sem)} título(s) traduzido(s) sem {{#id}} (rode ancorar_titulos.py)')
    prosa = re.sub(r'`[^`]*`|<[^>]+>|\]\([^)]*\)', ' ', CERCA.sub('', c_pt)).lower()
    palavras = re.findall(r'[a-zà-ú]+', prosa)
    taxa = sum(p in EN for p in palavras) / max(len(palavras), 1)
    if taxa > 0.08:
        erros.append(f'prosa ainda parece inglês ({taxa:.0%} de palavras comuns em inglês)')
    return [f'{caminho}: {e}' for e in erros]


def main():
    arquivos = sys.argv[1:] or sorted(
        str(p.relative_to(ROOT)) for p in CONTEUDO.rglob('*.md') if FLAG.search(p.read_text()))
    erros = [e for a in arquivos for e in conferir(a)]
    for e in erros:
        print('ERRO', e)
    print(f'{len(arquivos)} arquivo(s) traduzido(s), {len(erros)} erro(s)')
    sys.exit(1 if erros else 0)


if __name__ == '__main__':
    main()
