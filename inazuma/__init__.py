import random

from kivy.resources import resource_find
from kivy.uix.screenmanager import FadeTransition, ScreenManager
from kivy.uix.settings import SettingsWithSidebar
from kivymd.app import MDApp
from viu_media.core.config import AppConfig

from .View.components.media_card.media_card import MediaPopup
from .View.screens import screens


class Inazuma(MDApp):
    default_anime_image = resource_find(random.choice(["default_1.jpg", "default.jpg"]))
    default_banner_image = resource_find(random.choice(["banner_1.jpg", "banner.jpg"]))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from inazuma.core.viu import Viu

        self.viu_config = AppConfig()

        self.viu = Viu(self.viu_config)
        # self.icon = resource_find("logo.png")

        self.load_all_kv_files(self.directory)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Lightcoral"
        self.manager_screens = ScreenManager()
        self.manager_screens.transition = FadeTransition()

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

    # def search_for_anime(self, search_field, **kwargs):
    #     if self.manager_screens.current != "search screen":
    #         self.manager_screens.current = "search screen"
    #     self.search_screen.handle_search_for_anime(search_field, **kwargs)
    #
    # def show_anime_screen(self, anilist_data, caller_screen_name: str):
    #     self.manager_screens.current = "anime screen"
    #     self.anime_screen.controller.update_anime_view(anilist_data, caller_screen_name)

    #
    def download_anime_video(self, url: str, anime_title, anime_server):
        pass
        # from viu_media.cli.service.download import DownloadService
        #
        # from .Utility.show_notification import show_notification
        #
        # self.download_screen.new_download_task(anime_title)
        # show_notification("New Download", f"{anime_title[0]} episode: {anime_title[1]}")
        # progress_hook = self.download_screen.on_episode_download_progress
        # downloader.download_file(
        #     url, anime_title, anime_server["episode_title"], USER_VIDEOS_DIR
        # )

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
