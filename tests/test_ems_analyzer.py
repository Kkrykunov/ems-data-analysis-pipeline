#!/usr/bin/env python3
"""
Unit tests for EMS Analyzer module.
"""

import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add src directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ems_analyzer import EMSAnalyzer


class TestEMSAnalyzer(unittest.TestCase):
    """Test cases for EMSAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EMSAnalyzer()
        
        # Create test DataFrame with EMS data
        self.test_data = pd.DataFrame({
            'Время_вызова_minutes': [480, 720, 1200, 60, 300],  # Various times
            'response_time_minutes': [15, 25, 35, 10, 20],
            'Район': ['Central', 'North', 'South', 'Central', 'North'],
            'Диагноз': ['Cardiac', 'Respiratory', 'Trauma', 'Cardiac', 'Neurological'],
            'Адрес': ['St. A', 'St. B', 'St. C', 'St. D', 'St. E']
        })
    
    def test_initialization(self):
        """Test EMSAnalyzer initialization."""
        self.assertIsInstance(self.analyzer, EMSAnalyzer)
    
    def test_analyze_response_times_valid_data(self):
        """Test response time analysis with valid data."""
        result = self.analyzer.analyze_response_times(self.test_data, 'response_time_minutes')
        
        self.assertIsInstance(result, dict)
        self.assertIn('mean', result)
        self.assertIn('median', result)
        self.assertIn('std', result)
        self.assertIn('min', result)
        self.assertIn('max', result)
        
        # Check calculated values
        expected_mean = self.test_data['response_time_minutes'].mean()
        self.assertAlmostEqual(result['mean'], expected_mean, places=2)
    
    def test_analyze_response_times_invalid_column(self):
        """Test response time analysis with invalid column."""
        result = self.analyzer.analyze_response_times(self.test_data, 'nonexistent_column')
        self.assertIsNone(result)
    
    def test_analyze_response_times_empty_dataframe(self):
        """Test response time analysis with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = self.analyzer.analyze_response_times(empty_df, 'response_time_minutes')
        self.assertIsNone(result)
    
    def test_analyze_disease_distribution_valid_data(self):
        """Test disease distribution analysis with valid data."""
        result = self.analyzer.analyze_disease_distribution(self.test_data, 'Диагноз')
        
        self.assertIsInstance(result, dict)
        self.assertIn('distribution', result)
        self.assertIn('total_cases', result)
        self.assertIn('unique_diseases', result)
        
        # Check specific values
        self.assertEqual(result['total_cases'], 5)
        self.assertEqual(result['unique_diseases'], 4)  # Cardiac appears twice
        
        # Check that Cardiac has count of 2
        distribution = result['distribution']
        self.assertEqual(distribution['Cardiac'], 2)
    
    def test_analyze_disease_distribution_invalid_column(self):
        """Test disease distribution analysis with invalid column."""
        result = self.analyzer.analyze_disease_distribution(self.test_data, 'nonexistent_column')
        self.assertIsNone(result)
    
    def test_analyze_temporal_patterns_valid_data(self):
        """Test temporal pattern analysis with valid data."""
        result = self.analyzer.analyze_temporal_patterns(self.test_data, 'Время_вызова_minutes')
        
        self.assertIsInstance(result, dict)
        self.assertIn('hourly_distribution', result)
        self.assertIn('peak_hours', result)
        self.assertIn('low_hours', result)
        
        # Check that we have some hourly distribution data
        hourly_dist = result['hourly_distribution']
        self.assertIsInstance(hourly_dist, dict)
        self.assertTrue(len(hourly_dist) > 0)
    
    def test_analyze_temporal_patterns_invalid_column(self):
        """Test temporal pattern analysis with invalid column."""
        result = self.analyzer.analyze_temporal_patterns(self.test_data, 'nonexistent_column')
        self.assertIsNone(result)
    
    def test_analyze_workload_valid_data(self):
        """Test workload analysis with valid data."""
        result = self.analyzer.analyze_workload(self.test_data)
        
        self.assertIsInstance(result, dict)
        self.assertIn('total_calls', result)
        self.assertIn('calls_by_district', result)
        self.assertIn('average_response_time', result)
        
        # Check calculated values
        self.assertEqual(result['total_calls'], 5)
        
        if 'response_time_minutes' in self.test_data.columns:
            expected_avg = self.test_data['response_time_minutes'].mean()
            self.assertAlmostEqual(result['average_response_time'], expected_avg, places=2)
    
    def test_analyze_workload_empty_dataframe(self):
        """Test workload analysis with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = self.analyzer.analyze_workload(empty_df)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result['total_calls'], 0)
    
    def test_analyze_territorial_distribution_valid_data(self):
        """Test territorial distribution analysis with valid data."""
        result = self.analyzer.analyze_territorial_distribution(self.test_data, 'Район')
        
        self.assertIsInstance(result, dict)
        self.assertIn('distribution', result)
        self.assertIn('total_areas', result)
        self.assertIn('calls_per_area', result)
        
        # Check specific values
        distribution = result['distribution']
        self.assertEqual(distribution['Central'], 2)  # Central appears twice
        self.assertEqual(distribution['North'], 2)    # North appears twice
        self.assertEqual(distribution['South'], 1)    # South appears once
        
        self.assertEqual(result['total_areas'], 3)    # 3 unique areas
    
    def test_analyze_territorial_distribution_invalid_column(self):
        """Test territorial distribution analysis with invalid column."""
        result = self.analyzer.analyze_territorial_distribution(self.test_data, 'nonexistent_column')
        self.assertIsNone(result)
    
    def test_analyze_response_times_with_missing_values(self):
        """Test response time analysis with missing values."""
        # Add some NaN values
        data_with_nan = self.test_data.copy()
        data_with_nan.loc[0, 'response_time_minutes'] = np.nan
        data_with_nan.loc[1, 'response_time_minutes'] = np.nan
        
        result = self.analyzer.analyze_response_times(data_with_nan, 'response_time_minutes')
        
        self.assertIsInstance(result, dict)
        # Should still work with remaining valid values
        self.assertIn('mean', result)
        # Mean should be calculated from non-NaN values only
        expected_mean = data_with_nan['response_time_minutes'].dropna().mean()
        self.assertAlmostEqual(result['mean'], expected_mean, places=2)
    
    def test_analyze_temporal_patterns_edge_cases(self):
        """Test temporal pattern analysis with edge cases."""
        # Test with midnight and end-of-day times
        edge_data = pd.DataFrame({
            'Время_вызова_minutes': [0, 1439, 720, 0, 1439]  # Midnight, 23:59, noon
        })
        
        result = self.analyzer.analyze_temporal_patterns(edge_data, 'Время_вызова_minutes')
        
        self.assertIsInstance(result, dict)
        self.assertIn('hourly_distribution', result)
        
        # Check that hour 0 and hour 23 are represented
        hourly_dist = result['hourly_distribution']
        self.assertIn(0, hourly_dist)   # Midnight hour
        self.assertIn(23, hourly_dist)  # 23:59 hour
        self.assertIn(12, hourly_dist)  # Noon hour


class TestEMSAnalyzerIntegration(unittest.TestCase):
    """Integration tests for EMSAnalyzer with realistic data scenarios."""
    
    def setUp(self):
        """Set up test fixtures with more realistic data."""
        self.analyzer = EMSAnalyzer()
        
        # Create larger, more realistic test dataset
        np.random.seed(42)  # For reproducible results
        n_records = 100
        
        self.realistic_data = pd.DataFrame({
            'Время_вызова_minutes': np.random.randint(0, 1440, n_records),
            'response_time_minutes': np.random.normal(20, 8, n_records).clip(5, 60),
            'Район': np.random.choice(['Central', 'North', 'South', 'East', 'West'], n_records),
            'Диагноз': np.random.choice(['Cardiac', 'Respiratory', 'Trauma', 'Neurological', 'Other'], n_records),
            'Адрес': [f"Address {i}" for i in range(n_records)]
        })
    
    def test_comprehensive_analysis(self):
        """Test running all analysis methods on realistic data."""
        # Response time analysis
        response_result = self.analyzer.analyze_response_times(
            self.realistic_data, 'response_time_minutes'
        )
        self.assertIsNotNone(response_result)
        
        # Disease distribution analysis
        disease_result = self.analyzer.analyze_disease_distribution(
            self.realistic_data, 'Диагноз'
        )
        self.assertIsNotNone(disease_result)
        
        # Temporal patterns analysis
        temporal_result = self.analyzer.analyze_temporal_patterns(
            self.realistic_data, 'Время_вызова_minutes'
        )
        self.assertIsNotNone(temporal_result)
        
        # Workload analysis
        workload_result = self.analyzer.analyze_workload(self.realistic_data)
        self.assertIsNotNone(workload_result)
        
        # Territorial distribution analysis
        territorial_result = self.analyzer.analyze_territorial_distribution(
            self.realistic_data, 'Район'
        )
        self.assertIsNotNone(territorial_result)
        
        # Verify that all analyses returned meaningful results
        self.assertEqual(workload_result['total_calls'], 100)
        self.assertEqual(territorial_result['total_areas'], 5)
        self.assertTrue(response_result['mean'] > 0)


if __name__ == '__main__':
    unittest.main()