#!/system/bin/sh
MODDIR=${0%/*}

# This script runs in late_start service mode. Keep work idempotent.
# Add module-specific runtime work here; do not assume a fixed module path.
