#!/usr/bin/env python3
"""
Unit tests for EMS Data Loader module.
"""

import unittest
import tempfile
import os
import pandas as pd
import sys
from pathlib import Path

# Add src directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_loader import EMSDataLoader


class TestEMSDataLoader(unittest.TestCase):
    """Test cases for EMSDataLoader class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.loader = EMSDataLoader()
        
        # Create test CSV data
        self.test_data = {
            'Время_вызова': ['08:30:00', '14:45:30', '23:15:45'],
            'Время_прибытия': ['08:45:00', '15:00:30', '23:30:45'],
            'Район': ['Central', 'North', 'South'],
            'Диагноз': ['Cardiac', 'Respiratory', 'Trauma']
        }
        self.test_df = pd.DataFrame(self.test_data)
        
    def test_initialization(self):
        """Test EMSDataLoader initialization."""
        self.assertIsInstance(self.loader, EMSDataLoader)
        
    def test_detect_encoding_utf8(self):
        """Test encoding detection for UTF-8 files."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
            self.test_df.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            encoding = self.loader.detect_encoding(temp_file)
            self.assertIn(encoding.lower(), ['utf-8', 'ascii'])
        finally:
            os.unlink(temp_file)
    
    def test_detect_encoding_invalid_file(self):
        """Test encoding detection with invalid file path."""
        with self.assertRaises(FileNotFoundError):
            self.loader.detect_encoding("nonexistent_file.csv")
    
    def test_validate_data_valid(self):
        """Test data validation with valid DataFrame."""
        self.assertTrue(self.loader.validate_data(self.test_df))
    
    def test_validate_data_empty(self):
        """Test data validation with empty DataFrame."""
        empty_df = pd.DataFrame()
        self.assertFalse(self.loader.validate_data(empty_df))
    
    def test_validate_data_none(self):
        """Test data validation with None input."""
        self.assertFalse(self.loader.validate_data(None))
    
    def test_load_data_success(self):
        """Test successful data loading."""
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
            self.test_df.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            result = self.loader.load_data(temp_file)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 3)
            self.assertIn('Время_вызова', result.columns)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_nonexistent_file(self):
        """Test data loading with nonexistent file."""
        result = self.loader.load_data("nonexistent_file.csv")
        self.assertIsNone(result)
    
    def test_load_data_with_encoding_issues(self):
        """Test data loading with various encoding issues."""
        # Create a file with special characters
        special_data = pd.DataFrame({
            'Name': ['Київ', 'Львів', 'Одеса'],
            'Value': [1, 2, 3]
        })
        
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
            special_data.to_csv(f.name, index=False)
            temp_file = f.name
        
        try:
            result = self.loader.load_data(temp_file)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertEqual(len(result), 3)
        finally:
            os.unlink(temp_file)
    
    def test_load_data_with_separators(self):
        """Test data loading with different separators."""
        # Create tab-separated file
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', delete=False, suffix='.csv') as f:
            # Write tab-separated data
            f.write("Col1\tCol2\tCol3\nValue1\tValue2\tValue3\n")
            temp_file = f.name
        
        try:
            result = self.loader.load_data(temp_file)
            self.assertIsInstance(result, pd.DataFrame)
            self.assertTrue(len(result) >= 1)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main()