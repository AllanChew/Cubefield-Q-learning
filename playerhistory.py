from collections import deque

# example usage: PlayerHistory(20)
class PlayerHistory:
    q = deque() # most recent to least recent
    def __init__(self,max_history):
        self.max_history = max_history
    def UpdateHistoryQueue(self,action,reward): # called after applying each action
        while len(self.q) > self.max_history: # remove old entries
            self.q.pop() # removes least recent (oldest)
        self.q.appendleft((action,reward)) # add current value to queue

