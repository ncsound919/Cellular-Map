"""Orchestration utilities - Lightweight pipeline management without bloat"""
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
import json


class PipelineStage:
    """Represents a single stage in the analysis pipeline"""
    
    def __init__(
        self,
        name: str,
        function: Callable,
        dependencies: Optional[List[str]] = None
    ):
        self.name = name
        self.function = function
        self.dependencies = dependencies or []
        self.status = "pending"
        self.output = None
        self.error = None
        self.start_time = None
        self.end_time = None
    
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the stage function"""
        self.status = "running"
        self.start_time = datetime.now()
        
        try:
            self.output = self.function(inputs)
            self.status = "completed"
        except Exception as e:
            self.error = str(e)
            self.status = "failed"
            self.output = {"error": str(e)}
        
        self.end_time = datetime.now()
        return self.output
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stage to dictionary"""
        return {
            "name": self.name,
            "status": self.status,
            "dependencies": self.dependencies,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": (self.end_time - self.start_time).total_seconds() 
                       if self.start_time and self.end_time else None,
            "error": self.error
        }


class NetworkologyPipeline:
    """
    Lightweight pipeline orchestrator for Networkology workflows.
    
    Implements the core DAG: ingest → map → analyze → intervene
    Without the bloat of Airflow/Nextflow.
    """
    
    def __init__(self, name: str = "NetworkologyPipeline"):
        self.name = name
        self.stages: Dict[str, PipelineStage] = {}
        self.execution_order: List[str] = []
        self.results: Dict[str, Any] = {}
    
    def add_stage(
        self,
        name: str,
        function: Callable,
        dependencies: Optional[List[str]] = None
    ) -> "NetworkologyPipeline":
        """
        Add a stage to the pipeline.
        
        Parameters
        ----------
        name : str
            Unique stage identifier
        function : Callable
            Function to execute for this stage
        dependencies : Optional[List[str]]
            List of stage names this depends on
            
        Returns
        -------
        NetworkologyPipeline
            Self for chaining
        """
        self.stages[name] = PipelineStage(name, function, dependencies)
        return self
    
    def _resolve_dependencies(self) -> List[str]:
        """Topological sort to determine execution order"""
        visited = set()
        order = []
        
        def visit(stage_name: str):
            if stage_name in visited:
                return
            visited.add(stage_name)
            
            stage = self.stages[stage_name]
            for dep in stage.dependencies:
                if dep in self.stages:
                    visit(dep)
            
            order.append(stage_name)
        
        for stage_name in self.stages:
            visit(stage_name)
        
        return order
    
    def execute(self, initial_inputs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute the entire pipeline.
        
        Parameters
        ----------
        initial_inputs : Optional[Dict[str, Any]]
            Initial inputs for the pipeline
            
        Returns
        -------
        Dict[str, Any]
            Pipeline execution results
        """
        self.execution_order = self._resolve_dependencies()
        self.results = initial_inputs or {}
        
        execution_log = []
        
        for stage_name in self.execution_order:
            stage = self.stages[stage_name]
            
            # Gather inputs from dependencies
            stage_inputs = {}
            for dep_name in stage.dependencies:
                if dep_name in self.results:
                    stage_inputs[dep_name] = self.results[dep_name]
            
            # Add initial inputs
            stage_inputs.update(self.results.get("initial", {}))
            
            # Execute stage
            output = stage.execute(stage_inputs)
            self.results[stage_name] = output
            
            execution_log.append(stage.to_dict())
            
            # Stop on failure if configured
            if stage.status == "failed":
                break
        
        return {
            "pipeline": self.name,
            "status": "completed" if all(
                s.status == "completed" for s in self.stages.values()
            ) else "failed",
            "execution_order": self.execution_order,
            "results": self.results,
            "log": execution_log
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            "pipeline": self.name,
            "total_stages": len(self.stages),
            "stages": {
                name: stage.to_dict() 
                for name, stage in self.stages.items()
            }
        }


class NetworkologyDAG:
    """
    Pre-configured DAG for standard Networkology workflow:
    Ingest → Map → Analyze → Intervene
    """
    
    def __init__(self):
        self.pipeline = NetworkologyPipeline("NetworkologyCore")
        self._setup_core_dag()
    
    def _setup_core_dag(self):
        """Setup the core 4-stage DAG"""
        
        # Stage 1: Ingest
        def ingest_stage(inputs: Dict[str, Any]) -> Dict[str, Any]:
            """Data ingestion from OMIM, GenBank, KEGG"""
            # Import here to avoid circular dependencies and handle missing modules gracefully
            try:
                from .ingestion import DataIngestionService
                
                service = DataIngestionService()
                gene = inputs.get("gene", "TP53")
                
                return {
                    "status": "success",
                    "stage": "ingest",
                    "data": service.biokleisli_join(gene)
                }
            except ImportError as e:
                return {
                    "status": "error",
                    "stage": "ingest",
                    "error": f"Failed to import ingestion service: {str(e)}"
                }
        
        # Stage 2: Map
        def map_stage(inputs: Dict[str, Any]) -> Dict[str, Any]:
            """Network mapping - build universal interactome"""
            try:
                from .network import UniversalInteractomeService
                
                service = UniversalInteractomeService()
                
                return {
                    "status": "success",
                    "stage": "map",
                    "network_stats": {
                        "nodes": 0,
                        "edges": 0,
                        "note": "Network mapping placeholder"
                    }
                }
            except ImportError as e:
                return {
                    "status": "error",
                    "stage": "map",
                    "error": f"Failed to import network service: {str(e)}"
                }
        
        # Stage 3: Analyze
        def analyze_stage(inputs: Dict[str, Any]) -> Dict[str, Any]:
            """AI analysis - causal discovery and hub identification"""
            try:
                from .ai_scientist import CausalDiscoveryService
                
                service = CausalDiscoveryService()
                
                return {
                    "status": "success",
                    "stage": "analyze",
                    "analysis": service.identify_causal_examples()
                }
            except ImportError as e:
                return {
                    "status": "error",
                    "stage": "analyze",
                    "error": f"Failed to import AI scientist service: {str(e)}"
                }
        
        # Stage 4: Intervene
        def intervene_stage(inputs: Dict[str, Any]) -> Dict[str, Any]:
            """Design intervention - CRISPR repair"""
            try:
                from .repair import RepairDesignService
                
                service = RepairDesignService()
                
                return {
                    "status": "success",
                    "stage": "intervene",
                    "repair_design": {
                        "note": "CRISPR design placeholder"
                    }
                }
            except ImportError as e:
                return {
                    "status": "error",
                    "stage": "intervene",
                    "error": f"Failed to import repair service: {str(e)}"
                }
        
        # Build DAG
        self.pipeline.add_stage("ingest", ingest_stage, dependencies=[])
        self.pipeline.add_stage("map", map_stage, dependencies=["ingest"])
        self.pipeline.add_stage("analyze", analyze_stage, dependencies=["map"])
        self.pipeline.add_stage("intervene", intervene_stage, dependencies=["analyze"])
    
    def run(self, gene: str = "TP53") -> Dict[str, Any]:
        """
        Run the complete Networkology DAG.
        
        Parameters
        ----------
        gene : str
            Gene to analyze
            
        Returns
        -------
        Dict[str, Any]
            Complete pipeline results
        """
        return self.pipeline.execute({"initial": {"gene": gene}})


class TapSpeakGenerator:
    """
    Plain Python + CSV lexicon for TapSpeak generation.
    Lightweight NLP without huge stack.
    """
    
    def __init__(self, lexicon_path: str = "/tmp/tapspeak_lexicon.csv"):
        self.lexicon_path = lexicon_path
        self.lexicon = {}
        self._load_lexicon()
    
    def _load_lexicon(self):
        """Load or create CSV lexicon"""
        try:
            import csv
            with open(self.lexicon_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.lexicon[row['term']] = {
                        'hook': row['hook'],
                        'explanation': row['explanation']
                    }
        except FileNotFoundError:
            # Create default lexicon
            self.lexicon = {
                'hub': {
                    'hook': 'network traffic controller',
                    'explanation': 'critical connection point in cellular network'
                },
                'scale_free': {
                    'hook': 'follows power law',
                    'explanation': 'few nodes have many connections, most have few'
                },
                'Achilles_heel': {
                    'hook': 'critical vulnerability',
                    'explanation': 'removing key hubs causes network collapse'
                }
            }
    
    def generate_hook(self, technical_term: str) -> str:
        """
        Generate plain-language hook for technical term.
        
        Parameters
        ----------
        technical_term : str
            Technical/scientific term
            
        Returns
        -------
        str
            Plain-language hook
        """
        if technical_term in self.lexicon:
            return self.lexicon[technical_term]['hook']
        
        # Simple heuristic fallback
        return f"simplified: {technical_term.replace('_', ' ')}"
    
    def update_lexicon(self, term: str, hook: str, explanation: str):
        """Add or update term in lexicon"""
        self.lexicon[term] = {
            'hook': hook,
            'explanation': explanation
        }
    
    def export_lexicon(self):
        """Export lexicon to CSV"""
        import csv
        
        with open(self.lexicon_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['term', 'hook', 'explanation'])
            writer.writeheader()
            for term, data in self.lexicon.items():
                writer.writerow({
                    'term': term,
                    'hook': data['hook'],
                    'explanation': data['explanation']
                })


class BBTechMetrics:
    """
    BBTech metric calculations using simple CSV stack.
    No platform bloat - just Python + CSV.
    """
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_trueness(
        self,
        restored_edges: int,
        total_disrupted_edges: int
    ) -> float:
        """
        Calculate Trueness metric.
        
        Trueness = restored_edges / total_disrupted_edges
        """
        if total_disrupted_edges == 0:
            return 0.0
        return restored_edges / total_disrupted_edges
    
    def calculate_flow(
        self,
        delivered_molecules: int,
        target_molecules: int
    ) -> float:
        """
        Calculate Flow metric.
        
        Flow = delivered_molecules / target_molecules
        """
        if target_molecules == 0:
            return 0.0
        return delivered_molecules / target_molecules
    
    def calculate_gravity(
        self,
        hub_degree: int,
        hub_betweenness: float
    ) -> float:
        """
        Calculate Gravity metric.
        
        Gravity = log(degree) * betweenness
        """
        import math
        if hub_degree <= 0:
            return 0.0
        return math.log(hub_degree + 1) * hub_betweenness
    
    def export_to_csv(self, filepath: str = "/tmp/bbtech_metrics.csv"):
        """Export metrics to CSV"""
        import csv
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['metric', 'value', 'timestamp'])
            for name, value in self.metrics.items():
                writer.writerow([name, value, datetime.now().isoformat()])
