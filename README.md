# Emergency Medical Services (EMS) Data Analysis Pipeline

## Overview

This comprehensive data analysis pipeline processes Emergency Medical Services (EMS) dispatch data to provide actionable insights for healthcare administrators and emergency service managers. The system analyzes response times, disease patterns, territorial distribution, and temporal trends to optimize emergency medical resource allocation.

## 🚀 Key Features

### Data Processing & Validation
- **Robust Data Loading**: Multi-encoding support (UTF-8, CP1251, Windows-1251) with automatic detection
- **Time Standardization**: Converts various time formats to consistent HH:MM:SS format
- **Response Time Calculation**: Handles overnight calls and cross-midnight scenarios
- **Data Quality Validation**: Comprehensive checks for missing values and data integrity

### Analytics Capabilities
- **Response Time Analysis**: Statistical analysis of emergency response metrics
- **Disease Distribution Mapping**: Categorization and frequency analysis of medical conditions
- **Territorial Analysis**: Geographic distribution of emergency calls by districts
- **Temporal Pattern Recognition**: Peak hours, seasonal trends, and workload analysis
- **Workload Assessment**: Resource utilization and demand forecasting

### Visualization & Reporting
- **Interactive Dashboards**: Comprehensive multi-panel visualizations
- **Statistical Charts**: Distribution plots, time series, and comparative analysis
- **Automated Reports**: JSON and CSV exports with detailed summaries
- **Publication-Ready Graphics**: High-DPI exports suitable for presentations

## 📁 Project Structure

```
ems-data-analysis-pipeline/
├── src/                           # Core application modules
│   ├── data_loader.py            # Data ingestion and validation
│   ├── time_processor.py         # Time standardization utilities
│   ├── ems_analyzer.py           # Statistical analysis engine
│   ├── visualizer.py             # Data visualization components
│   ├── main.py                   # Pipeline orchestration
│   └── utils.py                  # Helper utilities
├── tests/                         # Comprehensive test suite
│   ├── test_data_loader.py       # Data loading tests
│   ├── test_time_processor.py    # Time processing tests
│   ├── test_ems_analyzer.py      # Analysis engine tests
│   ├── test_visualizer.py        # Visualization tests
│   └── test_main.py              # Integration tests
├── data/                          # Sample datasets
│   ├── DATASET_v1.csv            # Primary EMS dataset
│   └── HeRAMS NSZU.csv           # Healthcare facility data
├── notebooks/                     # Original Jupyter analysis
│   └── Untitled19_processed_clean_clean_clean.ipynb
├── output/                        # Generated results (created at runtime)
│   ├── reports/                  # Analysis summaries and data exports
│   ├── visualizations/           # Generated charts and dashboards
│   └── ems_analysis.log          # Execution logs
├── requirements.txt               # Python dependencies
├── run_tests.py                  # Test execution script
└── README.md                     # This documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment support
- 4GB+ RAM recommended for large datasets

### Quick Start

```bash
# 1. Clone the repository
git clone <repository-url>
cd ems-data-analysis-pipeline

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the complete analysis pipeline
python src/main.py
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥1.3.0 | Data manipulation and analysis |
| numpy | ≥1.20.0 | Numerical computing |
| matplotlib | ≥3.4.0 | Basic plotting and visualization |
| seaborn | Latest | Statistical data visualization |
| plotly | Latest | Interactive visualizations |
| chardet | Latest | Character encoding detection |
| polars | Latest | High-performance data processing |

## 📊 Usage Examples

### Basic Pipeline Execution

```python
from src.main import EMSAnalysisPipeline

# Initialize pipeline with data file
pipeline = EMSAnalysisPipeline(
    data_file_path="data/DATASET_v1.csv",
    output_dir="output"
)

# Execute complete analysis
success = pipeline.run_full_pipeline()

if success:
    print("Analysis completed successfully!")
    print("Check output/ directory for results")
```

### Individual Component Usage

```python
from src.data_loader import EMSDataLoader
from src.time_processor import TimeProcessor
from src.ems_analyzer import EMSAnalyzer

# Load and process data
loader = EMSDataLoader()
data = loader.load_data("data/DATASET_v1.csv")

# Process time columns
processor = TimeProcessor()
data['call_time_minutes'] = data['Время_вызова'].apply(
    lambda x: processor.time_to_minutes(
        processor.standardize_time_format(x)
    )
)

# Analyze response times
analyzer = EMSAnalyzer()
response_analysis = analyzer.analyze_response_times(
    data, 'response_time_minutes'
)
```

### Custom Analysis Workflow

```python
# Step-by-step analysis
pipeline = EMSAnalysisPipeline("data/your_data.csv", "custom_output")

# 1. Load and validate data
if pipeline.load_data():
    print(f"Loaded {len(pipeline.raw_data)} records")

# 2. Process temporal data
if pipeline.process_time_data():
    print("Time processing completed")

# 3. Run specific analyses
if pipeline.run_analysis():
    print("Statistical analysis completed")

# 4. Generate visualizations
if pipeline.generate_visualizations():
    print("Visualizations created")

# 5. Export reports
if pipeline.generate_reports():
    print("Reports generated")
```

## 🧪 Testing

### Running the Test Suite

```bash
# Run all tests with detailed output
python run_tests.py

# Run specific test modules
python -m unittest tests.test_data_loader
python -m unittest tests.test_ems_analyzer
```

### Test Coverage

The test suite includes:
- **Unit Tests**: Individual component functionality
- **Integration Tests**: End-to-end pipeline execution
- **Edge Case Testing**: Error handling and boundary conditions
- **Data Validation Tests**: Input/output format verification

## 📈 Analysis Outputs

### Generated Reports

1. **Analysis Summary** (`output/reports/analysis_summary.txt`)
   - Dataset overview and quality metrics
   - Key statistical findings
   - Data completeness assessment

2. **Processed Data** (`output/reports/processed_data.csv`)
   - Clean, standardized dataset
   - Calculated response times
   - Time-based derived features

3. **Analysis Results** (`output/reports/analysis_results.json`)
   - Structured analysis outcomes
   - Statistical summaries
   - Performance metrics

### Visualization Outputs

1. **Response Time Analysis**
   - Distribution histograms
   - Box plots by district/time
   - Trend analysis charts

2. **Disease Pattern Analysis**
   - Frequency distribution charts
   - Categorical breakdowns
   - Comparative visualizations

3. **Temporal Analysis**
   - Hourly call volume patterns
   - Seasonal trend analysis
   - Peak demand identification

4. **Comprehensive Dashboard**
   - Multi-panel overview
   - Key performance indicators
   - Executive summary visuals

## 🔧 Configuration & Customization

### Data File Requirements

Your EMS data CSV should include these columns (Russian/Ukrainian names supported):
- `Время_вызова` / `Call_Time`: Emergency call timestamp
- `Время_прибытия` / `Arrival_Time`: Emergency response arrival time
- `Район` / `District`: Geographic district or zone
- `Диагноз` / `Diagnosis`: Medical diagnosis or condition
- `Адрес` / `Address`: Call location address

### Pipeline Configuration

```python
# Custom configuration example
pipeline = EMSAnalysisPipeline(
    data_file_path="path/to/your/data.csv",
    output_dir="custom_output_directory"
)

# Configure specific analysis parameters
analyzer = EMSAnalyzer()
analyzer.set_response_time_thresholds(
    excellent=10,    # minutes
    good=15,
    acceptable=20,
    poor=30
)
```

## 🚨 Troubleshooting

### Common Issues

1. **File Encoding Errors**
   ```
   Solution: The pipeline automatically detects encoding.
   If issues persist, manually convert to UTF-8.
   ```

2. **Missing Dependencies**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Memory Issues with Large Datasets**
   ```python
   # Process data in chunks
   loader = EMSDataLoader()
   loader.set_chunk_size(10000)  # Process 10k records at a time
   ```

4. **Time Format Inconsistencies**
   ```
   The TimeProcessor handles multiple formats automatically.
   Check logs for unsupported time formats.
   ```

### Log Analysis

Check `output/ems_analysis.log` for detailed execution information:
```bash
tail -f output/ems_analysis.log  # Monitor real-time progress
grep ERROR output/ems_analysis.log  # Find error messages
```

## 🤝 Contributing

This project welcomes contributions! Areas for improvement:

- Additional visualization types
- Machine learning predictive models
- Real-time data streaming support
- Geographic mapping integration
- Mobile dashboard interface

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 📞 Support

For questions, issues, or feature requests:
1. Check the troubleshooting section above
2. Review the test outputs for debugging information
3. Submit issues with log files and sample data (anonymized)

## 🏆 Acknowledgments

This project processes critical emergency medical services data to support healthcare decision-making. The analysis framework is designed to respect data privacy while providing maximum analytical value for improving emergency response systems.

---

**Last Updated**: January 2025  
**Version**: 1.0.0  
**Python Compatibility**: 3.8+