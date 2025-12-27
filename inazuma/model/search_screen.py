from .base_model import BaseScreenModel
from typing import TYPE_CHECKING
from viu_media.libs.media_api.params import MediaSearchParams
from viu_media.libs.media_api.types import MediaSort

if TYPE_CHECKING:
    from inazuma.core.viu import Viu


class SearchScreenModel(BaseScreenModel):
    viu: "Viu"

    def __init__(self, viu: "Viu") -> None:
        super().__init__()
        self.viu = viu

    def get_trending(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.TRENDING_DESC,per_page=self.viu.config.anilist.per_page)
        )

    def search_for_anime(self, anime_title, filters={}):
        filters = {k: v for k, v in filters.items() if v not in [None, "DISABLED"]}
        return self.viu.media_api.search_media(
            MediaSearchParams(query=anime_title, per_page=self.viu.config.anilist.per_page,**filters)
        )


__all__ = ["SearchScreenModel"]
