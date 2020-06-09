import re
from src import modules


def main(url, path):
    print(url)

    urllist = []
    namelist = []
    i = 0
    link_pattern = re.compile(r'mangareader.net/(.*?)/(\d+)')
    result = link_pattern.search(url)
    mangaName = result.group(1)
    mangaChapter = result.group(2)

    # print('Getting pages list...')
    while True:

        i += 1
        url_now = 'http://www.mangareader.net/' + mangaName + '/' + mangaChapter + '/' + str(i)
        content = modules.get_page(url_now)  # byte literal est obtenu (python2 fait pas de diff avec string, python trois le fait
        content = content.decode("utf-8").replace("\n", '')

        content_pattern = re.compile(r"document\['pu'\]\s=\s'(.*?)';")
        result = re.findall(content_pattern, content)

        if len(result) == 0:
            break

        k = len(result[0]) - 1
        if k == -1:
            break

        urllist.append(result[0])

        while result[0][k] != '/':
            k -= 1

        S = ""
        for p in range(k+1, len(result[0])):
            S += result[0][p]

        namelist.append(S)
    page_counter = 1
    for i in range(0, len(urllist)):
        dl = modules.download(urllist[i], path+str(page_counter)+'.'+namelist[i].split('.')[-1])
        if dl != 'None':
            page_counter += 1
    if page_counter > 1:
        modules.convert_to_pdf(path)


if __name__ == '__main__':
    main()
