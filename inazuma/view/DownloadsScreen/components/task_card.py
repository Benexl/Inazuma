from kivy.properties import (
    ListProperty,
    StringProperty,
    ObjectProperty,
    NumericProperty,
)
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
        """Update the progress of this task"""
        self.progress = percentage
        self.progress_text = text

    def mark_complete(self, result=None):
        """Mark this task as completed"""
        self.status = "completed"
        self.progress = 100
        self.progress_text = f"Download complete: {self.media_item.title.english or self.media_item.title.romaji} - Episode {self.episode}"

    def mark_error(self, error_message: str):
        """Mark this task as failed"""
        self.status = "error"
        self.progress_text = f"Error: {error_message}"
