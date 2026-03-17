from abc import abstractmethod, ABC
import pickle

all_books = []
all_users = []

#Проверка что пользователь ввел хотя бы что-то
def check_for_input():
    while (True):
        text = input("Вводите: ")
        if len(text) != 0:
            return text
        else:
            print("Вы ничего не ввели")

#Выбор пользователя
def choice_user():
    while (True):
        print("Вводите имя пользователей без ошибок (если вы хотите выйти из меню выбора пользователя введите команду 'quit'")
        name = check_for_input()
        if name.lower() == "quit":
            return "quit_system"
        for i in all_users:
            if name == i._name:
                print(f"Пользователь {i._name} выбран")
                return i
            
        print("Пожалуйста. Вводите имя без ошибок и проверьте что такой пользователь сущевствует")

#Запись файлов для их возможного чтения (ПОЛЬЗОВАТЕЛИ)
def react_file_for_user(list_for_file):
    with open("users_for_user.txt", "w", encoding="UTF-8") as file:
        if len(list_for_file) == 0:
            file.write("------------------------------\n")
            file.write("ДАННЫЕ В СИСТЕМЕ НЕ ОБНАРУЖЕНЫ\n")
            file.write("------------------------------\n")
        else:
            file.write("---------------------------------\n")
            file.write("ДАННЫЕ ВСЕХ ПОЛЬЗОВАТЕЛЕЙ СИСТЕМЫ\n")
            file.write("---------------------------------\n")
            count = 0
            for i in list_for_file:
                count += 1
                file.write(f"{count} - {i._name}")
                if i.list_book != 0:
                    file.write("\n")
                    file.write("----------------------\n")
                    file.write("ВСЕ КНИГИ ПОЛЬЗОВАТЕЛЯ\n")
                    file.write("----------------------\n")
                    file.write("\n")
                    count_for_book = 0
                    for i in i.list_book:
                        count_for_book += 1
                        file.write(f"{count_for_book} - {i.name}, {i.author}\n")

                file.write("\n")

#Запись файлов для их возможного чтения (КНИГИ)
def react_file_for_book(list_for_file):
    with open("book_for_user.txt", "w", encoding="UTF-8") as file:
        if len(list_for_file) == 0:
            file.write("------------------------------\n")
            file.write("ДАННЫЕ В СИСТЕМЕ НЕ ОБНАРУЖЕНЫ\n")
            file.write("------------------------------\n")
        else:
            file.write("---------------\n")
            file.write("ДАННЫЕ ВСЕХ КНИГ В СИСТЕМЫ\n")
            file.write("---------------\n")
            count = 0
            for i in list_for_file:
                count += 1
                if i.enable == True:
                    enable_book = "Доступно"
                else:
                    enable_book = "Недоступно"
                file.write(f"{count} - {i.name}, {i.author} ({enable_book})\n")


#Запись файлов для дальнейшей загрузки их в систему (ПОБИТОВО)
def react_file(list_for_file, name_file):
    with open(name_file, 'wb') as file:
        pickle.dump(list_for_file, file)

#Чтение файлов для загрузки их в систему (ПОБИТОВО)
def read_files(name_file):
    try:
        with open(name_file, 'rb') as file:
            return pickle.load(file)
        
    except Exception:
        return []

#Класс книги с его характеристиками
class Book:
    def __init__(self, name, author, enable):
        self.name = name
        self.author = author
        self.enable = enable

class view_book_class(ABC):
    @abstractmethod
    def view_book():
        pass

class Person():
    def __init__(self, name):
        self._name = name

#Класс пользователя
class User(Person, view_book_class):
    def __init__(self, name):
        self._name = name
        self.list_book = []
    
    #ПРОСМОТР ВСЕХ ДОСТУПНЫХ КНИГ
    def view_book(self):
        print()
        print("-------------------")
        print("Все доступные книги")
        print("-------------------")
        print()
        count = 0
        for i in all_books:
            if i.enable == True:
                count += 1
                print(f"{count} - {i.name}, {i.author}")
            else:
                pass
        print()
    
    #ПОЛУЧЕНИЕ ДОСТУПНОЙ КНИГИ
    def __get_book(self, name, author):
        for i in all_books:
            if i.name == name and i.author == author and i.enable == True:
                self.list_book.append(i)
                i.enable = False
                print(f"Книга получена пользователем")
                print()
                return
            
            elif i.name == name and i.author == author and i.enable == False:
                print("Книга сейчас находится у другого пользователя")
        
        print("----------------")
        print("Книга не найдена")
        print("----------------")
        print()

    #СДАЧА КНИГИ ОБРАТНО
    def __give_book(self, name, author):
        for i in self.list_book:
            if i.name == name and i.author == author:
                self.list_book.remove(i)
                for j in all_books:
                    if j.name == name and j.author == author and j.enable == False:
                        j.enable = True
                        print("Книга успешно отдана, спасибо что вернули")
                        print()
                        return  
                          
        
        print("-------------------------------------------------------")
        print("Такой книги либо не существует, либо сейчас нет доступа")
        print("-------------------------------------------------------")
        print()

    #ПРОСМОТР ВСЕХ ВЗЯТЫХ КНИГ
    def __view_my_book(self):
        print("----------------------")
        print("Все взятые вами книги:")
        print("----------------------")
        print()
        count = 0
        if (len(self.list_book) != 0):
            for i in self.list_book:
                count += 1
                print(f"{count} - {i.name} - {i.author}")

        else:
            print('У вас нет книг')
            print()

#Класс библиотекаря
class Librian(Person):
    def __init__(self, name):
        self._name = name
    
    #ДОБАВЛЕНИЕ КНИГИ В СИСТЕМУ
    def _add_book(self, name, author):       
        for i in all_books:
            if i.name == name and i.author == author:
                print("Такая книга уже есть в системе")
                print()
                return
        if (len(name) != 0 and len(author) != 0):
            all_books.append(Book(name, author, True))
            print("Книга добавлена в систему")
            print()
        else:
            print("Параметры для добавления заполнены некорректно")
            print()

    #УДАЛЕНИЕ КНИГИ ИЗ СИСТЕМЫ
    def _del_books(self, name):
        count = 0
        for i in all_books:
            if i.name == name:
                print(f"Книга под названием {i.name} успешно удалена из системы и у всех пользователей")
                print()
                for j in all_users:
                    for o in j.list_book:
                        if o.name == name:
                            j.list_book.remove(o)

                all_books.remove(i)
                count += 1
        if (count == 0):
            print("К сожалению, книга не найдена. Попробуйте ещё раз")
            print()

    #ДОБАВЛЕНИЕ ПОЛЬЗОВАТЕЛЕЙ В СИСТЕМУ
    def _add_user(self, name):
        if (len(name) != 0):
            all_users.append(User(name))
            print(f"Пользователь {name} успешно добавлен")
            print()
        else:
            print("Параметры для добавления заполнены некорректно")
            print()

    #ПРОСМОТР ВСЕХ ПОЛЬЗОВАТЕЛЕЙ В СИСТЕМЕ
    def _check_all_users(self):
        print()
        print("---------------------------------")
        print("СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ СИСТЕМЫ")
        print("---------------------------------")
        print()

        if len(all_users) != 0:
            for i in all_users:
                print(f"Имя - {i._name}, список всех книг {i._name}:")
                if len(i.list_book) != 0:
                    for i in i.list_book:
                        print(f"{i.name} {i.author} ")
                else:
                    print("Книг нет(")
                    print()

        else:
            print("Пользователей нет")
            print()

    #ПРОСМОТР ВСЕХ КНИГ КОТОРЫЕ ЕСТЬ В СИСТЕМЕ
    def view_book(self):
        print("------------------------------------------")
        print("Абсолютно все книги которые есть в системе")
        print("------------------------------------------")
        if (len(all_books) != 0):
            for i in all_books:
                if (i.enable == True) :
                    a = "Доступно"
                else:
                    a = "Недоступно"
                print(f"Название - {i.name}, автор - {i.author} -- {a}")
        else:
            print("Список пуст")
    
OK = True

#СОЗДАНИЕ НАЗВАНИЯ ДЛЯ ФАЙЛОВ, ГДЕ БУДУТ ХРАНИТЬСЯ ОБЪЕКТЫ
name_for_file_book = "books_sys.txt"
name_for_file_user = "users_sys.txt"

#Подкачка всех данных из файлов
all_books = read_files(name_for_file_book)
all_users = read_files(name_for_file_user)
print("----------------------------------------")
print("Добро пожаловать в приложение библеотеки")
print("----------------------------------------")
print()
while(OK):
    print("----------------------------------------")
    print("Список доступных команд (введите цифру):\n1. Войти как библеотекарь\n2. Войти как пользователь\n3. Выйти из приложения")
    print("----------------------------------------")
    print()
    choose = input("Введите цифру от 1-3: ")
    
    match (choose):
        case "1":
            librian1 = Librian("admin1")
            print()
            print("-----------------------------------")
            print("Вы вошли в систему как библиотекарь")
            print("-----------------------------------")
            print()
            while True:
                print()
                print("-----------------------")
                print("СПИСОК ДОСТУПНЫХ КОМАНД")
                print("-----------------------")
                print()
                print("Вызываются с помощью цифр\n-----------------\n1 - Добавление книги в систему\n2 - Удаление книги из системы")
                print("3 - Добавление пользователей в систему\n4 - Просмотр всех пользователей системы\n5 - Просмотр всех книг находящихся в системе\n0000 - выход в главное меню")
                choice_librian = input("Введите цифру: ")
                match choice_librian:
                    case "1":
                        print()
                        print("Введите название книги")
                        name = check_for_input()
                        print("Введите автора книги")
                        author = check_for_input()
                        librian1._add_book(name, author)
                    case "2":
                        print()
                        print("Введите название книги")
                        name = check_for_input()
                        librian1._del_books(name)
                    case "3":
                        print()
                        print("Введите имя пользователя")
                        login = check_for_input()
                        librian1._add_user(login)
                    case "4":
                        print()
                        librian1._check_all_users()
                    case "5":
                        print()
                        librian1.view_book()
                    case "0000":
                        print("Переход в главное меню")
                        break
                    case _:
                        print()
                        print("Команда не найдена. Пожалуйста, соблюдайте правила")
                        print()
            
        case "2":
            if (len(all_users) != 0):
                print()
                print("---------------------------------------------")
                print("СНАЧАЛА НЕОБХОДИМО ВОЙТИ ПОД КАКИМ-ТО ЛОГИНОМ")
                print("---------------------------------------------")
                print()
                print("За какого пользователя вы хотите зайти?")
                print()
                print("-------------------------")
                print("Список всех пользователей")
                print("-------------------------")
                count = 0
                for i in all_users:
                    count += 1
                    print(f"{count} - {i._name}")
                print()
                print("Напишите имя пользователя, за которого хотите зайти")
                print()
                user = choice_user()

                if user != "quit_system":
                    print()
                    print("----------------------------------------------------------------------")
                    print(f"{user._name}, добро пожаловать в библиотеку. Вы зашли как пользователь")
                    print("----------------------------------------------------------------------")
                    print()

                    while True:
                        print()
                        print("-----------------------")
                        print("СПИСОК ДОСТУПНЫХ КОМАНД")
                        print("-----------------------")
                        print()
                        print("Вызываются с помощью цифр\n-----------------\n1 - Просмотр всех доступных книг\n2 - Получить доступную книгу")
                        print("3 - Отдать взятую книгу\n4 - Просмотр всех взятых вами книг\n0000 - Выход в главное меню")
                        choice_user_1 = check_for_input()
                        match choice_user_1:
                            case "1":
                                print()
                                user.view_book()

                            case "2":
                                print()
                                print("Введите название книги")
                                name = check_for_input()
                                print("Введите автора книги")
                                author = check_for_input()
                                print()
                                user._User__get_book(name, author)

                            case "3":
                                print()
                                print("Введите название книги")
                                name = check_for_input()
                                print("Введите автора книги")
                                author = check_for_input()
                                print()
                                user._User__give_book(name, author)

                            case "4":
                                user._User__view_my_book()
                                print()
                            
                            case "0000":
                                print()
                                print("Выход в главное меню")
                                break

                            case _:
                                print("Пожалуйста. Вводите доступные команды")

            else:
                print()
                print("Не найдено ни одного пользователя в системе, пожалуйста обратитесь к библиотекарю, чтобы он вас добавил в систему")
                print()
                print("Переход в главное меню")

        case "3":
            print()
            print("-----------------------------------")
            print("Выход из приложения, всего хорошего")
            print("-----------------------------------")
            react_file_for_user(all_users)
            react_file_for_book(all_books)
            react_file(all_books, name_for_file_book)
            react_file(all_users, name_for_file_user)    
            OK = False
        case _:
            print()
            print("Команда не распознана")
            print()