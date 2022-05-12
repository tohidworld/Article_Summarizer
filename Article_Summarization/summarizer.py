from gensim.summarization.summarizer import summarize



def textSummarizer(text):
    try:
        text = text.replace('\n', '')
    except:
        pass
    try:
        body = summarize(text, ratio=0.3)
        body = str(body)
        status = 0
    except Exception as e:
        body = str(e)
        status= 1
    #print(body)
    return status, body
'''text = 'The five remaining Congress MLAs in Meghalaya have written to Chief Minister Conrad Sangma, announcing their decision to join the National People's Party (NPP)-led Mghalaya Democratic Alliance (MDA) government in the state.'
status, body = textSummarizer(text)
print(body)'''
