---
title: Criando tipos a partir de tipos
layout: docs
permalink: /docs/handbook/2/types-from-types.html
oneline: "Uma visão geral das formas de criar novos tipos a partir de tipos existentes."
ia-translate: true
---

O sistema de tipos do TypeScript é muito poderoso porque permite expressar tipos _em termos de outros tipos_.

A forma mais simples dessa ideia são os genéricos. Além disso, temos uma grande variedade de _operadores de tipo_ disponíveis.
Também é possível expressar tipos em termos de _valores_ que já temos.

Combinando diversos operadores de tipo, podemos expressar operações e valores complexos de forma sucinta e fácil de manter.
Nesta seção veremos como expressar um novo tipo em termos de um tipo ou valor existente.

- [Genéricos](/docs/handbook/2/generics.html) - Tipos que recebem parâmetros
- [Operador de tipo Keyof](/docs/handbook/2/keyof-types.html) - Usando o operador `keyof` para criar novos tipos
- [Operador de tipo Typeof](/docs/handbook/2/typeof-types.html) - Usando o operador `typeof` para criar novos tipos
- [Tipos de acesso indexado](/docs/handbook/2/indexed-access-types.html) - Usando a sintaxe `Type['a']` para acessar um subconjunto de um tipo
- [Tipos condicionais](/docs/handbook/2/conditional-types.html) - Tipos que se comportam como instruções if no sistema de tipos
- [Tipos mapeados](/docs/handbook/2/mapped-types.html) - Criando tipos ao mapear cada propriedade de um tipo existente
- [Tipos de template literal](/docs/handbook/2/template-literal-types.html) - Tipos mapeados que alteram propriedades por meio de strings template literal
