from kivy.properties import ObjectProperty
from kivy.logger import Logger
from typing import TYPE_CHECKING


from ...view.base_screen import BaseScreenView

from inazuma.view.components.media_card import MediaCard, MediaCardsContainer

if TYPE_CHECKING:
    from viu_media.libs.media_api.types import MediaSearchResult


class HomeScreenView(BaseScreenView):
    main_container = ObjectProperty()

    def add_new_anime_list(self, list_name: str, anime_list: "MediaSearchResult"):
        cards_container = MediaCardsContainer()
        cards_container.list_name = list_name.upper()
        for anime in anime_list.media:
            card = MediaCard(anime, self)
            cards_container.container.add_widget(card)
        self.main_container.add_widget(cards_container)


__all__ = ["HomeScreenView"]
