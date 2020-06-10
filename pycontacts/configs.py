"""
All configurations for pymakehelper
"""


from pytconf.config import Config, ParamCreator


class ConfigSymlinkInstall(Config):
    """
    Parameters for the symlink install tool
    """
    source_folder = ParamCreator.create_existing_folder(
        help_string="Which folder to install from?",
    )
    target_folder = ParamCreator.create_existing_folder(
        help_string="Which folder to install to?",
    )
    recurse = ParamCreator.create_bool(
        help_string="should I recurse?",
        default=True,
    )
    doit = ParamCreator.create_bool(
        help_string="actually perform the actions?",
        default=True,
    )
    debug = ParamCreator.create_bool(
        help_string="print what we are doing?",
        default=True,
    )
    force = ParamCreator.create_bool(
        help_string="remove target files if they are links?",
        default=True,
    )


class ConfigRemoveFolders(Config):
    """
    Parameters for the remove folder tool
    """
    filenames = ParamCreator.create_list_str(


    )
