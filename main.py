import os
import openai
import chainlit as cl
import dotenv

dotenv.load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

model_name = "text-davinci-003"

settings = {
    "temperature": 0.9,
    "max_tokens": 500,
    "top_p": 0.3,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["<END>"],
}

prompt = """
About your Owner
Shubham choudhari
nickname joey
You are Joey's (Shubham choudhari) personal ai assistant CARA
you will answere question about him and behalf of him.
If someone ask you code give it in markdown
:
{question}
"""


@cl.on_message
def main(message: str):
    fromatted_prompt = prompt.format(question=message)
    msg = cl.Message(
        content="",
        prompt=fromatted_prompt,
        llm_settings=cl.LLMSettings(model_name=model_name, **settings),
    )

    for resp in openai.Completion.create(
        model=model_name, prompt=fromatted_prompt, stream=True, **settings
    ):
        token = resp.choices[0].text
        msg.stream_token(token)

    text = msg.send()

