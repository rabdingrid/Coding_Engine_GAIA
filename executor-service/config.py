"""Configuration constants and settings"""
import os

# Resource limits for security
MAX_CPU_TIME = 10  # seconds
MAX_MEMORY = 1024 * 1024 * 1024  # 1GB
MAX_PROCESSES = 50
EXECUTION_TIMEOUT = 5  # seconds
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_CODE_LENGTH = 100 * 1024  # 100KB
MAX_INPUT_SIZE = 10 * 1024  # 10KB
MAX_OUTPUT_SIZE = 10 * 1024  # 10KB

# Database - SECURITY FIX: Require environment variable, no hardcoded fallback
# Note: Will raise error when database.py tries to use it if not set
DATABASE_URL = os.environ.get('DATABASE_URL')

# Rate limits
RATE_LIMIT_RUN = "50 per minute"
RATE_LIMIT_RUNALL = "1000 per minute"
RATE_LIMIT_SUBMIT = "200 per minute"

# Blocked patterns for code sanitization
BLOCKED_PATTERNS = {
    'python': [
        r'import\s+os\b',
        r'from\s+os\s+import',
        r'import\s+subprocess\b',
        r'from\s+subprocess\s+import',
        r'import\s+sys\b',
        r'from\s+sys\s+import',
        r'__import__\s*\(',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\([^)]*[\'"]w[\'"]',
        r'open\s*\([^)]*[\'"]a[\'"]',
    ],
    'javascript': [
        r'require\s*\(\s*[\'"]fs[\'"]',
        r'require\s*\(\s*[\'"]child_process[\'"]',
        r'require\s*\(\s*[\'"]os[\'"]',
        r'eval\s*\(',
        r'Function\s*\(',
        r'process\.(exec|fork|spawn|kill|chdir|cwd|umask|setuid|setgid)',
        r'process\.(nextTick|_kill|_fatalException)',
    ],
    'java': [
        r'java\.io\.File',
        r'java\.net\.',
        r'Runtime\.getRuntime',
        r'ProcessBuilder',
        r'Process',
    ],
    'cpp': [
        r'#include\s*<fstream>',
        r'#include\s*<sys/socket\.h>',
        r'system\s*\(',
        r'popen\s*\(',
    ],
    'csharp': [
        r'System\.IO\.File',
        r'System\.Net\.',
        r'System\.Diagnostics\.Process',
        r'System\.Runtime\.InteropServices',
        r'DllImport',
        r'Marshal\.',
        r'File\.',
        r'Directory\.',
        r'Process\.Start',
    ]
}

BLOCKED_NETWORK_PATTERNS = [
    r'socket\.',
    r'urllib\.',
    r'requests\.',
    r'http\.',
    r'https\.',
    r'fetch\s*\(',
    r'XMLHttpRequest',
]

