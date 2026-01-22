from fastapi import APIRouter, UploadFile, File, HTTPException, status

from app.api.v1.schemas.analysis_chemas import AnalysisResponse
from app.services.file_processing_service import FileProcessingService
from app.services.dataframe_storage_service import DataFrameStorageService
from app.services.dataframe_analysis_service import DataProcessor
from app.services.llm_service import get_llm_service
from app.api.v1.schemas.base_api_response import APIResponse

anality = APIRouter(prefix="/v1/api", tags=["analysis"])

@anality.post("/analyze-file", response_model=APIResponse[AnalysisResponse], status_code=status.HTTP_200_OK)
async def analyze_file(file: UploadFile = File(...)):
    try:

        dataFrame = await FileProcessingService.read_file_to_dataframe(file)
        
        dataframe_id = DataFrameStorageService.store_dataframe(dataFrame)
        
        column_names, data_types, statistical_summary = DataProcessor.get_complete_analysis(dataFrame)
        
        llm_service = get_llm_service()
        chart_suggestions = llm_service.generate_chart_suggestions(
            column_names=column_names,
            data_types=data_types,
            statistical_summary=statistical_summary
        )
        
        data = AnalysisResponse(
            dataframe_id=dataframe_id,
            chart_suggestions=chart_suggestions
        )

        return APIResponse(status_code=status.HTTP_200_OK, message="Analysis successfully completed", data=data)

    except HTTPException:
        raise