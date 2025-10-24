import logging

from viu_media.libs.media_api.types import MediaSearchResult
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Factory
from kivymd.uix.button import MDButton

from ...View.base_screen import BaseScreenView

logger = logging.getLogger((__name__))


class EpisodeButton(MDButton):
    text = StringProperty()
    change_episode_callback = ObjectProperty()


Factory.register("EpisodeButton", cls=EpisodeButton)


class AnimeScreenView(BaseScreenView):
    """The anime screen view"""

    current_anilist_data: "MediaSearchResult | None" = None
    current_server = ObjectProperty()
    current_link = StringProperty()
    current_servers = ListProperty([])
    current_anime_data = ObjectProperty()
    caller_screen_name = ObjectProperty()
    current_title = ""
    episodes_container = ObjectProperty()
    total_episodes = 0
    current_episode = 1
    video_player = ObjectProperty()
    current_server_name = "dropbox"
    is_dub = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.update_episodes(100)

    def update_episodes(self, episodes_list):
        self.episodes_container.data = []
        self.total_episodes = len(episodes_list)
        for episode in episodes_list:
            self.episodes_container.data.append(
                {
                    "viewclass": "EpisodeButton",
                    "text": str(episode),
                    "change_episode_callback": lambda x=episode: self.update_current_episode(
                        x
                    ),
                }
            )

    def next_episode(self):
        next_episode = self.current_episode + 1
        if next_episode <= self.total_episodes:
            self.update_current_episode(str(next_episode))

    def previous_episode(self):
        previous_episode = self.current_episode - 1
        if previous_episode > 0:
            self.update_current_episode(str(previous_episode))

    def on_current_anime_data(self, instance, value):
        self.update_episodes(value["availableEpisodesDetail"]["sub"][::-1])
        self.current_episode = int("1")
        self.update_current_video_stream(self.current_server_name)
        self.video_player.state = "play"

    def update_current_episode(self, episode):
        self.current_episode = int(episode)
        self.controller.fetch_streams(
            self.current_anilist_data, self.is_dub.active, episode
        )
        self.update_current_video_stream(self.current_server_name)
        self.video_player.state = "play"

    def update_current_video_stream(self, server_name, is_dub=False):
        for server in self.current_servers:
            if server["server"] == server_name:
                self.current_server = server
                self.current_server_name = server["server"]
                self.current_link = server["links"][0]["link"]
                self.video_player.state = "play"
                logger.debug(f"found {self.current_server_name} server")
                logger.debug(f"found {self.current_link} link")
                break
            else:
                logger.warning(
                    f"Found {server['server']} server but {server_name} wanted"
                )

    def add_to_user_anime_list(self, *args):
        self.app.add_anime_to_user_anime_list(self.model.anime_id)


__all__ = ["AnimeScreenView"]
