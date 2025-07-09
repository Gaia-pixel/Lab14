from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def get_stores():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.*
                        FROM stores s
                            """
            cursor.execute(query)

            for row in cursor:
                result.append(Store(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNodes(store):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT o.*
                        FROM orders o
                        WHERE o.store_id = %s
                                """
            cursor.execute(query, (store.store_id, ))

            for row in cursor:
                result.append(Order(**row))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi1(store, k):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t1.order_id as o1, t2.order_id as o2, t1.p1+t2.p2 as peso
                        FROM (SELECT o.order_id, o.order_date, COUNT(oi.item_id) as p1
                                FROM orders o, order_items oi 
                                WHERE o.order_id  = oi.order_id 
                                        and o.store_id  = %s
                                GROUP BY o.order_id, o.order_date) t1,
                                (SELECT o.order_id, o.order_date, COUNT(oi.item_id) as p2
                                FROM orders o, order_items oi 
                                WHERE o.order_id  = oi.order_id 
                                        and o.store_id  = %s
                                GROUP BY o.order_id, o.order_date) t2
                        WHERE DATEDIFF(t1.order_date, t2.order_date) > 0
                        and DATEDIFF(t1.order_date, t2.order_date) < %s
                        """
            cursor.execute(query, (store.store_id, store.store_id, k))

            for row in cursor:
                result.append((row['o1'], row['o2'], row['peso']))

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllArchi2(store):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT o.order_id as o, o.order_date as data, COUNT(oi.item_id) as numOgg
                        FROM orders o, order_items oi 
                        WHERE o.order_id  = oi.order_id 
                                and o.store_id  = %s
                        GROUP BY o.order_id, o.order_date
                            """
            cursor.execute(query, (store.store_id, ))

            for row in cursor:
                result.append((row['o'], row['data'], row['numOgg']))

            cursor.close()
            cnx.close()

        return result



