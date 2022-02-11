from datetime import datetime
import psycopg2

from typing import Sequence, Any

from webtemplate.repo.base import AbstractRepository, ConnectionAPI

from .models import User


class PostgresRepository(AbstractRepository):

    def __init__(self, repository_url: dict):
        super().__init__(repository_url)
        self.connection = None
        self.connection_class_api = PostgresConnectionAPI

    def _connect(self):

        try:
            con = psycopg2.connect(
                host=self.repo_url["host"],
                user=self.repo_url["user"],
                password=self.repo_url["pw"],
                database=self.repo_url["database"],
            )
            return con

        except psycopg2.OperationalError:
            return self.connection

        except Exception:
            return self.connection

    def can_connect(self):
        con = self._connect()
        if con:
            if getattr(con, 'closed') == 0:
                return True

        return False

    def initialize(self) -> bool:
        con = self._connect()
        if not con:
            return False

        cur = con.cursor()

        try:
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE"
                " table_schema='public' "
            )

            tables = {row[0] for row in cur.fetchall()}

            if "users" not in tables:
                cur.execute(
                    """
                create table users (
                    ident VARCHAR(256) UNIQUE NOT NULL,
                    name VARCHAR(256) NOT NULL,
                    first_name VARCHAR(256) NOT NULL,
                    last_name VARCHAR(256) NOT NULL,
                    email VARCHAR(256) UNIQUE NOT NULL,
                    password VARCHAR(256) NOT NULL,
                    datetime TIMESTAMP,
                    PRIMARY KEY (ident)
                )
                """
                )

        finally:
            cur.close()
            con.commit()

        return True

    def create(self) -> ConnectionAPI:

        return self.connection_class_api(self._connect())


class PostgresConnectionAPI(ConnectionAPI):

    def __init__(self, connection) -> None:
        self._connection = connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
        self._connection = None

    def _execute_one(self, sql_query: str, values: Sequence[Any] = ()):
        if self._connection is None:
            raise TypeError("Postgres connection is None.")

        cur = self._connection.cursor()
        cur.execute(sql_query, values)
        row = cur.fetchone()
        cur.close()

        return row

    def _execute_many(self, sql_query: str, values: Sequence[Any] = ()):
        if self._connection is None:
            raise TypeError("Postgres connection is None.")

        cur = self._connection.cursor()
        cur.execute(sql_query, values)
        row = cur.fetchall()
        cur.close()

        return row

    def _execute(self, sql_query: str, values: Sequence[Any] = ()):
        if self._connection is None:
            raise TypeError("Postgres connection is None.")

        cur = self._connection.cursor()
        cur.execute(sql_query, values)
        cur.close()
        self._connection.commit()

    def set_user(self, user: User):
        self._execute(
            "INSERT INTO users(ident, name, first_name, last_name, email, password, datetime) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (user.ident, user.name, user.first_name, user.last_name, user.email, user.password, datetime.today().strftime('%Y-%m-%d %H:%M:%S')),
        )
    
    def get_user(self, ident: str = None, email: str = None) -> User:
        user = self._execute_one(
            "SELECT ident, name, first_name, last_name, email, password "
            "FROM users "
            "WHERE ident=%s "
            "OR email=%s",
            (ident, email),
        )

        if user:
            return User(user[0], user[1], user[2], user[3], user[4], user[5])

        return user

    def get_ident(self, email):
        ident = self._execute_one(
            "SELECT ident "
            "FROM users "
            "WHERE email=%s",
            (email,),
        )

        return ident[0]

    def get_email(self, email):
        email = self._execute_one(
            "SELECT email "
            "FROM users "
            "WHERE email=%s",
            (email,),
        )

        return email
    
    def get_password(self, email):
        password = self._execute_one(
            "SELECT password "
            "FROM users "
            "WHERE email=%s",
            (email,),
        )

        return password[0]