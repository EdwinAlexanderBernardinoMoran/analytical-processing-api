from fastapi import UploadFile, HTTPException
import pandas as pd
import io

class FileProcessingService:
    @staticmethod
    async def read_file_to_dataframe(file: UploadFile) -> pd.DataFrame:
        contents = await file.read()

        if file.filename.endswith('.csv'):
            dataFrame = pd.read_csv(io.BytesIO(contents))

        if file.filename.endswith(('.xls', '.xlsx')):
            dataFrame = pd.read_excel(io.BytesIO(contents))

        if not file.filename.endswith(('csv', '.xls', '.xlsx')):
            raise HTTPException(
                status_code=400,
                detail="File format not supported. Use CSV or XLSX."
            )

        if dataFrame.empty:
            raise HTTPException(
                status_code=400,
                detail="The file is empty or does not contain valid data."
            )
            
        return dataFrame
        