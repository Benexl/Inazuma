from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty

from ...view.base_screen import BaseScreenView
from .components.filters import Filters
from .components.pagination import SearchResultsPagination
from .components.trending_sidebar import TrendingAnimeSideBar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from viu_media.libs.media_api.types import MediaSearchResult, PageInfo
    from inazuma.controller.search_screen import SearchScreenController


class SearchScreenView(BaseScreenView):
    controller: "SearchScreenController"

    trending_anime_sidebar: TrendingAnimeSideBar = ObjectProperty()
    search_results_pagination: SearchResultsPagination = ObjectProperty()
    filters: Filters = ObjectProperty()

    search_results_container = ObjectProperty()
    search_term: str = StringProperty()
    is_searching = False
    has_next_page = False
    current_page = 0
    total_pages = 0


    def add_or_update_search_results(self, media_list: "MediaSearchResult"):
        self.update_pagination(media_list.page_info)
        self.search_results_container.data = []
        for anime in media_list.media:
            anime_card = {
                "viewclass": "MediaCard",
                "media_item": anime,
                "screen": self,
                "anime_id": anime.id,
                "title": anime.title.english,
                "episodes": str(anime.episodes),
                "popularity": str(anime.popularity),
                "favourites": str(anime.favourites),
                "media_status": str(anime.status.value),
                "genres": ", ".join([genre.value for genre in anime.genres]),
                "description": anime.description or "",
                "cover_image_url": anime.cover_image.medium
                if anime.cover_image
                else "",
                "studios": ", ".join(
                    [studio.name for studio in anime.studios if studio and studio.name]
                ),
                "tags": ", ".join([tag.name.value for tag in anime.tags]),
            }

            self.search_results_container.data.append(anime_card)

    def add_or_update_trending(self, media_list: "MediaSearchResult"):
        self.trending_anime_sidebar.data = []
        for anime in media_list.media:
            anime_card = {
                "viewclass": "MediaCard",
                "media_item": anime,
                "screen": self,
                "anime_id": anime.id,
                "title": anime.title.english,
                "episodes": str(anime.episodes),
                "popularity": str(anime.popularity),
                "favourites": str(anime.favourites),
                "media_status": str(anime.status.value),
                "genres": ", ".join([genre.value for genre in anime.genres]),
                "description": anime.description or "",
                "cover_image_url": anime.cover_image.medium
                if anime.cover_image
                else "",
                "studios": ", ".join(
                    [studio.name for studio in anime.studios if studio and studio.name]
                ),
                "tags": ", ".join([tag.name.value for tag in anime.tags]),
            }
            self.trending_anime_sidebar.data.append(anime_card)

    def update_pagination(self, pagination_info: "PageInfo"):
        self.search_results_pagination.current_page = self.current_page = (
            pagination_info.current_page
        )
        self.search_results_pagination.total_pages = self.total_pages = max(
            int(pagination_info.total / 30), 1
        )
        self.has_next_page = pagination_info.has_next_page

    def next_page(self):
        if self.has_next_page:
            page = self.current_page + 1
            self.controller.handle_search_for_anime(page=page)

    def previous_page(self):
        if self.current_page > 1:
            page = self.current_page - 1
            self.controller.handle_search_for_anime(page=page)

    def on_pre_enter(self, *args):
        self._initial_trending_loaded = False
        if not self._initial_trending_loaded:
            self.controller.add_or_update_trending()
        self._initial_trending_loaded = True


__all__ = ["SearchScreenView"]
