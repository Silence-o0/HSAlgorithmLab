class Message:
    def __init__(self, mes_id, direction, distance):
        self.mes_id = mes_id   
        self.direction = direction  
        self.distance = distance 


class Process:
    def __init__(self, pid):
        self.id = pid
        self.left = None
        self.right = None
        self.active = True
        self.is_leader = False
        self.inbox = []

    def send_own_id(self, distance):
        self.left.inbox.append(Message(self.id, 'LEFT', distance))
        self.right.inbox.append(Message(self.id, 'RIGHT', distance))

    def forward(self, msg):
        if msg.direction == 'LEFT':
            target = self.left
        else:
            target = self.right
        msg.distance -= 1
        target.inbox.append(msg)

    def receive(self):            
        if not self.active:
            for msg in self.inbox:
                if msg.distance > 0:
                    self.forward(msg)
        else:
            for msg in self.inbox:
                if msg.mes_id == self.id:
                    self.is_leader = True
                elif msg.mes_id > self.id:
                    self.active = False
                    if msg.distance > 0:
                        self.forward(msg)
        self.inbox.clear()


class HS:
    def __init__(self, ids):
        self.processes = [Process(pid) for pid in ids]
        self.proc_num = len(self.processes)
        for i in range(self.proc_num):
            self.processes[i].left = self.processes[(i - 1) % self.proc_num]
            self.processes[i].right = self.processes[(i + 1) % self.proc_num]
        self.rounds = 0
        self.messages = 0

    def run(self):
        while True:
            dist = 2**self.rounds
            self.rounds += 1

            for p in self.processes:
                if p.active:
                    p.send_own_id(dist)
                    self.messages += 2 

            max_steps = dist
            for step in range(max_steps):
                for p in self.processes:
                    p.receive()
                
                for p in self.processes:
                    if p.is_leader:
                        return p.id, self.rounds, self.messages
                


def main():
    tests = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        [1, 3, 2, 7, 9, 11, 8],
        [10, 4, 6, 9],
        [8, 6, 4, 2, 10, 12]
    ]
    
    for ids in tests:
        hs_algorithm = HS(ids)
        leader, rounds, messages = hs_algorithm.run()
        
        print(f"\nIDs: {ids}")
        print(f"Leader ID: {leader}")
        print(f"Rounds: {rounds}")
        print(f"Messages sent: {messages}")
        

if __name__ == "__main__":
    main()