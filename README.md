<div align="center">

<img src="https://raw.githubusercontent.com/sukisu-ultra/sukisu-ultra/main/.github/logo.png" width="120" alt="Kernel Logo" onerror="this.style.display='none'"/>

# 🔥 Custom GKI Kernel — Xiaomi 14T Pro

<p>
  <img src="https://img.shields.io/badge/Device-Xiaomi%2014T%20Pro-ff6b6b?style=for-the-badge&logo=xiaomi&logoColor=white"/>
  <img src="https://img.shields.io/badge/SoC-Dimensity%209300+-0099ff?style=for-the-badge&logo=mediatek&logoColor=white"/>
  <img src="https://img.shields.io/badge/Kernel-GKI%206.1%20%7C%20Android%2014-4ade80?style=for-the-badge&logo=linux&logoColor=white"/>
  <img src="https://img.shields.io/badge/Root-SukiSU%20Ultra-a855f7?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Stealth-SUSFS%20v2.1-f59e0b?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/github/actions/workflow/status/MoonShadowKeeper/xiaomi-14t-pro-kernel/build-gki.yml?style=flat-square&label=Build&logo=github-actions"/>
  <img src="https://img.shields.io/github/last-commit/MoonShadowKeeper/xiaomi-14t-pro-kernel?style=flat-square&label=Last%20Build"/>
  <img src="https://img.shields.io/github/downloads/MoonShadowKeeper/xiaomi-14t-pro-kernel/total?style=flat-square&label=Downloads"/>
</p>

**Кастомное GKI-ядро Android 14 для Xiaomi 14T Pro**  
Собирается из официальных исходников Google с наложением патчей SukiSU Ultra + SUSFS.  
Максимальная производительность · Скрытый рут · Актуальный KernelSU

</div>

---

## ✨ Что включено

| Компонент | Описание |
|-----------|----------|
| 🔑 **SukiSU Ultra** | Следующее поколение KernelSU — рут на уровне ядра |
| 🫥 **SUSFS v2.1+** | Полное сокрытие рута от банковских приложений и игр |
| 📦 **KPM** | Kernel Patch Module — горячая загрузка патчей без перезагрузки |
| 🌐 **BBR** | Алгоритм контроля перегрузки Google (v1, доступен в ядре 6.1) — быстрее `cubic` |
| 🔒 **WireGuard** | Встроенный современный VPN-протокол |
| 💾 **ZRAM + ZSTD** | Сжатие оперативной памяти, ускоряет многозадачность |
| 📁 **NTFS3 + ExFAT** | Нативная поддержка файловых систем Windows |
| 🧠 **LRU Gen** | Новый менеджер памяти от Google (MGLRU) |
| 📊 **DAMON** | Мониторинг и оптимизация паттернов доступа к памяти |
| ⚡ **TEO Governor** | Улучшенный алгоритм управления энергопотреблением CPU |

---

## 📱 Совместимость

| Параметр | Значение |
|----------|----------|
| **Устройство** | Xiaomi 14T Pro (corot) |
| **Процессор** | MediaTek Dimensity 9300+ |
| **Android** | 14 (Android U) |
| **Архитектура** | ARM64 / AArch64 |
| **Тип ядра** | GKI 2.0 (Generic Kernel Image) |
| **Версия Linux** | 6.1.x |

---

## ⚡ Быстрая установка

> [!WARNING]
> Перед прошивкой обязательно сделайте резервную копию. Прошивка кастомного ядра может привести к потере данных, если что-то пойдёт не так.

### Способ 1: AnyKernel3 (Рекомендуется)

1. Скачайте последний `AnyKernel3-Xiaomi-14T-Pro-GKI-*.zip` из вкладки [Actions → Artifacts](../../actions)
2. Загрузитесь в **TWRP** или **KernelSU Recovery**
3. Прошейте ZIP-архив
4. Перезагрузитесь

### Способ 2: Вручную через fastboot

```bash
# Загрузитесь в fastboot
adb reboot bootloader

# Прошейте образ ядра
fastboot flash boot Image

# Перезагрузитесь
fastboot reboot
```

---

## 🏗️ Сборка из исходников

Сборка происходит автоматически через **GitHub Actions** на самостоятельно размещённом раннере (Self-Hosted Runner) с использованием **Bazel (Kleaf)** — официальной системы сборки GKI от Google.

### Что происходит при сборке:

```
1. Синхронизация исходников GKI 6.1 с серверов Google
2. Применение патчей SUSFS v2.1+ (сокрытие рута)
3. Внедрение SukiSU Ultra (KernelSU)
4. Добавление твиков BBR, ZRAM, NTFS3, DAMON и др.
5. Компиляция через Bazel с LTO=thin
6. Упаковка в AnyKernel3 ZIP
```

### Запуск сборки вручную:

1. Перейдите во вкладку **[Actions](../../actions)**
2. Выберите **"Build Custom GKI Kernel (Xiaomi 14T Pro)"**
3. Нажмите **"Run workflow"**
4. Дождитесь завершения (~20 минут)
5. Скачайте артефакт из раздела **Artifacts**

---

## 🧩 Архитектура решения

```
Google GKI 6.1 Sources
         │
         ▼
   repo sync (manifest)
         │
         ▼
  ┌─────────────────┐
  │  SUSFS v2.1+    │  ← Скрытие рута (namespace, proc, stat)
  └─────────────────┘
         │
         ▼
  ┌─────────────────┐
  │ SukiSU Ultra    │  ← KernelSU + KPM поддержка
  └─────────────────┘
         │
         ▼
  ┌─────────────────┐
  │  Kernel Tweaks  │  ← BBR3, ZRAM/ZSTD, NTFS3, DAMON...
  └─────────────────┘
         │
         ▼
   Bazel (Kleaf) Build
         │
         ▼
  AnyKernel3 ZIP  🎉
```

---

## 📜 Changelog

### Latest build
- ✅ Переработан workflow — убраны все баги предыдущих версий
- ✅ Обновлён SukiSU Ultra до последней версии
- ✅ Исправлен патч SUSFS `namespace.c` (Hunk #1 — ручная вставка)
- ✅ Добавлены NTFS3, ExFAT, LRU Gen, DAMON
- ✅ LTO=thin для оптимального баланса скорости и производительности

---

## 🙏 Credits

| Проект | Ссылка |
|--------|--------|
| SukiSU Ultra | [sukisu-ultra/sukisu-ultra](https://github.com/sukisu-ultra/sukisu-ultra) |
| SUSFS | [gitlab.com/simonpunk/susfs4ksu](https://gitlab.com/simonpunk/susfs4ksu) |
| AnyKernel3 | [osm0sis/AnyKernel3](https://github.com/osm0sis/AnyKernel3) |
| Google GKI | [android.googlesource.com/kernel/manifest](https://android.googlesource.com/kernel/manifest) |

---

<div align="center">

Made with ❤️ for **Xiaomi 14T Pro** community

</div>
