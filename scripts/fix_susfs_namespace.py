#!/usr/bin/env python3
"""
Fix SUSFS Hunk #1 for fs/namespace.c.
The standard patch fails on latest GKI 6.1 because Google shifted
a few lines. This script finds the correct anchor lines and injects
the required SUSFS code precisely.
"""
import sys

with open('fs/namespace.c', 'r') as f:
    lines = f.readlines()

# Already patched?
if any('CONFIG_KSU_SUSFS_SUS_MOUNT' in l for l in lines):
    print(">> namespace.c already contains SUSFS — skipping")
    sys.exit(0)

# --- Block 1: inject after mnt_idmapping.h ---
anchor = next((i for i, l in enumerate(lines) if 'mnt_idmapping.h' in l), None)
if anchor is None:
    print("ERROR: mnt_idmapping.h not found in namespace.c", file=sys.stderr)
    sys.exit(1)

block1 = [
    '\n',
    '#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n',
    '#include <linux/susfs_def.h>\n',
    '#endif\n',
]
lines = lines[:anchor + 1] + block1 + lines[anchor + 1:]

# --- Block 2: inject after #include "internal.h" ---
anchor2 = next((i for i, l in enumerate(lines) if '#include "internal.h"' in l), None)
if anchor2 is None:
    print("ERROR: #include \"internal.h\" not found in namespace.c", file=sys.stderr)
    sys.exit(1)

block2 = [
    '\n',
    '#ifdef CONFIG_KSU_SUSFS_SUS_MOUNT\n',
    'extern bool susfs_is_current_ksu_domain(void);\n',
    'extern struct static_key_true susfs_is_sdcard_android_data_not_decrypted;\n',
    '#define CL_COPY_MNT_NS BIT(25)\n',
    '#endif\n',
]
lines = lines[:anchor2 + 1] + block2 + lines[anchor2 + 1:]

with open('fs/namespace.c', 'w') as f:
    f.writelines(lines)

print(">> namespace.c patched via Python successfully")
