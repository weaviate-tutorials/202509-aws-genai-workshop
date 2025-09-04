<!-- image -->

## Chapter Highlights

- 1.  AI  masters  new  benchmarks  faster  than  ever. In  2023,  AI  researchers  introduced  several  challenging  new benchmarks, including MMMU, GPQA, and SWE-bench, aimed at testing the limits of increasingly capable AI systems. By 2024, AI performance on these benchmarks saw remarkable improvements, with gains of 18.8 and 48.9 percentage points on MMMU and GPQA, respectively. On SWE-bench, AI systems could solve just 4.4% of coding problems in 2023-a fi gure that jumped to 71.7% in 2024.
- 2. Open-weight models catch up. Last year's AI Index revealed that leading open-weight models lagged signi fi cantly behind their closed-weight counterparts. By 2024, this gap had nearly disappeared. In early January 2024, the leading closedweight model outperformed the top open-weight model by 8.04% on the Chatbot Arena Leaderboard. By February 2025, this gap had narrowed to 1.70%.
- 3. The gap between Chinese and US models closes. In 2023, leading American models signi fi cantly outperformed their Chinese counterparts-a trend that no longer holds. At the end of 2023, performance gaps on benchmarks such as MMLU, MMMU, MATH, and HumanEval were 17.5, 13.5, 24.3, and 31.6 percentage points, respectively. By the end of 2024, these di ff erences had narrowed substantially to just 0.3, 8.1, 1.6, and 3.7 percentage points.
- 4. AI model performance converges at the frontier. According to last year's AI Index, the Elo score di ff erence between the top and 10th-ranked model on the Chatbot Arena Leaderboard was 11.9%. By early 2025, this gap had narrowed to just 5.4%. Likewise, the di ff erence between the top two models shrank from 4.9% in 2023 to just 0.7% in 2024. The AI landscape is becoming increasingly competitive, with high-quality models now available from a growing number of developers.
- 5. New reasoning paradigms like test-time compute improve model performance. In 2024, OpenAI introduced models like o1 and o3 that are designed to iteratively reason through their outputs. This test-time compute approach dramatically improved performance, with o1 scoring 74.4% on an International Mathematical Olympiad qualifying exam, compared to GPT4o's 9.3%. However, this enhanced reasoning comes at a cost: o1 is nearly six times more expensive and 30 times slower than GPT-4o.

<!-- image -->

<!-- image -->

## Chapter Highlights (cont'd)

- 6. More challenging benchmarks are continually proposed. The saturation of traditional AI benchmarks like MMLU, GSM8K, and HumanEval, coupled with improved performance on newer, more challenging benchmarks such as MMMU and GPQA, has pushed researchers to explore additional evaluation methods for leading AI systems. Notable among these are Humanity's Last Exam, a rigorous academic test where the top system scores just 8.80%; FrontierMath, a complex mathematics benchmark where AI systems solve only 2% of problems; and BigCodeBench, a coding benchmark where AI systems achieve a 35.5% success rate-well below the human standard of 97%.

7. High-quality AI video generators demonstrate signi fi cant improvement. In 2024, several advanced AI models capable of generating high-quality videos from text inputs were launched. Notable releases include OpenAI's SORA, Stable Video 3D and 4D, Meta's Movie Gen, and Google DeepMind's Veo 2. These models produce videos of signi fi cantly higher quality compared to those from 2023.

- 8. Smaller models drive stronger performance. In 2022, the smallest model registering a score higher than 60% on MMLU was PaLM, with 540 billion parameters. By 2024, Microsoft's Phi-3-mini, with just 3.8 billion parameters, achieved the same threshold. This represents a 142-fold reduction in over two years.
- 9.  Complex  reasoning  remains  a  problem. Even  though  the  addition  of  mechanisms  such  as  chain-of-thought reasoning has signi fi cantly improved the performance of LLMs, these systems still cannot reliably solve problems for which provably correct solutions can be found using logical reasoning, such as arithmetic and planning, especially on instances larger than those they were trained on. This has a signi fi cant impact on the trustworthiness of these systems and their suitability in high-risk applications.
- 10. AI agents show early promise. The launch of RE-Bench in 2024 introduced a rigorous benchmark for evaluating complex tasks for AI agents. In short time-horizon settings (two-hour budget), top AI systems score four times higher than human experts, but as the time budget increases, human performance surpasses AI-outscoring it two to one at 32 hours. AI agents already match human expertise in select tasks, such as writing Triton kernels, while delivering results faster and at lower costs.

<!-- image -->

## Chapter 2: Technical Performance

## RAG: Retrieval Augment Generation (RAG)

An  increasingly  common  capability  being  tested  in  LLMs is retrieval-augmented generation (RAG). This approach integrates LLMs  with retrieval mechanisms  to enhance their  response  generation. The  model fi rst  retrieves  relevant information  from fi les  or  documents  and  then  generates  a response tailored to the user's query based on the retrieved content.  RAG  has  diverse  use  cases,  including  answering precise questions from large databases and addressing customer queries using information from company documents.

models. 2024 also saw the release of numerous benchmarks for  evaluating  RAG  systems,  including  Ragnarok  (a  RAG arena battleground) and CRAG (Comprehensive RAG benchmark). Additionally, specialized RAG benchmarks, such as FinanceBench for fi nancial question answering, have been developed to address speci fi c use cases.

## Berkeley Function Calling Leaderboard

In recent years, RAG has received increasing attention from researchers  and  companies.  For  example,  in  September 2024, Anthropic introduced Contextual Retrieval, a method that signi fi cantly enhances the retrieval capabilities of RAG

The  Berkeley  Function  Calling  Leaderboard  evaluates  the ability  of  LLMs  to  accurately  call  functions  or  tools.  The evaluation suite includes over 2,000  question-functionanswer pairs across multiple programming languages (such as  Python,  Java,  JavaScript,  and  REST  API)  and  spans  a variety of testing domains (Figure 2.2.17).

## Data composition on the Berkeley Function Calling Leaderboard

Source: Yan et al., 2024

## Berkeley Function-Calling Leaderboard Evaluation Data Composition

<!-- image -->

Figure 2.2.17 9

| Javascript (AST)          | Chatting Capability             |
|---------------------------|---------------------------------|
| 2.5%                      | 10.0%                           |
| SQL (AST) 5.0%            | Simple (Exec)                   |
| Java (AST)                | 5.0% Multiple (Exec)            |
| 5.0% REST (Exec)          | 2.5% Parallel (Exec)            |
| Relevance 12.0%           | 2.5% Parallel & Multiple (Exec) |
| Parallel & Multiple (AST) | Simple (AST) 20.0%              |
|                           | 2.0%                            |
| 10.0%                     |                                 |
| Parallel (AST)            | Multiple (AST)                  |
| 10.0%                     | 10.0%                           |

9 In this context: AST (abstract syntax tree) refers to tasks that involve analyzing or manipulating code at the structural level, using its parsed representation as a tree of syntactic elements. Evaluations labeled with 'AST' likely test an AI model's ability to understand, generate, or manipulate code in a structured manner. Exec (execution-based) indicates tasks that require actual execution of function calls to verify correctness. Evaluations labeled with 'Exec' likely assess whether the AI model can correctly call and execute functions, ensuring the expected outputs are produced.

<!-- image -->

## Chapter 2: Technical Performance

2.2 Language

The top model on the Berkeley Function Calling Leaderboard is  watt-tool-70b,  a fi ne-tuned  variant  of  Llama-3.3-70BInstruct designed speci fi cally for function calling. It achieved an overall accuracy of 74.31 (Figure 2.2.18). The next-highestscoring  model  was  a  November variant  of  GPT-4o,  with  a score of 72.08. Performance on this benchmark has improved signi fi cantly over the course of 2024, with top models at the end of the year achieving accuracies up to 50 points higher than those recorded early in the year.

## Berkeley Function-Calling: overall accuracy

Model

<!-- image -->

Figure 2.2.18

<!-- image -->

## Chapter 2: Technical Performance

2.2 Language

## MTEB: Massive Text Embedding Benchmark

The  Massive Text  Embedding  Benchmark  (MTEB),  created by a team at Hugging Face and Cohere, was introduced in late 2022 to comprehensively evaluate how models perform on various embedding tasks. Embedding involves converting data,  such  as  words,  texts,  or  documents,  into  numerical vectors that capture rough semantic meanings and distance between vectors. Embedding is an essential component of RAG. During a RAG task, when users input a query, the model

## Tasks in the MTEB benchmark

Source: Muennigho ff et al., 2023

<!-- image -->

Figure 2.2.19

<!-- image -->

transforms it into an embedding vector. This transformation enables the  model to then  search for  relevant  information. MTEB  includes  58  datasets  spanning  112  languages  and eight embedding tasks (Figure 2.2.19). 10  For example, in the bitext mining task, there are two sets of sentences from two di ff erent languages, and for every sentence in the fi rst  set, the model is tasked to fi nd the best match in the second set.

## Chapter 2: Technical Performance

## 2.2 Language

As of early 2025, the top-performing embedding model on the MTEB benchmark was Voyage AI's voyage-3-m-exp, with a score of 74.03. Voyage AI is focused on creating high-quality AI embedding models. The voyage-3-m-exp model is a variant of the voyage-3-large, a large foundation model speci fi cally designed  for  embedding  tasks,  and  it  uses  strategies  like Matryoshka Representation Learning and quantization-aware training  to  improve  its  performance.  The  voyage-3-m-exp model narrowly outperformed NV-Embed-v2 (72.31), which held  the  top  spot  for  most  of  2024  (Figure  2.2.20).  When the MTEB benchmark was fi rst introduced in late 2022, the leading model achieved an average score of 59.5. Over the past  two  years,  therefore,  performance  on  the  benchmark has meaningfully improved.

<!-- image -->

Figure 2.2.20

<!-- image -->