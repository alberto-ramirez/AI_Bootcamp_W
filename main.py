#import ipywidgets as widgets
import re
import time
import PyPDF2
import pprint

from ikki_module import ChatGPT

review_resumes_message="You are an effective headhunter and you will be provided with a list of resumes, your task is to determine in depth the job area and subarea for which the person is more suitabale"
summarize_resumes_message="You are an efficient HR recruiter and you will be provided with a list of persons and their skills, your task is only to get the name of the person and the main job area as well as subarea"
advice_list = []
total_cost = 0
tmp_list=''
response=''
param=''
content = []
final_list = []
buffer = ''
summarizing_list = []
summarizing_cost = 0
pp = pprint.PrettyPrinter(indent=2,width=57, compact=True)
audio=0

def cost_calculator_for_GPT_3_5_turbo(response):
    '''This fucntion was previously provided, it computes the cost of each call'''
    # These 2 values are valid only for the "gpt-3.5-turbo-1106" model.
    # Check https://openai.com/pricing for up-to-date prices
    cost_of_input_tokens = 0.001
    cost_of_output_tokens = 0.002

    completion_tokens = response.model_dump()['usage']['completion_tokens']
    prompt_tokens = response.model_dump()['usage']['prompt_tokens']

    total_cost = ((prompt_tokens * cost_of_input_tokens) + (completion_tokens * cost_of_output_tokens)) / 1000
    return total_cost

if __name__ == "__main__":

    print('\n============= Hello! and Thanks for using Ikki your HR assistant =============')
    print('We will start checking all the resumes availables in the current directory')
    print('We are assuming that all the resumes are in PDF format and with searchable text, in other words, not images\n')

    bot = ChatGPT()

    # Getting the list of all files in the current directory
    file_list = ChatGPT.get_file_list()

    # Keeping only the resumes that are in pdf format
    regex = re.compile(".*.pdf")
    resumes_list = list(filter(regex.match, file_list))
    
    # Getting the content of the files by candidate
    for file in resumes_list:
        content.append( PyPDF2.PdfReader( open(file,'rb') ) )
        open(file,'rb').close()

    # Creating one list with each element have the content of the whole resume no matter the number of pages of each resume
    for i in range(len(content)):
        for j in range(len(content[i].pages)):
            buffer += content[i].pages[j].extract_text()
        final_list.append(buffer)
        buffer=''

    ### Final Section
    for k in range(len(final_list)):
        tmp_list,response=bot.chatgpt_resumes(final_list[k],review_resumes_message)
        advice_list.append(tmp_list)
        total_cost+=cost_calculator_for_GPT_3_5_turbo(response)
        print('Waiting 75 seconds for next API call ... ')
        time.sleep(75)
    
    print('\nPlease find the total cost of the whole operation in USD: ', total_cost)
    print('Below is the list of advices for each candidate: \n')
    pp.pprint(advice_list)
    print('\nIn case you do not have time to read all the information, do not worry we will summarize for you')

    for j in range(len(advice_list)):
        tmp_list,response=bot.chatgpt_resumes(advice_list[j],summarize_resumes_message)
        summarizing_list.append(tmp_list)        
        total_cost+=cost_calculator_for_GPT_3_5_turbo(response)
        print('Waiting 75 seconds for next API call ... ')
        time.sleep(75)        

    print('\nPlease find the total cost of the whole operation in USD after summarize the resumes: ', total_cost)
    print('Below is the list resumes summarized for each candidate: \n')
    pp.pprint(summarizing_list)

    print('\nWe have created audio tracks with the profiles summarized in case you needed\n')

    for i in range(len(summarizing_list)):
        audio=bot.chatgpt_textTo_audio(summarizing_list[i])
        audio.stream_to_file(f"candidate_Number_{i}.mp3")
        print('Waiting 75 seconds for next API call ... ')
        time.sleep(75)

    print('Please find below the list of the current files:\n')
    pp.pprint(ChatGPT.get_file_list())
    print('\n------ Thanks for use Ikki assistant.\n')