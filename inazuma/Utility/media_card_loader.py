import yt_dlp
from viu_media.libs.media_api.types import MediaItem, MediaSearchResult
from kivy.cache import Cache
from kivy.logger import Logger

from . import user_data_helper

Cache.register("trailer_urls.anime", timeout=360)


class MediaCardDataLoader(object):
    """this class loads an anime media card and gets the trailer url from yt-dlp"""

    def media_card(
        self,
        anime_item: MediaItem,
    ):
        media_card_data = {}
        media_card_data["anilist_data"] = anime_item
        media_card_data["viewclass"] = "MediaCard"
        media_card_data["anime_id"] = anime_id = anime_item.id
        return media_card_data

    def _get_stream_link(self, yt_url: str) -> str | None:
        video_url: str | None = ""
        with yt_dlp.YoutubeDL() as ydl:
            info_dict = ydl.extract_info(yt_url, download=False)
            if isinstance(info_dict, dict):
                video_url = info_dict.get("url")

        return video_url

    def get_trailer_from_yt_dlp(self, trailer_url, anime):
        if trailer := Cache.get("trailer_urls.anime", trailer_url):
            return trailer
        try:
            trailer = self._get_stream_link(trailer_url)
            Logger.info(f"yt-dlp Success:For {anime}")
            if trailer:
                Cache.append("trailer_urls.anime", trailer_url, trailer)
            return trailer
        except Exception as e:
            Logger.error(f"Yt-dlp Failure:For {anime} reason: {e}")
            return ""


media_card_loader = MediaCardDataLoader()
