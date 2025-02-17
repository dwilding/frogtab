from pathlib import Path

class Read(PermissionError):
    def __init__(self, file: Path):
        super().__init__(f"unable to read file '{file}'")
        self.file = file

class Write(PermissionError):
    def __init__(self, file: Path):
        super().__init__(f"unable to write file '{file}'")
        self.file = file

class WrongVersion(Exception):
    def __init__(self, port: int, version: str):
        super().__init__(f"version {version} of Frogtab Local is running on port {port}")
        self.port = port
        self.version = version

class WrongApp(Exception):
    def __init__(self, port: int):
        super().__init__(f"a different app is using port {port}")
        self.port = port

class Running(Exception):
    def __init__(self, port: int):
        super().__init__(f"Frogtab Local is running on port {port}")
        self.port = port

class NotRunning(Exception):
    def __init__(self, port: int):
        super().__init__(f"Frogtab Local is not running on port {port}")
        self.port = port