import os
import re
from openai import OpenAI

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="[https://api.deepseek.com](https://api.deepseek.com)")

# 自动更新专八难词
words = "superfluous, exacerbate, pragmatic, ephemeral, meticulous, precarious, ubiquitous"

prompt = f"""
Write a 200-word news article or essay in English. 
Style: The Economist / The New Yorker. 
Target Words: {words}.

REQUIRED FORMAT:
For each target word, you MUST use this HTML tag: <span class="word" onclick="clickWord('Word', 'Phonetic', 'English Meaning', '中文释义')">Word</span>.
Do NOT use Markdown. Do NOT use ```html blocks.
The output should only be the story content with HTML tags.
"""

try:
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    story_html = response.choices[0].message.content
    # 清洗掉可能出现的 Markdown 代码块标记
    story_html = story_html.replace("```html", "").replace("```", "").strip()

    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

   # 这段代码会更加智能地寻找标记，无论它们中间有多少空格
    import re
    
    # 查找标记及其之间的任何内容（包含换行符）
    pattern = r'.*?'
    replacement = f'\n{story_html}\n'
    
    # 检查内容里到底有没有这两个标记
    if "STORY_START" in content and "STORY_END" in content:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Success: Story replaced!")
    else:
        print("Error: Could not find STORY_START or STORY_END markers in index.html")
        # 如果找不到，脚本会报错，你会看到 Actions 变红，我们就知道问题在哪了
        exit(1)

