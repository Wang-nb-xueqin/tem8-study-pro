import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

# 换一组更有难度的专八词汇
words = "superfluous, exacerbate, pragmatic, ephemeral, meticulous"

# 极严格的指令
prompt = f"""
Write a professional, high-quality short story in ENGLISH (about 200 words) for a TEM-8 student.
Vocabulary to include: {words}.

IMPORTANT RULES:
1. The story must be in ENGLISH.
2. Format each target word EXACTLY like this: <span class="word" onclick="clickWord('Word', 'Phonetic', 'English Meaning', '中文释义')">Word</span>.
3. Replace 'Word', 'Phonetic', 'English Meaning', '中文释义' with the real data for each word.
4. Use a sophisticated, literary style (New Yorker style).
"""

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}]
)

story_html = response.choices[0].message.content

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
new_content = re.sub(r'.*?', 
                     f'\n<div class="story-fade-in">{story_html}</div>\n', 
                     content, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)
