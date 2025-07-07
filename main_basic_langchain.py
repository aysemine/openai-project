from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from tools import calculator
load_dotenv()


def main():
    model = ChatOpenAI(temperature=0)

    tools = [calculator]
    agent_executer = create_react_agent(model, tools)

    print("Welcome! I'am your AI assitant. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            break

        print("\nAssitant: ", end="") ## this for assistant text and the assistant response to be in same line
        for chunk in agent_executer.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")
        print()

if __name__ == "__main__":
    main()




    