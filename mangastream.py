import re
import requests
from modules import download, get_page


def main( url  ):

    urllist = []
    namelist = []
    i = 0

    while url[-1] != '/':
        url = url[:-1]

    print ('Getting pages list...')

    while True:
        i += 1
        url_now = url + str(i)
        content = get_page(url_now)
        content = content.replace("\n", '')

        content_pattern = re.compile(r'<img id="manga-page"(\s+)src="(.*?)\"/>')
        result = re.findall(content_pattern, content)
        if len(result) == 0:
            break

        urllist.append(result[0][1])

        k = len(result[0][1]) - 1

        while result[0][1][k] != '/':
            k -= 1

        S = ""

        for p in xrange(k+1, len(result[0][1])):
            S += result[0][1][p]

        namelist.append(S)

    for i in xrange(0, len(urllist)):
        download(urllist[i], namelist[i])


if __name__ == '__main__':
	main()
