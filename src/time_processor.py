"""
Time Processing Module for EMS Data Analysis
Handles temporal data standardization and response time calculations
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Union, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TimeProcessor:
    """
    Comprehensive time processing class for EMS temporal data
    """
    
    def __init__(self):
        self.time_columns = {
            'call_time': 'Время приёма вызова (создания заявки) в формате 09:55:45',
            'dispatch_time': 'Время выезда в формате 09:55:45', 
            'arrival_time': 'Время прибытия в формате 09:55:45',
            'hospital_time': 'Время госпитализации в формате 09:55:45',
            'completion_time': 'Время возвращения (завершения) в формате 09:55:45'
        }
    
    def standardize_time(self, time_str: Union[str, float, None]) -> Optional[float]:
        """
        Standardize time strings to minutes since midnight
        
        Args:
            time_str: Time string in format HH:MM:SS or HH:MM:SS AM/PM
            
        Returns:
            Minutes since midnight as float, or np.nan if invalid
        """
        try:
            if pd.isna(time_str) or time_str == '' or time_str is None:
                return np.nan
            
            # Convert to string and clean
            time_str = str(time_str).strip()
            
            # Handle AM/PM format
            if 'AM' in time_str or 'PM' in time_str:
                # Parse 12-hour format
                time_obj = datetime.strptime(time_str, '%I:%M:%S %p')
            else:
                # Remove AM/PM if present but not needed
                time_str = time_str.replace(' AM', '').replace(' PM', '')
                
                # Handle different time formats
                if ':' in time_str:
                    parts = time_str.split(':')
                    if len(parts) >= 2:
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        return float(hours * 60 + minutes)
                else:
                    return np.nan
            
            return float(time_obj.hour * 60 + time_obj.minute)
            
        except (ValueError, TypeError, AttributeError) as e:
            logger.debug(f"Time parsing failed for '{time_str}': {e}")
            return np.nan
    
    def process_time_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process all time columns in the dataframe
        
        Args:
            df: Input dataframe with time columns
            
        Returns:
            DataFrame with processed time columns
        """
        df_processed = df.copy()
        
        # Find time columns that exist in the dataframe
        existing_time_cols = []
        for col in df.columns:
            if ':' in str(col) and any(char.isdigit() for char in str(col)):
                existing_time_cols.append(col)
        
        logger.info(f"Found time columns: {existing_time_cols}")
        
        # Process each time column
        for col in existing_time_cols:
            processed_col_name = f"{col}_minutes"
            df_processed[processed_col_name] = df_processed[col].apply(self.standardize_time)
            logger.info(f"Processed {col} -> {processed_col_name}")
        
        # Try to identify standard time columns by name matching
        for key, expected_col in self.time_columns.items():
            if expected_col in df.columns:
                processed_col_name = f"{key}_minutes"
                df_processed[processed_col_name] = df_processed[expected_col].apply(self.standardize_time)
                logger.info(f"Processed {expected_col} -> {processed_col_name}")
        
        return df_processed
    
    def calculate_response_intervals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate various response time intervals
        
        Args:
            df: DataFrame with processed time columns
            
        Returns:
            DataFrame with calculated intervals
        """
        df_with_intervals = df.copy()
        
        # Find available time columns
        time_minute_cols = [col for col in df.columns if col.endswith('_minutes')]
        
        # Map common time patterns
        dispatch_cols = [col for col in time_minute_cols if 'dispatch' in col.lower() or 'выезд' in col.lower()]
        arrival_cols = [col for col in time_minute_cols if 'arrival' in col.lower() or 'прибыт' in col.lower()]
        call_cols = [col for col in time_minute_cols if 'call' in col.lower() or 'приём' in col.lower()]
        
        # Also check for direct time column patterns
        if not dispatch_cols:
            dispatch_cols = [col for col in time_minute_cols if '3:54' in col or 'выезд' in str(df.columns)]
        if not arrival_cols:
            arrival_cols = [col for col in time_minute_cols if '31:15' in col or 'прибыт' in str(df.columns)]
        
        logger.info(f"Dispatch columns: {dispatch_cols}")
        logger.info(f"Arrival columns: {arrival_cols}")
        logger.info(f"Call columns: {call_cols}")
        
        # Calculate response time (arrival - dispatch)
        if dispatch_cols and arrival_cols:
            dispatch_col = dispatch_cols[0]
            arrival_col = arrival_cols[0]
            
            df_with_intervals['response_time'] = (
                df_with_intervals[arrival_col] - df_with_intervals[dispatch_col]
            )
            
            # Handle overnight calls (negative times)
            overnight_mask = df_with_intervals['response_time'] < -1000
            df_with_intervals.loc[overnight_mask, 'response_time'] += 1440  # Add 24 hours in minutes
            
            logger.info(f"Calculated response_time using {arrival_col} - {dispatch_col}")
        
        # Calculate dispatch delay (dispatch - call)
        if call_cols and dispatch_cols:
            call_col = call_cols[0]
            dispatch_col = dispatch_cols[0]
            
            df_with_intervals['dispatch_delay'] = (
                df_with_intervals[dispatch_col] - df_with_intervals[call_col]
            )
            
            # Handle overnight calls
            overnight_mask = df_with_intervals['dispatch_delay'] < -1000
            df_with_intervals.loc[overnight_mask, 'dispatch_delay'] += 1440
            
            logger.info(f"Calculated dispatch_delay using {dispatch_col} - {call_col}")
        
        return df_with_intervals
    
    def validate_time_data(self, df: pd.DataFrame) -> dict:
        """
        Validate processed time data and return quality metrics
        
        Args:
            df: DataFrame with processed time data
            
        Returns:
            Dictionary with validation metrics
        """
        metrics = {
            'total_records': len(df),
            'time_columns_processed': 0,
            'response_time_valid': 0,
            'response_time_stats': {},
            'data_quality_score': 0
        }
        
        # Count processed time columns
        time_cols = [col for col in df.columns if col.endswith('_minutes')]
        metrics['time_columns_processed'] = len(time_cols)
        
        # Validate response time if available
        if 'response_time' in df.columns:
            valid_response_mask = (
                df['response_time'].notna() & 
                (df['response_time'] >= 0) & 
                (df['response_time'] <= 180)  # Max 3 hours
            )
            
            metrics['response_time_valid'] = valid_response_mask.sum()
            
            if metrics['response_time_valid'] > 0:
                valid_times = df.loc[valid_response_mask, 'response_time']
                metrics['response_time_stats'] = {
                    'mean': valid_times.mean(),
                    'median': valid_times.median(),
                    'std': valid_times.std(),
                    'min': valid_times.min(),
                    'max': valid_times.max(),
                    'q25': valid_times.quantile(0.25),
                    'q75': valid_times.quantile(0.75)
                }
        
        # Calculate overall data quality score
        if metrics['total_records'] > 0:
            quality_factors = []
            
            # Time processing completeness
            if metrics['time_columns_processed'] > 0:
                quality_factors.append(min(metrics['time_columns_processed'] / 5, 1.0))
            
            # Response time validity
            if 'response_time' in df.columns:
                response_validity = metrics['response_time_valid'] / metrics['total_records']
                quality_factors.append(response_validity)
            
            metrics['data_quality_score'] = np.mean(quality_factors) * 100 if quality_factors else 0
        
        return metrics


def process_ems_time_data(df: pd.DataFrame) -> tuple:
    """
    Convenience function to process EMS time data
    
    Args:
        df: Raw dataframe with time columns
        
    Returns:
        Tuple of (processed_dataframe, validation_metrics)
    """
    processor = TimeProcessor()
    
    # Process time columns
    df_processed = processor.process_time_columns(df)
    
    # Calculate intervals
    df_with_intervals = processor.calculate_response_intervals(df_processed)
    
    # Validate results
    validation_metrics = processor.validate_time_data(df_with_intervals)
    
    return df_with_intervals, validation_metrics


if __name__ == "__main__":
    # Test the time processor
    # Create sample data for testing
    sample_data = {
        '0:03:54': ['0:03:54', '0:05:30', '0:10:15'],
        '0:31:15': ['0:31:15', '0:28:45', '0:25:30'],
        'District': ['District A', 'District B', 'District C']
    }
    
    df_test = pd.DataFrame(sample_data)
    
    print("Testing time processor...")
    df_processed, metrics = process_ems_time_data(df_test)
    
    print("\nProcessed DataFrame:")
    print(df_processed.head())
    
    print("\nValidation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value}")