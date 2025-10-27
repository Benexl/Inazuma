from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    ObjectProperty,
    StringProperty,
)
from kivymd.app import MDApp
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from viu_media.libs.media_api.types import MediaItem

from .components.media_popup import MediaPopup


class MediaCard(HoverBehavior, MDBoxLayout):
    screen = ObjectProperty()
    anime_id = NumericProperty()
    title = StringProperty()
    is_play = ObjectProperty()
    trailer_url = StringProperty()
    _trailer_url: str | None = StringProperty(allow_none=True)
    episodes = StringProperty()
    favourites = StringProperty()
    popularity = StringProperty()
    media_status = StringProperty("Releasing")
    is_in_my_list = BooleanProperty(False)
    is_in_my_notify = BooleanProperty(False)
    genres = StringProperty()
    first_aired_on = StringProperty()
    description = StringProperty()
    producers = StringProperty()
    studios = StringProperty()
    next_airing_episode = StringProperty()
    tags = StringProperty()
    stars = ListProperty([0, 0, 0, 0, 0, 0])
    cover_image_url = StringProperty()
    preview_image = StringProperty()
    has_trailer_color = ListProperty([0.5, 0.5, 0.5, 0.5])
    _popup_opened = False
    _title = ()

    def __init__(self, media_item: MediaItem, **kwargs):
        super().__init__(**kwargs)
        self.media_item = media_item
        self.anime_id = media_item.id
        self.title = media_item.title.english
        self.episodes = str(media_item.episodes)
        self.popularity = str(media_item.popularity)
        self.favourites = str(media_item.favourites)
        self.media_status = str(media_item.status.value)
        self.genres = ", ".join([genre.value for genre in media_item.genres])
        self.description = media_item.description or ""
        self.cover_image_url = (
            media_item.cover_image.medium if media_item.cover_image else ""
        )
        self.studios = ", ".join(
            [studio.name for studio in media_item.studios if studio and studio.name]
        )
        self.tags = ", ".join([tag.name.value for tag in media_item.tags])

        self.orientation = "vertical"
        self.app: MDApp | None = MDApp.get_running_app()
        self.adaptive_size = True

    def on_touch_down(self, touch):
        if touch.is_mouse_scrolling:
            return False
        if not self.collide_point(touch.x, touch.y):
            return False
        if self in touch.ud:
            return False

        if not self.app:
            return False
        disabled = True
        # FIXME: double tap not working
        #
        if not disabled and touch.is_double_tap:
            self.app.show_anime_screen(self.anime_id, self.screen.name)
            touch.grab(self)
            touch.ud[self] = True
            self.last_touch = touch

        elif self.collide_point(*touch.pos):
            if not self._popup_opened:
                Clock.schedule_once(self.open)
            self._popup_opened = True
            touch.grab(self)
            touch.ud[self] = True
            self.last_touch = touch
            return True
        else:
            super().on_touch_down(touch)

    # FIXME: Figure a good way implement this
    # for now its debugy so scraping it till fix
    def on_enter(self):
        def _open_popup(dt):
            if self.hovering:
                window = self.get_parent_window()
                if window:
                    for widget in window.children:  # type: ignore
                        if isinstance(widget, MediaPopup):
                            return
                    self.open()

        # Clock.schedule_once(_open_popup, 5)

    def on_popup_open(self, popup: MediaPopup):
        popup.center = self.center

    def on_dismiss(self, popup: MediaPopup):
        popup.player.state = "stop"
        self._popup_opened = False
        #   if popup.player._video:
        #       popup.player._video.unload()

    def set_preview_image(self, image):
        self.preview_image = image

    def set_trailer_url(self, trailer_url):
        self.trailer_url = trailer_url

    def open(self, *_):
        if app := self.app:
            popup: MediaPopup = app.media_card_popup
            # self.popup.caller = self
            popup.update_caller(self)
            popup.title = self.title
            popup.bind(on_dismiss=self.on_dismiss, on_open=self.on_popup_open)
            popup.open(self)

    # ---------------respond to user actions and call appropriate model-------------------------
    def on_is_in_my_list(self, instance, in_user_anime_list):
        if self.screen:
            if in_user_anime_list:
                self.screen.app.add_anime_to_user_anime_list(self.anime_id)
            else:
                self.screen.app.remove_anime_from_user_anime_list(self.anime_id)

    def on_trailer_url(self, *args):
        pass


Factory.register("MediaCard", MediaCard)


class MediaCardsContainer(MDBoxLayout):
    container = ObjectProperty()
    list_name = StringProperty()
