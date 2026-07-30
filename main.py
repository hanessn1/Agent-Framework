from agent.messages import MessageHistory
from agent.agent import Agent


history=MessageHistory("You are a helpful assistant. You use tools when appropriate")

agent=Agent(
    llm=ChatLLM(),
    history=history,
    tools=registry,
    stream=False
)

answer=agent.run("What is the current time? and what is 238*7234?")
print(answer)

# ------------ no streaming ------------
message=stream.choices[0].message
print(message.content)
print(message.tool_calls)

if message.tool_calls:
    tool_call=message.tool_calls
    if tool_call.function.name=="get_time":
        result=get_time()

        # append assistant tool call
        HISTORY.append({
            "role":"assistant",
            "tool_calls":message.tool_calls
        })

        # add tool output
        HISTORY.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":str(result)
        })

        # print(messages)
        # ask model again


# ----------- streaming -----------
# tool_name=""
# tool_arguments=""

# for chunk in stream:
#     delta=chunk.choices[0].delta

#     if(delta.tool_calls):
#         tc=delta.tool_calls[0]
#         print(tc)

#         if tc.function.name:
#             tool_name+=tc.function_name

#         if tc.function.arguments:
#            tool_arguments+=tc.function.arguments

#     print(chunk.choices[0].delta.content,end='')

# print(tool_name)
# print(tool_arguments)