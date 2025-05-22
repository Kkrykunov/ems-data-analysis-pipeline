#!/usr/bin/env python3
"""
EMS Analysis Pipeline - Main Orchestration Module

This module coordinates the complete Emergency Medical Services data analysis workflow,
integrating data loading, time processing, analysis, and visualization components.
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import pandas as pd

from data_loader import EMSDataLoader
from time_processor import TimeProcessor
from ems_analyzer import EMSAnalyzer
from visualizer import EMSVisualizer


class EMSAnalysisPipeline:
    """
    Complete EMS analysis pipeline orchestrator.
    
    Coordinates the entire workflow from raw data to final reports and visualizations.
    """
    
    def __init__(self, data_file_path: str, output_dir: str = "output"):
        """
        Initialize the EMS analysis pipeline.
        
        Args:
            data_file_path: Path to the EMS data CSV file
            output_dir: Directory for saving outputs
        """
        self.data_file_path = Path(data_file_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.data_loader = EMSDataLoader()
        self.time_processor = TimeProcessor()
        self.analyzer = EMSAnalyzer()
        self.visualizer = EMSVisualizer()
        
        # Setup logging
        self._setup_logging()
        
        # Pipeline state
        self.raw_data = None
        self.processed_data = None
        self.analysis_results = {}
        
    def _setup_logging(self):
        """Configure logging for the pipeline."""
        log_file = self.output_dir / "ems_analysis.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_data(self) -> bool:
        """
        Load and validate EMS data.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info(f"Loading data from {self.data_file_path}")
            self.raw_data = self.data_loader.load_data(str(self.data_file_path))
            
            if self.raw_data is not None:
                self.logger.info(f"Successfully loaded {len(self.raw_data)} records")
                return True
            else:
                self.logger.error("Failed to load data")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
            return False
    
    def process_time_data(self) -> bool:
        """
        Process and standardize time-related columns.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Processing time data")
            
            if self.raw_data is None:
                raise ValueError("No data loaded. Call load_data() first.")
            
            # Create a copy for processing
            self.processed_data = self.raw_data.copy()
            
            # Process time columns if they exist
            time_columns = ['Время_вызова', 'Время_прибытия', 'Время_завершения']
            existing_time_cols = [col for col in time_columns if col in self.processed_data.columns]
            
            for col in existing_time_cols:
                self.logger.info(f"Processing time column: {col}")
                standardized_times = []
                
                for time_str in self.processed_data[col]:
                    if pd.notna(time_str):
                        standardized = self.time_processor.standardize_time_format(str(time_str))
                        minutes = self.time_processor.time_to_minutes(standardized)
                        standardized_times.append(minutes)
                    else:
                        standardized_times.append(None)
                
                self.processed_data[f"{col}_minutes"] = standardized_times
            
            # Calculate response times if call and arrival times exist
            if 'Время_вызова_minutes' in self.processed_data.columns and 'Время_прибытия_minutes' in self.processed_data.columns:
                self.logger.info("Calculating response times")
                response_times = []
                
                for _, row in self.processed_data.iterrows():
                    call_time = row.get('Время_вызова_minutes')
                    arrival_time = row.get('Время_прибытия_minutes')
                    
                    if pd.notna(call_time) and pd.notna(arrival_time):
                        response_time = self.time_processor.calculate_response_time(call_time, arrival_time)
                        response_times.append(response_time)
                    else:
                        response_times.append(None)
                
                self.processed_data['response_time_minutes'] = response_times
            
            self.logger.info("Time processing completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error processing time data: {str(e)}")
            return False
    
    def run_analysis(self) -> bool:
        """
        Execute comprehensive EMS data analysis.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Running comprehensive EMS analysis")
            
            if self.processed_data is None:
                raise ValueError("No processed data available. Run process_time_data() first.")
            
            # Response time analysis
            if 'response_time_minutes' in self.processed_data.columns:
                self.logger.info("Analyzing response times")
                self.analysis_results['response_times'] = self.analyzer.analyze_response_times(
                    self.processed_data, 'response_time_minutes'
                )
            
            # Disease distribution analysis
            disease_columns = [col for col in self.processed_data.columns 
                             if any(keyword in col.lower() for keyword in ['диагноз', 'болезнь', 'заболевание', 'disease'])]
            
            if disease_columns:
                self.logger.info("Analyzing disease distribution")
                for col in disease_columns:
                    self.analysis_results[f'diseases_{col}'] = self.analyzer.analyze_disease_distribution(
                        self.processed_data, col
                    )
            
            # Temporal patterns analysis
            if 'Время_вызова_minutes' in self.processed_data.columns:
                self.logger.info("Analyzing temporal patterns")
                self.analysis_results['temporal_patterns'] = self.analyzer.analyze_temporal_patterns(
                    self.processed_data, 'Время_вызова_minutes'
                )
            
            # Workload analysis
            self.logger.info("Analyzing workload patterns")
            self.analysis_results['workload'] = self.analyzer.analyze_workload(self.processed_data)
            
            # Territorial analysis if location data exists
            location_columns = [col for col in self.processed_data.columns 
                              if any(keyword in col.lower() for keyword in ['адрес', 'район', 'территория', 'location', 'address'])]
            
            if location_columns:
                self.logger.info("Analyzing territorial distribution")
                for col in location_columns:
                    self.analysis_results[f'territorial_{col}'] = self.analyzer.analyze_territorial_distribution(
                        self.processed_data, col
                    )
            
            self.logger.info("Analysis completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during analysis: {str(e)}")
            return False
    
    def generate_visualizations(self) -> bool:
        """
        Generate comprehensive visualizations and save to output directory.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Generating visualizations")
            
            if self.processed_data is None:
                raise ValueError("No processed data available for visualization.")
            
            viz_dir = self.output_dir / "visualizations"
            viz_dir.mkdir(exist_ok=True)
            
            # Response time visualizations
            if 'response_time_minutes' in self.processed_data.columns:
                self.logger.info("Creating response time visualizations")
                fig = self.visualizer.plot_response_time_distribution(
                    self.processed_data, 'response_time_minutes'
                )
                fig.savefig(viz_dir / "response_time_distribution.png", dpi=300, bbox_inches='tight')
                
                fig = self.visualizer.plot_response_time_by_hour(
                    self.processed_data, 'response_time_minutes', 'Время_вызова_minutes'
                )
                fig.savefig(viz_dir / "response_time_by_hour.png", dpi=300, bbox_inches='tight')
            
            # Disease distribution visualizations
            disease_columns = [col for col in self.processed_data.columns 
                             if any(keyword in col.lower() for keyword in ['диагноз', 'болезнь', 'заболевание'])]
            
            for col in disease_columns:
                if col in self.processed_data.columns:
                    self.logger.info(f"Creating disease distribution visualization for {col}")
                    fig = self.visualizer.plot_disease_distribution(self.processed_data, col)
                    fig.savefig(viz_dir / f"disease_distribution_{col}.png", dpi=300, bbox_inches='tight')
            
            # Temporal patterns visualization
            if 'Время_вызова_minutes' in self.processed_data.columns:
                self.logger.info("Creating temporal patterns visualization")
                fig = self.visualizer.plot_hourly_call_volume(
                    self.processed_data, 'Время_вызова_minutes'
                )
                fig.savefig(viz_dir / "hourly_call_volume.png", dpi=300, bbox_inches='tight')
            
            # Create comprehensive dashboard
            self.logger.info("Creating comprehensive dashboard")
            dashboard_fig = self.visualizer.create_dashboard(self.processed_data)
            dashboard_fig.savefig(viz_dir / "ems_dashboard.png", dpi=300, bbox_inches='tight')
            
            self.logger.info("Visualizations generated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating visualizations: {str(e)}")
            return False
    
    def generate_reports(self) -> bool:
        """
        Generate comprehensive analysis reports.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.logger.info("Generating analysis reports")
            
            reports_dir = self.output_dir / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            # Generate summary report
            summary_file = reports_dir / "analysis_summary.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write("EMS Data Analysis Summary Report\n")
                f.write("=" * 50 + "\n\n")
                
                if self.processed_data is not None:
                    f.write(f"Total Records: {len(self.processed_data)}\n")
                    f.write(f"Data Columns: {len(self.processed_data.columns)}\n\n")
                    
                    # Data quality summary
                    f.write("Data Quality Summary:\n")
                    f.write("-" * 20 + "\n")
                    missing_data = self.processed_data.isnull().sum()
                    for col, missing_count in missing_data.items():
                        if missing_count > 0:
                            percentage = (missing_count / len(self.processed_data)) * 100
                            f.write(f"{col}: {missing_count} missing ({percentage:.1f}%)\n")
                    f.write("\n")
                
                # Analysis results summary
                if self.analysis_results:
                    f.write("Analysis Results Summary:\n")
                    f.write("-" * 25 + "\n")
                    for analysis_type, results in self.analysis_results.items():
                        f.write(f"\n{analysis_type.upper()}:\n")
                        if isinstance(results, dict):
                            for key, value in results.items():
                                f.write(f"  {key}: {value}\n")
                        else:
                            f.write(f"  {results}\n")
            
            # Save processed data
            data_file = reports_dir / "processed_data.csv"
            if self.processed_data is not None:
                self.processed_data.to_csv(data_file, index=False, encoding='utf-8')
            
            # Save analysis results as JSON
            import json
            results_file = reports_dir / "analysis_results.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                # Convert any non-serializable objects to strings
                serializable_results = {}
                for key, value in self.analysis_results.items():
                    try:
                        json.dumps(value)  # Test if serializable
                        serializable_results[key] = value
                    except (TypeError, ValueError):
                        serializable_results[key] = str(value)
                
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            
            self.logger.info("Reports generated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            return False
    
    def run_full_pipeline(self) -> bool:
        """
        Execute the complete EMS analysis pipeline.
        
        Returns:
            bool: True if successful, False otherwise
        """
        self.logger.info("Starting full EMS analysis pipeline")
        
        steps = [
            ("Loading data", self.load_data),
            ("Processing time data", self.process_time_data),
            ("Running analysis", self.run_analysis),
            ("Generating visualizations", self.generate_visualizations),
            ("Generating reports", self.generate_reports)
        ]
        
        for step_name, step_function in steps:
            self.logger.info(f"Executing step: {step_name}")
            if not step_function():
                self.logger.error(f"Pipeline failed at step: {step_name}")
                return False
        
        self.logger.info("EMS analysis pipeline completed successfully")
        return True


def main():
    """
    Main function to execute the EMS analysis pipeline.
    """
    # Configuration
    project_root = Path(__file__).parent.parent
    data_file = project_root / "data" / "ems_data.csv"
    
    # Check if data file exists, otherwise look for any CSV in data directory
    if not data_file.exists():
        data_dir = project_root / "data"
        if data_dir.exists():
            csv_files = list(data_dir.glob("*.csv"))
            if csv_files:
                data_file = csv_files[0]
                print(f"Using data file: {data_file}")
            else:
                print("No CSV files found in data directory")
                # Try the external data directory mentioned in the requirements
                external_data_dir = Path("/mnt/c/Desktop/work for claude/google_colab/data")
                if external_data_dir.exists():
                    external_csv_files = list(external_data_dir.glob("*.csv"))
                    if external_csv_files:
                        data_file = external_csv_files[0]
                        print(f"Using external data file: {data_file}")
                    else:
                        print("No CSV files found in external data directory either")
                        return False
                else:
                    print("External data directory not found")
                    return False
        else:
            print("Data directory not found")
            return False
    
    # Initialize and run pipeline
    output_dir = project_root / "output"
    pipeline = EMSAnalysisPipeline(str(data_file), str(output_dir))
    
    success = pipeline.run_full_pipeline()
    
    if success:
        print("\n" + "="*50)
        print("EMS ANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"Output directory: {output_dir}")
        print("Generated files:")
        print("- Reports: output/reports/")
        print("- Visualizations: output/visualizations/")
        print("- Logs: output/ems_analysis.log")
    else:
        print("\n" + "="*50)
        print("EMS ANALYSIS PIPELINE FAILED")
        print("="*50)
        print("Check the log file for detailed error information")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)