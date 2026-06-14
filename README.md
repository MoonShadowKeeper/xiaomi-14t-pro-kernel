# Xiaomi 14T Pro Wild GKI Kernel

<p align="center">
  <b>KernelSU-Next · SUSFS v2.1.0 · Baseband Guard · DroidSpaces · Wild GKI 6.1.138</b><br>
  <sub>Кастомное GKI-ядро для Xiaomi 14T Pro / rothko на базе Android 14 GKI 2025-06</sub>
</p>

<p align="center">
  <img alt="Kernel" src="https://img.shields.io/badge/kernel-6.1.138-blue">
  <img alt="Device" src="https://img.shields.io/badge/device-Xiaomi%2014T%20Pro%20(rothko)-orange">
  <img alt="Root" src="https://img.shields.io/badge/root-KernelSU--Next-red">
  <img alt="SUSFS" src="https://img.shields.io/badge/SUSFS-v2.1.0-purple">
  <img alt="Build" src="https://img.shields.io/badge/build-Bazel%20%2F%20Kleaf-green">
</p>

---

## О проекте

Это кастомное **GKI-ядро** для **Xiaomi 14T Pro (`rothko`)**.

Текущая база: **WildKernels FULL** на **KernelSU-Next `dev-susfs`**. Сборка повторяет рабочую логику WildKernels GKI, затем добавляет дополнительные фичи для памяти, файловых систем и idle governor.

```text
Android Common Kernel: common-android14-6.1-2025-06
Kernel version:        6.1.138
Runtime uname:         6.1.138-android14-Wild
Root:                  KernelSU-Next dev-susfs
Build system:          Bazel / Kleaf
Target:                //common:kernel_aarch64_dist
Device:                Xiaomi 14T Pro / rothko
```

Главная цель сборки: сохранить рабочую совместимость WildKernels с vendor-модулями Xiaomi, включая Wi-Fi и Bluetooth, и добавить нужные фичи без ухода на нестабильный ACK HEAD.

---

## Что добавлено в ядро

| Фича | Статус | Что даёт |
|---|---:|---|
| **KernelSU-Next** | ✅ | Root на уровне ядра, ветка `dev-susfs` как в WildKernels |
| **SUSFS v2.1.0+** | ✅ | Скрытие root-следов, mount points, подозрительных путей и spoof системной информации |
| **Baseband Guard (BBG)** | ✅ | Защита критичных разделов от опасной записи из системы |
| **DroidSpaces-OSS** | ✅ | IPC / namespace совместимость для контейнерных сценариев |
| **Wild branding** | ✅ | Версия ядра приводится к `6.1.138-android14-Wild` |
| **Module version bypass** | ✅ | Vendor-модули грузятся даже при чувствительном vermagic |
| **Networking FULL** | ✅ | ipset, netfilter extras, BBR, FQ, FQ_CODEL, WireGuard |
| **ZRAM + ZSTD** | ✅ | Более эффективный сжатый swap в RAM |
| **NTFS3** | ✅ | Поддержка NTFS через in-kernel драйвер |
| **ExFAT** | ✅ | Поддержка ExFAT-накопителей |
| **MGLRU** | ✅ | Более современный механизм освобождения памяти |
| **DAMON** | ✅ | Мониторинг и оптимизация работы памяти |
| **TEO Governor** | ✅ | Более современный CPU idle governor |
| **TMPFS XATTR / POSIX ACL** | ✅ | Лучше совместимость с tmpfs-монтированиями |

> KPM в этой ветке не включён. KernelSU-Next baseline его не использует. Для KPM нужна отдельная SukiSU Ultra сборка.

---

## KernelSU-Next

**KernelSU-Next** используется как root-слой текущей Wild-сборки.

Источник setup-скрипта:

```text
https://raw.githubusercontent.com/pershoot/KernelSU-Next/dev-susfs/kernel/setup.sh
```

В workflow используется ref:

```text
KSUN_REF=dev-susfs
```

Базовые конфиги:

```text
CONFIG_KSU=y
CONFIG_KSU_MANUAL_HOOK=y
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
```

Workflow также подтягивает WildKernels `static.patch` для KernelSU-Next. Если патч не применяется чисто к текущему дереву, сборка не падает, но пишет warning.

---

## SUSFS v2.1.0+

**SUSFS** добавляет root hiding и spoof-механизмы поверх KernelSU-Next.

Что включено:

| Возможность | Что делает |
|---|---|
| **SUS_PATH** | Скрывает подозрительные пути, по которым приложения могут искать root |
| **SUS_MOUNT** | Скрывает mount points, связанные с root/модулями |
| **SUS_KSTAT** | Подменяет kernel stat-информацию |
| **SUS_OVERLAYFS** | Добавляет совместимость SUSFS с overlayfs-сценариями |
| **SUS_MAP** | Защищает и скрывает подозрительные memory mappings |
| **SPOOF_UNAME** | Подменяет данные, которые возвращает `uname` |
| **SPOOF_CMDLINE** | Подменяет boot cmdline / bootconfig |
| **OPEN_REDIRECT** | Позволяет перенаправлять обращения к файлам |
| **HIDE_SYMBOLS** | Скрывает символы KSU/SUSFS в ядре |
| **MAGIC_MOUNT** | Включает совместимость с magic mount |

Конфиги:

```text
CONFIG_KSU_SUSFS=y
CONFIG_KSU_SUSFS_SUS_PATH=y
CONFIG_KSU_SUSFS_SUS_MOUNT=y
CONFIG_KSU_SUSFS_SUS_KSTAT=y
CONFIG_KSU_SUSFS_SUS_OVERLAYFS=y
CONFIG_KSU_SUSFS_SUS_MAP=y
CONFIG_KSU_SUSFS_SPOOF_UNAME=y
CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG=y
CONFIG_KSU_SUSFS_OPEN_REDIRECT=y
CONFIG_KSU_SUSFS_ENABLE_LOG=y
CONFIG_KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS=y
CONFIG_KSU_SUSFS_HAS_MAGIC_MOUNT=y
```

SUSFS хранится локально в репозитории (`deps/susfs`), чтобы сборка не зависела от внешнего репозитория во время билда.

---

## Baseband Guard (BBG)

**Baseband Guard**: LSM-модуль для защиты критичных разделов устройства от опасной записи.

Включено:

```text
CONFIG_BBG=y
CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,integrity,selinux,smack,tomoyo,apparmor,bpf,baseband_guard"
```

`baseband_guard` добавлен в `CONFIG_LSM`, иначе BBG не активируется как полноценный Linux Security Module.

---

## DroidSpaces-OSS

Workflow применяет патч DroidSpaces-OSS:

```text
001.GKI-below-6.12-fix_sysvipc_kabi_6_7_8.patch
```

Конфиги:

```text
CONFIG_PID_NS=y
CONFIG_SYSVIPC=y
CONFIG_POSIX_MQUEUE=y
CONFIG_IPC_NS=y
CONFIG_DEVTMPFS=y
CONFIG_BINFMT_MISC=y
CONFIG_BINFMT_SCRIPT=y
CONFIG_BINFMT_ELF=y
```

Это повторяет WildKernels FULL и помогает сценариям, где нужны IPC, namespaces и контейнерная совместимость.

---

## Сеть

Сетевой набор взят из WildKernels FULL и дополнен WireGuard:

```text
CONFIG_IP_SET=y
CONFIG_IP_SET_MAX=65534
CONFIG_NETFILTER_XT_MATCH_ADDRTYPE=y
CONFIG_NETFILTER_XT_SET=y
CONFIG_NETFILTER_XT_TARGET_LOG=y
CONFIG_NETFILTER_XT_MATCH_RECENT=y
CONFIG_IP6_NF_NAT=y
CONFIG_IP6_NF_TARGET_MASQUERADE=y
CONFIG_TCP_CONG_ADVANCED=y
CONFIG_TCP_CONG_BBR=y
CONFIG_DEFAULT_BBR=y
CONFIG_DEFAULT_TCP_CONG="bbr"
CONFIG_NET_SCH_FQ=y
CONFIG_NET_SCH_FQ_CODEL=y
CONFIG_WIREGUARD=y
```

**BBR + FQ** помогают держать стабильную скорость и задержку, особенно на мобильных сетях и Wi-Fi.

**WireGuard** даёт поддержку VPN прямо в ядре.

BBRv3 не добавлен: для GKI 6.1 он требует отдельные патчи и повышает риск конфликтов.

---

## Память и производительность

### ZRAM + ZSTD

```text
CONFIG_ZSMALLOC=m
CONFIG_ZRAM=m
CONFIG_ZSTD_COMPRESS=y
CONFIG_ZSTD_DECOMPRESS=y
CONFIG_ZRAM_DEF_COMP_ZSTD=y
CONFIG_ZRAM_DEF_COMP="zstd"
```

ZRAM и ZSMALLOC оставлены модулями (`=m`), потому что GKI ожидает `zram.ko` и `zsmalloc.ko` как отдельные модули.

### MGLRU

```text
CONFIG_LRU_GEN=y
CONFIG_LRU_GEN_ENABLED=y
CONFIG_LRU_GEN_STATS=y
```

**MGLRU (Multi-Generational LRU)** помогает ядру точнее решать, какие страницы памяти выгружать первыми.

### DAMON

```text
CONFIG_DAMON=y
CONFIG_DAMON_VADDR=y
CONFIG_DAMON_PADDR=y
CONFIG_DAMON_SYSFS=y
CONFIG_DAMON_RECLAIM=y
CONFIG_DAMON_LRU_SORT=y
```

**DAMON (Data Access MONitor)** отслеживает реальные паттерны доступа к памяти и помогает reclaim/LRU-механизмам.

### TEO Governor

```text
CONFIG_CPU_IDLE_GOV_TEO=y
```

**TEO Governor**: CPU idle governor, который помогает процессору эффективнее уходить в idle-состояния.

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

**NTFS3**: in-kernel драйвер NTFS для внешних накопителей без FUSE-костылей.

**ExFAT**: поддержка флешек, карт памяти и внешних накопителей в ExFAT.

**TMPFS XATTR / POSIX ACL**: совместимость для tmpfs-монтирований и похожих сценариев.

---

## Совместимость с WildKernels GKI

Сборка выровнена по рабочему подходу WildKernels:

- база: `common-android14-6.1-2025-06`
- kernel sublevel: `6.1.138`
- runtime версия: `6.1.138-android14-Wild`
- root: `KernelSU-Next dev-susfs`
- сборка: Bazel/Kleaf
- флаги: `--config=fast`, `--config=stamp`
- фикс timestamp: `2025-06-05 04:20:00 UTC`
- clean dirty flags
- remove protected exports
- module version bypass в `kernel/module/version.c`
- упаковка через WildKernels AnyKernel3 `gki-2.0`

Зачем это нужно: vendor-модули Xiaomi чувствительны к версии ядра и vermagic. Если уйти в строку вроде `6.1.138-android14-11-g...`, ядро может загрузиться, но Wi-Fi/Bluetooth отвалятся. Wild branding и module bypass держат совместимость ближе к рабочей WildKernels сборке.

---

## Артефакты сборки

Workflow выгружает два основных артефакта:

| Артефакт | Что внутри |
|---|---|
| `AnyKernel3-Xiaomi14TPro-Wild-KSUN-*` | Готовый flashable AnyKernel3-пакет |
| `boot-images-*` | `boot.img`, `boot-lz4.img`, `boot-gz.img`, raw `Image`, `build.log` |

ZIP внутри workflow называется:

```text
KernelSU-Next_Wild_Xiaomi14TPro_GKI6.1.138_<date>.zip
```

AnyKernel3 выгружается без вложенного zip-архива, чтобы его было удобнее скачивать и прошивать.

---

## Текущий статус

Текущий workflow переключён на **Wild KernelSU-Next FULL plus extras**.

Тестовая цель: сначала подтвердить, что Wi-Fi и Bluetooth работают как на WildKernels, затем уже решать, какие дополнительные фичи оставлять постоянно.

---

## Credits

- Google Android Common Kernel
- KernelSU-Next
- SUSFS by simonpunk
- Baseband Guard by vc-teahouse
- DroidSpaces-OSS by ravindu644
- AnyKernel3 by osm0sis / WildKernels `gki-2.0`
- WildKernels GKI workflow patterns
