from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT *
                        FROM stores"""

            cursor.execute(query)

            for row in cursor:
                result.append(
                    Store(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def get_orders(store):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """ SELECT *
                        FROM orders o
                        WHERE o.store_id = %s"""

            cursor.execute(query, (store,))

            for row in cursor:
                result.append(
                    Order(**row))

            cursor.close()
            cnx.close()

        return result

