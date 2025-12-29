#!/usr/bin/env python3
"""
Safe local test script for Java execution
Uses the same security measures as the deployed executor
"""

import subprocess
import tempfile
import os
import shutil
import resource
import time

# Same resource limits as production
MAX_CPU_TIME = 10
MAX_MEMORY = 1024 * 1024 * 1024  # 1GB
MAX_PROCESSES = 10
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def set_resource_limits():
    """Set resource limits for code execution (same as production)"""
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (MAX_CPU_TIME, MAX_CPU_TIME))
        resource.setrlimit(resource.RLIMIT_AS, (MAX_MEMORY, MAX_MEMORY))
        resource.setrlimit(resource.RLIMIT_NPROC, (MAX_PROCESSES, MAX_PROCESSES))
        resource.setrlimit(resource.RLIMIT_FSIZE, (MAX_FILE_SIZE, MAX_FILE_SIZE))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))  # Block core dumps
    except Exception as e:
        print(f"Warning: Could not set resource limits: {e}")

def create_sandboxed_directory():
    """Create a sandboxed temporary directory"""
    temp_dir = tempfile.mkdtemp(prefix='exec_', dir='/tmp')
    os.chmod(temp_dir, 0o700)
    return temp_dir

def test_java_execution():
    """Test Java execution with the same settings as production"""
    print("=" * 60)
    print("Safe Local Java Execution Test")
    print("=" * 60)
    print()
    
    # Test 1: Simple Java code
    print("Test 1: Simple Java code (System.out.println)")
    print("-" * 60)
    
    temp_dir = create_sandboxed_directory()
    try:
        # Write Java code
        java_file = os.path.join(temp_dir, 'Main.java')
        with open(java_file, 'w') as f:
            f.write("public class Main { public static void main(String[] args) { System.out.println(42); } }")
        
        # Clean environment (same as production)
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('JAVA') and not key.startswith('_JAVA'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        if 'JAVA_TOOL_OPTIONS' in clean_env:
            del clean_env['JAVA_TOOL_OPTIONS']
        if '_JAVA_OPTIONS' in clean_env:
            del clean_env['_JAVA_OPTIONS']
        
        # Compile
        print("Compiling Java code...")
        compile_result = subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=temp_dir,
            env=clean_env
        )
        
        if compile_result.returncode != 0:
            print(f"❌ Compilation failed:")
            print(compile_result.stderr)
            return False
        
        print("✅ Compilation successful")
        
        # Execute with same JVM flags as production
        print("Executing Java code with production JVM flags...")
        start_time = time.time()
        
        process = subprocess.Popen(
            ['java', 
             '-Xmx20m',  # 20MB heap
             '-Xms4m',   # Initial heap
             '-XX:ReservedCodeCacheSize=4m',  # Code cache
             '-XX:InitialCodeCacheSize=2m',   # Initial cache
             '-XX:MaxMetaspaceSize=12m',      # Metaspace
             '-XX:+UseSerialGC',  # Serial GC
             '-XX:+TieredCompilation',  # Tiered compilation
             '-XX:TieredStopAtLevel=1',  # Stop at C1
             '-XX:MaxDirectMemorySize=4m',  # Direct memory
             '-cp', temp_dir, 'Main'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            preexec_fn=set_resource_limits,
            cwd=temp_dir,
            env=clean_env
        )
        
        stdout, stderr = process.communicate(timeout=5)
        execution_time = time.time() - start_time
        
        if process.returncode == 0:
            print(f"✅ Execution successful (took {execution_time:.3f}s)")
            print(f"   Output: {stdout.strip()}")
            if stderr:
                print(f"   Stderr: {stderr.strip()}")
            return True
        else:
            print(f"❌ Execution failed (return code: {process.returncode})")
            print(f"   Stdout: {stdout.strip()}")
            print(f"   Stderr: {stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Execution timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print()

def test_java_with_input():
    """Test Java code with input (like the Clone Graph question)"""
    print("Test 2: Java code with input (Clone Graph pattern)")
    print("-" * 60)
    
    temp_dir = create_sandboxed_directory()
    try:
        # Write Java code (fixed version with single quotes)
        java_file = os.path.join(temp_dir, 'Main.java')
        java_code = """import java.util.*;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine().trim();
        if (s.equals("[]")) {
            System.out.println(0);
            return;
        }
        int count = 0;
        for (char c : s.toCharArray()) {
            if (c == '[') count++;
        }
        System.out.println(Math.max(0, count - 1));
    }
}"""
        
        with open(java_file, 'w') as f:
            f.write(java_code)
        
        # Clean environment
        clean_env = {}
        for key, value in os.environ.items():
            if not key.startswith('JAVA') and not key.startswith('_JAVA'):
                clean_env[key] = value
        clean_env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
        if 'JAVA_TOOL_OPTIONS' in clean_env:
            del clean_env['JAVA_TOOL_OPTIONS']
        if '_JAVA_OPTIONS' in clean_env:
            del clean_env['_JAVA_OPTIONS']
        
        # Compile
        print("Compiling Java code...")
        compile_result = subprocess.run(
            ['javac', java_file],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=temp_dir,
            env=clean_env
        )
        
        if compile_result.returncode != 0:
            print(f"❌ Compilation failed:")
            print(compile_result.stderr)
            return False
        
        print("✅ Compilation successful")
        
        # Test with different inputs
        test_cases = [
            ("[[2,4],[1,3],[2,4],[1,3]]", "4"),
            ("[[]]", "1"),
            ("[]", "0")
        ]
        
        all_passed = True
        for input_data, expected in test_cases:
            print(f"\n  Testing input: {input_data}")
            start_time = time.time()
            
            process = subprocess.Popen(
                ['java', 
                 '-Xmx20m',
                 '-Xms4m',
                 '-XX:ReservedCodeCacheSize=4m',
                 '-XX:InitialCodeCacheSize=2m',
                 '-XX:MaxMetaspaceSize=12m',
                 '-XX:+UseSerialGC',
                 '-XX:+TieredCompilation',
                 '-XX:TieredStopAtLevel=1',
                 '-XX:MaxDirectMemorySize=4m',
                 '-cp', temp_dir, 'Main'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=set_resource_limits,
                cwd=temp_dir,
                env=clean_env
            )
            
            stdout, stderr = process.communicate(input=input_data, timeout=5)
            execution_time = time.time() - start_time
            
            output = stdout.strip()
            if process.returncode == 0 and output == expected:
                print(f"    ✅ PASSED (output: {output}, time: {execution_time:.3f}s)")
            else:
                print(f"    ❌ FAILED")
                print(f"       Expected: {expected}, Got: {output}")
                if stderr:
                    print(f"       Stderr: {stderr.strip()}")
                all_passed = False
        
        return all_passed
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        print()

def check_java_version():
    """Check Java version and memory settings"""
    print("Java Environment Check")
    print("-" * 60)
    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True, timeout=5)
        print(result.stderr.strip())
        
        result = subprocess.run(['javac', '-version'], capture_output=True, text=True, timeout=5)
        print(f"Compiler: {result.stderr.strip()}")
        
        # Check available memory
        import psutil
        mem = psutil.virtual_memory()
        print(f"\nSystem Memory:")
        print(f"  Total: {mem.total / (1024**3):.2f} GB")
        print(f"  Available: {mem.available / (1024**3):.2f} GB")
        print(f"  Used: {mem.percent}%")
        
    except Exception as e:
        print(f"❌ Error checking Java: {e}")
    print()

if __name__ == '__main__':
    print()
    check_java_version()
    
    result1 = test_java_execution()
    result2 = test_java_with_input()
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Test 1 (Simple Java): {'✅ PASSED' if result1 else '❌ FAILED'}")
    print(f"Test 2 (Java with Input): {'✅ PASSED' if result2 else '❌ FAILED'}")
    print()
    
    if result1 and result2:
        print("✅ All tests passed! Java execution works locally.")
        print("   This suggests the issue might be container-specific.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print()


