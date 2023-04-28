from abc import ABC, abstractmethod


# State Pattern
class ElevatorState(ABC):
    @abstractmethod
    def up(self):
        pass

    @abstractmethod
    def down(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class MovingUpState(ElevatorState):
    def up(self):
        print("The elevator is already moving up.")
        return self

    def down(self):
        print("The elevator cannot go down while moving up.")
        return self

    def stop(self):
        print("The elevator is stopping.")
        return StoppedState()


class MovingDownState(ElevatorState):
    def up(self):
        print("The elevator cannot go up while moving down.")
        return self

    def down(self):
        print("The elevator is already moving down.")
        return self

    def stop(self):
        print("The elevator is stopping.")
        return StoppedState()


class StoppedState(ElevatorState):
    def up(self):
        print("The elevator is moving up.")
        return MovingUpState()

    def down(self):
        print("The elevator is moving down.")
        return MovingDownState()

    def stop(self):
        print("The elevator is already stopped.")


class Elevator:
    def __init__(self):
        self.current_floor = 1
        self.state = StoppedState()

    def set_state(self, state):
        self.state = state

    def up(self):
        self.current_floor += 1
        self.state = self.state.up()
        print(f"The elevator is now at floor {self.current_floor}.")

    def down(self):
        self.current_floor -= 1
        self.state = self.state.down()
        print(f"The elevator is now at floor {self.current_floor}.")

    def stop(self):
        self.state = self.state.stop()
        print("The elevator has stopped.")


# Observer Pattern
class ElevatorObserver:
    def __init__(self, elevator):
        self.elevator = elevator

    def update(self, event):
        if event == "maintenance":
            print("Elevator is in maintenance mode.")
        elif event == "stuck":
            print("Elevator is stuck. Please call for assistance.")


class ElevatorSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def notify(self, event):
        for observer in self.observers:
            observer.update(event)


# Flyweight Pattern
class ElevatorMusic:
    def __init__(self, music):
        self.music = music


class ElevatorMusicFactory:
    def __init__(self):
        self.music_cache = {}

    def get_music(self, music):
        if music not in self.music_cache:
            self.music_cache[music] = ElevatorMusic(music)
        return self.music_cache[music]


if __name__ == '__main__':
    # Creating elevator object
    elevator = Elevator()

    # Creating elevator observers
    maintenance_observer = ElevatorObserver(elevator)
    stuck_observer = ElevatorObserver(elevator)

    # Creating elevator subject and attaching observers
    elevator_subject = ElevatorSubject()
    elevator_subject.attach(maintenance_observer)
    elevator_subject.attach(stuck_observer)

    # Setting elevator state to MovingUpState
    elevator.set_state(MovingUpState())

    # Moving elevator up
    elevator.up()

    # Moving elevator up again
    elevator.up()
