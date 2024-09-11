# Let's see the current and the future of the Linux with LLM Agent

Imagine if you can ask every kernel developer to do a completed survey/questionare about a commit/a mail, what can you find with the results?

Workflow/Method: 

```
[Human Experts (LLM) design survey] -> [LLM Agent complete survey] -> [Human Experts (LLM) evaluate survey results samples] -> [Human Experts (LLM) give the report]
```

You can define LLM Agent for each step, but it will be better to work with Human Experts to get better results in 2024.


Let's take eBPF as an example, the same tool can be directly applied to other subsystems.

## Datasets with eBPF: Linux BPF subsystem

- 680+ eBPF expert seleted Important feature commits information, with feature name, type(Map, helper, kfunc, prog, attach, etc...)
- bpf related feature commits information, with LLM Agent survey and summary
- 120000+ All bpf subsystem related mails, with LLM Agent survey
- vector index for all of them

All the datasets are automatically updated by CI! The interative analysis is on the way to deployment...

The result can be found in [report_ebpf.md](report_ebpf.md).

## why llm?

- Researcher has proved that LLM can acheive similar level as human when doing summary/survey/questionare task in Market, Chemistry... Such system is also deployed and explored in production for... (See the citation)
- why not other methods?
  - domain knowledge (cite)
  - unstructured data（cite）
  - human expert is too expensive and impossible for such task
 
What question can llm help answer but other cannot?

- bug...

## How to define a LLM Agent for analysis

- Task:
- Tool:
- The input survey define: 3 types of questions
    - Answer: yes or no
    - The tag: choose between something: uprobe/kprobe/xdp...
    - The summary: should be complete in one or 2 sentence.
- Memory: which database can it access?
- Planer(Predefined)

## Config

```yml

```


## reference

1. domain knowledge
   1. [Knowledge solver: Teaching llms to search for domain knowledge from knowledge graphs](https://proceedings.neurips.cc/paper_files/paper/2023/hash/1190733f217404edc8a7f4e15a57f301-Abstract-Datasets_and_Benchmarks.html)
   2. [Openagi: When llm meets domain experts](https://arxiv.org/abs/2309.03118)
2. unstructured data
   1. [Embedding-based Retrieval with LLM for Effective Agriculture Information Extracting from Unstructured Data](https://arxiv.org/abs/2308.03107)
3. kernel mail
   1. [How to Communicate when Submitting Patches: An Empirical Study of the Linux Kernel](https://dl.acm.org/doi/abs/10.1145/3359210?casa_token=5CrG9X-8QNgAAAAA:mm-N0p2baZSzxgfNbBcSi5HYBF67jdM7VZlJfTbhI2ht2cv1oCHRSL_FRPmM7DHr6ISpV91szCTOEg)
   2. [Differentiating Communication Styles of Leaders on the Linux Kernel Mailing List](https://dl.acm.org/doi/abs/10.1145/2957792.2957801?casa_token=VMchS_jhea0AAAAA:EubJDL_ftM5jmV3_yzwWzDLvLq8hAsexZnss1x3j754OZr4VNENST_tSl0ijQEBnVg5AaFWpZGf3kQ)
   3. [An Empirical Study on the Challenges of eBPF Application Development](https://dl.acm.org/doi/abs/10.1145/3672197.3673429)
