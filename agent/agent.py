import os

from dotenv import load_dotenv

load_dotenv()

import csv

from model import CommitFeedback
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    organization=os.getenv("OPENAI_ORGNIZATION"),
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 定义函数：调用GPT-4o分析commit
def analyze_commit(commit_message: str):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the commit message and provide feedback on the feature.",
                },
                {"role": "user", "content": f"Commit message: {commit_message}"},
            ],
            response_format=CommitFeedback,  # 结构化输出格式
        )
        feedback = completion.choices[0].message.parsed
        return feedback
    except Exception as e:
        print(f"Error processing commit message: {e}")
        return None


# 读取CSV文件并分析每个commit
def process_commits(input_csv_path, output_csv_path):
    # 确认输入文件是否存在
    if not os.path.exists(input_csv_path):
        print(f"Input file not found: {input_csv_path}")
        return

    with open(input_csv_path, mode="r", newline="", encoding="utf-8") as infile, open(
        output_csv_path, mode="w", newline="", encoding="utf-8"
    ) as outfile:

        # 读取CSV
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + [
            "is_good_feature",
            "category",
            "summary",
        ]  # 添加新的AI反馈栏位
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        # 写入CSV头
        writer.writeheader()

        # 逐行处理每个commit
        for row in reader:
            commit_message = row["commit_message"]
            feedback = analyze_commit(commit_message)

            if feedback:
                # 将AI生成的反馈添加到原始数据中
                row["is_good_feature"] = feedback.is_good_feature
                row["category"] = feedback.category
                row["summary"] = feedback.summary
            else:
                # 如果反馈出错，用默认值填充
                row["is_good_feature"] = "N/A"
                row["category"] = "N/A"
                row["summary"] = "N/A"

            # 将新的数据写入到输出文件
            writer.writerow(row)

            break

    print(f"Processing complete. Results saved to {output_csv_path}")

# 运行示例
input_csv = "../data/feature_commit_details.csv"  # 替换为你的输入文件路径
output_csv = "output.csv"  # 输出文件路径

process_commits(input_csv, output_csv)

