import os
import os.path as osp
import subprocess
from constant import BASE_IMAGES, AI_USER, GITHUB_AI_TOKEN, GPUS, PLATFORM
import time
import socket
import json
from pathlib import Path
import shutil
wd = Path(__file__).parent.resolve()
from dataclasses import dataclass, field
from typing import Optional, Union, Dict
from functools import update_wrapper
from inspect import signature
import socket
@dataclass
class DockerConfig: 
    container_name: str
    workplace_name: str 
    communication_port: int # 12345
    test_pull_name: str = field(default='main')
    task_name: Optional[str] = field(default=None)
    git_clone: bool = field(default=False)
    setup_package: Optional[str] = field(default=None)
    local_root: str = field(default=os.getcwd())
    

class DockerEnv:
    def __init__(self, config: Union[DockerConfig, Dict]):
        if isinstance(config, Dict):
            config = DockerConfig(**config)
        self.workplace_name = config.workplace_name
        self.local_workplace = osp.join(config.local_root, config.workplace_name)
        self.docker_workplace = f"/{config.workplace_name}"
        self.container_name = config.container_name
        self.test_pull_name = config.test_pull_name
        self.task_name = config.task_name
        self.git_clone = config.git_clone
        self.setup_package = config.setup_package
        self.communication_port = config.communication_port

    @staticmethod
    def is_port_available(port: int) -> bool:
        """Check if a port is available for binding."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return True
            except socket.error:
                return False
        
    def init_container(self):
        container_check_command = ["docker", "ps", "-a", "--filter", f"name={self.container_name}", "--format", "{{.Names}}"]
        existing_container = subprocess.run(container_check_command, capture_output=True, text=True)
        os.makedirs(self.local_workplace, exist_ok=True)
        
        if self.setup_package is not None:
            unzip_command = ["tar", "-xzvf", f"packages/{self.setup_package}.tar.gz", "-C", self.local_workplace]
            subprocess.run(unzip_command)
        if self.git_clone:
            if not os.path.exists(os.path.join(self.local_workplace, 'metachain')):
                git_command = ["cd", self.local_workplace, "&&", "git", "clone", "-b", self.test_pull_name, f"https://{AI_USER}:{GITHUB_AI_TOKEN}@github.com/tjb-tech/metachain.git"]
                git_command = " ".join(git_command)
                
                result = subprocess.run(git_command, shell=True)
                if result.returncode != 0:
                    raise Exception(f"Failed to clone the repository. Please check your internet connection and try again.")
                # create a new branch
            new_branch_name = f"{self.test_pull_name}_{self.task_name}"
            create_branch_command = f"cd {self.local_workplace}/metachain && git checkout -b {new_branch_name}"
            result = subprocess.run(create_branch_command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(Exception(f"Failed to create and switch to new branch. Error: {result.stderr}"))
                switch_branch_command = f"cd {self.local_workplace}/metachain && git checkout {new_branch_name}"
                result = subprocess.run(switch_branch_command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"Failed to switch to new branch. Error: {result.stderr}")
                else:
                    print(f"Successfully switched to new branch: {new_branch_name}")
            else:
                print(f"Successfully created and switched to new branch: {new_branch_name}")

        if existing_container.stdout.strip() == self.container_name:
            port_info = check_container_ports(self.container_name)

            if port_info:
                # This is a valid, port-mapped container. Check if we can use it.
                self.communication_port = port_info[0]
                if not DockerEnv.is_port_available(self.communication_port):
                    raise Exception(f"Error: Container '{self.container_name}' needs port {self.communication_port}, but it's already in use by another process. Please free the port and try again.")

                running_check_command = ["docker", "ps", "--filter", f"name={self.container_name}", "--format", "{{.Names}}"]
                running_container = subprocess.run(running_check_command, capture_output=True, text=True)

                if running_container.stdout.strip() != self.container_name:
                    print(f"Attempting to start existing container '{self.container_name}' on port {self.communication_port}...")
                    try:
                        start_command = ["docker", "start", self.container_name]
                        subprocess.run(start_command, check=True, capture_output=True, text=True)
                        print(f"Container '{self.container_name}' has been started successfully.")
                    except subprocess.CalledProcessError as e:
                        raise Exception(f"Failed to start container '{self.container_name}'. Docker error: {e.stderr}")
                else:
                    print(f"Container '{self.container_name}' is already running on port {self.communication_port}.")
                return
            else:
                # This is a zombie container (created but not started, no port). Remove it.
                print(f"Warning: Found existing container '{self.container_name}' but it has no port mapping. It is likely a zombie from a failed startup. Removing it.")
                try:
                    rm_command = ["docker", "rm", "-f", self.container_name]
                    subprocess.run(rm_command, check=True, capture_output=True, text=True)
                    print(f"Removed zombie container '{self.container_name}'.")
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Failed to remove zombie container '{self.container_name}'. Docker error: {e.stderr}")
        
        # If we are here, either the container did not exist or we just removed a zombie.
        # Create a new container and let Docker assign a random available port.
        gpu_cmd = ["--gpus", GPUS] if GPUS else []
        docker_command = [
            "docker", "run", "-d", "--platform", PLATFORM, "--userns=host",] + gpu_cmd + ["--name", self.container_name,
            "--user", "root", "-v", f"{self.local_workplace}:{self.docker_workplace}",
            "-w", f"{self.docker_workplace}", "-p", "8000", # Let Docker assign a random host port
            "--restart", "unless-stopped", BASE_IMAGES
        ]
        print(f"Creating new container '{self.container_name}'...")
        print(docker_command)

        try:
            subprocess.run(docker_command, check=True, capture_output=True, text=True)

            # Discover the port that Docker assigned
            port_info = check_container_ports(self.container_name)
            if not port_info:
                raise Exception("Failed to discover port for newly created container.")
            self.communication_port = port_info[0]
            print(f"Container created successfully. Docker assigned port {self.communication_port}.")

            if self.wait_for_container_ready(timeout=60):
                print(f"Container '{self.container_name}' is ready.")
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to create container. Docker error: {e.stderr}")

    @staticmethod
    def is_port_open(host, port, timeout=2):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except Exception:
            return False

    def wait_for_container_ready(self, timeout=30):
        """using subprocess to check if the container is running"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Running}}", self.container_name],
                capture_output=True,
                text=True
            )
            print("result.returncode", result.returncode)
            print("result.stdout", result.stdout)
            
            if result.returncode == 0 and "true" in result.stdout.lower():
                # 额外检查 tcp_server 是否运行
                try:
                    port_info = check_container_ports(self.container_name)
                    if port_info:
                        host_port, container_port = port_info
                        self.communication_port = host_port

                        if DockerEnv.is_port_open("localhost", host_port):
                            result = self.run_command('ps aux')
                            print("result", result)
                            if "tcp_server.py" in result['result']:
                                return True
                        else:
                            print(f"Port {host_port} not yet open")
                except Exception as e:
                    print(f"Failed to check container ports: {e}")
                
            time.sleep(1)
            
        raise TimeoutError(f"Container {self.container_name} failed to start within {timeout} seconds")
    def stop_container(self):
        stop_command = ["docker", "stop", self.container_name]
        result = subprocess.run(stop_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to stop container: {result.stderr}")
    
    def run_command(self, command, stream_callback=None):
        """
        communicate with docker container and execute command, support stream output
        
        Args:
            command: the command to execute
            stream_callback: optional callback function, for handling stream output
                            the function signature should be callback(text: str)
        
        Returns:
            dict: the complete JSON result returned by the docker container
        """
        hostname = 'localhost'
        port = self.communication_port
        buffer_size = 4096
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((hostname, port))
            s.sendall(command.encode())
            
            partial_line = ""
            while True:
                chunk = s.recv(buffer_size)
                if not chunk:
                    break
                    
                # add new received data to the unfinished data
                data = partial_line + chunk.decode('utf-8')
                lines = data.split('\n')
                
                # except the last line, process all complete lines
                for line in lines[:-1]:
                    if line:
                        try:
                            response = json.loads(line)
                            if response['type'] == 'chunk':
                                # process stream output
                                if stream_callback:
                                    stream_callback(response['data'])
                            elif response['type'] == 'final':
                                # return the final result
                                return {
                                    'status': response['status'],
                                    'result': response['result']
                                }
                        except json.JSONDecodeError:
                            print(f"Invalid JSON: {line}")
                
                # save the possibly unfinished last line
                partial_line = lines[-1]
                
        # if the loop ends normally without receiving a final response
        return {
            'status': -1,
            'result': 'Connection closed without final response'
        }
    
def with_env(env: DockerEnv):
    """将env注入到工具函数中的装饰器"""
    def decorator(func):
        def wrapped(*args, **kwargs):
            return func(env=env, *args, **kwargs)
        
        # 保留原始函数的所有属性
        update_wrapper(wrapped, func)
        # 修改signature，移除env参数
        wrapped.__signature__ = signature(func).replace(
            parameters=[p for p in signature(func).parameters.values() if p.name != 'env']
        )
        if func.__doc__:
            try:
                if '{docker_workplace}' in func.__doc__:
                    wrapped.__doc__ = func.__doc__.format(docker_workplace=env.docker_workplace)
                else:
                    wrapped.__doc__ = func.__doc__
                if '{local_workplace}' in func.__doc__:
                    wrapped.__doc__ = func.__doc__.format(local_workplace=env.local_workplace)
                else:
                    wrapped.__doc__ = func.__doc__
            except (KeyError, IndexError, ValueError):
                # 如果格式化失败（没有占位符），保持原始文档
                wrapped.__doc__ = func.__doc__
        return wrapped
    return decorator

def check_container_ports(container_name: str):
    """
    check if the container has port mapping
    return format:
    - if the container exists and has port mapping: '0.0.0.0:12345->12345/tcp'
    - if the container does not exist or does not have port mapping: None
    """
    # use docker ps to check the container and get the port information
    container_check_command = [
        "docker", "ps", "-a",
        "--filter", f"name={container_name}",
        "--format", "{{.Ports}}"
    ]
    
    result = subprocess.run(container_check_command, capture_output=True, text=True)
    ports_info = result.stdout.strip()
    
    if not ports_info:
        return None
        
    # only process the mapped ports
    for mapping in ports_info.split(','):
        mapping = mapping.strip()
        if '->' in mapping:
            # parse '0.0.0.0:12345->12345/tcp' to (12345, 12345)
            host_part, container_part = mapping.split('->')
            host_port = host_part.split(':')[1]  # get '12345' from '0.0.0.0:12345'
            container_port = container_part.split('/')[0]  # get '12345' from '12345/tcp'
            return (int(host_port), int(container_port))  # convert to integers
    return None

def check_container_exist(container_name: str):
    container_check_command = [
        "docker", "ps", "-a",
        "--filter", f"name={container_name}",
        "--format", "{{.Names}}"
    ]
    result = subprocess.run(container_check_command, capture_output=True, text=True)
    return container_name in result.stdout.strip()

def check_container_running(container_name: str):
    container_check_command = [
        "docker", "ps",
        "--filter", f"name={container_name}",
        "--format", "{{.Names}}"
    ]
    result = subprocess.run(container_check_command, capture_output=True, text=True)
    return container_name in result.stdout.strip()
