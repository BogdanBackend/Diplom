# TODO: Пофіксити кирилицю в pdf

# sudo apt update && sudo apt install -y pandoc texlive texlive-latex-extra texlive-xetex ttf-mscorefonts-installer
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
# Вихідні файли
output_docx = script_dir / "out/document_dev.docx"
output_pdf = script_dir / "out/document_dev.pdf"


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

if len(sys.argv) > 1:
    if sys.argv[1] == "clear":
        remove_temp_files(files)
        print("Тимчасові файли видалено.")
        exit(0)
    print("Невірний аргумент. Використовуйте 'clear' для видалення тимчасових файлів.")
    exit(1)

links = []

for file in files:
    file_temp = get_file_temp_name(file)
    with open(file, "r", encoding="utf-8") as f_in, open(file_temp, "w", encoding="utf-8") as f_out:
        content = f_in.read()
        # Пошук інтернет посилань
        # Формат: [Назва](http://example.com) або [Назва](https://example.com)
        # Заміна їх на [1]або [2] і так далі по номеру в списку links
        for url in re.findall(r"\[.*?\]\(https?://[^\s)]+\)", content):
            # Додаємо URL до списку
            links.append(url)
            # Заміна URL на [номер]
            content = content.replace(url, f"{url.split("](")[0][1:]}[{len(links)}]")
        
        f_out.write('<div style="page-break-after: always;"></div>\n') # Додаємо розрив сторінки для Pandoc
        f_out.write(content)

# Збереження списку посилань у файл
links_file = script_dir / "links_temp.md"

with open(links_file, "w", encoding="utf-8") as f:
    f.write('<div style="page-break-after: always;"></div>\n')
    f.write('# Список використаних джерел\n')
    links.append("[Архів проєкту КПК](https://github.com/Bogd-an/Diplom)")
    for i, link in enumerate(links):
        # Додаємо URL до списку
       text = link.split("](")[0][1:]
       url = link.split("](")[1][:-1]
       f.write(f"[{i + 1}] {text}, [Електронний ресурс] URL: {url} (дата звернення: 01.05.2025)\n")


# Функція для виконання Pandoc
def convert_to_format(output_file, files):
    try:
        subprocess.run(["pandoc", "diplom_template.docx", *files, "-o", str(output_file),], check=True)
        print(f"Файл {output_file} успішно створено!")
    except subprocess.CalledProcessError as e:
        print(f"Помилка під час створення {output_file} :", e)

files_out = [get_file_temp_name(file) for file in files]
files_out.append(str(links_file))

# Конвертація в DOCX
convert_to_format(output_docx, files_out)

# Конвертація в PDF
# convert_to_format(output_pdf, files_out)