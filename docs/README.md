[Завантажити DOCX](https://github.com/Bogd-an/Diplom/raw/refs/heads/main/docs/out/doc_dev.docx)

[Github](https://github.com/Bogd-an/Diplom/blob/main/docs/README.md)

---

Зміст:


 # [1 Вступ][ref1]

 # [2 ОГЛЯД ІСНУЮЧИХ РОЗРОБОК][ref2]

  ## [2.1 Радіостанція Hack RF One Portapack H4 Mayhem SDR 1 МГц – 6 ГГц.][ref3]

  ## [2.2 Радіостанція Libre SDR PLUTO з Zynq 7020 70 МГц – 6 ГГц.][ref4]

  ## [2.3 Радіостанція 1.10D DSP SDR 10 МГц-2 ГГц][ref5]

  ## [2.4 Радіостанція Amator SDR  1 МГц - 6 ГГц.][ref6]

  ## [2.5 Malahit DSP2 SDR Radio Firmware 2.40 Genuine Second Generation Receiver 10 кГц - 2 ГГц.][ref7]

  ## [2.6 Висновок по розділу][ref8]

 # [3 РОЗРОБКА ТЕХНІЧНОГО ЗАВДАННЯ][ref9]

  ## [3.1 Висновок по розділу][ref10]

 # [4 Розробка структурної схеми][ref11]

  ## [4.1 Опис роботи системи][ref12]

  ## [4.2 Висновок][ref13]

 # [5 Підбір елементної бази][ref14]

  ## [5.1 Антени][ref15]

  ## [5.2 Пристрій захоплення радіосигналу][ref16]

   ### [5.2.1 HackRF-One][ref17]

   ### [5.2.2 RTL-SDR v3][ref18]

   ### [5.2.3 LimeSDR Mini v2][ref19]

   ### [5.2.4 BladeRF 2.0 micro xA4 SDR трансівер 47 МГц-6 ГГц 49 КЛЕ ПЛІС][ref20]

  ## [5.3 Центральне ядро обчислень][ref21]

   ### [5.3.1 Raspberry Pi Compute Module 4][ref22]

   ### [5.3.2 NVIDIA Jetson Nano][ref23]

   ### [5.3.3 Radxa CM3][ref24]

   ### [5.3.4 Banana Pi BPI-CM4][ref25]

  ## [5.4 Пристрій захоплення аналогового відеосигналу][ref26]

   ### [5.4.1 USB карта відеозахоплення LUX EasyCap][ref27]

   ### [5.4.2 Digitnow USB 2.0 Video Capture Card][ref28]

  ## [5.5 Пристрій геопозиціонування][ref29]

   ### [5.5.1 GPS модуль NEO-6M v2][ref30]

   ### [5.5.2 u-blox NEO-M8N][ref31]

   ### [5.5.3 Quectel L86 GPS/GNSS модуль][ref32]

  ## [5.6 Пристрій збереження данних][ref33]

   ### [5.6.1 SSD диск Transcend MTS420S 240GB M.2 2242 SATAIII 3D NAND TLC][ref34]

   ### [5.6.2 KingSpec M.2 2242 SATAIII 256GB][ref35]

   ### [5.6.3 ADATA SU650 M.2 2280 SATAIII 240GB][ref36]

  ## [5.7 Дисплей][ref37]

   ### [5.7.1 Сенсорний дисплей IBM Lenovo Wacom 12.1in XGA LCD Touch Screen][ref38]

   ### [5.7.2 Waveshare 10.1" HDMI LCD with Capacitive Touch][ref39]

   ### [5.7.3 Official Raspberry Pi 7" Touchscreen Display][ref40]

  ## [5.8 Батарея][ref41]

   ### [5.8.1 Принцип роботи][ref42]

   ### [5.8.2 Типи та різновиди][ref43]

  ## [5.9 Материнська плата][ref44]

   ### [5.9.1 Compute Module 4 IO Board][ref45]

   ### [5.9.2 Waveshare CM4 IO Base Board B][ref46]

   ### [5.9.3 Seeed Studio reComputer CM4 IO Board][ref47]

  ## [5.10 Висновок по розділу][ref48]

 # [6 Розробка принципової схеми][ref49]

 # [7 Розробка корпусу][ref50]

  ## [7.1 Деталі корпусу][ref51]

   ### [7.1.1 Корпус][ref52]

   ### [7.1.2 Захисна кришка з органічного скла][ref53]

  ## [7.2 Симуляція навантаження][ref54]

   ### [7.2.1 Навантаження зверху на захисне органічне скло екрану][ref55]

   ### [7.2.2 Бічне навантаження][ref56]

   ### [7.2.3 Бічне навантаження][ref57]

 # [8 Документація, користувацький інтерфейс, інструкція][ref58]

 # [9 Автономність][ref59]

 # [10 Принцип роботи (фізичний та алгоритмічний)][ref60]

<!-- Links -->
[ref1]: chapter1.md#вступ
[ref2]: chapter2.md#огляд-існуючих-розробок
[ref3]: chapter2.md#радіостанція-hack-rf-one-portapack-h4-mayhem-sdr-1-мгц-–-6-ггц.
[ref4]: chapter2.md#радіостанція-libre-sdr-pluto-з-zynq-7020-70-мгц-–-6-ггц.
[ref5]: chapter2.md#радіостанція-1.10d-dsp-sdr-10-мгц-2-ггц
[ref6]: chapter2.md#радіостанція-amator-sdr--1-мгц---6-ггц.
[ref7]: chapter2.md#malahit-dsp2-sdr-radio-firmware-2.40-genuine-second-generation-receiver-10-кгц---2-ггц.
[ref8]: chapter2.md#висновок-по-розділу
[ref9]: chapter3.md#розробка-технічного-завдання
[ref10]: chapter3.md#висновок-по-розділу
[ref11]: chapter4.md#розробка-структурної-схеми
[ref12]: chapter4.md#опис-роботи-системи
[ref13]: chapter4.md#висновок
[ref14]: chapter5.md#підбір-елементної-бази
[ref15]: chapter5.md#антени
[ref16]: chapter5.md#пристрій-захоплення-радіосигналу
[ref17]: chapter5.md#hackrf-one
[ref18]: chapter5.md#rtl-sdr-v3
[ref19]: chapter5.md#limesdr-mini-v2
[ref20]: chapter5.md#bladerf-2.0-micro-xa4-sdr-трансівер-47-мгц-6-ггц-49-кле-пліс
[ref21]: chapter5.md#центральне-ядро-обчислень
[ref22]: chapter5.md#raspberry-pi-compute-module-4
[ref23]: chapter5.md#nvidia-jetson-nano
[ref24]: chapter5.md#radxa-cm3
[ref25]: chapter5.md#banana-pi-bpi-cm4
[ref26]: chapter5.md#пристрій-захоплення-аналогового-відеосигналу
[ref27]: chapter5.md#usb-карта-відеозахоплення-lux-easycap
[ref28]: chapter5.md#digitnow-usb-2.0-video-capture-card
[ref29]: chapter5.md#пристрій-геопозиціонування
[ref30]: chapter5.md#gps-модуль-neo-6m-v2
[ref31]: chapter5.md#u-blox-neo-m8n
[ref32]: chapter5.md#quectel-l86-gps/gnss-модуль
[ref33]: chapter5.md#пристрій-збереження-данних
[ref34]: chapter5.md#ssd-диск-transcend-mts420s-240gb-m.2-2242-sataiii-3d-nand-tlc
[ref35]: chapter5.md#kingspec-m.2-2242-sataiii-256gb
[ref36]: chapter5.md#adata-su650-m.2-2280-sataiii-240gb
[ref37]: chapter5.md#дисплей
[ref38]: chapter5.md#сенсорний-дисплей-ibm-lenovo-wacom-12.1in-xga-lcd-touch-screen
[ref39]: chapter5.md#waveshare-10.1"-hdmi-lcd-with-capacitive-touch
[ref40]: chapter5.md#official-raspberry-pi-7"-touchscreen-display
[ref41]: chapter5.md#батарея
[ref42]: chapter5.md#принцип-роботи
[ref43]: chapter5.md#типи-та-різновиди
[ref44]: chapter5.md#материнська-плата
[ref45]: chapter5.md#compute-module-4-io-board
[ref46]: chapter5.md#waveshare-cm4-io-base-board-b
[ref47]: chapter5.md#seeed-studio-recomputer-cm4-io-board
[ref48]: chapter5.md#висновок-по-розділу
[ref49]: chapter6.md#розробка-принципової-схеми
[ref50]: chapter7.md#розробка-корпусу
[ref51]: chapter7.md#деталі-корпусу
[ref52]: chapter7.md#корпус
[ref53]: chapter7.md#захисна-кришка-з-органічного-скла
[ref54]: chapter7.md#симуляція-навантаження
[ref55]: chapter7.md#навантаження-зверху-на-захисне-органічне-скло-екрану
[ref56]: chapter7.md#бічне-навантаження
[ref57]: chapter7.md#бічне-навантаження
[ref58]: chapter8.md#документація,-користувацький-інтерфейс,-інструкція
[ref59]: chapter9.md#автономність
[ref60]: chapter10.md#принцип-роботи-(фізичний-та-алгоритмічний)
