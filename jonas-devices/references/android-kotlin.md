# Android app development (Kotlin)

### 6.1 General Kotlin guidelines

- English for all code and documentation.
- Always declare variable and function types explicitly. Avoid `Any`; create custom types instead.
- No blank lines inside function bodies.
- **Naming:** PascalCase = classes/interfaces/enums; camelCase = variables/functions/methods; underscores_case = files and directories; UPPERCASE = environment variables and constants. No magic numbers (use constants). Functions start with an action verb. Booleans use `is`/`has`/`can` prefixes (`isLoading`, `hasError`, `canDelete`).
- **Functions:** under 20 instructions, single responsibility. Boolean returns prefixed `is`/`has`/`can`; void returns prefixed `execute`/`save`/`send`. Reduce nesting with early returns, extracted utilities and higher-order functions. Use default parameters instead of null checks. Group parameters into objects (RO-RO).
- **Data/classes:** data classes for data structures; wrap primitives in composite types and validate internally; favor immutability (`val`); SOLID; composition over inheritance. Classes under 200 instructions, 10 public methods, 10 properties.
- **Exceptions:** only for unexpected errors; catch only to fix anticipated issues or add context; custom exception types for domain errors.

### 6.2 Architecture

- **Clean architecture** with clear layer separation; repository pattern for persistence/caching; business logic in Use Cases/Interactors; separate UI, domain and data.

```
app/
├── data/           # Data sources, repositories, models
├── domain/         # Use cases, domain models, interfaces
├── presentation/   # UI components, ViewModels, state
└── di/             # Dependency injection modules
```

- **MVI:** ViewModel exposes a single immutable UI state object; UI observes state and renders; user intents/events enter through a single entry point; side effects are predictable and traceable.

### 6.3 UI

- **Prefer XML layouts + Fragments over Jetpack Compose** (unless Compose is specifically required). ConstraintLayout for complex layouts. Material 3. Responsive across screen sizes.
- Navigation Component for fragment/activity routing; navigation graph for app flow; deep links through Navigation Component; Safe Args for type-safe arguments.
- `MainActivity` manages primary navigation with `BottomNavigationView` (Home, Profile, Settings, …); handle navigation state across configuration changes.
- ViewBinding for view access; Flow or LiveData for UI state, observed lifecycle-aware; handle loading, error and success states consistently.
- Authentication flow screens: Splash → Login → Register → Forgot Password → Verify Email.

### 6.4 Testing

- Arrange-Act-Assert. Unit-test ViewModels, Use Cases, Repositories with test doubles; good coverage of business logic.
- UI: widget tests for components, integration tests for API modules, navigation-flow tests, Espresso for instrumented tests.

### 6.5 Best practices

- Handle lifecycle events properly; avoid leaks; use lifecycle-aware components.
- Coroutines for async work (handle cancellation); WorkManager for deferrable background work.
- Hilt or Dagger for DI; scope dependencies appropriately; keep DI config organized.
- Never block the main thread; DiffUtil for RecyclerView; lazy-load heavy resources; profile memory.
- Building on-device (Redmi): follow `references/redmi-termux.md` (verify JDK/Gradle/NDK, respect memory/thermal limits). Never generate or replace an Android release-signing key without authorization — losing it prevents app updates.
