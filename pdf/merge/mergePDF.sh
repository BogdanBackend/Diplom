#!/bin/bash

# chmod +x mergePDF.sh

# Встановлення poppler-utils (якщо потрібно)
if ! dpkg -s poppler-utils >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y poppler-utils
fi

# Перехід у директорію з PDF
cd "$(dirname "$0")/.."


echo "Об'єднання PDF файлів у один документ..."

pdfunite \
    doc.pdf \
    A4/Специфікація.pdf \
    A4/Cover.pdf \
    A4/Top.pdf \
    A1/Box.pdf \
    A1/Assem.pdf \
    A1/CM5IO.pdf \
    A1/A1_experiment.drawio.pdf \
    A1/PCB.pdf \
    A4/Plagiarism.pdf \
    merge/Diplom2025.pdf

echo "Готово! Всі PDF об'єднано у файл $(dirname "$0")/Diplom2025.pdf"