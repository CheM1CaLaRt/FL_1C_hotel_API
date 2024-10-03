import requests

def check_url_accessibility(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return f"URL {url} доступен."
        else:
            return f"URL {url} вернул код состояния {response.status_code}."
    except requests.exceptions.ConnectionError:
        return f"URL {url} недоступен."
    except requests.exceptions.Timeout:
        return f"Проверка URL {url} завершилась по тайм-ауту."
    except requests.exceptions.RequestException as e:
        return f"Произошла ошибка при проверке URL {url}: {e}"

url = "http://192.168.0.50:8181/hotel-test/"
result = check_url_accessibility(url)
print(result)
