# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Inazuma
Build with: pyinstaller inazuma.spec
"""

import os
import sys
from pathlib import Path

# Import kivy_deps only on Windows
if sys.platform == 'win32':
    try:
        from kivy_deps import sdl2, glew
    except ImportError:
        sdl2 = glew = None
else:
    sdl2 = glew = None

# Get the project root directory
project_root = Path(SPECPATH)
inazuma_dir = project_root / 'inazuma'

block_cipher = None

# Collect all .kv files and other data files from inazuma package
def collect_data_files():
    """Collect all .kv, .ini, .json, and image files from the inazuma package."""
    data_files = []
    
    for root, dirs, files in os.walk(str(inazuma_dir)):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        
        for file in files:
            if file.endswith(('.kv', '.ini', '.json', '.png', '.jpg', '.jpeg', '.gif')):
                src_path = os.path.join(root, file)
                # Calculate relative destination path
                rel_path = os.path.relpath(root, str(project_root))
                data_files.append((src_path, rel_path))
    
    return data_files

def collect_viu_media_assets():
    """Collect viu_media asset files."""
    import viu_media
    viu_media_path = Path(viu_media.__file__).parent
    assets_path = viu_media_path / 'assets'
    data_files = []
    
    if assets_path.exists():
        for root, dirs, files in os.walk(str(assets_path)):
            # Skip __pycache__ directories
            dirs[:] = [d for d in dirs if d != '__pycache__']
            
            for file in files:
                src_path = os.path.join(root, file)
                # Calculate relative destination path
                rel_path = os.path.relpath(root, str(viu_media_path.parent))
                data_files.append((src_path, rel_path))
    
    return data_files

# Collect KivyMD data files
from kivymd import hooks_path as kivymd_hooks_path
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

a = Analysis(
    [str(project_root / 'inazuma' / '__main__.py')],
    pathex=[str(project_root)],
    binaries=[],
    datas=collect_data_files() + collect_viu_media_assets(),
    hiddenimports=[
        # Kivy imports
        'kivy.core.window',
        'kivy.core.window.window_sdl2',
        'kivy.core.text',
        'kivy.core.text.text_sdl2',
        'kivy.core.image',
        'kivy.core.image.img_pil',
        'kivy.core.image.img_sdl2',
        'kivy.core.image.img_ffpyplayer',
        'kivy.core.audio',
        'kivy.core.audio.audio_sdl2',
        'kivy.core.video',
        'kivy.core.video.video_ffpyplayer',
        'kivy.core.clipboard',
        'kivy.core.clipboard.clipboard_sdl2',
        'kivy.core.spelling',
        'kivy.graphics.cgl',
        'kivy.graphics.opengl',
        'kivy.uix.recycleview',
        'kivy.uix.recyclegridlayout',
        'kivy.uix.recycleboxlayout',
        
        # PIL/Pillow for image loading
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        
        # KivyMD imports
        'kivymd.uix.behaviors',
        'kivymd.uix.button',
        'kivymd.uix.card',
        'kivymd.uix.dialog',
        'kivymd.uix.label',
        'kivymd.uix.list',
        'kivymd.uix.menu',
        'kivymd.uix.navigationrail',
        'kivymd.uix.screen',
        'kivymd.uix.screenmanager',
        'kivymd.uix.scrollview',
        'kivymd.uix.textfield',
        'kivymd.uix.toolbar',
        'kivymd.uix.spinner',
        'kivymd.uix.snackbar',
        'kivymd.uix.tab',
        'kivymd.uix.chip',
        'kivymd.uix.boxlayout',
        'kivymd.uix.floatlayout',
        'kivymd.uix.gridlayout',
        'kivymd.uix.relativelayout',
        'kivymd.uix.anchorlayout',
        'kivymd.uix.widget',
        'kivymd.uix.selectioncontrol',
        'kivymd.uix.slider',
        'kivymd.uix.imagelist',
        'kivymd.uix.pickers',
        'kivymd.uix.progressindicator',
        'kivymd.uix.tooltip',
        'kivymd.uix.transition',
        'kivymd.icon_definitions',
        'kivymd.font_definitions',
        'kivymd.theming',
        
        # Inazuma modules
        'inazuma',
        'inazuma.core',
        'inazuma.core.viu',
        'inazuma.model',
        'inazuma.model.base_model',
        'inazuma.model.home_screen',
        'inazuma.model.anime_screen',
        'inazuma.model.search_screen',
        'inazuma.model.download_screen',
        'inazuma.model.my_list_screen',
        'inazuma.view',
        'inazuma.view.base_screen',
        'inazuma.view.screens',
        'inazuma.view.HomeScreen',
        'inazuma.view.AnimeScreen',
        'inazuma.view.SearchScreen',
        'inazuma.view.DownloadsScreen',
        'inazuma.view.MylistScreen',
        'inazuma.view.components',
        'inazuma.view.components.media_card',
        'inazuma.view.components.auth_modal',
        'inazuma.controller',
        'inazuma.controller.home_screen',
        'inazuma.controller.anime_screen',
        'inazuma.controller.search_screen',
        'inazuma.controller.downloads_screen',
        'inazuma.controller.my_list_screen',
        'inazuma.utility',
        'inazuma.utility.data',
        'inazuma.utility.notification',
        'inazuma.utility.observer',
        'inazuma.utility.utils',
        'inazuma.utility.kivy_markup_helper',
        
        # viu-media library
        'viu_media',
        'viu_media.core',
        'viu_media.core.config',
        'viu_media.core.config.model',
        'viu_media.core.downloader',
        'viu_media.core.downloader.base',
        'viu_media.core.downloader.downloader',
        'viu_media.core.downloader.default',
        'viu_media.core.downloader.yt_dlp',
        'viu_media.core.downloader.model',
        'viu_media.core.downloader.params',
        'viu_media.libs',
        'viu_media.libs.media_api',
        'viu_media.libs.media_api.api',
        'viu_media.libs.media_api.base',
        'viu_media.libs.media_api.anilist',
        'viu_media.libs.media_api.anilist.api',
        'viu_media.libs.media_api.anilist.types',
        'viu_media.libs.media_api.anilist.gql',
        'viu_media.libs.media_api.anilist.mapper',
        'viu_media.libs.media_api.jikan',
        'viu_media.libs.media_api.jikan.api',
        'viu_media.libs.media_api.jikan.mapper',
        'viu_media.libs.media_api.types',
        'viu_media.libs.media_api.params',
        'viu_media.libs.provider',
        'viu_media.libs.provider.anime',
        'viu_media.libs.provider.anime.provider',
        'viu_media.libs.provider.anime.base',
        'viu_media.libs.provider.anime.params',
        'viu_media.libs.provider.anime.types',
        'viu_media.libs.provider.anime.allanime',
        'viu_media.libs.provider.anime.allanime.provider',
        'viu_media.libs.provider.anime.animepahe',
        'viu_media.libs.provider.anime.animepahe.provider',
        'viu_media.libs.provider.anime.animeunity',
        'viu_media.libs.provider.anime.animeunity.provider',
        'viu_media.libs.provider.anime.utils',
        'viu_media.libs.provider.scraping',
        'viu_media.libs.provider.scraping.html_parser',
        'viu_media.libs.provider.scraping.utils',
        'viu_media.libs.player',
        'viu_media.libs.player.player',
        'viu_media.libs.player.base',
        'viu_media.libs.player.types',
        'viu_media.libs.player.params',
        'viu_media.libs.player.mpv',
        'viu_media.libs.player.mpv.player',
        'viu_media.libs.player.vlc',
        'viu_media.libs.player.vlc.player',
        'viu_media.libs.selectors',
        'viu_media.libs.selectors.selector',
        'viu_media.libs.selectors.base',
        'viu_media.libs.selectors.fzf',
        'viu_media.libs.selectors.fzf.selector',
        'viu_media.libs.selectors.inquirer',
        'viu_media.libs.selectors.inquirer.selector',
        'viu_media.libs.selectors.rofi',
        'viu_media.libs.selectors.rofi.selector',
        
        # FFpyplayer
        'ffpyplayer',
        'ffpyplayer.player',
        'ffpyplayer.pic',
        
        # Standard library / common dependencies
        'json',
        'threading',
        'functools',
        'typing',
        'dataclasses',
        'pathlib',
        'certifi',
        'requests',
        'urllib3',
        'charset_normalizer',
        'idna',
    ],
    hookspath=[kivymd_hooks_path] + hookspath(),
    hooksconfig={},
    runtime_hooks=runtime_hooks(),
    excludes=[
        'tkinter',
        'unittest',
        'pydoc',
        'doctest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='inazuma',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you need console output for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='path/to/icon.ico',  # Uncomment and set path to your icon
)

# Collect additional dependencies for Windows
extra_datas = []
if sys.platform == 'win32' and sdl2 and glew:
    extra_datas = [Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)]

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *extra_datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='inazuma',
)

# Uncomment below for macOS .app bundle
# app = BUNDLE(
#     coll,
#     name='Inazuma.app',
#     icon='path/to/icon.icns',
#     bundle_identifier='org.benexl.inazuma',
#     info_plist={
#         'CFBundleName': 'Inazuma',
#         'CFBundleDisplayName': 'Inazuma',
#         'CFBundleVersion': '3.2.7',
#         'CFBundleShortVersionString': '3.2.7',
#         'NSHighResolutionCapable': 'True',
#     },
# )
