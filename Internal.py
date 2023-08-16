import requests
import base64
import time
import pandas as pd
import yfinance

onedrive_link = "https://1drv.ms/x/s!An5vj5U_jKaNcAf8iwLEeRyBe4g?e=vDcDGe"
CoinDatabase = {}

def UpdateCoinDatabase(CoinCodes, NotifyPrices, FallOffPrices):
    for CoinIndex, CoinName in enumerate(CoinCodes):
        if CoinName in CoinDatabase:
            CoinDatabase[CoinName]["NotifyPrice"] = NotifyPrices[CoinIndex]
            CoinDatabase[CoinName]["FallOffPrice"] = FallOffPrices[CoinIndex]
        else:
            CoinDatabase[CoinName] = {}
            CoinDatabase[CoinName]["NotifyPrice"] = NotifyPrices[CoinIndex]
            CoinDatabase[CoinName]["FallOffPrice"] = FallOffPrices[CoinIndex]

def create_onedrive_direct_download(onedrive_link):
    data_bytes64 = base64.b64encode(bytes(onedrive_link, 'utf-8'))
    data_bytes64_string = data_bytes64.decode('utf-8').replace('/','_').replace('+','-').rstrip("=")
    result_url = f"https://api.onedrive.com/v1.0/shares/u!{data_bytes64_string}/root/content"
    return result_url

def GetResults():
    results = []
    for CoinName, CoinData in enumerate(CoinDatabase):
        ticker_name = CoinData + '-USD'
        data = yfinance.download(tickers=ticker_name, period='1d', interval='1m')
        dataframe = pd.DataFrame(data)
        prices = dataframe.get("Open")
        results.append(prices[len(prices)-1])

    return results

def SendNotification(NotifType, Coin):
    if NotifType:
        Notification = Coin + " Is UPPPP!!!!!"
        requests.post("https://ntfy.sh/HarshuCriptoe", data=Notification, headers={"Title": "Crupdate"})
    else:
        Notification = Coin + " Is No Longer Up"
        requests.post("https://ntfy.sh/HarshuCriptoe", data=Notification, headers={"Title": "Crupdate"})

def CheckAndNotify(CoinResults):
    for CoinIndex, CoinValue in enumerate(CoinDatabase):
        if 'AlreadyNotified' in CoinDatabase[CoinValue]:
            if CoinDatabase[CoinValue]['AlreadyNotified'] == True:
                if CoinResults[CoinIndex] <= CoinDatabase[CoinValue]['FallOffPrice']:
                    CoinDatabase[CoinValue]['AlreadyNotified'] = False
                    SendNotification(False, CoinValue)
            else:
                if CoinResults[CoinIndex] >= CoinDatabase[CoinValue]['NotifyPrice']:
                    SendNotification(True, CoinValue)
                    CoinDatabase[CoinValue]['AlreadyNotified'] = True
        else:
            CoinDatabase[CoinValue]['AlreadyNotified'] = False
            if CoinResults[CoinIndex] >= CoinDatabase[CoinValue]['NotifyPrice']:
                SendNotification(True, CoinValue)
                CoinDatabase[CoinValue]['AlreadyNotified'] = True

while(True):
    onedrive_direct_link = create_onedrive_direct_download(onedrive_link)
    Excel_Data = pd.read_excel(onedrive_direct_link)
    CoinCodes = Excel_Data.get("Coin Code")
    NotifyPrices = Excel_Data.get("Notify Price")
    FallOffPrices = Excel_Data.get("Fall Off Price")
    UpdateCoinDatabase(CoinCodes, NotifyPrices, FallOffPrices)

    CoinResults = GetResults()
    CheckAndNotify(CoinResults)
    time.sleep(300)