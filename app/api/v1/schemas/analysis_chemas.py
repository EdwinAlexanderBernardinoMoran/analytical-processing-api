from pydantic import BaseModel, Field
from typing import List

from app.api.v1.schemas.chart_schema import ChartSuggestion

class AnalysisResponse(BaseModel):
    # message: str = Field(default="Analysis completed successfully")
    dataframe_id: str = Field(..., description="Unique ID to retrieve chart data")
    # column_names: List[str] = Field(..., description="List of column names")
    # data_types: Dict[str, str] = Field(..., description="Data types of each column")
    # statistical_summary: Dict[str, Any] = Field(..., description="Statistical summary from df.describe()")
    chart_suggestions: List[ChartSuggestion] = Field(..., description="Suggested visualizations from LLM")
