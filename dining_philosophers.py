import random
import threading
import time

# The following code uses a monitor to manage fork access.
# Alternatively, it could be implemented with semaphores.

PHILOSOPHER_COUNT = 5

names = [
    "Aristotle",
    "Plato",
    "Socrates",
    "Descartes",
    "Confucius",
]


class Philosopher(threading.Thread):

    def __init__(self, name: str, left_fork: "Fork", right_fork: "Fork"):
        super().__init__()
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            self.think()
            self.pick_up_forks()
            self.eat()
            self.return_forks()

    def eat(self):
        eating_time = random.randint(8, 10)
        print(f"{self.name} is eating for {eating_time} seconds")
        time.sleep(eating_time)
        print(f"{self.name} finished eating")

    def think(self):
        think_time = random.randint(1, 3)
        print(f"{self.name} is thinking for {think_time} seconds")
        time.sleep(think_time)
        print(f"{self.name} is back from thinking")

    def pick_up_forks(self):
        self.left_fork.pick_up(self)
        self.right_fork.pick_up(self)

    def return_forks(self):
        self.left_fork.put_down()
        self.right_fork.put_down()


class Fork:

    def __init__(self, owner: "Philosopher | None" = None):
        self.owner = owner
        self.lock = threading.Lock()
        self.available = threading.Condition(self.lock)

    def pick_up(self, philosopher: Philosopher):
        with self.lock:
            while self.owner is not None:
                print(
                    f"{philosopher.name} is hungry and waiting for {self.owner.name} to stop eating"
                )
                self.available.wait()
            self.owner = philosopher
            print(f"{self.owner.name} picked up a fork")

    def put_down(self):
        with self.lock:
            print(f"{self.owner.name} returned a fork")
            self.owner = None
            self.available.notify()


def main():
    forks = [Fork() for _ in range(PHILOSOPHER_COUNT)]
    philosophers = []
    for i in range(PHILOSOPHER_COUNT):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % PHILOSOPHER_COUNT]
        philosopher = Philosopher(names[i], left_fork, right_fork)
        philosophers.append(philosopher)

    for philosopher in philosophers:
        philosopher.start()

    for philosopher in philosophers:
        philosopher.join()


if __name__ == "__main__":
    main()
