from kivy.properties import DictProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.menu import MDDropdownMenu
from viu_media.libs.media_api.types import MediaSort, MediaStatus


class FilterDropDown(MDDropDownItem):
    text: str = StringProperty()


class Filters(MDBoxLayout):
    filters: dict = DictProperty(
        {"sort": MediaSort.SEARCH_MATCH.value, "status": "DISABLED"}
    )

    def open_filter_menu(self, menu_item, filter_name):
        items = []
        match filter_name:
            case "sort":
                items = [f for f in MediaSort.__members__.keys()]
            case "status":
                items = [f for f in MediaStatus.__members__.keys()]
                items.append("DISABLED")
            case _:
                items = []
        if items:
            menu_items = [
                {
                    "text": f"{item}",
                    "on_release": lambda filter_value=f"{item}": self._filter_menu_callback(
                        filter_name, filter_value
                    ),
                }
                for item in items
            ]
            MDDropdownMenu(caller=menu_item, items=menu_items).open()

    def _filter_menu_callback(self, filter_name, filter_value):
        match filter_name:
            case "sort":
                self.ids.sort_filter.text = filter_value
                self.filters["sort"] = filter_value
            case "status":
                self.ids.status_filter.text = filter_value
                self.filters["status"] = filter_value
