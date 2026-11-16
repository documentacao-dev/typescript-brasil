---
title: Manual do TypeScript
layout: docs
permalink: /docs/handbook/intro.html
oneline: Seu primeiro passo para aprender TypeScript
handbook: "true"
ia-translate: true
---

## Sobre este manual {#about-this-handbook}

Mais de 20 anos depois de sua introdução na comunidade de programação, o JavaScript é hoje uma das linguagens multiplataforma mais difundidas já criadas. Começou como uma pequena linguagem de script para adicionar interatividade simples a páginas web, e cresceu até se tornar a escolha para aplicações de frontend e backend de todos os tamanhos. Enquanto o tamanho, o escopo e a complexidade dos programas escritos em JavaScript cresceram exponencialmente, a capacidade da linguagem de expressar as relações entre diferentes unidades de código não acompanhou. Somado à semântica de execução bem peculiar do JavaScript, esse descompasso entre linguagem e complexidade do programa tornou o desenvolvimento em JavaScript difícil de gerenciar em grande escala.

Os tipos de erro mais comuns cometidos por programadores podem ser descritos como erros de tipo: um certo tipo de valor foi usado onde se esperava outro tipo de valor. Isso pode acontecer por simples erros de digitação, por não entender bem a superfície da API de uma biblioteca, por suposições incorretas sobre o comportamento em tempo de execução, ou por outros motivos. O objetivo do TypeScript é ser um verificador de tipos estático para programas JavaScript — em outras palavras, uma ferramenta que roda antes de o código ser executado (estática) e garante que os tipos do programa estão corretos (verificados por tipo).

Se você está chegando ao TypeScript sem experiência com JavaScript, com a intenção de que o TypeScript seja a sua primeira linguagem, recomendamos começar lendo a documentação do [tutorial de JavaScript da Microsoft Learn](https://developer.microsoft.com/javascript/) ou o [JavaScript na documentação web da Mozilla](https://developer.mozilla.org/docs/Web/JavaScript/Guide).
Se você tem experiência em outras linguagens, deve conseguir aprender a sintaxe do JavaScript bem rápido lendo este manual.

## Como este manual está estruturado {#how-is-this-handbook-structured}

O manual é dividido em duas seções:

- **O Manual**

  O Manual do TypeScript pretende ser um documento completo que explica o TypeScript para programadores do dia a dia. Você pode ler o manual do início ao fim, seguindo a navegação à esquerda.

  Espere que cada capítulo ou página ofereça uma boa compreensão dos conceitos apresentados. O Manual do TypeScript não é uma especificação completa da linguagem, mas pretende ser um guia abrangente de todos os recursos e comportamentos da linguagem.

  Um leitor que terminar o passo a passo deve ser capaz de:

  - Ler e entender a sintaxe e os padrões do TypeScript mais usados
  - Explicar o efeito das opções importantes do compilador
  - Prever corretamente o comportamento do sistema de tipos na maioria dos casos

  Em nome da clareza e da brevidade, o conteúdo principal do Manual não vai explorar todos os casos extremos ou detalhes minuciosos dos recursos abordados. Você pode encontrar mais detalhes sobre conceitos específicos nos artigos de referência.

- **Arquivos de referência**

  A seção de referência, abaixo do manual na navegação, existe para oferecer uma compreensão mais profunda de como uma parte específica do TypeScript funciona. Você pode lê-la do início ao fim, mas cada seção se propõe a explicar em mais profundidade um único conceito, então não há a intenção de manter continuidade entre elas.

### Não são objetivos {#non-goals}

O Manual também pretende ser um documento conciso, que possa ser lido com tranquilidade em algumas horas. Alguns tópicos não serão abordados para manter o texto curto.

Em particular, o Manual não apresenta em detalhes os fundamentos básicos do JavaScript, como funções, classes e closures. Quando for apropriado, incluiremos links para leituras de apoio, para que você possa estudar esses conceitos.

O Manual também não pretende substituir uma especificação da linguagem. Em alguns casos, casos extremos ou descrições formais do comportamento serão deixados de lado em favor de explicações de alto nível e mais fáceis de entender. Para isso existem páginas de referência separadas, que descrevem de forma mais precisa e formal muitos aspectos do comportamento do TypeScript. Essas páginas não são feitas para quem não conhece o TypeScript, então podem usar terminologia avançada ou citar tópicos que você ainda não leu.

Por fim, o Manual não cobre como o TypeScript interage com outras ferramentas, exceto quando isso for necessário. Tópicos como configurar o TypeScript com webpack, rollup, parcel, react, babel, closure, lerna, rush, bazel, preact, vue, angular, svelte, jquery, yarn ou npm estão fora do escopo — você pode encontrar esses recursos em outros lugares da web.

## Começando {#get-started}

Antes de começar com [Fundamentos](/docs/handbook/2/basic-types.html), recomendamos ler uma das páginas introdutórias a seguir. Essas introduções destacam as principais semelhanças e diferenças entre o TypeScript e a linguagem que você prefere, e esclarecem equívocos comuns específicos dessas linguagens.

- [TypeScript para quem está começando a programar](/docs/handbook/typescript-from-scratch.html)
- [TypeScript para programadores JavaScript](/docs/handbook/typescript-in-5-minutes.html)
- [TypeScript para programadores Java/C#](/docs/handbook/typescript-in-5-minutes-oop.html)
- [TypeScript para programadores funcionais](/docs/handbook/typescript-in-5-minutes-func.html)

Caso contrário, vá direto para [Fundamentos](/docs/handbook/2/basic-types.html).
