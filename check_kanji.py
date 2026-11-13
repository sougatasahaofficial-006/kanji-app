import re

levels = ["n5", "n4", "n3", "n2", "n1"]
seen_kanji = set()

for lvl in levels:
    with open(f"src/data/{lvl}.ts", "r", encoding="utf-8") as f:
        text = f.read()

    lesson_count = len(re.findall(r'"lessonNumber"\s*:', text))
    words = re.findall(r'"word"\s*:\s*"([^"]+)"', text)

    new_kanji = []
    for word in words:
        for ch in re.findall(r"[\u4e00-\u9faf]", word):
            if ch not in seen_kanji:
                seen_kanji.add(ch)
                new_kanji.append(ch)

    first = new_kanji[0] if new_kanji else "None"
    last = new_kanji[-1] if new_kanji else "None"
    print(f"{lvl.upper()}: {lesson_count} lessons | {len(new_kanji)} root Kanji (First: {first}, Last: {last})")

print(f"\nTotal Unique Root Kanji across N5–N1: {len(seen_kanji)}")