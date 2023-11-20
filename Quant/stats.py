ans = 0
for m in range(1, 21):
    for n in range(1, 31):
        if m >= n:
            ans += m
        else:
            ans -= n
print(ans / 600)