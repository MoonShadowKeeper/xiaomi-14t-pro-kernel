#!/usr/bin/env python3
"""
Verify that all expected kernel configs are present in the final built .config.
Exits with code 1 if any required option is missing or has wrong value.
"""
import sys
import os

# --- Define expected options ---
REQUIRED = {
    # KernelSU / SukiSU Ultra
    "CONFIG_KSU":                       "y",
    # SUSFS
    "CONFIG_KSU_SUSFS":                 "y",
    "CONFIG_KSU_SUSFS_SUS_MOUNT":       "y",
    # Networking
    "CONFIG_TCP_CONG_BBR":              "y",
    "CONFIG_DEFAULT_BBR":               "y",
    "CONFIG_WIREGUARD":                 "y",
    # Filesystem
    "CONFIG_NTFS3_FS":                  "y",
    "CONFIG_EXFAT_FS":                  "y",
    "CONFIG_TMPFS_POSIX_ACL":           "y",
    # Memory
    "CONFIG_LRU_GEN":                   "y",
    "CONFIG_DAMON":                     "y",
    "CONFIG_DAMON_RECLAIM":             "y",
    # ZRAM
    "CONFIG_ZRAM":                      "m",
    "CONFIG_CRYPTO_ZSTD":               "y",
    "CONFIG_ZRAM_DEF_COMP_ZSTD":        "y",
    # Power
    "CONFIG_CPU_IDLE_GOV_TEO":          "y",
    # KPM
    "CONFIG_KPM":                       "y",
}

# These are checked but only warn (not fail) if missing
OPTIONAL = {
    "CONFIG_LRU_GEN_ENABLED":           "y",
    "CONFIG_DAMON_VADDR":               "y",
    "CONFIG_DAMON_PADDR":               "y",
    "CONFIG_ENERGY_MODEL":              "y",
    "CONFIG_SCHED_MC":                  "y",
    "CONFIG_NET_SCH_FQ":                "y",
}


def parse_config(path):
    config = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or '=' not in line:
                continue
            key, _, val = line.partition('=')
            config[key.strip()] = val.strip()
    return config


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else None

    if not config_path or not os.path.exists(config_path):
        # Try to find it automatically
        search_dirs = [
            "/root/kernel_workspace/out/dist",
            "/root/kernel_workspace/out",
            "/root/kernel_workspace/common",
        ]
        for d in search_dirs:
            candidate = os.path.join(d, ".config")
            if os.path.exists(candidate):
                config_path = candidate
                break

    if not config_path or not os.path.exists(config_path):
        print("::error::Could not find .config file — build may have failed silently")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Kernel Config Verification")
    print(f"  Config: {config_path}")
    print(f"{'='*60}\n")

    config = parse_config(config_path)
    errors = []
    warnings = []

    # Check required
    print("[ REQUIRED OPTIONS ]")
    for key, expected in sorted(REQUIRED.items()):
        actual = config.get(key)
        if actual == expected:
            print(f"  ✅  {key}={actual}")
        elif actual is not None:
            msg = f"{key}: expected={expected}, got={actual}"
            print(f"  ❌  {msg}")
            errors.append(msg)
        else:
            # check if explicitly disabled
            msg = f"{key} not found (expected={expected})"
            print(f"  ❌  {msg}")
            errors.append(msg)

    # Check optional
    print("\n[ OPTIONAL OPTIONS ]")
    for key, expected in sorted(OPTIONAL.items()):
        actual = config.get(key)
        if actual == expected:
            print(f"  ✅  {key}={actual}")
        else:
            msg = f"{key}: expected={expected}, got={actual or 'not set'}"
            print(f"  ⚠️   {msg}")
            warnings.append(msg)

    print(f"\n{'='*60}")
    print(f"  Results: {len(REQUIRED)} required, {len(OPTIONAL)} optional")
    print(f"  Errors:   {len(errors)}")
    print(f"  Warnings: {len(warnings)}")
    print(f"{'='*60}\n")

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  ::warning::{w}")

    if errors:
        print("ERRORS (build will fail):")
        for e in errors:
            print(f"  ::error::{e}")
        sys.exit(1)

    print("✅ All required kernel options verified successfully!")


if __name__ == "__main__":
    main()
