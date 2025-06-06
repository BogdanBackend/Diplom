@echo off
setlocal

:: Встановлюємо BASE як абсолютний шлях до папки, де знаходиться скрипт
set "BASE=%~dp0"

:: Видаляємо фінальний бекслеш, якщо треба — не обов'язково, можна лишити
:: set "BASE=%BASE:~0,-1%"

mklink pdf\A1_Assem.pdf %BASE%model\Assem.pdf
mklink pdf\A1_Box.pdf %BASE%model\Box.pdf
mklink pdf\A4_Cover.pdf %BASE%model\Cover.pdf
mklink pdf\A4_Top.pdf %BASE%model\Top.pdf

mklink pdf\A4_specification.pdf %BASE%msDocx\specification.doc

mklink pdf\A1_CM5IO.pdf %BASE%motherBoard\Out\CM5IO.pdf
mklink pdf\A1_PCB.pdf %BASE%motherBoard\Out\pcb\PCB.pdf

mklink pdf\A1_experiment.drawio.pdf %BASE%msDocx\A1_experiment.drawio.pdf
