class apple:
    def __init__(self, num) -> None:
        super().__init__()
        self.num = num

    def add(self, num):
        self.num += num

    def __str__(self) -> str:
        return str(self.num)

    def test(self, x):
        print(x(self.num))


class Animal:
    def __init__(self):
        print("Animal created")

    def whoAmI(self):
        print("Animal")


class Dog(Animal):
    def __init__(self):
        super().__init__()
        print("Dog created")

    def whoAmI(self):
        print("Dog")


def main():
    a_dog = Dog()
    a_dog.whoAmI()


if __name__ == '__main__':
    main()
