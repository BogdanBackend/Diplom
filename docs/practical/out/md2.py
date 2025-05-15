# sudo apt update && sudo apt install -y pandoc && pip install python-docx

import re
import subprocess
from pathlib import Path
import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

TEMPLATE_DOCX = "practiacal_template.docx"
OUT_DOCX      = "prac_dev.docx"

# Визначення шляху до README.md відносно місця розташування скрипта
script_dir = Path(__file__).parent.parent.resolve()
readme_path = script_dir / "README.md"
template_docx = script_dir /"out"/ TEMPLATE_DOCX
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


links = []
for file in files:
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
        
        f_out.write('<div style="page-break-after: always;"></div>\n') # Додаємо розрив сторінки для Pandoc
        f_out.write(content)

files_out = [get_file_temp_name(file) for file in files]

if links:
        # Збереження списку посилань у файл
    links_file = script_dir / "links_temp.md"
    files_out.append(str(links_file))

    with open(links_file, "w", encoding="utf-8") as f:
        f.write('<div style="page-break-after: always;"></div>\n')
        f.write('# Список використаних джерел\n')
        links.append("[Архів проєкту КПК](https://github.com/Bogd-an/Diplom)")
        for i, link in enumerate(links):
            # Додаємо URL до списку
            text, url = (link.split("](")[0][1:], link.split("](")[1][:-1])
            f.write(f"[{i + 1}] {text}, [Електронний ресурс] URL: {url} (дата звернення: 01.05.2025)\n")

# Конвертація в DOCX
try:
    subprocess.run(["pandoc", f"--reference-doc={template_docx}", *files_out, "-o", str(ms2docx)], check=True)
    print(f"Файл {ms2docx} успішно створено!")
except subprocess.CalledProcessError as e:
    print(f"Помилка під час створення {ms2docx} :", e)


try:
    # Відкриваємо шаблон (основний документ)
    master = Document(template_docx)

    # Перевіряємо, чи існує стиль 'Normal'
    style_names = [s.name for s in master.styles]
    if 'Normal' not in style_names:
        style = master.styles.add_style('Normal', WD_STYLE_TYPE.PARAGRAPH)
    else:
        style = master.styles['Normal']

    # Налаштовуємо стиль 'Normal'
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(14)

    pf = style.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing = 1.5

    # Вивід стилів для перевірки
    print("\nСписок стилів у шаблоні:")
    for s in master.styles:
        print(f"Назва: {s.name}")
        if hasattr(s, 'font'):
            f = s.font
            print(f"  Шрифт: {f.name}, Розмір: {f.size}, Жирний: {f.bold}, Курсив: {f.italic}")
        if hasattr(s, 'paragraph_format'):
            pf = s.paragraph_format
            print(f"  Відступи: left={pf.left_indent}, right={pf.right_indent}, first_line={pf.first_line_indent}")
            print(f"  Вирівнювання: {pf.alignment}")
        print("-" * 40)
    print("\n")

    # Відкриваємо другий документ (той, який треба додати)
    sub = Document(ms2docx)

    # Переносимо вміст другого документа в перший
    for element in sub.element.body:
        master.element.body.append(element)

    # Зберігаємо результат
    master.save(out_docx)
    print(f"Файл {out_docx} успішно створено шляхом об'єднання!")
    ms2docx.unlink()  # Видаляємо тимчасовий файл
except Exception as e:
    print(f"Помилка при об'єднанні DOCX-файлів:", e)

if len(sys.argv) == 1:
    remove_temp_files(files)
    exit(0)