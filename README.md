# Code-Survey: Uncovering Insights in Complex Software evolutions with LLM

- Do we really know how complex systems like the Linux works?
- How can we understand the high-level design cohice and evolution of a Super Complex system, like the Linux kernel?

**Code-Survey** is `the first step` here to change that.

> Imagine if you can ask every entry-level kernel developer, or a Graduate Student who is studying kernel, to do a survey and answer questions about every commit, what can you find with the results?

Code-Survey helps you `explore` and `analyze` the world's largest and most intricate codebases, like the Linux kernel. By carefully **design a survey** and **transforming** `unstructured data` like commits, mails into organized, `structed and easy-to-analyze data`, then you can do `quantitative` analysis on it. Code-Survey makes it simpler to uncover valuable insights in modern complex software systems.

Code-Survey is the first step trying to bridges the gap between high level `design`, `implementation`, `maintenance`, `reliability` and `security` using LLM, making complex systems more accessible.

Unlike other approaches:

- No human can do that before, but AI can.
- No chatbots, RAG document search, or code generation: **stop the stupid AI!**
- Just using data like git message and email data. Design a survey and run with hundreds lines of codes in Python. Just Apply to other project or subsystems by designing your code-survey!

**Let's do Code-Survey!**

## What can `Code-Survey` help answer?

- How do new feature introductions in component affect software stability and performance over the time?
- What identifiable phases exist in a component lifecycle? Is it new, mature, refactored or deprecated?
- What dependencies have emerged between features and component, and how do they affect software evolution?
- How does bug frequency correlate with feature complexity?
- What were the trade-offs considered in design decisions, and how do they manifest in the system's implementation?
- How does the collaboration between developers affect the consistency and coherence of feature development?

Here is an example of analysis: **[docs/report_ebpf.md](docs/report_ebpf.md).** (Not yet complete...more is adding)

## Workflow / Methodolog

The core idea of Code-survey is to treat LLMs like human participants in a survey: 

- they can process data faster and cheaper, but are also prone to errors and limitations. 
- By applying traditional human survey methods, we can efficiently conduct LLM-based surveys, while human experts provide oversight and validation to ensure accuracy.
- You can let LLM help you with survey design and data 

![workflow](docs/workflow.jpg)

Our approach follows a well-defined workflow:

1. **Human Experts or LLM Agents design surveys**: Tailored questions for each unstructured data type (e.g., commits, emails) to extract key information.
2. **LLM Agents complete the surveys**: Answering yes/no, tagging relevant data, and summarizing key information. **This is the key steps to turn unstructured data into structured data.**
3. **Human Experts or LLM Agents analysis results**: Ensuring accuracy and uncover new insights easily from that. If the results are not statisfied, go back to step 1 to enhance the survey.
4. **Generate Reports**: Summarize the results and provide insights into the data.

There are also 4 key steps to allow LLM Agent asistant to design the survey. The workflow and prompts are like:

1. **Identify the target audience and their roles**: If you can ask every kernel developer to do a completed survey/questionare about a commit/a mail, what kinds of people may be intereted in it? Describe the roles in detail.
2. **Designing High Level insightful questions based on the roles**: What are the most insightful questions related to `design`, `implementation`, `maintenance`, `reliability` and `security` of {role} may be interested in? Describe the questions for each role in detail.
3. **Identify the required data types and sources for the insightful questions**: What are the data types and sources required to answer the insightful question {Your question} your descirbed before? Describe the data types and sources for each question in detail.
4. **Design the survey questions to get the data:** What are the survey questions you can design to get the {data type} for the insightful question {Your question} from {data source} your descirbed before? Describe the survey questions for {data source} * {data type} in detail.

## Linux-bpf Dataset

The **Linux-bpf dataset** focuses on the eBPF subsystem and is continuously updated via CI. The dataset includes:

- **680+ expert-selected commits**: Features, commit details, types (Map, Helper, Kfunc, Prog, etc.). Human experts tagged these commits and can be analyzed by LLM Agents. [dataset here](data/feature_commit_details.csv)
- **12,000+ BPF-related commits**: LLM Agent surveys and summaries. You can download [dataset here](data/commit_survey.csv).
- **150,000+ BPF subsystem-related emails**: LLM Agent surveys and summaries(`TODO`).

**To see more details abot what we find, check the analysis in [report_ebpf.md](docs/report_ebpf.md).**

A simplest approach to see how these data works is just **Upload the CSV to ChatGPT**(**Or other platforms) and Ask questions to let it Analysis for you!

Note this is just a very simple demo now --- there are hundreds of ways to improve the survey accuracy:

- It's using gpt4o API, o1 model can be much better;
- You can simply run it multiple times to get multiple survey results and then average them. This is typically a real survey d and the result would be much better, but we need time and more money for API.
- More Advance Agent design with multi-steps and reasonging, or multi-agent;
- Better prompt engineering;


## Survey Example

You can find this example in [survey/commit_survey.yml](survey/commit_survey.yml), which analysis all the 10000+ bpf commits in the Linux kernel eBPF subsystem.

```yml
title: "Commit Classification Survey"
description: "A survey about the commit in Linux eBPF, to help better understand the design and evolution of bpf subsystem. For choice, try to be as specific as possible based on the commit message and code changes. If the commit message is not clear or does not provide enough information, you can choose the 'I'm not sure' option."
hint: "For example, when seems not related to eBPF, confirm it's a rare cases really has nothing to do with eBPF in all it's contents, such as btrfs or misspelled commit message. Do not tag subsystem changes related to eBPF as not."
questions:
- id: summary
  type: fill_in
  question: "Please provide a summary of It in one short sentence not longer than 30 words. Only output one sentence."
  required: true

- id: keywords
  type: fill_in
  question: "Please extract no more than 3 keywords from the commit. Only output 3 keywords without any special characters."
  required: true

- id: commit_classification
  type: single_choice
  question: "What may be the main type of the commit?"
  choices:
    - value: A bug fix. It primarily resolves a bug or issue in the code.
    - value: A new feature. It adds a new capability or feature that was not previously present.
    - value: A performance optimization. It improves the performance of existing code such as reducing latency or improving throughput.
    - value: A cleanup or refactoring in the code. It involves changes to improve code readability maintainability or structure without changing its functionality.
    - value: A documentation change or typo fix. It only involves changes to documentation files or fixes a typographical error.
    - value: A test case or test infrastructure change. It adds or modifies test cases test scripts or testing infrastructure.
    - value: A build system or CI/CD change. It affects the build process continuous integration or deployment pipelines.
    - value: A security fix. It resolves a security vulnerability or strengthens security measures.
    - value: It's like a merge commit. It merges changes from another branch or repository.
    - value: It's other type of commit. It does not fit into any of the categories listed above.
    - value: I'm not sure about the type of the commit. The nature of It is unclear or uncertain.

- id: major_related_implementation_component
  type: single_choice
  question: "What major implementation component is modified by the commit? It's typically where the code changes happened."
  choices:
    - value: The eBPF verifier. This component ensures that eBPF programs are safe to run within the kernel.
    - value: The eBPF JIT compiler for different architectures. It changes how eBPF bytecode is translated into machine code for different hardware architectures.
    - value: The helper and kfuncs. It modifies or adds helpers and kernel functions that eBPF programs can call.
    - value: The syscall interface. It changes the system calls through which user-space programs interact with eBPF.
    - value: The eBPF maps. It changes how data structures shared between user-space and kernel-space (maps) are created or managed.
    - value: The libbpf library. It affects the library that simplifies interaction with eBPF from user-space applications.
    - value: The bpftool utility. It modifies the bpftool utility used for introspecting and interacting with eBPF programs and maps.
    - value: The test cases and makefiles. It adds or modifies test cases or makefile scripts used for testing or building eBPF programs.
    - value: The implementation happens in other subsystem and is related to eBPF events. e.g. probes perf events tracepoints network scheduler HID LSM etc. Note it's still related to how eBPF programs interact with these events. 
    - value: It's like a merge commit. It includes significant changes across multiple components of the system.
    - value: It's not related to any above. It affects an implementation component not listed but does related to the BPF subsystem.
    - value: It's not related to any above. It affects an implementation component is totally unrelated to the BPF subsystem.  It's not related to any above because it totally not related to the BPF subsystem. It's a rare case wrong data and need removed.
    - value: I'm not sure about the implementation component of the commit. The component affected by It is unclear.
......
```

## Why LLM?

LLMs have been proven effective in survey, summarization, and analysis tasks in fields like market research and chemistry. With LLMs, we can analyze unstructured data, which traditional methods struggle to handle efficiently. 

### Why Not Other Methods? Why human experts can't?

- **Domain Knowledge**: Required for Linux kernel analysis Domain Knowledge. Just use keyword search or simple NLP tools can't handle that.
- **Unstructured Data**: Commit messages and emails are difficult to process with traditional tools.
- **Expert Cost**: Manually analyzing this data is time-consuming and expensive. **It's impossible to do that for the whole Linux kernel commits.**
Here’s a focused version emphasizing **Designing Questions** and **Using Statistical Methods** for ensuring correctness and consistency:

### How to Make Sure the Result is Correct and Meaningful?

- **Design Questions for Correctness**: Create well-structured, specific questions that minimize ambiguity. Design questions to compare similar features, commits, or components across different contexts, which helps identify inconsistencies and errors in the results.
- **Cross-Check with Known Data**: Ensure that the questions target areas where the answers can be validated with reliable sources like commit logs, documentation, or expert knowledge, allowing easy verification of correctness.
- **Use Statistical Methods to Ensure Consistency**: Apply statistical tools like variance analysis or correlation checks to spot inconsistencies across different answers. If similar questions yield divergent results, investigate potential errors in data collection or question framing.
- **Detect Anomalies and Outliers**: Statistical analysis can flag unusual or extreme responses that deviate from the norm. Review these outliers to assess whether they highlight real anomalies or potential mistakes in survey logic.
- **Measure Agreement Between Runs**: Use methods like inter-rater reliability or other consistency metrics to compare results across multiple runs of the survey, ensuring consistent responses to repeated questions.

### Best Practices for Designing Surveys:

The key points to consider when designing code-surveys are:

1. Use **pre-defined tags and categories** to structure responses and avoid open-ended questions where LLMs may hallucinate.  
2. Allow LLMs to answer "I don’t know" for unfamiliar questions to prevent incorrect or random responses.  
3. Using **feedback loops, CoT planning** and memory for LLM Agents to review and refine answers multiple times for better accuracy.  
4. Perform **pilot testing** and apply **data validation** to ensure logical consistency and filter out low-quality responses.

For a more detailed explanation and the general approach, see the [docs/best-practice-survey.md](docs/best-practice-survey.md) document.

### Limitations

- **Dependency on Data Quality:** The method relies on complete and well-structured commit data, and incomplete data can obscure analysis.
- **LLM Mistakes:** LLMs, like humans, can misinterpret or hallucinate, but careful survey design can help mitigate these issues.
- **Human Expert Oversight:** Expert involvement is essential for designing effective surveys and interpreting results, which may limit scalability.

### Future Work

1. **Improved Evaluation of LLM-Generated Data:** Develop validation frameworks and benchmarks to improve accuracy in LLM outputs.
2. **Automation and Performance Enhancement:** Automate the process further with advanced models and improve performance for seamless machine analysis.
3. **Application to Other Repositories:** Expand the method to projects like Kubernetes, LLVM, and Apache for scalability and versatility.
4. **Direct Structuring of Code and Functions:** Move beyond commits and mailing lists to structure code and functions into queryable data.
5. **Integration of Additional Data Sources:** Incorporate data from reviews, issue trackers, and documentation to enhance insights into feature evolution.
6. **Ethical and Privacy Considerations:** Focus on anonymization, regulatory compliance, and secure handling of sensitive data.

## References

Linux development:

1. [Submitting patches: the essential guide to getting your code into the kernel](https://www.kernel.org/doc/html/v4.10/process/submitting-patches.html)
2. [how to ask question in maillist](https://www.linuxquestions.org/questions/linux-kernel-70/how-to-ask-question-in-maillist-4175719442/)
3. [How to Communicate When Submitting Patches: An Empirical Study of the Linux Kernel](https://dl.acm.org/doi/abs/10.1145/3359210)
3. [Differentiating Communication Styles of Leaders on the Linux Kernel Mailing List](https://dl.acm.org/doi/abs/10.1145/2957792)

AI model:

- [Introducing OpenAI o1-preview](https://openai.com/index/introducing-openai-o1-preview/) They can reason through complex tasks and solve harder problems than previous models in science, coding, and math.
