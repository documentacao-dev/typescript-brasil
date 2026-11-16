# CLAUDE.md

Tradução PT-BR da documentação de **TypeScript (typescriptlang.org)**, fork de `microsoft/TypeScript-Website`, parte da org [`documentacao-dev`](https://github.com/documentacao-dev).

- Conteúdo traduzível: `packages/documentation/copy/en/**/*.md`, traduzido no lugar (primeiro o `handbook-v2/`). A localização oficial em português (microsoft/TypeScript-Website-Localizations, `docs/documentation/pt/`) não tem o Handbook atual
- Site: Gatsby (monorepo pnpm): `pnpm install && pnpm bootstrap && pnpm start`
- Sync: branch `sync/upstream-AAAA-MM` com merge de `upstream/v2`, retradução só do que mudou, atualização de `tool/traducao/ultimo-sync-upstream.txt`.

## Modelo da tradução: sempre Haiku

Toda tradução e retradução de página (tradução nova, sync com o upstream, revisão de trecho) roda no **Haiku** (`model: haiku`, hoje Claude Haiku 5.5), local ou na nuvem (Claude Code na web, GitHub App, rotinas agendadas).

- Os agentes em `.claude/agents/` já declaram `model: haiku`. Não troque.
- Se um orquestrador disparar subagentes para traduzir, passe `model: "haiku"` na ferramenta Agent.
- O modelo principal da sessão fica só com a orquestração: merge do upstream, scripts de conferência, commits e PR. Ele não traduz páginas.

## Convenções do typescriptlang.org

- Front matter YAML: traduza `title`, `oneline` e o texto de `preamble` (mantendo o HTML); `layout`, `permalink`, `translatable` e demais chaves ficam iguais. Acrescente `ia-translate: true`.
- Blocos ` ```ts twoslash ` são compilados no build: o código, inclusive os comentários e as diretivas `// @errors`, `// ^?`, `// @noErrors`, fica idêntico ao inglês.
- Títulos traduzidos levam a âncora original: rode `python3 tool/traducao/ancorar_titulos.py <arquivos>` depois de traduzir (acrescenta `{#slug-do-inglês}`; o `gatsby-config.js` do fork liga `enableCustomId`). Links `#...` ficam como estão.
