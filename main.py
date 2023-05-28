import numpy as np
import random
import pandas as pd
from demo import Demo

demo = Demo(uri='bolt://localhost:7687', user='neo4j', password='12345678')
# demo.print_greeting(message="Hello World!")


# generate financial transaction

# unique transaction id's
transaction_id = [i for i in range(1, 51)]

# vendor/customer number
vendor_number = np.random.randint(low=1, high=2500, size=(50,))

# transaction amount
transaction_amount = np.random.randint(low=20, high=1250000, size=(50,))

# transaction type
transaction_types = ['cash_withdrawl', 'cash_deposit', 'transfer_domestic', 'transfer_international']

# generate list of random integers
random_integers = [random.randint(0, 3) for i in range(0, 50)]
transaction_list = [transaction_types[i] for i in random_integers]

transaction_data = {"transaction_ID": transaction_id,
                    "vendor_number": list(vendor_number),
                    "transaction_amount": list(transaction_amount),
                    "transaction_type": transaction_list}

transaction_DataFrame = pd.DataFrame(transaction_data)
transaction_list = transaction_DataFrame.values.tolist()
print(transaction_list)
for i in transaction_list:
    demo.create_transaction(transaction_id=str(i[0]),
                            vendor_number=str(i[1]),
                            transaction_amount=str(i[2]),
                            transaction_type=str(i[3]))
