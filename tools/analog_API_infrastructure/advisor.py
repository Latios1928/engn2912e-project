from openai import OpenAI
import os 

client = OpenAI(
        base_url = "https://openrouter.ai/api/v1",
        api_key = os.environ["OPENROUTER_API_KEY"],
) 

resp = client.chat.completions.create(
        model = "<provider>/<model>", #information for AI model selected 
        messages [{"role": "system", "content": ...},{"role": "user", "content": ...}],
        response_format = {"type": "json_schema", "json_schema": {...}},
        temperature = 0.2,
) 


