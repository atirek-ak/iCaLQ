import json

class CodeInfraConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CodeInfraConfig, cls).__new__(cls)
            with open("config/code_infra.json", 'r') as f:
                cls._config = json.load(f)
        return cls._instance

    def get(self, key, default=None):
        return self._config.get(key, default)
    
class FilePathsConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FilePathsConfig, cls).__new__(cls)
            with open("config/file_paths.json", 'r') as f:
                cls._config = json.load(f)
        return cls._instance

    def get(self, key, default=None):
        return self._config.get(key, default)

class PhysicsConfig:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PhysicsConfig, cls).__new__(cls)
            with open("config/physics.json", 'r') as f:
                cls._config = json.load(f)
        return cls._instance

    def get(self, key, default=None):
        return self._config.get(key, default)

# Create the singleton instance at module level so that it is shared by all the modules that import this module
code_infra_config = CodeInfraConfig()
file_paths_config = FilePathsConfig()
physics_config = PhysicsConfig()
