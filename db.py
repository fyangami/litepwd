#  sqlcipher executor by fyang
import os
from subprocess import Popen, PIPE
from utils import print_cyan, error_exit
from log import logger


class SqlcipherExecutor:
    __base_dir = os.path.dirname(__file__)
    __sqlcipher = f"{__base_dir}/bin/sqlcipher"
    __empty_msg = b''

    def __init__(self, db: str, password: str, mode='list', timeout=3, debug=False, shell=False):
        self.db = db
        self.__password = password
        self.db_path = f"{self.__base_dir}/{db}"
        self.__mode = mode
        self.__timeout = timeout
        self.__debug = debug
        self.shell = shell
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
                        _group text,
                        create_time int
                    );
                """)
                if e != self.__empty_msg:
                    os.remove(self.db_path)
                    error_exit(shell=self.shell)
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

    def insert(self, name: str, val: str, _group: str, create_time: int, table_name='store') -> str:
        # column, vals = self.__data_join(**kwargs)
        sql = f"insert into {table_name}(id, name, val, _group, create_time) " \
              f"values(null, '{name}', '{val}', '{_group}', {create_time})"
        out, err = self.__sqlcipher_executor(sql)
        return err.decode()

    def delete(self, table_name='store', **kwargs) -> bool:
        pass

    def update(self, table_name='store', **kwargs) -> bool:
        pass

    def query_one(self, table_name='store', **kwargs) -> dict:
        pass

    def query_all(self, table_name='store') -> list:
        sql = f"""
            select * from {table_name};
        """
        out, err = self.__sqlcipher_executor(sql)
        if err != self.__empty_msg:
            logger.error(err.decode())
            error_exit(shell=self.shell)
        return self.__store_dict_creator(out.decode())

    def query_by_group(self, key, table_name='store', like=False) -> list:
        return self.__query_by(key, "_group", table_name, like)

    def __query_by(self, key, by, table_name, like) -> list:
        sql = f"""
            select * from {table_name} where {by}{" like " if like else "="}'{"%" if like else ""}{key}{"%" if like else ""}';
        """
        out, err = self.__sqlcipher_executor(sql)
        if err != self.__empty_msg:
            logger.error(err.decode())
            error_exit(shell=self.shell)
        if table_name == 'store':
            return self.__store_dict_creator(out.decode())
        return self.__result_splitter(out.decode())

    def __store_dict_creator(self, out) -> list:
        lines = self.__result_splitter(out)
        res = []
        try:
            for line in lines:
                _ = line.split("|")
                res.append({
                    "id": _[0],
                    "name": _[1],
                    "password": _[2],
                    "_group": _[3],
                    "create_time": _[4]
                })
            print(res)
            return res
        except KeyError as e:
            logger.error(e)
            error_exit(shell=self.shell)

    def rekey(self, key):
        sql = f"""
            PRAGMA rekey = '{key}'
        """
        out, err = self.__sqlcipher_executor(sql)
        if err != self.__empty_msg:
            logger.error(err.decode())
            error_exit(shell=self.shell)

    def update_store_pwd(self, pwd_hash, table_name="store", name="", group="") -> bool:
        q_sql = "select name from store where "
        sql_part = f"_group='{group}'" if name == "" else f"name='{name}';"
        q_sql += sql_part
        print_cyan(q_sql)
        out, err = self.__sqlcipher_executor(q_sql)
        if err != self.__empty_msg:
            logger.error(err.decode())
            error_exit()
        # print_cyan(self.__result_splitter(out))
        if not len(self.__result_splitter(out.decode())):
            return False
        u_sql = f"update store set val='{pwd_hash}' where "
        u_sql += sql_part
        o, e = self.__sqlcipher_executor(u_sql)
        if e != self.__empty_msg:
            logger.error(err.decode())
            error_exit(shell=self.shell)
        return True

    def query_by_name(self, key, table_name="store", like=False) -> list:
        return self.__query_by(key, "name", table_name, like)

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
