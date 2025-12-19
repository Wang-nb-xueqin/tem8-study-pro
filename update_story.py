import os
from openai import OpenAI

# 1. 连通 AI
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 2. 这里的单词列表你可以之后改成读取 data.json
words = "abide, abrupt, alleviate, ambiguous, analogous" 

# 3. 让 AI 生成故事
prompt = f"请用以下专八单词写一个300字故事，要求单词加粗，并使用 <span class='word' onclick='clickWord(...)'>单词</span> 格式包裹。单词列表：{words}"

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)

story_html = response.choices[0].message.content

# 4. 自动替换 index.html 里的内容
with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 假设你在 index.html 里用了 作为标记
import re
new_content = re.sub(r'.*?', 
                     f'{story_html}', 
                     content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
