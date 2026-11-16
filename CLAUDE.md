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

## Publicação: typescript.documentacao.dev

- Firebase Hosting, projeto `transliteradu`, site `typescript-documentacao` (https://typescript-documentacao.web.app; o domínio `typescript.documentacao.dev` é apontado à parte). Config em `firebase.json` + `.firebaserc`, servindo `packages/typescriptlang-org/public` com `cleanUrls: false` (as URLs do site terminam em `.html`).
- CI: `.github/workflows/deploy-firebase.yml` faz build + deploy em cada push em `v2` que mexa em `packages/documentation/**` (ou no próprio `firebase.json`/workflow) e publica um canal de preview (7 dias) em cada PR. Usa o secret `FIREBASE_SERVICE_ACCOUNT`. Também roda manualmente (`workflow_dispatch`).
- Os workflows do upstream (CI, Pages, preview no Azure, publicação de pacotes, CodeQL, keepalive) só rodam em `microsoft/TypeScript-Website`.
- Build local (Node 20, pnpm 10.30.3 via corepack, ~22 min no Mac; o `build-site` leva ~16 min porque compila os blocos twoslash):
  ```bash
  nvm use 20 && corepack enable
  pnpm install && pnpm bootstrap && pnpm build && pnpm build-site
  firebase deploy --only hosting --project transliteradu
  ```
  Não rode `pnpm docs-sync pull ...` (localizações oficiais): o site publicado é só o conteúdo de `copy/en`, que aqui está em pt-BR.
- Erro de twoslash no build aponta o `.md`: o código do bloco tem que ser idêntico ao inglês (`git show $(cat tool/traducao/ultimo-sync-upstream.txt):<arquivo>`).
- O build regrava `packages/typescriptlang-org/src/__generated__/gatsby-types.ts`; descarte essa mudança antes de commitar.
