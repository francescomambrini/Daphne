#!/usr/bin/env python3

from glob import glob

for filename in glob("**/*.conllu", recursive=True):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace ASCII apostrophe (U+0027) with right single quote (U+2019)
    updated_content = content.replace('\u0027', '\u2019')

    if updated_content != content:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(updated_content)
        print(f"Updated: {filename}")
    else:
        print(f"No change: {filename}")