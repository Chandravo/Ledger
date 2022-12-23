import string 
import random

s=''.join(random.choice(string.digits) for _ in range(6))
print(s)