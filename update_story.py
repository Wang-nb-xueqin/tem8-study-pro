import os
import re
from openai import OpenAI

# 1. 初始化 AI
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 2. 专八单词池
words = "superfluous, exacerbate, pragmatic, ephemeral, meticulous, precarious, ubiquitous"

# 3. 编写 AI 指令
prompt = f"""
Write a high-quality 200-word short story in ENGLISH for a TEM-8 student.
Style: The New Yorker / The Economist.
Target Vocabulary: {words}.

FORMAT RULES:
- Use <span class="word" onclick="clickWord('Word', 'Phonetic', 'English Meaning', '中文释义')">Word</span> for EACH target word.
- DO NOT use Markdown formatting (No ```html).
- Output the raw HTML content directly.
"""

try:
    # 4. 获取 AI 内容
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    story_html = response.choices[0].message.content
    story_html = story_html.replace("```html", "").replace("```", "").strip()

    # 5. 读取 index.html
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 6. 核心逻辑：直接寻找 <article> 标签进行替换
    pattern = r'(<article id="story-body">).*?(</article>)'
    # 构造新内容
    replacement = f'\\1\n\n{story_html}\n\n\\2'
    
    if '<article id="story-body">' in content:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: Magazine content updated!")
    else:
        print("Error: Could not find <article id='story-body'> in index.html")
        exit(1)

except Exception as e:
    print(f"Error occurred: {e}")
    exit(1)
