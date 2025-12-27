from inazuma.model.base_model import BaseScreenModel
from typing import TYPE_CHECKING
from viu_media.libs.media_api.params import UserMediaListSearchParams
from viu_media.libs.media_api.types import UserMediaListStatus

if TYPE_CHECKING:
    from inazuma.core.viu import Viu


class MyListScreenModel(BaseScreenModel):
    already_in_user_anime_list = []

    viu: "Viu"

    def __init__(self, viu: "Viu") -> None:
        super().__init__()
        self.viu = viu

    def get_watching(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.WATCHING)
        )

    def get_paused(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.PAUSED)
        )

    def get_planning(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.PLANNING)
        )

    def get_completed(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.COMPLETED)
        )

    def get_dropped(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.DROPPED)
        )

    def get_repeating(self):
        return self.viu.media_api.search_media_list(
            UserMediaListSearchParams(status=UserMediaListStatus.REPEATING)
        )
