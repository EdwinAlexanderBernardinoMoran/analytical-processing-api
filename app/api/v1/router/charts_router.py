from fastapi import APIRouter, HTTPException, status

from app.api.v1.schemas.chart_schema import ChartDataResponse, ChartDataRequest
from app.api.v1.schemas.base_api_response import APIResponse
from app.services.charts_service import ChartDataProcessor
from app.services.dataframe_storage_service import DataFrameStorageService

charts = APIRouter(prefix="/v1/api", tags=["charts"])

@charts.post("/get-chart-data", response_model=APIResponse[ChartDataResponse], status_code=status.HTTP_200_OK)
async def get_chart_data(request: ChartDataRequest):
    try:
        dataFrame = DataFrameStorageService.get_dataframe(request.dataframe_id)
        print("Received request for chart data:", dataFrame)
        
        if dataFrame is None:
            raise HTTPException(
                status_code=404,
                detail="DataFrame not found or expired. Please re-upload the file."
            )
        
        chart_data = ChartDataProcessor.prepare_chart_data(
            dataFrame=dataFrame,
            chart_type=request.chart_type,
            x_axis=request.x_axis,
            y_axis=request.y_axis
        )
        
        data = ChartDataResponse(
            chart_type=request.chart_type,
            datasets=chart_data
        )
        
        
        return APIResponse(status_code=status.HTTP_200_OK, message="Chart data successfully retrieved", data=data)

    except HTTPException:
        raise