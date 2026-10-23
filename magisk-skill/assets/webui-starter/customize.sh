#!/system/bin/sh
# Minimal installer: nothing to patch, the WebUI lives in webroot/.
ui_print "- Installing module"
ui_print "- Open the module's WebUI from your manager"
set_perm_recursive "$MODPATH/webroot" 0 0 0755 0644
