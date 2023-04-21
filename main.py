import os
import sys
import traceback

from langchain.agents import AgentType, initialize_agent

from langchain.chat_models import ChatOpenAI

# Our custome tool
from CustomStockPriceRetrievalTool import CustomStockPriceRetrievalTool

# global variable for our env key
ENV_VAR_OPENAI_API_KEY = "OPENAI_API_KEY"


def check_openai_api_key_available():

    try:
        openai_api_key = os.environ[ENV_VAR_OPENAI_API_KEY]

        if not openai_api_key:
            print("The environment variable " + ENV_VAR_OPENAI_API_KEY + " was found but it does not have a value.")
            print("Please set this to your OpenAI API key.")
            return False

        # if we made it here, we have a key.  It might not work, but
        # at least it's something
        return True

    except KeyError:
        print("Could not find an environment varable named " + ENV_VAR_OPENAI_API_KEY )
        print("Make make sure to set this environment variable with your OPENAI_API_KEY")
        return False


def start_agent_with_custom_tool():

    # Tools are the "things" the LLM use to help
    # figure out/solve what it's been asked to do
    tools = [CustomStockPriceRetrievalTool()]

    # the large langauge model our agent is
    # going to use
    llm = ChatOpenAI(temperature=0)

    # The agent is constructed with the tools/llm.  The AgentType drives
    # Lanchain to select some of its internal prompts that it will use
    # to bootstrap the agent.
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

    # What will happen here is the LLM will figure out that our
    # custom tool needs a stock symbol, so it will internally find
    # the symbol from it's training, then because our custom tool says
    # "use me to lookup a stock price" it will invoke our custom tool.
    response = agent.run("What is the stock price for Apple?")

    print(response)


if __name__ == '__main__':

    try:
        if not check_openai_api_key_available():
            sys.exit("No API key set, terminating.")

        start_agent_with_custom_tool()

    except Exception as exp:
        print("Well, this is embarrassing. I barfed :(... technical details follow")
        print(exp)
        traceback.print_exc()