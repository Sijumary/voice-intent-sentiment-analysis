from pydantic import BaseModel
from typing import List, Optional


class AgentScore(BaseModel):
    politeness: Optional[int] =  None
    clarity: Optional[int] = None
    resolution: Optional[int] = None


class AnalysisResponse(BaseModel):
    sentiment: str
    tone: str
    intent: str
    urgency: str
    summary: str
    important_phrases: Optional[List[str]] = None
    agent_score: Optional[AgentScore] = None
    raw_response: Optional[str] = None