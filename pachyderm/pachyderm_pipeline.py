import jsonpickle
from typing import Optional
from typing import Iterable


class Pipeline(object):
    def __init__(self,
                 name=""
                 ):
        self.name = name


class Transform(object):
    def __init__(self,
                 image="",
                 cmd=[],
                 stdin=[],
                 env=[],
                 accept_return_code=[],
                 working_dir=""
                 ):
        self.image = image
        self.cmd = cmd
        self.stdin = stdin
        self.env = env
        self.accept_return_code = accept_return_code
        self.working_dir = working_dir


class ResourceRequests(object):
    def __init__(self,
                 memory: str = "",
                 cpu: str = "",
                 disk: str = ""
                 ):
        self.memory = memory
        self.cpu = cpu
        self.disk = disk


class ResourceLimits(object):
    def __init__(self,
                 memory: str = "",
                 cpu: str = "",
                 disk: str = ""
                 ):
        self.memory = memory
        self.cpu = cpu
        self.disk = disk


class Pfs(object):
    def __init__(self,
                 name: str = "",
                 repo: str = "",
                 branch: str = "",
                 glob: str = "",
                 lazy: bool = False,
                 empty_files: bool = False
                 ):
        self.name = name
        self.repo = repo
        self.branch = branch
        self.glob = glob
        self.lazy = lazy
        self.empty_files = empty_files


class Input(object):
    def __init__(self,
                 pfs: Optional[Pfs] = None,
                 cross: Iterable[Pfs] = [],
                 union: Iterable[Pfs] = []
                 ):
        self.pfs = pfs
        self.cross = cross
        self.union = union


class PipelineDef(object):

    def __init__(self,
                 pipeline: Pipeline = Pipeline(),
                 description: str = "",
                 transform: Transform = Transform(),
                 resource_requests: ResourceRequests = ResourceRequests(),
                 resource_limits: ResourceLimits = ResourceLimits(),
                 job_timeout: str = "",
                 input: Input = Input()
                 ):
        self.pipeline = pipeline
        self.description = description
        self.transform = transform
        self.resource_requests = resource_requests
        self.resource_limits = resource_limits
        self.job_timeout = job_timeout
        self.input = input

    def toJson(self):
        return jsonpickle.encode(self, unpicklable=False)
