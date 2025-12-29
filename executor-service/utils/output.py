"""Output normalization and comparison"""
def normalize_output(output: str) -> str:
    """Normalize output for comparison"""
    if not output:
        return ""
    return output.rstrip()

def compare_outputs(actual: str, expected: str) -> bool:
    """Compare actual output with expected output"""
    return normalize_output(actual) == normalize_output(expected)

