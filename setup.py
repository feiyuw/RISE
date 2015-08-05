import os
from IPython import release

ipython_version = release.version

livereveal_dir = os.path.join(os.path.dirname(__file__), 'livereveal')

if ipython_version <= '3.2.1':
    from IPython.html.nbextensions import install_nbextension
    from IPython.html.services.config import ConfigManager
    from IPython.utils.path import locate_profile

    default_profile = 'default'

    def get_config_manager(profile):
        profile_dir = locate_profile(profile)
        return ConfigManager(profile_dir=profile_dir)
else:
    from notebook.nbextensions import install_nbextension
    from notebook.services.config import ConfigManager
    from jupyter_core.paths import jupyter_config_dir as get_jupyter_config_dir

    default_profile = get_jupyter_config_dir()

    def get_config_manager(profile):
        return ConfigManager(config_dir=profile)


def install(use_symlink=False, profile=default_profile, enable=True):
    # Install the livereveal code.
    install_nbextension(livereveal_dir, symlink=use_symlink,
                        overwrite=use_symlink, user=True)

    if enable:
        # Enable the extension in the given profile.
        cm = get_config_manager(profile)
        cm.update('notebook', {"load_extensions": {"livereveal/main": True}})


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='valid subcommands',
                                       help='additional help')

    install_parser = subparsers.add_parser('install')
    install_parser.add_argument('--profile', action='store', default=default_profile,
                                help=("The name of the profile to use or the jupyter config directory."))
    install_parser.add_argument('--develop', action='store_true',
                                help="Install livereveal  as a symlink to the source.")
    install_parser.add_argument('--no-enable', action='store_true',
                                help="Install but don't enable the extension.")

    args = parser.parse_args(sys.argv[1:])

    install(profile=args.profile,
            use_symlink=args.develop,
            enable=(not args.no_enable))


if __name__ == '__main__':
    main()
