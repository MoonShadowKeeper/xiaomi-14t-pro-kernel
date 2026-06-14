# Xiaomi 14T Pro GKI Kernel

<p align="center">
  <b>SukiSU Ultra · SUSFS v2.1.0 · KPM · Baseband Guard · GKI 6.1.138</b><br>
  <sub>Кастомное GKI-ядро для Xiaomi 14T Pro / rothko на базе Android 14 GKI 2025-06</sub>
</p>

<p align="center">
  <img alt="Kernel" src="https://img.shields.io/badge/kernel-6.1.138-blue">
  <img alt="Device" src="https://img.shields.io/badge/device-Xiaomi%2014T%20Pro%20(rothko)-orange">
  <img alt="Root" src="https://img.shields.io/badge/root-SukiSU%20Ultra-red">
  <img alt="SUSFS" src="https://img.shields.io/badge/SUSFS-v2.1.0-purple">
  <img alt="Build" src="https://img.shields.io/badge/build-Bazel%20%2F%20Kleaf-green">
</p>

---

## О проекте

Это кастомное **GKI-ядро** для **Xiaomi 14T Pro (`rothko`)**.

База ядра выбрана не случайно: используется тот же Android Common Kernel таргет, на котором работают совместимые GKI-сборки для этого устройства.

```text
Android Common Kernel: common-android14-6.1-2025-06
Kernel version:        6.1.138
Build system:          Bazel / Kleaf
Target:                //common:kernel_aarch64_dist
Device:                Xiaomi 14T Pro / rothko
```

Главная цель сборки — получить рабочее GKI-ядро с root-функциями, скрытием root, защитой критичных разделов, улучшенной сетью, ZRAM, поддержкой дополнительных файловых систем и современными механизмами управления памятью.

---

## Что добавлено в ядро

| Фича | Статус | Что даёт |
|---|---:|---|
| **SukiSU Ultra** | ✅ | Root на уровне ядра, форк KernelSU с дополнительными возможностями |
| **SUSFS v2.1.0** | ✅ | Скрытие root-следов, mount points, подозрительных путей и spoof системной информации |
| **KPM** | ✅ | Поддержка Kernel Plugin Module для расширений ядра |
| **Baseband Guard (BBG)** | ✅ | Защита критичных разделов от опасной записи из системы |
| **BBR + FQ** | ✅ | Улучшенный TCP congestion control для более стабильной сети |
| **WireGuard** | ✅ | Поддержка WireGuard VPN прямо в ядре |
| **ZRAM + ZSTD** | ✅ | Более эффективный сжатый swap в RAM |
| **NTFS3** | ✅ | Поддержка NTFS через in-kernel драйвер |
| **ExFAT** | ✅ | Поддержка ExFAT-накопителей |
| **MGLRU** | ✅ | Более современный механизм освобождения памяти |
| **DAMON** | ✅ | Мониторинг и оптимизация работы памяти |
| **TEO Governor** | ✅ | Более современный CPU idle governor |
| **TMPFS XATTR / POSIX ACL** | ✅ | Лучше совместимость с Mountify и tmpfs-монтированиями |

---

## SukiSU Ultra

**SukiSU Ultra** — это root-решение на уровне ядра, основанное на KernelSU.

В отличие от классического root через boot/ramdisk, KernelSU-подход работает глубже: root-доступ контролируется ядром. Это даёт лучшую интеграцию, меньше лишних userspace-костылей и больше возможностей для продвинутых функций.

Включено:

```text
CONFIG_KSU=y
CONFIG_KPM=y
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
```

---

## KPM

**KPM (Kernel Plugin Module)** — это система плагинов для ядра.

Она позволяет использовать дополнительные kernel-level расширения, которым нужен доступ к символам ядра. Поэтому вместе с KPM включены:

```text
CONFIG_KPM=y
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
```

Если коротко: KPM нужен для более продвинутых модулей SukiSU Ultra.

---

## SUSFS v2.1.0

**SUSFS** — это набор патчей для скрытия root-следов и подмены части системной информации.

Версия в сборке:

```c
#define SUSFS_VERSION "v2.1.0"
```

Что включено:

| Возможность | Что делает |
|---|---|
| **SUS_PATH** | Скрывает подозрительные пути, по которым приложения могут искать root |
| **SUS_MOUNT** | Скрывает mount points, связанные с root/модулями |
| **SUS_KSTAT** | Подменяет kernel stat-информацию |
| **SUS_MAP** | Защищает и скрывает подозрительные memory mappings |
| **SPOOF_UNAME** | Подменяет данные, которые возвращает `uname` |
| **SPOOF_CMDLINE** | Подменяет boot cmdline / bootconfig |
| **OPEN_REDIRECT** | Позволяет перенаправлять обращения к файлам |
| **HIDE_SYMBOLS** | Скрывает символы KSU/SUSFS в ядре |
| **ENABLE_LOG** | Включает логирование SUSFS |

Конфиги:

```text
CONFIG_KSU_SUSFS=y
CONFIG_KSU_SUSFS_SUS_PATH=y
CONFIG_KSU_SUSFS_SUS_MOUNT=y
CONFIG_KSU_SUSFS_SUS_KSTAT=y
CONFIG_KSU_SUSFS_SUS_MAP=y
CONFIG_KSU_SUSFS_SPOOF_UNAME=y
CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG=y
CONFIG_KSU_SUSFS_OPEN_REDIRECT=y
CONFIG_KSU_SUSFS_ENABLE_LOG=y
CONFIG_KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS=y
```

SUSFS хранится локально в репозитории (`deps/susfs`), чтобы сборка не зависела от внешнего репозитория во время билда.

---

## Baseband Guard (BBG)

**Baseband Guard** — это LSM-модуль, который защищает важные разделы устройства от опасной записи.

Главная идея: не дать вредоносному скрипту, модулю или приложению случайно или намеренно повредить критичные разделы, связанные с boot/baseband/прошивкой.

Включено:

```text
CONFIG_BBG=y
CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,integrity,selinux,smack,tomoyo,apparmor,bpf,baseband_guard"
```

`baseband_guard` добавлен в `CONFIG_LSM`, потому что без этого BBG не активируется как полноценный Linux Security Module.

---

## Сеть

В ядре включены стабильные сетевые улучшения:

```text
CONFIG_TCP_CONG_BBR=y
CONFIG_NET_SCH_FQ=y
CONFIG_DEFAULT_TCP_CONG="bbr"
CONFIG_WIREGUARD=y
```

### BBR + FQ

**BBR** — TCP congestion control от Google. Он помогает сети держать более стабильную скорость и задержку, особенно на мобильных сетях и Wi‑Fi.

**FQ** нужен как qdisc, с которым BBR работает корректнее.

### WireGuard

**WireGuard** — современный VPN-протокол. Поддержка в ядре обычно быстрее и чище, чем userspace-реализация.

BBRv3 намеренно не добавлен: он не входит в стандартное GKI 6.1 и требует дополнительных патчей с высоким риском конфликтов.

---

## Память и производительность

### ZRAM + ZSTD

```text
CONFIG_ZRAM=m
CONFIG_ZRAM_DEF_COMP_ZSTD=y
CONFIG_ZRAM_DEF_COMP="zstd"
CONFIG_ZSMALLOC=m
```

**ZRAM** создаёт сжатый swap в оперативной памяти. Это помогает системе дольше держать приложения в памяти и меньше упираться в нехватку RAM.

**ZSTD** — быстрый и эффективный алгоритм сжатия. Обычно даёт хороший баланс скорости и степени сжатия.

ZRAM и ZSMALLOC оставлены модулями (`=m`), потому что GKI ожидает `zram.ko` и `zsmalloc.ko` как отдельные модули.

### MGLRU

```text
CONFIG_LRU_GEN=y
CONFIG_LRU_GEN_ENABLED=y
CONFIG_LRU_GEN_STATS=y
```

**MGLRU (Multi-Generational LRU)** — более современный алгоритм управления памятью. Он помогает ядру умнее решать, какие страницы памяти выгружать первыми.

На практике это может дать более плавную многозадачность и меньше агрессивных выгрузок приложений.

### DAMON

```text
CONFIG_DAMON=y
CONFIG_DAMON_VADDR=y
CONFIG_DAMON_PADDR=y
CONFIG_DAMON_SYSFS=y
CONFIG_DAMON_RECLAIM=y
CONFIG_DAMON_LRU_SORT=y
```

**DAMON (Data Access MONitor)** отслеживает, как реально используется память, и помогает ядру принимать более точные решения по reclaim/LRU.

В сборке включены DAMON reclaim и DAMON LRU sort.

### TEO Governor

```text
CONFIG_CPU_IDLE_GOV_TEO=y
```

**TEO Governor** — CPU idle governor, который помогает процессору эффективнее уходить в idle-состояния. Это может положительно влиять на энергопотребление без грубого вмешательства в частоты.

---

## Файловые системы

```text
CONFIG_NTFS3_FS=y
CONFIG_NTFS3_LZX_XPRESS=y
CONFIG_NTFS3_FS_POSIX_ACL=y
CONFIG_EXFAT_FS=y
CONFIG_TMPFS_XATTR=y
CONFIG_TMPFS_POSIX_ACL=y
```

### NTFS3

**NTFS3** — in-kernel драйвер NTFS. Нужен для нормальной работы с NTFS-накопителями без FUSE-костылей.

### ExFAT

**ExFAT** нужен для флешек, карт памяти и внешних накопителей, которые часто форматируются именно в ExFAT.

### TMPFS XATTR / POSIX ACL

Эти опции улучшают совместимость tmpfs-монтирований, в том числе для сценариев вроде Mountify.

---

## Совместимость с WildKernels GKI

Сборка выровнена по рабочему подходу WildKernels для GKI:

- база: `common-android14-6.1-2025-06`
- kernel sublevel: `6.1.138`
- сборка через Bazel/Kleaf
- `--config=fast`
- `--config=stamp`
- clean dirty flags, чтобы не получить `-maybe-dirty` в версии ядра
- remove protected exports для совместимости с vendor-модулями
- упаковка через WildKernels AnyKernel3 `gki-2.0`

Это важно: vendor-модули на устройстве чувствительны к версии ядра и vermagic. Поэтому сборка держится на 6.1.138/2025-06, а не на плавающем HEAD.

---

## Артефакты сборки

Workflow выгружает два основных артефакта:

| Артефакт | Что внутри |
|---|---|
| `AnyKernel3-Xiaomi14TPro-GKI6.1.138-*` | Готовый flashable AnyKernel3-пакет |
| `boot-images-*` | `boot.img`, `boot-lz4.img`, `boot-gz.img`, raw `Image`, `build.log` |

AnyKernel3 выгружается без вложенного zip-архива, чтобы его было удобнее скачивать и прошивать.

---

## Credits

- Google Android Common Kernel
- SukiSU Ultra
- SUSFS by simonpunk
- Baseband Guard by vc-teahouse
- AnyKernel3 by osm0sis
- WildKernels GKI workflow patterns
