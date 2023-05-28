import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class Demo:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        with self.driver.session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        print(f'result: {result.single()}')
        return result.single()[0]

    def create_transaction(self, transaction_id, vendor_number, transaction_amount, transaction_type):
        with self.driver.session() as session:
            result = session.execute_write(
                self._create_and_return_transaction,
                transaction_id,
                vendor_number,
                transaction_amount,
                transaction_type)
            for record in result:
                print(f"Created transaction: {record}")

    @staticmethod
    def _create_and_return_transaction(tx, transaction_id, vendor_number, transaction_amount, transaction_type):
        query = ("CREATE (t:Transaction {transaction_id: $transaction_id, vendor_number: $vendor_number,"
                 "transaction_amount: $transaction_amount, transaction_type: $transaction_type}) "
                 "RETURN t"
                 )
        result = tx.run(query,
                        transaction_id=transaction_id,
                        vendor_number=vendor_number,
                        transaction_amount=transaction_amount,
                        transaction_type=transaction_type)
        try:
            return [record["t"]["transaction_id"] for record in result]
            # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise
