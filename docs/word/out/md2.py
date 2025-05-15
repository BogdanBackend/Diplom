# sudo apt update && sudo apt install -y pandoc && pip install python-docx

import re
import subprocess
from pathlib import Path
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt

TEMPLATE_DOCX = "template.docx"
OUT_DOCX      = "diplom_dev.docx"
DEBUG = False
# Визначення шляху до README.md відносно місця розташування скрипта
script_dir = Path(__file__).parent.parent.resolve()
readme_path = script_dir / "README.md"
template_docx = script_dir /"out"/"template"/ TEMPLATE_DOCX
out_docx      = script_dir /"out"/ OUT_DOCX

# Вихідні файли
ms2docx = script_dir / "out/md2doc_dev.docx"

# Перевірка наявності README.md
if not readme_path.exists():
    print(f"Файл README.md не знайдено за шляхом: {readme_path}")
    exit(1)

# Зчитування файлу README.md
with readme_path.open("r", encoding="utf-8") as f:
    # Пошук файлів Markdown у README.md
    # Формат: [Назва](ім'я_файлу.md)
    files = re.findall(r"\[.*?\]\((.*?\.md)\)", f.read())

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
def delete_file(file):
    if file.exists():
        file.unlink()
        if DEBUG:
            print(f"Видалено тимчасовий файл: {file}")
def remove_temp_files(files):
    for file in files:
        delete_file(get_file_temp_name(file))
    delete_file(script_dir / "links_temp.md")

if len(sys.argv) > 1:
    if sys.argv[1] == "clear":
        remove_temp_files(files)
        print("Тимчасові файли видалено.")
        exit(0)
    elif sys.argv[1] != "no-clear":
        print("Невірний аргумент. clear або no-clear.")
        exit(1)

NEW_PAGE = '```{=openxml}\n<w:p>\n  <w:r>\n    <w:br w:type="page"/>\n  </w:r>\n</w:p>\n```\n\n'

links = []
for file_i, file in enumerate(files):
    file_temp = get_file_temp_name(file)
    with open(file, "r", encoding="utf-8") as f_in, open(file_temp, "w", encoding="utf-8") as f_out:
        content = f_in.read()
        # Пошук інтернет посилань
        # Формат: [Назва](http://example.com) або [Назва](https://example.com)
        # Заміна їх на [1] або [2] і так далі по номеру в списку links
        for url in re.findall(r"\[.*?\]\(https?://[^\s)]+\)", content):
            # Додаємо URL до списку
            links.append(url)
            # Заміна URL на [номер]
            content = content.replace(url, f"{url.split("](")[0][1:]}[{len(links)}]")
        for img_i, img in enumerate(re.findall(r"!\[.*?\]\([^\)]*\)", content)):
            # Заміна ![img](img) на [img](img)
            # парсинг опису та шляху до зображення

            img_parts = img.split("](")
            img_desc = img_parts[0][2:]
            img_path = img_parts[1][:-1]
            new_img = f"![Рис {file_i+1}.{img_i+1}. {img_desc}]({script_dir/img_path})"
            content = content.replace(img, new_img)
            # Додаємо img до списку
        f_out.write(NEW_PAGE)
        f_out.write(content)

files_out = [get_file_temp_name(file) for file in files]

if links:
        # Збереження списку посилань у файл
    links_file = script_dir / "links_temp.md"
    files_out.append(str(links_file))

    with open(links_file, "w", encoding="utf-8") as f:
        f.write(NEW_PAGE)        
        f.write('# Список використаних джерел\n')
        links.append("[Архів проєкту КПК](https://github.com/Bogd-an/Diplom)")
        for i, link in enumerate(links):
            # Додаємо URL до списку
            text, url = (link.split("](")[0][1:], link.split("](")[1][:-1])
            f.write(f"[{i + 1}] {text}, [Електронний ресурс] URL: {url} (дата звернення: 01.05.2025)\n\n")

# Конвертація в DOCX
try:
    command = ["pandoc",
                f"--reference-doc={template_docx}", 
                "--from=markdown", 
                "--to=docx", 
                *[str(f) for f in files_out], 
                "-o", 
                str(ms2docx)]
    if DEBUG:
        print(f"\n\nКоманда: {' '.join(command)}\n")
    result = subprocess.run(command, capture_output=True, text=True)
    warning_lines = [line for line in result.stderr.splitlines() if "[WARNING]" in line]
    if DEBUG:
        for line in warning_lines:
            # Витягуємо шлях до файлу з попередження
            match = re.search(r"Could not fetch resource '([^']+)'", line)
            if match:
                print(f"WARNING: {Path(match.group(1)).name}")
    if result.returncode != 0:
        print(result.stderr)
        raise subprocess.CalledProcessError(result.returncode, command)
    print(f"Файл {ms2docx} успішно створено!")
except subprocess.CalledProcessError as e:
    print(f"Помилка під час створення {ms2docx} :", e)
    exit(1)


if len(sys.argv) == 1:
    remove_temp_files(files)
    exit(0)