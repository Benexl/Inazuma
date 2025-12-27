from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.core.config import AppConfig
    from viu_media.libs.media_api.base import BaseApiClient
    from viu_media.libs.provider.anime.base import BaseAnimeProvider
    from viu_media.cli.service.download import DownloadService
    from viu_media.cli.service.registry import MediaRegistryService
    from viu_media.cli.service.player import PlayerService
    from viu_media.core.downloader.base import BaseDownloader


@dataclass
class Viu:
    config: "AppConfig"
    _media_api: "BaseApiClient | None" = None
    _anime_provider: "BaseAnimeProvider | None" = None
    _registry_service: "MediaRegistryService | None" = None
    _player_service: "PlayerService | None" = None
    _downloader: "BaseDownloader | None" = None
    _download_service: "DownloadService | None" = None

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

    @property
    def registry_service(self) -> "MediaRegistryService":
        if not self._registry_service:
            from viu_media.cli.service.registry import MediaRegistryService

            self._registry_service = MediaRegistryService(
                self.config.general.media_api, self.config.media_registry
            )
        return self._registry_service

    @property
    def player_service(self) -> "PlayerService":
        if not self._player_service:
            from viu_media.cli.service.player import PlayerService

            self._player_service = PlayerService(
                self.config, self.anime_provider, self.registry_service
            )

        return self._player_service

    @property
    def downloader(self) -> "BaseDownloader":
        if not self._downloader:
            from viu_media.core.downloader import create_downloader

            self._downloader = create_downloader(self.config.downloads)
        return self._downloader

    @property
    def download_service(self) -> "DownloadService":
        if not self._download_service:
            from viu_media.cli.service.download import DownloadService

            self._download_service = DownloadService(
                self.config, self.registry_service, self.media_api, self.anime_provider
            )
        return self._download_service
