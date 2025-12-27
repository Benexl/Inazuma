from .base_model import BaseScreenModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from inazuma.core.viu import Viu


class DownloadsScreenModel(BaseScreenModel):
    """
    Handles the download screen logic
    """

    viu: "Viu"

    def __init__(self, viu: "Viu") -> None:
        super().__init__()
        self.viu = viu
        # Track download statuses
        self.download_statuses = {}

    def update_download_progress(self, d):
        print(
            d["filename"],
            d["downloaded_bytes"],
            d["total_bytes"],
            d.get("total_bytes"),
            d["elapsed"],
            d["eta"],
            d["speed"],
            d.get("percent"),
        )
        if d["status"] == "finished":
            print("Done downloading, now converting ...")

    def on_download_complete(self, task_id: str, result):
        """Handle successful download completion"""
        self.download_statuses[task_id] = {"status": "completed", "result": result}
        print(f"Download completed: {task_id}")

    def on_download_error(self, task_id: str, error_message: str):
        """Handle download error"""
        self.download_statuses[task_id] = {"status": "error", "error": error_message}
        print(f"Download error for {task_id}: {error_message}")


__all__ = ["DownloadsScreenModel"]
