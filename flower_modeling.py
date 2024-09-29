import math
# DVR model

pear_a = 107.94
pear_b = 0.9

# 일평균
day_temp = []

DVRi = 1/(pear_a *(pear_b**day_temp))

# DVRi 누적값 100 -> 예상 만개기

# mDVR model
# DVR_1이 1 이면 자발휴면 타파, 2이면 저온감응기 종료, 이후 DVR_2 계산, 누적 최종적으로 DVR_2가 0.9593 -> 만개

# 시간별 기온
temp = ['시간별 기온']
# 최고기온(h), 최저기온(m), 전날최고기온(hy), 다음날 최저 기온(mt)
hour =['시간']
h = ['오늘 최고기온']
m = ['오늘 최저기온']
hy = ['전날 최고기온']
mt = ['다음날 최저기온']

if 0 <= hour <= 3:
    temp = (hy - m) * math.sin((4 - hour) * 3.14 / 30)**2 + m
elif 4 <= hour <= 13:
    temp = (h - m) * math.sin((hour - 4) * 3.14 / 18)**2 + m
elif 14 <= hour <= 23:
    temp = (h - mt) * math.sin((28 - hour) * 3.14 / 30)**2 + mt


# DVR_1
def DVR_1():
    if 0<= temp <=6 :
        DVR_1 = 1.333 * 10**-3
    elif 6< temp <=9 :
        DVR_1 = 2.276 * 10**-3 - 1.571 * 10**-4 * temp
    elif 9< temp <=12 :
        DVR_1 = 3.448 * 10**-3 - 2.874 * 10**-4 * temp

    return DVR_1

# DVR_1합 -> for 문?

# DVR_1합 = 1 -> 내생휴면 해제
# DVR_1합 = 2 -> 저온감응기 종료, DVR_2 계산 시작

# DVR_2
def DVR_2():
    if temp <= 20 :
        DVR_2 = math.exp(35.27 - 12094(temp + 273)**-1)
    elif 20 <= temp :
        DVR_2 = math.exp(5.82 - 3474(temp + 273)**-1)

    return DVR_2

# DVR_2합 = 0.9593 -> 예상 만개기
