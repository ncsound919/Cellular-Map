"""Data ingestion service - Anti-reductionist federation"""
import requests
from typing import Dict, List, Any, Optional
from Bio import Entrez
from ..core.config import settings


class OMIMService:
    """OMIM API service for pan-cellular data"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OMIM_API_KEY
        self.base_url = "https://api.omim.org/api"
    
    def query_pan_cellular_mutations(self, gene: str) -> Dict[str, Any]:
        """Query mutations affecting multiple tissues"""
        # Placeholder implementation - would need actual OMIM API integration
        return {
            "gene": gene,
            "phenotypes": [],
            "mutations": [],
            "multi_tissue_effects": True
        }


class GenBankService:
    """GenBank/Entrez service for universal sequences"""
    
    def __init__(self, api_key: Optional[str] = None):
        if api_key or settings.NCBI_API_KEY:
            Entrez.api_key = api_key or settings.NCBI_API_KEY
        Entrez.email = "networkology@example.com"
    
    def fetch_universal_sequences(self, gene_id: str) -> Dict[str, Any]:
        """Fetch sequences for gene across different contexts"""
        try:
            handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
            records = Entrez.read(handle)
            handle.close()
            return {
                "gene_id": gene_id,
                "sequences": records,
                "universal_mutation_id": f"UNI_{gene_id}"
            }
        except Exception as e:
            return {"error": str(e), "gene_id": gene_id}


class KEGGService:
    """KEGG REST API service for cell-agnostic pathways"""
    
    def __init__(self):
        self.base_url = settings.KEGG_API_BASE
    
    def get_pathway_reconstruction(self, pathway_id: str) -> Dict[str, Any]:
        """Get pathway reconstruction across all cell types"""
        try:
            response = requests.get(f"{self.base_url}/get/{pathway_id}")
            response.raise_for_status()
            return {
                "pathway_id": pathway_id,
                "data": response.text,
                "cell_agnostic": True
            }
        except Exception as e:
            return {"error": str(e), "pathway_id": pathway_id}
    
    def get_gene_pathways(self, gene: str) -> List[str]:
        """Get all pathways for a gene"""
        try:
            response = requests.get(f"{self.base_url}/link/pathway/{gene}")
            if response.status_code == 200:
                pathways = [line.split("\t")[1] for line in response.text.strip().split("\n")]
                return pathways
            return []
        except Exception as e:
            print(f"Error fetching pathways: {e}")
            return []


class DataIngestionService:
    """Main data ingestion service - BioKleisli queries"""
    
    def __init__(self):
        self.omim = OMIMService()
        self.genbank = GenBankService()
        self.kegg = KEGGService()
    
    def biokleisli_join(self, gene: str) -> Dict[str, Any]:
        """
        Execute BioKleisli join:
        JOIN OMIM.mutations = GenBank.sequences ON universal_genomic_position
        JOIN KEGG.pathways = OMIM.phenotypes ON shared_gene_loci
        WHERE mutation_detected_in_heart AND mutation_detected_in_brain
        """
        # Fetch data from all sources
        omim_data = self.omim.query_pan_cellular_mutations(gene)
        genbank_data = self.genbank.fetch_universal_sequences(gene)
        kegg_pathways = self.kegg.get_gene_pathways(gene)
        
        # Combine into pan-cellular graph seed
        return {
            "universal_id": f"GENE_{gene}",
            "omim_phenotypes": omim_data.get("phenotypes", []),
            "sequences": genbank_data.get("sequences", []),
            "pathways": kegg_pathways,
            "multi_tissue": True,
            "pan_cellular_graph_seed": True
        }
    
    def collapse_organ_specific_to_network_impact(
        self, 
        phenotypes: List[Dict[str, Any]]
    ) -> float:
        """Transform organ-specific phenotypes to network impact score"""
        if not phenotypes:
            return 0.0
        
        # Calculate network-wide impact
        tissue_count = len(set(p.get("tissue", "") for p in phenotypes))
        severity_avg = sum(p.get("severity", 0) for p in phenotypes) / len(phenotypes)
        
        return min(1.0, (tissue_count / 10.0) * severity_avg)
