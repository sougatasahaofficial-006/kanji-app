import os
import re
import json
import asyncio
import edge_tts

AUDIO_DIR = os.path.join("public", "audio")
MANIFEST_PATH = os.path.join(AUDIO_DIR, "manifest.json")
DATA_FILES = [
    os.path.join("src", "data", "n5.ts"),
    os.path.join("src", "data", "n4.ts"),
    os.path.join("src", "data", "n3.ts"),
    os.path.join("src", "data", "n2.ts"),
    os.path.join("src", "data", "n1.ts"),
]

VOICES = {
    "male": "ja-JP-KeitaNeural",
    "female": "ja-JP-NanamiNeural",
}


def extract_items(ts_path: str) -> list[dict]:
    if not os.path.exists(ts_path):
        return []
    with open(ts_path, "r", encoding="utf-8") as f:
        text = f.read()

    match = re.search(r"=\s*(\[.*\]);", text, re.DOTALL)
    if not match:
        return []

    lessons = json.loads(match.group(1))
    items = []
    for lesson in lessons:
        for item in lesson.get("items", []):
            items.append(item)
    return items


async def generate_clip(text: str, voice_name: str, out_path: str):
    communicate = edge_tts.Communicate(text, voice_name)
    await communicate.save(out_path)


async def main():
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Load previous kana->id manifest if it exists
    old_manifest: dict[str, str] = {}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
                old_manifest = json.load(f)
        except Exception:
            old_manifest = {}

    all_items = []
    seen_ids: dict[str, str] = {}
    duplicates = []

    for path in DATA_FILES:
        for item in extract_items(path):
            item_id = item["id"]
            kana_text = item["kana"].strip()
            if item_id in seen_ids:
                duplicates.append((item_id, seen_ids[item_id], kana_text, path))
            else:
                seen_ids[item_id] = kana_text
                all_items.append(item)

    if duplicates:
        print(f"⚠️ WARNING: Found {len(duplicates)} duplicate item IDs:")
        for dup_id, first_kana, second_kana, path in duplicates[:10]:
            print(f"   - ID '{dup_id}' in {path}: '{first_kana}' vs '{second_kana}'")

    tasks = []
    new_manifest: dict[str, str] = {}

    for item in all_items:
        item_id = item["id"]
        kana_text = item["kana"].strip()
        new_manifest[item_id] = kana_text

        # Regenerate if kana changed since last run OR file doesn't exist / is empty
        kana_changed = old_manifest.get(item_id) != kana_text

        for gender, voice_name in VOICES.items():
            out_path = os.path.join(AUDIO_DIR, f"{item_id}-{gender}.mp3")
            file_invalid = not os.path.exists(out_path) or os.path.getsize(out_path) == 0

            if kana_changed or file_invalid:
                tasks.append(generate_clip(kana_text, voice_name, out_path))

    print(f"Total unique words: {len(all_items)} | Clips needing (re)generation: {len(tasks)}")

    batch_size = 15
    for i in range(0, len(tasks), batch_size):
        await asyncio.gather(*tasks[i : i + batch_size])
        print(f"Generated {min(i + batch_size, len(tasks))} / {len(tasks)} clips...")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(new_manifest, f, ensure_ascii=False, indent=2)

    print(f"Done! All audio files in {AUDIO_DIR}/ now match exact kana readings.")


if __name__ == "__main__":
    asyncio.run(main())