from dataset_prepare import *
from model import *
import re
import pandas as pd
'''
Считаем метрику простых моделей. Не накидываются наши хитрые штуки.
'''
class Metrics_Calculate_BASE:
    def __init__(self, model, dataset, max_attemps_of_retry = 3):
        self.data = dataset 
        self.model = model
        self.max_attemps_of_retry = max_attemps_of_retry #SST2
        
        #self.data.SST2 = self.data.SST2.head(10)
        #self.data.MNLI = self.data.MNLI.head(10)
        #self.data.QNLI= self.data.QNLI.head(10)
        #self.data.AGNews = self.data.AGNews.head(10)
        #self.data.DBPedia = self.data.DBPedia.head(10)
        #self.data.COPA = self.data.COPA.head(10)
        
        self.SST2_table_result = self.calc_SST2_results()
        self.print_information(self.SST2_table_result, 'SST2')

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
        

    def print_information(self, table, name):
        metrics_table = pd.crosstab(
            table['Is_In_Class_List'],
            table['Is_Correct'],
            rownames=['Выбран класс из списка?'],
            colnames=['Класс верный?'],
            margins=True
        )
        table.to_csv(f"base_results/{name}_table_result.csv", index=False)
        print(f'\n=========RESULTS {name}=========')
        print(metrics_table)  
        print('==============================\n')

    def get_results(self, text, system_prompt):
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
            return answer
        elif prompt in result:
            return result[len(prompt):]
        else:
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

        while result not in class_list and attempt_count < self.max_attemps_of_retry:  # Limit retries to prevent infinite loops
            result = self.get_results(text, self.generate_unification_prompt(text, classes)).strip()
            attempt_count += 1  # Increment the attempt counter

        if result not in class_list:
            return result, False  # Return the result and a flag indicating it didn't match
        else:
            return result, True  # Return the result and a flag indicating it matched

    def calc_SST2_results(self):
        SST2_results = self.data.SST2.apply(lambda row: self.get_results(row['sentence'], row['raw query']), axis=1)
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
        MNLI_results = self.data.MNLI.apply(lambda row: self.get_results(row['premise / hypothesis'], row['raw query']), axis=1)
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
        QNLI_results_testrun = self.data.QNLI.apply(lambda row: self.get_results(row['question / sentence'], row['raw query']), axis=1)
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
        AGNews_results_testrun = self.data.AGNews.apply(lambda row: self.get_results(row['title / description'], row['raw query']), axis=1)
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
        DBPedia_results_testrun = self.data.DBPedia.apply(lambda row: self.get_results(row['text'], row['raw query']), axis=1)
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
        COPA_results_testrun = self.data.COPA.apply(lambda row: self.get_results(row['premise / choice1 / choice2'], row['raw query']), axis=1)
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

#model = Model(gemma_access_token = access_token)

key = 'KEY'
url = 'https://api.rockapi.ru/openai/v1'
model = ModelFactory.create_model(
    'chatgpt',
    api_key=key,
    base_url=url,
    temperature=0.7,
    max_tokens=100
)
dataset = Datasets()
metrics = Metrics_Calculate_BASE(model,dataset)


