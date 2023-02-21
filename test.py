import random
import threading


class Fish:
    def __init__(self, sex):
        self.sex = sex
        self.age = 0
        self.lifetime = random.randint(1, 5)
        self.is_alive = True

    def swim(self):
        self.age += 1
        if self.age >= self.lifetime:
            self.is_alive = False
            print(f"{self} has died.")
        else:
            print(f"{self} is swimming.")

    def __repr__(self):
        return f"Fish({self.sex}, {self.age}, {self.lifetime})"


class Aquarium:
    def __init__(self):
        self.male_fish = [Fish('male') for _ in range(random.randint(1, 3))]
        self.female_fish = [Fish('female') for _ in range(random.randint(1, 3))]
        self.fish = self.male_fish + self.female_fish
        self.babies = []
        self.is_running = True

    def run(self):
        while self.is_running:
            for f in self.fish:
                f.swim()
                if f.is_alive and f.sex == 'female':
                    if random.random() < 0.2:  # 20% chance of laying eggs
                        self.babies.append(Fish(random.choice(['male', 'female'])))

            if self.babies:
                self.fish += self.babies
                print(f"{len(self.babies)} new fish were born!")
                self.babies = []

            self.fish = [f for f in self.fish if f.is_alive]
            if not self.fish:
                print("All fish have died.")
                self.is_running = False

            threading.Event().wait(random.uniform(0.5, 2.0))


aquarium = Aquarium()
aquarium.run()
