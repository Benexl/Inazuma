import webbrowser
from threading import Thread
from typing import TYPE_CHECKING

from kivy.clock import Clock
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.modalview import ModalView
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import (
    BackgroundColorBehavior,
    CommonElevationBehavior,
    StencilBehavior,
)

if TYPE_CHECKING:
    from inazuma import Inazuma


class AuthPopup(
    ThemableBehavior,
    StencilBehavior,
    CommonElevationBehavior,
    BackgroundColorBehavior,
    ModalView,
):
    """Authentication popup for AniList login/logout."""

    # Properties bound to UI
    is_logged_in = BooleanProperty(False)
    username = StringProperty("")
    status_message = StringProperty("")
    is_loading = BooleanProperty(False)
    token_input = ObjectProperty(None)
    app: "Inazuma"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()  # type: ignore[assignment]

    def on_open(self):
        """Check auth status when popup opens."""
        self._check_auth_status()

    def _check_auth_status(self):
        """Check current authentication status."""
        self.is_loading = True
        Thread(target=self._check_auth_async).start()

    def _check_auth_async(self):
        """Background thread to check auth status."""
        try:
            auth_service = self.app.viu.auth
            auth_profile = auth_service.get_auth()

            if auth_profile:
                username = auth_profile.user_profile.name
                Clock.schedule_once(
                    lambda dt: self._update_logged_in_state(True, username)
                )
            else:
                Clock.schedule_once(lambda dt: self._update_logged_in_state(False, ""))
        except Exception as e:
            error_msg = f"Failed to check status: {str(e)}"
            Clock.schedule_once(lambda dt: self._show_error(error_msg))

    def _update_logged_in_state(self, logged_in: bool, username: str):
        """Update UI with login state."""
        self.is_logged_in = logged_in
        self.username = username
        self.is_loading = False
        if logged_in:
            self.status_message = f"Logged in as {username}"
        else:
            self.status_message = "Not logged in"

    def open_anilist_auth(self):
        """Open AniList auth page in browser."""
        from viu_media.core.constants import ANILIST_AUTH

        try:
            webbrowser.open(ANILIST_AUTH, new=2)
            self.status_message = (
                "Browser opened. Paste your token below after authorizing."
            )
        except Exception:
            self.status_message = (
                "Failed to open browser. Please visit AniList manually."
            )

    def login_with_token(self, token: str):
        """Authenticate with the provided token."""
        if not token or not token.strip():
            self.status_message = "Please enter a valid token."
            return

        self.is_loading = True
        self.status_message = "Authenticating..."
        Thread(target=self._login_async, args=(token.strip(),)).start()

    def _login_async(self, token: str):
        """Background thread for login."""
        try:
            from viu_media.libs.media_api.api import create_api_client

            api_client = create_api_client(
                self.app.viu.config.general.media_api, self.app.viu.config
            )

            # Validate token and get profile
            profile = api_client.authenticate(token)

            if profile:
                # Save credentials
                auth_service = self.app.viu.auth
                auth_service.save_user_profile(profile, token)

                # Reset viu services to pick up new auth
                self.app.viu.reset()

                Clock.schedule_once(lambda dt: self._on_login_success(profile.name))
            else:
                Clock.schedule_once(
                    lambda dt: self._show_error("Invalid or expired token.")
                )
        except Exception as e:
            error_msg = f"Login failed: {str(e)}"
            Clock.schedule_once(lambda dt: self._show_error(error_msg))

    def _on_login_success(self, username: str):
        """Handle successful login."""
        self.is_logged_in = True
        self.username = username
        self.is_loading = False
        self.status_message = f"Successfully logged in as {username}! ✨"
        # Clear token input
        if self.token_input:
            self.token_input.text = ""

    def logout(self):
        """Log out and clear credentials."""
        self.is_loading = True
        Thread(target=self._logout_async).start()

    def _logout_async(self):
        """Background thread for logout."""
        try:
            auth_service = self.app.viu.auth
            auth_service.clear_user_profile()

            # Reset viu services
            self.app.viu.reset()

            Clock.schedule_once(lambda dt: self._on_logout_success())
        except Exception as e:
            error_msg = f"Logout failed: {str(e)}"
            Clock.schedule_once(lambda dt: self._show_error(error_msg))

    def _on_logout_success(self):
        """Handle successful logout."""
        self.is_logged_in = False
        self.username = ""
        self.is_loading = False
        self.status_message = "You have been logged out."

    def _show_error(self, message: str):
        """Show error message."""
        self.is_loading = False
        self.status_message = message
