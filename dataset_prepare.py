import pandas as pd
import numpy as np
import copy

'''
Выровнять датасеты: сколько True столько и False до выборки данных
'''
class Datasets:
    def __init__(self, path_to_rawqueries = 'raw_queries (3).csv',
                 path_to_agnews = 'AGNews_test.csv', path_to_dbpedia='DBPEDIA_test.csv'):
        
        self.raw_queries_df = pd.read_csv(path_to_rawqueries, sep = ';')
        self.variables = {
            "queries": 10, #const from raw_queries
            "samples_per_query": 10, #можно увеличивать
        }
        self.lines = self.variables["queries"] * self.variables["samples_per_query"]

        self.SST2 = self.init_SST2()
        self.MNLI = self.init_MNLI()
        self.QNLI = self.init_QNLI()
        self.AGNews = self.init_AGNews(path_to_agnews)
        #self.DBPedia = self.init_DBPedia(path_to_dbpedia)
        self.COPA = self.init_COPA()
    def dataset_test_sampling(self, dataset):
        '''Функция для создания тестовой выборки с определенным количеством строк из исходного датасета'''
        test_df = dataset.sample(n=self.lines, random_state=15, replace=False)
        return test_df
    def df_for_model(self, queries_df, test_df, dataset_name):
        dataset = dataset_name
        queries = queries_df[queries_df['dataset'] == dataset]
        if queries.empty:
            raise ValueError(f"No queries found for dataset: {dataset}")
        queries_repeated = np.repeat(queries.values, self.variables["samples_per_query"], axis=0)
        queries_df = pd.DataFrame(queries_repeated, columns=queries.columns)
        model_df = copy.deepcopy(test_df)
        model_df["raw query"] = queries_df["raw query"].values
        return model_df
    def init_SST2(self):
        df_SST2 = pd.read_parquet("hf://datasets/nyu-mll/glue/sst2/train-00000-of-00001.parquet")
        test_df_SST2 = self.dataset_test_sampling(df_SST2)
        model_df_SST2 = self.df_for_model(self.raw_queries_df, test_df_SST2, 'SST2')
        SST2_unified = model_df_SST2[["sentence","label","raw query"]]
        SST2_unified['label'].replace(0, 'Negative', inplace=True)
        SST2_unified['label'].replace(1, 'Positive', inplace=True)
        return SST2_unified
    def init_MNLI(self):
        df_MNLI = pd.read_parquet("hf://datasets/nyu-mll/glue/mnli/train-00000-of-00001.parquet")
        test_df_MNLI = self.dataset_test_sampling(df_MNLI)
        model_df_MNLI = self.df_for_model(self.raw_queries_df, test_df_MNLI, 'MNLI')
        MNLI_unified = copy.deepcopy(model_df_MNLI)
        MNLI_unified["premise / hypothesis"] = ('Premise: ' + MNLI_unified["premise"] + ' Hypothesis: ' + MNLI_unified["hypothesis"])
        MNLI_unified = MNLI_unified[["premise / hypothesis", "label", "raw query"]]
        MNLI_unified['label'].replace(0, 'Entailment', inplace=True)
        MNLI_unified['label'].replace(1, 'Neutral', inplace=True)
        MNLI_unified['label'].replace(2, 'Contradiction', inplace=True)
        return MNLI_unified
    def init_QNLI(self):
        df_QNLI = pd.read_parquet("hf://datasets/nyu-mll/glue/qnli/train-00000-of-00001.parquet")
        test_df_QNLI = self.dataset_test_sampling(df_QNLI)
        model_df_QNLI = self.df_for_model(self.raw_queries_df, test_df_QNLI, 'QNLI')
        QNLI_unified = copy.deepcopy(model_df_QNLI)
        QNLI_unified["question / sentence"] = ('Question: ' + QNLI_unified["question"] + ' Sentence: ' + QNLI_unified["sentence"])
        QNLI_unified = QNLI_unified[["question / sentence", "label", "raw query"]]
        QNLI_unified['label'].replace(0, 'Entailment', inplace=True)
        QNLI_unified['label'].replace(1, 'Not Entailment', inplace=True)
        return QNLI_unified
    def init_AGNews(self, path_to_agnews):
        df_AGNews = pd.read_csv(path_to_agnews)#('/content/test.csv')
        test_df_AGNews = self.dataset_test_sampling(df_AGNews)
        model_df_AGNews = self.df_for_model(self.raw_queries_df, test_df_AGNews, 'AGNews')
        AGNews_unified = copy.deepcopy(model_df_AGNews)
        AGNews_unified["title / description"] = ("Title: " + AGNews_unified["Title"] + "." + " Description: " + AGNews_unified["Description"])
        AGNews_unified = AGNews_unified[["title / description","Class Index", "raw query"]]
        AGNews_unified.rename(columns = {'Class Index':'label'}, inplace = True )
        AGNews_unified['label'].replace(1, 'World', inplace=True)
        AGNews_unified['label'].replace(2, 'Sports', inplace=True)
        AGNews_unified['label'].replace(3, 'Business', inplace=True)
        AGNews_unified['label'].replace(4, 'Sci/Tech', inplace=True)
        return AGNews_unified
    def init_DBPedia(self, path_to_dbpedia):
        df_DBPedia = pd.read_csv (path_to_dbpedia) #('/content/DBPEDIA_test.csv')
        test_df_DBPedia = self.dataset_test_sampling(df_DBPedia)
        model_df_DBPedia = self.df_for_model(self.raw_queries_df, test_df_DBPedia, 'DBPedia')
        DBPedia_unified = model_df_DBPedia[["text","l1","raw query"]]
        DBPedia_unified.rename(columns = {'l1':'label'}, inplace = True )
        return DBPedia_unified
    def init_COPA(self):
        splits = {'train': 'train.csv', 'test': 'test.csv'}
        df_COPA = pd.read_csv("hf://datasets/pkavumba/balanced-copa/" + splits["test"])
        test_df_COPA = self.dataset_test_sampling(df_COPA)
        model_df_COPA = self.df_for_model(self.raw_queries_df, test_df_COPA, 'COPA')
        COPA_unified = copy.deepcopy(model_df_COPA)
        COPA_unified["premise / choice1 / choice2"] = ("Premise: " + COPA_unified["premise"] + " Choice 1: " + COPA_unified["choice1"] + " Choice 2: " + COPA_unified["choice2"])
        COPA_unified = COPA_unified[["premise / choice1 / choice2", "label", "raw query"]]
        COPA_unified['label'].replace(0, 'Choice 1', inplace=True)
        COPA_unified['label'].replace(1, 'Choice 2', inplace=True)
        return COPA_unified
