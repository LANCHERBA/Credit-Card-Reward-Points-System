import numpy as np

sample_transactions = {
    "T01": {"date": "2021-05-01", "merchant_code": "sportchek", "amount_cents": 21000},
    "T02": {"date": "2021-05-02", "merchant_code": "sportchek", "amount_cents": 8700},
    "T03": {"date": "2021-05-03", "merchant_code": "tim_hortons", "amount_cents": 323},
    "T04": {"date": "2021-05-04", "merchant_code": "tim_hortons", "amount_cents": 1267},
    "T05": {"date": "2021-05-05", "merchant_code": "tim_hortons", "amount_cents": 2116},
    "T06": {"date": "2021-05-06", "merchant_code": "tim_hortons", "amount_cents": 2211},
    "T07": {"date": "2021-05-07", "merchant_code": "subway", "amount_cents": 1853},
    "T08": {"date": "2021-05-08", "merchant_code": "subway", "amount_cents": 2153},
    "T09": {"date": "2021-05-09", "merchant_code": "sportchek", "amount_cents": 7326},
    "T10": {"date": "2021-05-10", "merchant_code": "tim_hortons", "amount_cents": 1321}
}

sample_transactions2 = {
    'T1': {'date': '2021-05-09', 'merchant_code': 'sportchek', 'amount_cents': 2500},
    'T2': {'date': '2021-05-10', 'merchant_code': 'tim_hortons', 'amount_cents': 1000},
    'T3': {'date': '2021-05-10', 'merchant_code': 'the_bay', 'amount_cents': 500},
    'T4': {'date': '2021-05-11', 'merchant_code': 'sportchek', 'amount_cents': 2000}
}

# Sport Check, Tim Hortons, Subway, Else, rewards points
rules = [
    [75, 25, 25, 0, 500],
    [75, 25, 0, 0, 300],
    [75, 0, 0, 0, 200],
    [25, 10, 10, 0, 150],
    [25, 10, 0, 0, 75],
    [20, 0, 0, 0, 75],
    [1, 0, 0, 0, 1],
    [0, 1, 0, 0, 1],
    [0, 0, 1, 0, 1],
    [0, 0, 0, 1, 1],
]


def get_max_monthly_reward_points(rules, transactions):
    """
    :param rules: reward_points calculation rules shaped as a matrix.
    :param transactions: monthly transactions dict
    :return: max monthly reward points
    """
    # Accumulate transaction total for each merchants
    sportchek_total, tim_hortons_total, subway_total, else_total = 0, 0, 0, 0
    for transaction in transactions.values():
        if transaction["merchant_code"] == "sportchek":
            sportchek_total += round(transaction["amount_cents"] / 100)
        elif transaction["merchant_code"] == "tim_hortons":
            tim_hortons_total += round(transaction["amount_cents"] / 100)
        elif transaction["merchant_code"] == "subway":
            subway_total += round(transaction["amount_cents"] / 100)
        else:
            else_total += round(transaction["amount_cents"] / 100)

    """
    Create DP problem data structure:
        1.dp 4D shape: sportcheck_total+1 | tim_hortons_total + 1 |subway_total + 1 | else_total + 1
        2.Example: dp[1][1][1][0] contains the max reward points when monthly transaction total contains:
          1 dollar of Sport Check purchase
          1 dollar of Tim Hortons purchase
          1 dollar of subway purchase 
          0 dollar of other purchase
        3.From dp[0][0][0][0] to dp[sportchek_total][tim_hortons_total][subway_total][else_total]
    """
    dp = np.zeros((sportchek_total + 1, tim_hortons_total + 1, subway_total + 1, else_total + 1), dtype=int)

    # temp: temperate highest score
    temp = 0
    # current_state: A vector to check which merchant's purchase is increased by 1
    current_state = [0, 0, 0, 0]
    for i in range(0, sportchek_total + 1):
        for j in range(0, tim_hortons_total + 1):
            for k in range(0, subway_total + 1):
                for l in range(0, else_total + 1):
                    # Assign default temp value based on which merchant's purchase is increase by 1.
                    if current_state[0] != i:
                        current_state[0] = i
                        temp = dp[i - 1][j][k][l] if i > 0 else dp[i][j][k][l]
                    elif current_state[1] != j:
                        current_state[1] = j
                        temp = dp[i][j - 1][k][l] if j > 0 else dp[i][j][k][l]
                    elif current_state[2] != k:
                        current_state[2] = k
                        temp = dp[i][j][k - 1][l] if k > 0 else dp[i][j][k][l]
                    elif current_state[3] != l:
                        current_state[3] = l
                        temp = dp[i][j][k][l - 1] if l > 0 else dp[i][j][k][l]
                    for rule in rules:
                        # Check if a rule can be applied on current total purchase (dp)
                        if (i - rule[0]) >= 0 and (j - rule[1]) >= 0 and (k - rule[2]) >= 0 and (l - rule[3]) >= 0:
                            new_highest_score = dp[i - rule[0]][j - rule[1]][k - rule[2]][l - rule[3]] + rule[4]
                            # Is the new score > the previous score before we add one dollar purchase to a brand?
                            temp = temp if temp >= new_highest_score else new_highest_score
                            dp[i][j][k][l] = temp

    result = dp[sportchek_total][tim_hortons_total][subway_total][else_total]
    print(result)
    return result


if __name__ == "__main__":
    get_max_monthly_reward_points(rules, sample_transactions)
