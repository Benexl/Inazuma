from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.core.config import AppConfig
    from viu_media.libs.media_api.base import BaseApiClient
    from viu_media.libs.provider.anime.base import BaseAnimeProvider


@dataclass
class Viu:
    config: "AppConfig"
    _media_api: "BaseApiClient | None" = None
    _anime_provider: "BaseAnimeProvider | None" = None

    @property
    def media_api(self) -> "BaseApiClient":
        if not self._media_api:
            from viu_media.libs.media_api.api import create_api_client

            self._media_api = create_api_client(
                self.config.general.media_api, self.config
            )
        return self._media_api

    @property
    def anime_provider(self) -> "BaseAnimeProvider":
        if not self._anime_provider:
            from viu_media.libs.provider.anime.provider import create_provider

            self._anime_provider = create_provider(self.config.general.provider)
        return self._anime_provider
