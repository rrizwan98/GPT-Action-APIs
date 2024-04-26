import json
import yaml
import logging
import time
import google.generativeai as genai

genai.configure(api_key='AIzaSyCo4e9cR0TZ7FETfG_cqO-HBiM-sWriwGo')
encoding = 'utf-8'

def load_configuration(file_path: str) -> dict:
    """
    Load the configuration from a YAML file.
    
    """
    with open(file_path, 'r', encoding=encoding) as file:
        return yaml.safe_load(file)

config = load_configuration('apis/app_config.yaml')
safety_settings = config['safety_settings']
instrucctions:str = config.get('instructions', '')

def to_json(text):
  text = text.replace('\n', '')
  text.strip()
  return json.loads(text)

def recommendation(message:str) -> str:
    start_time = time.time()
    try:
        contents = [instrucctions, message ]
        model = genai.GenerativeModel('gemini-pro')
        responses = model.generate_content(contents, safety_settings=safety_settings)
        responses.resolve()
        # response = to_json(responses.text)
        response = responses.text
        end_time = time.time()
        logging.info(f"SCRIPT_NAME: utils.py\nFUNCTION_NAME: poisonous_plant\nSTART_TIME: {start_time:.2f}s\nEND_TIME: {end_time:.2f}s\nEXECUTION_TIME: {end_time - start_time:.2f}s\nERROR STATUS: SUCCESSFULLY\nMODEL_NAME: Gemini-Pro\nTOKENS USED: {len(json.dumps(response))}")
        return response
         
    except Exception as e:
        end_time = time.time()
        logging.error(f"SCRIPT_NAME: utils.py\nFUNCTION_NAME: poisonous_plant\nSTART_TIME: {start_time:.2f}s\nEND_TIME: {end_time:.2f}s\nEXECUTION_TIME: {end_time - start_time:.2f}s\nERROR STATUS: {str(e)}\nMODEL_NAME: Gemini-Pro")
        raise Exception(f"Error occurred: {e}. Please try again later.")
