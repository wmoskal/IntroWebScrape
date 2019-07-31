import NHL_Player_Data_Extraction
import statistics


def getStdev(list):
    return statistics.stdev(list)

print('test')
goals = NHL_Player_Data_Extraction.getGoals()
print(goals)
if isinstance(goals, list) == True:
    print(len(goals))
stdevGoals = getStdev(goals)

print(stdevGoals)