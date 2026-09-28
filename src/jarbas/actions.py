from .task import TaskBuilder

ACTION_NAMESPACE = {}


class Actions(TaskBuilder):
    """
    Namespace that aggregates several generic actions in the context of Jarbas.
    """

    def __init__(self, tasks=None):
        super().__init__(ACTION_NAMESPACE, tasks)
