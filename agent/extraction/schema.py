from pydantic import BaseModel
from typing import List


class Source(BaseModel):
    file: str
    section: str | None = None


class Decision(BaseModel):
    id: str
    title: str
    summary: str
    tags: List[str]
    source: Source


class Rule(BaseModel):
    id: str
    rule: str
    scope: str
    source: Source


class Warning(BaseModel):
    id: str
    area: str
    message: str
    severity: str
    source: Source


class ExtractedKnowledge(BaseModel):
    decisions: List[Decision]
    rules: List[Rule]
    warnings: List[Warning]