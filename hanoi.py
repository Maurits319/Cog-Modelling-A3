import ccm
log = ccm.log()

# Buffer class to hold the goal
class Buffer:
    def __init__(self):
        self.content = None

    def set(self, value):
        self.content = value

    def get(self):
        return self.content

# Disk in the Tower of Hanoi
class Disk(ccm.Model):
    size = None  # Disk size

    def __init__(self, size):
        ccm.Model.__init__(self)
        self.size = size

# Peg in the Tower of Hanoi
class Peg(ccm.Model):
    def __init__(self, name):
        ccm.Model.__init__(self)
        self.name = name
        self.disks = []

    def add_disk(self, disk):
        if self.disks and disk.size > self.disks[-1].size:
            raise ValueError("Cannot place a larger disk on a smaller one!")
        self.disks.append(disk)

    def remove_disk(self):
        if not self.disks:
            raise ValueError("Peg {} is empty!".format(self.name))
        return self.disks.pop()

    def __repr__(self):
        return "Peg {name} has disks {disks}".format(
            name=self.name, disks=[disk.size for disk in self.disks]
        )

# Environment for Tower of Hanoi
class TowerOfHanoi(ccm.Model):
    def __init__(self, num_disks=3):
        ccm.Model.__init__(self)
        self.pegs = {
            'A': Peg('A'),
            'B': Peg('B'),
            'C': Peg('C')
        }
        self.num_disks = num_disks

        # Initialize all disks on peg A
        for size in range(num_disks, 0, -1):
            self.pegs['A'].add_disk(Disk(size))

        # Create a goal buffer
        self.goal = Buffer()
        self.goal.set('play hanoi')

    def move_disk(self, from_peg, to_peg):
        # Moves a disk and prints the move along with the state
        disk = self.pegs[from_peg].remove_disk()
        self.pegs[to_peg].add_disk(disk)

        print("Disk {} was moved to peg {}.".format(disk.size, to_peg))

        self.print_state()

        if self.is_goal_state():
            self.goal.set('hanoi solved')

    def print_state(self):
        print("Peg A has disks [{}]".format(", ".join(str(disk.size) for disk in self.pegs['A'].disks)))
        print("Peg B has disks [{}]".format(", ".join(str(disk.size) for disk in self.pegs['B'].disks)))
        print("Peg C has disks [{}]".format(", ".join(str(disk.size) for disk in self.pegs['C'].disks)))
        print()

    def is_goal_state(self):
        # Check if the current state matches the goal state
        # The goal is to have all disks on peg 'C' in correct order
        goal_state = {'A': [], 'B': [], 'C': [Disk(i) for i in range(self.num_disks, 0, -1)]}
        for peg_name in self.pegs:
            if [disk.size for disk in self.pegs[peg_name].disks] != [disk.size for disk in goal_state[peg_name]]:
                return False
        return True

    def solve(self, n, source, target, auxiliary):
        # If the goal state is reached, stop the recursion
        if self.goal.get() == 'hanoi solved':
            print("Goal state reached!")
            return

        # Base case: Move a single disk from source to target
        if n == 1:
            self.move_disk(source, target)
        else:
            # Move n-1 disks from source to auxiliary
            self.solve(n-1, source, auxiliary, target)
            # Move the nth disk from source to targets
            self.move_disk(source, target)
            # Move the n-1 disks from auxiliary to target
            self.solve(n-1, auxiliary, target, source)

if __name__ == "__main__":
    hanoi = TowerOfHanoi(num_disks=3)
    print("Initial State:")
    hanoi.print_state()
    hanoi.solve(hanoi.num_disks, 'A', 'C', 'B')