"""Common constants."""
from homeassistant.const import Platform


# Base component constants
NAME = "svk_mimer"
DOMAIN = "svk_mimer"
CURRENCY = "SEK"
INTEGRATION_VERSION = "master"
ISSUE_URL = "https://github.com/robinostlund/homeassistant-svk-mimer/issues"
UPDATE_INTERVAL = 600
URL_SVK_MIMER = "https://mimer.svk.se/PrimaryRegulation/PrimaryRegulationIndex"


# Platforms
PLATFORMS = [
    Platform.SENSOR,
]

# Configuration contants
CONF_KW_AVAILABLE = "kw_available"
CONF_FEE_PERCENT = "fee_percent"
CONF_VAT = "vat"

# Default value contants
DEFAULT_KW_AVAILABLE = 1
DEFAULT_FEE_PERCENT = 0
DEFAULT_VAT = False


# Message constants
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {INTEGRATION_VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""

CURRENT_CONFIG_VER = 1

EVENT_NEW_HOUR = "svk_mimer_update_hour"
EVENT_NEW_DAY = "svk_mimer_update_day"
