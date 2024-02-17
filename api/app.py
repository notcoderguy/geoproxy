import random
import json

from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

def get_proxy_as_json(text):
    """
    Parse the given text to extract proxy information and return it as a JSON object.

    Parameters:
    text (str): The text containing proxy information.

    Returns:
    dict: A dictionary containing the extracted proxy information, including 'ip', 'port', 'country', and 'anonymous' flag.
    """
    try:
        values = text.strip().split(",")

        if len(values) != 5:
            raise ValueError("Invalid proxy format: expected 5 comma-separated values")

        ip_port = values[0].split(":")
        ip = ip_port[0]
        port = int(ip_port[1])
        country = values[4]
        is_anonymous = values[3].lower() == "elite"

        proxy_data = {
            "ip": ip,
            "port": port,
            "country": country,
            "anonymous": is_anonymous
        }

        return proxy_data
    except (ValueError, IndexError) as e:
        raise ValueError(f"Error parsing proxy text: {e}") from e


def get_proxy(TYPE, google_pass, anonymous, amount):
    """
    Retrieves a list of proxies of a specified type from a text file, filters the proxies based on the provided criteria, and returns a list of proxy objects in JSON format.

    Parameters:
    TYPE (str): The type of proxy to retrieve.
    google_pass (bool): Whether to use proxies that pass Google reCAPTCHA.
    anonymous (bool): Whether to use anonymous proxies.
    amount (int): The number of proxies to retrieve.

    Returns:
    list: A list of proxy objects in JSON format.
    """
    TYPE = TYPE.upper()
    with open(f'out/{TYPE}.txt', 'r') as f:
        proxies = f.readlines()
    proxies = [x.strip() for x in proxies]
    result = []
    
    try:
        for i in range(amount):
            if google_pass:
                if anonymous:
                    proxies = [x for x in proxies if x.strip().split(",")[3].lower() == "elite"]
                random_proxy = get_proxy_as_json((random.choice(proxies)))
                result.append(random_proxy)
            else:
                if anonymous:
                    proxies = [x for x in proxies if x.strip().split(",")[3].lower() == "elite"]
                random_proxy = get_proxy_as_json((random.choice(proxies)))
                result.append(random_proxy)
    except IndexError:
        return None
        
    return result
    

@app.get("/")
def read_root():
    """
    A function that handles the root endpoint and returns information about the GeoIP API.
    """
    return {
        "message":"Welcome to the GeoIP API!",
        "version":"1.0.0",
        "website":"https://geoproxy.in",
        "documentation":"https://geoproxy.in/docs",
        "github":"https://github.com/notcoderguy/geoproxy-db",
        "author":"https://notcoderguy.com"
    }
    
@app.get("/{TYPE}")
def read_item(TYPE: str, format: str = Query("txt"), google_pass: bool = Query(False), anonymous: bool = Query(False), amount: int = Query(1)):
    """
    This function takes in parameters TYPE, format, google_pass, anonymous, and amount. 
    TYPE is a string, format is a string with a default value of "txt", google_pass and anonymous are boolean with default values of False, and amount is an integer with a default value of 1. 
    The function first checks if the input TYPE is valid and returns an error if not. Then it checks the amount and returns an error if it's invalid. 
    If all checks pass, it calls the get_proxy function with the input parameters and returns the result based on the format provided. 
    If the format is 'json', it returns the proxies as is. If the format is 'txt', it returns the proxies in a newline-separated string. 
    If the format is neither 'json' nor 'txt', it returns an error. 
    """
    TYPE = TYPE.upper()
    if TYPE not in ["HTTP", "SOCKS4", "SOCKS5"]:
        return {"error": "Invalid proxy type.  Choose 'HTTP', 'SOCKS4', or 'SOCKS5'"}
    
    if amount < 1:
        return {"error": "Amount must be greater than 0"}
    elif amount > 50:
        return {"error": "Amount must be less than 50"}
    
    proxies = get_proxy(TYPE, google_pass, anonymous, amount)

    if proxies is None:
        return {"error": "Either there are not enough proxies or the requested proxies are invalid"}
    
    if format.lower() == "json":
        return proxies
    elif format.lower() == "txt":
        txt_output = "\n".join([f"{proxy['ip']}:{proxy['port']}" for proxy in proxies])
        return Response(content=txt_output, media_type="text/plain") 
    else:
        return {"error": "Invalid format.  Choose 'txt' or 'json'"}
