from kivy.clock import Clock
from threading import Thread
from kivy.logger import Logger


from inazuma.model.my_list_screen import MyListScreenModel
from inazuma.view.MylistScreen.my_list_screen import MyListScreenView


class MyListScreenController:
    """
    The `MyListScreenController` class represents a controller implementation.
    Coordinates work of the view with the model.
    The controller implements the strategy pattern. The controller connects to
    the view to control its actions.
    """

    def __init__(self, model: MyListScreenModel):
        self.model = model
        self.view = MyListScreenView(controller=self, model=self.model)

        self._discover_anime_list = [
            {
                "list_name": "Watching",
                "data_getter": self.model.get_watching,
            },
            {
                "list_name": "Repeating",
                "data_getter": self.model.get_repeating,
            },
            {
                "list_name": "Paused",
                "data_getter": self.model.get_paused,
            },
            {
                "list_name": "Planning",
                "data_getter": self.model.get_planning,
            },
            {
                "list_name": "Completed",
                "data_getter": self.model.get_completed,
            },
            {
                "list_name": "Dropped",
                "data_getter": self.model.get_dropped,
            },
        ]
    def get_all_anime_lists(self):
        if not self._discover_anime_list:
            return
        self._discover_anime_list.reverse()

        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()
        self.get_more_anime()

    def get_view(self) -> MyListScreenView:
        return self.view

    def get_more_anime(self):
        task = self._discover_anime_list.pop()
        Thread(target=self._process_anime_list, args=(task,)).start()

    def _process_anime_list(self, task):
        anime_list = task["data_getter"]()
        Clock.schedule_once(
            lambda dt: self.view.add_new_anime_list(task["list_name"], anime_list)
        )


__all__ = ["MyListScreenController"]
