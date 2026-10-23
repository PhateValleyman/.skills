---
name: android-development
description: Practical Kotlin and Android application development guidance, including architecture, UI, lifecycle, testing, performance, and dependency injection. Use when designing, implementing, reviewing, or refactoring an Android app; adapt recommendations to the existing project, Android versions, and user requirements. Do not use for APK reverse engineering, device administration, or Magisk modules.
---

# Android Development Best Practices

## Workflow

1. Identify the app's existing language, architecture, UI toolkit, minimum Android version, build conventions, and tests before proposing changes. Preserve working project patterns unless the task calls for a migration.
2. Clarify the feature and its observable behavior. Prefer the smallest coherent change; do not add libraries or architectural layers without a concrete need.
3. Implement idiomatic Kotlin with clear names, narrow responsibilities, explicit handling of nullable values and failures, and immutable state where appropriate. Use type inference when it improves readability; do not impose arbitrary line, statement, or class-size limits.
4. Respect lifecycle and threading. Keep blocking I/O and expensive work off the main thread; use lifecycle-aware coroutines/Flow or the project’s established equivalent, with cancellation and error states handled. Use WorkManager for work that must be deferred or persisted.
5. Verify with the narrowest relevant unit, UI, or instrumentation tests and report what was and was not run.

## Architecture and state

Use separation of concerns that fits the app's size. For larger apps, a UI/presentation layer, domain logic, and data/repository boundary can help; a small feature may not need a separate use-case class. Prefer dependency inversion at meaningful boundaries, not boilerplate for its own sake.

MVI-style immutable UI state and explicit events are useful when they simplify state transitions. Keep side effects explicit and testable. Use repositories for shared data sources, caching, or persistence policy; avoid duplicating domain state across UI layers.

## UI and navigation

Follow the project's existing UI framework. Use Jetpack Compose when the app or requested feature uses Compose; use Views, Fragments, ViewBinding, or Navigation Component where they fit an existing Views-based project. Do not migrate frameworks merely because one is preferred here.

Make layouts responsive and accessible, preserve state across configuration changes, and represent loading, empty, success, and error states where relevant. Use lifecycle-aware collection/observation. Choose navigation and typed arguments consistent with the current app.

## Data, dependencies, and errors

Use data classes for value-shaped data and `val` by default. Validate inputs at appropriate boundaries. Handle expected failures explicitly; add context when translating errors and avoid swallowing exceptions. Choose Hilt/Dagger or another DI tool only when dependency graph complexity warrants it.

Avoid hard-coded secrets, magic values, main-thread I/O, memory leaks, unnecessary global state, and unbounded work. Optimize based on measurement; use list diffing/lazy loading when the UI and data volume benefit.

## Testing

Use Arrange–Act–Assert or the test style already used in the repository. Test business rules and ViewModel/state transitions with appropriate fakes; use UI/instrumentation tests for critical user flows and platform behavior. Prefer meaningful coverage over a numeric coverage target.
