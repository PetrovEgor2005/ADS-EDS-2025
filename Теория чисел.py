def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

LCM - Least Common Multiple

def lcm(a, b):
    return a * b / gcd(a, b)


-1 % 7 = 6

-7 % 7 = 0
-6 % 7 = 1
-5 % 7 = 2

1 % 7
1 + 6 = 7
-1 % 7
-1 - 6 = -7
 
 
 3 10
 3 = 10 mod 7
 3 % 7 = 3
 10 % 7 = 3
 n % 10 ** 9 + 7

7 * 15 = 105 % 26 = 1

2 ^ 123 % 26 

2 * 2 * 2 * 2 * ... * 2 (123 times) % 26

123 % 2 = 1
2 * 2 = 4 ^ 122
122 % 2 = 0
122 // 2 = 61
4 ^ 61
16 ^ 60
256 ^ 30
256 * 256 ^ 15
256 ^ 2 * 256
n != log n 

256 != 8

a = 2
p = 5


a ^ (p - 1) % p = 1
a ^ p % p = a

2 ^ (5 - 1) % 5 = 16 % 5 = 1
2 ^ 5 % 5 = 32 % 5 = 2

list_ = [True] * 100000

2 -> list_[4] = False -> list_[6] = False -> list_[8] = False -> ... -> list_[100000] = False
if i == True:
3 -> list_[9] = False list_[15] = False -> list_[21] = False -> ... -> list_[99999] = False
4
5 -> list_[25] = False -> list_[35] = False -> ... -> list_[99995] = False
7 
11 
13
17
19
23
29
31


11 * 11 = 121
11 * 1 = 11
11 * 2
11 * 3
11 * 4
11 * 5
11 * 6
11 * 7
11 * 8
11 * 9
11 * 10
11 * 11

11 -> 11 ** 2 -> 11 ** 3 -> 11 ** 4 -> 11 ** 5 -> 11 ** 6 -> 11 ** 7 -> 11 ** 8 -> 11 ** 9 -> 11 ** 10
5 

def seive(n:int) -> list:
    numbers = [True] * n
    primes = []
    for i in range(2, int(n ** 0.5) + 1):
        if numbers[i]:
            primes.append(i)
            for j in range(i * i, int(n ** 0.5) + 1, i):
                numbers[j] = False
    return primes