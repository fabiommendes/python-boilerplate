import json

from cookiecutter.generate import generate_context
from cookiecutter.prompt import prompt_for_config

import ezio
from .msgs import PRE_GEN_PROJECT_DATA, POST_GEN_PROJECT_DATA


def prepare_empty(tmp, conf):
    """
    Prepare build directory after copying the cookiecutter template to the
    cookiecutter-data and creating empty "package" and "merged" folders.

    The default implementation is a no-op. Packages may want to use it to add
    additional content to the cookiecutter template that depends only on the
    project configuration rather than on the user supplied data.
    """


def prompt_user(tmp, conf):
    """
    Asks for user input and generate a JSON structure that is used as
    configuration for the following steps.

    Default strategy:
    1. Check if cookiecutter.ezio exists. Initialize a namespace with the
    contents of cookiecutter.json and execute the ezio interaction.
    2. If cookiecutter.ezio does not exist, load cookiecutter.json using the
    same UI as cookiecutter.
    3. If neither file exist. Just return an empty dict.
    """

    if tmp.exists('cookiecutter-data/cookiecutter.ezio'):
        return prompt_user_from_ezio_data(tmp, conf)
    elif tmp.exists('cookiecutter-data/cookiecutter.json'):
        return prompt_user_from_json_data(tmp, conf)
    else:
        return {}


def prompt_user_from_ezio_data(tmp, conf):
    """
    Use cookiecutter-data/cookiecutter.ezio to interact with the user.
    """

    # Load initial data
    if tmp.exists('cookiecutter-data/cookiecutter.json'):
        with tmp.open('cookiecutter-data/cookiecutter.json') as F:
            namespace = json.load(F)
    else:
        namespace = {}

    # Run ezio interaction
    with tmp.open('cookiecutter-data/cookiecutter.ezio') as F:
        data = F.read()
    return ezio.interact(data, namespace, format=True)


def prompt_user_from_json_data(tmp, conf):
    """
    Use cookiecutter to interact with the user.
    """

    cfg_path = 'cookiecutter-data/cookiecutter.json'
    context = generate_context(tmp.getsyspath(cfg_path))
    return prompt_for_config(context)


def prepare_mod_conf(tmp, conf, mod_conf):
    """
    Prepare the mod_conf dictionary after user input.
    """
    return mod_conf


def prepare_cookiecutter(tmp, conf, mod_conf):
    """
    This method is executed after collecting user input into mod_conf and is
    the final change to modify the cookiecutter before file generation.

    The default implementation does a few standard modifications to the
    cookiecutter structure:

    1. Create the cookiecutter-data/hooks/(pre|post)_gen_project.py that simply
       calls the module's pre_gen_project and post_gen_project functions.
    2. Persist mod_conf as cookiecutter-data/mod-conf.json
    """
    hooks = tmp.makedirs('cookiecutter-data/hooks/', recreate=True)
    package_name = mod_conf['jarbas_package_name']

    # Generate pre/post gen hooks
    pre_gen = PRE_GEN_PROJECT_DATA.format(package_name=package_name)
    post_gen = POST_GEN_PROJECT_DATA.format(package_name=package_name)

    with hooks.open('pre_gen_project.py', 'w') as file:
        file.write(pre_gen)
    with hooks.open('post_gen_project.py', 'w') as file:
        file.write(post_gen)

    # Save mod_conf
    conf = {k: v for k, v in mod_conf.items() if not k.startswith('$')}
    with tmp.open('cookiecutter-data/cookiecutter.json', 'w') as file:
        json.dump(conf, file)
