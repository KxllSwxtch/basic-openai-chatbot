import gradio as gr
import openai

# MAKE SURE TO USE YOUR OPENAI API KEY
openai.api_key = open('key.txt', 'r').read().strip('\n')

message_history = []


def predict(input):
    global message_history

    message_history.append({'role': "user", 'content': str(input)})
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=message_history
    )
    reply_content = completion.choices[0].message.content

    print(reply_content)

    message_history.append({'role': 'assistant', 'content': reply_content})
    response = [(message_history[i]['content'], message_history[i+1]['content'])
                for i in range(0, len(message_history)-1, 2)]

    return response


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()

    with gr.Row():
        txt = gr.Textbox(show_label=False,
                         placeholder="Enter your message here").style(container=True)
        txt.submit(predict, txt, chatbot)
        txt.submit(None, None, txt, _js="() => {''}")

demo.launch()
