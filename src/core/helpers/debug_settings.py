from typing import Tuple

DEFAULT_DEBUG_APPS: Tuple = ('debug_toolbar',)
DEFAULT_DEBUG_MIDDLEWARES: Tuple = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)
DEFAULT_DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True
}
DEFAULT_DEBUG_INTERNAL_IPS: Tuple = ('127.0.0.1',)
PANELS: str = 'debug_toolbar.panels.'
DEFAULT_DEBUG_TOOLBAR_PANELS: Tuple = (
    f'{PANELS}versions.VersionsPanel', f'{PANELS}timer.TimerPanel',
    f'{PANELS}settings.SettingsPanel', f'{PANELS}headers.HeadersPanel',
    f'{PANELS}request.RequestPanel', f'{PANELS}sql.SQLPanel',
    f'{PANELS}staticfiles.StaticFilesPanel',
    f'{PANELS}templates.TemplatesPanel', f'{PANELS}cache.CachePanel',
    f'{PANELS}signals.SignalsPanel', f'{PANELS}logging.LoggingPanel',
    f'{PANELS}redirects.RedirectsPanel',
)
