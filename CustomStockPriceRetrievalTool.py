from langchain.tools import BaseTool
import requests
from bs4 import BeautifulSoup


class CustomStockPriceRetrievalTool(BaseTool):
    # The name of the tool
    name = "Stock Price Lookup"

    # The description should be robust enough to help the LLM know when it
    # should utilize this tool.  For example if you take off the last
    # sentence instructing to only pass the stock symbol, the LLM will
    # pass a different string that will break the lookup.
    # try commenting that out to see the different behavior
    description = """
        useful for when you already know the stock trading symbol and need 
        to answer a question about a stock trading price. Pass only the stock
        trading symbol.
        """

    def _run(self, query: str):

        # We use yahoo to load a page of content just like you
        # would in a browser.  Then, because the resulting
        # html is huge and exceeds our LLM token size,
        # we cheat a little and just extract a "blob" of that
        # html.  But what's cool is the LLM can parse thru
        # this chunk of stuff and find the stock price

        base_url = "https://finance.yahoo.com/quote/"

        url = base_url + query + "/"

        # Warning... no error/response checking, so this
        # code is brittle.
        response = requests.get(url)

        # Helper so we can parse up the html
        soup = BeautifulSoup(response.text, features="html.parser")

        # This will return a text string that still has all the
        # html markup/attributes.  The LLM is smart enough to
        # extract the trading price out of all this
        element = soup.find_all("fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)")

        # this chunk of code would strip out all the html
        # shizzle and return just the price
        # price = price[0].next.get_text()

        return element

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("We do not support async")