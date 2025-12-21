#!/usr/bin/env python3
"""
NetworkCellularMap v2.0 + Cerebro Desktop Tool
One-click autonomous discovery engine
Exports: JSON, CSV, HTML reports to ./exports/

Usage:
    python cellular_map_desktop.py

The tool will:
1. Set up working directories
2. Install dependencies (first run only)
3. Start backend services
4. Run autonomous discovery cycles every 4 hours
5. Export structured results (JSON, CSV, HTML)
"""

import os
import sys
import json
import subprocess
import time
import shutil
from datetime import datetime
from pathlib import Path
import signal
import atexit
from typing import Dict, Any, List, Optional


class CellularMapDesktop:
    """
    Desktop launcher for NetworkCellularMap v2.0 + Cerebro
    
    Provides autonomous discovery with structured exports.
    """
    
    # Configuration
    DISCOVERY_INTERVAL_HOURS = 4
    HIGH_IMPACT_GENES = ["TP53", "BRCA1", "EGFR", "KRAS", "PIK3CA"]
    HIGH_GRAVITY_THRESHOLD = 0.8
    BACKEND_PORT = 8000
    BACKEND_HOST = "127.0.0.1"
    
    def __init__(self, home_dir: Optional[Path] = None):
        """
        Initialize the desktop tool.
        
        Args:
            home_dir: Optional custom home directory. Defaults to ~/CellularMapDesktop
        """
        self.home = home_dir or Path.home() / "CellularMapDesktop"
        self.exports = self.home / "exports"
        self.logs = self.home / "logs"
        self.data = self.home / "data"
        
        # Create directory structure
        for path in [self.home, self.exports, self.logs, self.data]:
            path.mkdir(parents=True, exist_ok=True)
        
        self.processes: List[tuple] = []
        self.backend_proc: Optional[subprocess.Popen] = None
        self._shutdown_requested = False
        
        print("🧠 CellularMap Desktop - Big dogs eat first")
        print(f"📁 Working directory: {self.home}")
        print(f"📤 Exports directory: {self.exports}")
    
    def install_dependencies(self) -> None:
        """Install all required packages from backend requirements."""
        print("📦 Installing dependencies...")
        
        # Use the backend requirements.txt if available
        backend_dir = Path(__file__).parent / "backend"
        requirements_file = backend_dir / "requirements.txt"
        
        if requirements_file.exists():
            print(f"   Installing from {requirements_file}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
        else:
            # Fallback to core requirements
            requirements = [
                "fastapi", "uvicorn", "neo4j", "networkx", "torch",
                "scanpy", "pandas", "numpy", "requests", "pydantic",
                "python-dotenv"
            ]
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "--upgrade"
            ] + requirements)
        
        print("✅ Dependencies installed")
    
    def start_backend(self) -> bool:
        """
        Start the FastAPI backend server.
        
        Returns:
            True if backend started successfully, False otherwise
        """
        print("🚀 Starting backend services...")
        
        # Get path to backend directory
        backend_dir = Path(__file__).parent / "backend"
        
        if not (backend_dir / "main.py").exists():
            print("⚠️  Backend not found at expected location")
            print(f"   Expected: {backend_dir}")
            return False
        
        # Prepare environment
        env = os.environ.copy()
        env.update({
            "NEO4J_URI": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
            "NEO4J_USER": os.environ.get("NEO4J_USER", "neo4j"),
            "NEO4J_PASSWORD": os.environ.get("NEO4J_PASSWORD", "password"),
            "REDIS_URL": os.environ.get("REDIS_URL", "redis://localhost:6379"),
        })
        
        # Start uvicorn
        self.backend_proc = subprocess.Popen(
            [
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", self.BACKEND_HOST,
                "--port", str(self.BACKEND_PORT)
            ],
            cwd=str(backend_dir),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.processes.append(("backend", self.backend_proc))
        
        # Wait for backend to be ready
        print("   Waiting for backend to start...")
        backend_ready = self._wait_for_backend(timeout=30)
        
        if backend_ready:
            print("✅ Backend started successfully")
            return True
        else:
            print("⚠️  Backend may not be fully ready (continuing anyway)")
            return True
    
    def _wait_for_backend(self, timeout: int = 30) -> bool:
        """
        Wait for backend to be ready.
        
        Args:
            timeout: Maximum seconds to wait
            
        Returns:
            True if backend is ready, False otherwise
        """
        import time
        try:
            import requests
        except ImportError:
            # If requests not available, just wait a fixed time
            time.sleep(10)
            return True
        
        start = time.time()
        url = f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}/health"
        
        while time.time() - start < timeout:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    return True
            except (requests.RequestException, Exception):
                pass
            time.sleep(1)
        
        return False
    
    def _get_api_base_url(self) -> str:
        """Get the base URL for API calls."""
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}/api/v1"
    
    def autonomous_discovery_loop(self) -> None:
        """
        Run Cerebro's autonomous discovery loop.
        
        Runs discovery cycles every DISCOVERY_INTERVAL_HOURS hours.
        """
        print("🤖 Cerebro autonomous agent started...")
        
        cycle = 0
        while not self._shutdown_requested:
            try:
                cycle += 1
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                
                print(f"\n🔄 Discovery Cycle #{cycle} ({timestamp})")
                
                # Initialize Cerebro for this cycle
                self._initialize_cerebro()
                
                # Run Cerebro nightly report
                self.fetch_cerebro_report(timestamp)
                
                # Run Networkologist discoveries
                self.run_networkologist_discoveries(timestamp)
                
                # Generate TapSpeak insights
                self.generate_tapspeak_insights(timestamp)
                
                # Export structured results
                self.export_breakthroughs(timestamp)
                
                # Calculate sleep duration
                sleep_seconds = self.DISCOVERY_INTERVAL_HOURS * 3600
                print(f"✅ Cycle complete. Sleeping {self.DISCOVERY_INTERVAL_HOURS}h until next discovery...")
                
                # Sleep in small intervals to allow for graceful shutdown
                self._interruptible_sleep(sleep_seconds)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping gracefully...")
                break
            except Exception as e:
                print(f"⚠️  Cycle error: {e}")
                # Wait 1 hour on error before retrying
                self._interruptible_sleep(3600)
    
    def _interruptible_sleep(self, seconds: int) -> None:
        """
        Sleep for the specified duration, checking for shutdown requests.
        
        Args:
            seconds: Total seconds to sleep
        """
        interval = 10  # Check every 10 seconds
        elapsed = 0
        while elapsed < seconds and not self._shutdown_requested:
            time.sleep(min(interval, seconds - elapsed))
            elapsed += interval
    
    def _initialize_cerebro(self) -> None:
        """Initialize Cerebro for the current session."""
        try:
            import requests
            response = requests.post(
                f"{self._get_api_base_url()}/cerebro/initialize",
                json={"name": "DesktopAgent", "field": "Biotech"},
                timeout=10
            )
            if response.status_code == 200:
                print("   🧠 Cerebro initialized")
            else:
                print(f"   ⚠️  Cerebro init returned: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Cerebro init failed: {e}")
    
    def fetch_cerebro_report(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """
        Get Cerebro's autonomous discoveries.
        
        Args:
            timestamp: Current timestamp for file naming
            
        Returns:
            Report data if successful, None otherwise
        """
        try:
            import requests
            response = requests.get(
                f"{self._get_api_base_url()}/cerebro/nightly_report",
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"⚠️  Cerebro report returned status: {response.status_code}")
                return None
            
            report = response.json()
            
            # Save report
            report_path = self.exports / f"cerebro_report_{timestamp}.json"
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
            
            # Count discoveries
            discoveries = report.get("sections", {}).get("New Discoveries", [])
            discovery_count = len(discoveries) if isinstance(discoveries, list) else 0
            print(f"🧠 Cerebro discoveries: {discovery_count} new findings")
            print(f"   📄 Saved to: {report_path}")
            
            return report
            
        except ImportError:
            print("⚠️  requests library not available")
            return None
        except Exception as e:
            print(f"⚠️  Cerebro report failed: {e}")
            return None
    
    def run_networkologist_discoveries(self, timestamp: str) -> List[Dict[str, Any]]:
        """
        Run autonomous network analysis on high-impact genes.
        
        Args:
            timestamp: Current timestamp for file naming
            
        Returns:
            List of breakthrough discoveries
        """
        breakthroughs = []
        
        try:
            import requests
        except ImportError:
            print("⚠️  requests library not available")
            return breakthroughs
        
        print("🔬 Running Networkologist analysis on high-impact genes...")
        
        for gene in self.HIGH_IMPACT_GENES:
            try:
                # Analyze universal hub
                hub_url = f"{self._get_api_base_url()}/universal_hub/{gene}"
                hub_response = requests.get(hub_url, timeout=30)
                
                if hub_response.status_code != 200:
                    print(f"   ⚠️  {gene}: hub analysis failed ({hub_response.status_code})")
                    continue
                
                hub = hub_response.json()
                
                # Get gravity score from response
                pan_cellular = hub.get("pan_cellular_impact", {})
                gravity = pan_cellular.get("gravity_score", 0)
                
                # Also check codex_scores if available
                codex_scores = hub.get("codex_scores", {})
                if isinstance(codex_scores, dict):
                    gravity = max(gravity, codex_scores.get("gravity", 0))
                
                print(f"   📊 {gene}: gravity={gravity:.2f}")
                
                # Design repair if high gravity
                if gravity > self.HIGH_GRAVITY_THRESHOLD:
                    repair_url = f"{self._get_api_base_url()}/repair_design/{gene}"
                    repair_response = requests.post(
                        repair_url,
                        json={"hub_id": gene, "mutation_ids": [f"{gene}_common"]},
                        timeout=30
                    )
                    
                    repair_data = {}
                    if repair_response.status_code == 200:
                        repair_data = repair_response.json()
                    
                    breakthrough = {
                        "gene": gene,
                        "hub_analysis": hub,
                        "repair_design": repair_data,
                        "timestamp": timestamp,
                        "priority": "HIGH_GRAVITY",
                        "gravity_score": gravity
                    }
                    
                    # Save breakthrough
                    breakthrough_path = self.exports / f"breakthrough_{gene}_{timestamp}.json"
                    with open(breakthrough_path, "w", encoding="utf-8") as f:
                        json.dump(breakthrough, f, indent=2)
                    
                    breakthroughs.append(breakthrough)
                    print(f"   💡 BREAKTHROUGH: {gene} repair design ready")
                    print(f"      📄 Saved to: {breakthrough_path}")
                
            except Exception as e:
                print(f"   ⚠️  {gene} analysis failed: {e}")
        
        return breakthroughs
    
    def generate_tapspeak_insights(self, timestamp: str) -> Optional[Dict[str, Any]]:
        """
        Generate plain English insights using TapSpeak.
        
        Args:
            timestamp: Current timestamp for file naming
            
        Returns:
            Dashboard data if successful, None otherwise
        """
        try:
            import requests
            
            response = requests.get(
                f"{self._get_api_base_url()}/tapspeak/dashboard",
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"⚠️  TapSpeak dashboard returned status: {response.status_code}")
                return None
            
            insights = response.json()
            
            # Export as CSV
            csv_path = self.exports / f"tapspeak_insights_{timestamp}.csv"
            with open(csv_path, "w", encoding="utf-8") as f:
                f.write("tap_speak,professional,esat,cep,tags\n")
                
                # Combine all concept types
                all_concepts = []
                all_concepts.extend(insights.get("core_concepts", []))
                all_concepts.extend(insights.get("workflow_steps", []))
                all_concepts.extend(insights.get("codex_metrics", []))
                
                for concept in all_concepts:
                    tap_speak = concept.get("tap_speak", "").replace(",", ";")
                    professional = concept.get("professional", "").replace(",", ";")
                    confidence = concept.get("confidence", {})
                    esat = confidence.get("esat", 0)
                    cep = confidence.get("cep", 0)
                    tags = ";".join(concept.get("tags", []))
                    
                    f.write(f'"{tap_speak}","{professional}",{esat},{cep},"{tags}"\n')
            
            # Also save full JSON
            json_path = self.exports / f"tapspeak_insights_{timestamp}.json"
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(insights, f, indent=2)
            
            concept_count = len(all_concepts)
            print(f"💬 TapSpeak insights exported: {concept_count} concepts")
            print(f"   📄 CSV: {csv_path}")
            print(f"   📄 JSON: {json_path}")
            
            return insights
            
        except ImportError:
            print("⚠️  requests library not available")
            return None
        except Exception as e:
            print(f"⚠️  TapSpeak insights failed: {e}")
            return None
    
    def export_breakthroughs(self, timestamp: str) -> Path:
        """
        Generate unified HTML report.
        
        Args:
            timestamp: Current timestamp for file naming
            
        Returns:
            Path to the generated HTML file
        """
        formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_date = datetime.now().strftime("%Y-%m-%d")
        
        # Count exports from this cycle
        export_files = list(self.exports.glob(f"*_{timestamp}.*"))
        breakthrough_files = list(self.exports.glob(f"breakthrough_*_{timestamp}.json"))
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>CellularMap Breakthroughs {formatted_date}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 40px;
            background: #f5f7fa;
            color: #1a1a2e;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            color: #1e40af;
            border-bottom: 3px solid #3b82f6;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #1e3a8a;
            margin-top: 30px;
        }}
        .breakthrough {{
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }}
        .tap {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #f59e0b;
            border-radius: 4px;
        }}
        .meta {{
            color: #64748b;
            font-size: 0.9em;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #3b82f6;
        }}
        .file-list {{
            background: #f1f5f9;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.85em;
        }}
        .file-list li {{
            margin: 5px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 CellularMap Desktop - Breakthrough Report</h1>
        <p class="meta"><strong>Generated:</strong> {formatted_time}</p>
        <p class="meta"><strong>Cycle Timestamp:</strong> {timestamp}</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(export_files)}</div>
                <div>Total Exports</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(breakthrough_files)}</div>
                <div>Breakthroughs</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(self.HIGH_IMPACT_GENES)}</div>
                <div>Genes Analyzed</div>
            </div>
        </div>

        <h2>🎯 New Discoveries</h2>
        <div class="breakthrough">
            <p>Discovery analysis complete. Check the exports directory for detailed results:</p>
            <ul class="file-list">
"""
        
        # List all export files for this timestamp
        for file_path in sorted(export_files):
            html_content += f"                <li>📄 {file_path.name}</li>\n"
        
        if not export_files:
            html_content += "                <li>No exports generated in this cycle</li>\n"
        
        html_content += f"""            </ul>
        </div>

        <h2>💬 TapSpeak Quick Reference</h2>
        <div class="tap">
            <strong>"Big dogs eat first"</strong> = Hub centrality focus - Fix the kingpin first
        </div>
        <div class="tap">
            <strong>"Curry contagion"</strong> = High innovation exploration - Bold experiments win
        </div>
        <div class="tap">
            <strong>"Cells talk in 3D neighborhoods"</strong> = Spatial transcriptomics matters
        </div>

        <h2>📁 Export Directory</h2>
        <div class="file-list">
            <code>{self.exports}</code>
        </div>

        <h2>🔧 Configuration</h2>
        <ul>
            <li><strong>Discovery Interval:</strong> Every {self.DISCOVERY_INTERVAL_HOURS} hours</li>
            <li><strong>High-Impact Genes:</strong> {', '.join(self.HIGH_IMPACT_GENES)}</li>
            <li><strong>Gravity Threshold:</strong> {self.HIGH_GRAVITY_THRESHOLD}</li>
        </ul>

        <p class="meta" style="margin-top: 40px; text-align: center;">
            NetworkCellularMap v2.0 + Cerebro Autonomous Agent<br>
            <a href="https://github.com/ncsound919/Cellular-Map">github.com/ncsound919/Cellular-Map</a>
        </p>
    </div>
</body>
</html>
"""
        
        # Save HTML report
        html_path = self.exports / f"breakthroughs_{timestamp}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"📊 HTML report generated: {html_path}")
        
        # Copy to desktop if accessible
        try:
            desktop_path = Path.home() / "Desktop"
            if desktop_path.exists() and desktop_path.is_dir():
                desktop_file = desktop_path / f"CellularMap_{timestamp}.html"
                shutil.copy2(html_path, desktop_file)
                print(f"   📋 Copied to Desktop: {desktop_file}")
        except Exception as e:
            # Desktop copy is optional, don't fail if it doesn't work
            pass
        
        return html_path
    
    def cleanup(self) -> None:
        """Graceful shutdown of all services."""
        print("\n🛑 Cleaning up...")
        self._shutdown_requested = True
        
        for name, proc in self.processes:
            if proc and proc.poll() is None:  # Process is still running
                print(f"   Stopping {name}...")
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"   Force killing {name}...")
                    proc.kill()
        
        self.processes.clear()
        print("✅ Clean shutdown complete")


def main():
    """Main entry point for CellularMap Desktop."""
    print("\n" + "=" * 60)
    print("  NetworkCellularMap v2.0 + Cerebro Desktop Tool")
    print("  One-click autonomous discovery engine")
    print("=" * 60 + "\n")
    
    desktop = CellularMapDesktop()
    
    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        desktop.cleanup()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(desktop.cleanup)
    
    # Install dependencies on first run
    initialized_marker = desktop.home / "initialized"
    if not initialized_marker.exists():
        try:
            desktop.install_dependencies()
            initialized_marker.touch()
        except Exception as e:
            print(f"⚠️  Dependency installation failed: {e}")
            print("   Continuing anyway - some features may not work")
    
    # Start backend
    backend_started = desktop.start_backend()
    
    if not backend_started:
        print("\n⚠️  Backend not started. Running in export-only mode.")
        print("   Start the backend manually with:")
        print("   cd backend && uvicorn main:app --reload")
    
    # Run autonomous discovery loop
    try:
        desktop.autonomous_discovery_loop()
    except KeyboardInterrupt:
        pass
    finally:
        desktop.cleanup()


if __name__ == "__main__":
    main()
