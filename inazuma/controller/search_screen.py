from threading import Thread

from kivy.clock import Clock
from kivy.logger import Logger

from ..model.search_screen import SearchScreenModel
from ..view.SearchScreen.search_screen import SearchScreenView


class SearchScreenController:
    """The search screen controller"""

    is_searching = False
    search_term = ""

    def __init__(self, model: SearchScreenModel):
        self.model = model
        self.view = SearchScreenView(controller=self, model=self.model)

    def get_view(self) -> SearchScreenView:
        return self.view

    def handle_search_for_anime(self, search_widget=None, page=None):
        if search_widget:
            search_term = search_widget.text
        elif page:
            search_term = self.search_term
        else:
            search_term = ""

        if not self.is_searching:
            self.search_term = search_term
            filters = self.view.filters.filters.copy()
            filters["page"] = page if page else 1
            Thread(target=self._process_search, args=(search_term, filters)).start()

    def apply_filters(self):
        """Apply filters and search with current search term."""
        self.handle_search_for_anime(page=1)

    def add_or_update_trending(self):
        Thread(target=self._process_trending).start()

    def _process_search(self, anime_title, filters={}):
        media_list = self.model.search_for_anime(anime_title, filters)
        if not media_list:
            Logger.error(f"Search Screen:Failed to search for {anime_title}")
            return
        Clock.schedule_once(
            lambda dt: self.view.add_or_update_search_results(media_list)
        )

    def _process_trending(self):
        media_list = self.model.get_trending()
        if not media_list:
            Logger.error("Search Screen:Failed to get trending anime")
            return
        Clock.schedule_once(lambda dt: self.view.add_or_update_trending(media_list))


__all__ = ["SearchScreenController"]
