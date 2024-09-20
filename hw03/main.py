from datetime import datetime, timedelta
start_date = datetime(2024, 1, 10)

x = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
print(x)


