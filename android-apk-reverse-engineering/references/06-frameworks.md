## Phase 6 — Framework-specific analysis

### Kotlin and coroutines
Recognize synthetic methods, continuation objects, suspend functions, state machines, extension methods, and generated accessors. Trace the logical source-level operation across generated methods rather than assuming one method corresponds to one source function.

### Flutter
Inspect `libapp.so`, `libflutter.so`, assets, `flutter_assets`, Dart AOT artifacts, and platform-channel calls. Standard Java decompilation will not reconstruct the Dart application logic. Select tools according to whether the build is AOT, debug, or profile.

### React Native
Identify Hermes versus JavaScriptCore, inspect the JS bundle or Hermes bytecode with format-compatible tooling, and trace native module/platform bridge calls. Do not assume that the JavaScript bundle is plain readable source.

### Unity
Identify Mono versus IL2CPP, inspect managed assemblies where present, or analyze `libil2cpp.so`, `global-metadata.dat`, and native symbols with matching tools. Keep the app version and architecture consistent when mapping metadata to native code.

### Xamarin/.NET
Look for assemblies and runtime libraries, then use tooling compatible with the specific .NET/Mono packaging and obfuscation. Validate managed-code conclusions against JNI/native boundaries where applicable.

### WebView and hybrid apps
Inspect JavaScript, HTML, assets, bridge methods, URL allowlists, and origin validation. Treat JavaScript interfaces exposed to untrusted content as a security boundary.
