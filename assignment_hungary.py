# 最佳匹配算法 KM算法
from munkres import Munkres
import sys

matrix = [[5, 9, 1],
          [10, 3, 2],
          [8, 7, 4]]
profit_matrix = []

for row in matrix:
    profit_row = []
    for col in row:
        profit_row += [sys.maxsize - col]
    profit_matrix += [profit_row]

m = Munkres()
indexes_cost = m.compute(matrix)
indexes_profit = m.compute(profit_matrix)
total_cost = 0
total_profit = 0

for row, column in indexes_cost:
    value = matrix[row][column]
    total_cost += value
    print(f'({row}, {column}) -> {value}')
print(f'total cost: {total_cost}')

for row, column in indexes_profit:
    value = matrix[row][column]
    total_profit += value
    print(f'({row}, {column}) -> {value}')
print(f'total profit={total_profit}')

