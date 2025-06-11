from repositories import UserRepository
from data import User
from services import AuthService


def main() -> None:
    # Инициализация
    user_repository = UserRepository("users.json", User)
    auth_service = AuthService(user_repository, "session.json")

    print("1. Проверка автоматической авторизации:")
    if auth_service.is_authorized:
        print(f"Автоматически авторизован: {auth_service.current_user.name}")
    else:
        print("Нет активной сессии")
    print()
    
    users_data = [
        {'id': 1, 'name': "Александр", 'login': 'alex', 'password': 'alex123', 'email': 'alex@mail.ru'},
        {'id': 2, 'name': "Мария", 'login': 'maria', 'password': 'maria123', 'email': 'maria@mail.ru'},
        {'id': 3, 'name': "Дмитрий", 'login': 'dmitry', 'password': 'dmitry123'}
    ]
    
    print("2. Добавление пользователей:")
    for user_data in users_data:
        user = User(**user_data)
        user_repository.add(user)
        print(f"Добавлен: {user.name} (login: {user.login})")
    print()
    
    print("3. Список всех пользователей (отсортирован по name):")
    all_users = user_repository.get_all()
    for user in all_users:
        print(f"{user.name} (ID: {user.id}, login: {user.login}, email: {user.email})")
    print()
    
    print("4. Редактирование пользователя:")
    user_to_edit = user_repository.get_by_id(1)
    if user_to_edit:
        print(f"До: {user_to_edit.name}, email: {user_to_edit.email}")
        user_to_edit.name = "Алексей"
        user_to_edit.email = "alexey@newmail.ru"
        user_to_edit.address = "Калининград, ул. Невского 14"
        user_repository.update(user_to_edit)
        print(f"После: {user_to_edit.name}, email: {user_to_edit.email}, address: {user_to_edit.address}")
    print()
    
    print("5. Авторизация пользователя:")
    alex_data = next((user for user in users_data if user['login'] == 'alex'), None)
    login_user = user_repository.get_by_login('alex')
    if login_user:
        if login_user.password == alex_data['password']:
            auth_service.sign_in(login_user)
            print(f"Успешная авторизация: {auth_service.current_user.name}")
            print(f"Статус авторизации: {auth_service.is_authorized}")
        else:
            print("Неверный пароль!")
    print()
    
    print("6. Смена текущего пользователя:")
    print(f"Текущий пользователь: {auth_service.current_user.name}")
    
    maria_data = next((user for user in users_data if user['login'] == 'maria'), None)
    maria = user_repository.get_by_login('maria')
    if maria and maria.password == maria_data['password']:
        auth_service.sign_in(maria)
        print(f"Сменили на: {auth_service.current_user.name}")
    print()
    
    # Вернемся к первому пользователю
    if login_user:
        auth_service.sign_in(login_user)
        print(f"Вернулись к: {auth_service.current_user.name}")
    print()
    
    print("7. Выход из системы:")
    print(f"До выхода: авторизован = {auth_service.is_authorized}")
    auth_service.sign_out()
    print(f"После выхода: авторизован = {auth_service.is_authorized}")
    print()
    
    print("8. Повторный вход в систему для демонстрации автоматической авторизации:")
    print("Авторизуемся и выходим...")
    if login_user:
        auth_service.sign_in(login_user)
        print(f"Авторизован: {auth_service.current_user.name}")
    
    print("Имитация перезапуска программы...")
    new_auth_service = AuthService(user_repository, "session.json")
    
    if new_auth_service.is_authorized:
        print(f"Автоматическая авторизация работает! Пользователь: {new_auth_service.current_user.name}")
    else:
        print("Автоматическая авторизация не сработала")
    
    # Очистка
    new_auth_service.sign_out()

if __name__ == "__main__":
    main()