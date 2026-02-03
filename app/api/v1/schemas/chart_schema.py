from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class ChartParameters(BaseModel):
    x_axis: str = Field(..., description="Column name for x-axis")
    y_axis: str | List[str] = Field(..., description="Column name(s) for y-axis")
    aggregation: Optional[str] = Field("none", description="Aggregation type: avg, sum, count, min, max, none")
    metric_label: Optional[str] = Field("", description="Descriptive label for the calculated metric")
    

class ChartSuggestion(BaseModel):
    title: str = Field(..., description="Title of the chart")
    chart_type: str = Field(..., description="Type of chart (bar, line, pie)")
    parameters: ChartParameters = Field(..., description="Parameters for the chart")
    insight: str = Field(..., description="Brief analysis or insight about the chart")

class ChartDataRequest(BaseModel):
    dataframe_id: str = Field(..., description="ID of the stored DataFrame")
    chart_type: str = Field(..., description="Type of chart (bar, line, pie)")
    x_axis: str = Field(..., description="Column name for x-axis")
    y_axis: str | List[str] = Field(..., description="Column name(s) for y-axis")
    aggregation: Optional[str] = Field("none", description="Aggregation type: avg, sum, count, min, max, none")
    metric_label: Optional[str] = Field("", description="Descriptive label for the calculated metric")


class ChartDataResponse(BaseModel):
    chart_type: str = Field(..., description="Type of chart")
    datasets: Dict[str, Any] = Field(..., description="Formatted data for the chart")