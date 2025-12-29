"""Resource limits configuration"""
import resource
from executor_service.config import MAX_CPU_TIME, MAX_MEMORY, MAX_PROCESSES, MAX_FILE_SIZE

def set_resource_limits():
    """Set resource limits for code execution"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except Exception:
        pass

