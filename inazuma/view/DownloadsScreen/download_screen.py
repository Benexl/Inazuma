from kivy.clock import Clock
from kivy.properties import ObjectProperty

from ...view.base_screen import BaseScreenView
from .components.task_card import TaskCard
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.libs.provider.anime.types import Server
    from viu_media.libs.media_api.types import MediaItem


class DownloadsScreenView(BaseScreenView):
    main_container = ObjectProperty()
    progress_bar = ObjectProperty()
    download_progress_label = ObjectProperty()

    def add_task_card(self, media_item: "MediaItem", episode: str, server: "Server"):
        task_card = TaskCard(media_item, episode, server)
        Clock.schedule_once(lambda _: self.main_container.add_widget(task_card))
        return task_card

    def update_download_progress(self, percentage_completion: int, progress_text: str):
        self.progress_bar.value = percentage_completion
        self.download_progress_label.text = progress_text

    def update_layout(self, widget):
        self.user_anime_list_container.add_widget(widget)

        #
        #     d["filename"],
        #     d["downloaded_bytes"],
        #     d["total_bytes"],
        #     d.get("total_bytes"),
        #     d["elapsed"],
        #     d["eta"],
        #     d["speed"],
        #     d.get("percent"),
        # )
        #


__all__ = ["DownloadsScreenView"]
