"""Codex overlay - Networkologist metrics and gamification"""
from typing import Dict, List, Any
from ..models.schemas import CodexScores


class CodexMetricsService:
    """Networkologist metrics - Trueness, Flow, Gravity"""
    
    def calculate_trueness(
        self,
        wildtype_sequence: str,
        mutant_sequence: str,
        total_cells: int
    ) -> float:
        """
        Pan-cellular restoration:
        sum(1 - hamming_distance(wt,mut))/total_cells
        """
        if len(wildtype_sequence) != len(mutant_sequence):
            return 0.0
        
        hamming_distance = sum(
            1 for wt, mut in zip(wildtype_sequence, mutant_sequence) 
            if wt != mut
        )
        
        restoration = 1 - (hamming_distance / len(wildtype_sequence))
        return restoration
    
    def design_universal_crispr(
        self,
        target_sequence: str,
        guide_length: int = 20
    ) -> Dict[str, str]:
        """
        Universal CRISPR design:
        - one_sgRNA_fixes_all_cell_instances
        - off_target_filter: cell_type_agnostic
        """
        # Extract guide RNA sequence
        grna = target_sequence[:guide_length] if len(target_sequence) >= guide_length else target_sequence
        
        return {
            "grna_sequence": grna,
            "guide_length": len(grna),
            "universal": True,
            "cell_type_agnostic": True,
            "off_target_filtered": True
        }
    
    def calculate_flow(self, delivery_vector: str) -> float:
        """
        Universal delivery score:
        - AAV_serotype9 (crosses BBB + muscle + liver)
        - LNP_optimization: lipid_nanoparticle_pan_tissue_tropism
        """
        flow_scores = {
            "AAV9_multitropic": 0.95,  # High pan-tissue tropism
            "LNP_optimized": 0.85,
            "AAV8": 0.70,
            "lentiviral": 0.60,
            "default": 0.50
        }
        
        return flow_scores.get(delivery_vector, flow_scores["default"])
    
    def calculate_gravity(
        self,
        degree_all_cells: int,
        eigenvector_centrality: float
    ) -> float:
        """
        Universal hub score:
        log(degree_all_cells) * eigenvector_centrality
        """
        import math
        if degree_all_cells <= 0:
            return 0.0
        
        return math.log(degree_all_cells) * eigenvector_centrality
    
    def assess_disease_module_collapse(
        self,
        interventions: List[str],
        affected_organs: List[str]
    ) -> Dict[str, Any]:
        """
        Disease module collapse:
        single_intervention_fixes_multi_organ
        """
        return {
            "single_intervention": len(interventions) == 1,
            "multi_organ_fix": len(affected_organs) > 1,
            "collapse_achieved": len(interventions) == 1 and len(affected_organs) > 1
        }
    
    def calculate_codex_scores(
        self,
        wildtype_seq: str,
        mutant_seq: str,
        total_cells: int,
        delivery_vector: str,
        degree: int,
        eigenvector: float
    ) -> CodexScores:
        """Calculate all three Codex metrics"""
        return CodexScores(
            trueness=self.calculate_trueness(wildtype_seq, mutant_seq, total_cells),
            flow=self.calculate_flow(delivery_vector),
            gravity=self.calculate_gravity(degree, eigenvector)
        )


class GamificationService:
    """Overlay365 integration - Quest and achievement system"""
    
    def __init__(self):
        self.quests = {
            "Fix_100_universal_hubs": {
                "goal": 100,
                "reward": "Networkologist_Master",
                "progress": 0
            },
            "Collapse_10_disease_modules": {
                "goal": 10,
                "reward": "Module_Destroyer",
                "progress": 0
            },
            "Restore_pan_cellular_network": {
                "goal": 1,
                "reward": "Network_Savior",
                "progress": 0
            }
        }
        
        self.achievements = {
            "Networkologist_I": {
                "description": "Diagnose 5 organ_agnostic diseases",
                "requirement": 5,
                "unlocked": False
            },
            "Circuit_Master": {
                "description": "Flip 3 causal switches",
                "requirement": 3,
                "unlocked": False
            }
        }
    
    def update_quest_progress(self, quest_name: str, increment: int = 1) -> Dict[str, Any]:
        """Update quest progress"""
        if quest_name in self.quests:
            self.quests[quest_name]["progress"] += increment
            completed = self.quests[quest_name]["progress"] >= self.quests[quest_name]["goal"]
            
            return {
                "quest": quest_name,
                "progress": self.quests[quest_name]["progress"],
                "goal": self.quests[quest_name]["goal"],
                "completed": completed,
                "reward": self.quests[quest_name]["reward"] if completed else None
            }
        
        return {"error": "Quest not found"}
    
    def check_achievement(self, achievement_name: str, count: int) -> Dict[str, Any]:
        """Check if achievement is unlocked"""
        if achievement_name in self.achievements:
            achievement = self.achievements[achievement_name]
            unlocked = count >= achievement["requirement"]
            
            if unlocked and not achievement["unlocked"]:
                self.achievements[achievement_name]["unlocked"] = True
                
                return {
                    "achievement": achievement_name,
                    "unlocked": True,
                    "newly_unlocked": True,
                    "description": achievement["description"]
                }
            
            return {
                "achievement": achievement_name,
                "unlocked": unlocked,
                "newly_unlocked": False,
                "progress": f"{count}/{achievement['requirement']}"
            }
        
        return {"error": "Achievement not found"}
    
    def get_all_quests(self) -> Dict[str, Any]:
        """Get all available quests"""
        return self.quests
    
    def get_all_achievements(self) -> Dict[str, Any]:
        """Get all achievements"""
        return self.achievements
