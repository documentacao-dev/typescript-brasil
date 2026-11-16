---
title: Módulos
layout: docs
permalink: /docs/handbook/2/modules.html
oneline: "Como o JavaScript faz a comunicação entre os limites de arquivos."
ia-translate: true
---

O JavaScript tem um longo histórico de formas diferentes de modularizar código.
O TypeScript existe desde 2012 e implementou suporte a muitos desses formatos, mas, com o tempo, a comunidade e a especificação do JavaScript convergiram para um formato chamado ES Modules (ou módulos ES6). Você pode conhecê-lo pela sintaxe `import`/`export`.

ES Modules foi adicionado à especificação do JavaScript em 2015, e, em 2020, já tinha amplo suporte na maioria dos navegadores e runtimes JavaScript.

Para manter o foco, o handbook vai cobrir tanto ES Modules quanto a sintaxe `module.exports =` do seu antecessor CommonJS, popular até hoje. Você pode encontrar informações sobre os outros padrões de módulo na seção de referência, em [Módulos](/docs/handbook/modules.html).

## Como os módulos JavaScript são definidos {#how-javascript-modules-are-defined}

No TypeScript, assim como no ECMAScript 2015, qualquer arquivo que contenha um `import` ou `export` no nível superior é considerado um módulo.

Por outro lado, um arquivo sem nenhuma declaração `import` ou `export` no nível superior é tratado como um script, cujo conteúdo fica disponível no escopo global (e, portanto, também para os módulos).

Os módulos são executados dentro do próprio escopo, e não no escopo global.
Isso significa que variáveis, funções, classes etc. declaradas em um módulo não são visíveis fora dele, a menos que sejam explicitamente exportadas por uma das formas de `export`.
Da mesma forma, para consumir uma variável, função, classe, interface etc. exportada por outro módulo, ela precisa ser importada por uma das formas de `import`.

## Não módulos {#non-modules}

Antes de começar, é importante entender o que o TypeScript considera um módulo.
A especificação do JavaScript determina que qualquer arquivo JavaScript sem uma declaração `import`, `export` ou `await` de nível superior deve ser considerado um script, e não um módulo.


Dentro de um arquivo de script, variáveis e tipos são declarados no escopo global compartilhado, e presume-se que você vai usar a opção de compilador [`outFile`](/tsconfig#outFile) para juntar vários arquivos de entrada em um único arquivo de saída, ou usar várias tags `<script>` no seu HTML para carregar esses arquivos (na ordem correta!).

Se você tem um arquivo que não tem nenhum `import` ou `export` no momento, mas quer que ele seja tratado como módulo, adicione a linha:

```ts twoslash
export {};
```

que transforma o arquivo em um módulo que não exporta nada. Essa sintaxe funciona independentemente do seu alvo de módulo.

## Módulos no TypeScript {#modules-in-typescript}

<blockquote class='bg-reading'>
   <p>Leitura complementar:<br />
   <a href='https://exploringjs.com/impatient-js/ch_modules.html#overview-syntax-of-ecmascript-modules'>Impatient JS (Modules)</a><br/>
   <a href='https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules'>MDN: JavaScript Modules</a><br/>
   </p>
</blockquote>

Há três pontos principais a considerar ao escrever código baseado em módulos no TypeScript:

- **Sintaxe**: Qual sintaxe quero usar para importar e exportar coisas?
- **Resolução de módulos**: Qual é a relação entre os nomes (ou caminhos) dos módulos e os arquivos no disco?
- **Alvo de saída do módulo**: Como deve ser o módulo JavaScript emitido?

### Sintaxe de ES Module {#es-module-syntax}

Um arquivo pode declarar uma exportação principal via `export default`:

```ts twoslash
// @filename: hello.ts
export default function helloWorld() {
  console.log("Hello, world!");
}
```

Ela é então importada com:

```ts twoslash
// @filename: hello.ts
export default function helloWorld() {
  console.log("Hello, world!");
}
// @filename: index.ts
// ---cut---
import helloWorld from "./hello.js";
helloWorld();
```

Além da exportação padrão, você pode ter mais de uma exportação de variáveis e funções usando `export` sem o `default`:

```ts twoslash
// @filename: maths.ts
export var pi = 3.14;
export let squareTwo = 1.41;
export const phi = 1.61;

export class RandomNumberGenerator {}

export function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}
```

Elas podem ser usadas em outro arquivo pela sintaxe `import`:

```ts twoslash
// @filename: maths.ts
export var pi = 3.14;
export let squareTwo = 1.41;
export const phi = 1.61;
export class RandomNumberGenerator {}
export function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}
// @filename: app.ts
// ---cut---
import { pi, phi, absolute } from "./maths.js";

console.log(pi);
const absPhi = absolute(phi);
//    ^?
```

### Sintaxe de import adicional {#additional-import-syntax}

Um import pode ser renomeado usando um formato como `import {antigo as novo}`:

```ts twoslash
// @filename: maths.ts
export var pi = 3.14;
// @filename: app.ts
// ---cut---
import { pi as π } from "./maths.js";

console.log(π);
//          ^?
```

Você pode misturar a sintaxe acima em um único `import`:

```ts twoslash
// @filename: maths.ts
export const pi = 3.14;
export default class RandomNumberGenerator {}

// @filename: app.ts
import RandomNumberGenerator, { pi as π } from "./maths.js";

RandomNumberGenerator;
// ^?

console.log(π);
//          ^?
```

Você pode pegar todos os objetos exportados e colocá-los em um único namespace usando `* as nome`:

```ts twoslash
// @filename: maths.ts
export var pi = 3.14;
export let squareTwo = 1.41;
export const phi = 1.61;

export function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}
// ---cut---
// @filename: app.ts
import * as math from "./maths.js";

console.log(math.pi);
const positivePhi = math.absolute(math.phi);
//    ^?
```

Você pode importar um arquivo e _não_ incluir nenhuma variável no módulo atual usando `import "./file"`:

```ts twoslash
// @filename: maths.ts
export var pi = 3.14;
// ---cut---
// @filename: app.ts
import "./maths.js";

console.log("3.14");
```

Nesse caso, o `import` não faz nada. No entanto, todo o código de `maths.ts` foi avaliado, o que pode disparar efeitos colaterais que afetam outros objetos.

#### Sintaxe de ES Module específica do TypeScript {#typescript-specific-es-module-syntax}

Tipos podem ser exportados e importados com a mesma sintaxe usada para valores JavaScript:

```ts twoslash
// @filename: animal.ts
export type Cat = { breed: string; yearOfBirth: number };

export interface Dog {
  breeds: string[];
  yearOfBirth: number;
}

// @filename: app.ts
import { Cat, Dog } from "./animal.js";
type Animals = Cat | Dog;
```

O TypeScript estendeu a sintaxe de `import` com dois conceitos para declarar a importação de um tipo:

##### `import type`

É uma instrução de import que só pode importar tipos:

```ts twoslash
// @filename: animal.ts
export type Cat = { breed: string; yearOfBirth: number };
export type Dog = { breeds: string[]; yearOfBirth: number };
export const createCatName = () => "fluffy";

// @filename: valid.ts
import type { Cat, Dog } from "./animal.js";
export type Animals = Cat | Dog;

// @filename: app.ts
// @errors: 1361
import type { createCatName } from "./animal.js";
const name = createCatName();
```

##### Imports `type` em linha {#inline-type-imports}

A partir do TypeScript 4.5, também é possível prefixar imports individuais com `type`, para indicar que a referência importada é um tipo:

```ts twoslash
// @filename: animal.ts
export type Cat = { breed: string; yearOfBirth: number };
export type Dog = { breeds: string[]; yearOfBirth: number };
export const createCatName = () => "fluffy";
// ---cut---
// @filename: app.ts
import { createCatName, type Cat, type Dog } from "./animal.js";

export type Animals = Cat | Dog;
const name = createCatName();
```

Juntas, essas formas permitem que um transpilador que não é do TypeScript, como Babel, swc ou esbuild, saiba quais imports podem ser removidos com segurança.

#### Sintaxe de ES Module com comportamento CommonJS {#es-module-syntax-with-commonjs-behavior}

O TypeScript tem uma sintaxe de ES Module que se relaciona _diretamente_ com o `require` do CommonJS e do AMD. Os imports com ES Module são, _na maioria dos casos_, iguais ao `require` desses ambientes, mas essa sintaxe garante uma correspondência 1 para 1, no seu arquivo TypeScript, com a saída CommonJS:

```ts twoslash
/// <reference types="node" />
// @module: commonjs
// ---cut---
import fs = require("fs");
const code = fs.readFileSync("hello.ts", "utf8");
```

Você pode saber mais sobre essa sintaxe na [página de referência de módulos](/docs/handbook/modules.html#export--and-import--require).

## Sintaxe CommonJS {#commonjs-syntax}

CommonJS é o formato em que a maioria dos módulos do npm é distribuída. Mesmo que você escreva usando a sintaxe de ES Modules acima, ter uma noção básica de como funciona a sintaxe CommonJS vai ajudar você a depurar com mais facilidade.

### Exportando {#exporting}

Identificadores são exportados definindo a propriedade `exports` de uma variável global chamada `module`.

```ts twoslash
/// <reference types="node" />
// ---cut---
function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

module.exports = {
  pi: 3.14,
  squareTwo: 1.41,
  phi: 1.61,
  absolute,
};
```

Depois, esses arquivos podem ser importados por uma instrução `require`:

```ts twoslash
// @module: commonjs
// @filename: maths.ts
/// <reference types="node" />
function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

module.exports = {
  pi: 3.14,
  squareTwo: 1.41,
  phi: 1.61,
  absolute,
};
// @filename: index.ts
// ---cut---
const maths = require("./maths");
maths.pi;
//    ^?
```

Ou você pode simplificar um pouco usando o recurso de desestruturação do JavaScript:

```ts twoslash
// @module: commonjs
// @filename: maths.ts
/// <reference types="node" />
function absolute(num: number) {
  if (num < 0) return num * -1;
  return num;
}

module.exports = {
  pi: 3.14,
  squareTwo: 1.41,
  phi: 1.61,
  absolute,
};
// @filename: index.ts
// ---cut---
const { squareTwo } = require("./maths");
squareTwo;
// ^?
```

### Interoperabilidade entre CommonJS e ES Modules {#commonjs-and-es-modules-interop}

Há uma incompatibilidade de recursos entre CommonJS e ES Modules quanto à distinção entre um import padrão (default) e um import do objeto de namespace do módulo. O TypeScript tem uma flag do compilador para reduzir o atrito entre os dois conjuntos diferentes de restrições: [`esModuleInterop`](/tsconfig#esModuleInterop).

## Opções de resolução de módulos do TypeScript {#typescripts-module-resolution-options}

Resolução de módulos é o processo de pegar uma string da instrução `import` ou `require` e determinar a qual arquivo essa string se refere.

O TypeScript inclui duas estratégias de resolução: Classic e Node. A Classic, que é o padrão quando a opção do compilador [`module`](/tsconfig#module) não é `commonjs`, é incluída por compatibilidade com versões anteriores.
A estratégia Node replica o funcionamento do Node.js no modo CommonJS, com verificações adicionais para `.ts` e `.d.ts`.

Há muitas flags do TSConfig que influenciam a estratégia de módulos no TypeScript: [`moduleResolution`](/tsconfig#moduleResolution), [`baseUrl`](/tsconfig#baseUrl), [`paths`](/tsconfig#paths), [`rootDirs`](/tsconfig#rootDirs).

Para todos os detalhes sobre como essas estratégias funcionam, consulte a página de referência [Resolução de módulos](/docs/handbook/modules/reference.html#the-moduleresolution-compiler-option).

## Opções de saída de módulos do TypeScript {#typescripts-module-output-options}

Há duas opções que afetam a saída JavaScript emitida:

- [`target`](/tsconfig#target), que determina quais recursos do JS são rebaixados (convertidos para rodar em runtimes JavaScript mais antigos) e quais são mantidos intactos
- [`module`](/tsconfig#module), que determina qual código é usado para que os módulos interajam entre si

O [`target`](/tsconfig#target) que você usa é determinado pelos recursos disponíveis no runtime JavaScript em que você espera executar o código TypeScript. Pode ser: o navegador web mais antigo que você suporta, a versão mais baixa do Node.js em que você espera rodar ou restrições específicas do seu runtime, como o Electron, por exemplo.

Toda comunicação entre módulos acontece por meio de um carregador de módulos; a opção do compilador [`module`](/tsconfig#module) determina qual deles é usado.
Em tempo de execução, o carregador de módulos é responsável por localizar e executar todas as dependências de um módulo antes de executá-lo.

Por exemplo, aqui está um arquivo TypeScript que usa a sintaxe de ES Modules, mostrando algumas opções diferentes para [`module`](/tsconfig#module):

```ts twoslash
// @filename: constants.ts
export const valueOfPi = 3.142;
// @filename: index.ts
// ---cut---
import { valueOfPi } from "./constants.js";

export const twoPi = valueOfPi * 2;
```

### `ES2020`

```ts twoslash
// @showEmit
// @module: es2020
// @noErrors
import { valueOfPi } from "./constants.js";

export const twoPi = valueOfPi * 2;
```

### `CommonJS`

```ts twoslash
// @showEmit
// @module: commonjs
// @noErrors
import { valueOfPi } from "./constants.js";

export const twoPi = valueOfPi * 2;
```

### `UMD`

```ts twoslash
// @showEmit
// @module: umd
// @noErrors
import { valueOfPi } from "./constants.js";

export const twoPi = valueOfPi * 2;
```

> Observe que ES2020 é, na prática, o mesmo que o `index.ts` original.

Você pode ver todas as opções disponíveis e como fica o código JavaScript emitido para cada uma na [Referência do TSConfig para `module`](/tsconfig#module).

## Namespaces do TypeScript {#typescript-namespaces}

O TypeScript tem seu próprio formato de módulo chamado `namespaces`, que é anterior ao padrão ES Modules. Essa sintaxe tem muitos recursos úteis para criar arquivos de definição complexos, e ainda é bastante usada [no DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped). Embora não esteja descontinuada, a maioria dos recursos de namespaces existe em ES Modules, e recomendamos usar ES Modules para se alinhar à direção do JavaScript. Você pode saber mais sobre namespaces na [página de referência de namespaces](/docs/handbook/namespaces.html).
