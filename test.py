import pymorphy2

from random import randint as ri

morph = pymorphy2.MorphAnalyzer()

butyavka1 = morph.parse('александрийского')[0]
butyavka2 = morph.parse('театра')[0]

# print(butyavka1.word, '->', butyavka1.normal_form)
# print(butyavka2.word, '->', butyavka2.normal_form)

str = "дай маршрут для новичка по вело-дорожке в александровском парке".split(' ')


one_route = {'id': 1, 'type': 'wheel', 'distance': 3.9, 'tags_place': ['александровский', 'парк'], 'tags_route': ['вода', 'дорожка'], 'url': ''}
routes = [one_route]
result_routes = []
tmp_routes = []


prepositions = ['по', 'для', 'в', 'через']


for i, word in enumerate(str):
    butyavka1 = morph.parse(word)[0]
    for route in routes:
        # print(butyavka1.normal_form, route['tags_place'])
        if butyavka1.normal_form in prepositions:
            str.remove(word)

for i, word in enumerate(str):
    butyavka1 = morph.parse(word)[1]
    for route in routes:
        print(butyavka1.normal_form)
        if butyavka1.normal_form in route['tags_place']:
            result_routes.append(route)
            str.remove(word)

print(str)
print(result_routes)

# for word in str:
#     for route in routes:
#         if butyavka1.normal_form in route['tags_place']:
#             result_routes.append(route)
        
#     if result_routes:
#         routes = result_routes


# print(len(result_routes))