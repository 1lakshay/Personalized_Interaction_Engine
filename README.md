# gourinath-wasserstoff-AiTask

## test_chat_UI1.py 

This file contains the chatbot app using the RAG technique which isachieved using the Langcahin framework with theusage of the streamlit as to make the UI.
The wordpress plugin of this chatbpot is succesfully created and it extracts the content ofthe wordpress website in which it will beintegrated.

## RAG flow: 
Document which contains the content is extracted -> Chunks are created -> All the chunks are embedded and stored in vector database -> query is take from user -> 
query is corrected if contained the error -> context checking from the chat history if any -> Cot strategy to provided the rich perspective output -> 
similar chunks documents are retrieved -> Output in polished form is generated 

### Splitting Docs and creating vector Database:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/ecddb309-ab58-4258-88b4-422acce96df6)
 

### Prompt and chaining for corrceting query:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/e82f4e79-e36b-4229-89d6-efb3e89b19c6)

### Finding context from previous if any:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/209967ee-6290-4961-91ac-832c812fdb03)

### Using steps to reach at solution:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/07e8844d-0078-4f2c-b398-08f2e401b36a)
 
### Intializing chat_history & making previous chats visible:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/d1feac96-938d-4e7a-be06-0c211766885a)

### Code block that takes input and stores the repsonse:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/a93c0a0a-3eda-485c-8a3b-2f216704ac02)


## creating the wordpress plugin:
The plugin code is present inside the chatbot_lakshay.
in the loclhost it is created in the directory where wordpress is installed.
with file location as: xampp\htdocs\wordpress\wp-content\plugins

with the creating of the plugin it can beintegrated in anyw ordpress website with the inclusion of the shortcode which is chatbot_lakshay in this case.

### Integration of plugin in wp website:
![image](https://github.com/1lakshay/gourinath-wasserstoff-AiTask/assets/92805477/b9096118-5ea8-48b2-9dbb-101ad02670a1)



 
