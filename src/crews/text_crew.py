"""
Comic text generation crew for captions and dialogue.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import PanelText
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class TextCrew:
    """Text Generation Crew for captions and dialogue"""

    agents_config = "config/agents/text.yaml"
    tasks_config = "config/tasks/text.yaml"

    @llm
    def caption_llm(self):
        """LLM for caption generation"""
        return LLMFactory.get_caption_llm()
    
    @llm
    def dialogue_llm(self):
        """LLM for dialogue generation"""
        return LLMFactory.get_dialogue_llm()

    @agent
    def caption_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["caption_writer"],
            llm=self.caption_llm(),
            verbose=True,
        )

    @agent
    def dialogue_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["dialogue_writer"],
            llm=self.dialogue_llm(),
            verbose=True,
        )

    @task
    def caption_generation(self) -> Task:
        return Task(
            config=self.tasks_config["caption_generation"],
            agent=self.caption_writer(),
        )

    @task
    def dialogue_generation(self) -> Task:
        return Task(
            config=self.tasks_config["dialogue_generation"],
            agent=self.dialogue_writer(),
            output_pydantic=PanelText,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
