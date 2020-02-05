#  sqlcipher executor by fyang
import os
from subprocess import Popen, PIPE
from utils import print_cyan, error_exit


class SqlcipherExecutor:
    __base_dir = os.path.dirname(__file__)
    __sqlcipher = f"{__base_dir}/bin/sqlcipher"
    __empty_msg = b''

    def __init__(self, db: str, password: str, mode='list', timeout=3, debug=False):
        self.db = db
        self.__password = password
        self.db_path = f"{self.__base_dir}/{db}"
        self.__mode = mode
        self.__timeout = timeout
        self.__debug = debug
        if not self.__check():
            raise self.SqlcipherException("login failed!")

    def __check(self) -> bool:
        out, err = self.__sqlcipher_executor('.tables')
        if err == self.__empty_msg:
            tables = self.__result_splitter(out.decode())
            if 'store' not in tables:
                print_cyan("[*] init db...")
                o, e = self.__sqlcipher_executor("""
                    create table store(
                        id integer primary key autoincrement,
                        name text unique,
                        val text,
                        alias text,
                        create_time int
                    );
                """)
                if e != self.__empty_msg:
                    os.remove(self.db_path)
                    error_exit()
                print_cyan('[*] successfully!')
            return True
        return False

    @staticmethod
    def __result_splitter(result) -> list:
        return [line for line in result.split('\n') if line not in ('', 'ok')]

    def __popen_creator(self, q: str):
        return Popen(
            f'{self.__sqlcipher} {self.db_path} -{self.__mode} -init cmd "{q}" -cmd "PRAGMA key=\'{self.__password}\'"',
            shell=True,
            stdout=PIPE,
            stderr=PIPE
        )

    def __sqlcipher_executor(self, q):
        popen = self.__popen_creator(q)
        if self.__debug:
            print(popen.args)
        return popen.communicate(timeout=self.__timeout)

    def insert(self, table_name='store', **kwargs) -> str:
        column, vals = self.__data_join(**kwargs)
        sql = f"""
            insert into {table_name}(id, {column[:-1]}) values (null, {vals[:-1]})
        """
        out, err = self.__sqlcipher_executor(sql)
        return err.decode()

    def delete(self, table_name='store', **kwargs) -> bool:
        pass

    def update(self, table_name='store', **kwargs) -> bool:
        pass

    def query_one(self, table_name='store', **kwargs) -> dict:
        pass

    def query_all(self, table_name='store', **kwargs) -> list:
        pass

    def query_by_alias(self, alias, table_name='store') -> list:
        sql = f"""
            select * from {table_name} where alias='{alias}';
        """
        out, err = self.__sqlcipher_executor(sql)
        if err != self.__empty_msg:
            raise self.SqlcipherException(err.decode())
        return self.__result_splitter(out)

    def query_by_name(self) -> dict:
        pass

    @staticmethod
    def __data_join(**kwargs) -> tuple:
        column = ""
        vals = ""
        for k, v in kwargs.items():
            column += f"{k},"
            vals += f"'{v}',"
        return column, vals

    class SqlcipherException(Exception):
        pass
