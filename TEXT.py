METHOD_SELECTOR_TEXT = """
TASK:
You will be provided with user queries for classification tasks.
Select the most efficient prompting METHOD for the user's classification task. Use INSTRUCTIONS to select the METHOD.
Always end your answer with the phrase "The answer is..." and then name the selected prompting METHOD.

INSTRUCTIONS:
'''
- METHOD name: Standard Zero-Shot Learning. Description: a detailed reflection process is not required, user query contains zero examples, the model is expected to generate a response right after processing the user query.
  Examples:
  [User Query: Classify the following dishes into salads, main courses or desserts.
  Method: Standard Zero-Shot Learning.]
  [User Query: Classify the following drinks into  strong drinks or soft drinks.
  Method: Standard Zero-Shot Learning.]

- METHOD name: Standard One-Shot Learning. Description: a detailed reflection process is not required in the answer, user query contains a query and one short straightforward answer example not supported by a step by step reflection process; the model is expected to generate a response right after processing the user query and a related example, logical justifications for the conclusions in the answer are not needed. This method should be preferred for the tasks that contain one example with short straightforward answers without any detailed explanation of the model's reasoning process.
  Examples:
  [User Query: Classify the following dishes into salads, main courses or desserts. Example: Ceaser - salad. What is an ice-cream?
  Method: Standard One-Shot Learning.]
  [User Query: Determine if beer is a soft or hard drink? Examples: Coke is a soft drink.
  Method: Standard One-Shot Learning.]

- METHOD name: Standard Few-Shot Learning. Description: a detailed reflection process is not required in the answer, user query contains a query and two or more answer examples, examples include short straightforward answers not supported by a step by step reflection process; the model is expected to generate a response right after processing the user query and related examples, logical justifications for the conclusions in the answer are not needed. This method should be preferred for the tasks that contain examples with short straightforward answers without any detailed explanations of the model's reasoning process.
  Examples:
  [User Query: Classify the following dishes into salads, main courses or desserts. Example: Ceaser - salad, Tiramisu - dessert. What is an ice-cream?
  Method: Standard Few-Shot Learning.]
  [User Query: Determine if beer is a soft or hard drink? Examples: Coke is a soft drink.  Whiskey is a hard drink.
  Method: Standard Few-Shot Learning.]

- METHOD name: Few-Shot Chain-of-Thought. Description: user query contains one or more answer examples, examples include complete answers given in the form of step by step reflection that represents a logical justification for the final conclusion, a detailed reflection process is required in the model's answer; аfter processing the user query the model is expected to first produce detailed explanations in the form of a chain of thought reflection process on how a certain conclusion was made and then to generate the final answer. In case examples given in user queries do not contain a chain of thought reflection on how a model came to the response, then Few-Shot Chain-of-Thought method shouldn't be selected.
  Examples:
  [User Query: Classify the following victuals into either food or drink. Example: Steak - steak is a piece of fried meat, it's not liquid and one can't drink  it, one needs to chew it. The answer is: steak is food.
  Method: Few-Shot Chain-of-Thought]
  [User Query: Classify the following drinks into hard drinks or soft drinks. Example: Coke - coke is a fizzy flavored drink that does not contain alcohol, fizzy drinks without alcohol are soft drinks. The answer is:Coke is a soft drink.
  Method: Few-Shot Chain-of-Thought]

- METHOD name: Zero-Shot Chain-of-Thought. Description: user query contains NO answer examples, a detailed reflection process is required in the model's answer, this method is useful for the tasks that could be split into several steps and involve straightforward decision-making or categorization based on simple criteria; аfter processing the user query the model is expected to first respond "Let's think step by step" or with another similar phrase, then reproduce its' reasoning in detail for each step of the task, give logical justifications for the conclusions it's making and finally generate the final answer. For cases when Zero-Shot Chain-of-Though is enough to generate a quality answer, the model should not consider any further and more complex methods.
  Examples:
  [User Query: Review these recipes, evaluate how long it takes to cook a dish from each recipe and classify the recipes form quickest to longest.
  Method: Zero-Shot Chain-of-Thought]
  [User Query: Countries may be devided into strong and weak economies. What about Japan?
  Method: Zero-Shot Chain-of-Thought]

- METHOD name: Tree-of-Thought. Description: the model first comes up with intermediate solutions instead of trying to reach the full solution in a single shot; the model monitors thought process and determines whether to continue trying from the current thought or backtrack to the previous thought and explore alternative directions. Tree-of-Thought method is useful for tasks that require search and planning or for tasks where the user is trying to arrive at a decision based on several criteria and alternatives. In its response the model is expected to reproduce its thought process in detail and give resoning for selecting or rejecting one of multiple decision paths. The model must only use Tree-of-Thought method in case of comlex tasks in user queries where the response quality could be significantly enhanced by the Tree-of-Thought method. If a task may be fully solved by either Standard Zero-Shot Learning method or Standard Few-Shot Learning method or Few-Shot Chain-of-Thought method or Zero-Shot Chain-of-Thought method , then there is no need for the model to select Tree-of-Thought.
  Examples:
  [User Query: Help me decide if it's ethical or not ethical to wear fur?
  Method: Tree-of-Thought]
  [User Query: Check these people's characters and behavior descriptions and classify them into extravers or introverts.
  Method: Tree-of-Thought]

- METHOD name: CARP. Description: CARP stands for Clue and Reasoning Prompting, a detailed reflection process is required from LLM, user query contains zero examples, unlike Tree-of-Thought which  encourages the exploration of multiple lines of reasoning, CARP is linear and focused on on identifying specific clues that can guide reasoning. CARP involves three steps. Step 1 - receiving text or linguistic information that should be classified, extracting clues such as keywords, phrases, contextual information, semantic relations, semantic meaning, tones, references. Step 2 - diagnostics of reasoning process based on the clues and the received text and solving the overall classification task. Step 3 - considering the clues, the reasoning process and the received text, finalizing classification task and producing the response to the user request. CARP should be prioritized over other methods when a user request is dealing with complex text or liguistic or semantic classification requests.
  Examples:
  [User Query: Review the input at the level of key phrases and emotional emphasis. Determine the overall sentiment of the input as Positive or Negative.
  Input: "Cross their names off the list."
  Method: CARP]
  [User Query: Review this corpus of letters written by one person and classify the author as an introvert or an extravert. Pay attention to keywords, contextual information and references in the corpus.
  Method: CARP]
  [User Query: Students were asked to write an essay on the topic of "Good Мorning" in such a way that only nouns, adjectives, adverbs, prepositions and conjunctions were present in the essay. Check out their essays and decide which ones fully meet the requirements?
  Method: CARP]
'''
Q: Classify these movie reviews into positive, negative and neutral.
A: As long as this task doesn't require to reproduce a detailed reasoning process and  the user didn't give any answer examples, Standard Zero-Shot Learning method should fit. The answer is Standard Zero-Shot Learning.

Q: Classify these movie reviews into positive, negative or neutral. Example: review 1 - positive.
A: As long as this task doesn't require to reproduce a detailed reflection process and the user query has one answer example that is short, straightforward, not supported by a step by step thinking and contain no logical justifications of the model's answer, Standard One-Shot Learning method should fit. The answer is Standard One-Shot Learning.

Q: Classify these movie reviews into positive, negative or neutral. Examples: review 1 - positive, review 2 - negative, review 3 - neutral. What is review 4?
A: As long as this task doesn't require to reproduce a detailed reflection process and the user query has one or more answer examples that are short, straightforward, not supported by a step by step thinking and contain no logical justifications of the model's answer, Standard Few-Shot Learning method should fit. The answer is Standard Few-Shot Learning.

Q: Classify these movie reviews into positive, negative or neutral. Examples: review 1 says "The movie is great!", the word "great" has a positive sentiment, so the answer is review 1 is positive; review 2 says "The movie is boring", the word "boring" has a negative sentiment, so the answer is review 2 is negative.
A: As long as this task requires to reproduce a detailed reflection process, user query contains examples, the answers in examples are complete and detailed logical justifications of the final model's responses are given, Few-Shot Chain-of-Thought method should fit.The answer is Few-Shot Chain-of-Thought.

Q: Evaluate the sentiment of the movie reviews and classify those reviews into positive, negative and neutral.
A: Let's think step by step. As long as the user didn't support user queries by any examples and the task could be split into several steps like: step 1 - evaluating the sentiment of reviews and step 2 - classifying those reviews into positive, negative or neutral, the best method would be to think step by step and reproduce reasoning process for each of the steps, give logical justifications for the conclusions the model is making and finally, generate the answer, thus Zero-Shot Chain-of-Thought method should fit. The answer is Zero-Shot Chain-of-Thought.

Q: Classify viruses as alive or not alive.
A: As long as no response examples are given and answering this complex task involves a few intermediate solutions such as: what are the biological and philosopical criteria of life and if viruses satisfy these criteria or not, the model should build a decision tree in order to consider all the alternatives, decline inefficient decision paths, return to the most effective one and reproduce a detailed thought process in the response. In this case the correct method would be Tree-of-Thought. The answer is Tree-of-Thought.

Q: I'm trying to determine whether this article is discussing climate change or environmental conservation. Can you help me classify it?
A: As long as this query contains no examples and involves a linear classification task that requires the following steps: 1 - extracting clues (such as keywords like "climate change", "environmental conservation", phrases related to these topics, contextual information about the article's content, and any references to scientific studies or policies), 2 - diagnosing the reasoning process by analyzing the clues and the text in order to determine the main focus of the article, consider the tone, references, and overall message to make a classification, 3 - finalizing the classification task by considering all the clues and the reasoning process to confidently determine whether the article is about climate change or environmental conservation and provide a response to the user, we could conclude that the answer is CARP. The answer is CARP.
"""
METHOD_SELECTOR_TEXT_FOR_OLLAMA = """
TASK:
You will be provided with user queries for classification tasks.
Select the most efficient prompting METHOD for the user's classification task. Use INSTRUCTIONS to select the METHOD.
Always end your answer with the phrase "The answer is " and then name the selected prompting METHOD.

INSTRUCTIONS:
- METHOD name: Standard Zero-Shot Learning. Description: a detailed reflection process is not required, user query contains zero examples, the model is expected to generate a response right after processing the user query.
- METHOD name: Standard One-Shot Learning. Description: a detailed reflection process is not required in the answer, user query contains a query and one short straightforward answer example not supported by a step by step reflection process; the model is expected to generate a response right after processing the user query and a related example, logical justifications for the conclusions in the answer are not needed. This method should be preferred for the tasks that contain one example with short straightforward answers without any detailed explanation of the model's reasoning process.
- METHOD name: Standard Few-Shot Learning. Description: a detailed reflection process is not required in the answer, user query contains a query and two or more answer examples, examples include short straightforward answers not supported by a step by step reflection process; the model is expected to generate a response right after processing the user query and related examples, logical justifications for the conclusions in the answer are not needed. This method should be preferred for the tasks that contain examples with short straightforward answers without any detailed explanations of the model's reasoning process.
- METHOD name: Few-Shot Chain-of-Thought. Description: user query contains one or more answer examples, examples include complete answers given in the form of step by step reflection that represents a logical justification for the final conclusion, a detailed reflection process is required in the model's answer; аfter processing the user query the model is expected to first produce detailed explanations in the form of a chain of thought reflection process on how a certain conclusion was made and then to generate the final answer. In case examples given in user queries do not contain a chain of thought reflection on how a model came to the response, then Few-Shot Chain-of-Thought method shouldn't be selected.
- METHOD name: Zero-Shot Chain-of-Thought. Description: user query contains NO answer examples, a detailed reflection process is required in the model's answer, this method is useful for the tasks that could be split into several steps and involve straightforward decision-making or categorization based on simple criteria; аfter processing the user query the model is expected to first respond "Let's think step by step" or with another similar phrase, then reproduce its' reasoning in detail for each step of the task, give logical justifications for the conclusions it's making and finally generate the final answer. For cases when Zero-Shot Chain-of-Though is enough to generate a quality answer, the model should not consider any further and more complex methods.
- METHOD name: Tree-of-Thought. Description: the model first comes up with intermediate solutions instead of trying to reach the full solution in a single shot; the model monitors thought process and determines whether to continue trying from the current thought or backtrack to the previous thought and explore alternative directions. Tree-of-Thought method is useful for tasks that require search and planning or for tasks where the user is trying to arrive at a decision based on several criteria and alternatives. In its response the model is expected to reproduce its thought process in detail and give resoning for selecting or rejecting one of multiple decision paths. The model must only use Tree-of-Thought method in case of comlex tasks in user queries where the response quality could be significantly enhanced by the Tree-of-Thought method. If a task may be fully solved by either Standard Zero-Shot Learning method or Standard Few-Shot Learning method or Few-Shot Chain-of-Thought method or Zero-Shot Chain-of-Thought method , then there is no need for the model to select Tree-of-Thought.
- METHOD name: CARP. Description: CARP stands for Clue and Reasoning Prompting, a detailed reflection process is required from LLM, user query contains zero examples, unlike Tree-of-Thought which  encourages the exploration of multiple lines of reasoning, CARP is linear and focused on on identifying specific clues that can guide reasoning. CARP involves three steps. Step 1 - receiving text or linguistic information that should be classified, extracting clues such as keywords, phrases, contextual information, semantic relations, semantic meaning, tones, references. Step 2 - diagnostics of reasoning process based on the clues and the received text and solving the overall classification task. Step 3 - considering the clues, the reasoning process and the received text, finalizing classification task and producing the response to the user request. CARP should be prioritized over other methods when a user request is dealing with complex text or liguistic or semantic classification requests.
""" 
ONE_SHOT_LEARNING_TEXT = """
Act as a prompt engineer.
You will be provided with user queries.
Using the user’s query write a TASK for the model.
Use INSTRUCTIONS to write the TASK.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Then, provide only one example of the data as Q and the expected output as A.
Finally, create the space and ask the user to put his DATA for the TASK.
Use EXAMPLES for the output format.
'''

EXAMPLES:
'''
TASK: Classify the following text into positive, neutral or negative.

Q: Stora Enso Oyj said its second-quarter result would fall by half compared with the same period in 2007.
A: Negative
'''
"""

FEW_SHOT_LEARNING_TEXT = """
Act as a prompt engineer.
You will be provided with user queries.
Using the user’s query write a TASK for the model.
Use INSTRUCTIONS to write the TASK.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Then, provide no more than five examples of the data as Q and the expected output as A.
Finally, create the space and ask the user to put his DATA for the TASK.
Use EXAMPLES for the output format.
'''

EXAMPLES:
'''
TASK: Classify the following text into positive, neutral or negative.

Q: Stora Enso Oyj said its second-quarter result would fall by half compared with the same period in 2007.
A: Negative
'''
"""

ZERO_SHOT_LEARNING_TEXT = """
Act as a prompt engineer.
You will be provided with user queries.
Using the user’s query write a classification task for the model.
Use INSTRUCTIONS to write the task.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Finally, create the space as Q and A and ask the user to put his DATA  in Q for the TASK.
Use EXAMPLES for the output format.
'''

EXAMPLES:
'''
TASK: Classify the following text into positive, neutral or negative.
'''
"""

ZERO_SHOT_CHAIN_OF_THOUGHT_TEXT = """
"f""""""
Act as a prompt engineer. 
You will be provided with user queries.
Using the user’s query write a classification task for the model.
Use information in INSTRUCTIONS to write the TASK.

INSTRUCTIONS:
'''
First, clearly define the TASK, specifying that the model should generate a sequence of connected ideas before reaching the solution. 
Then, create the space as Q and A and ask the user to put his DATA in Q [ ] for the TASK.
Finally, put in A the following phrase ""Let's think step by step.""
Use EXAMPLES for the output format.
'''

EXAMPLES:
'''
TASK: Classify the following text into positive, neutral or negative.
'''
"""

FEW_SHOT_CHAIN_OF_THOUGHT_TEXT = """
"f""""""
Act as a prompt engineer. 
You will be provided with user queries.
Using the user’s query write a classification task for the model.
Use information in INSTRUCTIONS to write the TASK.
Limit the number of words to 250.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Then, provide no more than three examples of the DATA as Q and the expected output with reasoning as A.
If there are examples in user's query, put them into the format of Q and A, then provide a logical explanation on how the answer was achieved in A.
Finally, create the space and ask the user to put his DATA in Q for the TASK.
Use EXAMPLES for the output format.
'''

EXAMPLES:
'''
TASK: Classify the following news into positive, negative or neutral.

Q: Cash flow from operations rose to EUR 52.7 mln from EUR 15.6 mln in 2007.
A: The text mentions that “cash flow from operations rose to EUR 52.7 million from EUR 15.6 million in 2007.” This indicates a positive financial aspect, as there’s a significant increase in cash flow from operations. So the overall classification for this text would be positive due to the notable rise in cash flow. The answer is positive.

Q: Today the market experienced moderate fluctuations with no major disruptions. Several companies reported earnings in line with the expectations, and the economic indicators showed modest growth.
A: 
1. Market Fluctuations: The text mentions that “the market experienced moderate fluctuations with no major disruptions”. Fluctuations alone do not convey a positive or negative sentiment; the absence of major disruptions suggests stability. 
2. Companies’ Earnings: It states that “Several companies reported earnings in line with the expectations”. Reporting earnings in line with expectations is generally considered neutral, as it neither exceeds nor falls short of projections. 
3. Economic Indicators: The text notes that “economic indicators showed modest growth”. Modest growth is generally positive, indicating a degree of economic improvement. Considering the overall information, the text contains elements that could be interpreted as both neutral and positive. However, the lack of major disruptions and the general tone of statements suggest a more neutral sentiment overall. The answer is neutral.
'''
"""

CARP_TEXT = """
Act as a prompt engineer. 
You will be provided with user queries.
Based on the user’s query write the prompt.
Use the information in the INSTRUCTION to write the prompt.
Use EXAMPLES for the output format.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Then, create INPUT and ask the user to put his DATA in [] for the TASK.
Finally, write the following:  ""First, list CLUES (i.e., keywords, phrases, contextual information, semantic relations, semantic meaning, tones, \
references) that support the category determination of input.
Second, deduce the diagnostic REASONING process from premises (i.e., clues, input) that supports the INPUT \
category determination (Limit the number of words to 130).
Third, based on clues, reasoning and input, determine the category.""
'''

EXAMPLES:
'''
TASK: Classify the following film reviews into positive, neutral or negative.
INPUT: [Please insert your data here].

First, list CLUES (i.e., keywords, phrases, contextual information, semantic relations, semantic meaning, tones, \
references) that support the category determination of input.
Second, deduce the diagnostic REASONING process from premises (i.e., clues, input) that supports the INPUT \
category determination (Limit the number of words to 130).
Third, based on clues, reasoning and input, determine the category.
'''
"""

TREE_OF_THOUGHT_TEXT = """
"f""""""
Act as a prompt engineer. 
You will be provided with user queries.
Based on the user’s query write the prompt.
Use the information in the INSTRUCTION to write the prompt.
Use EXAMPLES for the output format.

INSTRUCTIONS:
'''
First, define the task you want the model to perform and write it in TASK.
Then, create the space and ask the user to put his DATA in [] for the TASK.
Then, write the following: ""Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking,\
then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.""
After that, formulate the question based on user query in the format: The question is...
'''

EXAMPLES:
'''
TASK: Classify the film reviews into positive, neutral or negative. [Please insert your data here.]

Imagine three different experts are answering this question.
All experts will write down 1 step of their thinking,\
then share it with the group.
Then all experts will go on to the next step, etc.
If any expert realises they're wrong at any point then they leave.
The question is to classify the film reviews into positive, neutral or negative.
'''
"""