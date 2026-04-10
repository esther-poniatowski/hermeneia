# Prose Metrics

This page catalogs common prose metrics used to support readability diagnosis.
These metrics are **proxies** for style, density, and processing burden; they do not directly measure conceptual difficulty or discourse quality.
Use them alongside rule findings from [Rule Registry](rule-registry.md), not as standalone verdicts.

---

## Classification of Metrics

Metrics are grouped into four families:

**Surface-count metrics**:

These are easy to compute and robust:

* words per sentence
* sentences per paragraph
* passive-voice rate
* pronoun density
* verb density
* clauses per sentence
* nominalization density

**Formula-based readability indices**:

These compress several surface features into one scalar:

* Flesch Reading Ease
* Flesch-Kincaid Grade Level
* Gunning-Fog
* SMOG
* Coleman-Liau
* ARI
* Dale-Chall

**Linguistically richer metrics**:

These require parsing, lexicons, or corpus resources:

* mean dependency length
* parse depth
* subordination ratio
* lexical frequency
* concreteness
* age of acquisition
* discourse overlap

**Model-based metrics**:

These rely on statistical or neural models:

* perplexity
* supervised readability classifiers

The rest of this page moves from lower-cost metrics (simple counts) to higher-cost metrics (parser-based and model-based methods).

---

## Pure structural counts

### Sentences per paragraph

**What it diagnoses**::

This is a proxy for **visual and rhetorical chunking**.

A high value often indicates:

* denser blocks of text
* weaker segmentation of ideas
* greater local memory load during reading

A low value often indicates:

* more frequent structural breaks
* clearer thematic progression
* easier visual scanning

This measure does **not** directly assess syntactic difficulty. It primarily diagnoses the **macro-organization of discourse**.

**Formula**::

$$
\text{sentences per paragraph}=\frac{\text{#Sentences}}{\text{#Paragraphs}}
$$

---

### Words per sentence

**What it diagnoses**::

This is a classic proxy for **syntactic load**.

Longer sentences tend, on average, to involve:

* more clauses
* more embeddings
* more coordination or subordination
* longer dependency spans

Thus, this measure approximates the **difficulty of parsing sentence structure**. It is only a proxy: a long sentence can remain clear, and a short sentence can still be conceptually difficult.

**Formula**::

$$
\text{words per sentence}=\frac{\text{#Words}}{\text{#Sentences}}
$$

---

### Verb density

**What it diagnoses**::

Verb density approximates the degree of **predicative activity** in the text. It may reflect:

* how propositionally packed the text is
* whether the prose is action/process oriented
* whether clauses are frequent relative to text length

A higher verb density often suggests more events, assertions, or clause structure per unit of text.
A lower verb density may suggest more nominal style, descriptive accumulation, or abstract noun-heavy prose.

This is therefore a proxy for the contrast between **verbal/clausal style** and **nominal style**.

**Formula**::

The standard word-based version is:

$$
\text{verb density}_{\text{word-based}}=\frac{\text{#Verbs}}{\text{#Words}}
$$

A sentence-based normalization also exists:

$$
\text{verb density}_{\text{sentence-based}}=\frac{\text{#Verbs}}{\text{#Sentences}}
$$

---

### Pronoun density

**What it diagnoses**::

Pronoun density is a proxy for **referential style** and **cohesion management**. It helps detect whether the text relies heavily on:

* anaphora
* discourse tracking across clauses
* interpersonal or narrative orientation

A high pronoun density may indicate:

* conversational or narrative prose
* repeated reference to participants
* stronger dependence on context for interpretation

A low pronoun density may indicate:

* more explicit noun repetition
* more technical, expository, or impersonal prose
* greater lexical explicitness

Thus, this measure diagnoses the balance between **context-dependent reference** and **lexically explicit reference**.

**Formula**::

$$
\text{pronoun density}=\frac{\text{#Pronouns}}{\text{#Words}}
$$

---

### Passive-voice rate

**What it diagnoses**::

This measure diagnoses the extent to which the text suppresses or backgrounds the agent and foregrounds the patient or result. A higher passive rate often correlates with:

* more impersonal style
* greater institutional or academic formality
* weaker agent salience
* potentially heavier clause structure

Passive voice does **not** automatically imply poor readability. In some genres it is functionally appropriate. But frequent passive constructions can increase processing cost by making thematic roles less direct.

**Formula**::

$$
\text{passive-voice rate}=\frac{\text{#Passive clauses}}{\text{#Clauses}}
$$

In practice, the exact denominator varies across implementations:

* all clauses
* all finite verbs
* all sentences

---

## Composite readability indices

### Flesch-Kincaid Grade Level & Flesch Reading Ease

**What it diagnoses**::

This metric estimates the **school grade level** required to understand the text. It combines two intuitions:

* longer sentences increase syntactic difficulty
* longer words, approximated by syllable count, increase lexical difficulty

Thus, it diagnoses a combination of **syntactic length** and **lexical complexity**.

**Formula**::

The formula for Flesch-Kincaid Grade Level (FKGL) is:
$$
\text{FKGL}=0.39\frac{\text{#Words}}{\text{#Sentences}}+11.8\frac{\text{#Syllables}}{\text{#Words}}-15.59
$$

Interpretation: a value around 8 corresponds roughly to eighth-grade readability, a value around 12 to late secondary-school level, and so on.

The Flesch Reading Ease (FRE) score is a related metric that also combines sentence length and
syllable count. However, the output scale is inverted: **higher scores mean easier text**.

**Formula**::

$$
\text{FRE}=206.835-1.015\frac{\text{#Words}}{\text{#Sentences}}-84.6\frac{\text{#Syllables}}{\text{#Words}}
$$

Typical interpretation:

* high score: easy prose
* mid-range score: moderately difficult prose
* low score: dense or technical prose

---

### Gunning-Fog index

**What it diagnoses**::

The Gunning-Fog index estimates the years of formal education needed to understand the text on first reading. It is designed to capture:

* sentence-level complexity
* prevalence of complex words

Here, "complex words" usually means words with **three or more syllables**, with standard exclusions depending on implementation.

Thus, it diagnoses the joint contribution of:

* long sentences
* polysyllabic vocabulary

**Formula**::

$$
\text{Gunning-Fog index}=0.4\left(\frac{\text{#Words}}{\text{#Sentences}}+100\frac{\text{#Complex Words}}{\text{#Words}}\right)
$$

The first term measures average sentence length.
The second term measures the percentage of complex words.

---

### SMOG

**What it diagnoses**:

SMOG estimates the education level required to understand a text. It emphasizes **polysyllabic vocabulary** more strongly than Flesch-type scores, and is often used for health or public-information writing.

**Formula**:

$$
\text{SMOG}=1.0430\sqrt{\text{#Words with 3+ syllables}\times\frac{30}{\text{#Sentences}}}+3.1291
$$

---

### Coleman-Liau Index

**What it diagnoses**:

This index approximates readability from **characters per word** and **sentences per word**, rather than syllables. It is therefore easier to compute automatically.

**Formula**:

$$
\text{CLI}=0.0588\left(100\frac{\text{#Letters}}{\text{#Words}}\right)-0.296\left(100\frac{\text{#Sentences}}{\text{#Words}}\right)-15.8
$$

---

### Automated Readability Index

**What it diagnoses**:

This metric estimates grade level from **word length in characters** and **sentence length**.

**Formula**:

$$
\text{ARI}=4.71\frac{\text{#Characters}}{\text{#Words}}+0.5\frac{\text{#Words}}{\text{#Sentences}}-21.43
$$

---

### Dale-Chall Readability Formula

**What it diagnoses**:

This metric tries to capture lexical difficulty more linguistically than syllable-based metrics. It uses the proportion of words that are **not** in a list of common familiar words.

**Formula**:

$$
\text{Raw Dale-Chall}=0.1579\left(100\frac{\text{#Difficult Words}}{\text{#Words}}\right)+0.0496\frac{\text{#Words}}{\text{#Sentences}}
$$

If the percentage of difficult words exceeds 5%, an adjustment is added:

$$
\text{Dale-Chall}=\text{Raw Dale-Chall}+3.6365
$$

---

### Linsear Write Formula

**What it diagnoses**:

This was designed for technical manuals. It distinguishes between "easy" and "hard" words, usually by syllable count.

**Procedure**:

* Select a 100-word sample
* Count easy words and hard words
* Compute a weighted score
* Normalize by sentence count

A common operational form is:

$$
\text{Score}=\frac{\text{#Easy Words}+3\,\text{#Hard Words}}{\text{#Sentences}}
$$

* if Score $>20$, divide by 2
* otherwise subtract 2, then divide by 2

Because implementations vary, this metric is less standardized than Flesch or SMOG.

---

## Lexical difficulty metrics

These do not always aim at a global readability score. They isolate **vocabulary-related burden**.

### Type-token ratio and lexical diversity

**What it diagnoses**:

This family measures lexical variety. A text with many distinct words may impose a greater lexical tracking burden.

**Formula**:

$$
\text{TTR}=\frac{\text{#Distinct Word Types}}{\text{#Word Tokens}}
$$

**Limitation**:

TTR is strongly length-dependent. For that reason, more stable variants are often preferred.

---

### MTLD

**What it diagnoses**:

MTLD measures lexical diversity while reducing sensitivity to text length.

It does not have a single short closed-form ratio like TTR. It is computed procedurally by tracking how many words are processed before TTR falls below a threshold, then averaging segment lengths.

This is often more reliable than raw TTR.

---

### HD-D

**What it diagnoses**:

This is another lexical diversity metric, based on a hypergeometric model. It estimates the probability that sampled words are of distinct types.

It is statistically more stable than simple TTR.

---

### Average word frequency

**What it diagnoses**:

This estimates how common the vocabulary is in a reference corpus. Rare words usually increase lexical difficulty.

A common measure is the mean log-frequency of content words in a corpus such as SUBTLEX, COCA, or other frequency databases.

No universal single formula exists, because the result depends on the corpus and normalization scheme.

---

### Percentage of rare words

**What it diagnoses**:

This is a simpler version of lexical frequency analysis. It measures how much of the text lies below a chosen familiarity threshold.

**Formula**:

$$
\text{rare-word rate}=\frac{\text{#Rare Words}}{\text{#Words}}
$$

---

## Syntactic complexity metrics

These target structure more directly than average sentence length.

### Clauses per sentence

**What it diagnoses**:

This approximates the degree of clausal embedding and structural complexity.

**Formula**:

$$
\text{clauses per sentence}=\frac{\text{#Clauses}}{\text{#Sentences}}
$$

---

### Mean dependency length

**What it diagnoses**:

This measures the average distance between syntactically linked words in a dependency parse. Longer dependencies often increase processing cost.

**Formula**:

$$
\text{MDL}=\frac{\sum(\text{head-dependent distances across dependency relations})}{\text{#Dependency relations}}
$$

This is more linguistically meaningful than raw sentence length, but requires syntactic parsing.

---

### Parse tree depth

**What it diagnoses**:

This estimates how deeply nested the syntactic structure is. Greater depth often correlates with more embedding and harder incremental parsing.

There is no unique universal formula beyond computing the depth of the sentence parse tree and averaging over sentences.

---

### Subordination ratio

**What it diagnoses**:

This measures the proportion of subordinate clauses relative to all clauses or to main clauses. It approximates hypotactic complexity.

**Formula**:

$$
\text{subordination ratio}=\frac{\text{#Subordinate clauses}}{\text{#Clauses}}
$$

---

### Nominalization density

**What it diagnoses**:

This estimates how strongly the text compresses processes into nouns rather than expressing them through verbs. Heavy nominalization is common in technical prose and often reduces immediate readability.

**Formula**:

$$
\text{nominalization density}=\frac{\text{#Nominalizations}}{\text{#Words}}
$$

---

## Cohesion and discourse metrics

These target difficulty at the discourse level rather than sentence level.

### Connective density

**What it diagnoses**:

This measures the frequency of discourse connectives such as *however*, *therefore*, *because*, *although*. It gives information about how explicitly logical relations are marked.

**Formula**:

$$
\text{connective density}=\frac{\text{#Connectives}}{\text{#Words}}
$$

High density may improve coherence if connectives are informative, but may also reflect dense argumentative structure.

---

### Referential overlap

**What it diagnoses**:

This measures how much content is linked across adjacent sentences by repeated nouns or semantically related terms. It approximates discourse cohesion.

There is no single universal formula; implementations differ. A simple version computes overlap between the content-word sets of neighboring sentences.

---

### Entity-grid coherence measures

**What they diagnose**:

These track how discourse entities persist and change grammatical role across sentences. The goal is to estimate coherence from patterns of topic continuity.

These are not simple hand formulas. They are procedural discourse models.

---

## Semantic and conceptual difficulty metrics

These attempt to address what classical readability formulas largely ignore.

### Concreteness

**What it diagnoses**:

Concrete words are usually easier to process than abstract words. A text with many abstract terms may be harder independently of sentence length.

A typical score is the average concreteness rating of words from psycholinguistic norms.

No single universal formula exists beyond averaging lexical ratings.

---

### Age of acquisition

**What it diagnoses**:

Words learned later in life are often harder to process. Mean age-of-acquisition can approximate lexical accessibility.

Again, this is generally computed by averaging norm-based ratings.

---

### Semantic density or information density

**What it diagnoses**:

This aims to capture how much information is packed into each unit of text. There are many versions:

* surprisal-based
* embedding-based
* proposition-count based

No single standard closed form exists across methods.

---

## Modern NLP-based readability metrics

These go beyond hand-crafted formulas.

### Language-model perplexity

**What it diagnoses**:

Perplexity measures how predictable the text is under a language model. Less predictable text can be harder to process, though predictability and readability are not identical.

**Formula**:

If a sequence has tokens $w_1,\dots,w_n$, then

$$
\text{Perplexity}=\exp\left(-\frac{1}{n}\sum_{i=1}^n\log p(w_i\mid w_{<i})\right)
$$

This is model-dependent.

---

### Supervised readability prediction

**What it diagnoses**:

A model is trained on texts labeled by grade level or difficulty. Features may include syntax, frequency, cohesion, discourse markers, morphology, or embeddings.

This does not have a single explicit closed formula, because the model may be a regression, SVM, random forest, or neural network.

---

## Methodological notes on metric use

No single metric captures readability in full. Different metrics diagnose different burdens:

* **visual burden**: paragraph length
* **syntactic burden**: sentence length, clause structure, dependency length
* **lexical burden**: syllables, rare words, frequency, age of acquisition
* **discourse burden**: cohesion, referential tracking, connective structure
* **conceptual burden**: abstraction, information density
* **predictive burden**: perplexity or model-based difficulty

For rigorous prose analysis, a better practice is usually to assemble a **profile of complementary metrics** rather than rely on a single scalar score.

A structured table grouping these metrics by linguistic level can be provided if needed.

---

## Integration in the Guide Workflow

Use metrics in this order:

1. Run lint and review rule findings in [Usage](usage.md).
2. Use selected metrics to prioritize dense or high-friction passages.
3. Apply policy thresholds and weighting decisions in [Configuration](configuration.md).
4. Keep final verdict decisions aligned with [Prose Audit Protocol](prose-audit-protocol.md).

This sequence keeps metrics in a supporting role instead of letting one scalar index override structural and argumentative diagnostics.

---

## Limitation

All of these are **surface proxies**.

For example, a mathematically rigorous paragraph can be short, active, and low in syllable count while still being difficult because the concepts are highly abstract. Conversely, a long sentence can remain easy if its internal structure is strongly guided and semantically transparent.
