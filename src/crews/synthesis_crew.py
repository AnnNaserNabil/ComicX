"""
Synthesis crew for combining elements and exporting.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import ComicBook, QualityReport
from src.tools.export_tools import CBZExportTool, PDFExportTool, WebExportTool
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class SynthesisCrew:
    """Synthesis Crew for final assembly and export"""

    agents_config = "../../config/agents/synthesis.yaml"
    tasks_config = "../../config/tasks/synthesis.yaml"

    @llm
    def llm_model(self):
        """Get Gemini LLM for synthesis tasks"""
        return LLMFactory.get_llm(task_type="general", temperature=0.0)

    @agent
    def synthesizer(self) -> Agent:
        return Agent(
            config=self.agents_config["synthesizer"], llm=self.llm_model(), verbose=True
        )

    @agent
    def quality_assurance(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_assurance"],
            llm=self.llm_model(),
            verbose=True,
        )

    @agent
    def export_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["export_agent"],
            tools=[PDFExportTool(), CBZExportTool(), WebExportTool()],
            llm=self.llm_model(),
            verbose=True,
        )

    @task
    def synthesis(self) -> Task:
        return Task(
            config=self.tasks_config["synthesis"],
            agent=self.synthesizer(),
            output_pydantic=ComicBook,
        )

    @task
    def quality_assurance_task(self) -> Task:
        return Task(
            config=self.tasks_config["quality_assurance"],
            agent=self.quality_assurance(),
            output_pydantic=QualityReport,
        )

    @task
    def export_task(self) -> Task:
        return Task(
            config=self.tasks_config["export"],
            agent=self.export_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True,
        )
