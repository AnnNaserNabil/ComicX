"""
Content generation crew for translation, story writing, and scriptwriting.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import ComicScript, StoryStructure, TranslatedContent
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class ContentCrew:
    """Content Generation Crew"""

    agents_config = "../../config/agents/content.yaml"
    tasks_config = "../../config/tasks/content.yaml"

    @llm
    def story_llm(self):
        """LLM for story generation (creative)"""
        return LLMFactory.get_story_llm()
    
    @llm
    def script_llm(self):
        """LLM for script writing (structured)"""
        return LLMFactory.get_script_llm()
    
    @llm
    def general_llm(self):
        """General purpose LLM"""
        return LLMFactory.get_llm(task_type="general", temperature=0.7)

    @agent
    def translator(self) -> Agent:
        return Agent(
            config=self.agents_config["translator"],
            llm=self.general_llm(),
            verbose=True
        )

    @agent
    def story_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["story_writer"],
            llm=self.story_llm(),  # Use creative LLM for story generation
            verbose=True
        )

    @agent
    def script_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["script_writer"],
            llm=self.script_llm(),  # Use structured LLM for script writing
            verbose=True
        )

    @task
    def translation(self) -> Task:
        return Task(
            config=self.tasks_config["translation"],
            agent=self.translator(),
            output_json=TranslatedContent,
        )

    @task
    def story_structuring(self) -> Task:
        return Task(
            config=self.tasks_config["story_structuring"],
            agent=self.story_writer(),
            context=[self.translation()],
            output_json=StoryStructure,
        )

    @task
    def scriptwriting(self) -> Task:
        return Task(
            config=self.tasks_config["scriptwriting"],
            agent=self.script_writer(),
            context=[self.story_structuring()],
            output_json=ComicScript,
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
