from lib.FileHandler import FileHandler
from lib.Requester import Requester
from lib.CloudflareRequester import CloudflareRequester
from lib.Logger import Logger
import asyncio
import random
from concurrent.futures import ThreadPoolExecutor

PROFILE_FILE = "account.txt"
TOKEN_FILE = "token.txt"
PROXY_FILE = "proxy.txt"
THREADS = 10

logger = Logger()
result = []


def login(index, proxy, email, password):
    try:
        api = Requester(
            base_url="https://api.oasis.ai",
            proxies={"http": proxy, "https": proxy}
        )
        
        res = api.post("internal/auth/login", json={
            "email": email,
            "password": password,
            "rememberSession": True
        })
        logger.debug(f"POST Login =>  {res}")
        result[index] = res["token"]


        
    except Exception as e:
        logger.error(f"Error: {e}")
        result[index] = "None"


async def main():
    accounts = FileHandler(PROFILE_FILE).read()
    proxies = FileHandler(PROXY_FILE).read()
    profiles = []
    
    # Setup profiles
    for i in range(len(accounts)):
        result.append("None")
        email, password = accounts[i].split("|")
        profiles.append({
            "index": i,
            "email": email,
            "password": password,
            "proxy": proxies[i%(len(proxies)-1)]
    })
    
    choice = input("Do actions: 1. Login 2. Do something: ")

    
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        loop = asyncio.get_event_loop()
        if choice == "1":
            logger.info("-----Start login------")
            tasks = [loop.run_in_executor(executor, login, profile["index"], profile["proxy"], profile["email"], profile["password"]) for profile in profiles]
            await asyncio.gather(*tasks)

            # Write result to file
            FileHandler(TOKEN_FILE).write(result)


if __name__ == "__main__":
    asyncio.run(main())
    