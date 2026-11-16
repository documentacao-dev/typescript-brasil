---
title: Narrowing
layout: docs
permalink: /docs/handbook/2/narrowing.html
oneline: "Entenda como o TypeScript usa o conhecimento do JavaScript para reduzir a quantidade de sintaxe de tipos nos seus projetos."
ia-translate: true
---

Imagine que temos uma função chamada `padLeft`.

```ts twoslash
function padLeft(padding: number | string, input: string): string {
  throw new Error("Not implemented yet!");
}
```

Se `padding` for um `number`, ele será tratado como a quantidade de espaços que queremos adicionar no início de `input`.
Se `padding` for uma `string`, basta adicionar `padding` no início de `input`.
Vamos tentar implementar a lógica para quando `padLeft` recebe um `number` em `padding`.

```ts twoslash
// @errors: 2345
function padLeft(padding: number | string, input: string): string {
  return " ".repeat(padding) + input;
}
```

Opa, estamos recebendo um erro em `padding`.
O TypeScript está avisando que estamos passando um valor do tipo `number | string` para a função `repeat`, que só aceita um `number`, e ele tem razão.
Em outras palavras, não verificamos explicitamente se `padding` é um `number` antes, nem tratamos o caso em que ele é uma `string`. Então vamos fazer exatamente isso.

```ts twoslash
function padLeft(padding: number | string, input: string): string {
  if (typeof padding === "number") {
    return " ".repeat(padding) + input;
  }
  return padding + input;
}
```

Se isso parece, na maior parte, um código JavaScript sem graça, esse é meio que o ponto.
Fora as anotações que colocamos, este código TypeScript parece JavaScript.
A ideia é que o sistema de tipos do TypeScript procura tornar o mais fácil possível escrever código JavaScript típico, sem precisar fazer malabarismos para ter segurança de tipos.

Pode não parecer muita coisa, mas há bastante coisa acontecendo por trás.
Assim como o TypeScript analisa valores em tempo de execução usando tipos estáticos, ele sobrepõe uma análise de tipos às estruturas de controle de fluxo do JavaScript, como `if/else`, ternários condicionais, laços, verificações de truthiness etc., que podem todas afetar esses tipos.

Dentro do nosso `if`, o TypeScript vê `typeof padding === "number"` e entende isso como uma forma especial de código chamada _type guard_.
O TypeScript segue os possíveis caminhos de execução que o programa pode seguir para analisar o tipo mais específico possível de um valor em uma dada posição.
Ele observa essas verificações especiais (chamadas de _type guards_) e atribuições, e o processo de refinar os tipos para tipos mais específicos do que os declarados é chamado de _narrowing_.
Em muitos editores podemos observar esses tipos mudando, e faremos isso nos nossos exemplos.

```ts twoslash
function padLeft(padding: number | string, input: string): string {
  if (typeof padding === "number") {
    return " ".repeat(padding) + input;
    //                ^?
  }
  return padding + input;
  //     ^?
}
```

Existem algumas construções diferentes que o TypeScript entende para fazer narrowing.

## Type guards com `typeof` {#typeof-type-guards}

Como vimos, o JavaScript tem um operador `typeof` que pode dar informações bem básicas sobre o tipo dos valores que temos em tempo de execução.
O TypeScript espera que ele retorne um conjunto específico de strings:

- `"string"`
- `"number"`
- `"bigint"`
- `"boolean"`
- `"symbol"`
- `"undefined"`
- `"object"`
- `"function"`

Assim como vimos com `padLeft`, esse operador aparece com bastante frequência em várias bibliotecas JavaScript, e o TypeScript consegue entendê-lo para fazer narrowing de tipos em diferentes ramos.

No TypeScript, comparar com o valor retornado por `typeof` é um type guard.
Como o TypeScript codifica como `typeof` opera sobre diferentes valores, ele conhece algumas das peculiaridades dessa operação no JavaScript.
Por exemplo, repare que, na lista acima, `typeof` não retorna a string `null`.
Veja o exemplo a seguir:

```ts twoslash
// @errors: 2531 18047
function printAll(strs: string | string[] | null) {
  if (typeof strs === "object") {
    for (const s of strs) {
      console.log(s);
    }
  } else if (typeof strs === "string") {
    console.log(strs);
  } else {
    // do nothing
  }
}
```

Na função `printAll`, tentamos verificar se `strs` é um objeto para saber se ele é um tipo de array (agora pode ser um bom momento para reforçar que arrays são tipos de objeto em JavaScript).
Mas acontece que, em JavaScript, `typeof null` é, na verdade, `"object"`!
Esse é um daqueles acidentes infelizes da história.

Quem tem bastante experiência talvez não se surpreenda, mas nem todo mundo já esbarrou nisso em JavaScript. Felizmente, o TypeScript nos avisa que `strs` foi restringido apenas a `string[] | null`, e não só a `string[]`.

Isso pode ser uma boa transição para o que vamos chamar de verificação de "truthiness".

## Narrowing por truthiness {#truthiness-narrowing}

Truthiness talvez não seja uma palavra que você encontre no dicionário, mas é algo sobre o qual você vai ouvir muito em JavaScript.

Em JavaScript, podemos usar qualquer expressão em condicionais, `&&`, `||`, instruções `if`, negações booleanas (`!`) e mais.
Como exemplo, instruções `if` não esperam que a condição tenha sempre o tipo `boolean`.

```ts twoslash
function getUsersOnlineMessage(numUsersOnline: number) {
  if (numUsersOnline) {
    return `There are ${numUsersOnline} online now!`;
  }
  return "Nobody's here. :(";
}
```

Em JavaScript, construções como `if` primeiro "convertem" suas condições para `boolean` para interpretá-las, e então escolhem o ramo dependendo de o resultado ser `true` ou `false`.
Valores como

- `0`
- `NaN`
- `""` (a string vazia)
- `0n` (a versão `bigint` do zero)
- `null`
- `undefined`

são todos convertidos para `false`, e os demais valores são convertidos para `true`.
Você sempre pode converter valores para `boolean` passando-os pela função `Boolean`, ou usando a dupla negação booleana, que é mais curta. (Esta última tem a vantagem de o TypeScript inferir o literal booleano `true`, enquanto a primeira é inferida como `boolean`.)

```ts twoslash
// both of these result in 'true'
Boolean("hello"); // type: boolean, value: true
!!"world"; // type: true,    value: true
```

É bastante comum aproveitar esse comportamento, especialmente para proteger contra valores como `null` ou `undefined`.
Como exemplo, vamos tentar usá-lo na nossa função `printAll`.

```ts twoslash
function printAll(strs: string | string[] | null) {
  if (strs && typeof strs === "object") {
    for (const s of strs) {
      console.log(s);
    }
  } else if (typeof strs === "string") {
    console.log(strs);
  }
}
```

Você vai notar que eliminamos o erro de antes ao verificar se `strs` é truthy.
Isso pelo menos evita os temidos erros quando rodamos o código, como:

```txt
TypeError: null is not iterable
```

Tenha em mente, porém, que verificar truthiness em primitivos pode ser propenso a erros.
Como exemplo, considere outra tentativa de escrever `printAll`

```ts twoslash {class: "do-not-do-this"}
function printAll(strs: string | string[] | null) {
  // !!!!!!!!!!!!!!!!
  //  DON'T DO THIS!
  //   KEEP READING
  // !!!!!!!!!!!!!!!!
  if (strs) {
    if (typeof strs === "object") {
      for (const s of strs) {
        console.log(s);
      }
    } else if (typeof strs === "string") {
      console.log(strs);
    }
  }
}
```

Envolvemos todo o corpo da função em uma verificação de truthy, mas isso tem uma desvantagem sutil: podemos deixar de tratar corretamente o caso da string vazia.

O TypeScript não nos prejudica em nada aqui, mas vale a pena notar esse comportamento se você não está tão familiarizado com JavaScript.
O TypeScript pode frequentemente ajudar a pegar bugs cedo, mas, se você escolher não fazer _nada_ com um valor, há só até onde ele consegue ir sem ser excessivamente prescritivo.
Se quiser, você pode garantir que trate situações como essas com um linter.

Uma última observação sobre narrowing por truthiness é que negações booleanas com `!` filtram os valores nos ramos negados.

```ts twoslash
function multiplyAll(
  values: number[] | undefined,
  factor: number
): number[] | undefined {
  if (!values) {
    return values;
  } else {
    return values.map((x) => x * factor);
  }
}
```

## Narrowing por igualdade {#equality-narrowing}

O TypeScript também usa instruções `switch` e verificações de igualdade como `===`, `!==`, `==` e `!=` para fazer narrowing de tipos.
Por exemplo:

```ts twoslash
function example(x: string | number, y: string | boolean) {
  if (x === y) {
    // We can now call any 'string' method on 'x' or 'y'.
    x.toUpperCase();
    // ^?
    y.toLowerCase();
    // ^?
  } else {
    console.log(x);
    //          ^?
    console.log(y);
    //          ^?
  }
}
```

Quando verificamos que `x` e `y` são iguais no exemplo acima, o TypeScript sabe que os tipos deles também precisam ser iguais.
Como `string` é o único tipo comum que `x` e `y` podem assumir, o TypeScript sabe que `x` e `y` precisam ser `string`s no primeiro ramo.

Comparar com valores literais específicos (em vez de variáveis) também funciona.
Na seção sobre narrowing por truthiness, escrevemos uma função `printAll` que era propensa a erros porque, sem querer, não tratava corretamente as strings vazias.
Em vez disso, poderíamos ter feito uma verificação específica para barrar os `null`, e o TypeScript ainda assim remove corretamente o `null` do tipo de `strs`.

```ts twoslash
function printAll(strs: string | string[] | null) {
  if (strs !== null) {
    if (typeof strs === "object") {
      for (const s of strs) {
        //            ^?
        console.log(s);
      }
    } else if (typeof strs === "string") {
      console.log(strs);
      //          ^?
    }
  }
}
```

As verificações de igualdade mais frouxas do JavaScript, com `==` e `!=`, também são corretamente tratadas no narrowing.
Se você não está familiarizado, verificar se algo `== null` não checa apenas se o valor é exatamente `null`: também checa se ele pode ser `undefined`.
O mesmo vale para `== undefined`: ele verifica se o valor é `null` ou `undefined`.

```ts twoslash
interface Container {
  value: number | null | undefined;
}

function multiplyValue(container: Container, factor: number) {
  // Remove both 'null' and 'undefined' from the type.
  if (container.value != null) {
    console.log(container.value);
    //                    ^?

    // Now we can safely multiply 'container.value'.
    container.value *= factor;
  }
}
```

## Narrowing com o operador `in` {#the-in-operator-narrowing}

O JavaScript tem um operador para determinar se um objeto, ou sua cadeia de protótipos, possui uma propriedade com determinado nome: o operador `in`.
O TypeScript leva isso em conta como uma forma de restringir os tipos possíveis.

Por exemplo, com o código `"value" in x`, em que `"value"` é um literal de string e `x` é um tipo union. O ramo "verdadeiro" restringe os tipos de `x` que têm a propriedade `value`, seja ela opcional ou obrigatória, e o ramo "falso" restringe para os tipos que têm a propriedade `value` opcional ou ausente.

```ts twoslash
type Fish = { swim: () => void };
type Bird = { fly: () => void };

function move(animal: Fish | Bird) {
  if ("swim" in animal) {
    return animal.swim();
  }

  return animal.fly();
}
```

Reforçando: propriedades opcionais existirão nos dois lados para o narrowing. Por exemplo, um ser humano pode nadar e voar (com o equipamento certo), então deve aparecer nos dois lados da verificação `in`:

<!-- prettier-ignore -->
```ts twoslash
type Fish = { swim: () => void };
type Bird = { fly: () => void };
type Human = { swim?: () => void; fly?: () => void };

function move(animal: Fish | Bird | Human) {
  if ("swim" in animal) {
    animal;
//  ^?
  } else {
    animal;
//  ^?
  }
}
```

## Narrowing com `instanceof` {#instanceof-narrowing}

O JavaScript tem um operador para verificar se um valor é uma "instância" de outro valor.
Mais especificamente, em JavaScript, `x instanceof Foo` verifica se a _cadeia de protótipos_ de `x` contém `Foo.prototype`.
Não vamos nos aprofundar aqui, e você verá mais sobre isso quando chegarmos a classes, mas eles ainda são úteis para a maioria dos valores que podem ser construídos com `new`.
Como você deve ter imaginado, `instanceof` também é um type guard, e o TypeScript faz narrowing nos ramos protegidos por `instanceof`.

```ts twoslash
function logValue(x: Date | string) {
  if (x instanceof Date) {
    console.log(x.toUTCString());
    //          ^?
  } else {
    console.log(x.toUpperCase());
    //          ^?
  }
}
```

## Atribuições {#assignments}

Como mencionamos antes, quando atribuímos a qualquer variável, o TypeScript analisa o lado direito da atribuição e faz o narrowing do lado esquerdo de forma apropriada.

```ts twoslash
let x = Math.random() < 0.5 ? 10 : "hello world!";
//  ^?
x = 1;

console.log(x);
//          ^?
x = "goodbye!";

console.log(x);
//          ^?
```

Repare que cada uma dessas atribuições é válida.
Mesmo que o tipo observado de `x` tenha mudado para `number` depois da primeira atribuição, ainda conseguimos atribuir uma `string` a `x`.
Isso acontece porque o _tipo declarado_ de `x` (o tipo com que `x` começou) é `string | number`, e a atribuibilidade é sempre verificada contra o tipo declarado.

Se tivéssemos atribuído um `boolean` a `x`, veríamos um erro, já que ele não fazia parte do tipo declarado.

```ts twoslash
// @errors: 2322
let x = Math.random() < 0.5 ? 10 : "hello world!";
//  ^?
x = 1;

console.log(x);
//          ^?
x = true;

console.log(x);
//          ^?
```

## Análise de fluxo de controle {#control-flow-analysis}

Até aqui, passamos por alguns exemplos básicos de como o TypeScript faz narrowing dentro de ramos específicos.
Mas há um pouco mais acontecendo do que simplesmente subir a partir de cada variável procurando type guards em `if`s, `while`s, condicionais etc.
Por exemplo:

```ts twoslash
function padLeft(padding: number | string, input: string) {
  if (typeof padding === "number") {
    return " ".repeat(padding) + input;
  }
  return padding + input;
}
```

`padLeft` retorna de dentro do primeiro bloco `if`.
O TypeScript conseguiu analisar esse código e ver que o restante do corpo (`return padding + input;`) é _inalcançável_ no caso em que `padding` é um `number`.
Como resultado, ele conseguiu remover `number` do tipo de `padding` (fazendo o narrowing de `string | number` para `string`) pelo resto da função.

Essa análise do código com base em alcançabilidade é chamada de _análise de fluxo de controle_, e o TypeScript usa essa análise de fluxo para restringir tipos conforme encontra type guards e atribuições.
Quando uma variável é analisada, o fluxo de controle pode se dividir e se juntar de novo várias vezes, e a variável pode ser observada com um tipo diferente em cada ponto.

```ts twoslash
function example() {
  let x: string | number | boolean;

  x = Math.random() < 0.5;

  console.log(x);
  //          ^?

  if (Math.random() < 0.5) {
    x = "hello";
    console.log(x);
    //          ^?
  } else {
    x = 100;
    console.log(x);
    //          ^?
  }

  return x;
  //     ^?
}
```

## Usando type predicates {#using-type-predicates}

Até agora trabalhamos com construções existentes do JavaScript para lidar com o narrowing, mas às vezes você quer um controle mais direto sobre como os tipos mudam ao longo do seu código.

Para definir um type guard definido pelo usuário, basta definir uma função cujo tipo de retorno seja um _type predicate_:

```ts twoslash
type Fish = { swim: () => void };
type Bird = { fly: () => void };
declare function getSmallPet(): Fish | Bird;
// ---cut---
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}
```

`pet is Fish` é o type predicate neste exemplo.
Um predicate tem a forma `parameterName is Type`, onde `parameterName` precisa ser o nome de um parâmetro da assinatura atual da função.

Sempre que `isFish` é chamada com alguma variável, o TypeScript vai _restringir_ essa variável para aquele tipo específico, se o tipo original for compatível.

```ts twoslash
type Fish = { swim: () => void };
type Bird = { fly: () => void };
declare function getSmallPet(): Fish | Bird;
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}
// ---cut---
// Both calls to 'swim' and 'fly' are now okay.
let pet = getSmallPet();

if (isFish(pet)) {
  pet.swim();
} else {
  pet.fly();
}
```

Repare que o TypeScript não sabe apenas que `pet` é um `Fish` no ramo `if`;
ele também sabe que, no ramo `else`, você _não_ tem um `Fish`, então precisa ter um `Bird`.

Você pode usar o type guard `isFish` para filtrar um array de `Fish | Bird` e obter um array de `Fish`:

```ts twoslash
type Fish = { swim: () => void; name: string };
type Bird = { fly: () => void; name: string };
declare function getSmallPet(): Fish | Bird;
function isFish(pet: Fish | Bird): pet is Fish {
  return (pet as Fish).swim !== undefined;
}
// ---cut---
const zoo: (Fish | Bird)[] = [getSmallPet(), getSmallPet(), getSmallPet()];
const underWater1: Fish[] = zoo.filter(isFish);
// or, equivalently
const underWater2: Fish[] = zoo.filter(isFish) as Fish[];

// The predicate may need repeating for more complex examples
const underWater3: Fish[] = zoo.filter((pet): pet is Fish => {
  if (pet.name === "sharkey") return false;
  return isFish(pet);
});
```

Além disso, classes podem [usar `this is Type`](/docs/handbook/2/classes.html#this-based-type-guards) para restringir o próprio tipo.

## Funções de asserção {#assertion-functions}

Os tipos também podem ser restringidos usando [funções de asserção](/docs/handbook/release-notes/typescript-3-7.html#assertion-functions).

## Unions discriminadas {#discriminated-unions}

A maioria dos exemplos que vimos até agora se concentrou em restringir variáveis únicas com tipos simples como `string`, `boolean` e `number`.
Embora isso seja comum, na maior parte do tempo em JavaScript vamos lidar com estruturas um pouco mais complexas.

Como motivação, imagine que estamos tentando codificar formas como círculos e quadrados.
Círculos guardam seus raios, e quadrados guardam o comprimento dos lados.
Vamos usar um campo chamado `kind` para saber com qual forma estamos lidando.
Aqui está uma primeira tentativa de definir `Shape`.

```ts twoslash
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}
```

Repare que estamos usando uma union de tipos literais de string: `"circle"` e `"square"`, para dizer se devemos tratar a forma como um círculo ou um quadrado, respectivamente.
Ao usar `"circle" | "square"` em vez de `string`, evitamos erros de digitação.

```ts twoslash
// @errors: 2367
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}

// ---cut---
function handleShape(shape: Shape) {
  // oops!
  if (shape.kind === "rect") {
    // ...
  }
}
```

Podemos escrever uma função `getArea` que aplica a lógica certa dependendo de estarmos lidando com um círculo ou um quadrado.
Vamos começar tratando os círculos.

```ts twoslash
// @errors: 2532 18048
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}

// ---cut---
function getArea(shape: Shape) {
  return Math.PI * shape.radius ** 2;
}
```

<!-- TODO -->

Com [`strictNullChecks`](/tsconfig#strictNullChecks) isso gera um erro, o que é apropriado, já que `radius` pode não estar definido.
Mas e se fizermos a verificação apropriada na propriedade `kind`?

```ts twoslash
// @errors: 2532 18048
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}

// ---cut---
function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
  }
}
```

Hmm, o TypeScript continua sem saber o que fazer aqui.
Chegamos a um ponto em que sabemos mais sobre os nossos valores do que o verificador de tipos. Poderíamos tentar usar uma asserção de não nulo (um `!` depois de `shape.radius`) para dizer que `radius` com certeza está presente.

```ts twoslash
interface Shape {
  kind: "circle" | "square";
  radius?: number;
  sideLength?: number;
}

// ---cut---
function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius! ** 2;
  }
}
```

Mas isso não parece ideal.
Tivemos que falar um pouco alto com o verificador de tipos, com essas asserções de não nulo (`!`), para convencê-lo de que `shape.radius` estava definido, mas essas asserções são propensas a erros se começarmos a mover o código de lugar.
Além disso, fora do [`strictNullChecks`](/tsconfig#strictNullChecks), ainda podemos acessar acidentalmente qualquer um desses campos (já que propriedades opcionais são simplesmente assumidas como sempre presentes na leitura).
Podemos fazer muito melhor.

O problema dessa codificação de `Shape` é que o verificador de tipos não tem como saber se `radius` ou `sideLength` estão presentes com base na propriedade `kind`.
Precisamos comunicar ao verificador de tipos o que _nós_ sabemos.
Com isso em mente, vamos dar outra tentativa para definir `Shape`.

```ts twoslash
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

type Shape = Circle | Square;
```

Aqui, separamos corretamente `Shape` em dois tipos com valores diferentes para a propriedade `kind`, mas `radius` e `sideLength` são declarados como propriedades obrigatórias nos respectivos tipos.

Vamos ver o que acontece quando tentamos acessar o `radius` de um `Shape`.

```ts twoslash
// @errors: 2339
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

type Shape = Circle | Square;

// ---cut---
function getArea(shape: Shape) {
  return Math.PI * shape.radius ** 2;
}
```

Assim como na nossa primeira definição de `Shape`, isso ainda é um erro.
Quando `radius` era opcional, recebíamos um erro (com [`strictNullChecks`](/tsconfig#strictNullChecks) ativado) porque o TypeScript não conseguia saber se a propriedade estava presente.
Agora que `Shape` é uma union, o TypeScript está nos dizendo que `shape` pode ser um `Square`, e `Square`s não têm `radius` definido!
As duas interpretações estão corretas, mas só a codificação de `Shape` como union vai gerar um erro independentemente de como o [`strictNullChecks`](/tsconfig#strictNullChecks) estiver configurado.

Mas e se tentarmos verificar a propriedade `kind` de novo?

```ts twoslash
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

type Shape = Circle | Square;

// ---cut---
function getArea(shape: Shape) {
  if (shape.kind === "circle") {
    return Math.PI * shape.radius ** 2;
    //               ^?
  }
}
```

Isso eliminou o erro!
Quando todo tipo em uma union contém uma propriedade em comum com tipos literais, o TypeScript considera que é uma _union discriminada_, e pode fazer o narrowing removendo os membros da union.

Neste caso, `kind` era essa propriedade em comum (que é o que se considera uma propriedade _discriminante_ de `Shape`).
Verificar se a propriedade `kind` é `"circle"` eliminou todos os tipos em `Shape` que não tinham uma propriedade `kind` com o tipo `"circle"`.
Isso restringiu `shape` ao tipo `Circle`.

A mesma verificação funciona com instruções `switch`.
Agora podemos tentar escrever nossa `getArea` completa, sem nenhuma asserção de não nulo incômoda (`!`).

```ts twoslash
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}

type Shape = Circle | Square;

// ---cut---
function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    //                 ^?
    case "square":
      return shape.sideLength ** 2;
    //       ^?
  }
}
```

O ponto importante aqui foi a codificação de `Shape`.
Comunicar a informação certa ao TypeScript (que `Circle` e `Square` eram realmente dois tipos separados, com campos `kind` específicos) foi crucial.
Fazendo isso, conseguimos escrever código TypeScript com segurança de tipos que não é diferente do JavaScript que escreveríamos de qualquer forma.
A partir daí, o sistema de tipos conseguiu fazer a coisa "certa" e descobrir os tipos em cada ramo da nossa instrução `switch`.

> Como um aparte, experimente mexer no exemplo acima e remover algumas das palavras-chave return.
> Você verá que a verificação de tipos ajuda a evitar bugs ao cair acidentalmente de uma cláusula para outra em uma instrução `switch`.

Unions discriminadas são úteis para mais do que falar sobre círculos e quadrados.
Elas são boas para representar qualquer tipo de esquema de mensagens em JavaScript, como quando enviamos mensagens pela rede (comunicação cliente/servidor), ou para codificar mutações em um framework de gerenciamento de estado.

## O tipo `never` {#the-never-type}

Ao fazer narrowing, você pode reduzir as opções de uma union a um ponto em que removeu todas as possibilidades e não sobrou nada.
Nesses casos, o TypeScript usará o tipo `never` para representar um estado que não deveria existir.

## Verificação de exaustividade {#exhaustiveness-checking}

O tipo `never` é atribuível a todos os tipos; porém, nenhum tipo é atribuível a `never` (exceto o próprio `never`). Isso significa que você pode usar narrowing e contar com o `never` aparecendo para fazer uma verificação de exaustividade em uma instrução `switch`.

Por exemplo, adicionar um `default` à nossa função `getArea` que tenta atribuir a forma a `never` não gera erro quando todos os casos possíveis foram tratados.

```ts twoslash
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}
// ---cut---
type Shape = Circle | Square;

function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    default:
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
  }
}
```

Adicionar um novo membro à union `Shape` vai causar um erro de TypeScript:

```ts twoslash
// @errors: 2322
interface Circle {
  kind: "circle";
  radius: number;
}

interface Square {
  kind: "square";
  sideLength: number;
}
// ---cut---
interface Triangle {
  kind: "triangle";
  sideLength: number;
}

type Shape = Circle | Square | Triangle;

function getArea(shape: Shape) {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "square":
      return shape.sideLength ** 2;
    default:
      const _exhaustiveCheck: never = shape;
      return _exhaustiveCheck;
  }
}
```
