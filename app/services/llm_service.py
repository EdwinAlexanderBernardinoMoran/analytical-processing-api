import json
from typing import List, Dict, Any
from app.api.v1.schemas.chart_schema import ChartSuggestion
from app.core.config import LLMConfig
from app.core.llm_prompt_builder import LLMPromptBuilder
from fastapi import HTTPException, status

class LLMService:
    
    _instance = None
    _model = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_model(self):
        if self._model is None:
            self._model = LLMConfig.configure_genai()
        return self._model
    
    def generate_chart_suggestions(
        self,
        column_names: List[str],
        data_types: Dict[str, str],
        statistical_summary: Dict[str, Any]
    ) -> List[ChartSuggestion]:
        
        prompt = LLMPromptBuilder.build_chart_suggestions_prompt(
            column_names, data_types, statistical_summary
        )
        
        try:
            model = self._get_model()
            
            generation_config = LLMConfig.get_generation_config()
            
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            content = response.text
            result = json.loads(content)
            
            suggestions = []
            charts = result.get("charts", [])
            
            for chart in charts:
                suggestion = ChartSuggestion(
                    title=chart["title"],
                    chart_type=chart["chart_type"],
                    parameters=chart["parameters"],
                    insight=chart["insight"]
                )
                suggestions.append(suggestion)
            
            return suggestions
        
        except json.JSONDecodeError as e:
            raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error with LLM model"
                )
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "quota" in error_msg.lower():
                raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="LLM quota exceeded."
            )
            
            elif "401" in error_msg or "unauthorized" in error_msg.lower():
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key for LLM."
            )
            
            else:
                print(f"LLM Service Error: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"LLM model not found or unavailable for this API version. Verify the model name and the methods it supports."
                )
            
def get_llm_service() -> LLMService:
    return LLMService()
