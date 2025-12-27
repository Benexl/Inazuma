import os
import random

from kivy.resources import resource_find
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.uix.settings import SettingsWithSidebar
from kivymd.app import MDApp
from inazuma.view.screens import screens
from inazuma.view.components.media_card.media_card import MediaPopup
from kivy.logger import Logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.libs.media_api.types import MediaItem
    from viu_media.libs.provider.anime.types import Server


class Inazuma(MDApp):
    default_anime_image = resource_find(random.choice(["default_1.jpg", "default.jpg"]))
    default_banner_image = resource_find(random.choice(["banner_1.jpg", "banner.jpg"]))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.environ["VIU_APP_NAME"] = "inazuma"
        from inazuma.core.viu import Viu
        from viu_media.core.config import AppConfig

        self.viu_config = AppConfig()

        self.viu = Viu(self.viu_config)
        if "MEDIA_API_TOKEN" in os.environ:
            self.viu.media_api.authenticate(os.environ["MEDIA_API_TOKEN"])
        # self.icon = resource_find("logo.png")

        self.load_all_kv_files(self.directory)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Lightcoral"
        self.manager_screens = ScreenManager()
        self.manager_screens.transition = FadeTransition()

        # Track active downloads by a unique key (media_id + episode)
        self.active_downloads = {}

    def build(self) -> ScreenManager:
        self.settings_cls = SettingsWithSidebar

        self.generate_application_screens()

        # if config := self.config:
        #     if theme_color := config.get("Preferences", "theme_color"):
        #         self.theme_cls.primary_palette = theme_color
        #     if theme_style := config.get("Preferences", "theme_style"):
        #         self.theme_cls.theme_style = theme_style
        #
        # self.anime_screen = self.manager_screens.get_screen("anime screen")
        # self.search_screen = self.manager_screens.get_screen("search screen")
        # self.download_screen = self.manager_screens.get_screen("downloads screen")
        self.home_screen = self.manager_screens.get_screen("home screen")
        return self.manager_screens

    def on_start(self, *args):
        self.media_card_popup = MediaPopup()

    def generate_application_screens(self) -> None:
        for i, name_screen in enumerate(screens.keys()):
            model = screens[name_screen]["model"](self.viu)
            controller = screens[name_screen]["controller"](model)
            view = controller.get_view()
            view.manager_screens = self.manager_screens
            view.name = name_screen
            self.manager_screens.add_widget(view)

    def search_for_anime(self, search_field, **kwargs):
        if self.manager_screens.current != "search screen":
            self.manager_screens.current = "search screen"
        search_screen = self.manager_screens.get_screen("search screen")
        search_screen.controller.handle_search_for_anime(search_field, **kwargs)

    def show_anime_screen(self, media_item: "MediaItem", caller_screen_name: str):
        self.manager_screens.current = anime_screen_name = "anime screen"
        self.manager_screens.get_screen(anime_screen_name).controller.update_anime_view(
            media_item, caller_screen_name
        )

    def play_on_external_player(
        self,
        url: str,
        episode: str,
        media_item: "MediaItem",
        server: "Server",
    ):
        from viu_media.libs.player.params import PlayerParams
        from threading import Thread

        episode_title = media_item.title.english + f"; Episode {episode}"
        player_thread = Thread(
            target=self.viu.player_service.play,
            args=(
                PlayerParams(
                    url=url,
                    title=episode_title,
                    episode=episode,
                    query=media_item.title.romaji or media_item.title.english,
                    headers=server.headers,
                ),
            ),
            daemon=True,
        )
        player_thread.start()

    #
    def download_media(
        self, url: str, episode: str, media_item: "MediaItem", server: "Server"
    ):
        from inazuma.utility.notification import show_notification
        from threading import Thread

        # Create unique identifier for this download task
        task_id = f"{media_item.id}_{episode}"

        # Check if already downloading
        if task_id in self.active_downloads:
            show_notification(
                "Download In Progress",
                f"{media_item.title.english}; Episode {episode} is already downloading",
            )
            return

        download_screen = self.manager_screens.get_screen("downloads screen")
        download_screen.controller.new_download_task(media_item, episode, server)

        # Mark as active
        self.active_downloads[task_id] = True

        # Create progress hook that includes task_id
        def progress_hook(data):
            download_screen.controller.on_episode_download_progress(task_id, data)

        download_thread = Thread(
            target=self._add_media_to_download_queue,
            args=(task_id, url, episode, media_item, server, [progress_hook]),
            daemon=True,
        )
        download_thread.start()

        show_notification(
            "New Download", f"{media_item.title.english}; Episode {episode}"
        )

    def _add_media_to_download_queue(
        self,
        task_id: str,
        url: str,
        episode: str,
        media_item: "MediaItem",
        server: "Server",
        progress_hooks=[],
    ):
        from viu_media.core.downloader import DownloadParams
        from inazuma.utility.notification import show_notification

        try:
            episode_title = f"{media_item.title.english}; Episode {episode}"
            download_result = self.viu.downloader.download(
                DownloadParams(
                    url=url,
                    anime_title=media_item.title.english,
                    episode_title=episode_title,
                    silent=True,
                    headers=server.headers,
                    progress_hooks=progress_hooks,
                    logger=Logger,
                )
            )

            # Handle completion
            if download_result:
                show_notification(
                    "Download Complete",
                    f"{media_item.title.english}; Episode {episode}",
                )

                # Update download screen to show completion
                download_screen = self.manager_screens.get_screen("downloads screen")
                download_screen.controller.on_download_complete(
                    task_id, download_result
                )
        except Exception as e:
            show_notification(
                "Download Failed",
                f"{media_item.title.english}; Episode {episode}: {str(e)}",
            )
            download_screen = self.manager_screens.get_screen("downloads screen")
            download_screen.controller.on_download_error(task_id, str(e))
        finally:
            # Remove from active downloads
            if task_id in self.active_downloads:
                del self.active_downloads[task_id]

    #
    # def build_config(self, config):
    #     # General settings setup
    #     config.setdefaults(
    #         "Preferences",
    #         {
    #             "theme_color": "Cyan",
    #             "theme_style": "Dark",
    #             "downloads_dir": USER_VIDEOS_DIR,
    #         },
    #     )
    #
    # def build_settings(self, settings: Settings):
    #     settings.add_json_panel(
    #         "Settings", self.config, resource_find("general_settings_panel.json")
    #     )
    #
    # def on_config_change(self, config, section, key, value):
    #     # TODO: Change to match case
    #     if section == "Preferences":
    #         match key:
    #             case "theme_color":
    #                 pass
    #                 # if value in themes_available:
    #                 #     self.theme_cls.primary_palette = value
    #                 # else:
    #                 #     Logger.warning(
    #                 #         "AniXStream Settings: An invalid theme has been entered and will be ignored"
    #                 #     )
    #                 #     config.set("Preferences", "theme_color", "Cyan")
    #                 #     config.write()
    #             case "theme_style":
    #                 self.theme_cls.theme_style = value
    #
    # def on_stop(self):
    #     pass
    #
    #
    # def add_anime_to_user_anime_list(self, id: int):
    #     updated_list = user_data_helper.get_user_anime_list()
    #     updated_list.append(id)
    #     user_data_helper.update_user_anime_list(updated_list)
    #
    # def remove_anime_from_user_anime_list(self, id: int):
    #     updated_list = user_data_helper.get_user_anime_list()
    #     if updated_list.count(id):
    #         updated_list.remove(id)
    #     user_data_helper.update_user_anime_list(updated_list)
    #


#
# def setup_app():
#     os.environ["KIVY_VIDEO"] = "ffpyplayer"  # noqa: E402
#     Config.set("graphics", "width", "1000")  # noqa: E402
#     Config.set("graphics", "minimum_width", "1000")  # noqa: E402
#     Config.set("kivy", "window_icon", resource_find("logo.ico"))  # noqa: E402
#     Config.write()  # noqa: E402
#
#     Loader.num_workers = 5
#     Loader.max_upload_per_frame = 10
#
#     resource_add_path(ASSETS_DIR)
#     resource_add_path(CONFIGS_DIR)
#
def main():
    Inazuma().run()
