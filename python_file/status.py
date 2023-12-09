import requests
def checkserver(url):
    try:
        response = requests.get(url)
        return "1" if response.status_code == 200 else "0"

    except requests.exceptions.RequestException:
        return "0"