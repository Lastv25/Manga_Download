
def fusion(gauche, droite):
    resultat = []
    index_gauche, index_droite = 0, 0
    while index_gauche < len(gauche) and index_droite < len(droite):
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


def tri_fusion(m):
    if len(m) <= 1:
        return m
    milieu = len(m) // 2
    gauche = m[:milieu]
    droite = m[milieu:]
    gauche = tri_fusion(gauche)
    droite = tri_fusion(droite)
    return list(fusion(gauche, droite))


list_int = [1, 3, 2, 4, 5, 6, 4, 19, 132, 0, 12, 56]

list_page = ['1.jpg', '10.jpg', '11.jpg', '2.jpg', '3.jpg']
print(tri_fusion(list_page))
