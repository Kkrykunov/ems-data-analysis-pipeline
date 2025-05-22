"""
EMS Data Visualizer
Creates comprehensive visualizations for Emergency Medical Services analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import warnings
import logging

# Set up plotting style
plt.style.use('default')
sns.set_palette("husl")
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EMSVisualizer:
    """
    Comprehensive visualization class for EMS data analysis
    """
    
    def __init__(self, df: pd.DataFrame, analysis_results: Dict = None):
        self.df = df.copy()
        self.analysis_results = analysis_results or {}
        self.figures = {}
        
        # Set up matplotlib parameters
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 12
        plt.rcParams['axes.labelsize'] = 11
        plt.rcParams['xtick.labelsize'] = 9
        plt.rcParams['ytick.labelsize'] = 9
        plt.rcParams['legend.fontsize'] = 10
        
    def plot_response_time_distribution(self, save_path: str = None) -> plt.Figure:
        """
        Create response time distribution visualizations
        """
        if 'response_time' not in self.df.columns:
            logger.warning("No response_time column found")
            return None
        
        # Filter valid response times
        valid_mask = (
            self.df['response_time'].notna() & 
            (self.df['response_time'] >= 0) & 
            (self.df['response_time'] <= 180)
        )
        df_valid = self.df[valid_mask]
        
        if len(df_valid) == 0:
            logger.warning("No valid response times to plot")
            return None
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Emergency Medical Services - Response Time Analysis', fontsize=16, fontweight='bold')
        
        # 1. Overall distribution histogram
        axes[0, 0].hist(df_valid['response_time'], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].axvline(df_valid['response_time'].mean(), color='red', linestyle='--', 
                          label=f'Mean: {df_valid["response_time"].mean():.1f} min')
        axes[0, 0].axvline(df_valid['response_time'].median(), color='green', linestyle='--', 
                          label=f'Median: {df_valid["response_time"].median():.1f} min')
        axes[0, 0].axvline(20, color='orange', linestyle='-', linewidth=2, 
                          label='Standard: 20 min')
        axes[0, 0].set_title('Response Time Distribution')
        axes[0, 0].set_xlabel('Response Time (minutes)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Box plot by district (if available)
        district_cols = [col for col in self.df.columns if 'район' in col.lower() or 'district' in col.lower()]
        if district_cols:
            district_col = district_cols[0]
            df_plot = df_valid[df_valid[district_col].notna()]
            
            # Limit to top districts by call volume
            top_districts = df_plot[district_col].value_counts().head(10).index
            df_plot = df_plot[df_plot[district_col].isin(top_districts)]
            
            if len(df_plot) > 0:
                sns.boxplot(data=df_plot, x=district_col, y='response_time', ax=axes[0, 1])
                axes[0, 1].axhline(20, color='red', linestyle='--', alpha=0.7, label='20 min standard')
                axes[0, 1].set_title('Response Time by District')
                axes[0, 1].set_xlabel('District')
                axes[0, 1].set_ylabel('Response Time (minutes)')
                axes[0, 1].tick_params(axis='x', rotation=45)
                axes[0, 1].legend()
                axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Box plot by urgency (if available)
        urgency_cols = [col for col in self.df.columns if 'терміново' in col.lower() or 'urgency' in col.lower()]
        if urgency_cols:
            urgency_col = urgency_cols[0]
            df_plot = df_valid[df_valid[urgency_col].notna()]
            
            if len(df_plot) > 0:
                sns.boxplot(data=df_plot, x=urgency_col, y='response_time', ax=axes[1, 0])
                axes[1, 0].axhline(20, color='red', linestyle='--', alpha=0.7, label='20 min standard')
                axes[1, 0].set_title('Response Time by Urgency')
                axes[1, 0].set_xlabel('Urgency Level')
                axes[1, 0].set_ylabel('Response Time (minutes)')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Cumulative distribution
        sorted_times = np.sort(df_valid['response_time'])
        cumulative_prob = np.arange(1, len(sorted_times) + 1) / len(sorted_times)
        
        axes[1, 1].plot(sorted_times, cumulative_prob * 100, linewidth=2, color='blue')
        axes[1, 1].axvline(20, color='red', linestyle='--', alpha=0.7, 
                          label=f'20 min: {(sorted_times <= 20).mean() * 100:.1f}%')
        axes[1, 1].set_title('Cumulative Response Time Distribution')
        axes[1, 1].set_xlabel('Response Time (minutes)')
        axes[1, 1].set_ylabel('Cumulative Percentage')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Response time plot saved to {save_path}")
        
        self.figures['response_time_distribution'] = fig
        return fig
    
    def plot_disease_distribution(self, save_path: str = None) -> plt.Figure:
        """
        Create disease distribution visualizations
        """
        # Find diagnosis column
        diagnosis_cols = [col for col in self.df.columns if 'мкх' in col.lower() or 'icd' in col.lower()]
        if not diagnosis_cols:
            logger.warning("No diagnosis column found")
            return None
        
        diagnosis_col = diagnosis_cols[0]
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Emergency Medical Services - Disease Distribution Analysis', fontsize=16, fontweight='bold')
        
        # 1. Top diseases overall
        disease_counts = self.df[diagnosis_col].value_counts().head(15)
        
        axes[0, 0].barh(range(len(disease_counts)), disease_counts.values, color='lightcoral')
        axes[0, 0].set_yticks(range(len(disease_counts)))
        axes[0, 0].set_yticklabels(disease_counts.index)
        axes[0, 0].set_title('Top 15 Diagnoses (Overall)')
        axes[0, 0].set_xlabel('Number of Cases')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Disease distribution pie chart (top 10)
        top_diseases = disease_counts.head(10)
        other_count = disease_counts.iloc[10:].sum()
        
        if other_count > 0:
            pie_data = list(top_diseases.values) + [other_count]
            pie_labels = list(top_diseases.index) + ['Others']
        else:
            pie_data = top_diseases.values
            pie_labels = top_diseases.index
        
        axes[0, 1].pie(pie_data, labels=pie_labels, autopct='%1.1f%%', startangle=90)
        axes[0, 1].set_title('Disease Distribution (Top 10)')
        
        # 3. Disease by urgency (if available)
        urgency_cols = [col for col in self.df.columns if 'терміново' in col.lower() or 'urgency' in col.lower()]
        if urgency_cols:
            urgency_col = urgency_cols[0]
            
            # Cross-tabulation of top diseases and urgency
            top_disease_list = disease_counts.head(10).index
            df_top_diseases = self.df[self.df[diagnosis_col].isin(top_disease_list)]
            
            disease_urgency = pd.crosstab(df_top_diseases[diagnosis_col], 
                                        df_top_diseases[urgency_col])
            
            disease_urgency.plot(kind='bar', stacked=True, ax=axes[1, 0], 
                               color=['lightblue', 'orange'])
            axes[1, 0].set_title('Top Diseases by Urgency Level')
            axes[1, 0].set_xlabel('Diagnosis')
            axes[1, 0].set_ylabel('Number of Cases')
            axes[1, 0].tick_params(axis='x', rotation=45)
            axes[1, 0].legend(title='Urgency')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Disease by district (if available)
        district_cols = [col for col in self.df.columns if 'район' in col.lower() or 'district' in col.lower()]
        if district_cols:
            district_col = district_cols[0]
            
            # Top districts and diseases
            top_districts = self.df[district_col].value_counts().head(5).index
            top_diseases_for_heatmap = disease_counts.head(10).index
            
            df_heatmap = self.df[
                (self.df[district_col].isin(top_districts)) & 
                (self.df[diagnosis_col].isin(top_diseases_for_heatmap))
            ]
            
            if len(df_heatmap) > 0:
                heatmap_data = pd.crosstab(df_heatmap[district_col], 
                                         df_heatmap[diagnosis_col])
                
                sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=axes[1, 1])
                axes[1, 1].set_title('Disease Distribution by District (Top 5 Districts)')
                axes[1, 1].set_xlabel('Diagnosis')
                axes[1, 1].set_ylabel('District')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Disease distribution plot saved to {save_path}")
        
        self.figures['disease_distribution'] = fig
        return fig
    
    def plot_workload_analysis(self, save_path: str = None) -> plt.Figure:
        """
        Create workload analysis visualizations
        """
        # Find relevant columns
        district_cols = [col for col in self.df.columns if 'район' in col.lower() or 'district' in col.lower()]
        team_cols = [col for col in self.df.columns if 'бригада' in col.lower() or 'team' in col.lower()]
        
        if not district_cols:
            logger.warning("No district column found for workload analysis")
            return None
        
        district_col = district_cols[0]
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Emergency Medical Services - Workload Analysis', fontsize=16, fontweight='bold')
        
        # 1. Calls by district
        district_counts = self.df[district_col].value_counts()
        
        axes[0, 0].bar(range(len(district_counts)), district_counts.values, color='steelblue')
        axes[0, 0].set_xticks(range(len(district_counts)))
        axes[0, 0].set_xticklabels(district_counts.index, rotation=45, ha='right')
        axes[0, 0].set_title('Total Calls by District')
        axes[0, 0].set_xlabel('District')
        axes[0, 0].set_ylabel('Number of Calls')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Team workload (if team data available)
        if team_cols:
            team_col = team_cols[0]
            team_counts = self.df[team_col].value_counts().head(20)
            
            axes[0, 1].bar(range(len(team_counts)), team_counts.values, color='lightgreen')
            axes[0, 1].set_title('Top 20 Teams by Call Volume')
            axes[0, 1].set_xlabel('Team Rank')
            axes[0, 1].set_ylabel('Number of Calls')
            axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Urgency distribution by district
        urgency_cols = [col for col in self.df.columns if 'терміново' in col.lower() or 'urgency' in col.lower()]
        if urgency_cols:
            urgency_col = urgency_cols[0]
            
            urgency_district = pd.crosstab(self.df[district_col], self.df[urgency_col], 
                                         normalize='index') * 100
            
            urgency_district.plot(kind='bar', ax=axes[1, 0], color=['lightcoral', 'lightblue'])
            axes[1, 0].set_title('Urgency Distribution by District (%)')
            axes[1, 0].set_xlabel('District')
            axes[1, 0].set_ylabel('Percentage')
            axes[1, 0].tick_params(axis='x', rotation=45)
            axes[1, 0].legend(title='Urgency Level')
            axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Response time by workload (if available)
        if 'response_time' in self.df.columns:
            # Calculate calls per district and average response time
            district_workload = self.df.groupby(district_col).agg({
                district_col: 'count',
                'response_time': 'mean'
            }).rename(columns={district_col: 'call_count'})
            
            district_workload = district_workload[district_workload['response_time'].notna()]
            
            if len(district_workload) > 0:
                scatter = axes[1, 1].scatter(district_workload['call_count'], 
                                           district_workload['response_time'],
                                           alpha=0.7, s=100, color='purple')
                
                # Add trend line
                if len(district_workload) > 1:
                    z = np.polyfit(district_workload['call_count'], 
                                 district_workload['response_time'], 1)
                    p = np.poly1d(z)
                    axes[1, 1].plot(district_workload['call_count'], 
                                   p(district_workload['call_count']), 
                                   "r--", alpha=0.8)
                
                axes[1, 1].set_title('Response Time vs. Call Volume')
                axes[1, 1].set_xlabel('Number of Calls')
                axes[1, 1].set_ylabel('Average Response Time (minutes)')
                axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Workload analysis plot saved to {save_path}")
        
        self.figures['workload_analysis'] = fig
        return fig
    
    def create_dashboard(self, save_path: str = None) -> plt.Figure:
        """
        Create a comprehensive dashboard with key metrics
        """
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('Emergency Medical Services - Comprehensive Dashboard', 
                    fontsize=20, fontweight='bold')
        
        # Create a grid layout
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Key metrics text box
        ax_metrics = fig.add_subplot(gs[0, :2])
        ax_metrics.axis('off')
        
        # Calculate key metrics
        total_calls = len(self.df)
        
        metrics_text = f"TOTAL CALLS: {total_calls:,}\n"
        
        if 'response_time' in self.df.columns:
            valid_response = self.df['response_time'].notna() & (self.df['response_time'] >= 0)
            if valid_response.any():
                avg_response = self.df.loc[valid_response, 'response_time'].mean()
                median_response = self.df.loc[valid_response, 'response_time'].median()
                compliance = (self.df.loc[valid_response, 'response_time'] <= 20).mean() * 100
                
                metrics_text += f"AVG RESPONSE TIME: {avg_response:.1f} minutes\n"
                metrics_text += f"MEDIAN RESPONSE TIME: {median_response:.1f} minutes\n"
                metrics_text += f"20-MIN COMPLIANCE: {compliance:.1f}%\n"
        
        # Find district info
        district_cols = [col for col in self.df.columns if 'район' in col.lower() or 'district' in col.lower()]
        if district_cols:
            districts = self.df[district_cols[0]].nunique()
            metrics_text += f"DISTRICTS SERVED: {districts}\n"
        
        ax_metrics.text(0.05, 0.95, metrics_text, transform=ax_metrics.transAxes, 
                       fontsize=14, fontweight='bold', verticalalignment='top',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        # Response time histogram
        if 'response_time' in self.df.columns:
            ax_hist = fig.add_subplot(gs[0, 2:])
            valid_times = self.df['response_time'][(self.df['response_time'] >= 0) & 
                                                 (self.df['response_time'] <= 180)]
            if len(valid_times) > 0:
                ax_hist.hist(valid_times, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                ax_hist.axvline(20, color='red', linestyle='--', linewidth=2, label='20 min standard')
                ax_hist.set_title('Response Time Distribution')
                ax_hist.set_xlabel('Response Time (minutes)')
                ax_hist.set_ylabel('Frequency')
                ax_hist.legend()
                ax_hist.grid(True, alpha=0.3)
        
        # District workload
        if district_cols:
            ax_district = fig.add_subplot(gs[1, :2])
            district_counts = self.df[district_cols[0]].value_counts().head(10)
            ax_district.barh(range(len(district_counts)), district_counts.values, color='lightcoral')
            ax_district.set_yticks(range(len(district_counts)))
            ax_district.set_yticklabels(district_counts.index)
            ax_district.set_title('Top 10 Districts by Call Volume')
            ax_district.set_xlabel('Number of Calls')
            ax_district.grid(True, alpha=0.3)
        
        # Disease distribution
        diagnosis_cols = [col for col in self.df.columns if 'мкх' in col.lower() or 'icd' in col.lower()]
        if diagnosis_cols:
            ax_disease = fig.add_subplot(gs[1, 2:])
            disease_counts = self.df[diagnosis_cols[0]].value_counts().head(10)
            ax_disease.barh(range(len(disease_counts)), disease_counts.values, color='lightgreen')
            ax_disease.set_yticks(range(len(disease_counts)))
            ax_disease.set_yticklabels(disease_counts.index)
            ax_disease.set_title('Top 10 Diagnoses')
            ax_disease.set_xlabel('Number of Cases')
            ax_disease.grid(True, alpha=0.3)
        
        # Urgency by district
        urgency_cols = [col for col in self.df.columns if 'терміново' in col.lower() or 'urgency' in col.lower()]
        if urgency_cols and district_cols:
            ax_urgency = fig.add_subplot(gs[2, :])
            urgency_district = pd.crosstab(self.df[district_cols[0]], self.df[urgency_cols[0]], 
                                         normalize='index') * 100
            urgency_district.plot(kind='bar', ax=ax_urgency, color=['lightcoral', 'lightblue'])
            ax_urgency.set_title('Urgency Distribution by District (%)')
            ax_urgency.set_xlabel('District')
            ax_urgency.set_ylabel('Percentage')
            ax_urgency.tick_params(axis='x', rotation=45)
            ax_urgency.legend(title='Urgency Level')
            ax_urgency.grid(True, alpha=0.3)
        
        # Monthly trend (if date data available)
        ax_trend = fig.add_subplot(gs[3, :])
        ax_trend.text(0.5, 0.5, 'Monthly Trend Analysis\n(Requires date column)', 
                     ha='center', va='center', transform=ax_trend.transAxes,
                     fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        ax_trend.set_title('Call Volume Trends')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Dashboard saved to {save_path}")
        
        self.figures['dashboard'] = fig
        return fig
    
    def save_all_figures(self, output_dir: str = "plots"):
        """
        Save all generated figures to specified directory
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, fig in self.figures.items():
            save_path = os.path.join(output_dir, f"{name}.png")
            fig.savefig(save_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved {name} to {save_path}")
    
    def show_all_figures(self):
        """
        Display all generated figures
        """
        for name, fig in self.figures.items():
            plt.figure(fig.number)
            plt.show()


def create_ems_visualizations(df: pd.DataFrame, analysis_results: Dict = None, 
                            output_dir: str = "plots") -> EMSVisualizer:
    """
    Convenience function to create all EMS visualizations
    
    Args:
        df: DataFrame with EMS data
        analysis_results: Results from EMS analysis
        output_dir: Directory to save plots
        
    Returns:
        EMSVisualizer instance with generated plots
    """
    visualizer = EMSVisualizer(df, analysis_results)
    
    # Create all visualizations
    visualizer.plot_response_time_distribution()
    visualizer.plot_disease_distribution()
    visualizer.plot_workload_analysis()
    visualizer.create_dashboard()
    
    # Save all figures
    visualizer.save_all_figures(output_dir)
    
    return visualizer


if __name__ == "__main__":
    # Test the visualizer with sample data
    sample_data = {
        'Миколаївський район': ['District A'] * 50 + ['District B'] * 30 + ['District C'] * 20,
        'Терміново': ['Терміново'] * 60 + ['Не терміново'] * 40,
        'МКХ-10': ['A01'] * 25 + ['B02'] * 35 + ['C03'] * 40,
        'response_time': np.random.normal(18, 5, 100),
        'бригада id': np.random.choice(range(1, 11), 100)
    }
    
    df_test = pd.DataFrame(sample_data)
    
    print("Testing EMS visualizer...")
    visualizer = create_ems_visualizations(df_test, output_dir="test_plots")
    
    print("Visualizations created and saved to test_plots directory")