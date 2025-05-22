"""
Emergency Medical Services Data Loader
Robust data loading with multiple methods and encoding detection
"""

import pandas as pd
import numpy as np
import polars as pl
from pathlib import Path
import chardet
import csv
from datetime import datetime
from typing import Optional, Tuple, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EMSDataLoader:
    """
    Comprehensive EMS data loader with multiple fallback methods
    and automatic encoding detection
    """
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.validation_results = {
            'file_exists': False,
            'encoding_detected': None,
            'successful_method': None,
            'data_structure': None,
            'row_count': 0
        }
    
    def validate_file_existence(self) -> bool:
        """Check if file exists"""
        self.validation_results['file_exists'] = self.file_path.exists()
        if not self.validation_results['file_exists']:
            raise FileNotFoundError(f"File not found: {self.file_path}")
        return True
    
    def detect_encoding(self) -> Optional[str]:
        """Detect file encoding using chardet"""
        try:
            with open(self.file_path, 'rb') as file:
                raw_data = file.read(100000)  # Read first 100KB
                result = chardet.detect(raw_data)
                self.validation_results['encoding_detected'] = result
                return result['encoding']
        except Exception as e:
            logger.error(f"Encoding detection failed: {str(e)}")
            return None
    
    def try_pandas_read(self, encoding: str = None) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Attempt to read file using pandas with various encodings"""
        encodings = [encoding] if encoding else ['cp1251', 'windows-1251', 'utf-8', 'latin1']
        
        for enc in encodings:
            try:
                # Try different pandas read methods
                methods = [
                    lambda: pd.read_csv(self.file_path, encoding=enc, skiprows=2),
                    lambda: pd.read_csv(self.file_path, encoding=enc, skiprows=2, on_bad_lines='skip'),
                    lambda: pd.read_csv(self.file_path, encoding=enc, skiprows=2, engine='python'),
                    lambda: pd.read_csv(self.file_path, encoding=enc, skiprows=2, quoting=csv.QUOTE_NONE, error_bad_lines=False)
                ]
                
                for i, method in enumerate(methods):
                    try:
                        df = method()
                        self.validation_results['successful_method'] = f'pandas_method_{i+1}_with_{enc}'
                        return df, enc
                    except:
                        continue
                        
            except Exception as e:
                logger.debug(f"Pandas read failed with {enc}: {str(e)}")
                continue
        
        return None, None
    
    def try_polars_read(self, encoding: str = None) -> Tuple[Optional[pl.DataFrame], Optional[str]]:
        """Attempt to read file using polars with various settings"""
        encodings = [encoding] if encoding else ['cp1251', 'windows-1251', 'utf-8', 'latin1']
        
        for enc in encodings:
            try:
                # Try different polars read methods
                methods = [
                    lambda: pl.read_csv(
                        self.file_path,
                        encoding=enc,
                        separator=',',
                        skip_rows=2,
                        truncate_ragged_lines=True
                    ),
                    lambda: pl.read_csv(
                        self.file_path,
                        encoding=enc,
                        separator=',',
                        skip_rows=2,
                        truncate_ragged_lines=True,
                        ignore_errors=True
                    )
                ]
                
                for i, method in enumerate(methods):
                    try:
                        df = method()
                        self.validation_results['successful_method'] = f'polars_method_{i+1}_with_{enc}'
                        return df, enc
                    except:
                        continue
                        
            except Exception as e:
                logger.debug(f"Polars read failed with {enc}: {str(e)}")
                continue
        
        return None, None
    
    def load_data(self) -> pd.DataFrame:
        """
        Main method to load data with multiple fallback strategies
        """
        logger.info("Starting data validation and loading process...")
        
        # Validate file existence
        self.validate_file_existence()
        logger.info("File found, starting validation...")
        
        # Detect encoding
        detected_encoding = self.detect_encoding()
        logger.info(f"Detected encoding: {detected_encoding}")
        
        # Try different loading methods
        df = None
        successful_encoding = None
        
        # Method 1: Try pandas
        logger.info("Attempting pandas read...")
        df_pandas, enc_pandas = self.try_pandas_read(detected_encoding)
        if df_pandas is not None:
            df = df_pandas
            successful_encoding = enc_pandas
            logger.info(f"Successfully loaded with pandas using {enc_pandas}")
        
        # Method 2: Try polars if pandas failed
        if df is None:
            logger.info("Attempting polars read...")
            df_polars, enc_polars = self.try_polars_read(detected_encoding)
            if df_polars is not None:
                df = df_polars.to_pandas()  # Convert to pandas for compatibility
                successful_encoding = enc_polars
                logger.info(f"Successfully loaded with polars using {enc_polars}")
        
        if df is not None:
            # Update validation results
            self.validation_results.update({
                'data_structure': {
                    'columns': len(df.columns),
                    'rows': len(df),
                    'missing_values': df.isnull().sum().sum()
                },
                'row_count': len(df),
                'successful_encoding': successful_encoding
            })
            
            logger.info(f"Data loaded successfully:")
            logger.info(f"Rows: {self.validation_results['row_count']}")
            logger.info(f"Columns: {self.validation_results['data_structure']['columns']}")
            logger.info(f"Method: {self.validation_results['successful_method']}")
            
            return df
        else:
            raise ValueError("Failed to load data with any method")
    
    def get_validation_results(self) -> Dict[str, Any]:
        """Return validation results"""
        return self.validation_results


def load_ems_data(file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Convenience function to load EMS data
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Tuple of (DataFrame, validation_results)
    """
    loader = EMSDataLoader(file_path)
    df = loader.load_data()
    validation_results = loader.get_validation_results()
    
    return df, validation_results


if __name__ == "__main__":
    # Test the loader
    try:
        file_path = "/mnt/c/Desktop/work for claude/google_colab/data/Mykolaivska_pro_mapping.csv"
        df, results = load_ems_data(file_path)
        
        print("\nData loading results:")
        for key, value in results.items():
            print(f"{key}: {value}")
            
        print(f"\nDataFrame shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"Error: {e}")