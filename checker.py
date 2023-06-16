import re
import requests
import vk_api


def main():
    # Логин и пароль от аккаунта
    login = "login"
    password = "password"

    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    while True:
        # Введите ссылку группы
        group_url = input("Введите ссылку на группу или короткое имя: ")

        # Получаем ID группы
        group_id = get_group_id(vk, group_url)
        print(f'ID Группы: {group_id}')

        # Проверяем комментарии
        comments_open = are_comments_open(vk, group_id)
        print(f'Комменты открыты: {comments_open}')
        print("--------------------------------------------------")


def get_group_id(vk, group_url):
    group_screen_name = extract_group_screen_name(group_url)
    group_info = vk.utils.resolveScreenName(screen_name=group_screen_name)
    return -group_info['object_id']


def extract_group_screen_name(group_url):
    match = re.search(r'(?:https?://vk\.com/)?(.+)', group_url)
    return match.group(1)


def are_comments_open(vk, group_id):
    response = vk.wall.get(owner_id=group_id, count=1)
    if response['items']:
        post = response['items'][0]
        return post.get('comments', {}).get('can_post', False)
    return False


if __name__ == '__main__':
    main()