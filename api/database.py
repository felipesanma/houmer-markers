import pymysql

import config

params = dict(config.get_env())


class MySQL:
    """
    A class for manage mysql connections
    """

    def __init__(self):
        self.mysql_host: str = params["MYSQL_HOST"]
        self.mysql_port: int = int(params["MYSQL_PORT"])
        self.mysql_user: str = params["MYSQL_USER"]
        self.mysql_password: str = params["MYSQL_PASS"]
        self.mysql_db: str = params["MYSQL_DATABASE"]
        self.connection = pymysql.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            password=self.mysql_password,
            db=self.mysql_db,
            charset="utf8",
            use_unicode=True,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def __str__(self):
        print_object = f"""MySQL(mysql_host={self.mysql_host},mysql_port={self.mysql_port},mysql_user={self.mysql_user},mysql_password={self.mysql_password},mysql_db={self.mysql_db})"""
        return print_object

    def __enter__(self):
        self.connection.ping(reconnect=True)
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()


class BasicQuerys:

    """
    A class for doing basic query to mysql
    """

    def __init__(self, query: str, mysql_db: MySQL = MySQL()):

        self.mysql_db = mysql_db
        self.query = query

    def select(self) -> tuple[bool, list]:
        config.log.info(f"Executing select: {self.query}")
        with self.mysql_db as cursor:
            cursor.execute(self.query)
            data = cursor.fetchall()
        fetched = True if len(data) > 0 else False
        return fetched, data

    def insert(self) -> bool:
        result = False
        config.log.info(f"Executing select: {self.query}")
        with self.mysql_db as cursor:
            cursor.execute(self.query)
            result = True
        return result

    def update(self) -> bool:
        config.log.info(f"Executing update: {self.query}")
        result = False
        with self.mysql_db as cursor:
            cursor.execute(self.query)
            result = True
        return result
