import os
from langchain_core.tools import tool
from services.groq_llm import llm
import requests
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from typing import List,Dict,Any
load_dotenv()


WALLET_ADDRESS=os.getenv("WALLET_ADDRESS")
ETHERSCAN_API_KEY=os.getenv("ETHERSCAN_API_KEY")

# This tool is also working
@tool
def get_single_address_balance(address: str) -> Dict[str, Any]:
    """
    Fetch the Ethereum balance for a single given address provided by the user using the Etherscan API.

    Parameters:
    - address (str): The Ethereum address to check the balance for.

    Returns:
    - JSONResponse: The balance in JSON format or an error message if the request fails.
    """
    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url=API_URL)
    if response.status_code == status.HTTP_200_OK:
        result = response.json()
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )

# tool for getting the get_muliple_address_balance.

# Not working giving empty '' Output
@tool
def get_multiple_address_balance(addresses: List[str])->Dict[str,Any]:
    """
    Fetch the Ethereum balance for multiple addresses given by user using the Etherscan API.
    
    Parameters:
    - addresses (List[str]): The list of Ethereum addresses to check the balance for.
    
    Returns:
    - dict: A dictionary containing the balances for the provided addresses or an error message.
    """
    if not addresses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Address list cannot be empty."}
        )

    # Join the list of addresses into a single comma-separated string
    address_str = ','.join(addresses)
    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=balancemulti&address={address_str}&tag=latest&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url=API_URL)

    if response.status_code == 200:  # Check for successful response
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        else:
            return {
                "error": "Error fetching balances.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )
# tool for getting the normal transcatoion list.
@tool
def normal_transcation_list(address: str) -> Dict[str, Any]:
    """
    Fetch the Normal Transcation by balance for a  given address by user in single call using the Etherscan API.

    Parameters:
    - address (str): The Ethereum address to check the balance for.
    - api_key (str): Your Etherscan API key.

    Returns:
    - balance (float): The balance in Ether (ETH) or an error message if the request fails.
    """
    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url=API_URL)
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )
    
# this tool is also working...
@tool
def get_internal_transactions_by_address(address: str) -> Dict[str, Any]:
    """
    Fetch a list of internal transactions for a given Ethereum address using the Etherscan API.

    Parameters:
    - address (str): The Ethereum address for which to fetch internal transactions.

    Returns:
    - JSONResponse: A JSON response containing the list of internal transactions or an error message if the request fails.
    """
    # Set default values for the API call
    start_block = 0
    end_block = 99999999
    page = 1
    offset = 10
    sort = "asc"

    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort={sort}&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url=API_URL)

    if response.status_code == 200:  # Check if the request was successful
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        else:
            return {
                "error": "Error fetching transactions.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )

# This tool is also working.
@tool
def get_internal_transactions_by_hash(txhash: str) -> Dict[str, Any]:
    """
    Fetch a list of internal transactions for a given Ethereum transaction hash using the Etherscan API.

    Parameters:
    - txhash (str): The transaction hash (txhash) for which to fetch internal transactions.

    Returns:
    - JSONResponse: A JSON response containing the internal transactions or an error message if the request fails.
    """
    API_URL = f"https://api-sepolia.etherscan.io/api?module=account&action=txlistinternal&txhash={txhash}&apikey={ETHERSCAN_API_KEY}"

    response = requests.get(url=API_URL)

    if response.status_code == 200:  # Check if the request was successful
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return JSONResponse(content=result, status_code=status.HTTP_200_OK)
        else:
            return {
                "error": "Error fetching transactions.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )

"""
=======================================
Get "Internal Transactions" by Block Range
========================================
"""
# This tool is Working
@tool
def get_internal_transactions_by_block_range() -> Dict[str, Any]:
    """
    Fetch internal transactions for a specific block range using the Etherscan API.

    Parameters:
    - startblock (int, optional): The starting block number to fetch transactions from. Default is 0.
    - endblock (int, optional): The ending block number to fetch transactions up to. Default is 99999999.
    - page (int, optional): The page number to fetch. Default is 1.
    - offset (int, optional): The number of transactions per page. Default is 10.
    - sort (str, optional): The sorting order of the transactions ("asc" for ascending, "desc" for descending). Default is "asc".

    Returns:
    - dict: A dictionary containing the response from the Etherscan API, including internal transactions or an error message.
    
    Raises:
    - HTTPException: Raises an exception if the API call fails or if the response is not successful.
    """
    API_URL=f"https://api-sepolia.etherscan.io/api?module=account&action=txlistinternal&startblock=484887&endblock=765371&page=1&offset=10&sort=asc&apikey={ETHERSCAN_API_KEY}"
    

    response = requests.get(API_URL)

    if response.status_code == 200:  # Check for a successful response
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return result
        else:
            return {
                "error": "Error fetching internal transactions.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )
        
        
"""
===========================================================
Get a list of 'ERC20 - Token Transfer Events' by Address
===========================================================
"""

# Not working:
@tool
def get_erc20_token_transfer_events(
    contractaddress: str,
    address: str,
    startblock: int = 0,
    endblock: int = 99999999,
    page: int = 1,
    offset: int = 100,
    sort: str = "asc"
) -> Dict[str, Any]:
    """
    Fetch a list of ERC20 token transfer events for a contractaddress and Specific using the Etherscan API.

    Parameters:
    - contractaddress (str): The contract address of the ERC20 token.
    - address (str): The Ethereum address to check for token transfer events.
    - startblock (int, optional): The starting block number to fetch events from. Default is 0.
    - endblock (int, optional): The ending block number to fetch events up to. Default is 99999999.
    - page (int, optional): The page number to fetch. Default is 1.
    - offset (int, optional): The number of events per page. Default is 100.
    - sort (str, optional): The sorting order of the events ("asc" for ascending, "desc" for descending). Default is "asc".

    Returns:
    - dict: A dictionary containing the response from the Etherscan API, including ERC20 token transfer events or an error message.
    
    Raises:
    - HTTPException: Raises an exception if the API call fails or if the response is not successful.
    """
    API_URL = (
        f"https://api-sepolia.etherscan.io/api"
        f"?module=account&action=tokentx"
        f"&contractaddress={contractaddress}&address={address}"
        f"&startblock={startblock}&endblock={endblock}"
        f"&page={page}&offset={offset}&sort={sort}"
        f"&apikey={ETHERSCAN_API_KEY}"
    )

    response = requests.get(API_URL)

    if response.status_code == 200:  # Check for a successful response
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return result
        else:
            return {
                "error": "Error fetching token transfer events.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )
        

"""
===========================================================
Fetch a list of ERC721 token transfer events for a specified address 
===========================================================
"""



# not working
@tool
def get_erc721_token_transfer_events(
    contractaddress: str,
    address: str
):
    """
    Fetch a list of ERC721 token transfer events for a specified address using the Etherscan API.

    Parameters:
    - contractaddress (str): The contract address of the ERC721 token.
    - address (str): The Ethereum address to check for token transfer events.

    Returns:
    - dict: A dictionary containing the response from the Etherscan API, including ERC721 token transfer events or an error message.

    Raises:
    - HTTPException: Raises an exception if the API call fails or if the response is not successful.
    """

    # Construct the API URL in a single f-string
    API_URL = (
        f"https://api-sepolia.etherscan.io/api?module=account&action=tokennfttx"
        f"&contractaddress={contractaddress}&address={address}&startblock=0&endblock=99999999&page=1&offset=100&sort=asc&apikey={ETHERSCAN_API_KEY}"
    )

    response = requests.get(API_URL)

    if response.status_code == 200:  # Check for a successful response
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return result
        else:
            return {
                "error": "Error fetching token transfer events.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )

"""
===========================================================
Fetch a list of blocks mined by a specified address using the Etherscan API.
===========================================================
"""


# this tool is working:
@tool
def get_mined_blocks_by_address(
    address: str,
    blocktype: str = "blocks",
    page: int = 1,
    offset: int = 10
) -> Dict[str, Any]:
    """
    Fetch a list of blocks mined by a specified address using the Etherscan API.

    Parameters:
    - address (str): The Ethereum address for which to fetch the mined blocks.
    - blocktype (str, optional): The type of blocks to return ("blocks" or "long"). Default is "blocks".
    - page (int, optional): The page number to fetch. Default is 1.
    - offset (int, optional): The number of results per page. Default is 10.

    Returns:
    - dict: A dictionary containing the response from the Etherscan API, including mined blocks or an error message.

    Raises:
    - HTTPException: Raises an exception if the API call fails or if the response is not successful.
    """
    API_URL = (
        f"https://api-sepolia.etherscan.io/api"
        f"?module=account&action=getminedblocks"
        f"&address={address}&blocktype={blocktype}"
        f"&page={page}&offset={offset}&apikey={ETHERSCAN_API_KEY}"
    )

    response = requests.get(API_URL)

    if response.status_code == 200:  # Check for a successful response
        result = response.json()
        if result.get("status") == "1":  # API call was successful
            return result
        else:
            return {
                "error": "Error fetching mined blocks.",
                "message": result.get("message", "Unknown error")
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred while processing your request."
            }
        )


# bind tools with LLM
tools=[
    get_single_address_balance,
    get_multiple_address_balance,
    normal_transcation_list,
    get_internal_transactions_by_address,
    get_internal_transactions_by_hash,
    get_internal_transactions_by_block_range,
    get_erc20_token_transfer_events,
    get_mined_blocks_by_address,
    get_erc721_token_transfer_events
    
    
    
]
llm_with_tools=llm.bind_tools(tools)

    


