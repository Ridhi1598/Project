import sys
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from common.util.config import ConfigReader
from features.steps.globalVar import GlobalVar


class Postgres:
    def __init__(self):
        """Establishes session with db engine"""
        self.session = None
        self.metadata = None
        configdata = ConfigReader().configFileReader(f"{sys.argv[1]}_appConfig.json")
        self.username = configdata.get("postgres_username")
        self.password = configdata.get("postgres_password")
        self.host = configdata.get("postgres_host")
        self.port = configdata.get("postgres_port")
        self.name = configdata.get("postgres_name")
        url = "postgresql://{}:{}@{}:{}/{}".format(self.username, self.password, self.host, str(self.port), self.name)
        self.engine = create_engine(url, pool_pre_ping=True, pool_recycle=300)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)

    def find_tables(self):
        """returns list of all existing tables in db"""
        tables = self.metadata.tables
        return tables

    def create_session(self):
        """creates session for db queries"""
        db_session = sessionmaker(bind=self.engine)
        self.session = db_session()
        return

    def get_table_data(self, table_name, column_name, filter_term):
        """this method is used to query into a table using filter details"""
        self.find_tables()
        table = self.metadata.tables[table_name]
        self.create_session()
        # results = self.session.query(table).all()
        # print(results)
        results = self.session.query(table).filter(table.columns[column_name] == filter_term).all()
        return results

    def stop_connection(self):
        """closes connection with postgres"""
        self.session.close()
