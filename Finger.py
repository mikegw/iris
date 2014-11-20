class Finger:

    total = 0

    def __init__(self, position):
        Finger.total += 1
        self.number = Finger.total
        self.position = position
        self.velocity_history = []
        self.position_history = [position]
        self.state = 'Inactive'

    def pos_update(self, position):
        self.position_history.append(position)
        if len(self.position_history) == 10:
            del self.position_history[0]

    def vel_update(self, velocity):
        self.velocity_history.append(velocity)
        if len(self.velocity_history) == 10:
            del self.velocity_history[0]

    def vel_calc(self):
        if len(self.position_history) > 1:
            dx = self.position_history[-1][0] - self.position_history[-2][0]
            dy = self.position_history[-1][1] - self.position_history[-2][1]
            dt = self.position_history[-1][2] - self.position_history[-2][2]
            return (dx/dt,dy/dt, self.position_history[-1][2])
        else:
            print("Error: Cannot Calculate Velocity - Only one position!")
            return(None)

    def activate(self):
        self.state = 'Active'

    def update(self, position):
        self.pos_update(position)
        self.vel_update(self.vel_calc())
        

