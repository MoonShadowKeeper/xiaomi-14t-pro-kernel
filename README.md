# Xiaomi 14T Pro GKI Kernel

<p align="center">
  <b>SukiSU Ultra · SUSFS v2.1.0 · KPM · Baseband Guard · GKI 6.1.138</b><br>
  <sub>Custom GKI kernel for Xiaomi 14T Pro / rothko, aligned with Android 14 GKI 2025-06</sub>
</p>

<p align="center">
  <img alt="Kernel" src="https://img.shields.io/badge/kernel-6.1.138-blue">
  <img alt="Device" src="https://img.shields.io/badge/device-Xiaomi%2014T%20Pro%20(rothko)-orange">
  <img alt="Root" src="https://img.shields.io/badge/root-SukiSU%20Ultra-red">
  <img alt="SUSFS" src="https://img.shields.io/badge/SUSFS-v2.1.0-purple">
  <img alt="Build" src="https://img.shields.io/badge/build-Bazel%20%2F%20Kleaf-green">
</p>

---

## Overview

This kernel is built for **Xiaomi 14T Pro (`rothko`)** on top of the official Android Common Kernel GKI tree:

```text
Android Common Kernel: android14-6.1-2025-06
Kernel version:        6.1.138
Build system:          Bazel / Kleaf
Target:                //common:kernel_aarch64_dist
```

The build follows the same GKI base generation style used by WildKernels, then layers SukiSU Ultra, SUSFS, KPM, Baseband Guard, networking improvements, filesystem support, and memory-management tuning.

---

## Core Features

| Feature | Status | Notes |
|---|---:|---|
| **SukiSU Ultra** | ✅ | KernelSU-based root implementation with SukiSU features |
| **SUSFS v2.1.0** | ✅ | Root hiding, mount hiding, uname spoofing, cmdline spoofing, open redirect |
| **KPM** | ✅ | Kernel Plugin Module support enabled |
| **Baseband Guard (BBG)** | ✅ | LSM-based protection for critical partitions and baseband-related paths |
| **BBR + FQ** | ✅ | Stable TCP congestion control improvement for GKI 6.1 |
| **WireGuard** | ✅ | Kernel-side VPN support |
| **ZRAM + ZSTD** | ✅ | ZRAM built as GKI module, ZSTD selected as compression backend |
| **NTFS3** | ✅ | NTFS read/write support through the in-kernel NTFS3 driver |
| **ExFAT** | ✅ | Native ExFAT filesystem support |
| **MGLRU** | ✅ | Multi-Generational LRU memory reclaim |
| **DAMON** | ✅ | Data Access MONitor with reclaim and LRU sort support |
| **TEO Governor** | ✅ | Timer Events Oriented CPU idle governor |
| **TMPFS XATTR / POSIX ACL** | ✅ | Required for better Mountify-style tmpfs compatibility |

---

## SukiSU Ultra

SukiSU Ultra is integrated directly into the kernel tree during the build.

Enabled root-side features:

```text
CONFIG_KSU=y
CONFIG_KPM=y
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
```

KPM support is included for plugin-based kernel extensions. The build keeps KALLSYMS enabled because KPM depends on symbol visibility.

---

## SUSFS v2.1.0

SUSFS is vendored locally under `deps/susfs/` and applied during the build. The included version reports:

```c
#define SUSFS_VERSION "v2.1.0"
```

Enabled SUSFS features:

| SUSFS feature | Config |
|---|---|
| SUSFS core | `CONFIG_KSU_SUSFS=y` |
| Hide suspicious paths | `CONFIG_KSU_SUSFS_SUS_PATH=y` |
| Hide mount points | `CONFIG_KSU_SUSFS_SUS_MOUNT=y` |
| Spoof kernel stat data | `CONFIG_KSU_SUSFS_SUS_KSTAT=y` |
| Memory mapping protection | `CONFIG_KSU_SUSFS_SUS_MAP=y` |
| Spoof uname output | `CONFIG_KSU_SUSFS_SPOOF_UNAME=y` |
| Spoof cmdline / bootconfig | `CONFIG_KSU_SUSFS_SPOOF_CMDLINE_OR_BOOTCONFIG=y` |
| Redirect file opens | `CONFIG_KSU_SUSFS_OPEN_REDIRECT=y` |
| SUSFS logging | `CONFIG_KSU_SUSFS_ENABLE_LOG=y` |
| Hide KSU/SUSFS symbols | `CONFIG_KSU_SUSFS_HIDE_KSU_SUSFS_SYMBOLS=y` |

SUSFS is applied from a local copy, so the workflow does not depend on the external SUSFS repository at build time.

---

## Baseband Guard

Baseband Guard is included from the vendored `deps/baseband-guard/` tree.

Enabled config:

```text
CONFIG_BBG=y
CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,integrity,selinux,smack,tomoyo,apparmor,bpf,baseband_guard"
```

BBG is wired as a Linux Security Module and added to `CONFIG_LSM`, which is required for it to load correctly on modern GKI kernels.

---

## Networking

The networking stack keeps the stable GKI 6.1 path:

```text
CONFIG_TCP_CONG_BBR=y
CONFIG_NET_SCH_FQ=y
CONFIG_DEFAULT_TCP_CONG="bbr"
CONFIG_WIREGUARD=y
```

BBRv3 is intentionally not included. It is not part of the stock 6.1 GKI tree and would require extra patching with higher conflict risk. Standard BBR + FQ is the safer choice here.

---

## Memory and Storage

Memory-management changes:

```text
CONFIG_ZRAM=m
CONFIG_ZRAM_DEF_COMP_ZSTD=y
CONFIG_ZRAM_DEF_COMP="zstd"
CONFIG_ZSMALLOC=m
CONFIG_LRU_GEN=y
CONFIG_LRU_GEN_ENABLED=y
CONFIG_LRU_GEN_STATS=y
CONFIG_DAMON=y
CONFIG_DAMON_RECLAIM=y
CONFIG_DAMON_LRU_SORT=y
CONFIG_CPU_IDLE_GOV_TEO=y
```

Filesystem changes:

```text
CONFIG_NTFS3_FS=y
CONFIG_NTFS3_LZX_XPRESS=y
CONFIG_NTFS3_FS_POSIX_ACL=y
CONFIG_EXFAT_FS=y
CONFIG_TMPFS_XATTR=y
CONFIG_TMPFS_POSIX_ACL=y
```

ZRAM and ZSMALLOC are kept as modules because the GKI module list expects `zram.ko` and `zsmalloc.ko` to exist.

---

## WildKernels Alignment

The workflow follows the same compatibility pattern used by WildKernels GKI builds:

- pinned ACK branch: `common-android14-6.1-2025-06`
- kernel sublevel: `6.1.138`
- clean dirty flags for a stable release string
- remove protected exports for vendor-module compatibility
- use Bazel/Kleaf with `--config=fast` and `--config=stamp`
- package with WildKernels AnyKernel3 `gki-2.0`

This keeps the kernel close to the known-working GKI base while still adding SukiSU Ultra, SUSFS, KPM, BBG, and the selected tuning.

---

## Build Artifacts

The workflow produces separate artifacts:

| Artifact | Contents |
|---|---|
| `AnyKernel3-Xiaomi14TPro-GKI6.1.138-*` | Flashable AnyKernel3 package contents |
| `boot-images-*` | `boot.img`, `boot-lz4.img`, `boot-gz.img`, raw `Image`, build log |

The AnyKernel3 artifact is uploaded as a direct flashable package, not as a zip nested inside another zip.

---

## Credits

- Android Common Kernel, Google
- SukiSU Ultra
- SUSFS by simonpunk
- Baseband Guard by vc-teahouse
- AnyKernel3 by osm0sis
- WildKernels GKI workflow patterns
