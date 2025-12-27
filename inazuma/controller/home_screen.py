from kivy.clock import Clock
from threading import Thread
from kivy.logger import Logger

from ..model.home_screen import HomeScreenModel
from ..view.HomeScreen.home_screen import HomeScreenView


# TODO:Move the update home screen to homescreen.py
class HomeScreenController:
    """
    The `HomeScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    populate_errors = []
    _discover_anime_list = []

    def __init__(self, model: HomeScreenModel):
        self.model = model  # model.main_screen.MainScreenModel
        self.view = HomeScreenView(controller=self, model=self.model)

        self._discover_anime_list = [
            {
                "list_name": "Trending",
                "data_getter": self.model.get_trending_anime,
            },
            {
                "list_name": "Most Favourite",
                "data_getter": self.model.get_most_favourite_anime,
            },
            {
                "list_name": "Most Popular",
                "data_getter": self.model.get_most_popular_anime,
            },
            {
                "list_name": "Recent",
                "data_getter": self.model.get_most_recently_updated_anime,
            },
            {
                "list_name": "Most Scored",
                "data_getter": self.model.get_most_scored_anime,
            },
            {
                "list_name": "Upcoming",
                "data_getter": self.model.get_upcoming_anime,
            },
        ]

        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()

    def get_view(self) -> HomeScreenView:
        return self.view

    def get_more_anime(self):
        task = self._discover_anime_list.pop()
        Thread(target=self._process_anime_list, args=(task,)).start()

    def _process_anime_list(self, task):
        anime_list = task["data_getter"]()
        Clock.schedule_once(
            lambda dt: self.view.add_new_anime_list(task["list_name"], anime_list)
        )


__all__ = ["HomeScreenController"]
