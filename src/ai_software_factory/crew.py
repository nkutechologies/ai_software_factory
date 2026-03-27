from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from ai_software_factory.tools.deployment_tools import FileWriterTool, ShellCommandTool

# Shared tool instances
_file_writer = FileWriterTool()
_shell_command = ShellCommandTool()
_code_tools = [_file_writer, _shell_command]


@CrewBase
class AiSoftwareFactory():
    """AI Software Factory Pipeline crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # ─── Agents ───────────────────────────────────────────────

    @agent
    def requirement_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['requirement_analyst'],
            verbose=True
        )

    @agent
    def architecture_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['architecture_agent'],
            verbose=True
        )

    @agent
    def planning_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['planning_agent'],
            verbose=True
        )

    @agent
    def database_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['database_engineer'],
            verbose=True,
            tools=_code_tools
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            verbose=True,
            tools=_code_tools
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            verbose=True,
            tools=_code_tools
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],
            verbose=True,
            tools=[_shell_command]
        )

    @agent
    def evaluation_engine(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluation_engine'],
            verbose=True
        )

    @agent
    def git_integration_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['git_integration_agent'],
            verbose=True,
            tools=_code_tools
        )

    @agent
    def deployment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['deployment_agent'],
            verbose=True,
            tools=_code_tools
        )

    # ─── Tasks (sequential order) ─────────────────────────────

    @task
    def requirement_task(self) -> Task:
        return Task(
            config=self.tasks_config['requirement_task'],
            output_file='output/01_srs.md'
        )

    @task
    def architecture_task(self) -> Task:
        return Task(
            config=self.tasks_config['architecture_task'],
            output_file='output/02_architecture.md'
        )

    @task
    def planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['planning_task'],
            output_file='output/03_task_plan.json'
        )

    @task
    def database_task(self) -> Task:
        # Agent writes real files with file_writer + creates hosted DB
        return Task(
            config=self.tasks_config['database_task'],
        )

    @task
    def backend_task(self) -> Task:
        # Agent writes real code files with file_writer
        return Task(
            config=self.tasks_config['backend_task'],
        )

    @task
    def frontend_task(self) -> Task:
        # Agent writes real code files with file_writer
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def qa_task(self) -> Task:
        # Agent tests with shell_command (curl)
        return Task(
            config=self.tasks_config['qa_task'],
        )

    @task
    def evaluation_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluation_task'],
            output_file='output/08_evaluation.json'
        )

    @task
    def git_integration_task(self) -> Task:
        # Agent pushes to GitHub with shell_command
        return Task(
            config=self.tasks_config['git_integration_task'],
        )

    @task
    def deployment_task(self) -> Task:
        # Agent deploys to Vercel with shell_command
        return Task(
            config=self.tasks_config['deployment_task'],
        )

    # ─── Crew ─────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the AI Software Factory pipeline crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
