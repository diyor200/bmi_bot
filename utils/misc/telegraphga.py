import telegraph
from data.config import ACCESS_TOKEN


def add_to_telegraph(info):
    telegraph_api = telegraph.Telegraph(ACCESS_TOKEN)
    content = [
        {
            'tag': 'h1',
            'children': ['Chetlatilganlarning sababi:']
        }
    ]
    print(info)
    for i in info:
        print(i)
        l = []
        l += [str(i[0])] + [str(i[1])] + [str(i[2])] + [str(i[3])] + [str(i[4])]
        print(l)
        content.append({'tag': 'p',
                        'children': l})
    page = telegraph_api.create_page('Test Page', content=content)
    page_url = 'https://telegra.ph/{}'.format(page['path'])

    return page_url

