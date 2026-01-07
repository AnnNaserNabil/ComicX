"""
Visual generation crew for artwork, style consistency, and layout.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import PageLayout, PanelArtwork, StyleAnalysis
from src.tools.image_tools import ModelsLabImageTool
from src.tools.layout_tools import ComicLayoutTool, TypographyTool
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class VisualCrew:
    """Visual Generation Crew"""

    agents_config = "../../config/agents/visual.yaml"
    tasks_config = "../../config/tasks/visual.yaml"

    @llm
    def llm_model(self):
        """Get Gemini LLM for visual tasks"""
        return LLMFactory.get_llm(task_type="general", temperature=0.8)

    @agent
    def visual_artist(self) -> Agent:
        modelslab_tool = ModelsLabImageTool(
            model=settings.image_model,
            width=settings.image_width,
            height=settings.image_height,
            samples=settings.image_samples,
            num_inference_steps=settings.image_steps,
            guidance_scale=settings.image_guidance_scale,
            use_community=True,  # Use community models for better quality
        )
        return Agent(
            config=self.agents_config["visual_artist"],
            tools=[modelslab_tool],
            llm=self.llm_model(),
            verbose=True,
        )

    @agent
    def style_consistency(self) -> Agent:
        return Agent(
            config=self.agents_config["style_consistency"],
            llm=self.llm_model(),
            verbose=True,
        )

    @agent
    def comic_layout(self) -> Agent:
        return Agent(
            config=self.agents_config["comic_layout"],
            tools=[ComicLayoutTool(), TypographyTool()],
            llm=self.llm_model(),
            verbose=True,
        )

    @task
    def illustration(self) -> Task:
        return Task(
            config=self.tasks_config["illustration"],
            agent=self.visual_artist(),
            output_pydantic=PanelArtwork,
        )

    @task
    def style_check(self) -> Task:
        return Task(
            config=self.tasks_config["style_check"],
            agent=self.style_consistency(),
            output_pydantic=StyleAnalysis,
        )

    @task
    def layout_design(self) -> Task:
        return Task(
            config=self.tasks_config["layout_design"],
            agent=self.comic_layout(),
            output_pydantic=PageLayout,
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
