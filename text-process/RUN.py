from relevance import *
from timeit import default_timer as timer

start = timer()

URL = "https://www.theguardian.com/world/2020/nov/10/nagorno-karabakh-armenia-pm-signs-deal-to-end-war-with-azerbaijan-and-russia"
#URL = "https://www.euronews.com/2020/10/26/nagorno-karabakh-new-ceasefire-struck-but-azerbaijan-and-armenia-accuse-each-other-of-brea"
#URL = "https://www.euronews.com/2020/10/18/nagorno-karabakh-armenia-and-azerbaijan-announce-humanitarian-truce-2"
#URL = "https://www.theguardian.com/world/2020/oct/17/nagorno-karabakh-azerbaijan-says-12-civilians-killed-by-shelling-in-ganja"
#URL = "https://www.theguardian.com/world/2020/nov/10/nagorno-karabakh-peace-deal-turkey-russia-reshapes-regional-geopolitics"

aze_content = relevance('aze',URL,5,15)
arm_content = relevance('arm',URL,5,15)

for i in range(len(aze_content)):
    print(aze_content[i])
    print('----------------------------------------------------------------------------------------------------------------------------')
    print(arm_content[i])
    print('===========================================================================================================================')

end = timer()
time = end - start
print('Execution time is {}'.format(time)) # Time in seconds, e.g. 5.38091952400282
