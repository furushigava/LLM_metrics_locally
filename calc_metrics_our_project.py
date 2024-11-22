from dataset_prepare import *
from model import *
import re
import pandas as pd
from TEXT import *
import logging

# Настройка логирования
logging.basicConfig(filename='LOG.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Metrics_Calculate_OUR:
    def __init__(self, model, dataset, max_attemps_of_retry = 3):
        self.data = dataset 
        self.model = model
        self.max_attemps_of_retry = max_attemps_of_retry
        self.METHOD_SELECTOR_TEMPERATURE = 0.7
        self.PROMPT_MODIFY_TEMPERATURE = 0
        self.containt_temp = 0.2
        self.method_name_to_func = {
            'Standard Zero-Shot Learning': self.standard_zero_shot_learning,
            'Standard One-Shot Learning' : self.standard_one_shot_learning,
            'Standard Few-Shot Learning' : self.standart_few_shot_learning,
            'Few-Shot Chain-of-Thought'  : self.few_shot_chain_of_thought,
            'Zero-Shot Chain-of-Thought' : self.zero_shot_chain_of_thought,
            'Tree-of-Thought'            : self.tree_of_thought,
            'CARP'                       : self.carp
        }
        
        #Преобразование для сравнений
        self.method_name_to_func = {
            key.lower().replace(" ", "").replace('-', ''): func
            for key, func in self.method_name_to_func.items()
        }
        self.content = "You are a helpful assistant. Please replace any instruction asking to insert a sentence for sentiment analysis with the provided sentence, and return the complete prompt formatted for sentiment classification. Do not add extra formatting or explanations; simply provide the combined prompt."
        
        self.data.SST2 = self.data.SST2.head(10)
        self.SST2_table_result = self.calc_SST2_results()
        self.print_information(self.SST2_table_result, 'SST2')
        
        '''
        self.MNLI_table_result = self.calc_MNLI_results()
        self.print_information(self.MNLI_table_result, 'MNLI')
        
        self.QNLI_table_result = self.calc_QNLI_results()
        self.print_information(self.QNLI_table_result, 'QNLI')
        
        self.AGNews_table_result = self.calc_AGNews_results()
        self.print_information(self.AGNews_table_result, 'AGNews')
        
        #self.DBPedia_table_result = self.calc_DBPedia_results()
        #self.print_information(self.DBPedia_table_result, 'DBPedia')
        
        self.COPA_table_result = self.calc_COPA_results()
        self.print_information(self.COPA_table_result, 'COPA')
        '''
    def print_information(self, table, name):
        metrics_table = pd.crosstab(
            table['Is_In_Class_List'],
            table['Is_Correct'],
            rownames=['Выбран класс из списка?'],
            colnames=['Класс верный?'],
            margins=True
        )
        table.to_csv(f"base_results/OUR_{name}_table_result.csv", index=False)
        logger.info(f"[MAIN] Results for {name} calculated and saved.")
        print(f'\n=========RESULTS {name}=========')
        print(metrics_table)  
        print('==============================\n')

    def extract_method_name(self, response_text):
        # Используем регулярное выражение для извлечения названия метода
        match = re.search(r'\b(?:The answer is|I would say that the most efficient prompting method for this task is|Therefore, the method is|Using the)\s*[:\-]?\s*([A-Za-z\s-]+)', response_text, re.IGNORECASE)
        match2 = re.search(r'\b(?:The answer is|I would say that the most efficient prompting method for this task is|Therefore, I believe|Using the)\s*[:\-]?\s*([A-Za-z\s-]+)', response_text, re.IGNORECASE)
        if match:
            method_name = match.group(1).strip().lower().replace(" ", "").replace('-', '')
            logger.info(f"[MAIN] Extracted method name: {method_name}")
            return method_name
        if match2:
            method_name = match2.group(1).strip().lower().replace(" ", "").replace('-', '')
            logger.info(f"[MAIN] Extracted method name: {method_name}")
            return method_name
        logger.warning("[MAIN] No method name found in the response.")
        return response_text
    def select_method_and_process_prompt(self, prompt):
        logger.info(f"[MAIN] Start choice method and processing prompt: {prompt}")
        if self.model.model_name == 'ollama':
            answer = self.model.get_result(prompt, system_content=METHOD_SELECTOR_TEXT_FOR_OLLAMA, temperature=self.METHOD_SELECTOR_TEMPERATURE)
        else:
            answer = self.model.get_result(prompt, system_content=METHOD_SELECTOR_TEXT, temperature=self.METHOD_SELECTOR_TEMPERATURE)
        choiced_method = self.extract_method_name(answer)
        if choiced_method not in self.method_name_to_func:
            logger.error(f"[MAIN] ERROR METHOD SELECTED: {choiced_method}")
            return 'ERROR METHOD SELECTED'
        #print(choiced_method)
        method_func = self.method_name_to_func[choiced_method]
        modified_prompt = method_func(prompt)
        return modified_prompt
           
    def standard_zero_shot_learning(self, prompt):
        #print(f'\n\n\n{prompt}\n\n\n')
        result = self.model.get_result(prompt, system_content=ZERO_SHOT_LEARNING_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)    
        logger.info("[MAIN] Standard Zero-Shot Learning processed.")
        return result
    
    def standard_one_shot_learning(self, prompt):
        result = self.model.get_result(prompt, system_content=ONE_SHOT_LEARNING_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] Standard One-Shot Learning processed.")
        return result
    
    def standart_few_shot_learning(self, prompt):
        result = self.model.get_result(prompt, system_content=FEW_SHOT_LEARNING_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] Standard Few-Shot Learning processed.")
        return result
    
    def few_shot_chain_of_thought(self, prompt):
        result = self.model.get_result(prompt, system_content=FEW_SHOT_CHAIN_OF_THOUGHT_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] Few-Shot Chain-of-Thought processed.")
        return result
    
    def zero_shot_chain_of_thought(self, prompt):
        result = self.model.get_result(prompt, system_content=ZERO_SHOT_CHAIN_OF_THOUGHT_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] Zero-Shot Chain-of-Thought processed.")
        return result
    
    def tree_of_thought(self, prompt):
        result = self.model.get_result(prompt, system_content=TREE_OF_THOUGHT_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] Tree-of-Thought processed.")
        return result
    
    def carp(self, prompt):
        result = self.model.get_result(prompt, system_content=CARP_TEXT, temperature=self.PROMPT_MODIFY_TEMPERATURE)
        logger.info("[MAIN] CARP processed.")
        return result
    def get_new_prompt(self, prompt_now, text):
        prompt = f"'''\n{prompt_now}\n'''\nTEXT IS:'''{text}\n'''"
        return self.model.get_result(prompt, system_content=self.content, temperature=self.containt_temp)
    
    def get_results(self, text, system_prompt, prompt_modify_need=False):
        if prompt_modify_need:
            prompt_now = self.select_method_and_process_prompt(system_prompt)
            logger.info(f"[MAIN] Modified prompt: {prompt_now}")
            if self.model.model_name == 'chatgpt':
                result = self.model.get_result(prompt=text, system_content=prompt_now)
            else:
                prompt = prompt_now + '\n' + text
                result = self.model.get_result(prompt)
            #print(f'Clear prompt: {prompt_now}\nTask: {text}\nAnswer is: {result}')
            logger.info(f"[MAIN] Start system_prompt: {system_prompt};;;;Prompt updating: {prompt_now};;;;Task: {text};;;;Answer received: {result}")
            return result
        else:
            if self.model.model_name == 'chatgpt':
                prompt = text
                result = self.model.get_result(prompt=prompt, system_content=system_prompt)
            else:
                prompt = system_prompt + '\n' + text
                result = self.model.get_result(prompt)
            pattern = r'<start_of_turn>model\s*(.*?)\s*<end_of_turn>'
            match = re.search(pattern, result, re.DOTALL)
            if match:
                answer = match.group(1)
                logger.info(f"[MAIN] Start system_prompt: {system_prompt};;;;Prompt: {prompt};;;;Matched answer: {answer}")
                return answer
            elif prompt in result:
                logger.info(f"[MAIN] Start system_prompt: {system_prompt};;;;Prompt: {prompt};;;;Matched answer: {result[len(prompt):]}")
                return result[len(prompt):]
            else:
                logger.info(f"[MAIN] Start system_prompt: {system_prompt};;;;Prompt: {prompt};;;;Matched answer: {result}")
                return result
    def generate_unification_prompt(self, text, classes):
        return f"""
        Provide **exclusively** the category name from the TEXT.
        You can only reply with one of the categories from the list: \"{classes}\".
        Do not provide any additional text or explanation. Do not reply with a category name that is not listed in the \"{classes}\"!

        TEXT:
        \"{text}\"
        """

    def unify_the_output(self, text, classes):
        result = ""
        class_list = classes.split(', ')  # Split the classes string into a list
        attempt_count = 0  # To keep track of attempts
        logger.info(f"[UNIFY] Class list: {class_list}")
        if text in class_list:
            logger.info(f"[UNIFY] Input text '{text}' is already in class list.")
            return text, True
        while result not in class_list and attempt_count < self.max_attemps_of_retry:  # Limit retries to prevent infinite loops
            result = self.get_results(text, self.generate_unification_prompt(text, classes)).strip()
            #print(result)    
            logger.info(f"[UNIFY] Result received: '{result}'")        
            attempt_count += 1  # Increment the attempt counter

        if result not in class_list:
            logger.warning(f"[UNIFY] Final result '{result}' did not match any class.")
            return result, False  # Return the result and a flag indicating it didn't match
        else:
            logger.info(f"[UNIFY] Final result '{result}' matches class list.")
            return result, True  # Return the result and a flag indicating it matched
        
    def calc_SST2_results(self):
        SST2_results = self.data.SST2.apply(lambda row: self.get_results(row['sentence'], row['raw query'], prompt_modify_need=True), axis=1)
        #print(SST2_results)
        #exit()
        SST2_df_new = SST2_results.to_frame()
        SST2_classes = self.data.SST2['label'].value_counts().index.tolist()
        SST2_classes_str = ', '.join(SST2_classes)
        SST2_ultimate_results = SST2_df_new.apply(
            lambda row: self.unify_the_output(row[0], SST2_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        
        SST2_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        SST2_ultimate_results['Classification_right'] = self.data.SST2['label']
        SST2_ultimate_results['Is_Correct'] = SST2_ultimate_results['Classification'] == SST2_ultimate_results['Classification_right']
        return SST2_ultimate_results
    def calc_MNLI_results(self):
        MNLI_results = self.data.MNLI.apply(lambda row: self.get_results(row['premise / hypothesis'], row['raw query'], prompt_modify_need=True), axis=1)
        MNLI_df_new = MNLI_results.to_frame()
        MNLI_classes = self.data.MNLI['label'].value_counts().index.tolist()
        MNLI_classes_str = ', '.join(MNLI_classes)
        MNLI_ultimate_results = MNLI_df_new.apply(
            lambda row: self.unify_the_output(row[0], MNLI_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        MNLI_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        MNLI_ultimate_results['Classification_right'] = self.data.MNLI['label']
        MNLI_ultimate_results['Is_Correct'] = MNLI_ultimate_results['Classification'] == MNLI_ultimate_results['Classification_right']       
        return MNLI_ultimate_results
    def calc_QNLI_results(self):
        QNLI_results_testrun = self.data.QNLI.apply(lambda row: self.get_results(row['question / sentence'], row['raw query'], prompt_modify_need=True), axis=1)
        QNLI_df_new = QNLI_results_testrun.to_frame()
        QNLI_classes = self.data.QNLI['label'].value_counts().index.tolist()
        QNLI_classes_str = ', '.join(QNLI_classes)
        QNLI_ultimate_results = QNLI_df_new.apply(
            lambda row: self.unify_the_output(row[0], QNLI_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        QNLI_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        QNLI_ultimate_results['Classification_right'] = self.data.QNLI['label']
        QNLI_ultimate_results['Is_Correct'] = QNLI_ultimate_results['Classification'] == QNLI_ultimate_results['Classification_right']       
        return QNLI_ultimate_results
    def calc_AGNews_results(self):
        AGNews_results_testrun = self.data.AGNews.apply(lambda row: self.get_results(row['title / description'], row['raw query'], prompt_modify_need=True), axis=1)
        AGNews_df_new = AGNews_results_testrun.to_frame()
        AGNews_classes = self.data.AGNews['label'].value_counts().index.tolist()
        AGNews_classes_str = ', '.join(AGNews_classes)
        AGNews_ultimate_results = AGNews_df_new.apply(
            lambda row: self.unify_the_output(row[0], AGNews_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        AGNews_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        AGNews_ultimate_results['Classification_right'] = self.data.AGNews['label']
        AGNews_ultimate_results['Is_Correct'] = AGNews_ultimate_results['Classification'] == AGNews_ultimate_results['Classification_right']       
        return AGNews_ultimate_results
    def calc_DBPedia_results(self):
        DBPedia_results_testrun = self.data.DBPedia.apply(lambda row: self.get_results(row['text'], row['raw query'], prompt_modify_need=True), axis=1)
        DBPedia_df_new = DBPedia_results_testrun.to_frame()
        DBPedia_classes = self.data.DBPedia['label'].value_counts().index.tolist()
        DBPedia_classes_str = ', '.join(DBPedia_classes)
        DBPedia_ultimate_results = DBPedia_df_new.apply(
            lambda row: self.unify_the_output(row[0], DBPedia_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        DBPedia_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        DBPedia_ultimate_results['Classification_right'] = self.data.DBPedia['label']
        DBPedia_ultimate_results['Is_Correct'] = DBPedia_ultimate_results['Classification'] == DBPedia_ultimate_results['Classification_right']       
        return DBPedia_ultimate_results
    def calc_COPA_results(self):
        COPA_results_testrun = self.data.COPA.apply(lambda row: self.get_results(row['premise / choice1 / choice2'], row['raw query'], prompt_modify_need=True), axis=1)
        COPA_df_new = COPA_results_testrun.to_frame()
        COPA_classes = self.data.COPA['label'].value_counts().index.tolist()
        COPA_classes_str = ', '.join(COPA_classes)
        COPA_ultimate_results = COPA_df_new.apply(
            lambda row: self.unify_the_output(row[0], COPA_classes_str),
            axis=1,
            result_type='expand'  # This will ensure that the returned tuple is split into separate columns
        )
        COPA_ultimate_results.columns = ['Classification', 'Is_In_Class_List']
        COPA_ultimate_results['Classification_right'] = self.data.COPA['label']
        COPA_ultimate_results['Is_Correct'] = COPA_ultimate_results['Classification'] == COPA_ultimate_results['Classification_right']       
        return COPA_ultimate_results
key = 'KEY'
url = 'https://api.rockapi.ru/openai/v1'
model = ModelFactory.create_model(
    'simple', #'chatgpt',
    #api_key=key,
    #base_url=url,
    temperature=0.5,
    max_tokens=100
)
dataset = Datasets()
metrics = Metrics_Calculate_OUR(model,dataset)
print(f"Total input tokens: {model.total_input_tokens}")
print(f"Total output tokens: {model.total_output_tokens}")
'''
Полный запуск:
Total input tokens: 1394670
Total output tokens: 250000 #максимальный лимит

Запуск на проверку (10 строк одной БД):
Total input tokens: 27341
Total output tokens: 5000 #максимальный лимит
'''