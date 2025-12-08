score = [(0.5125, 'A'), (0.5115, 'B'), (0.8, 'C')]
score.sort(key=lambda x: x[0], reverse=True)
print(score)

score2 = [(0.5125, 'A'), (0.5115, 'B'), (0.8, 'C')]
score2.sort(reverse=True)
print(score2)
