from .base_model import BaseScreenModel
from viu_media.libs.media_api.params import MediaSearchParams
from viu_media.libs.media_api.types import MediaSort, MediaStatus
from inazuma.core.viu import Viu


class HomeScreenModel(BaseScreenModel):
    """The home screen model"""

    viu: Viu

    def __init__(self, viu: Viu) -> None:
        super().__init__()
        self.viu = viu

    def get_trending_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.TRENDING_DESC)
        )

    def get_most_favourite_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.FAVOURITES_DESC)
        )

    def get_most_recently_updated_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.UPDATED_AT_DESC)
        )

    def get_most_popular_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.POPULARITY_DESC)
        )

    def get_most_scored_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(sort=MediaSort.SCORE_DESC)
        )

    def get_upcoming_anime(self):
        return self.viu.media_api.search_media(
            MediaSearchParams(
                status=MediaStatus.NOT_YET_RELEASED, sort=MediaSort.POPULARITY_DESC
            )
        )


__all__ = ["HomeScreenModel"]
