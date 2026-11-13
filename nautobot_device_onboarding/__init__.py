"""App declaration for nautobot_device_onboarding."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig



def _version():
    """The installed distribution's version, or the source checkout's when the app runs uninstalled.

    An app can be put on the import path without being pip-installed (a git checkout on PYTHONPATH, a
    bind-mounted apps directory). It then has no package metadata and `metadata.version` raises
    PackageNotFoundError, which Nautobot reports as "Unable to import plugin" and refuses to start.
    """
    try:
        return metadata.version(__name__)
    except metadata.PackageNotFoundError:
        import pathlib  # pylint: disable=import-outside-toplevel

        pyproject = pathlib.Path(__file__).resolve().parent.parent / "pyproject.toml"
        try:
            import tomllib  # pylint: disable=import-outside-toplevel  # Python 3.11+

            with pyproject.open("rb") as handle:
                return tomllib.load(handle)["tool"]["poetry"]["version"]
        except (ImportError, OSError, KeyError, ValueError):  # TOMLDecodeError is a ValueError
            return "0.0.0"


__version__ = _version()


class NautobotDeviceOnboardingConfig(NautobotAppConfig):
    """App configuration for the nautobot_device_onboarding app."""

    name = "nautobot_device_onboarding"
    verbose_name = "Device Onboarding"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App that simplifies device onboarding (and re-onboarding) by \
                   collecting and populating common device 'facts' into Nautobot."
    base_url = "nautobot-device-onboarding"
    required_settings = []
    default_settings = {
        "create_platform_if_missing": True,
        "create_manufacturer_if_missing": True,
        "create_device_type_if_missing": True,
        "create_device_role_if_missing": True,
        "default_device_role": "network",
        "default_device_role_color": "ff0000",
        "default_management_interface": "PLACEHOLDER",
        "default_management_prefix_length": 0,
        "default_device_status": "Active",
        "default_ip_status": "Active",
        "create_management_interface_if_missing": True,
        "skip_device_type_on_update": False,
        "skip_manufacturer_on_update": False,
        "platform_map": {},
        "assign_secrets_group": False,
        "set_management_only_interface": False,
        "onboarding_extensions_map": {
            "ios": "nautobot_device_onboarding.onboarding_extensions.ios",
        },
        "object_match_strategy": "loose",
    }
    docs_view_name = "plugins:nautobot_device_onboarding:docs"
    home_view_name = "extras:job_list"  # Jobs only for now. May change in the future.
    searchable_models = []


config = NautobotDeviceOnboardingConfig  # pylint:disable=invalid-name
