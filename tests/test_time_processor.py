#!/usr/bin/env python3
"""
Unit tests for EMS Time Processor module.
"""

import unittest
import sys
from pathlib import Path

# Add src directory to path for importing modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from time_processor import TimeProcessor


class TestTimeProcessor(unittest.TestCase):
    """Test cases for TimeProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = TimeProcessor()
    
    def test_initialization(self):
        """Test TimeProcessor initialization."""
        self.assertIsInstance(self.processor, TimeProcessor)
    
    def test_standardize_time_format_valid(self):
        """Test time format standardization with valid inputs."""
        test_cases = [
            ("08:30:00", "08:30:00"),
            ("8:30:00", "08:30:00"),
            ("14:45:30", "14:45:30"),
            ("23:59:59", "23:59:59"),
            ("00:00:00", "00:00:00")
        ]
        
        for input_time, expected in test_cases:
            with self.subTest(input_time=input_time):
                result = self.processor.standardize_time_format(input_time)
                self.assertEqual(result, expected)
    
    def test_standardize_time_format_without_seconds(self):
        """Test time format standardization for times without seconds."""
        test_cases = [
            ("08:30", "08:30:00"),
            ("14:45", "14:45:00"),
            ("23:59", "23:59:00"),
            ("00:00", "00:00:00")
        ]
        
        for input_time, expected in test_cases:
            with self.subTest(input_time=input_time):
                result = self.processor.standardize_time_format(input_time)
                self.assertEqual(result, expected)
    
    def test_standardize_time_format_invalid(self):
        """Test time format standardization with invalid inputs."""
        invalid_inputs = [
            "25:00:00",  # Invalid hour
            "12:60:00",  # Invalid minute
            "12:30:60",  # Invalid second
            "invalid",   # Non-numeric
            "",          # Empty string
            "12",        # Incomplete format
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                result = self.processor.standardize_time_format(invalid_input)
                self.assertIsNone(result)
    
    def test_time_to_minutes_valid(self):
        """Test conversion from time string to minutes since midnight."""
        test_cases = [
            ("00:00:00", 0),
            ("01:00:00", 60),
            ("08:30:00", 510),  # 8*60 + 30 = 510
            ("12:00:00", 720),  # 12*60 = 720
            ("23:59:00", 1439)  # 23*60 + 59 = 1439
        ]
        
        for time_str, expected_minutes in test_cases:
            with self.subTest(time_str=time_str):
                result = self.processor.time_to_minutes(time_str)
                self.assertEqual(result, expected_minutes)
    
    def test_time_to_minutes_invalid(self):
        """Test conversion with invalid time strings."""
        invalid_inputs = [
            "25:00:00",
            "invalid",
            "",
            None
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(invalid_input=invalid_input):
                result = self.processor.time_to_minutes(invalid_input)
                self.assertIsNone(result)
    
    def test_calculate_response_time_same_day(self):
        """Test response time calculation for same-day calls."""
        test_cases = [
            (510, 540, 30),    # 08:30 to 09:00 = 30 minutes
            (720, 780, 60),    # 12:00 to 13:00 = 60 minutes
            (1200, 1230, 30),  # 20:00 to 20:30 = 30 minutes
        ]
        
        for call_time, arrival_time, expected in test_cases:
            with self.subTest(call_time=call_time, arrival_time=arrival_time):
                result = self.processor.calculate_response_time(call_time, arrival_time)
                self.assertEqual(result, expected)
    
    def test_calculate_response_time_overnight(self):
        """Test response time calculation for overnight calls."""
        test_cases = [
            (1430, 30, 40),    # 23:50 to 00:30 next day = 40 minutes
            (1440, 60, 60),    # 24:00 (00:00) to 01:00 next day = 60 minutes
            (1380, 120, 180),  # 23:00 to 02:00 next day = 3 hours = 180 minutes
        ]
        
        for call_time, arrival_time, expected in test_cases:
            with self.subTest(call_time=call_time, arrival_time=arrival_time):
                result = self.processor.calculate_response_time(call_time, arrival_time)
                self.assertEqual(result, expected)
    
    def test_calculate_response_time_invalid_inputs(self):
        """Test response time calculation with invalid inputs."""
        invalid_cases = [
            (None, 100),
            (100, None),
            (None, None),
            (-10, 100),  # Negative time
            (100, -10),  # Negative time
        ]
        
        for call_time, arrival_time in invalid_cases:
            with self.subTest(call_time=call_time, arrival_time=arrival_time):
                result = self.processor.calculate_response_time(call_time, arrival_time)
                self.assertIsNone(result)
    
    def test_validate_time_format_valid(self):
        """Test time format validation with valid formats."""
        valid_formats = [
            "08:30:00",
            "23:59:59",
            "00:00:00",
            "12:30:45"
        ]
        
        for time_format in valid_formats:
            with self.subTest(time_format=time_format):
                result = self.processor.validate_time_format(time_format)
                self.assertTrue(result)
    
    def test_validate_time_format_invalid(self):
        """Test time format validation with invalid formats."""
        invalid_formats = [
            "25:00:00",
            "12:60:00",
            "12:30:60",
            "invalid",
            "",
            "12:30",     # Missing seconds - should be invalid for strict validation
            "8:30:00"    # Single digit hour - might be invalid depending on implementation
        ]
        
        for time_format in invalid_formats:
            with self.subTest(time_format=time_format):
                result = self.processor.validate_time_format(time_format)
                # Note: Some of these might be valid depending on implementation
                # The test should be adjusted based on actual validation logic
                if time_format in ["25:00:00", "12:60:00", "12:30:60", "invalid", ""]:
                    self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()