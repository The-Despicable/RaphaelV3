"""Stub module for sandbox."""
import logging
logger = logging.getLogger("sandbox")


class PatchSandbox:
    def __init__(self):
        self.running = False

    async def validate_syntax(self, code: str) -> tuple[bool, str]:
        return True, ""

    async def run_code(self, code: str, timeout: int = 30) -> dict:
        return {"stdout": "", "stderr": "sandbox not available", "exit_code": -1}


sandbox = PatchSandbox()
