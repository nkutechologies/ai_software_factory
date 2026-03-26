from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from ai_software_factory.tools.deployment_tools import FileWriterTool, ShellCommandTool


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
            verbose=True
        )

    @agent
    def backend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_developer'],
            verbose=True
        )

    @agent
    def frontend_developer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_developer'],
            verbose=True
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],
            verbose=True
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
            verbose=True
        )

    @agent
    def deployment_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['deployment_agent'],
            verbose=True,
            tools=[FileWriterTool(), ShellCommandTool()]
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
        return Task(
            config=self.tasks_config['database_task'],
            output_file='output/04_database.sql'
        )

    @task
    def backend_task(self) -> Task:
        return Task(
            config=self.tasks_config['backend_task'],
            output_file='output/05_backend.md'
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
            output_file='output/06_frontend.md'
        )

    @task
    def qa_task(self) -> Task:
        return Task(
            config=self.tasks_config['qa_task'],
            output_file='output/07_tests.md'
        )

    @task
    def evaluation_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluation_task'],
            output_file='output/08_evaluation.json'
        )

    @task
    def git_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['git_integration_task'],
            output_file='output/09_pull_request.md'
        )

    @task
    def deployment_task(self) -> Task:
        return Task(
            config=self.tasks_config['deployment_task'],
            output_file='output/10_deployment.md'
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
