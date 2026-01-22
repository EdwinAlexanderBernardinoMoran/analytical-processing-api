from pydantic import BaseModel, Field
from typing import Dict, List, Any

class ChartParameters(BaseModel):
    x_axis: str = Field(..., description="Column name for x-axis")
    y_axis: str | List[str] = Field(..., description="Column name(s) for y-axis")
    

class ChartSuggestion(BaseModel):
    title: str = Field(..., description="Title of the chart")
    chart_type: str = Field(..., description="Type of chart (bar, line, pie, scatter)")
    parameters: ChartParameters = Field(..., description="Parameters for the chart")
    insight: str = Field(..., description="Brief analysis or insight about the chart")

class ChartDataRequest(BaseModel):
    dataframe_id: str = Field(..., description="ID of the stored DataFrame")
    chart_type: str = Field(..., description="Type of chart (bar, line, pie, scatter)")
    x_axis: str = Field(..., description="Column name for x-axis")
    y_axis: str | List[str] = Field(..., description="Column name(s) for y-axis")


class ChartDataResponse(BaseModel):
    chart_type: str = Field(..., description="Type of chart")
    datasets: Dict[str, Any] = Field(..., description="Formatted data for the chart")