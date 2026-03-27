import os
import subprocess
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from pathlib import Path


# ──────────────────────────────────────────────────
#  PROJECT_DIR: all agents write files here
# ──────────────────────────────────────────────────
PROJECT_DIR = Path("output/project")


class FileWriterInput(BaseModel):
    """Input for FileWriterTool."""
    file_path: str = Field(
        ...,
        description=(
            "Relative path inside the project for the file to create "
            "(e.g., 'server.js', 'routes/students.js', 'public/index.html')"
        ),
    )
    content: str = Field(..., description="The full content to write to the file")


class FileWriterTool(BaseTool):
    name: str = "file_writer"
    description: str = (
        "Writes content to a file inside the project directory (output/project/). "
        "Creates parent directories automatically. Use this to create ANY project "
        "file: server.js, db.js, routes/*.js, controllers/*.js, public/index.html, "
        "public/js/app.js, package.json, vercel.json, SQL scripts, etc."
    )
    args_schema: Type[BaseModel] = FileWriterInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            # Block path traversal
            if ".." in file_path:
                return "Error: path traversal (..) not allowed"
            full_path = PROJECT_DIR / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            if file_path.endswith('.sh'):
                full_path.chmod(0o755)
            return f"✅ Wrote file: {full_path}"
        except Exception as e:
            return f"Error writing file: {e}"


class ShellCommandInput(BaseModel):
    """Input for ShellCommandTool."""
    command: str = Field(..., description="The shell command to execute")
    working_dir: str = Field(
        default="",
        description=(
            "Working directory (relative to project root). "
            "Leave empty to use the project directory (output/project/)."
        ),
    )


class ShellCommandTool(BaseTool):
    name: str = "shell_command"
    description: str = (
        "Executes a shell command and returns stdout+stderr. "
        "Default working directory is the project folder (output/project/). "
        "Use for: npm install, neonctl commands, git commands, vercel deploy, "
        "psql, curl to test endpoints, etc."
    )
    args_schema: Type[BaseModel] = ShellCommandInput

    def _run(self, command: str, working_dir: str = "") -> str:
        blocked = ['rm -rf /', 'mkfs', 'dd if=', ':(){', 'fork bomb']
        for b in blocked:
            if b in command.lower():
                return "Blocked: dangerous command detected"

        try:
            cwd = Path(working_dir) if working_dir else PROJECT_DIR
            cwd.mkdir(parents=True, exist_ok=True)

            env = {**os.environ, "CI": "true", "FORCE_COLOR": "0"}
            # Ensure psql and other homebrew tools are in PATH
            env["PATH"] = "/opt/homebrew/opt/libpq/bin:" + env.get("PATH", "")

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=180,
                cwd=str(cwd),
                env=env,
            )

            output = ""
            if result.stdout:
                output += f"STDOUT:\n{result.stdout[-3000:]}\n"
            if result.stderr:
                output += f"STDERR:\n{result.stderr[-2000:]}\n"
            output += f"Exit code: {result.returncode}"
            return output if output.strip() else f"Command completed (exit {result.returncode})"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 180 seconds"
        except Exception as e:
            return f"Error executing command: {e}"
            output += f"Exit code: {result.returncode}"

            return output if output.strip() else f"Command completed with exit code {result.returncode}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 120 seconds"
        except Exception as e:
            return f"Error executing command: {e}"
