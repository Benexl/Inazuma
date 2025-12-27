# Inazuma - Copilot Instructions

## Project Overview

Inazuma is a Kivy/KivyMD GUI application that wraps the `viu-media` library for browsing, streaming, and downloading anime. It uses an **MVC (Model-View-Controller) architecture** with an **Observer pattern** for reactive updates.

## Architecture

### Core Structure

```
inazuma/
├── __init__.py      # Main app class (Inazuma), entry point, global utilities
├── core/viu.py      # Lazy-loaded service container for viu-media integration
├── model/           # Data layer - fetches from viu-media APIs
├── view/            # UI layer - Kivy screens and components
├── controller/      # Coordination layer - connects model ↔ view
└── utility/         # Helpers: observer, notifications, data utils
```

### MVC + Observer Pattern

Every screen follows a consistent pattern (see [view/screens.py](inazuma/view/screens.py)):

1. **Model** (`model/<screen>.py`): Inherits `BaseScreenModel`, accesses `viu` services, notifies observers via `notify_observers(screen_name)`
2. **View** (`view/<Screen>/<screen>.py` + `.kv`): Inherits `BaseScreenView` (which implements `Observer`), auto-registers as observer in `__init__`
3. **Controller** (`controller/<screen>.py`): Instantiates model and view, handles user actions, uses threading for async operations

### Screen Registration

New screens must be registered in [view/screens.py](inazuma/view/screens.py):

```python
screens = {
    "screen name": {
        "model": ScreenModel,
        "controller": ScreenController,
    },
}
```

### Threading Pattern

All network/API calls must run in background threads. Use `kivy.clock.Clock.schedule_once()` to update UI:

```python
from threading import Thread
from kivy.clock import Clock

def handle_action(self):
    Thread(target=self._process_async).start()

def _process_async(self):
    result = self.model.fetch_data()  # blocking call
    Clock.schedule_once(lambda dt: self.view.update_ui(result))  # UI update
```

## Key Integrations

### viu-media Library

The `Viu` dataclass in [core/viu.py](inazuma/core/viu.py) provides lazy-loaded access to:

- `media_api`: Search and fetch anime metadata (AniList)
- `anime_provider`: Get streaming sources/links
- `download_service` / `downloader`: Handle downloads
- `player_service`: External player integration

Types are imported from `viu_media.libs.*` under `TYPE_CHECKING` blocks.

### Kivy/KivyMD

- UI defined in `.kv` files alongside Python classes
- Use `ObjectProperty`, `StringProperty`, etc. for reactive bindings
- Main app loads all `.kv` files automatically via `load_all_kv_files()`
- Access app instance from views: `self.app = MDApp.get_running_app()`

## Development Commands

```bash
uv sync && uv run python -m inazuma
```

## Conventions

### File Organization

- Each screen has its own folder: `view/<ScreenName>/` containing `__init__.py`, `<name>.py`, `<name>.kv`
- Shared components go in `view/components/`
- Component-specific sub-components in nested `components/` folders

### Naming

- Screen names use spaces: `"home screen"`, `"anime screen"` (used for navigation)
- Class names: `HomeScreenView`, `HomeScreenController`, `HomeScreenModel`
- `.kv` widget rules match class names exactly: `<HomeScreenView>`

### Download Task Tracking

Downloads are tracked by `task_id = f"{media_item.id}_{episode}"` to prevent duplicates. The `active_downloads` dict in the main app and `task_cards` in the controller maintain state.

## Common Tasks

### Adding a New Screen

1. Create `model/<screen>_screen.py` extending `BaseScreenModel`
2. Create `view/<Screen>Screen/<screen>_screen.py` extending `BaseScreenView`
3. Create matching `.kv` file with `<ScreenNameView>` rule
4. Create `controller/<screen>_screen.py` with view/model coordination
5. Register in `view/screens.py`
6. Add navigation in `view/components/navrail.kv`

### Working with Media Data

Media items use types from `viu_media.libs.media_api.types.MediaItem`. Key fields:

- `title.english`, `title.romaji`
- `id`, `episodes`, `status`, `genres`, `cover_image`

Search uses `MediaSearchParams` with sort options like `MediaSort.TRENDING_DESC`.
