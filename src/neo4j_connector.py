# app/neo4j_connector.py
from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]
    
    def get_apartment_by_name(self, name):
        query = (
            "MATCH (n) "
            "WHERE n.name = $name "
            "RETURN id(n) AS identity, n.name AS name, n.description AS description"
        )
        result = self.query(query, {"name": name})
        return result

# Neo4j 연결 인스턴스 생성
uri = "bolt://localhost:7687"
user = "neo4j"
password = "89468946"
neo4j_connector = Neo4jConnector(uri, user, password)
