---
title: Tipos de template literal
layout: docs
permalink: /docs/handbook/2/template-literal-types.html
oneline: "Gerando tipos de mapeamento que alteram propriedades por meio de strings de template literal."
ia-translate: true
---

Tipos de template literal são construídos sobre [tipos de string literal](/docs/handbook/2/everyday-types.html#literal-types) e têm a capacidade de se expandir em muitas strings por meio de uniões.

Eles têm a mesma sintaxe dos [template literals de strings em JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals), mas são usados em posições de tipo.
Quando usado com tipos literais concretos, um template literal produz um novo tipo de string literal, concatenando o conteúdo.

```ts twoslash
type World = "world";

type Greeting = `hello ${World}`;
//   ^?
```

Quando uma união é usada na posição interpolada, o tipo é o conjunto de todos os string literals possíveis que cada membro da união pode representar:

```ts twoslash
type EmailLocaleIDs = "welcome_email" | "email_heading";
type FooterLocaleIDs = "footer_title" | "footer_sendoff";

type AllLocaleIDs = `${EmailLocaleIDs | FooterLocaleIDs}_id`;
//   ^?
```

Para cada posição interpolada no template literal, as uniões são multiplicadas em produto cartesiano:

```ts twoslash
type EmailLocaleIDs = "welcome_email" | "email_heading";
type FooterLocaleIDs = "footer_title" | "footer_sendoff";
// ---cut---
type AllLocaleIDs = `${EmailLocaleIDs | FooterLocaleIDs}_id`;
type Lang = "en" | "ja" | "pt";

type LocaleMessageIDs = `${Lang}_${AllLocaleIDs}`;
//   ^?
```

Em geral, recomendamos gerar com antecedência as uniões de strings grandes, mas isso é útil em casos menores.

## Uniões de strings em tipos {#string-unions-in-types}

O poder dos template literals aparece quando você define uma nova string com base em informações dentro de um tipo.

Considere o caso em que uma função (`makeWatchedObject`) adiciona uma nova função chamada `on()` a um objeto passado para ela.
Em JavaScript, a chamada poderia ser assim:
`makeWatchedObject(baseObject)`. Podemos imaginar que o objeto base seja assim:

```ts twoslash
// @noErrors
const passedObject = {
  firstName: "Saoirse",
  lastName: "Ronan",
  age: 26,
};
```

A função `on` que será adicionada ao objeto base espera dois argumentos: um `eventName` (uma `string`) e um `callback` (uma `function`).

O `eventName` deve ter a forma `propriedadeDoObjetoPassado + "Changed"`; assim, `firstNameChanged` é derivado da propriedade `firstName` do objeto base.

A função `callback`, quando chamada:
  * Deve receber um valor do tipo associado ao nome `propriedadeDoObjetoPassado`; assim, como `firstName` é tipada como `string`, o callback do evento `firstNameChanged` espera receber uma `string` no momento da chamada. Da mesma forma, eventos associados a `age` devem esperar ser chamados com um argumento `number`
  * Deve ter tipo de retorno `void` (por simplicidade da demonstração)

A assinatura ingênua da função `on()` poderia então ser: `on(eventName: string, callback: (newValue: any) => void)`. No entanto, na descrição anterior, identificamos restrições de tipo importantes que gostaríamos de documentar no nosso código. Tipos de template literal nos permitem trazer essas restrições para o código.

```ts twoslash
// @noErrors
declare function makeWatchedObject(obj: any): any;
// ---cut---
const person = makeWatchedObject({
  firstName: "Saoirse",
  lastName: "Ronan",
  age: 26,
});

// makeWatchedObject has added `on` to the anonymous Object

person.on("firstNameChanged", (newValue) => {
  console.log(`firstName was changed to ${newValue}!`);
});
```

Repare que `on` escuta o evento `"firstNameChanged"`, e não apenas `"firstName"`. Nossa especificação ingênua de `on()` poderia ser mais robusta se garantíssemos que o conjunto de nomes de evento elegíveis fosse restrito à união dos nomes de atributos do objeto observado com "Changed" no final. Embora estejamos à vontade para fazer esse cálculo em JavaScript, isto é, ``Object.keys(passedObject).map(x => `${x}Changed`)``, template literals _dentro do sistema de tipos_ oferecem uma abordagem semelhante para manipulação de strings:

```ts twoslash
type PropEventSource<Type> = {
    on(eventName: `${string & keyof Type}Changed`, callback: (newValue: any) => void): void;
};

/// Create a "watched object" with an `on` method
/// so that you can watch for changes to properties.
declare function makeWatchedObject<Type>(obj: Type): Type & PropEventSource<Type>;
```

Com isso, podemos construir algo que gera erro quando recebe a propriedade errada:

```ts twoslash
// @errors: 2345
type PropEventSource<Type> = {
    on(eventName: `${string & keyof Type}Changed`, callback: (newValue: any) => void): void;
};

declare function makeWatchedObject<T>(obj: T): T & PropEventSource<T>;
// ---cut---
const person = makeWatchedObject({
  firstName: "Saoirse",
  lastName: "Ronan",
  age: 26
});

person.on("firstNameChanged", () => {});

// Prevent easy human error (using the key instead of the event name)
person.on("firstName", () => {});

// It's typo-resistant
person.on("frstNameChanged", () => {});
```

## Inferência com template literals {#inference-with-template-literals}

Repare que não aproveitamos todas as informações fornecidas no objeto original passado. Dada a mudança de um `firstName` (ou seja, um evento `firstNameChanged`), devemos esperar que o callback receba um argumento do tipo `string`. Da mesma forma, o callback para a mudança de `age` deve receber um argumento `number`. Estamos usando `any` de forma ingênua para tipar o argumento do `callback`. Mais uma vez, tipos de template literal tornam possível garantir que o tipo de dado de um atributo seja o mesmo tipo do primeiro argumento do callback desse atributo.

A ideia-chave que torna isso possível é: podemos usar uma função com um genérico de modo que:

1. O literal usado no primeiro argumento seja capturado como um tipo literal
2. Esse tipo literal possa ser validado como pertencente à união dos atributos válidos no genérico
3. O tipo do atributo validado possa ser buscado na estrutura do genérico usando Indexed Access
4. Essa informação de tipo _então_ possa ser aplicada para garantir que o argumento da
   função callback seja do mesmo tipo

```ts twoslash
type PropEventSource<Type> = {
    on<Key extends string & keyof Type>
        (eventName: `${Key}Changed`, callback: (newValue: Type[Key]) => void): void;
};

declare function makeWatchedObject<Type>(obj: Type): Type & PropEventSource<Type>;

const person = makeWatchedObject({
  firstName: "Saoirse",
  lastName: "Ronan",
  age: 26
});

person.on("firstNameChanged", newName => {
    //                        ^?
    console.log(`new name is ${newName.toUpperCase()}`);
});

person.on("ageChanged", newAge => {
    //                  ^?
    if (newAge < 0) {
        console.warn("warning! negative age");
    }
})
```

Aqui transformamos `on` em um método genérico.

Quando o usuário chama com a string `"firstNameChanged"`, o TypeScript tenta inferir o tipo certo para `Key`.
Para isso, ele compara `Key` com o conteúdo antes de `"Changed"` e infere a string `"firstName"`.
Depois que o TypeScript descobre isso, o método `on` pode buscar o tipo de `firstName` no objeto original, que neste caso é `string`.
Da mesma forma, quando chamado com `"ageChanged"`, o TypeScript encontra o tipo da propriedade `age`, que é `number`.

A inferência pode ser combinada de diferentes maneiras, muitas vezes para desconstruir strings e reconstruí-las de outras formas.

## Tipos intrínsecos de manipulação de strings {#intrinsic-string-manipulation-types}

Para ajudar na manipulação de strings, o TypeScript inclui um conjunto de tipos que podem ser usados nessa tarefa. Esses tipos vêm integrados ao compilador por questão de desempenho e não podem ser encontrados nos arquivos `.d.ts` incluídos com o TypeScript.

### `Uppercase<StringType>`

Converte cada caractere da string para sua versão em maiúsculas.

#### Exemplo {#example}

```ts twoslash
type Greeting = "Hello, world"
type ShoutyGreeting = Uppercase<Greeting>
//   ^?

type ASCIICacheKey<Str extends string> = `ID-${Uppercase<Str>}`
type MainID = ASCIICacheKey<"my_app">
//   ^?
```

### `Lowercase<StringType>`

Converte cada caractere da string para o equivalente em minúsculas.

#### Exemplo {#example-1}

```ts twoslash
type Greeting = "Hello, world"
type QuietGreeting = Lowercase<Greeting>
//   ^?

type ASCIICacheKey<Str extends string> = `id-${Lowercase<Str>}`
type MainID = ASCIICacheKey<"MY_APP">
//   ^?
```

### `Capitalize<StringType>`

Converte o primeiro caractere da string para o equivalente em maiúsculas.

#### Exemplo {#example-2}

```ts twoslash
type LowercaseGreeting = "hello, world";
type Greeting = Capitalize<LowercaseGreeting>;
//   ^?
```

### `Uncapitalize<StringType>`

Converte o primeiro caractere da string para o equivalente em minúsculas.

#### Exemplo {#example-3}

```ts twoslash
type UppercaseGreeting = "HELLO WORLD";
type UncomfortableGreeting = Uncapitalize<UppercaseGreeting>;
//   ^?
```

<details>
    <summary>Detalhes técnicos sobre os tipos intrínsecos de manipulação de strings</summary>
    <p>O código, a partir do TypeScript 4.1, dessas funções intrínsecas usa diretamente as funções de string do runtime JavaScript para a manipulação e não é sensível à localidade (locale).</p>
    <code><pre>
function applyStringMapping(symbol: Symbol, str: string) {
    switch (intrinsicTypeKinds.get(symbol.escapedName as string)) {
        case IntrinsicTypeKind.Uppercase: return str.toUpperCase();
        case IntrinsicTypeKind.Lowercase: return str.toLowerCase();
        case IntrinsicTypeKind.Capitalize: return str.charAt(0).toUpperCase() + str.slice(1);
        case IntrinsicTypeKind.Uncapitalize: return str.charAt(0).toLowerCase() + str.slice(1);
    }
    return str;
}</pre></code>
</details>
