#!/usr/bin/env python3
"""
Unit tests for EMS Visualizer module.
"""

import unittest
import pandas as pd
import numpy as np
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from visualizer import EMSVisualizer


class TestEMSVisualizer(unittest.TestCase):
    """Test cases for EMSVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = EMSVisualizer()
        
        # Create test DataFrame with EMS data
        self.test_data = pd.DataFrame({
            'Время_вызова_minutes': [480, 720, 1200, 60, 300],  # Various times
            'response_time_minutes': [15, 25, 35, 10, 20],
            'Район': ['Central', 'North', 'South', 'Central', 'North'],
            'Диагноз': ['Cardiac', 'Respiratory', 'Trauma', 'Cardiac', 'Neurological'],
            'Адрес': ['St. A', 'St. B', 'St. C', 'St. D', 'St. E']
        })
    
    def test_initialization(self):
        """Test EMSVisualizer initialization."""
        self.assertIsInstance(self.visualizer, EMSVisualizer)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_response_time_distribution(self, mock_figure, mock_show):
        """Test response time distribution plotting."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.plot_response_time_distribution(
            self.test_data, 'response_time_minutes'
        )
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_response_time_distribution_invalid_column(self, mock_figure, mock_show):
        """Test response time distribution plotting with invalid column."""
        result = self.visualizer.plot_response_time_distribution(
            self.test_data, 'nonexistent_column'
        )
        
        # Should return None for invalid column
        self.assertIsNone(result)
        mock_figure.assert_not_called()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_disease_distribution(self, mock_figure, mock_show):
        """Test disease distribution plotting."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.plot_disease_distribution(
            self.test_data, 'Диагноз'
        )
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_disease_distribution_invalid_column(self, mock_figure, mock_show):
        """Test disease distribution plotting with invalid column."""
        result = self.visualizer.plot_disease_distribution(
            self.test_data, 'nonexistent_column'
        )
        
        # Should return None for invalid column
        self.assertIsNone(result)
        mock_figure.assert_not_called()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_hourly_call_volume(self, mock_figure, mock_show):
        """Test hourly call volume plotting."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.plot_hourly_call_volume(
            self.test_data, 'Время_вызова_minutes'
        )
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_hourly_call_volume_invalid_column(self, mock_figure, mock_show):
        """Test hourly call volume plotting with invalid column."""
        result = self.visualizer.plot_hourly_call_volume(
            self.test_data, 'nonexistent_column'
        )
        
        # Should return None for invalid column
        self.assertIsNone(result)
        mock_figure.assert_not_called()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_response_time_by_hour(self, mock_figure, mock_show):
        """Test response time by hour plotting."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.plot_response_time_by_hour(
            self.test_data, 'response_time_minutes', 'Время_вызова_minutes'
        )
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_response_time_by_hour_invalid_columns(self, mock_figure, mock_show):
        """Test response time by hour plotting with invalid columns."""
        result = self.visualizer.plot_response_time_by_hour(
            self.test_data, 'nonexistent_column', 'Время_вызова_minutes'
        )
        
        # Should return None for invalid column
        self.assertIsNone(result)
        mock_figure.assert_not_called()
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_create_dashboard(self, mock_figure, mock_show):
        """Test dashboard creation."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.create_dashboard(self.test_data)
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    def test_create_dashboard_empty_dataframe(self):
        """Test dashboard creation with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = self.visualizer.create_dashboard(empty_df)
        
        # Should return None for empty DataFrame
        self.assertIsNone(result)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_territorial_distribution(self, mock_figure, mock_show):
        """Test territorial distribution plotting."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        result = self.visualizer.plot_territorial_distribution(
            self.test_data, 'Район'
        )
        
        # Verify that matplotlib functions were called
        mock_figure.assert_called_once()
        self.assertEqual(result, mock_fig)
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_plot_territorial_distribution_invalid_column(self, mock_figure, mock_show):
        """Test territorial distribution plotting with invalid column."""
        result = self.visualizer.plot_territorial_distribution(
            self.test_data, 'nonexistent_column'
        )
        
        # Should return None for invalid column
        self.assertIsNone(result)
        mock_figure.assert_not_called()


class TestEMSVisualizerIntegration(unittest.TestCase):
    """Integration tests for EMSVisualizer with realistic data scenarios."""
    
    def setUp(self):
        """Set up test fixtures with more realistic data."""
        self.visualizer = EMSVisualizer()
        
        # Create larger, more realistic test dataset
        np.random.seed(42)  # For reproducible results
        n_records = 50  # Smaller for faster testing
        
        self.realistic_data = pd.DataFrame({
            'Время_вызова_minutes': np.random.randint(0, 1440, n_records),
            'response_time_minutes': np.random.normal(20, 8, n_records).clip(5, 60),
            'Район': np.random.choice(['Central', 'North', 'South', 'East', 'West'], n_records),
            'Диагноз': np.random.choice(['Cardiac', 'Respiratory', 'Trauma', 'Neurological', 'Other'], n_records),
            'Адрес': [f"Address {i}" for i in range(n_records)]
        })
    
    @patch('matplotlib.pyplot.show')
    @patch('matplotlib.pyplot.figure')
    def test_comprehensive_visualization(self, mock_figure, mock_show):
        """Test creating all visualization types with realistic data."""
        mock_fig = MagicMock()
        mock_figure.return_value = mock_fig
        
        # Test response time distribution
        result1 = self.visualizer.plot_response_time_distribution(
            self.realistic_data, 'response_time_minutes'
        )
        self.assertIsNotNone(result1)
        
        # Test disease distribution
        result2 = self.visualizer.plot_disease_distribution(
            self.realistic_data, 'Диагноз'
        )
        self.assertIsNotNone(result2)
        
        # Test hourly call volume
        result3 = self.visualizer.plot_hourly_call_volume(
            self.realistic_data, 'Время_вызова_minutes'
        )
        self.assertIsNotNone(result3)
        
        # Test response time by hour
        result4 = self.visualizer.plot_response_time_by_hour(
            self.realistic_data, 'response_time_minutes', 'Время_вызова_minutes'
        )
        self.assertIsNotNone(result4)
        
        # Test territorial distribution
        result5 = self.visualizer.plot_territorial_distribution(
            self.realistic_data, 'Район'
        )
        self.assertIsNotNone(result5)
        
        # Test dashboard creation
        dashboard_result = self.visualizer.create_dashboard(self.realistic_data)
        self.assertIsNotNone(dashboard_result)
        
        # Verify that matplotlib figure was called multiple times
        self.assertTrue(mock_figure.call_count >= 6)  # At least 6 plots created
    
    def test_data_validation_in_visualizations(self):
        """Test that visualizations handle data validation properly."""
        # Test with data containing NaN values
        data_with_nan = self.realistic_data.copy()
        data_with_nan.loc[0:5, 'response_time_minutes'] = np.nan
        
        # All visualization methods should handle NaN values gracefully
        with patch('matplotlib.pyplot.figure') as mock_figure:
            mock_fig = MagicMock()
            mock_figure.return_value = mock_fig
            
            # These should not raise exceptions
            self.visualizer.plot_response_time_distribution(
                data_with_nan, 'response_time_minutes'
            )
            self.visualizer.plot_response_time_by_hour(
                data_with_nan, 'response_time_minutes', 'Время_вызова_minutes'
            )
            self.visualizer.create_dashboard(data_with_nan)
    
    def test_visualization_with_minimal_data(self):
        """Test visualizations with minimal data sets."""
        # Test with just 2 data points
        minimal_data = pd.DataFrame({
            'Время_вызова_minutes': [480, 720],
            'response_time_minutes': [15, 25],
            'Район': ['Central', 'North'],
            'Диагноз': ['Cardiac', 'Respiratory']
        })
        
        with patch('matplotlib.pyplot.figure') as mock_figure:
            mock_fig = MagicMock()
            mock_figure.return_value = mock_fig
            
            # All visualization methods should work with minimal data
            result1 = self.visualizer.plot_response_time_distribution(
                minimal_data, 'response_time_minutes'
            )
            self.assertIsNotNone(result1)
            
            result2 = self.visualizer.plot_disease_distribution(
                minimal_data, 'Диагноз'
            )
            self.assertIsNotNone(result2)
            
            result3 = self.visualizer.create_dashboard(minimal_data)
            self.assertIsNotNone(result3)


if __name__ == '__main__':
    unittest.main()