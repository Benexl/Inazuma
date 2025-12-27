from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
)
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.libs.provider.anime.types import Server
    from viu_media.libs.media_api.types import MediaItem


class TaskCard(MDBoxLayout):
    file = ListProperty(("", ""))
    eta = StringProperty()
    media_item: "MediaItem" = ObjectProperty()
    episode: str = StringProperty()
    server: "Server" = ObjectProperty()
    progress = NumericProperty(0)
    status = StringProperty("downloading")  # downloading, completed, error
    progress_text = StringProperty("")

    def __init__(
        self, media_item: "MediaItem", episode: str, server: "Server", *args, **kwargs
    ):
        self.media_item = media_item
        self.episode = episode
        self.server = server
        super().__init__(*args, **kwargs)
        self.status = "downloading"

    def update_progress(self, percentage: int, text: str):
        """Update the progress of this task (thread-safe)"""

        def _update(dt):
            self.progress = percentage
            self.progress_text = text

        Clock.schedule_once(_update)

    def mark_complete(self, result=None):
        """Mark this task as completed (thread-safe)"""

        def _complete(dt):
            self.status = "completed"
            self.progress = 100
            self.progress_text = f"Completed successfully"

        Clock.schedule_once(_complete)

    def mark_error(self, error_message: str):
        """Mark this task as failed (thread-safe)"""

        def _error(dt):
            self.status = "error"
            self.progress_text = f"Error: {error_message}"

        Clock.schedule_once(_error)
