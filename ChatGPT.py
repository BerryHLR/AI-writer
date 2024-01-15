import openai
# openai.api_key = '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'
openai.api_key = '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'
# openai.api_key='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'
# openai.api_key = 'sk-JalnO0ioesEEXlAl9e5558A0FaF44b1aA17e41C2097b5287'
# openai.base_url = 'https://d2.xiamoai.top'
proxy = {
    'http':'127.0.0.1:7890',
    'https':'127.0.0.1:7890'
}
openai.ProxiesTypes=proxy
def ChatGPT(prompt, max_tokens):
    model_engine = "text-davinci-003"
 
    completions = openai.completions.create(
        model=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.5,
    )
    answer = completions.choices[0].text
    return answer