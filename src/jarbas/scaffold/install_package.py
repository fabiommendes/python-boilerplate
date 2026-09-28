import logging
import os
from pprint import pformat

import fs
from cookiecutter.generate import generate_files
from fs.osfs import OSFS

from . import hooks
from .merge_files import MergeJob

log = logging.getLogger('jarbas.scaffold')


def install_package_from_module(mod, conf, clean=True):
    """
    Install Jarbas package.

    Args:
        mod (module):
            Python module that implements the jarbas package.
        conf (ProjectConfig):
            Project configuration.
    """

    job = InstallPackageFromModuleJob(mod, conf)
    job.run()
    if clean:
        job.clean()


class InstallPackageFromModuleJob:
    """
    Private namespace that implements install_package_from_module.
    """

    tmp_path = 'build/jarbas-scaffold/'

    def __init__(self, module, conf):
        self.mod = module
        self.conf = conf
        self.tmp = None
        self.mod_conf = None
        self.project_path = conf.project_path

    def run(self):
        self.tmp = self.prepare_build_files()
        self.prompt_user()
        self.prepare_mod_conf()
        self.prepare_cookiecutter()
        self.run_cookiecutter()
        self.merge_files()
        self.update_config()
        self.tmp.close()

    def clean(self):
        """
        Clean temporary files.
        """
        self.project_path.removetree(self.tmp_path)
        if not (any(self.project_path.walk.files('build')) or
                    any(self.project_path.walk.dirs('build'))):
            self.project_path.removetree('build')
        self.tmp.close()

    def prepare_build_files(self):
        """
        This function is always executed by Jarbas prior to the prepare_empty()
        function in a Jarbas plugin package.

        Steps:

        * Create the <project>/build/jarbas-scaffold/ as tmp.
        * Copy the module's cookiecutter template to the cookiecutter-data/
          folder under it.
        * Execute the preparation hook of the Jarbas package.
        """

        # Prepare empty dirs
        tmp = self.conf.makedir(self.tmp_path)
        tmp.makedir('generated')
        tmp.makedir('merged')

        # Copy Jarbas package cookiecutter-data template to the build folder.
        cookie_dest = tmp.makedir('cookiecutter-data')
        cookie_source = get_package_cookiecutter_data(self.mod)
        fs.copy.copy_fs(cookie_source, cookie_dest)

        # Prepare template using the prepare_empty hook.
        method = get_hook(self.mod, 'prepare_empty')
        method(tmp, self.conf)
        log.info('temporary installation directory is prepared')

        return tmp

    def prompt_user(self):
        method = get_hook(self.mod, 'prompt_user')
        self.mod_conf = method(self.tmp, self.conf)

    def prepare_mod_conf(self):
        """
        Calls mod.prepare_mod_conf and than update mod_conf with the required
        variables.
        """
        method = get_hook(self.mod, 'prepare_mod_conf')
        self.mod_conf = method(self.tmp, self.conf, self.mod_conf)

        # Required variables
        self.mod_conf['jarbas_package_name'] = self.mod.__name__
        for key, value in self.conf['jarbas-author'].items():
            self.mod_conf['author_' + key] = value
        for key, value in self.conf['jarbas-project'].items():
            self.mod_conf['project_' + key] = value

    def prepare_cookiecutter(self):
        method = get_hook(self.mod, 'prepare_cookiecutter')
        method(self.tmp, self.conf, self.mod_conf)
        log.info('cookiecutter ready to be executed')
        log.info('package configuration: ', pformat(self.mod_conf))

    def run_cookiecutter(self):
        path = self.tmp.getsyspath('cookiecutter-data/')
        output_path = self.tmp.getsyspath('generated/')
        context = self.mod_conf.copy()
        context['cookiecutter'] = context.copy()
        generate_files(path, context=context, output_dir=output_path,
                       overwrite_if_exists=True)
        log.info('cookiecutter successfully executed')

    def merge_files(self):
        """
        Move files from the tmp/generated/ folder to the main project structure.
        """
        merge_job = MergeJob(self.mod, self.tmp, self.conf, self.mod_conf)
        merge_job.run()

    def update_config(self):
        try:
            method = self.mod.contribute_to_config
        except AttributeError:
            pass
        else:
            self.conf.update(method(self.tmp, self.conf, self.mod_conf))


def get_package_cookiecutter_data(mod):
    mod_path = os.path.dirname(mod.__file__)
    return OSFS(mod_path).opendir('cookiecutter-data')


def get_hook(mod, attr):
    try:
        return getattr(mod, attr)
    except AttributeError:
        return getattr(hooks, attr)
