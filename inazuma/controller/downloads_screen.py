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
        downloaded = (
            format_bytes_to_human(data.get("downloaded_bytes", 0))
            if data.get("downloaded_bytes")
            else "0 B"
        )
        total = (
            format_bytes_to_human(data.get("total_bytes", 0))
            if data.get("total_bytes")
            else "0 B"
        )
        eta = data.get("eta", 0) if data.get("eta") else 0
        progress_text = f"{downloaded}/{total} • {speed}/s • ETA: {eta}s"

        # Update specific task card if it exists
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.update_progress(percentage_completion, progress_text)

        # Update overall progress bar with aggregate stats
        self._update_overall_progress()

    def _update_overall_progress(self):
        """Calculate and update overall download progress across all tasks"""
        if not self.task_cards:
            self.view.update_download_progress(0, "No active downloads")
            return

        total_progress = 0
        completed_count = 0
        error_count = 0
        downloading_count = 0

        for task_card in self.task_cards.values():
            total_progress += task_card.progress
            if task_card.status == "completed":
                completed_count += 1
            elif task_card.status == "error":
                error_count += 1
            elif task_card.status == "downloading":
                downloading_count += 1

        avg_progress = round(total_progress / len(self.task_cards))
        total_tasks = len(self.task_cards)

        status_parts = []
        if downloading_count > 0:
            status_parts.append(f"{downloading_count} downloading")
        if completed_count > 0:
            status_parts.append(f"{completed_count} completed")
        if error_count > 0:
            status_parts.append(f"{error_count} failed")

        status_text = " • ".join(status_parts) if status_parts else "Idle"
        progress_text = (
            f"Overall: {status_text} ({completed_count}/{total_tasks} tasks)"
        )

        self.view.update_download_progress(avg_progress, progress_text)

    def on_download_complete(self, task_id: str, result):
        """Handle download completion for a specific task"""
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.mark_complete(result)

        # Update model
        self.model.on_download_complete(task_id, result)

        # Update overall progress
        self._update_overall_progress()

    def on_download_error(self, task_id: str, error_message: str):
        """Handle download error for a specific task"""
        if task_id in self.task_cards:
            task_card = self.task_cards[task_id]
            task_card.mark_error(error_message)

        # Update model
        self.model.on_download_error(task_id, error_message)

        # Update overall progress
        self._update_overall_progress()


__all__ = ["DownloadsScreenController"]
