"""Neo4j database connection and utilities"""
from neo4j import GraphDatabase
from typing import Optional, List, Dict, Any
from ..core.config import settings


class Neo4jConnection:
    """Neo4j database connection manager"""
    
    def __init__(self):
        self._driver = None
        
    def connect(self):
        """Establish connection to Neo4j"""
        self._driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )
        
    def close(self):
        """Close the connection"""
        if self._driver:
            self._driver.close()
            
    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None):
        """Execute a Cypher query"""
        with self._driver.session(database=settings.NEO4J_DATABASE) as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def create_universal_gene_node(self, node_data: Dict[str, Any]):
        """Create a UniversalGene node"""
        query = """
        CREATE (g:UniversalGene {
            universal_id: $universal_id,
            mutation_status: $mutation_status,
            hub_gravity: $hub_gravity,
            organ_agnostic_impact: $organ_agnostic_impact,
            network_role: $network_role
        })
        RETURN g
        """
        return self.execute_query(query, node_data)
    
    def create_pan_cellular_edge(self, edge_data: Dict[str, Any]):
        """Create a pan-cellular relationship"""
        query = """
        MATCH (a:UniversalGene {universal_id: $source_id})
        MATCH (b:UniversalGene {universal_id: $target_id})
        CREATE (a)-[r:INTERACTS {
            relation_type: $relation_type,
            disruption_impact: $disruption_impact,
            weight: $weight,
            exists_in_all_cells: true
        }]->(b)
        RETURN r
        """
        return self.execute_query(query, edge_data)
    
    def find_universal_hubs(self, degree_threshold: int = 50) -> List[Dict[str, Any]]:
        """Find universal hub nodes"""
        query = """
        MATCH (g:UniversalGene)
        WITH g, size((g)-[]-()) as degree
        WHERE degree > $threshold
        RETURN g.universal_id as hub_id, degree, g.hub_gravity as gravity
        ORDER BY degree DESC
        """
        return self.execute_query(query, {"threshold": degree_threshold})
    
    def get_disease_module(self, mutation_ids: List[str]) -> Dict[str, Any]:
        """Get disease module for given mutations"""
        query = """
        MATCH (g:UniversalGene)
        WHERE g.universal_id IN $mutation_ids
        MATCH path = (g)-[*1..3]-(related:UniversalGene)
        WITH collect(DISTINCT related.universal_id) as module_nodes
        RETURN module_nodes
        """
        return self.execute_query(query, {"mutation_ids": mutation_ids})
    
    def initialize_schema(self):
        """Initialize database schema with constraints and indexes"""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (g:UniversalGene) REQUIRE g.universal_id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:PanCellularProtein) REQUIRE p.universal_id IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (g:UniversalGene) ON (g.network_role)",
            "CREATE INDEX IF NOT EXISTS FOR (g:UniversalGene) ON (g.mutation_status)",
            "CREATE INDEX IF NOT EXISTS FOR (g:UniversalGene) ON (g.hub_gravity)",
        ]
        
        for constraint in constraints:
            try:
                self.execute_query(constraint)
            except Exception as e:
                print(f"Constraint/Index creation warning: {e}")


# Global connection instance
db_connection = Neo4jConnection()


def get_db():
    """Dependency for database connection"""
    return db_connection
