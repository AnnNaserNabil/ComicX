"""
Video generation agent for creating animated comic sequences.
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, llm, task

from src.models.config import get_settings
from src.models.schemas import VideoSequence
from src.tools.image_tools import ModelsLabVideoTool
from src.utils.llm_factory import LLMFactory

settings = get_settings()


@CrewBase
class VideoCrew:
    """Video Generation Crew for animated sequences"""

    agents_config = "config/agents/video.yaml"
    tasks_config = "config/tasks/video.yaml"

    @llm
    def llm_model(self):
        """Get Gemini LLM for video tasks"""
        return LLMFactory.get_llm(task_type="general", temperature=0.8)

    @agent
    def video_generator(self) -> Agent:
        video_tool = ModelsLabVideoTool(
            model=settings.video_model,
            width=settings.video_width,
            height=settings.video_height,
            num_frames=settings.video_frames,
            num_inference_steps=settings.video_steps,
        )
        return Agent(
            config=self.agents_config["video_generator"],
            tools=[video_tool],
            llm=self.llm_model(),
            verbose=True,
        )

    @agent
    def video_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["video_editor"],
            llm=self.llm_model(),
            verbose=True,
        )

    @task
    def video_generation(self) -> Task:
        return Task(
            config=self.tasks_config["video_generation"],
            agent=self.video_generator(),
        )

    @task
    def video_editing(self) -> Task:
        return Task(
            config=self.tasks_config["video_editing"],
            agent=self.video_editor(),
            output_pydantic=VideoSequence,
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
