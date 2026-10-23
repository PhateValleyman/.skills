#!/system/bin/sh

ui_print "- Installing Example Module"

# Add only installation-time checks that are required by the module.
# Example API guard (uncomment and adjust only when the feature truly requires it):
# [ "$API" -ge 29 ] || abort "! Android 10 (API 29) or later is required"

# customize.sh is sourced by the installer: do not call exit.
