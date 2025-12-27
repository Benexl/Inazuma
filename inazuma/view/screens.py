from inazuma.controller.anime_screen import AnimeScreenController

# from inazuma.controller.downloads_screen import DownloadsScreenController
from inazuma.controller.home_screen import HomeScreenController
from inazuma.model.home_screen import HomeScreenModel

from inazuma.controller.my_list_screen import MyListScreenController
from inazuma.controller.search_screen import SearchScreenController
from inazuma.model.anime_screen import AnimeScreenModel

# from inazuma.model.download_screen import DownloadsScreenModel
from inazuma.model.my_list_screen import MyListScreenModel
from inazuma.model.search_screen import SearchScreenModel


screens = {
    "home screen": {
        "model": HomeScreenModel,
        "controller": HomeScreenController,
    },
    "anime screen": {
        "model": AnimeScreenModel,
        "controller": AnimeScreenController,
    },
    "search screen": {
        "model": SearchScreenModel,
        "controller": SearchScreenController,
    },
    "my list screen": {
        "model": MyListScreenModel,
        "controller": MyListScreenController,
    },
    # "downloads screen": {
    #     "model": DownloadsScreenModel,
    #     "controller": DownloadsScreenController,
    # },
}
