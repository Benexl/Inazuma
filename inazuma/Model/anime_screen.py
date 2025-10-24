from viu_media.libs.media_api.api import create_api_client
from viu_media.libs.provider.anime.provider import create_provider
from viu_media.libs.media_api.types import MediaSearchResult
from viu_media.cli.utils.search import find_best_match_title
from viu_media.libs.provider.anime.types import ProviderName
from kivy.cache import Cache
from kivy.logger import Logger

from .base_model import BaseScreenModel

Cache.register("streams.anime", limit=10)

anime_provider = create_provider(ProviderName.ALLANIME)


class AnimeScreenModel(BaseScreenModel):
    """the Anime screen model"""

    data = {}
    anime_id = 0
    current_anime_data = None
    current_anilist_anime_id = "0"
    current_provider_anime_id = "0"
    current_title = ""
    media_search_result: "MediaSearchResult | None" = None

    def get_anime_data_from_provider(
        self, media_search_result: "MediaSearchResult", is_dub, id=None
    ):
        try:
            if (self.media_search_result or {"id": -1})["id"] == media_search_result[
                "id"
            ] and self.current_anime_data:
                return self.current_anime_data
            translation_type = "dub" if is_dub else "sub"
            search_results = anime_provider.search_for_anime(
                media_search_result["title"]["romaji"]
                or media_search_result["title"]["english"],
                translation_type,
            )

            if search_results:
                _search_results = search_results["results"]
                result = max(
                    _search_results,
                    key=lambda x: anime_title_percentage_match(
                        x["title"], media_search_result
                    ),
                )
                self.current_anilist_anime_id = media_search_result["id"]
                self.current_provider_anime_id = result["id"]
                self.current_anime_data = anime_provider.get_anime(result["id"])
                if self.current_anime_data:
                    Logger.debug(f"Got data of {self.current_anime_data['title']}")
                return self.current_anime_data
            return {}
        except Exception as e:
            Logger.info("anime_screen error: %s" % e)
            return {}

    def get_episode_streams(self, episode, is_dub):
        translation_type = "dub" if is_dub else "sub"

        try:
            if self.current_anime_data:
                streams = anime_provider.get_episode_streams(
                    self.current_provider_anime_id, episode, translation_type
                )
                if not streams:
                    return []
                return [episode_stream for episode_stream in streams]

            return []
        except Exception as e:
            Logger.error("anime_screen error: %s" % e)
            return []

        # should return {type:{provider:streamlink}}

    def get_anime_data(self, id: int):
        return AniList.get_anime(id)


__all__ = ["AnimeScreenModel"]
