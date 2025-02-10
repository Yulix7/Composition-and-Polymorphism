import json


# 1. Базовый класс Animal
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        raise NotImplementedError("Подклассы должны реализовать этот метод")

    def eat(self):
        print(f"{self.name} ест.")

    def __str__(self):
        return f"{self.__class__.__name__}(Имя: {self.name}, Возраст: {self.age})"


# 2. Подклассы Bird, Mammal, Reptile
class Bird(Animal):
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        print(f"{self.name} говорит: Чирик-чирик!")


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        print(f"{self.name} говорит: Рррр!")


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        print(f"{self.name} говорит: Шшшш!")


# 3. Полиморфизм: функция animal_sound
def animal_sound(animals):
    for animal in animals:
        animal.make_sound()


# 4. Класс Zoo с композицией
class Zoo:
    def __init__(self):
        self.animals = []
        self.staff = []

    def add_animal(self, animal):
        if isinstance(animal, Animal):
            self.animals.append(animal)
            print(f"Добавлено {animal.name} в зоопарк.")
        else:
            print("Некорректный объект животного.")

    def add_staff(self, staff_member):
        if isinstance(staff_member, (ZooKeeper, Veterinarian)):
            self.staff.append(staff_member)
            print(f"Добавлен {staff_member.name} в штат зоопарка.")
        else:
            print("Некорректный объект сотрудника.")

    def save_to_file(self, filename):
        data = {
            "animals": [{"type": animal.__class__.__name__, "name": animal.name, "age": animal.age} for animal in
                        self.animals],
            "staff": [{"type": staff.__class__.__name__, "name": staff.name} for staff in self.staff]
        }
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Данные зоопарка сохранены в {filename}.")

    def load_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)

        for animal_data in data["animals"]:
            if animal_data["type"] == "Bird":
                animal = Bird(animal_data["name"], animal_data["age"], wingspan=0)  # Пример
            elif animal_data["type"] == "Mammal":
                animal = Mammal(animal_data["name"], animal_data["age"], fur_color="неизвестно")
            elif animal_data["type"] == "Reptile":
                animal = Reptile(animal_data["name"], animal_data["age"], scale_type="неизвестно")
            self.add_animal(animal)

        for staff_data in data["staff"]:
            if staff_data["type"] == "ZooKeeper":
                staff = ZooKeeper(staff_data["name"])
            elif staff_data["type"] == "Veterinarian":
                staff = Veterinarian(staff_data["name"])
            self.add_staff(staff)

        print(f"Данные зоопарка загружены из {filename}.")


# 5. Классы для сотрудников
class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        print(f"{self.name} кормит {animal.name}.")


class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        print(f"{self.name} лечит {animal.name}.")


# Пример использования
if __name__ == "__main__":
    # Создаем зоопарк
    zoo = Zoo()

    # Создаем животных
    parrot = Bird("Попугай Полли", 2, wingspan=0.5)
    lion = Mammal("Лев Симба", 5, fur_color="золотистый")
    snake = Reptile("Змея Каа", 3, scale_type="гладкая")

    # Добавляем животных в зоопарк
    zoo.add_animal(parrot)
    zoo.add_animal(lion)
    zoo.add_animal(snake)

    # Создаем сотрудников
    keeper = ZooKeeper("Иван")
    vet = Veterinarian("Доктор Смирнов")

    # Добавляем сотрудников в зоопарк
    zoo.add_staff(keeper)
    zoo.add_staff(vet)

    # Демонстрация полиморфизма
    animal_sound(zoo.animals)

    # Сотрудники выполняют свои обязанности
    keeper.feed_animal(lion)
    vet.heal_animal(snake)

    # Сохраняем данные зоопарка в файл
    zoo.save_to_file("zoo_data.json")

    # Загружаем данные зоопарка из файла
    new_zoo = Zoo()
    new_zoo.load_from_file("zoo_data.json")