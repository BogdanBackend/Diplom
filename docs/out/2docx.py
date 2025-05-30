'''
посилання:

[Текст](посилання) -> Текст[0]
[Текст !](посилання) -> [1]
>>> ЯКАСЬ СТАТТЯ -> [2]
![підпис](посилання) -> рисунок по центру з підписом і нумерацією 
![підпис w=15](посилання) -> те саме але з шириною 15 см
![Table: підпис](посилання) -> таблиця по центру з підписом і нумерацією
'''

import argparse
import re
import subprocess
import sys
from pathlib import Path
import hashlib

# === Константи ===
TEMPLATE_DOCX = "template.docx"
# OUT_DOCX = "diplom_dev.docx"

# === Шляхи ===
script_dir = Path(__file__).parent.parent.resolve()
content_path = script_dir / "content.md"
readme_path = script_dir / "README.md"
template_docx = script_dir / "out" / "template" / TEMPLATE_DOCX
# out_docx = script_dir / "out" / OUT_DOCX
ms2docx = script_dir / "out" / "doc_dev.docx"

# === Параметри ===
DEBUG = False

# === Константи для форматування ===
NEW_PAGE = '```{=openxml}\n<w:p>\n  <w:r>\n    <w:br w:type="page"/>\n  </w:r>\n</w:p>\n```\n\n'
CENTER_XML = '```{=openxml}\n<w:p><w:pPr><w:jc w:val="center"/></w:pPr></w:p>\n```\n'
IMG_WIDHT = 8.0

def TABLE_CAPTION_XML(caption: str) -> str:
    return f'\n```{{=openxml}}\n<w:p>\n  <w:pPr>\n    <w:pStyle w:val="Table Caption"/>\n  </w:pPr>\n  <w:r>\n    <w:t>{caption}</w:t>\n  </w:r>\n</w:p>\n```\n\n'

# === Парсинг аргументів ===
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", nargs="?", choices=["clear", "no-clear", "debug"], help="Очищення тимчасових файлів")
    return parser.parse_args()

# === Зчитування README.md та пошук .md файлів ===
def extract_md_files(path: Path) -> list:
    if not path.exists():
        print(f"Файл README.md не знайдено за шляхом: {path}", file=sys.stderr)
        sys.exit(1)

    with path.open("r", encoding="utf-8") as f:
        files = re.findall(r"\[.*?\]\((.*?\.md)\)", f.read())
    if not files:
        print("У README.md не знайдено посилань на файли Markdown!", file=sys.stderr)
        sys.exit(1)
    # Прибирання згадок .docx файлів
    files = [file for file in files if not file.endswith(".docx")]
    files = [file for file in files if not '.pdf' in str(file)]
    return files

# === Перевірка наявності файлів ===
def validate_files(files):
    missing = [file for file in files if not (script_dir / file).exists()]
    if missing:
        print(f"Наступні файли не знайдено: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    return [script_dir / file for file in files]

# === Тимчасові файли ===
def get_temp_name(file):
    return file.with_name(file.stem + "_temp" + file.suffix)

def delete_file(file):
    if file.exists():
        file.unlink()
        if DEBUG:
            print(f"Видалено файл: {file}")

def remove_temp_files(files):
    for file in files:
        delete_file(get_temp_name(file))
    delete_file(script_dir / "links_temp.md")

# === Парсинг посилань ===
def replace_links(content: str, links: list) -> str:
    # >>> посилання -> [0]
    # [text](url) посилання -> [1]
    pattern = re.compile(
        r'(?P<arrow>(^|\n)>>>\s*(?P<text1>[^\n]+))'
        r'|(?P<md>\[(?P<text2>[^\]]+)\]\((?P<url>https?://[^\s\)]+)\))',
        re.MULTILINE
    )

    result = []
    last_pos = 0

    for match in pattern.finditer(content):
        start, end = match.span()
        result.append(content[last_pos:start])

        if match.group('arrow'):
            text = match.group('text1').strip()
            entry = (">>>", text)
            if entry not in links:
                links.append(entry)
            index = links.index(entry)
            # Додаємо \n лише якщо було захоплено \n на початку
            if match.group(2) == '\n':
                result.append('\n')
            result.append(f"[{index+1}]")

        elif match.group('md'):
            text = match.group('text2')
            url = match.group('url')

            # якщо в кінці [ !] то приховати текст в content
            needHideText = text.endswith(' !')
            if needHideText:
                text = text[:-2].strip()
            entry = (text, url)
            if entry not in links:
                links.append(entry)
            index = links.index(entry)
            if needHideText:
                result.append(f"[{index+1}]")
            else:
                result.append(f"{text}[{index+1}]")

        last_pos = end

    result.append(content[last_pos:])
    return ''.join(result)


img_index_dict = {}
table_index_dict = {}
# === Парсинг зображень з шириною і вирівнюванням ===
def replace_images(content: str, file_i: int) -> str:
    global img_index_dict, table_index_dict
    # file_i = 1 -> 1, 2.1 -> 2 2.2 -> 2
    # Витягуємо основний номер розділу з file_i (наприклад, 2.1 -> 2)
    main_chapter = file_i.split('.')[0]
    if main_chapter not in img_index_dict:
        img_index_dict[main_chapter] = 0
    if main_chapter not in table_index_dict:
        table_index_dict[main_chapter] = 0
    def replacer(match):
        global img_index_dict, table_index_dict
        nonlocal main_chapter
        desc, path = match.groups()
        new_path = script_dir / path
        # OpenXML блок для центрування (перед зображенням)
        # Повна конструкція з вирівнюванням і фіксованою шириною
        img_width = IMG_WIDHT
        # Рис 1.1. Hack w=20 зберегти 20 в img_width і викинути з desc w=20 
        width_match = re.search(r'w=(\d+)', desc)
        if width_match:
            img_width = width_match.group(1) + '.0'
            desc = re.sub(r'\s*w=\d+', '', desc).strip()
        if 'Table:' in desc:
            table_index_dict[main_chapter] += 1
            img_index_dict[main_chapter] -= 1
            desc = desc.split('Table:')[1].strip()
            desc = f"Таблиця {main_chapter}.{table_index_dict[main_chapter]} {desc}."
            return f'{TABLE_CAPTION_XML(desc)} ![]({new_path}){{ width={img_width}cm }}'
        else:
            img_index_dict[main_chapter] += 1
            desc = f"Рис.{main_chapter}.{img_index_dict[main_chapter]} {desc}."
            return f"![{desc}]({new_path}){{ width={img_width}cm }}"
    return re.sub(r"!\[(.*?)\]\((.*?)\)", replacer, content)

def format_headers(content: str) -> str:
    def repl(match):
        hashes = match.group(1)
        text = match.group(2).strip()
        # Перевіряємо чи вже жирний і великими
        if text.startswith("**") and text.endswith("**") and text[2:-2].isupper():
            return match.group(0)
        # Робимо великими і жирними
        return f"{hashes} **{text.upper()}**"
    # Замінюємо лише якщо не закоментовано
    return re.sub(r'^(#{1,6})\s+([^\n]+)$', repl, content, flags=re.MULTILINE)

# === Обробка markdown-файлів ===
def process_markdown_files(files: list[Path], links: list) -> list:
    processed = []
    for i, file in enumerate(files):
        temp_file = get_temp_name(file)
        with file.open("r", encoding="utf-8") as f_in:
            content = f_in.read()
        content = replace_links(content, links)
        # file_index має отримуватись з назви файлу напркилад: ch1.md -> 1 ch2.1.md -> 2.1
        # Витягуємо file_index з назви файлу, наприклад ch1.md -> 1, ch2.1.md -> 2.1
        stem = file.stem
        match = re.search(r'ch([\d\.]+)', stem)
        file_index = match.group(1) if match else str(i + 1)
        content = replace_images(content, file_index)
        # content = format_headers(content)  # <--- Додаємо цю строку
        with temp_file.open("w", encoding="utf-8") as f_out:
            # Додаємо NEW_PAGE лише якщо перший рядок починається з одного #
            first_line = content.lstrip().splitlines()[0] if content.lstrip().splitlines() else ""
            if first_line.startswith("# ") and not first_line.startswith("##"):
                f_out.write(NEW_PAGE)
            f_out.write(content)
        processed.append(temp_file)
    return processed


def generate_link_list(links: list) -> Path:
    if not links: return None
    # Додаємо посилання на архів проєкту у форматі Markdown
    links.append(("Архів проєкту КПК","https://github.com/Bogd-an/Diplom"))
    out = script_dir / "links_temp.md"
    with out.open("w", encoding="utf-8") as f:
        f.write(NEW_PAGE)
        f.write("# **СПИСОК ВИКОРИСТАНИХ ДЖЕРЕЛ**\n")
        for i, link in enumerate(links):
            text, url = link
            # Визначаємо текст опису
            if '>>>' in text:
                f.write(f"[{i+1}] {url}\n\n")
            else:
                # Для http-посилань просто текст — сам URL
                f.write(f"[{i+1}] {text}, [Електронний ресурс] URL: {url} (дата звернення: 10.05.2024)\n\n")
    return out

# === Виклик Pandoc ===
def convert_to_docx(input_files: list[Path], output: Path):
    cmd = ["pandoc", f"--reference-doc={template_docx}", "--from=markdown", "--to=docx"]
    cmd += [str(f) for f in input_files]
    cmd += ["-o", str(output)]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if DEBUG:
        print("Команда:", " ".join(cmd))
        for line in result.stderr.splitlines():
            if "[WARNING]" in line:
                match = re.search(r"Could not fetch resource '([^']+)'", line)
                if match:
                    print(f"WARNING: {Path(match.group(1)).name}")

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise subprocess.CalledProcessError(result.returncode, cmd)
    print(f"Файл {output} успішно створено!")

def update_readme_with_toc(md_paths: list[Path], readme_path: Path):
    toc_lines = [
                 '[Завантажити DOCX](https://github.com/Bogd-an/Diplom/raw/refs/heads/main/docs/out/doc_dev.docx)\n',
                 '[Github](https://github.com/Bogd-an/Diplom/blob/main/docs/README.md)\n',
                 "---\n",
                 "Зміст:\n"]
    ref_dict = {}
    ref_counter = 1
    levels = [0] * 6  # до 6 рівнів

    for md_file in md_paths:
        with md_file.open("r", encoding="utf-8") as f:
            inside_comment = False
            for line in f:
                # Визначаємо, чи ми всередині коментаря
                if "<!--" in line:
                    inside_comment = True
                if "-->" in line:
                    inside_comment = False
                    continue
                if inside_comment:
                    continue
                # Пропускаємо закоментовані заголовки
                if line.strip().startswith("<!--") or line.strip().endswith("-->"):
                    continue
                if line.startswith("#"):
                    header_level = len(line) - len(line.lstrip("#"))
                    header_text = line.strip("#").strip()
                    anchor = header_text.lower().replace(" ", "-")
                    header_text = header_text.replace("**", "")
                    ref_key = f"ref{ref_counter}"
                    ref_url = f"{md_file.name}#{anchor}"
                    ref_dict[ref_key] = ref_url

                    levels[header_level - 1] += 1
                    for i in range(header_level, len(levels)):
                        levels[i] = 0
                    num = ".".join(str(levels[i]) for i in range(header_level) if levels[i] > 0)
                    indent = " " * (header_level - 2)
                    toc_lines.append(f"\n{indent} {'#'*header_level} [{num} {header_text}][{ref_key}]")
                    ref_counter += 1

    toc_lines.append("\n<!-- Links -->")
    for key, url in ref_dict.items():
        toc_lines.append(f"[{key}]: {url}")

    with readme_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(toc_lines) + "\n")

# === Основна функція ===
def main():
    args = parse_args()
    if args.mode == "debug":
        global DEBUG
        DEBUG = True
        print("DEBUG mode is ON")
    
    md_files = extract_md_files(content_path)
    md_paths = validate_files(md_files)

    if args.mode == "clear":
        remove_temp_files(md_paths)
        print("Тимчасові файли видалено.")
        return

    links = []
    temp_files = process_markdown_files(md_paths, links)

    links_file = generate_link_list(links)
    if links_file:
        temp_files.append(links_file)

    # ОНОВЛЕННЯ README.md ЗІ ЗМІСТОМ
    update_readme_with_toc(md_paths, readme_path)

    try:
        convert_to_docx(temp_files, ms2docx)
    except subprocess.CalledProcessError:
        sys.exit(1)

    if args.mode != "no-clear":
        remove_temp_files(md_paths)

if __name__ == "__main__":
    main()