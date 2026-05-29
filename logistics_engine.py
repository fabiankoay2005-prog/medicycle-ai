def transfer_simulation(stock_a, stock_b, demand):

    shortage = max(0, demand - stock_a)

    transfer = min(stock_b, shortage)

    stock_a += transfer
    stock_b -= transfer

    return {
        "hospital_A_stock": stock_a,
        "hospital_B_stock": stock_b,
        "transferred": transfer,
        "status": "balanced" if stock_a >= demand else "critical"
    }