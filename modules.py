import requests
import os
import img2pdf
import re


def download(img_url, filename):
    count = 0
    for i in range(50):
        try:
            downloaded_image = open(filename, "wb")
            image_on_web = requests.get(img_url)
            downloaded_image.write(image_on_web.content)
            downloaded_image.close()
        except:
            print('download Error')
            count += 1
    if count == 9:
        return 'None'
    else:
        return 'Done'

def get_page(url):
    r = requests.get(url)
    content = r.text.encode('utf-8', 'ignore')
    return content


def get_chapter_number(manga_name, site_url):
    r = get_page(site_url+manga_name).decode("utf-8")
    chap_str_and_more = r[r.find('chapterlist'):]  # get string after the chapterlist node
    chap_str = chap_str_and_more[:chap_str_and_more.find('/table')]  # get string before the end of the table defining
    # the chapters
    chap_list_and_more = chap_str.split("\n")  # creating a list from the string

    chap_list = []
    for i in chap_list_and_more:  # get only the lines where chapters are named
        if manga_name in i:
            chap_list.append(i)

    return len(chap_list)


def get_chapter_list(manga_name, site_url):
    r = get_page(site_url+manga_name).decode("utf-8")
    chap_str_and_more = r[r.find('chapterlist'):]  # get string after the chapterlist node
    chap_str = chap_str_and_more[:chap_str_and_more.find('/table')]  # get string before the end of the table defining
    # the chapters
    chap_list_and_more = chap_str.split("\n")  # creating a list from the string

    chap_list = []
    for i in chap_list_and_more:  # get only the lines where chapters are named
        if manga_name in i:
            chap_list.append(i.split('</a>')[0].split('>')[1]+ i.split('</a>')[1].split('<')[0])
    return chap_list


def fusion_pdf(gauche, droite):
    resultat = []
    index_gauche, index_droite = 0, 0
    while index_gauche < len(gauche) and index_droite < len(droite):
        # print(gauche[index_gauche].split('.')[0], droite[index_droite].split('.')[0])
        if int(gauche[index_gauche].split('.')[0]) <= int(droite[index_droite].split('.')[0]):
            resultat.append(gauche[index_gauche])
            index_gauche += 1
        else:
            resultat.append(droite[index_droite])
            index_droite += 1
    if gauche:
        resultat.extend(gauche[index_gauche:])
    if droite:
        resultat.extend(droite[index_droite:])
    return resultat


def fusion_chap(gauche, droite):
    resultat = []
    index_gauche, index_droite = 0, 0
    while index_gauche < len(gauche) and index_droite < len(droite):
        left = re.findall('\d+', gauche[index_gauche])[0]
        right = re.findall('\d+', droite[index_droite])[0]
        if int(left) <= int(right):
            resultat.append(gauche[index_gauche])
            index_gauche += 1
        else:
            resultat.append(droite[index_droite])
            index_droite += 1
    if gauche:
        resultat.extend(gauche[index_gauche:])
    if droite:
        resultat.extend(droite[index_droite:])
    return resultat


def tri_fusion(m, pdf_bool):
    if len(m) <= 1:
        return m
    milieu = len(m) // 2
    gauche = m[:milieu]
    droite = m[milieu:]
    gauche = tri_fusion(gauche, pdf_bool)
    droite = tri_fusion(droite, pdf_bool)
    if pdf_bool:
        return list(fusion_pdf(gauche, droite))
    else:
        return list(fusion_chap(gauche, droite))


def convert_to_pdf(file_path):
    print('convert')
    chap_name = file_path.split("\\")[-2]
    list_images = tri_fusion(os.listdir(file_path), True)
    with open(file_path+chap_name+'.pdf', 'wb+') as file:
        file.write(img2pdf.convert([file_path+i for i in list_images if i.endswith(".jpg")]))
    file.close()

