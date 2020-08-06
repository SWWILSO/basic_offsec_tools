import requests

def download(url):
    get_response = requests.get(url)
    filename = url.split("/")[-1]
    with open(filename, "wb") as output:
        output.write(get_response.content)

download("https://people.eng.unimelb.edu.au/ammoffat/ppsaa/c/helloworld.c")