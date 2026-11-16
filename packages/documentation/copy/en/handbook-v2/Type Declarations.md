---
title: Declarações de tipos
layout: docs
permalink: /docs/handbook/2/type-declarations.html
oneline: "Como o TypeScript fornece tipos para JavaScript sem tipagem."
ia-translate: true
---

Nas seções que você leu até agora, demonstramos conceitos básicos do TypeScript usando as funções nativas presentes em todos os runtimes JavaScript.
No entanto, quase todo JavaScript hoje usa várias bibliotecas para realizar tarefas comuns.
Ter tipos para as partes da sua aplicação que _não_ são código seu vai melhorar muito sua experiência com TypeScript.
De onde vêm esses tipos?

## Como são as declarações de tipo? {#what-do-type-declarations-look-like}

Vamos supor que você escreva um código como este:

```ts twoslash
// @errors: 2339
const k = Math.max(5, 6);
const j = Math.mix(7, 8);
```

Como o TypeScript sabe que `max` existe, mas `mix` não, mesmo que a implementação de `Math` não faça parte do seu código?

A resposta é que existem _arquivos de declaração_ que descrevem esses objetos nativos.
Um arquivo de declaração permite _declarar_ a existência de alguns tipos ou valores sem fornecer as implementações desses valores.

## Arquivos `.d.ts` {#dts-files}

O TypeScript tem dois tipos principais de arquivo.
Os arquivos `.ts` são arquivos de _implementação_ que contêm tipos e código executável.
São esses arquivos que geram as saídas `.js`, e é onde você normalmente escreve o seu código.

Os arquivos `.d.ts` são arquivos de _declaração_ que contêm _apenas_ informações de tipo.
Eles não geram saídas `.js`; são usados somente na verificação de tipos.
Mais adiante, vamos aprender a escrever os nossos próprios arquivos de declaração.

## Definições de tipos nativas {#built-in-type-definitions}

O TypeScript inclui arquivos de declaração para todas as APIs nativas padronizadas disponíveis nos runtimes JavaScript.
Isso inclui coisas como métodos e propriedades de tipos nativos como `string` ou `function`, nomes de nível superior como `Math` e `Object`, e os tipos associados a eles.
Por padrão, o TypeScript também inclui tipos para o que está disponível quando o código roda no navegador, como `window` e `document`; esses são chamados coletivamente de APIs do DOM.

O TypeScript nomeia esses arquivos de declaração com o padrão `lib.[algo].d.ts`.
Se você abrir um arquivo com esse nome, saberá que está lidando com alguma parte nativa da plataforma, e não com código do usuário.

### Configuração `target` {#target-setting}

Os métodos, propriedades e funções que você tem à disposição variam de acordo com a _versão_ do JavaScript em que o seu código roda.
Por exemplo, o método `startsWith` de strings só está disponível a partir da versão do JavaScript chamada _ECMAScript 6_.

É importante saber em qual versão do JavaScript o seu código vai rodar, porque você não quer usar APIs de uma versão mais nova do que a plataforma onde faz o deploy.
Essa é uma das funções da configuração de compilador [`target`](/tsconfig#target).

O TypeScript ajuda com esse problema variando quais arquivos `lib` são incluídos por padrão, de acordo com a sua configuração [`target`](/tsconfig#target).
Por exemplo, se [`target`](/tsconfig#target) for `ES5`, você verá um erro ao tentar usar o método `startsWith`, porque esse método só está disponível no `ES6` ou em versões posteriores.

### Configuração `lib` {#lib-setting}

A configuração [`lib`](/tsconfig#lib) permite um controle mais refinado sobre quais arquivos de declaração nativos são considerados disponíveis no seu programa.
Veja a página da documentação sobre [`lib`](/tsconfig#lib) para mais informações.

## Definições externas {#external-definitions}

Para APIs que não são nativas, existem várias formas de obter arquivos de declaração.
Como fazer isso depende de qual biblioteca você está tipando.

### Tipos incluídos no pacote {#bundled-types}

Se uma biblioteca que você usa é publicada como pacote npm, ela pode já incluir arquivos de declaração de tipos na sua distribuição.
Você pode ler a documentação do projeto para descobrir, ou simplesmente tentar importar o pacote e ver se o TypeScript consegue resolver os tipos automaticamente.

Se você é autor de um pacote e está pensando em incluir definições de tipo junto com ele, pode ler nosso guia sobre [como empacotar definições de tipo](/docs/handbook/declaration-files/publishing.html#including-declarations-in-your-npm-package).

### DefinitelyTyped / `@types`

O [repositório DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped/) é um repositório centralizado que armazena arquivos de declaração de milhares de bibliotecas.
A grande maioria das bibliotecas mais usadas tem arquivos de declaração disponíveis no DefinitelyTyped.

As definições do DefinitelyTyped também são publicadas automaticamente no npm, no escopo `@types`.
O nome do pacote de tipos é sempre igual ao nome do próprio pacote original.
Por exemplo, se você instalou o pacote npm `react`, pode instalar os tipos correspondentes executando

```sh
npm install --save-dev @types/react
```

O TypeScript encontra automaticamente as definições de tipo em `node_modules/@types`, então não é preciso nenhum outro passo para deixar esses tipos disponíveis no seu programa.

### Suas próprias definições {#your-own-definitions}

No caso raro de uma biblioteca não ter incluído os próprios tipos e não existir definição no DefinitelyTyped, você mesmo pode escrever um arquivo de declaração.
Veja o apêndice [Escrevendo arquivos de declaração](/docs/handbook/declaration-files/introduction.html) para um guia.

Se você quiser silenciar avisos sobre um módulo específico sem escrever um arquivo de declaração, também pode declarar rapidamente o módulo com tipo `any`, colocando uma declaração vazia para ele em um arquivo `.d.ts` do seu projeto.
Por exemplo, se você quisesse usar um módulo chamado `some-untyped-module` sem ter definições para ele, escreveria:

```ts twoslash
declare module "some-untyped-module";
```
