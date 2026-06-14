# Xiaomi 14T Pro Kernel Builder

Автоматическая сборка кастомного ядра **GKI 6.1.138** для **Xiaomi 14T Pro** (`rothko`, Dimensity 9300+) через GitHub Actions на self-hosted runner.

Ядро собирается из **чистых исходников Google (Android Common Kernel)** с помощью **Bazel/Kleaf**, поверх накатываются root-решение и набор тюнинга.

---

## Что внутри

| Компонент | Описание |
|-----------|----------|
| 🔑 **SukiSU Ultra** | Root-решение (форк KernelSU), пин на стабильный тег `v4.1.3` |
| 🕵️ **SUSFS v2.1+** | Сокрытие следов root (ветка `gki-android14-6.1`) |
| 🔌 **KPM** | Kernel Plugin Module |
| 📡 **BBR** | TCP BBR congestion control + FQ qdisc |
| 🔒 **WireGuard** | Встроенный VPN |
| 💾 **ZRAM + ZSTD** | Сжатый swap в RAM |
| 📁 **NTFS3** | Чтение/запись NTFS |
| 📁 **ExFAT** | Поддержка ExFAT |
| 🧹 **MGLRU** | Multi-Generational LRU |
| 📊 **DAMON** | Data Access Monitor (reclaim, lru_sort) |
| ⚡ **TEO** | Timer Events Oriented cpuidle governor |

---

## Как собрать

1. **Actions → Build Xiaomi 14T Pro Kernel → Run workflow**
2. При запуске можно поменять параметры:

| Параметр | По умолчанию | Назначение |
|----------|--------------|------------|
| `ACK_BRANCH` | `common-android14-6.1` | Ветка манифеста Android Common Kernel (для Android 15 → `common-android15-6.1`) |
| `KLEAF_TARGET` | `//common:kernel_aarch64_dist` | Bazel/Kleaf dist target |
| `SUSFS_BRANCH` | `gki-android14-6.1` | Ветка SUSFS (должна совпадать с версией ядра) |
| `ENABLE_KPM` | `true` | Включить KPM |
| `UPLOAD_RELEASE` | `true` | Публиковать GitHub Release |

3. На выходе — готовый **AnyKernel3 zip** в Artifacts и в Release.

---

## Процесс сборки

```
repo init + sync  →  чистый GKI от Google (tools/bazel, MODULE.bazel)
        │
        ├─ SukiSU Ultra  → setup.sh в common/
        ├─ SUSFS         → патч + fs/ + include/ в common/
        ├─ feature config → дописывается в gki_defconfig
        │
tools/bazel run //common:kernel_aarch64_dist -- --dist_dir=dist
        │
AnyKernel3 zip  →  Artifacts + Release
```

---

## Требования к runner

- Self-hosted runner с label `self-hosted`
- Linux (Debian/Ubuntu), работает от root
- Зависимости ставятся автоматически (`apt-get`), либо предустановлены
- ~30+ ГБ свободного места (ACK + сборка)

---

## Прошивка

1. Загрузиться в TWRP или использовать Magisk / KernelFlasher
2. Прошить полученный zip
3. Перезагрузиться

> ⚠️ Только для **Xiaomi 14T Pro (rothko)**. Проверьте устройство перед прошивкой.

---

## Источники

- [Android Common Kernel](https://android.googlesource.com/kernel/common) — базовые исходники GKI
- [SukiSU-Ultra](https://github.com/SukiSU-Ultra/SukiSU-Ultra)
- [SUSFS (susfs4ksu)](https://gitlab.com/simonpunk/susfs4ksu)
- [AnyKernel3](https://github.com/osm0sis/AnyKernel3)
- [MiCode/Xiaomi_Kernel_OpenSource](https://github.com/MiCode/Xiaomi_Kernel_OpenSource) — `bsp-rothko-u-oss`
