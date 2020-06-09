import re
import requests
from modules import download, get_page


def main( url ):

    urllist = []
    namelist = []
    i = 0

    if url[-6:-1] == 'page_':
        url =  url[:-7]

    if url[-1] != '/':
        url += '/'

    print ('Getting pages list...')

    while True:
        i += 1
        url_now = url + 'page_' + str(i)
        content = get_page(url_now)
        content = content.replace("\n", '')
        content = content.replace("\t", '')
        content = content.replace(' ', '')

        content_pattern = re.compile(r"onclick=\"changeafterzoom\(\)\"src=\"(.*?)\"/>")
        result = re.findall(content_pattern, content)

        if len(result) == 0 or result[0][-3:] == "///":
            break

        k = len(result[0]) - 1

        if k <= 0:
            break

        while result[0][k] != '/':
            k -= 1

        S = ""

        urllist.append(result[0])

        for p in xrange(k+1, len(result[0])):
            S += result[0][p]

        namelist.append(S)

    for i in xrange(0, len(urllist)):
        download(urllist[i], namelist[i])


if __name__ == '__main__':
	main()