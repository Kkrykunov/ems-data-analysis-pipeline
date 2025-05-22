#!/usr/bin/env python3
"""
Unit tests for EMS Analysis Pipeline main module.
"""

import unittest
import tempfile
import shutil
import os
import pandas as pd
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import EMSAnalysisPipeline, main


class TestEMSAnalysisPipeline(unittest.TestCase):
    """Test cases for EMSAnalysisPipeline class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "test_data.csv")
        self.output_dir = os.path.join(self.temp_dir, "output")
        
        # Create test CSV data
        self.test_data = pd.DataFrame({
            'Время_вызова': ['08:30:00', '14:45:30', '23:15:45', '12:00:00', '18:30:15'],
            'Время_прибытия': ['08:45:00', '15:00:30', '23:30:45', '12:15:00', '18:45:15'],
            'Район': ['Central', 'North', 'South', 'Central', 'North'],
            'Диагноз': ['Cardiac', 'Respiratory', 'Trauma', 'Cardiac', 'Neurological'],
            'Адрес': ['St. A', 'St. B', 'St. C', 'St. D', 'St. E']
        })
        
        # Save test data to file
        self.test_data.to_csv(self.data_file, index=False, encoding='utf-8')
        
        # Create pipeline instance
        self.pipeline = EMSAnalysisPipeline(self.data_file, self.output_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary directory
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test EMSAnalysisPipeline initialization."""
        self.assertIsInstance(self.pipeline, EMSAnalysisPipeline)
        self.assertEqual(str(self.pipeline.data_file_path), self.data_file)
        self.assertEqual(str(self.pipeline.output_dir), self.output_dir)
        self.assertTrue(os.path.exists(self.output_dir))
    
    def test_load_data_success(self):
        """Test successful data loading."""
        result = self.pipeline.load_data()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.pipeline.raw_data)
        self.assertIsInstance(self.pipeline.raw_data, pd.DataFrame)
        self.assertEqual(len(self.pipeline.raw_data), 5)
    
    def test_load_data_nonexistent_file(self):
        """Test data loading with nonexistent file."""
        # Create pipeline with nonexistent file
        pipeline = EMSAnalysisPipeline("nonexistent.csv", self.output_dir)
        result = pipeline.load_data()
        
        self.assertFalse(result)
        self.assertIsNone(pipeline.raw_data)
    
    def test_process_time_data_success(self):
        """Test successful time data processing."""
        # First load data
        self.pipeline.load_data()
        
        # Then process time data
        result = self.pipeline.process_time_data()
        
        self.assertTrue(result)
        self.assertIsNotNone(self.pipeline.processed_data)
        
        # Check that time columns were processed
        expected_columns = [
            'Время_вызова_minutes',
            'Время_прибытия_minutes',
            'response_time_minutes'
        ]
        
        for col in expected_columns:
            self.assertIn(col, self.pipeline.processed_data.columns)
    
    def test_process_time_data_without_loading(self):
        """Test time data processing without loading data first."""
        result = self.pipeline.process_time_data()
        
        self.assertFalse(result)
    
    def test_run_analysis_success(self):
        """Test successful analysis execution."""
        # Load and process data first
        self.pipeline.load_data()
        self.pipeline.process_time_data()
        
        # Run analysis
        result = self.pipeline.run_analysis()
        
        self.assertTrue(result)
        self.assertIsInstance(self.pipeline.analysis_results, dict)
        self.assertTrue(len(self.pipeline.analysis_results) > 0)
    
    def test_run_analysis_without_processing(self):
        """Test analysis execution without processing data first."""
        result = self.pipeline.run_analysis()
        
        self.assertFalse(result)
    
    @patch('matplotlib.pyplot.figure')
    def test_generate_visualizations_success(self, mock_figure):
        """Test successful visualization generation."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Load and process data first
        self.pipeline.load_data()
        self.pipeline.process_time_data()
        
        # Generate visualizations
        result = self.pipeline.generate_visualizations()
        
        self.assertTrue(result)
        
        # Check that visualization directory was created
        viz_dir = Path(self.output_dir) / "visualizations"
        self.assertTrue(viz_dir.exists())
    
    def test_generate_visualizations_without_processing(self):
        """Test visualization generation without processing data first."""
        result = self.pipeline.generate_visualizations()
        
        self.assertFalse(result)
    
    def test_generate_reports_success(self):
        """Test successful report generation."""
        # Load, process, and analyze data first
        self.pipeline.load_data()
        self.pipeline.process_time_data()
        self.pipeline.run_analysis()
        
        # Generate reports
        result = self.pipeline.generate_reports()
        
        self.assertTrue(result)
        
        # Check that reports directory was created
        reports_dir = Path(self.output_dir) / "reports"
        self.assertTrue(reports_dir.exists())
        
        # Check that specific report files were created
        expected_files = [
            "analysis_summary.txt",
            "processed_data.csv",
            "analysis_results.json"
        ]
        
        for filename in expected_files:
            file_path = reports_dir / filename
            self.assertTrue(file_path.exists(), f"Report file {filename} was not created")
    
    def test_generate_reports_without_analysis(self):
        """Test report generation without running analysis first."""
        result = self.pipeline.generate_reports()
        
        # Should still succeed but with minimal data
        self.assertTrue(result)
    
    @patch('matplotlib.pyplot.figure')
    def test_run_full_pipeline_success(self, mock_figure):
        """Test successful full pipeline execution."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.pipeline.run_full_pipeline()
        
        self.assertTrue(result)
        
        # Check that all outputs were created
        self.assertIsNotNone(self.pipeline.raw_data)
        self.assertIsNotNone(self.pipeline.processed_data)
        self.assertTrue(len(self.pipeline.analysis_results) > 0)
        
        # Check output directories
        viz_dir = Path(self.output_dir) / "visualizations"
        reports_dir = Path(self.output_dir) / "reports"
        self.assertTrue(viz_dir.exists())
        self.assertTrue(reports_dir.exists())
    
    def test_run_full_pipeline_with_invalid_data(self):
        """Test full pipeline execution with invalid data file."""
        # Create pipeline with nonexistent file
        pipeline = EMSAnalysisPipeline("nonexistent.csv", self.output_dir)
        
        result = pipeline.run_full_pipeline()
        
        self.assertFalse(result)
    
    def test_logging_configuration(self):
        """Test that logging is configured properly."""
        self.assertIsNotNone(self.pipeline.logger)
        
        # Check that log file is created
        log_file = Path(self.output_dir) / "ems_analysis.log"
        
        # Generate some log messages
        self.pipeline.logger.info("Test log message")
        
        # Log file should exist (though it might be empty due to buffering)
        self.assertTrue(log_file.exists())


class TestMainFunction(unittest.TestCase):
    """Test cases for the main function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_data.csv")
        
        # Create test data
        test_data = pd.DataFrame({
            'Время_вызова': ['08:30:00', '14:45:30'],
            'Время_прибытия': ['08:45:00', '15:00:30'],
            'Район': ['Central', 'North'],
            'Диагноз': ['Cardiac', 'Respiratory']
        })
        test_data.to_csv(self.test_data_file, index=False)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('sys.argv', ['main.py'])
    @patch('matplotlib.pyplot.figure')
    @patch('pathlib.Path.glob')
    @patch('pathlib.Path.exists')
    def test_main_function_with_data_file(self, mock_exists, mock_glob, mock_figure):
        """Test main function execution with available data file."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Mock file system interactions
        mock_exists.return_value = True
        mock_glob.return_value = [Path(self.test_data_file)]
        
        # Mock the pipeline to avoid actual file operations
        with patch('main.EMSAnalysisPipeline') as mock_pipeline_class:
            mock_pipeline = MagicMock()
            mock_pipeline.run_full_pipeline.return_value = True
            mock_pipeline_class.return_value = mock_pipeline
            
            result = main()
            
            self.assertTrue(result)
            mock_pipeline.run_full_pipeline.assert_called_once()
    
    @patch('sys.argv', ['main.py'])
    @patch('pathlib.Path.exists')
    def test_main_function_without_data_file(self, mock_exists):
        """Test main function execution without available data file."""
        # Mock no data files available
        mock_exists.return_value = False
        
        result = main()
        
        self.assertFalse(result)
    
    @patch('sys.argv', ['main.py'])
    @patch('matplotlib.pyplot.figure')
    @patch('pathlib.Path.glob')
    @patch('pathlib.Path.exists')
    def test_main_function_pipeline_failure(self, mock_exists, mock_glob, mock_figure):
        """Test main function execution when pipeline fails."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Mock file system interactions
        mock_exists.return_value = True
        mock_glob.return_value = [Path(self.test_data_file)]
        
        # Mock the pipeline to simulate failure
        with patch('main.EMSAnalysisPipeline') as mock_pipeline_class:
            mock_pipeline = MagicMock()
            mock_pipeline.run_full_pipeline.return_value = False
            mock_pipeline_class.return_value = mock_pipeline
            
            result = main()
            
            self.assertFalse(result)
            mock_pipeline.run_full_pipeline.assert_called_once()


class TestEMSAnalysisPipelineIntegration(unittest.TestCase):
    """Integration tests for the complete EMS Analysis Pipeline."""
    
    def setUp(self):
        """Set up test fixtures for integration testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.temp_dir, "integration_test_data.csv")
        self.output_dir = os.path.join(self.temp_dir, "output")
        
        # Create more comprehensive test data
        import numpy as np
        np.random.seed(42)
        
        n_records = 20
        test_data = pd.DataFrame({
            'Время_вызова': [f"{hour:02d}:{minute:02d}:{second:02d}" 
                           for hour, minute, second in zip(
                               np.random.randint(0, 24, n_records),
                               np.random.randint(0, 60, n_records),
                               np.random.randint(0, 60, n_records)
                           )],
            'Время_прибытия': [f"{hour:02d}:{minute:02d}:{second:02d}" 
                             for hour, minute, second in zip(
                                 np.random.randint(0, 24, n_records),
                                 np.random.randint(0, 60, n_records),
                                 np.random.randint(0, 60, n_records)
                             )],
            'Район': np.random.choice(['Central', 'North', 'South', 'East', 'West'], n_records),
            'Диагноз': np.random.choice(['Cardiac', 'Respiratory', 'Trauma', 'Neurological', 'Other'], n_records),
            'Адрес': [f"Street {i}, City" for i in range(n_records)]
        })
        
        test_data.to_csv(self.data_file, index=False, encoding='utf-8')
        
        self.pipeline = EMSAnalysisPipeline(self.data_file, self.output_dir)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('matplotlib.pyplot.figure')
    def test_complete_pipeline_integration(self, mock_figure):
        """Test complete pipeline execution with all steps."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Execute complete pipeline
        result = self.pipeline.run_full_pipeline()
        
        self.assertTrue(result)
        
        # Verify all pipeline steps completed successfully
        self.assertIsNotNone(self.pipeline.raw_data)
        self.assertIsNotNone(self.pipeline.processed_data)
        self.assertIsInstance(self.pipeline.analysis_results, dict)
        self.assertTrue(len(self.pipeline.analysis_results) > 0)
        
        # Verify output structure
        output_path = Path(self.output_dir)
        self.assertTrue(output_path.exists())
        
        # Check reports
        reports_dir = output_path / "reports"
        self.assertTrue(reports_dir.exists())
        self.assertTrue((reports_dir / "analysis_summary.txt").exists())
        self.assertTrue((reports_dir / "processed_data.csv").exists())
        self.assertTrue((reports_dir / "analysis_results.json").exists())
        
        # Check visualizations
        viz_dir = output_path / "visualizations"
        self.assertTrue(viz_dir.exists())
        
        # Check log file
        log_file = output_path / "ems_analysis.log"
        self.assertTrue(log_file.exists())
        
        # Verify processed data has expected columns
        expected_columns = [
            'Время_вызова_minutes',
            'Время_прибытия_minutes',
            'response_time_minutes'
        ]
        
        for col in expected_columns:
            self.assertIn(col, self.pipeline.processed_data.columns)
        
        # Verify analysis results contain expected keys
        expected_analyses = [
            'response_times',
            'workload'
        ]
        
        for analysis in expected_analyses:
            self.assertIn(analysis, self.pipeline.analysis_results)


if __name__ == '__main__':
    unittest.main()