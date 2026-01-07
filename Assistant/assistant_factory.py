from Assistant.assistant import Assistant
from Assistant.gorq_assistant import GorqAssistant


class AiAssistantFactory:
     _providers = {
         "groq" : GorqAssistant
     }

     def create_assistant(self,provider_name:str,api_key:str) -> Assistant:
         try:
             return self._providers[provider_name](api_key)
         except KeyError:
             raise ValueError("Invalid provider name")



