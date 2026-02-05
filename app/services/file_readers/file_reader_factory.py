import pandas as pd
import io
from typing import Union

from .csv_reader import CSVReader
from .excel_reader import ExcelReader

class FileReaderFactory:

    READERS = {
        '.csv': CSVReader,
        '.xls': ExcelReader,
        '.xlsx': ExcelReader,
    }
    
    # Lee un archivo usando el lector apropiado.
    @staticmethod
    def read(
        file_path_or_buffer: Union[str, io.BytesIO],
        extension: str
    ) -> pd.DataFrame:
        
        reader_class = FileReaderFactory.READERS.get(extension)
        
        if reader_class is None:
            raise ValueError(
                f"Extensión '{extension}' no soportada. "
                f"Use una de: {', '.join(FileReaderFactory.READERS.keys())}"
            )
        
        return reader_class.read(file_path_or_buffer)
