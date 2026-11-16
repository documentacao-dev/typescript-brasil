---
title: Tipos do dia a dia
layout: docs
permalink: /docs/handbook/2/everyday-types.html
oneline: "Os primitivos da linguagem."
ia-translate: true
---

Neste capítulo, vamos cobrir alguns dos tipos de valores mais comuns que você vai encontrar em código JavaScript, e explicar as formas correspondentes de descrever esses tipos em TypeScript.
Esta não é uma lista exaustiva, e os próximos capítulos vão descrever mais formas de nomear e usar outros tipos.

Os tipos também podem aparecer em muitos outros _lugares_ além das anotações de tipo.
À medida que aprendemos sobre os próprios tipos, também aprenderemos sobre os lugares onde podemos referenciar esses tipos para formar novas construções.

Começaremos revisando os tipos mais básicos e comuns que você pode encontrar ao escrever código JavaScript ou TypeScript.
Eles depois formarão os blocos de construção centrais dos tipos mais complexos.

## Os primitivos: `string`, `number` e `boolean` {#the-primitives-string-number-and-boolean}

O JavaScript tem três [primitivos](https://developer.mozilla.org/en-US/docs/Glossary/Primitive) muito usados: `string`, `number` e `boolean`.
Cada um tem um tipo correspondente em TypeScript.
Como seria de se esperar, esses são os mesmos nomes que você veria se usasse o operador `typeof` do JavaScript em um valor desses tipos:

- `string` representa valores de texto como `"Hello, world"`
- `number` é para números como `42`. O JavaScript não tem um valor especial em tempo de execução para inteiros, então não existe equivalente a `int` ou `float` - tudo é simplesmente `number`
- `boolean` é para os dois valores `true` e `false`

> Os nomes de tipo `String`, `Number` e `Boolean` (com letra maiúscula) são válidos, mas se referem a alguns tipos especiais embutidos que raramente vão aparecer no seu código. _Sempre_ use `string`, `number` ou `boolean` para tipos.

## Arrays

Para especificar o tipo de um array como `[1, 2, 3]`, você pode usar a sintaxe `number[]`; essa sintaxe funciona para qualquer tipo (por exemplo, `string[]` é um array de strings, e assim por diante).
Você também pode ver isso escrito como `Array<number>`, que significa a mesma coisa.
Vamos aprender mais sobre a sintaxe `T<U>` quando falarmos de _generics_.

> Observe que `[number]` é outra coisa; consulte a seção sobre [Tuplas](/docs/handbook/2/objects.html#tuple-types).

## `any`

O TypeScript também tem um tipo especial, `any`, que você pode usar sempre que não quiser que um valor específico cause erros de verificação de tipos.

Quando um valor é do tipo `any`, você pode acessar qualquer propriedade dele (que, por sua vez, será do tipo `any`), chamá-lo como função, atribuí-lo a (ou a partir de) um valor de qualquer tipo, ou praticamente qualquer outra coisa que seja sintaticamente válida:

```ts twoslash
let obj: any = { x: 0 };
// None of the following lines of code will throw compiler errors.
// Using `any` disables all further type checking, and it is assumed
// you know the environment better than TypeScript.
obj.foo();
obj();
obj.bar = 100;
obj = "hello";
const n: number = obj;
```

O tipo `any` é útil quando você não quer escrever um tipo longo só para convencer o TypeScript de que uma determinada linha de código está correta.

### `noImplicitAny`

Quando você não especifica um tipo, e o TypeScript não consegue inferi-lo a partir do contexto, o compilador normalmente assume `any` por padrão.

Você geralmente quer evitar isso, porque `any` não passa pela verificação de tipos.
Use a flag do compilador [`noImplicitAny`](/tsconfig#noImplicitAny) para marcar qualquer `any` implícito como erro.

## Anotações de tipo em variáveis {#type-annotations-on-variables}

Quando você declara uma variável usando `const`, `var` ou `let`, pode opcionalmente adicionar uma anotação de tipo para especificar explicitamente o tipo da variável:

```ts twoslash
let myName: string = "Alice";
//        ^^^^^^^^ Type annotation
```

> O TypeScript não usa declarações com tipo "à esquerda" como `int x = 0;`
> Anotações de tipo sempre vêm _depois_ da coisa que está sendo tipada.

Na maioria dos casos, porém, isso não é necessário.
Sempre que possível, o TypeScript tenta _inferir_ automaticamente os tipos no seu código.
Por exemplo, o tipo de uma variável é inferido com base no tipo do seu valor inicial:

```ts twoslash
// No type annotation needed -- 'myName' inferred as type 'string'
let myName = "Alice";
```

Na maior parte do tempo, você não precisa aprender explicitamente as regras de inferência.
Se você está começando, tente usar menos anotações de tipo do que imagina - você pode se surpreender com quão poucas são necessárias para o TypeScript entender completamente o que está acontecendo.

## Funções {#functions}

Funções são o principal meio de passar dados pelo JavaScript.
O TypeScript permite que você especifique os tipos tanto dos valores de entrada quanto dos de saída das funções.

### Anotações de tipo de parâmetros {#parameter-type-annotations}

Quando você declara uma função, pode adicionar anotações de tipo depois de cada parâmetro para declarar quais tipos de parâmetros a função aceita.
As anotações de tipo dos parâmetros vêm depois do nome do parâmetro:

```ts twoslash
// Parameter type annotation
function greet(name: string) {
  //                 ^^^^^^^^
  console.log("Hello, " + name.toUpperCase() + "!!");
}
```

Quando um parâmetro tem uma anotação de tipo, os argumentos passados para essa função serão verificados:

```ts twoslash
// @errors: 2345
declare function greet(name: string): void;
// ---cut---
// Would be a runtime error if executed!
greet(42);
```

> Mesmo que você não tenha anotações de tipo nos seus parâmetros, o TypeScript ainda vai verificar se você passou o número certo de argumentos.

### Anotações de tipo de retorno {#return-type-annotations}

Você também pode adicionar anotações de tipo de retorno.
As anotações de tipo de retorno aparecem depois da lista de parâmetros:

```ts twoslash
function getFavoriteNumber(): number {
  //                        ^^^^^^^^
  return 26;
}
```

Assim como as anotações de tipo de variáveis, você normalmente não precisa de uma anotação de tipo de retorno, porque o TypeScript vai inferir o tipo de retorno da função com base nas suas instruções `return`.
A anotação de tipo no exemplo acima não muda nada.
Algumas bases de código especificam explicitamente um tipo de retorno para fins de documentação, para evitar mudanças acidentais, ou simplesmente por preferência pessoal.

#### Funções que retornam Promises {#functions-which-return-promises}

Se você quiser anotar o tipo de retorno de uma função que retorna uma promise, deve usar o tipo `Promise`:

```ts twoslash
async function getFavoriteNumber(): Promise<number> {
  return 26;
}
```

### Funções anônimas {#anonymous-functions}

Funções anônimas são um pouco diferentes das declarações de função.
Quando uma função aparece em um lugar onde o TypeScript consegue determinar como ela será chamada, os parâmetros dessa função recebem tipos automaticamente.

Aqui está um exemplo:

```ts twoslash
// @errors: 2551
const names = ["Alice", "Bob", "Eve"];

// Contextual typing for function - parameter s inferred to have type string
names.forEach(function (s) {
  console.log(s.toUpperCase());
});

// Contextual typing also applies to arrow functions
names.forEach((s) => {
  console.log(s.toUpperCase());
});
```

Mesmo que o parâmetro `s` não tenha anotação de tipo, o TypeScript usou os tipos da função `forEach`, junto com o tipo inferido do array, para determinar o tipo que `s` terá.

Esse processo é chamado de _contextual typing_ (tipagem contextual), porque o _contexto_ em que a função aparece informa qual tipo ela deve ter.

Assim como as regras de inferência, você não precisa aprender explicitamente como isso acontece, mas entender que isso _acontece_ pode ajudar você a perceber quando anotações de tipo não são necessárias.
Mais adiante, veremos mais exemplos de como o contexto em que um valor aparece pode afetar o seu tipo.

## Tipos de objeto {#object-types}

Além dos primitivos, o tipo mais comum que você vai encontrar é um _tipo de objeto_.
Isso se refere a qualquer valor do JavaScript com propriedades, o que vale para quase todos!
Para definir um tipo de objeto, basta listar suas propriedades e os tipos delas.

Por exemplo, aqui está uma função que recebe um objeto no formato de um ponto:

```ts twoslash
// The parameter's type annotation is an object type
function printCoord(pt: { x: number; y: number }) {
  //                      ^^^^^^^^^^^^^^^^^^^^^^^^
  console.log("The coordinate's x value is " + pt.x);
  console.log("The coordinate's y value is " + pt.y);
}
printCoord({ x: 3, y: 7 });
```

Aqui, anotamos o parâmetro com um tipo que tem duas propriedades - `x` e `y` - ambas do tipo `number`.
Você pode usar `,` ou `;` para separar as propriedades, e o último separador é opcional em qualquer um dos casos.

A parte do tipo de cada propriedade também é opcional.
Se você não especificar um tipo, ele será considerado como `any`.

### Propriedades opcionais {#optional-properties}

Tipos de objeto também podem especificar que algumas ou todas as suas propriedades são _opcionais_.
Para isso, adicione um `?` depois do nome da propriedade:

```ts twoslash
function printName(obj: { first: string; last?: string }) {
  // ...
}
// Both OK
printName({ first: "Bob" });
printName({ first: "Alice", last: "Alisson" });
```

No JavaScript, se você acessar uma propriedade que não existe, você recebe o valor `undefined` em vez de um erro em tempo de execução.
Por causa disso, ao _ler_ uma propriedade opcional, você precisa verificar se é `undefined` antes de usá-la.

```ts twoslash
// @errors: 18048
function printName(obj: { first: string; last?: string }) {
  // Error - might crash if 'obj.last' wasn't provided!
  console.log(obj.last.toUpperCase());
  if (obj.last !== undefined) {
    // OK
    console.log(obj.last.toUpperCase());
  }

  // A safe alternative using modern JavaScript syntax:
  console.log(obj.last?.toUpperCase());
}
```

## Tipos union {#union-types}

O sistema de tipos do TypeScript permite construir novos tipos a partir de tipos existentes usando uma grande variedade de operadores.
Agora que sabemos escrever alguns tipos, é hora de começar a _combiná-los_ de formas interessantes.

### Definindo um tipo union {#defining-a-union-type}

A primeira forma de combinar tipos que você pode ver é um tipo _union_.
Um tipo union é um tipo formado a partir de dois ou mais outros tipos, representando valores que podem ser _qualquer um_ desses tipos.
Chamamos cada um desses tipos de _membros_ da union.

Vamos escrever uma função que pode operar sobre strings ou números:

```ts twoslash
// @errors: 2345
function printId(id: number | string) {
  console.log("Your ID is: " + id);
}
// OK
printId(101);
// OK
printId("202");
// Error
printId({ myID: 22342 });
```

> O separador dos membros da union é permitido antes do primeiro elemento, então você também pode escrever assim:
> ```ts twoslash
> function printTextOrNumberOrBool(
>   textOrNumberOrBool:
>     | string
>     | number
>     | boolean
> ) {
>   console.log(textOrNumberOrBool);
> }
> ```

### Trabalhando com tipos union {#working-with-union-types}

É fácil _fornecer_ um valor que corresponda a um tipo union - basta fornecer um tipo que corresponda a qualquer um dos membros da union.
Se você _tem_ um valor de tipo union, como trabalhar com ele?

O TypeScript só vai permitir uma operação se ela for válida para _todos_ os membros da union.
Por exemplo, se você tem a union `string | number`, não pode usar métodos que existem apenas em `string`:

```ts twoslash
// @errors: 2339
function printId(id: number | string) {
  console.log(id.toUpperCase());
}
```

A solução é _restringir_ a union com código, da mesma forma que você faria em JavaScript sem anotações de tipo.
O _narrowing_ acontece quando o TypeScript consegue deduzir um tipo mais específico para um valor com base na estrutura do código.

Por exemplo, o TypeScript sabe que apenas um valor `string` terá o valor de `typeof` igual a `"string"`:

```ts twoslash
function printId(id: number | string) {
  if (typeof id === "string") {
    // In this branch, id is of type 'string'
    console.log(id.toUpperCase());
  } else {
    // Here, id is of type 'number'
    console.log(id);
  }
}
```

Outro exemplo é usar uma função como `Array.isArray`:

```ts twoslash
function welcomePeople(x: string[] | string) {
  if (Array.isArray(x)) {
    // Here: 'x' is 'string[]'
    console.log("Hello, " + x.join(" and "));
  } else {
    // Here: 'x' is 'string'
    console.log("Welcome lone traveler " + x);
  }
}
```

Repare que, no ramo `else`, não precisamos fazer nada especial - se `x` não era um `string[]`, então ele precisa ter sido uma `string`.

Às vezes você terá uma union em que todos os membros têm algo em comum.
Por exemplo, tanto arrays quanto strings têm um método `slice`.
Se todo membro de uma union tem uma propriedade em comum, você pode usar essa propriedade sem fazer narrowing:

```ts twoslash
// Return type is inferred as number[] | string
function getFirstThree(x: number[] | string) {
  return x.slice(0, 3);
}
```

> Pode parecer confuso que uma _union_ de tipos aparente ter a _interseção_ das propriedades desses tipos.
> Isso não é acidente - o nome _union_ vem da teoria dos tipos.
> A _union_ `number | string` é composta pegando a união _dos valores_ de cada tipo.
> Repare que, dados dois conjuntos com fatos correspondentes sobre cada conjunto, apenas a _interseção_ desses fatos se aplica à _união_ dos próprios conjuntos.
> Por exemplo, se tivéssemos uma sala de pessoas altas usando chapéu, e outra sala de falantes de espanhol usando chapéu, depois de juntar as salas, a única coisa que sabemos sobre _cada_ pessoa é que ela deve estar usando um chapéu.

## Aliases de tipo {#type-aliases}

Temos usado tipos de objeto e tipos union escrevendo-os diretamente nas anotações de tipo.
Isso é conveniente, mas é comum querer usar o mesmo tipo mais de uma vez e referenciá-lo por um único nome.

Um _alias de tipo_ é exatamente isso - um _nome_ para qualquer _tipo_.
A sintaxe de um alias de tipo é:

```ts twoslash
type Point = {
  x: number;
  y: number;
};

// Exactly the same as the earlier example
function printCoord(pt: Point) {
  console.log("The coordinate's x value is " + pt.x);
  console.log("The coordinate's y value is " + pt.y);
}

printCoord({ x: 100, y: 100 });
```

Na verdade, você pode usar um alias de tipo para dar nome a qualquer tipo, não apenas a tipos de objeto.
Por exemplo, um alias de tipo pode nomear um tipo union:

```ts twoslash
type ID = number | string;
```

Observe que aliases são _apenas_ aliases - você não pode usar aliases de tipo para criar "versões" diferentes e distintas do mesmo tipo.
Quando você usa o alias, é exatamente como se você tivesse escrito o tipo apelidado.
Em outras palavras, este código _parece_ ilegal, mas é aceito pelo TypeScript porque ambos os tipos são aliases para o mesmo tipo:

```ts twoslash
declare function getInput(): string;
declare function sanitize(str: string): string;
// ---cut---
type UserInputSanitizedString = string;

function sanitizeInput(str: string): UserInputSanitizedString {
  return sanitize(str);
}

// Create a sanitized input
let userInput = sanitizeInput(getInput());

// Can still be re-assigned with a string though
userInput = "new input";
```

## Interfaces

Uma _declaração de interface_ é outra forma de dar nome a um tipo de objeto:

```ts twoslash
interface Point {
  x: number;
  y: number;
}

function printCoord(pt: Point) {
  console.log("The coordinate's x value is " + pt.x);
  console.log("The coordinate's y value is " + pt.y);
}

printCoord({ x: 100, y: 100 });
```

Assim como quando usamos um alias de tipo acima, o exemplo funciona como se tivéssemos usado um tipo de objeto anônimo.
O TypeScript só se preocupa com a _estrutura_ do valor que passamos para `printCoord` - ele só se importa que o valor tenha as propriedades esperadas.
Preocupar-se apenas com a estrutura e as capacidades dos tipos é o motivo pelo qual chamamos o TypeScript de um sistema de tipos _estruturalmente tipado_.

### Diferenças entre aliases de tipo e interfaces {#differences-between-type-aliases-and-interfaces}

Aliases de tipo e interfaces são muito parecidos, e em muitos casos você pode escolher entre eles livremente. Quase todos os recursos de uma `interface` estão disponíveis em `type`; a principal diferença é que um tipo não pode ser reaberto para adicionar novas propriedades, enquanto uma interface sempre pode ser estendida.

<div class='table-container'>
<table class='full-width-table'>
  <tbody>
    <tr>
      <th><code>Interface</code></th>
      <th><code>Type</code></th>
    </tr>
    <tr>
      <td>
        <p>Estendendo uma interface</p>
        <code><pre>
interface Animal {
  name: string;
}<br/>
interface Bear extends Animal {
  honey: boolean;
}<br/>
const bear = getBear();
bear.name;
bear.honey;
        </pre></code>
      </td>
      <td>
        <p>Estendendo um tipo via interseções</p>
        <code><pre>
type Animal = {
  name: string;
}<br/>
type Bear = Animal & { 
  honey: boolean;
}<br/>
const bear = getBear();
bear.name;
bear.honey;
        </pre></code>
      </td>
    </tr>
    <tr>
      <td>
        <p>Adicionando novos campos a uma interface existente</p>
        <code><pre>
interface Window {
  title: string;
}<br/>
interface Window {
  ts: TypeScriptAPI;
}<br/>
const src = 'const a = "Hello World"';
window.ts.transpileModule(src, {});
        </pre></code>
      </td>
      <td>
        <p>Um tipo não pode ser alterado depois de criado</p>
        <code><pre>
type Window = {
  title: string;
}<br/>
type Window = {
  ts: TypeScriptAPI;
}<br/>
<span style="color: #A31515"> // Error: Duplicate identifier 'Window'.</span><br/>
        </pre></code>
      </td>
    </tr>
    </tbody>
</table>
</div>

Você vai aprender mais sobre esses conceitos em capítulos posteriores, então não se preocupe se não entender tudo isso de imediato.

- Antes da versão 4.2 do TypeScript, os nomes de aliases de tipo [_podiam_ aparecer nas mensagens de erro](/play?#code/PTAEGEHsFsAcEsA2BTATqNrLusgzngIYDm+oA7koqIYuYQJ56gCueyoAUCKAC4AWHAHaFcoSADMaQ0PCG80EwgGNkALk6c5C1EtWgAsqOi1QAb06groEbjWg8vVHOKcAvpokshy3vEgyyMr8kEbQJogAFND2YREAlOaW1soBeJAoAHSIkMTRmbbI8e6aPMiZxJmgACqCGKhY6ABGyDnkFFQ0dIzMbBwCwqIccabcYLyQoKjIEmh8kwN8DLAc5PzwwbLMyAAeK77IACYaQSEjUWZWhfYAjABMAMwALA+gbsVjoADqgjKESytQPxCHghAByXigYgBfr8LAsYj8aQMUASbDQcRSExCeCwFiIQh+AKfAYyBiQFgOPyIaikSGLQo0Zj-aazaY+dSaXjLDgAGXgAC9CKhDqAALxJaw2Ib2RzOISuDycLw+ImBYKQflCkWRRD2LXCw6JCxS1JCdJZHJ5RAFIbFJU8ADKC3WzEcnVZaGYE1ABpFnFOmsFhsil2uoHuzwArO9SmAAEIsSFrZB-GgAjjA5gtVN8VCEc1o1C4Q4AGlR2AwO1EsBQoAAbvB-gJ4HhPgB5aDwem-Ph1TCV3AEEirTp4ELtRbTPD4vwKjOfAuioSQHuDXBcnmgACC+eCONFEs73YAPGGZVT5cRyyhiHh7AAON7lsG3vBggB8XGV3l8-nVISOgghxoLq9i7io-AHsayRWGaFrlFauq2rg9qaIGQHwCBqChtKdgRo8TxRjeyB3o+7xAA), às vezes no lugar do tipo anônimo equivalente (o que pode ou não ser desejável). Interfaces sempre aparecerão com o nome nas mensagens de erro.
- Aliases de tipo não podem participar [de declaration merging, mas interfaces podem](/play?#code/PTAEEEDtQS0gXApgJwGYEMDGjSfdAIx2UQFoB7AB0UkQBMAoEUfO0Wgd1ADd0AbAK6IAzizp16ALgYM4SNFhwBZdAFtV-UAG8GoPaADmNAcMmhh8ZHAMMAvjLkoM2UCvWad+0ARL0A-GYWVpA29gyY5JAWLJAwGnxmbvGgALzauvpGkCZmAEQAjABMAMwALLkANBl6zABi6DB8okR4Jjg+iPSgABboovDk3jjo5pbW1d6+dGb5djLwAJ7UoABKiJTwjThpnpnGpqPBoTLMAJrkArj4kOTwYmycPOhW6AR8IrDQ8N04wmo4HHQCwYi2Waw2W1S6S8HX8gTGITsQA).
- Interfaces só podem ser usadas para [declarar o formato de objetos, não para renomear primitivos](/play?#code/PTAEAkFMCdIcgM6gC4HcD2pIA8CGBbABwBtIl0AzUAKBFAFcEBLAOwHMUBPQs0XFgCahWyGBVwBjMrTDJMAshOhMARpD4tQ6FQCtIE5DWoixk9QEEWAeV37kARlABvaqDegAbrmL1IALlAEZGV2agBfampkbgtrWwMAJlAAXmdXdy8ff0Dg1jZwyLoAVWZ2Lh5QVHUJflAlSFxROsY5fFAWAmk6CnRoLGwmILzQQmV8JmQmDzI-SOiKgGV+CaYAL0gBBdyy1KCQ-Pn1AFFplgA5enw1PtSWS+vCsAAVAAtB4QQWOEMKBuYVUiVCYvYQsUTQcRSBDGMGmKSgAAa-VEgiQe2GLgKQA).
- Nomes de interfaces [_sempre_ aparecem na forma original](/play?#code/PTAEGEHsFsAcEsA2BTATqNrLusgzngIYDm+oA7koqIYuYQJ56gCueyoAUCKAC4AWHAHaFcoSADMaQ0PCG80EwgGNkALk6c5C1EtWgAsqOi1QAb06groEbjWg8vVHOKcAvpokshy3vEgyyMr8kEbQJogAFND2YREAlOaW1soBeJAoAHSIkMTRmbbI8e6aPMiZxJmgACqCGKhY6ABGyDnkFFQ0dIzMbBwCwqIccabcYLyQoKjIEmh8kwN8DLAc5PzwwbLMyAAeK77IACYaQSEjUWY2Q-YAjABMAMwALA+gbsVjNXW8yxySoAADaAA0CCaZbPh1XYqXgOIY0ZgmcK0AA0nyaLFhhGY8F4AHJmEJILCWsgZId4NNfIgGFdcIcUTVfgBlZTOWC8T7kAJ42G4eT+GS42QyRaYbCgXAEEguTzeXyCjDBSAAQSE8Ai0Xsl0K9kcziExDeiQs1lAqSE6SyOTy0AKQ2KHk4p1V6s1OuuoHuzwArMagA) nas mensagens de erro, mas _só_ quando são usados pelo nome.
- Usar interfaces com `extends` [pode ser, muitas vezes, mais performático para o compilador](https://github.com/microsoft/TypeScript/wiki/Performance#preferring-interfaces-over-intersections) do que aliases de tipo com interseções

Na maior parte das vezes, você pode escolher com base na preferência pessoal, e o TypeScript vai avisar se precisar que algo seja do outro tipo de declaração. Se quiser uma heurística, use `interface` até precisar de recursos de `type`.

## Asserções de tipo {#type-assertions}

Às vezes você terá informações sobre o tipo de um valor que o TypeScript não consegue saber.

Por exemplo, se você está usando `document.getElementById`, o TypeScript só sabe que isso vai retornar _algum_ tipo de `HTMLElement`, mas você pode saber que sua página sempre terá um `HTMLCanvasElement` com um determinado ID.

Nessa situação, você pode usar uma _asserção de tipo_ para especificar um tipo mais específico:

```ts twoslash
const myCanvas = document.getElementById("main_canvas") as HTMLCanvasElement;
```

Assim como uma anotação de tipo, asserções de tipo são removidas pelo compilador e não afetam o comportamento em tempo de execução do seu código.

Você também pode usar a sintaxe com colchetes angulares (exceto se o código estiver em um arquivo `.tsx`), que é equivalente:

```ts twoslash
const myCanvas = <HTMLCanvasElement>document.getElementById("main_canvas");
```

> Lembrete: como asserções de tipo são removidas em tempo de compilação, não há nenhuma verificação em tempo de execução associada a uma asserção de tipo.
> Não haverá uma exceção nem um `null` gerado se a asserção de tipo estiver errada.

O TypeScript só permite asserções de tipo que convertem para uma versão _mais específica_ ou _menos específica_ de um tipo.
Essa regra evita coerções "impossíveis" como:

```ts twoslash
// @errors: 2352
const x = "hello" as number;
```

Às vezes essa regra pode ser conservadora demais e vai proibir coerções mais complexas que poderiam ser válidas.
Se isso acontecer, você pode usar duas asserções: primeiro para `any` (ou `unknown`, que vamos apresentar mais adiante), e depois para o tipo desejado:

```ts twoslash
declare const expr: any;
type T = { a: 1; b: 2; c: 3 };
// ---cut---
const a = expr as any as T;
```

## Tipos literais {#literal-types}

Além dos tipos gerais `string` e `number`, podemos nos referir a strings e números _específicos_ em posições de tipo.

Uma forma de pensar nisso é considerar como o JavaScript oferece diferentes formas de declarar uma variável. Tanto `var` quanto `let` permitem mudar o que está guardado dentro da variável, e `const` não. Isso se reflete em como o TypeScript cria tipos para literais.

```ts twoslash
let changingString = "Hello World";
changingString = "Olá Mundo";
// Because `changingString` can represent any possible string, that
// is how TypeScript describes it in the type system
changingString;
// ^?

const constantString = "Hello World";
// Because `constantString` can only represent 1 possible string, it
// has a literal type representation
constantString;
// ^?
```

Por si só, tipos literais não são muito valiosos:

```ts twoslash
// @errors: 2322
let x: "hello" = "hello";
// OK
x = "hello";
// ...
x = "howdy";
```

Não adianta muito ter uma variável que só pode ter um valor!

Mas, ao _combinar_ literais em unions, você pode expressar um conceito muito mais útil - por exemplo, funções que só aceitam um certo conjunto de valores conhecidos:

```ts twoslash
// @errors: 2345
function printText(s: string, alignment: "left" | "right" | "center") {
  // ...
}
printText("Hello, world", "left");
printText("G'day, mate", "centre");
```

Tipos literais numéricos funcionam da mesma forma:

```ts twoslash
function compare(a: string, b: string): -1 | 0 | 1 {
  return a === b ? 0 : a > b ? 1 : -1;
}
```

É claro que você pode combinar esses tipos com tipos não literais:

```ts twoslash
// @errors: 2345
interface Options {
  width: number;
}
function configure(x: Options | "auto") {
  // ...
}
configure({ width: 100 });
configure("auto");
configure("automatic");
```

Existe mais um tipo de literal: literais booleanos.
Há apenas dois tipos literais booleanos e, como você deve imaginar, eles são os tipos `true` e `false`.
O tipo `boolean` em si é, na verdade, apenas um alias para a union `true | false`.

### Inferência de literais {#literal-inference}

Quando você inicializa uma variável com um objeto, o TypeScript assume que as propriedades desse objeto podem mudar de valor depois.
Por exemplo, se você escrevesse código assim:

```ts twoslash
declare const someCondition: boolean;
// ---cut---
const obj = { counter: 0 };
if (someCondition) {
  obj.counter = 1;
}
```

O TypeScript não assume que atribuir `1` a um campo que antes tinha `0` seja um erro.
Dizendo de outra forma, `obj.counter` precisa ter o tipo `number`, e não `0`, porque os tipos são usados para determinar tanto o comportamento de _leitura_ quanto o de _escrita_.

O mesmo vale para strings:

```ts twoslash
// @errors: 2345
declare function handleRequest(url: string, method: "GET" | "POST"): void;

const req = { url: "https://example.com", method: "GET" };
handleRequest(req.url, req.method);
```

No exemplo acima, `req.method` é inferido como `string`, e não como `"GET"`. Como pode haver código executado entre a criação de `req` e a chamada de `handleRequest` — código que poderia atribuir uma nova string como `"GUESS"` a `req.method` —, o TypeScript considera que esse código tem um erro.

Há duas formas de contornar isso.

1. Você pode mudar a inferência adicionando uma asserção de tipo em qualquer um dos dois lugares:

   ```ts twoslash
   declare function handleRequest(url: string, method: "GET" | "POST"): void;
   // ---cut---
   // Change 1:
   const req = { url: "https://example.com", method: "GET" as "GET" };
   // Change 2
   handleRequest(req.url, req.method as "GET");
   ```

   A mudança 1 significa "pretendo que `req.method` sempre tenha o _tipo literal_ `"GET"`", impedindo a possível atribuição de `"GUESS"` a esse campo depois.
   A mudança 2 significa "sei, por outros motivos, que `req.method` tem o valor `"GET"`".

2. Você pode usar `as const` para converter o objeto inteiro em literais de tipo:

   ```ts twoslash
   declare function handleRequest(url: string, method: "GET" | "POST"): void;
   // ---cut---
   const req = { url: "https://example.com", method: "GET" } as const;
   handleRequest(req.url, req.method);
   ```

O sufixo `as const` age como `const`, mas para o sistema de tipos, garantindo que todas as propriedades recebam o tipo literal em vez de uma versão mais geral como `string` ou `number`.

## `null` e `undefined` {#null-and-undefined}

O JavaScript tem dois valores primitivos usados para sinalizar um valor ausente ou não inicializado: `null` e `undefined`.

O TypeScript tem dois _tipos_ correspondentes com os mesmos nomes. Como esses tipos se comportam depende de a opção [`strictNullChecks`](/tsconfig#strictNullChecks) estar ativada ou não.

### `strictNullChecks` desativada {#strictnullchecks-off}

Com [`strictNullChecks`](/tsconfig#strictNullChecks) _desativada_, valores que podem ser `null` ou `undefined` ainda podem ser acessados normalmente, e os valores `null` e `undefined` podem ser atribuídos a uma propriedade de qualquer tipo.
Isso é parecido com o comportamento de linguagens sem verificação de null (por exemplo, C# e Java).
A falta de verificação desses valores tende a ser uma grande fonte de bugs; sempre recomendamos ativar a [`strictNullChecks`](/tsconfig#strictNullChecks) se for viável na sua base de código.

### `strictNullChecks` ativada {#strictnullchecks-on}

Com [`strictNullChecks`](/tsconfig#strictNullChecks) _ativada_, quando um valor é `null` ou `undefined`, você precisará testar esses valores antes de usar métodos ou propriedades desse valor.
Assim como verificar `undefined` antes de usar uma propriedade opcional, podemos usar _narrowing_ para verificar valores que podem ser `null`:

```ts twoslash
function doSomething(x: string | null) {
  if (x === null) {
    // do nothing
  } else {
    console.log("Hello, " + x.toUpperCase());
  }
}
```

### Operador de asserção de não nulo (`!` pós-fixo) {#non-null-assertion-operator-postfix-}

O TypeScript também tem uma sintaxe especial para remover `null` e `undefined` de um tipo sem fazer nenhuma verificação explícita.
Escrever `!` depois de qualquer expressão é, na prática, uma asserção de tipo de que o valor não é `null` nem `undefined`:

```ts twoslash
function liveDangerously(x?: number | null) {
  // No error
  console.log(x!.toFixed());
}
```

Assim como outras asserções de tipo, isso não muda o comportamento em tempo de execução do seu código, então é importante usar `!` apenas quando você sabe que o valor _não pode_ ser `null` ou `undefined`.

## Enums

Enums são um recurso adicionado ao JavaScript pelo TypeScript que permite descrever um valor que pode ser um de um conjunto de constantes nomeadas possíveis. Diferentemente da maioria dos recursos do TypeScript, isso _não_ é uma adição de nível de tipo ao JavaScript, mas algo adicionado à linguagem e ao runtime. Por causa disso, é um recurso que você deve saber que existe, mas talvez deva evitar usar a menos que tenha certeza. Você pode ler mais sobre enums na [página de referência de Enums](/docs/handbook/enums.html).

## Primitivos menos comuns {#less-common-primitives}

Vale mencionar os demais primitivos do JavaScript que são representados no sistema de tipos.
Ainda que não vamos entrar em detalhes aqui.

### `bigint`

A partir do ES2020, existe um primitivo no JavaScript usado para inteiros muito grandes, `BigInt`:

```ts twoslash
// @target: es2020

// Creating a bigint via the BigInt function
const oneHundred: bigint = BigInt(100);

// Creating a BigInt via the literal syntax
const anotherHundred: bigint = 100n;
```

Você pode saber mais sobre BigInt nas [notas de versão do TypeScript 3.2](/docs/handbook/release-notes/typescript-3-2.html#bigint).

### `symbol`

Existe um primitivo no JavaScript usado para criar uma referência globalmente única através da função `Symbol()`:

```ts twoslash
// @errors: 2367
const firstName = Symbol("name");
const secondName = Symbol("name");

if (firstName === secondName) {
  // Can't ever happen
}
```

Você pode saber mais sobre eles na [página de referência de Symbols](/docs/handbook/symbols.html).
