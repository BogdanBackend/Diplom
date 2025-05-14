# TODO: Пофіксити кирилицю в pdf

# sudo apt update && sudo apt install -y pandoc texlive texlive-latex-extra texlive-xetex
import re
import subprocess
from pathlib import Path
import sys

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

def get_file_temp_name(file):
    return Path(file).with_name(Path(file).stem + "_temp" + Path(file).suffix)

# Видалення тимчасових файлів
def remove_temp_files(files):
    def delete_file(file):
        if file.exists():
            file.unlink()
            print(f"Видалено тимчасовий файл: {file}")
    
    for file in files:
        delete_file(get_file_temp_name(file))
    
    delete_file(script_dir / "links_temp.md")

if len(sys.argv) > 1 and sys.argv[1] == "clear":
    remove_temp_files(files)
    print("Тимчасові файли видалено.")
    exit(0)

links = []

for file in files:
    file_temp = get_file_temp_name(file)
    with open(file, "r", encoding="utf-8") as f_in, open(file_temp, "w", encoding="utf-8") as f_out:
        f_in_content = f_in.read()
        f_out_content = f_in_content
        # Пошук інтернет посилань
        # Формат: [Назва](http://example.com) або [Назва](https://example.com)
        # Заміна їх на [1]або [2] і так далі по номеру в списку links
        # Знаходимо всі markdown-посилання на http/https
        urls = re.findall(r"\[.*?\]\(https?://[^\s)]+\)", f_in_content)
        print('urls', urls)
        for i, url in enumerate(urls):
            # Додаємо URL до списку
            links.append(url)
            # Заміна URL на [номер]
            f_out_content = f_out_content.replace(url, f"[{i + 1}]")
        f_out.write(f_out_content)

# Збереження списку посилань у файл
links_file = script_dir / "links_temp.md"

with open(links_file, "w", encoding="utf-8") as f:
    for i, link in enumerate(links):
        # Додаємо URL до списку
        f.write(f"[{i + 1}] {link}\n")

    # with open(file, "r", encoding="utf-8") as f:
    #     with open(file, "w", encoding="utf-8") as f_out:
            

# for file in files:
#     with open(file, "r", encoding="utf-8") as f:
#         # пошук інтернет посилань 

#         # Формат: [Назва](http://example.com)
#         urls = re.findall(r"\[.*?\]\((https?://[^\s)]+)\)", f.read())
#         print(urls)

