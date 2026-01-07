"""
Processing crew for document extraction and validation.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import ProcessedDocument, ValidationResult
from src.tools.pdf_tools import PDFProcessorTool, TextProcessorTool
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class ProcessingCrew:
    """Processing Crew for document extraction and validation"""

    agents_config = "../../config/agents/processing.yaml"
    tasks_config = "../../config/tasks/processing.yaml"

    @llm
    def llm_model(self):
        """Get Gemini LLM for processing tasks"""
        return LLMFactory.get_llm(task_type="general", temperature=0.0)

    @agent
    def document_processor(self) -> Agent:
        return Agent(
            config=self.agents_config["document_processor"],
            tools=[PDFProcessorTool(), TextProcessorTool()],
            llm=self.llm_model(),
            verbose=True,
        )

    @agent
    def content_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_validator"],
            llm=self.llm_model(),
            verbose=True,
        )

    @task
    def document_processing(self) -> Task:
        return Task(
            config=self.tasks_config["document_processing"],
            agent=self.document_processor(),
            output_pydantic=ProcessedDocument,
        )

    @task
    def content_validation(self) -> Task:
        return Task(
            config=self.tasks_config["content_validation"],
            agent=self.content_validator(),
            output_pydantic=ValidationResult,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
