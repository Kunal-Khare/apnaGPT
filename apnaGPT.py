'''


import chainlit as cl
import ollama


@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "intersaction",
        {
            {
                "role":"system",
                "content":"You are amazing assist"
            }
        },
    )


    msg =cl.Message(content="")

    start_message = "Hello, I'm your CHUT assistant"

    for token in start_message:
        await msg.stream_token(token)

        await msg.send()

 
 # get interaction object
@cl.step(type="tool")
async def tool(input_message):

    interaction = cl.user_session.get("interaction")

#add to history
    interaction.append({"role":"user", 
                        "content": input_message})
    

# give the response
    response = ollama.chat(model="deepseek-r1",
                           message=interaction)
    

    interaction.append({"role": "assistant",
                        "content": response.message.content})
    

    # add the response to history
    return response


#invoking the tool method
@cl.on_message
async def message(message: cl.Message):
    tool_res = await tool(message.content)

    msg = cl.Message(content="")


# response back to user
    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()    
    '''


import chainlit as cl
import ollama

@cl.on_chat_start
async def start_chat():
    # Corrected the structure of the dictionary
    cl.user_session.set(
        "interaction",  # Fixed spelling from "intersaction" to "interaction"
        [
            {
                "role": "system",
                "content": "You are an amazing assistant"
            }
        ],
    )

    msg = cl.Message(content="")
    start_message = "Hello, I'm your assistant"

    for token in start_message:
        await msg.stream_token(token)

    await msg.send()  # Moved outside of the loop to send the complete message once


# Get interaction object
@cl.step(type="tool")
async def tool(input_message): 
    interaction = cl.user_session.get("interaction")

    # Add to history
    interaction.append({"role": "user", "content": input_message})

    # Give the response
    response = ollama.chat(model="deepseek-r1:1.5b", messages=interaction)

    interaction.append({"role": "assistant", "content": response.message.content})

    # Add the response to history
    return response


# Invoking the tool method
@cl.on_message
async def message(message: cl.Message):
    tool_res = await tool(message.content)

    msg = cl.Message(content="")

    # Response back to user
    for token in tool_res.message.content:
        await msg.stream_token(token)

    await msg.send()  # Ensure this is called after streaming tokens
