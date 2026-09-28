import logging

log = logging.getLogger('jarbas.scaffold')


def merge_files(mod, tmp, conf, mod_conf):
    """
    Execute merging of generated data with project files.

    Merging is done in a tree step way:

    1) Collect all files in <tmp>/generated/<project_slug>/* that are not
       present in the project tree and move to <tmp>/merged/.
    2) Merge each of the remaining files to to <tmp>/merged/ using their
       specific hints.
    3) Copy all files in <tmp>/merged/ to the main project root.

    Args:

    """
    job = MergeJob(mod, tmp, conf, mod_conf)
    job.run()


class MergeJob:
    """
    Namespace for functions that implement a complete merge task.
    """

    def __init__(self, mod, tmp, conf, mod_conf):
        self.mod = mod
        self.tmp = tmp
        self.conf = conf
        self.project_path = conf.project_path
        self.mod_conf = mod_conf

    def run(self):
        """
        Execute job.
        """
        self.merge_safe()
        if self.has_unmerged():
            hints = self.get_merge_hints()
            self.merge_unsafe(hints)
        self.copy_files_to_project()
        log.info('files successfully merged to project tree')

    def merge_safe(self):
        """
        Move all files from the tmp/generated folder that do not exist on the
        project tree to tmp/merged.
        """

        project_slug = self.conf['jarbas-project', 'slug']
        project = self.project_path
        merged = self.tmp.opendir('merged')
        generated = self.tmp.opendir('generated/{}'.format(project_slug))

        for dir in generated.walk.dirs():
            merged.makedirs(dir, recreate=True)

        # Copy files that can be safely merged
        merged_files = []
        for file in generated.walk.files():
            if not project.exists(file):
                merged.setbytes(file, generated.getbytes(file))
                merged_files.append(file)

        # Remove those files from the generated dir
        for file in merged_files:
            generated.remove(file)

    def merge_unsafe(self, hints):
        raise NotImplementedError

    def has_unmerged(self):
        return any(self.tmp.walk.files('generated/'))

    def get_merge_hints(self):
        raise NotImplementedError

    def copy_files_to_project(self):
        project = self.project_path
        merged = self.tmp.opendir('merged')

        for dir in merged.walk.dirs():
            project.makedirs(dir, recreate=True)

        for file in merged.walk.files():
            project.setbytes(file, merged.getbytes(file))
