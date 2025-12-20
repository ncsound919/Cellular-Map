"""
TapSpeak Translation Engine for NetworkCellularMap v2.0

Bi-directional translation engine that converts complex biotech/networkology
concepts into instantly memorable plain English using basketball analogies.

Philosophy: "Common man must grok rocket science in 5 seconds"
"""

from typing import List, Optional, Dict, Any
from ..models.schemas import (
    TapSpeakTranslation,
    BBTechMapping,
    ConfidenceMetrics,
    TapSpeakCategory,
    TapSpeakDashboardData
)


class TapSpeakEngine:
    """
    TapSpeak Translation Engine
    
    Converts technical biotech concepts to plain English using:
    - Basketball analogies (BBTech layer)
    - Mnemonic hooks
    - 7-layer translation structure
    """
    
    def __init__(self):
        """Initialize TapSpeak engine with all translations"""
        self._core_concepts = self._load_core_concepts()
        self._networkology_workflow = self._load_networkology_workflow()
        self._codex_translations = self._load_codex_translations()
        self._bbtech_bridge = self._load_bbtech_bridge()
        
        # Build search index
        self._all_translations = (
            self._core_concepts + 
            self._networkology_workflow + 
            self._codex_translations
        )
        self._tag_index = self._build_tag_index()
        
    def _load_core_concepts(self) -> List[TapSpeakTranslation]:
        """Load core biotech + networkology concepts"""
        return [
            TapSpeakTranslation(
                id=1,
                tap_speak="Cells talk in 3D neighborhoods",
                professional="Spatial transcriptomics + tissue geometry",
                operational="MERFISH maps RNA locations in tissue slices",
                translational="Same mutation hits heart brain toe differently due to location",
                confidence=ConfidenceMetrics(esat=85.0, cep=90.0),
                hooks="Cells have addresses not just phone numbers",
                tags=["geometry", "spatial", "merfish", "networkology"]
            ),
            TapSpeakTranslation(
                id=2,
                tap_speak="Fat storing switch flips everywhere",
                professional="Pan-cellular network dysfunction",
                operational="MC4R mutation disrupts leptin signaling across all cells",
                translational="One gene fix cures obesity in heart brain liver simultaneously",
                confidence=ConfidenceMetrics(esat=80.0, cep=85.0),
                hooks="Same broken wire different room symptoms",
                tags=["pan_cellular", "hubs", "obesity", "causal"]
            ),
            TapSpeakTranslation(
                id=3,
                tap_speak="Cut the fat (3PAr high)",
                professional="Innovation exploration metric",
                operational="High 3-point attempt rate = adaptation cycle spread",
                translational="Biotech pathways that explore more options win evolution",
                confidence=ConfidenceMetrics(esat=75.0, cep=80.0),
                hooks="Curry contagion - spread good ideas fast",
                tags=["basketball", "biotech", "gravity", "innovation"]
            ),
            TapSpeakTranslation(
                id=4,
                tap_speak="Don't drop the ball (low TOV)",
                professional="Error propagation threshold",
                operational="Turnover minimization prevents network collapse",
                translational="Too many mutations = system crashes like Eigen threshold",
                confidence=ConfidenceMetrics(esat=80.0, cep=85.0),
                hooks="One fumble loses the game",
                tags=["error_threshold", "stability", "replicator"]
            ),
            TapSpeakTranslation(
                id=5,
                tap_speak="Big dogs eat first (high Gravity)",
                professional="Hub centrality + attractiveness index",
                operational="Scale-free network hubs control 80% system state",
                translational="Fix the kingpin one shot cures whole disease",
                confidence=ConfidenceMetrics(esat=90.0, cep=95.0),
                hooks="Elephant in room pulls whole circus",
                tags=["hubs", "achilles", "gravity", "codex"]
            )
        ]
    
    def _load_networkology_workflow(self) -> List[TapSpeakTranslation]:
        """Load networkology workflow step translations"""
        return [
            TapSpeakTranslation(
                id=10,
                tap_speak="Suck in all the data",
                professional="Heterogeneous federation (BioKleisli)",
                operational="OMIM + GenBank + KEGG + MERFISH via middleware",
                translational="Pulls 100 databases into one map instantly",
                confidence=ConfidenceMetrics(esat=85.0, cep=90.0),
                hooks="Vacuum cleaner for science papers",
                tags=["ingest", "federation", "biokleisli"]
            ),
            TapSpeakTranslation(
                id=11,
                tap_speak="Draw the wiring diagram",
                professional="Geometric interactome construction",
                operational="Neo4j + SpatialGCN builds 3D manifold",
                translational="Shows how genes talk across tissue folds",
                confidence=ConfidenceMetrics(esat=80.0, cep=85.0),
                hooks="City map not phone book",
                tags=["mapping", "geometry", "manifold"]
            ),
            TapSpeakTranslation(
                id=12,
                tap_speak="Find the broken wires",
                professional="Causal discovery + hub detection",
                operational="PC algorithm + NOTEARS on geometric gradients",
                translational="Pinpoints exact mutation causing multi-organ failure",
                confidence=ConfidenceMetrics(esat=85.0, cep=90.0),
                hooks="Detective finds smoking gun",
                tags=["causal", "ai", "hubs", "achilles"]
            ),
            TapSpeakTranslation(
                id=13,
                tap_speak="Score the fixes",
                professional="Codex metrics overlay",
                operational="Trueness(Flow+Gravity) ranks CRISPR targets",
                translational="Gamifies best therapy like fantasy basketball",
                confidence=ConfidenceMetrics(esat=80.0, cep=85.0),
                hooks="NBA stats for DNA repairs",
                tags=["codex", "gamification", "trueness"]
            ),
            TapSpeakTranslation(
                id=14,
                tap_speak="Build the repair crew",
                professional="Vector engineering + digital twins",
                operational="AAV9 follows tissue curvature to hubs",
                translational="Prints custom medicine matching your body geometry",
                confidence=ConfidenceMetrics(esat=75.0, cep=80.0),
                hooks="Uber for CRISPR delivery",
                tags=["intervention", "crispr", "digital_twin"]
            )
        ]
    
    def _load_codex_translations(self) -> List[TapSpeakTranslation]:
        """Load Codex metric translations"""
        return [
            TapSpeakTranslation(
                id=20,
                tap_speak="True as steel",
                professional="Trueness metric",
                operational="CRISPR edit fidelity 1-hamming_distance",
                translational="How perfect is the DNA fix",
                confidence=ConfidenceMetrics(esat=85.0, cep=90.0),
                hooks="No typos in the genome edit",
                tags=["codex", "trueness", "crispr"]
            ),
            TapSpeakTranslation(
                id=21,
                tap_speak="Traffic flow smooth",
                professional="Flow metric",
                operational="AAV delivery efficiency x half_life",
                translational="Medicine reaches target before expiring",
                confidence=ConfidenceMetrics(esat=80.0, cep=85.0),
                hooks="FedEx for genes",
                tags=["codex", "flow", "viral_vector"]
            ),
            TapSpeakTranslation(
                id=22,
                tap_speak="Kingpin power",
                professional="Gravity metric",
                operational="log(degree) x eigenvector_centrality",
                translational="One fix cascades to cure whole system",
                confidence=ConfidenceMetrics(esat=90.0, cep=95.0),
                hooks="Pull one thread unravel disease",
                tags=["codex", "gravity", "hubs"]
            )
        ]
    
    def _load_bbtech_bridge(self) -> List[BBTechMapping]:
        """Load Basketball-Biotech bridge mappings"""
        return [
            BBTechMapping(
                id=30,
                tap_speak="Curry contagion",
                professional="3PAr = innovation exploration",
                operational="High 3PT% = adaptation cycle spread",
                translational="Biotech needs bold experiments like Steph shots",
                confidence=ConfidenceMetrics(esat=75.0, cep=80.0),
                hooks="Splash brothers = mutation winners",
                tags=["bbtech", "3par", "evolution"]
            ),
            BBTechMapping(
                id=31,
                tap_speak="No turnovers",
                professional="TOV = error propagation",
                operational="Low turnovers = mutation stability",
                translational="One bad copy crashes whole pathway",
                confidence=ConfidenceMetrics(esat=85.0, cep=90.0),
                hooks="Fumble = cancer",
                tags=["bbtech", "tov", "eigen_threshold"]
            ),
            BBTechMapping(
                id=32,
                tap_speak="Big dog gravity",
                professional="Gravity = hub attractiveness",
                operational="LeBron ball dominance = network hub control",
                translational="Fix superstar gene cures team",
                confidence=ConfidenceMetrics(esat=90.0, cep=95.0),
                hooks="GOAT gene rules the court",
                tags=["bbtech", "gravity", "scale_free"]
            )
        ]
    
    def _build_tag_index(self) -> Dict[str, List[TapSpeakTranslation]]:
        """Build tag-based search index"""
        index = {}
        for translation in self._all_translations:
            for tag in translation.tags:
                if tag not in index:
                    index[tag] = []
                index[tag].append(translation)
        return index
    
    def get_all_concepts(self, category: Optional[TapSpeakCategory] = None) -> List[TapSpeakTranslation]:
        """Get all translations by category"""
        if category == TapSpeakCategory.CORE_CONCEPTS:
            return self._core_concepts
        elif category == TapSpeakCategory.NETWORKOLOGY_WORKFLOW:
            return self._networkology_workflow
        elif category == TapSpeakCategory.CODEX_TRANSLATIONS:
            return self._codex_translations
        else:
            return self._all_translations
    
    def get_bbtech_mappings(self) -> List[BBTechMapping]:
        """Get all BBTech bridge mappings"""
        return self._bbtech_bridge
    
    def search(
        self,
        query: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_esat: float = 70.0,
        min_cep: float = 80.0
    ) -> List[TapSpeakTranslation]:
        """
        Search TapSpeak translations
        
        Args:
            query: Text search in tap_speak, professional, or hooks
            tags: Filter by tags
            min_esat: Minimum ESAT confidence
            min_cep: Minimum CEP confidence
        """
        results = self._all_translations.copy()
        
        # Filter by tags
        if tags:
            tag_results = []
            for tag in tags:
                if tag in self._tag_index:
                    tag_results.extend(self._tag_index[tag])
            # Remove duplicates by using translation IDs
            seen_ids = set()
            unique_results = []
            for t in tag_results:
                if t.id not in seen_ids:
                    seen_ids.add(t.id)
                    unique_results.append(t)
            results = unique_results
        
        # Filter by query
        if query:
            query_lower = query.lower()
            results = [
                t for t in results
                if (query_lower in t.tap_speak.lower() or
                    query_lower in t.professional.lower() or
                    query_lower in t.hooks.lower() or
                    any(query_lower in tag for tag in t.tags))
            ]
        
        # Filter by confidence
        results = [
            t for t in results
            if t.confidence.meets_threshold(min_esat, min_cep)
        ]
        
        return results
    
    def translate_term(self, technical_term: str, domain: str = "biotech") -> Optional[TapSpeakTranslation]:
        """
        Translate a technical term to TapSpeak
        
        This is a simple lookup implementation. In production, this would use
        an LLM fine-tuned on TapSpeak patterns (spaCy + TapSpeak_LLM_fine_tune).
        """
        # Search for exact or partial match in professional field
        matches = [
            t for t in self._all_translations
            if technical_term.lower() in t.professional.lower()
        ]
        
        if matches:
            return matches[0]
        
        # Search in operational or tags
        matches = [
            t for t in self._all_translations
            if (technical_term.lower() in t.operational.lower() or
                any(technical_term.lower() in tag for tag in t.tags))
        ]
        
        if matches:
            return matches[0]
        
        return None
    
    def get_dashboard_data(self) -> TapSpeakDashboardData:
        """Get all data for TapSpeak dashboard"""
        # Calculate average confidence
        all_confidences = [t.confidence for t in self._all_translations]
        avg_esat = sum(c.esat for c in all_confidences) / len(all_confidences)
        avg_cep = sum(c.cep for c in all_confidences) / len(all_confidences)
        
        return TapSpeakDashboardData(
            core_concepts=self._core_concepts,
            workflow_steps=self._networkology_workflow,
            codex_metrics=self._codex_translations,
            bbtech_mappings=self._bbtech_bridge,
            total_translations=len(self._all_translations),
            average_confidence=ConfidenceMetrics(esat=avg_esat, cep=avg_cep)
        )
    
    def validate_translation(self, translation: TapSpeakTranslation) -> Dict[str, Any]:
        """
        Validate a TapSpeak translation quality
        
        Returns validation metrics and suggestions.
        """
        validations = {
            "valid": True,
            "issues": [],
            "suggestions": []
        }
        
        # Check confidence thresholds
        if not translation.confidence.meets_threshold():
            validations["issues"].append(
                f"Confidence below threshold: ESAT={translation.confidence.esat}, CEP={translation.confidence.cep}"
            )
            validations["valid"] = False
        
        # Check TapSpeak length (should be short and memorable)
        if len(translation.tap_speak) > 50:
            validations["suggestions"].append(
                "TapSpeak phrase is long. Consider shortening for better memorability."
            )
        
        # Check if hooks exist
        if not translation.hooks or len(translation.hooks) < 5:
            validations["issues"].append("Mnemonic hook is missing or too short")
            validations["valid"] = False
        
        # Check tags
        if not translation.tags or len(translation.tags) < 2:
            validations["suggestions"].append("Add more tags for better searchability")
        
        return validations


# Global TapSpeak engine instance
tapspeak_engine = TapSpeakEngine()


def get_tapspeak_engine() -> TapSpeakEngine:
    """Get the global TapSpeak engine instance"""
    return tapspeak_engine
