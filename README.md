# README.md

## Описание проекта

Проект предназначен для вычисления метрик производительности моделей машинного обучения на нескольких стандартных датасетах (например, SST2, MNLI, QNLI, AGNews и др.). Он использует различные методы подсказок (`prompts`) и позволяет автоматизировать процесс обработки данных и оценки результатов.

Ключевые особенности:
- Поддержка различных методов подсказок, включая **Zero-Shot**, **Few-Shot** и их вариации (**Chain-of-Thought**, **Tree-of-Thought** и др.).
- Обработка данных с использованием пользовательских моделей.
- Логирование и сохранение результатов в удобном формате для последующего анализа.

---

## Установка и настройка

1. Подготовьте файл calc_metrics_.py:
    - Укажите api-ключ
    - Выберите нужную модель
    - Тексты системных подсказок (`prompts`), используемых для генерации ответов.

2. Убедитесь, что настроен API-доступ для модели, если требуется (например, OpenAI или другая платформа). 

---

## Использование

1. Запустите скрипт **`calc_metrics_our_project.py`**:
    ```bash
    python calc_metrics_our_project.py
    ```

2. По умолчанию, результаты рассчитываются только для SST2 (первые 10 строк для тестового запуска). Чтобы включить другие датасеты, раскомментируйте соответствующие строки в файле `calc_metrics_our_project.py` в секции:
    ```python
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
    ```

3. Результаты сохраняются в директорию `base_results` в формате CSV. Дополнительно, основные метрики отображаются в консоли и логируются в файл `LOG.log`.

---

## Основные классы и функции

### Класс `Metrics_Calculate_OUR`

**Описание:** 
Основной класс для расчета метрик. Использует переданную модель и датасет для обработки запросов.

- **Методы подсказок:**
  - `Standard Zero-Shot Learning`
  - `Standard One-Shot Learning`
  - `Standard Few-Shot Learning`
  - `Few-Shot Chain-of-Thought`
  - `Zero-Shot Chain-of-Thought`
  - `Tree-of-Thought`
  - `CARP`

- **Ключевые методы:**
  - `extract_method_name(response_text)` — Извлечение имени метода из ответа модели.
  - `select_method_and_process_prompt(prompt)` — Выбор метода подсказок и модификация запроса.
  - `calc_SST2_results()`, `calc_MNLI_results()` и т.д. — Подсчет результатов для каждого датасета.
  - `unify_the_output(text, classes)` — Упрощение и унификация ответов модели для сравнения с классами.

---

## Пример результатов

### Итоговая структура данных

После выполнения скрипта результаты для каждого датасета имеют следующую структуру:

### Пример консольного вывода для SST2
```text
=========RESULTS SST2=========
Класс верный?            False  True  All
Выбран класс из списка?
False                        4     0    4
True                        11    85   96
All                         15    85  100
==============================
```

## Доступные модели

Проект поддерживает работу с различными моделями для генерации текстов. Ниже представлены доступные реализации моделей и их особенности.

### 1. **BaseModel**
Базовый класс для всех моделей. Определяет общий интерфейс и структуру. Должен быть унаследован конкретной моделью.

- **Атрибуты:**
  - `max_tokens` — Максимальное количество токенов для вывода.
  - `model_name` — Имя модели.
  - `total_input_tokens` — Счётчик токенов для входных данных.
  - `total_output_tokens` — Счётчик токенов для выходных данных.

- **Метод:**
  - `get_result(prompt, system_content=None, temperature=0.7)` — Абстрактный метод, который реализуется в дочерних классах.

---

### 2. **SimpleModel**
Простая модель для демонстрации. Не использует внешние API и возвращает строку-заглушку.

- **Особенности:**
  - Лёгкая, не требует подключения к внешним сервисам.
  - Считает количество входных и выходных токенов с использованием библиотеки `tiktoken`.

- **Использование:**
  ```python
  model = SimpleModel(max_tokens=100, model='gpt-3.5-turbo', temperature=0.7)
  response = model.get_result(prompt="What is the capital of France?")
  print(response)  # Вывод: "Simple string"
  ```

### 3. **ChatGPTModel**
Реализация, использующая API OpenAI для взаимодействия с моделью ChatGPT.

- **Особенности:**
    - Поддерживает настройку температуры и длины ответа.
    - Использует библиотеку openai для работы с API.
    - Логирует данные о токенах и вызовах API.
- **Использование:**
  ```python
  model = ChatGPTModel(
    api_key="YOUR_API_KEY",
    base_url="https://api.openai.com/v1",
    model="gpt-3.5-turbo",
    temperature=0.7,
    max_tokens=100
  )
  response = model.get_result(prompt="What is the capital of France?", system_content="You are a helpful assistant.")
  print(response)  # Вывод: "The capital of France is Paris."
  ```

## Логирование
Для всех моделей настроено логирование с использованием стандартного модуля logging. Основные логи сохраняются в LOG.log