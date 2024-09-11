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
  - domain knowledgeit（cite)
  - unstruct data （cite）
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

