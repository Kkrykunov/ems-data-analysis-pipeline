"""
EMS Data Analyzer
Comprehensive analysis of Emergency Medical Services data including
response time analysis, disease distribution, and workload assessment
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EMSAnalyzer:
    """
    Comprehensive analyzer for Emergency Medical Services data
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.results = {}
        self.column_mapping = self._map_columns()
        
    def _map_columns(self) -> Dict[str, str]:
        """
        Map column names to standardized names based on content
        """
        column_mapping = {}
        
        # Map district columns
        district_patterns = ['район', 'district', 'миколаївський']
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in district_patterns):
                column_mapping['district'] = col
                break
        
        # Map urgency columns
        urgency_patterns = ['терміново', 'срочн', 'urgency', 'тип выезда']
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in urgency_patterns):
                column_mapping['urgency'] = col
                break
        
        # Map diagnosis columns
        diagnosis_patterns = ['мкх', 'icd', 'диагноз']
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in diagnosis_patterns):
                column_mapping['diagnosis'] = col
                break
        
        # Map team ID columns
        team_patterns = ['бригада', 'team', 'brigade']
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in team_patterns):
                column_mapping['team_id'] = col
                break
        
        # Map call reason columns
        reason_patterns = ['причина', 'reason', 'вызов']
        for col in self.df.columns:
            col_lower = str(col).lower()
            if any(pattern in col_lower for pattern in reason_patterns):
                column_mapping['call_reason'] = col
                break
        
        logger.info(f"Column mapping: {column_mapping}")
        return column_mapping
    
    def analyze_response_times(self) -> Dict:
        """
        Analyze response time patterns by district and urgency
        """
        if 'response_time' not in self.df.columns:
            logger.warning("No response_time column found")
            return {}
        
        # Filter valid response times
        valid_mask = (
            self.df['response_time'].notna() & 
            (self.df['response_time'] >= 0) & 
            (self.df['response_time'] <= 180)
        )
        
        df_valid = self.df[valid_mask].copy()
        
        if len(df_valid) == 0:
            logger.warning("No valid response times found")
            return {}
        
        results = {
            'overall_stats': {
                'count': len(df_valid),
                'mean': df_valid['response_time'].mean(),
                'median': df_valid['response_time'].median(),
                'std': df_valid['response_time'].std(),
                'min': df_valid['response_time'].min(),
                'max': df_valid['response_time'].max(),
                'q25': df_valid['response_time'].quantile(0.25),
                'q75': df_valid['response_time'].quantile(0.75)
            }
        }
        
        # Analysis by district
        if 'district' in self.column_mapping:
            district_col = self.column_mapping['district']
            district_stats = df_valid.groupby(district_col)['response_time'].agg([
                'count', 'mean', 'median', 'std',
                lambda x: x.quantile(0.25),
                lambda x: x.quantile(0.75)
            ]).round(2)
            district_stats.columns = ['count', 'mean', 'median', 'std', 'q25', 'q75']
            district_stats['iqr'] = district_stats['q75'] - district_stats['q25']
            
            results['by_district'] = district_stats.to_dict('index')
        
        # Analysis by urgency
        if 'urgency' in self.column_mapping:
            urgency_col = self.column_mapping['urgency']
            urgency_stats = df_valid.groupby(urgency_col)['response_time'].agg([
                'count', 'mean', 'median', 'std'
            ]).round(2)
            
            results['by_urgency'] = urgency_stats.to_dict('index')
        
        # Combined analysis (district + urgency)
        if 'district' in self.column_mapping and 'urgency' in self.column_mapping:
            district_col = self.column_mapping['district']
            urgency_col = self.column_mapping['urgency']
            
            combined_stats = df_valid.groupby([district_col, urgency_col])['response_time'].agg([
                'count', 'mean', 'median', 'std'
            ]).round(2)
            
            results['by_district_urgency'] = combined_stats.to_dict('index')
        
        # Compliance with standards (20 minutes)
        compliance_rate = (df_valid['response_time'] <= 20).mean() * 100
        results['compliance_20min'] = compliance_rate
        
        self.results['response_time_analysis'] = results
        return results
    
    def analyze_disease_distribution(self) -> Dict:
        """
        Analyze disease distribution patterns
        """
        if 'diagnosis' not in self.column_mapping:
            logger.warning("No diagnosis column found")
            return {}
        
        diagnosis_col = self.column_mapping['diagnosis']
        
        # Overall disease distribution
        disease_counts = self.df[diagnosis_col].value_counts()
        disease_percentages = (disease_counts / len(self.df) * 100).round(2)
        
        results = {
            'overall_distribution': {
                'top_diseases': disease_counts.head(10).to_dict(),
                'disease_percentages': disease_percentages.head(10).to_dict()
            }
        }
        
        # Distribution by district
        if 'district' in self.column_mapping:
            district_col = self.column_mapping['district']
            
            district_disease = pd.crosstab(
                self.df[district_col], 
                self.df[diagnosis_col], 
                normalize='index'
            ) * 100
            
            results['by_district'] = district_disease.round(2).to_dict('index')
        
        # Urgency by disease
        if 'urgency' in self.column_mapping:
            urgency_col = self.column_mapping['urgency']
            
            urgency_disease = pd.crosstab(
                self.df[diagnosis_col], 
                self.df[urgency_col], 
                normalize='index'
            ) * 100
            
            results['urgency_by_disease'] = urgency_disease.round(2).to_dict('index')
        
        self.results['disease_analysis'] = results
        return results
    
    def analyze_workload(self) -> Dict:
        """
        Analyze workload distribution across teams and districts
        """
        results = {}
        
        # District-level workload
        if 'district' in self.column_mapping:
            district_col = self.column_mapping['district']
            
            district_workload = self.df.groupby(district_col).agg({
                district_col: 'count'
            }).rename(columns={district_col: 'total_calls'})
            
            # Add team information if available
            if 'team_id' in self.column_mapping:
                team_col = self.column_mapping['team_id']
                
                team_counts = self.df.groupby(district_col)[team_col].nunique()
                district_workload['unique_teams'] = team_counts
                district_workload['calls_per_team'] = (
                    district_workload['total_calls'] / district_workload['unique_teams']
                ).round(2)
            
            # Add urgency information if available
            if 'urgency' in self.column_mapping:
                urgency_col = self.column_mapping['urgency']
                
                urgent_calls = self.df[self.df[urgency_col] == 'Терміново'].groupby(district_col).size()
                district_workload['urgent_calls'] = urgent_calls.fillna(0)
                district_workload['urgent_percentage'] = (
                    district_workload['urgent_calls'] / district_workload['total_calls'] * 100
                ).round(2)
            
            results['district_workload'] = district_workload.to_dict('index')
        
        # Team-level workload
        if 'team_id' in self.column_mapping:
            team_col = self.column_mapping['team_id']
            
            team_workload = self.df.groupby(team_col).agg({
                team_col: 'count'
            }).rename(columns={team_col: 'total_calls'})
            
            # Add response time if available
            if 'response_time' in self.df.columns:
                team_response = self.df.groupby(team_col)['response_time'].agg([
                    'mean', 'median', 'count'
                ]).round(2)
                
                team_workload = team_workload.join(team_response)
            
            results['team_workload'] = team_workload.to_dict('index')
        
        self.results['workload_analysis'] = results
        return results
    
    def analyze_call_patterns(self) -> Dict:
        """
        Analyze call reason patterns
        """
        if 'call_reason' not in self.column_mapping:
            logger.warning("No call reason column found")
            return {}
        
        reason_col = self.column_mapping['call_reason']
        
        # Overall call reason distribution
        reason_counts = self.df[reason_col].value_counts()
        reason_percentages = (reason_counts / len(self.df) * 100).round(2)
        
        results = {
            'overall_patterns': {
                'top_reasons': reason_counts.head(10).to_dict(),
                'reason_percentages': reason_percentages.head(10).to_dict()
            }
        }
        
        # Patterns by district
        if 'district' in self.column_mapping:
            district_col = self.column_mapping['district']
            
            district_reasons = pd.crosstab(
                self.df[district_col], 
                self.df[reason_col], 
                normalize='index'
            ) * 100
            
            results['by_district'] = district_reasons.round(2).to_dict('index')
        
        self.results['call_pattern_analysis'] = results
        return results
    
    def run_comprehensive_analysis(self) -> Dict:
        """
        Run all analysis modules and return comprehensive results
        """
        logger.info("Starting comprehensive EMS data analysis...")
        
        # Run all analysis modules
        self.analyze_response_times()
        self.analyze_disease_distribution()
        self.analyze_workload()
        self.analyze_call_patterns()
        
        # Generate summary
        summary = {
            'data_overview': {
                'total_records': len(self.df),
                'columns_available': list(self.df.columns),
                'column_mapping': self.column_mapping,
                'analysis_modules_run': list(self.results.keys())
            },
            'analysis_results': self.results
        }
        
        logger.info("Comprehensive analysis completed")
        return summary
    
    def get_analysis_summary(self) -> str:
        """
        Generate a text summary of the analysis results
        """
        summary_lines = []
        summary_lines.append("EMS Data Analysis Summary")
        summary_lines.append("=" * 40)
        
        # Data overview
        summary_lines.append(f"Total records analyzed: {len(self.df)}")
        summary_lines.append(f"Columns mapped: {len(self.column_mapping)}")
        
        # Response time summary
        if 'response_time_analysis' in self.results:
            rt_analysis = self.results['response_time_analysis']
            if 'overall_stats' in rt_analysis:
                stats = rt_analysis['overall_stats']
                summary_lines.append(f"\nResponse Time Analysis:")
                summary_lines.append(f"- Valid response times: {stats['count']}")
                summary_lines.append(f"- Mean response time: {stats['mean']:.2f} minutes")
                summary_lines.append(f"- Median response time: {stats['median']:.2f} minutes")
                
                if 'compliance_20min' in rt_analysis:
                    summary_lines.append(f"- Compliance with 20min standard: {rt_analysis['compliance_20min']:.1f}%")
        
        # Disease analysis summary
        if 'disease_analysis' in self.results:
            disease_analysis = self.results['disease_analysis']
            if 'overall_distribution' in disease_analysis:
                top_diseases = disease_analysis['overall_distribution']['top_diseases']
                summary_lines.append(f"\nTop diseases: {list(top_diseases.keys())[:3]}")
        
        # Workload summary
        if 'workload_analysis' in self.results:
            workload = self.results['workload_analysis']
            if 'district_workload' in workload:
                districts = len(workload['district_workload'])
                summary_lines.append(f"\nDistricts analyzed: {districts}")
        
        return "\n".join(summary_lines)


def analyze_ems_data(df: pd.DataFrame) -> Tuple[Dict, str]:
    """
    Convenience function to analyze EMS data
    
    Args:
        df: DataFrame with EMS data
        
    Returns:
        Tuple of (analysis_results, summary_text)
    """
    analyzer = EMSAnalyzer(df)
    results = analyzer.run_comprehensive_analysis()
    summary = analyzer.get_analysis_summary()
    
    return results, summary


if __name__ == "__main__":
    # Test the analyzer with sample data
    sample_data = {
        'Миколаївський район': ['District A', 'District B', 'District A', 'District C'],
        'Терміново': ['Терміново', 'Не терміново', 'Терміново', 'Терміново'],
        'МКХ-10': ['A01', 'B02', 'A01', 'C03'],
        'response_time': [15, 25, 18, 22],
        'бригада id': [1, 2, 1, 3]
    }
    
    df_test = pd.DataFrame(sample_data)
    
    print("Testing EMS analyzer...")
    results, summary = analyze_ems_data(df_test)
    
    print("\nAnalysis Summary:")
    print(summary)
    
    print("\nDetailed Results:")
    for key, value in results['analysis_results'].items():
        print(f"\n{key}:")
        print(value)