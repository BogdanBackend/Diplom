# TODO: Пофіксити кирилицю в pdf

# sudo apt update && sudo apt install -y pandoc texlive texlive-latex-extra texlive-xetex
import re
import subprocess
from pathlib import Path

# Визначення шляху до README.md відносно місця розташування скрипта
script_dir = Path(__file__).parent.parent.resolve()
readme_path = script_dir / "README.md"

# Перевірка наявності README.md
if not readme_path.exists():
    print(f"Файл README.md не знайдено за шляхом: {readme_path}")
    exit(1)

# Зчитування файлу README.md
with readme_path.open("r", encoding="utf-8") as f:
    content = f.read()

# Пошук файлів Markdown у README.md
# Формат: [Назва](ім'я_файлу.md)
files = re.findall(r"\[.*?\]\((.*?\.md)\)", content)

# Перевірка, чи знайдено файли
if not files:
    print("У README.md не знайдено посилань на файли Markdown!")
    exit(1)

# Перевірка існування файлів
missing_files = [file for file in files if not (script_dir / file).exists()]
if missing_files:
    print(f"Наступні файли не знайдено: {', '.join(missing_files)}")
    exit(1)

# Повний шлях до файлів
files = [str(script_dir / file) for file in files]


print(f"Файли: {files}")

for file in files:
    with open(file, "r", encoding="utf-8") as f:
        # пошук інтернет посилань 
        # Формат: [Назва](http://example.com)
        urls = re.findall(r"\[.*?\]\((https?://[^\s)]+)\)", f.read())
        print(urls)

