import logging
import tiktoken
from openai import OpenAI

# Настройка базового логирования
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class BaseModel:
    def __init__(self, max_tokens=100, model_name=''):
        self.max_tokens = max_tokens
        self.model_name = model_name
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        logger.info(f'[Model] Initialized BaseModel with model_name={model_name}, max_tokens={max_tokens}')

    def get_result(self, prompt, system_content=None, temperature=0.7):
        raise NotImplementedError("Subclasses should implement this!")

class SimpleModel(BaseModel):
    def __init__(self, max_tokens=100, model='gpt-3.5-turbo', temperature=0.7):
        super().__init__(max_tokens, 'simple_model')
        self.model = model
        logger.info(f'[Model] SimpleModel initialized with model={model}')

    def get_result(self, prompt, system_content=None, temperature=0.7):
        logger.info(f'[Model] Getting result for prompt="{prompt}..." with temperature={temperature}')
        # Используем tiktoken для кодирования токенов
        encoding = tiktoken.get_encoding("cl100k_base")

        # Формируем сообщения для подсчета токенов
        messages = [{"role": "user", "content": prompt}]
        if system_content:
            messages.insert(0, {"role": "system", "content": system_content})

        # Считаем токены для всех сообщений в качестве входных токенов
        input_tokens = sum(len(encoding.encode(message['content'])) for message in messages)
        self.total_input_tokens += input_tokens
        self.total_output_tokens += self.max_tokens
        logger.info(f'[Model] Input tokens: {input_tokens}, Total input tokens: {self.total_input_tokens}')
        logger.info(f'[Model] Allocated output tokens: {self.max_tokens}, Total output tokens: {self.total_output_tokens}')

        return "Simple string"

class ChatGPTModel(BaseModel):
    def __init__(self, api_key, base_url, model='gpt-3.5-turbo', temperature=0.7, max_tokens=100):
        super().__init__(max_tokens, 'chatgpt')
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        logger.info(f'[Model] ChatGPTModel initialized with model={model} at base_url={base_url}')

    def get_result(self, prompt, system_content=None, temperature=0.7):
        logger.info(f'[Model] Getting result for prompt="{prompt}..." with temperature={temperature}')
        messages = [{"role": "user", "content": prompt}]
        if system_content:
            messages.insert(0, {"role": "system", "content": system_content})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )
        logger.info('[Model] Result successfully received from ChatGPTModel')
        return completion.choices[0].message.content

class ModelFactory:
    @staticmethod
    def create_model(model_type, **kwargs):
        if model_type == 'simple':
            logger.info('[Model] Creating SimpleModel')
            return SimpleModel(**kwargs)
        elif model_type == 'chatgpt':
            logger.info('[Model] Creating ChatGPTModel')
            return ChatGPTModel(**kwargs)
        else:
            logger.error('[Model] Unknown model type')
            raise ValueError("Unknown model type")

# Пример использования:
if __name__ == "__main__":
    model = ModelFactory.create_model(
        model_type='simple',
        max_tokens=100
    )
    prompt = "What is the capital of France?"
    system_content = "You are a helpful assistant."
    response = model.get_result(prompt, system_content=system_content, temperature=0.7)
    print(response)
    #logger.info(f'[Model] Total input tokens: {model.total_input_tokens}')
    #logger.info(f'[Model] Total output tokens: {model.total_output_tokens}')
