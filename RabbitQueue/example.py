from queueClassServerRabbit import *
from inputBox import *

t = Consumer()
t.start()
input = InputBox()

texto = input.input()
print(texto)

t.kill()
