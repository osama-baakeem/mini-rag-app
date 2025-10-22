from ..LLMInterface import LLMInterface
from ..LLMEnums import HuggingFaceEnums
from huggingface_hub import InferenceClient
import logging

class HuggingFaceProvider(LLMInterface):
    def __init__(self, api_key: str, 
                 default_input_max_characters: int=1000, 
                 default_generation_max_output_tokens: int=1000, 
                 default_generation_temperature: float=0.1):
        self.api_key = api_key
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.generation_client = None
        self.embedding_client = None
        
        self.logger = logging.getLogger(__name__)
    
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
        self.generation_client = InferenceClient(
            model=self.generation_model_id,
            token=self.api_key
        )
    
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size
        self.embedding_client = InferenceClient(
            model=self.embedding_model_id,
            token=self.api_key
        )
    
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self, prompt: str, chat_history: list=[], 
                     max_output_tokens: int=None, temperature: float=None):
        if not self.generation_client:
            self.logger.error("HuggingFace generation client was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model for HuggingFace was not set")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature
        
        # Append current prompt to chat history
        messages = chat_history + [
            self.construct_prompt(role=HuggingFaceEnums.USER.value, prompt=prompt)
        ]
        
        try:
            response = self.generation_client.chat_completion(
                messages=messages,
                max_tokens=max_output_tokens,
                temperature=temperature
            )
            
            if not response or not response.choices or len(response.choices) == 0:
                self.logger.error("Error while generating text with HuggingFace")
                return None
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error while generating text with HuggingFace: {str(e)}")
            return None
    
    def embed_text(self, text: str, document_type: str=None):
        if not self.embedding_client:
            self.logger.error("HuggingFace embedding client was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for HuggingFace was not set")
            return None
        
        try:
            processed_text = self.process_text(text)
            response = self.embedding_client.feature_extraction(processed_text)
            
            if response is None:
                self.logger.error("Error while embedding text with HuggingFace")
                return None
            
            # HuggingFace returns embeddings in different formats depending on the model
            # Most models return a list or nested list structure
            if isinstance(response, list):
                # If it's a 2D array, take the first element (sentence embedding)
                if isinstance(response[0], list):
                    return response[0]
                return response
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error while embedding text with HuggingFace: {str(e)}")
            return None
    
    def construct_prompt(self, role: str, prompt: str):
        return {
            "role": role,
            "content": self.process_text(prompt)
        }