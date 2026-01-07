"""
Configuration management for the comic book generator.
"""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # OpenRouter Configuration
    openrouter_api_key: Optional[str] = Field(None, description="OpenRouter API key")
    openrouter_model: str = Field(default="xiaomi/mimo-v2-flash:free", description="OpenRouter model")
    openrouter_base_url: str = Field(default="https://openrouter.ai/api/v1", description="OpenRouter API base URL")
    
    # LLM Settings
    llm_temperature: float = Field(default=0.8, ge=0, le=2)
    llm_max_tokens: int = Field(default=8000, ge=1)
    
    # ModelsLab Configuration
    
    # ModelsLab Configuration
    modelslab_api_key: str = Field(..., description="ModelsLab API key")
    modelslab_enterprise: bool = Field(default=False, description="Use enterprise endpoints")
    
    # Image Generation Settings
    image_model: str = Field(default="flux", description="Image generation model")
    image_width: int = Field(default=1024, ge=256, le=2048)
    image_height: int = Field(default=1024, ge=256, le=2048)
    image_samples: int = Field(default=1, ge=1, le=4)
    image_steps: int = Field(default=30, ge=1, le=100)
    image_guidance_scale: float = Field(default=7.5, ge=1, le=20)
    
    # Video Generation Settings
    video_model: str = Field(default="cogvideox", description="Video generation model")
    video_width: int = Field(default=512, ge=256, le=1024)
    video_height: int = Field(default=512, ge=256, le=1024)
    video_frames: int = Field(default=25, ge=10, le=100)
    video_steps: int = Field(default=20, ge=1, le=50)
    
    # AgentOps Configuration
    agentops_api_key: Optional[str] = Field(None, description="AgentOps API key")
    
    # Application Settings
    app_name: str = Field(default="Comic Book Generator")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # API Settings
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1, le=65535)
    api_workers: int = Field(default=4, ge=1)
    api_reload: bool = Field(default=False)
    
    # Redis Configuration
    redis_host: str = Field(default="redis")
    redis_port: int = Field(default=6379, ge=1, le=65535)
    redis_db: int = Field(default=0, ge=0)
    redis_password: Optional[str] = Field(None)
    
    # Storage Configuration
    output_dir: Path = Field(default=Path("/app/outputs"))
    temp_dir: Path = Field(default=Path("/app/outputs/temp"))
    max_file_size: int = Field(default=52428800, description="Max file size in bytes (50MB)")
    cleanup_after_days: int = Field(default=7, ge=1)
    
    # Generation Defaults
    default_art_style: str = Field(default="cartoon")
    default_target_pages: int = Field(default=20, ge=1, le=100)
    default_language: str = Field(default="en")
    default_target_audience: str = Field(default="general")
    
    # Performance Settings
    max_parallel_panels: int = Field(default=5, ge=1, le=20)
    cache_enabled: bool = Field(default=True)
    cache_ttl: int = Field(default=3600, ge=0)
    
    # Security
    allowed_origins: List[str] = Field(
        default_factory=lambda: ["http://localhost:3000", "http://localhost:8000"]
    )
    max_upload_size: int = Field(default=52428800)
    rate_limit_per_minute: int = Field(default=10, ge=1)
    
    # Monitoring
    enable_metrics: bool = Field(default=True)
    metrics_port: int = Field(default=9090, ge=1, le=65535)
    
    @property
    def redis_url(self) -> str:
        """Get Redis connection URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "comics").mkdir(exist_ok=True)
        (self.output_dir / "reports").mkdir(exist_ok=True)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.ensure_directories()
    return settings
