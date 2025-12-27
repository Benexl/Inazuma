from inazuma.model.download_screen import DownloadsScreenModel
from inazuma.view.DownloadsScreen.download_screen import DownloadsScreenView

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.libs.provider.anime.types import Server
    from viu_media.libs.media_api.types import MediaItem
from kivy.utils import format_bytes_to_human


class DownloadsScreenController:
    """The controller for the download screen"""

    def __init__(self, model: DownloadsScreenModel):
        self.model = model
        self.view = DownloadsScreenView(controller=self, model=self.model)
        # Track task cards by task_id
        self.task_cards = {}

    def get_view(self) -> DownloadsScreenView:
        return self.view

    def new_download_task(
        self, media_item: "MediaItem", episode: str, server: "Server"
    ):
        task_id = f"{media_item.id}_{episode}"
        task_card = self.view.add_task_card(media_item, episode, server)
        # Store task card reference for updates
        self.task_cards[task_id] = task_card
        return task_card

    def on_episode_download_progress(self, task_id: str, data: dict):
        """Update progress for a specific download task"""
        percentage_completion = 0
        if data.get("total_bytes", 0) > 0:
            percentage_completion = round(
                (data.get("downloaded_bytes", 0) / data.get("total_bytes", 0)) * 100
            )

        speed = (
            format_bytes_to_human(data.get("speed", 0)) if data.get("speed") else "0 B"
        )
        progress_text = f"Downloading: {data.get('filename', 'unknown')} ({format_bytes_to_human(data.get('downloaded_bytes', 0)) if data.get('downloaded_bytes') else '0 B'}/{format_bytes_to_human(data.get('total_bytes', 0)) if data.get('total_bytes') else '0 B'})\nElapsed: {round(data.get('elapsed', 0)) if data.get('elapsed') else 0}s ETA: {data.get('eta', 0) if data.get('eta') else 0}s Speed: {speed}/s"

        # Update overall progress bar
        self.view.update_download_progress(percentage_completion, progress_text)

        # Update specific task card if it exists
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.update_progress(percentage_completion, progress_text)

    def on_download_complete(self, task_id: str, result):
        """Handle download completion for a specific task"""
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.mark_complete(result)

        # Update model
        self.model.on_download_complete(task_id, result)

    def on_download_error(self, task_id: str, error_message: str):
        """Handle download error for a specific task"""
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.mark_error(error_message)

        # Update model
        self.model.on_download_error(task_id, error_message)


__all__ = ["DownloadsScreenController"]
