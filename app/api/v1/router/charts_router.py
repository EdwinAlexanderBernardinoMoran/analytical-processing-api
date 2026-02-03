from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Union

from app.api.v1.schemas.chart_schema import ChartDataResponse
from app.api.v1.schemas.base_api_response import APIResponse
from app.services.charts_service import ChartDataProcessor
from app.services.dataframe_storage_service import DataFrameStorageService

charts = APIRouter(prefix="/v1/api/chart", tags=["chart"])

@charts.get("/data", response_model=APIResponse[ChartDataResponse], status_code=status.HTTP_200_OK)
async def get_chart_data(
    dataframe_id: str = Query(..., description="ID of the stored DataFrame"),
    chart_type: str = Query(..., description="Type of chart (bar, line, pie)"),
    x_axis: str = Query(..., description="Column name for x-axis"),
    y_axis: str | List[str] = Query(..., description="Column name(s) for y-axis"),
    aggregation: str = Query("none", description="Aggregation type: avg, sum, count, min, max, none"),
    metric_label: str = Query("", description="Descriptive label for the calculated metric")
):
    try:
        dataFrame = DataFrameStorageService.get_dataframe(dataframe_id)
        
        if dataFrame is None:
            raise HTTPException(
                status_code=404,
                detail="DataFrame not found or expired. Please re-upload the file."
            )
        
        chart_data = ChartDataProcessor.prepare_chart_data(
            dataFrame=dataFrame,
            chart_type=chart_type,
            x_axis=x_axis,
            y_axis=y_axis,
            aggregation=aggregation,
            metric_label=metric_label
        )
        
        data = ChartDataResponse(
            chart_type=chart_type,
            datasets=chart_data
        )
        
        
        return APIResponse(status_code=status.HTTP_200_OK, message="Chart data successfully retrieved", data=data)

    except HTTPException:
        raise