from inazuma.Controller.anime_screen import AnimeScreenController

# from inazuma.Controller.downloads_screen import DownloadsScreenController
from inazuma.Controller.home_screen import HomeScreenController
from inazuma.Model.home_screen import HomeScreenModel

# from inazuma.Controller.my_list_screen import MyListScreenController
from inazuma.Controller.search_screen import SearchScreenController
from inazuma.Model.anime_screen import AnimeScreenModel

# from inazuma.Model.download_screen import DownloadsScreenModel
# from inazuma.Model.my_list_screen import MyListScreenModel
from inazuma.Model.search_screen import SearchScreenModel


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
    # "my list screen": {
    #     "model": MyListScreenModel,
    #     "controller": MyListScreenController,
    # },
    # "downloads screen": {
    #     "model": DownloadsScreenModel,
    #     "controller": DownloadsScreenController,
    # },
}
