# NLP com spaCy + Streamlit

Aplicação web feita em **Python** com **Streamlit** e **spaCy** para analisar textos em português de forma visual. O app mostra a estrutura gramatical das frases, as entidades encontradas (pessoas, organizações, lugares) e a similaridade entre palavras, além de permitir comparar os modelos pequeno, médio e grande do spaCy.

## O que é NLP e o que é o spaCy

- **NLP** (*Natural Language Processing*, ou Processamento de Linguagem Natural) é a área que ensina o computador a entender texto escrito por pessoas.
- **spaCy** é uma das bibliotecas de NLP mais usadas em Python. É rápida, roda localmente (sem custo por uso) e tem modelos prontos em português.
- **spacy-streamlit** é um complemento que monta, com uma linha de código, uma página interativa para explorar o que o spaCy faz com um texto.

## Funcionalidades

- Escolha entre os modelos `pt_core_news_sm`, `pt_core_news_md` e `pt_core_news_lg`
- Caixa de texto para digitar qualquer frase
- **Dependency Parse & Part-of-speech**: setas mostrando como as palavras se ligam e a classe gramatical de cada uma
- **Named Entities (NER)**: entidades destacadas no texto e listadas numa tabela com rótulo e posição
- **Vectors & Similarity**: o quanto duas palavras ou textos são parecidos
- **Token attributes**: tabela com os detalhes de cada palavra (lema, classe, dependência...)
- **Pipeline info**: componentes e versão do modelo em uso

## Código

```python
import streamlit as st
import spacy_streamlit

# Compatibilidade: o spacy-streamlit (até a versão 1.0.6) ainda usa
# st.experimental_rerun, que foi removido do Streamlit. Este apelido resolve.
if not hasattr(st, "experimental_rerun"):
    st.experimental_rerun = st.rerun

modelos = ["pt_core_news_sm", "pt_core_news_md", "pt_core_news_lg"]
texto_padrao = "Claro tem números abaixo da operadora Vivo"

spacy_streamlit.visualize(modelos, texto_padrao)
```

## Como executar

```bash
# criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

# instalar as bibliotecas
pip install streamlit spacy spacy-streamlit

# baixar os modelos de português (o lg tem centenas de MB)
python -m spacy download pt_core_news_sm
python -m spacy download pt_core_news_md
python -m spacy download pt_core_news_lg

# rodar o app
streamlit run app.py
```

> Para começar com pouco espaço em disco ou internet lenta, baixe só o `sm` e deixe `modelos = ["pt_core_news_sm"]`.

## Problemas conhecidos

| Erro | Causa | Solução |
|---|---|---|
| `module 'streamlit' has no attribute 'experimental_rerun'` | o `spacy-streamlit` usa um comando removido do Streamlit | o apelido no início do código; ou `visualize(..., color=None)` |
| `Can't find model 'pt_core_news_md'` | o modelo não foi baixado | `python -m spacy download pt_core_news_md` |
| erro ao instalar o spaCy | Python muito novo, ainda sem suporte | usar uma versão do Python suportada pelo spaCy |

---

## Guia de referência

### Os três modelos

| Modelo | Tamanho | Vetores de palavras | Quando usar |
|---|---|---|---|
| `sm` (*small*) | pequeno | **não tem** vetores reais | testes e protótipos, máquinas modestas |
| `md` (*medium*) | médio | sim, reduzidos | bom equilíbrio entre qualidade e tamanho |
| `lg` (*large*) | grande | sim, completos | quando a qualidade importa mais que o tamanho |

> A **similaridade** só é confiável no `md` e no `lg`. No `sm`, o spaCy faz uma aproximação e costuma dar resultados estranhos.

### Rótulos de entidades (modelos em português)

| Rótulo | Significado | Exemplo |
|---|---|---|
| `PER` | pessoa | Machado de Assis |
| `ORG` | organização | Vivo, Petrobras |
| `LOC` | local | São Paulo, Brasil |
| `MISC` | outros (eventos, obras, produtos...) | Copa do Mundo |

> Os modelos em português **não reconhecem datas e valores** (`DATE`, `MONEY`) como os de inglês. Para isso é preciso usar regras próprias ou regex.

### Classes gramaticais (POS) mais comuns

| Tag | Classe | Tag | Classe |
|---|---|---|---|
| `NOUN` | substantivo | `ADJ` | adjetivo |
| `PROPN` | nome próprio | `ADV` | advérbio |
| `VERB` | verbo | `ADP` | preposição |
| `AUX` | verbo auxiliar | `DET` | artigo/determinante |
| `PRON` | pronome | `NUM` | número |

> Dica: `spacy.explain("ADV")` explica qualquer rótulo direto no Python.

---

## Observação importante: marcas que são palavras comuns

No texto de teste, mesmo o **modelo grande** classificou:

- **"Vivo" → ORG** ✅
- **"Claro" → LOC** e **ADV (advérbio)** ❌

Marcas que também são palavras do dia a dia (**Claro**, **Oi**, **Vivo**, **Natura**...) são o caso mais difícil para os modelos prontos. O **contexto** ajuda: frases como *"A operadora Claro..."* ou *"A Claro anunciou..."* costumam ser reconhecidas melhor.

---

## O que vale saber além da aula

### 1. Usar o spaCy direto no código (sem a tela)

```python
import spacy

nlp = spacy.load("pt_core_news_lg")
doc = nlp("A Claro anunciou um novo plano em São Paulo.")

for ent in doc.ents:
    print(ent.text, ent.label_)            # entidades

for token in doc:
    print(token.text, token.lemma_, token.pos_)   # palavra, forma básica, classe
```

### 2. Ensinar nomes próprios com o `EntityRuler`

Dá para criar **regras** que garantem que certos termos sejam reconhecidos como organização, sem treinar o modelo:

```python
import spacy

nlp = spacy.load("pt_core_news_lg")
ruler = nlp.add_pipe("entity_ruler", before="ner")
ruler.add_patterns([
    {"label": "ORG", "pattern": "Claro"},
    {"label": "ORG", "pattern": "Vivo"},
    {"label": "ORG", "pattern": [{"LOWER": "claro"}, {"LOWER": "brasil"}]},
])

doc = nlp("Claro tem números abaixo da operadora Vivo")
print([(ent.text, ent.label_) for ent in doc.ents])
```

> Cuidado: a regra `"Claro"` com maiúscula também vai marcar *"Claro que vamos!"* no início de frase. Padrões com contexto (ex.: `"a Claro"`, `"operadora Claro"`) são mais seguros.

### 3. Lematização: buscar pela forma básica

O lema transforma *"comprou"*, *"comprando"* e *"comprarão"* em **"comprar"**. Útil para buscar termos sem se preocupar com conjugação, plural ou gênero.

### 4. Processar muitos textos de uma vez: `nlp.pipe`

```python
textos = ["primeira notícia...", "segunda notícia...", "terceira notícia..."]
for doc in nlp.pipe(textos, batch_size=50):
    print([(ent.text, ent.label_) for ent in doc.ents])
```

É **bem mais rápido** que chamar `nlp(texto)` num loop, porque processa em lotes.

### 5. Desligar o que não vai usar

Se só precisa das entidades, desligar o resto deixa tudo mais rápido:

```python
nlp = spacy.load("pt_core_news_lg", disable=["parser", "lemmatizer"])
```

### 6. Carregar o modelo uma vez só no Streamlit

O Streamlit roda o script a cada clique. Para não recarregar o modelo (que é pesado) toda hora:

```python
@st.cache_resource
def carregar_modelo(nome):
    return spacy.load(nome)

nlp = carregar_modelo("pt_core_news_lg")
```

> `@st.cache_resource` é para objetos pesados que não mudam (modelos, conexões); `@st.cache_data` é para dados (tabelas, resultados).

### 7. O que o spaCy **não** faz sozinho em português

- **Sentimento** (positivo/negativo): não vem pronto. A seção *Text Classification* do app fica vazia por isso. Opções: treinar um classificador, usar um modelo do Hugging Face ou uma IA via API.
- **Resumo** de textos: também não. Isso é tarefa para modelos de IA generativa.

### 8. Quando usar spaCy e quando usar IA

| | spaCy | IA (LLMs) |
|---|---|---|
| Custo | grátis, roda local | pago por uso ou servidor caro |
| Velocidade | muito rápido (milhares de textos por segundo) | mais lento |
| Bom em | gramática, entidades, pré-filtrar grandes volumes | contexto amplo, ironia, sentimento, resumo |

Uma estratégia comum é usar os dois em camadas: **regras/regex → spaCy → IA só nos casos difíceis**.

---

## Tecnologias

- Python 3
- Streamlit
- spaCy 3
- spacy-streamlit
- Modelos `pt_core_news_sm`, `pt_core_news_md`, `pt_core_news_lg`