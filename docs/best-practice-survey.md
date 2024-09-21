# The best practice in Code-survey

AI can be similar to human, as for Now (2024.9), most AI may be like a graduate student from human perspective:

- Hallucinate: AI can hallucinate, like a graduate student can imagine.
    - Has a higher chance to filled randomly to a survey.
    - Answering questions very quickly but may no thinking carefully.
    - May lose some important information in the question.

We may need more evaluation to confirm that, but following these best practices can help improve the quality of the survey data and analysis, and avoid the problems above.

## Best Practices for Designing Code-survey

Designing a survey for graduate students who may have limited focus or a tendency to provide random responses—particularly when dealing with technical subjects like Linux kernel commits—requires careful consideration to ensure data quality and reliability. Below are best practices tailored to your specific scenario:

## **1. Clearly Define Survey Objectives**

- **Specificity:** Clearly outline what you aim to achieve with the survey. For example, understanding the categorization of Linux kernel commits, identifying patterns in bug fixes vs. feature additions, or analyzing the impact of certain features like eBPF.
- **Scope Limitation:** Keep the objectives narrow to avoid overwhelming respondents with too many topics.

## **2. Streamline Survey Design for Engagement**

- **Concise Length:** Graduate students are often pressed for time. Aim for a survey that can be completed in 10-15 minutes to reduce the likelihood of disengagement and random responses. This may also similar to the LLM model.

- **Logical Flow:** Organize questions in a logical sequence, starting with broader topics and narrowing down to specifics. This helps maintain a natural progression and keeps respondents engaged.

- **Sectioning:** Break the survey into sections with clear headings (e.g., **General Software Questions**, **eBPF-Specific Questions**) to provide structure and make navigation easier.

## **3. Optimize Question Design**

- **Clarity and Simplicity:** Use straightforward language, especially for technical questions. Avoid jargon unless necessary, and provide definitions or examples where appropriate.
- **Balanced Question Types:**
  - **Closed-Ended Questions:** Utilize multiple-choice, Likert scales, and categorical options to facilitate easier and quicker responses. It's much easier for LLM to answer these questions.
  - **Open-Ended Questions:** Limit these to essential areas where qualitative insights are necessary, as they require more effort and can lead to disengagement. In `Code-survey` with LLM, these could be used for summarizing commit details or identifying key words, but should be avoided in most cases.
- **Avoid Ambiguity:** Ensure each question is unambiguous and targets a single concept to prevent confusion and random answers. Provide clear instructions and examples for each question.
- **Use of Tags and Categories:** When tagging features (e.g., bug vs. new feature), provide clear definitions and examples to guide respondents accurately.
- **Give more time and space to answer and review**: For LLM, it may need more time to answer and review the questions. It may need to read the question multiple times to understand it. It may need to review the answer multiple times to make sure it's correct. SO you can define like a feedback loop to let it review the answer multiple times and selet the best one.

## **4. Implement Quality Control Measures**

- **Let unexpert select or say "I don't know'**: If the LLM is not expert enough, it may be better to let it select "I don't know" to reduce random answers. This is also the same for human.

- **evalute the domain knowledge**: It might be helpful to design some easy questions to evaluate the domain knowledge of the LLM. If the LLM is not expert enough, it may be better to give more information and examples to help it understand the question, or you need to build a RAG/fine-tuning model to help it understand the question. If not work, wait until the LLM is expert enough. 
    - For Linux kernel, LLM already have some domain knowledge, but it may not be enough for some too specific questions styles. E.g. It's nearly impossible for LLM to write correct kernel code for a specific feature in 2024.9. It's hard to answer very specific questions like "What is the usage and design goal of `bpf_link`?". But it can do summary and make choices for the feature types and commit types, once the information is provided.

- **Consistency Checks:**
  - **Logical Consistency:** Include questions that check for consistency in responses. For example, if a respondent categorizes a commit as a "merge commit," ensure they also marked as "merge" in other questions.

- **Validation Rules:**
  - **Mandatory Fields:** Ensure critical questions cannot be skipped.
  - **Input Validation:** Use validation to prevent nonsensical answers (e.g., date ranges, numerical limits).

- **Pilot Testing:** Conduct a pilot survey with a small group of graduate students to identify potential issues with question clarity, survey length, and technical functionality.
    -  **Feedback Loop:** Gather feedback from pilot participants to refine the survey design and improve clarity and engagement.
    - **Iterative Refinement:** Continuously refine the survey based on feedback and pilot results to enhance data quality.

## **7. Minimize Survey Fatigue**

- **Question Optimization:** Avoid overly lengthy or repetitive questions. Ensure each question serves a clear purpose aligned with your objectives. For LLM, this is important to avoid random answers. However, if the LLM is not advanced enough and do not have too much doman knowledge, it may be better to give more information and examples to help it understand the question.

## **8. Analyze and Filter Responses Post-Collection**

- **Data Cleaning:** After data collection, identify and exclude responses that fail attention checks or show patterns indicative of random answering (e.g., straight-lining in Likert scales).

## **9. Provide Clear Instructions and Support**

- **Comprehensive Guidance:** Offer clear instructions at the beginning of the survey and before each section to guide respondents effectively.


## **11. Tailor Questions to the Technical Context**

- **Relevance to Linux Kernel Commits:** Design questions that are directly relevant to analyzing Linux kernel commits, such as categorizing commit types, assessing the impact of specific features like eBPF, or understanding development patterns.

- **Provide Contextual Information:** When asking about specific features (e.g., `bpf_link`), provide sufficient context or references to ensure respondents understand the subject matter, reducing the likelihood of random or uninformed answers.

## **12. Leverage Pre-Defined Tags and Categories**

- **Structured Responses:** Use predefined tags and categories for respondents to select from, which can standardize responses and simplify data analysis. **DO NOT LET AI ANSWER OPEN-ENDED QUESTIONS RELATED TO TAGS**.
- **Multi-Select Options:** Allow multiple tags where applicable to capture the complexity of features or commits.

## **Example Implementation Strategies**

Given your focus on analyzing Linux kernel commits with tags like feature types and distinguishing between bugs and new features, here are some tailored strategies:

- **Pre-Classification:** Provide respondents with a list of predefined tags and categories based on your analysis (e.g., bug, new feature, performance improvement) to choose from when categorizing commits.
- **Contextual Questions:** For each commit, include a brief description or summary to help respondents make informed categorizations, reducing random tagging.
- **Hierarchical Structuring:** Implement hierarchical questions where the selection of a broad category (e.g., bug) leads to more specific follow-up questions about that category.
- **Examples and Non-Examples:** Include examples of how to categorize certain commits to guide respondents and minimize misclassification.

## **Conclusion**

Designing a survey for graduate students level LLM in a technical domain like Linux kernel commits requires balancing thoroughness with simplicity to maintain engagement and data quality. By implementing clear objectives, streamlined and well-structured questions, robust quality control measures, and strategies to enhance respondent motivation, you can effectively gather reliable and meaningful data. Additionally, tailoring the survey to the technical context and providing adequate support and instructions will further mitigate the risks of random or inattentive responses.

If you need further assistance with specific aspects of your survey design or have additional questions, feel free to ask!

## **Best Practices for Designing a general Survey**

Designing an effective survey and ensuring its quality are crucial steps in gathering reliable and actionable data. Below are best practices for survey design and strategies to control and enhance quality:


### 1. **Define Clear Objectives**
- **Purpose Identification:** Clearly articulate what you aim to achieve with the survey. Whether it's understanding customer satisfaction, gauging employee engagement, or researching market trends, having a well-defined purpose guides all other aspects of the survey design.
- **Specific Goals:** Break down the main objective into specific, measurable goals to ensure the survey addresses all necessary areas.

### 2. **Identify the Target Audience**
- **Demographics and Characteristics:** Understand who your respondents are, including age, gender, location, occupation, etc.
- **Relevance:** Ensure that the target audience is relevant to the survey objectives to gather meaningful data.

### 3. **Choose the Right Survey Method**
- **Delivery Mode:** Decide between online surveys, telephone interviews, face-to-face interviews, or paper questionnaires based on your audience and objectives.
- **Accessibility:** Ensure the survey is accessible to all intended respondents, considering factors like language, device compatibility, and ease of use.

### 4. **Design Clear and Concise Questions**
- **Simplicity:** Use straightforward language to avoid confusion.
- **Relevance:** Ensure each question aligns with the survey's objectives.
- **Brevity:** Keep questions as concise as possible without sacrificing clarity.

### 5. **Use Appropriate Question Types**
- **Closed-Ended Questions:** Useful for quantitative analysis (e.g., multiple-choice, Likert scales).
- **Open-Ended Questions:** Allow for qualitative insights but can be more time-consuming to analyze.
- **Balanced Options:** Provide a balanced set of response options to avoid bias.

### 6. **Avoid Leading and Biased Questions**
- **Neutral Wording:** Frame questions in a neutral manner to prevent influencing responses.
- **Balanced Scales:** Ensure response scales are balanced and do not favor a particular outcome.

### 7. **Logical Flow and Structure**
- **Logical Sequence:** Organize questions in a logical order, typically starting with general questions and moving to more specific ones.
- **Grouping:** Group related questions together to maintain a coherent flow.

### 8. **Pilot Testing**
- **Trial Run:** Conduct a pilot survey with a small subset of your target audience to identify any issues with question clarity, survey length, or technical problems.
- **Feedback Incorporation:** Use feedback from the pilot to refine and improve the survey before full deployment.

### 9. **Ensure Anonymity and Confidentiality**
- **Privacy Assurance:** Inform respondents about how their data will be used and ensure their anonymity if applicable, which can increase honesty in responses.
- **Data Protection:** Implement measures to protect respondent data from unauthorized access.

### 10. **Provide Clear Instructions**
- **Guidance:** Offer clear instructions on how to complete the survey, including how to navigate, answer questions, and submit responses.
- **Contact Information:** Provide a way for respondents to reach out if they encounter issues or have questions.

## **Controlling and Enhancing Survey Quality**

### 1. **Ensure Validity and Reliability**
- **Content Validity:** Make sure the survey covers all aspects related to the research objectives.
- **Construct Validity:** Ensure that the survey accurately measures the theoretical constructs it intends to.
- **Reliability Testing:** Assess the consistency of the survey results over time and across different populations.

### 2. **Implement Data Quality Checks**
- **Skip Logic and Validation:** Use survey software features to implement skip logic, mandatory fields, and input validation to minimize incomplete or inconsistent responses.
- **Duplicate Detection:** Identify and eliminate duplicate responses to ensure each respondent is only counted once.

### 3. **Maintain High Response Rates**
- **Engagement Strategies:** Use personalized invitations, reminders, and incentives to encourage participation.
- **Optimal Length:** Keep the survey as short as possible to prevent respondent fatigue, which can lead to lower quality responses.

### 4. **Analyze and Interpret Data Carefully**
- **Statistical Analysis:** Use appropriate statistical methods to analyze the data, ensuring that conclusions are supported by the evidence.
- **Bias Identification:** Be vigilant about potential biases in responses and account for them in your analysis.

### 5. **Continuous Improvement**
- **Feedback Loops:** After completing the survey, gather feedback on the survey process and use it to improve future surveys.
- **Regular Updates:** Keep the survey content and methodology up-to-date with current best practices and evolving research standards.

### 6. **Ethical Considerations**
- **Informed Consent:** Ensure that respondents are fully informed about the purpose of the survey and consent to participate.
- **Transparency:** Be transparent about how the data will be used, stored, and shared.

### 7. **Training for Survey Administrators**
- **Proper Training:** Ensure that those administering the survey are well-trained in delivering it consistently and handling respondent queries appropriately.
- **Standardization:** Use standardized procedures to minimize variability in how the survey is conducted.

## **Tools and Resources**

- **Survey Software:** Utilize reputable survey platforms like Qualtrics, SurveyMonkey, or Google Forms that offer robust features for design, distribution, and analysis.
- **Statistical Software:** Employ tools like SPSS, R, or Python for in-depth data analysis.
- **Guidelines and Frameworks:** Refer to established guidelines such as those from the American Association for Public Opinion Research (AAPOR) for best practices in survey research.

### **Conclusion**

Effective survey design and quality control are foundational to obtaining reliable and actionable data. By following these best practices and implementing robust quality control measures, you can enhance the validity, reliability, and overall effectiveness of your survey research.

If you have specific aspects of survey design you'd like to delve deeper into or need assistance with a particular stage of your survey project, feel free to ask!
