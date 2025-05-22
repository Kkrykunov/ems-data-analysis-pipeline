#!/usr/bin/env python3
"""
Utility functions extracted from Jupyter notebook
"""

import numpy as np
import pandas as pd


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import chardet

class EMSDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.encoding = self._detect_encoding()

    def _detect_encoding(self):
        with open(self.file_path, 'rb') as file:
            return chardet.detect(file.read())['encoding']

    def load_data(self):
        """
        Systematic data loading with encoding validation
        Returns: DataFrame with standardized structure
        """
        encodings = [self.encoding, 'utf-8', 'cp1251', 'windows-1251']

        for encoding in encodings:
            try:
                return pd.read_csv(self.file_path,
                                 encoding=encoding,
                                 sep='\t',
                                 parse_dates=['Час створення заявки',
                                            'Час виїзду',
                                            'Час прибуття'],
                                 date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S', errors='coerce'))
            except Exception as e:
                continue

        raise ValueError("Data encoding validation failed across all standard encodings")
        class EMSAnalyzer:
    def __init__(self, df):
        self.df = df
        self.results = {
            'temporal_metrics': {},
            'geographical_distribution': {},
            'clinical_patterns': {},
            'resource_utilization': {}
        }

    def compute_response_metrics(self):
        """
        Calculate standardized response time metrics
        """
        self.df['response_time'] = (
            pd.to_datetime(self.df['Час прибуття']) -
            pd.to_datetime(self.df['Час виїзду'])
        ).dt.total_seconds() / 60

        return pd.DataFrame({
            'mean_response': self.df.groupby('Район')['response_time'].mean(),
            'median_response': self.df.groupby('Район')['response_time'].median(),
            'std_response': self.df.groupby('Район')['response_time'].std()
        })

    def analyze_disease_patterns(self):
        """
        Comprehensive disease distribution analysis
        """
        return {
            'district_distribution': pd.crosstab(
                self.df['Район'],
                self.df['МКХ-10'],
                normalize='index'
            ),
            'urgency_stratification': pd.crosstab(
                [self.df['Район'], self.df['МКХ-10']],
                self.df['Помощь по диагнозу(Срочная, несрочная).']
            )
        }
        class EMSVisualizer:
    def __init__(self, analysis_results):
        self.results = analysis_results
        plt.style.use('seaborn')

    def generate_response_time_analysis(self):
        """
        Generate statistical visualization for response times
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

        # Response Time Distribution
        sns.boxplot(data=self.results['temporal_metrics'], ax=ax1)
        ax1.set_title('Response Time Distribution by District')
        ax1.set_ylabel('Minutes')

        # Temporal Patterns
        sns.heatmap(
            self.results['temporal_patterns'],
            cmap='YlOrRd',
            annot=True,
            fmt='.2f',
            ax=ax2
        )

        plt.tight_layout()
        return fig
        processor = EMSDataProcessor('paste.txt')
df = processor.load_data()
analyzer = EMSAnalyzer(df)
results = {
    'response_metrics': analyzer.compute_response_metrics(),
    'disease_patterns': analyzer.analyze_disease_patterns()
}
class EMSVisualizer:
    def __init__(self, analysis_results):
        self.results = analysis_results
        plt.style.use('seaborn')

    def generate_response_time_analysis(self):
        """
        Generate statistical visualization for response times
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

        # Response Time Distribution
        sns.boxplot(data=self.results['temporal_metrics'], ax=ax1)
        ax1.set_title('Response Time Distribution by District')
        ax1.set_ylabel('Minutes')

        # Temporal Patterns
        sns.heatmap(
            self.results['temporal_patterns'],
            cmap='YlOrRd',
            annot=True,
            fmt='.2f',
            ax=ax2
        )

        plt.tight_layout()
        return fig
        processor = EMSDataProcessor('paste.txt')
df = processor.load_data()
analyzer = EMSAnalyzer(df)
results = {
    'response_metrics': analyzer.compute_response_metrics(),
    'disease_patterns': analyzer.analyze_disease_patterns()
}
visualizer = EMSVisualizer(results)
visualizer.generate_response_time_analysis()
plt.savefig('ems_analysis.png', dpi=300, bbox_inches='tight')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import chardet

class EMSDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.encoding = self._detect_encoding()

    def _detect_encoding(self):
        with open(self.file_path, 'rb') as file:
            return chardet.detect(file.read())['encoding']

    def load_data(self):
        """
        Systematic data loading with encoding validation
        Returns: DataFrame with standardized structure
        """
        encodings = [self.encoding, 'utf-8', 'cp1251', 'windows-1251']

        for encoding in encodings:
            try:
                return pd.read_csv(self.file_path,
                                 encoding=encoding,
                                 sep='\t',
                                 parse_dates=['Час створення заявки',
                                            'Час виїзду',
                                            'Час прибуття'],
                                 date_parser=lambda x: pd.to_datetime(x, format='%H:%M:%S',
                                                                    errors='coerce'))
            except Exception as e:
                continue

        raise ValueError("Data encoding validation failed across all standard encodings")

class EMSAnalyzer:
    def __init__(self, df):
        self.df = df
        self.results = {
            'temporal_metrics': {},
            'geographical_distribution': {},
            'clinical_patterns': {},
            'resource_utilization': {}
        }

    def compute_response_metrics(self):
        """
        Calculate standardized response time metrics
        Returns: DataFrame with statistical indicators
        """
        self.df['response_time'] = (
            pd.to_datetime(self.df['Час прибуття']) -
            pd.to_datetime(self.df['Час виїзду'])
        ).dt.total_seconds() / 60

        return pd.DataFrame({
            'mean_response': self.df.groupby('Район')['response_time'].mean(),
            'median_response': self.df.groupby('Район')['response_time'].median(),
            'std_response': self.df.groupby('Район')['response_time'].std()
        })

    def analyze_disease_patterns(self):
        """
        Comprehensive disease distribution analysis
        Returns: Dictionary of analytical results
        """
        return {
            'district_distribution': pd.crosstab(
                self.df['Район'],
                self.df['МКХ-10'],
                normalize='index'
            ),
            'urgency_stratification': pd.crosstab(
                [self.df['Район'], self.df['МКХ-10']],
                self.df['Помощь по диагнозу(Срочная, несрочная).']
            )
        }

class EMSVisualizer:
    def __init__(self, analysis_results):
        self.results = analysis_results
        plt.style.use('seaborn')

    def generate_response_time_analysis(self):
        """
        Generate statistical visualization for response times
        Returns: matplotlib figure object
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

        sns.boxplot(data=self.results['temporal_metrics'], ax=ax1)
        ax1.set_title('Response Time Distribution by District')
        ax1.set_ylabel('Minutes')

        sns.heatmap(
            self.results['temporal_patterns'],
            cmap='YlOrRd',
            annot=True,
            fmt='.2f',
            ax=ax2
        )

        plt.tight_layout()
        return fig

# Implementation
def main():
    # Data Processing
    processor = EMSDataProcessor('paste.txt')
    df = processor.load_data()

    # Analysis
    analyzer = EMSAnalyzer(df)
    results = {
        'response_metrics': analyzer.compute_response_metrics(),
        'disease_patterns': analyzer.analyze_disease_patterns()
    }

    # Visualization
    visualizer = EMSVisualizer(results)
    fig = visualizer.generate_response_time_analysis()
    plt.savefig('ems_analysis.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
from datetime import datetime
import chardet

class EMSDataLoader:
    """
    Методологічний компонент завантаження та валідації даних ЕМД

    Параметри:
    - file_path: шлях до файлу даних
    - encoding_attempts: список можливих кодувань
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.encoding_attempts = ['utf-8', 'cp1251', 'windows-1251']
        self.validation_metrics = {
            'missing_values': 0,
            'invalid_times': 0,
            'data_quality_score': 0
        }

    def load_and_validate(self):
        """
        Завантаження даних з валідацією часових показників

        Повертає:
        - DataFrame з валідованими даними
        """
        # Визначення кодування
        with open(self./content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        # Завантаження даних
        df = pd.read_csv(self.file_path,
                        encoding=encoding,
                        sep='\t',
                        parse_dates=['Час створення заявки',
                                   'Час виїзду',
                                   'Час прибуття'])

        # Валідація часових даних
        df['valid_times'] = pd.notnull(df['Час виїзду']) & \
                           pd.notnull(df['Час прибуття'])

        self.validation_metrics['missing_values'] = df['valid_times'].isna().sum()
        self.validation_metrics['data_quality_score'] = \
            (1 - df['valid_times'].isna().mean()) * 100

        return df[df['valid_times']]

# Використання:
loader = EMSDataLoader('paste.txt')
validated_data = loader.load_and_validate()
print(f"Якість даних: {loader.validation_metrics['data_quality_score']:.2f}%")

class ResponseTimeAnalyzer:
    """
    Аналітичний компонент для розрахунку часу реагування

    Методологічні параметри:
    - response_threshold: нормативний час реагування (хвилини)
    - urgency_categories: категорії терміновості
    """
    def __init__(self, df, response_threshold=20):
        self.df = df
        self.response_threshold = response_threshold
        self.results = {
            'mean_response': None,
            'compliance_rate': None,
            'urgency_stratification': None
        }

    def compute_metrics(self):
        """
        Розрахунок статистичних показників часу реагування
        """
        # Розрахунок часу реагування
        self.df['response_time'] = (
            pd.to_datetime(self.df['Час прибуття']) -
            pd.to_datetime(self.df['Час виїзду'])
        ).dt.total_seconds() / 60

        # Статистичний аналіз
        urgency_groups = self.df.groupby('Помощь по диагнозу(Срочная, несрочная).')

        self.results['mean_response'] = urgency_groups['response_time'].mean()
        self.results['compliance_rate'] = (
            self.df['response_time'] <= self.response_threshold
        ).mean() * 100

        # Стратифікація за терміновістю
        self.results['urgency_stratification'] = pd.DataFrame({
            'mean_time': urgency_groups['response_time'].mean(),
            'median_time': urgency_groups['response_time'].median(),
            'std_time': urgency_groups['response_time'].std(),
            'compliance': urgency_groups.apply(
                lambda x: (x['response_time'] <= self.response_threshold).mean() * 100
            )
        })

        return self.results

# Використання:
analyzer = ResponseTimeAnalyzer(validated_data)
response_metrics = analyzer.compute_metrics()

import matplotlib.pyplot as plt
import seaborn as sns

class EMSResponseVisualizer:
    """
    Компонент візуалізації результатів аналізу часу реагування

    Параметри візуалізації:
    - figure_size: розмір графіків
    - color_palette: палітра кольорів
    """
    def __init__(self, analysis_results):
        self.results = analysis_results
        plt.style.use('seaborn')

    def generate_report(self):
        """
        Створення комплексної візуалізації результатів
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12))

        # Розподіл часу реагування
        sns.boxplot(
            data=self.results['urgency_stratification'],
            y='mean_time',
            ax=ax1
        )
        ax1.set_title('Розподіл Часу Реагування за Терміновістю')
        ax1.set_ylabel('Хвилини')

        # Відповідність нормативам
        compliance_data = self.results['urgency_stratification']['compliance']
        compliance_data.plot(
            kind='bar',
            ax=ax2,
            color='darkblue',
            alpha=0.7
        )
        ax2.set_title('Відповідність Нормативному Часу Реагування (%)')
        ax2.set_ylabel('Відсоток відповідності')

        plt.tight_layout()
        plt.savefig('response_time_analysis.png', dpi=300, bbox_inches='tight')

        return fig

# Використання:
visualizer = EMSResponseVisualizer(response_metrics)
fig = visualizer.generate_report()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import chardet

class EMSResponseAnalysis:
    """
    Комплексний аналіз часу реагування служби ЕМД

    Методологічні параметри:
    - data_path: шлях до файлу даних
    - mapping_path: шлях до файлу картування районів
    - temporal_resolution: часова деталізація аналізу
    """
    def __init__(self, data_path, mapping_path):
        self.data_path = data_path
        self.mapping_path = mapping_path
        self.validation_metrics = {
            'sample_size': 0,
            'missing_data': {},
            'data_quality': {}
        }

    def load_and_validate(self):
        """
        Валідація та завантаження даних з множинною перевіркою кодування

        Повертає:
        DataFrame: Валідований набір даних
        """
        try:
            # Завантаження даних ЕМД
            df_ems = pd.read_csv(self.data_path,
                               encoding='utf-8',
                               sep='\t',
                               parse_dates=['Час створення заявки',
                                          'Час виїзду',
                                          'Час прибуття'])

            # Завантаження картування районів
            df_mapping = pd.read_csv(self.mapping_path,
                                   encoding='utf-8')

            # Валідація даних
            self.validation_metrics['sample_size'] = len(df_ems)
            self.validation_metrics['missing_data'] = df_ems.isnull().sum()

            # Об'єднання з картуванням районів
            df_merged = pd.merge(df_ems,
                               df_mapping,
                               how='left',
                               left_on='Населений пункт',
                               right_on='settlement')

            return df_merged

        except UnicodeDecodeError:
            # Спроба альтернативних кодувань
            encodings = ['cp1251', 'windows-1251', 'latin1']
            for encoding in encodings:
                try:
                    df_ems = pd.read_csv(self.data_path,
                                       encoding=encoding,
                                       sep='\t')
                    return self.load_and_validate()
                except:
                    continue
            raise ValueError("Не вдалося визначити коректне кодування файлу")

    def compute_response_metrics(self, df):
        """
        Розрахунок метрик часу реагування

        Параметри:
        - df: DataFrame з валідованими даними

        Повертає:
        Dict: Статистичні показники часу реагування
        """
        # Розрахунок часу реагування
        df['response_time'] = (
            pd.to_datetime(df['Час прибуття']) -
            pd.to_datetime(df['Час виїзду'])
        ).dt.total_seconds() / 60

        # Статистичний аналіз
        metrics = {
            'district_response': df.groupby('district_new')['response_time'].agg([
                'mean',
                'median',
                'std',
                'count'
            ]),
            'urgency_response': pd.crosstab(
                df['district_new'],
                df['Помощь по диагнозу(Срочная, несрочная).'],
                values=df['response_time'],
                aggfunc='mean'
            )
        }

        return metrics

# Використання:
analysis = EMSResponseAnalysis(
    data_path='/content/drive/MyDrive/Colab Notebooks/paste.txt',
    mapping_path='/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv'
)

# Завантаження та валідація даних
validated_data = analysis.load_and_validate()

# Розрахунок метрик
response_metrics = analysis.compute_response_metrics(validated_data)

# Виведення результатів
print("\nСтатистика часу реагування за районами:")
print(response_metrics['district_response'])

print("\nЧас реагування за терміновістю:")
print(response_metrics['urgency_response'])


import pandas as pd
import polars as pl
import numpy as np
import chardet
import codecs
from pathlib import Path
import csv

class DataDecodingAnalysis:
    """
    Comprehensive methodological approach to file decoding and loading
    utilizing multiple libraries and encoding detection methods.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.encoding_attempts = [
            'utf-8', 'cp1251', 'windows-1251', 'latin1',
            'iso-8859-1', 'utf-16', 'ascii'
        ]
        self.results = {
            'successful_method': None,
            'encoding_used': None,
            'data_shape': None,
            'column_names': None
        }

    def attempt_all_methods(self):
        """
        Systematic attempt of all possible loading methods
        with detailed error logging and success validation.
        """
        methods = [
            self._try_pandas_basic,
            self._try_pandas_engine,
            self._try_polars,
            self._try_raw_python,
            self._try_chardet_method,
            self._try_codecs_method
        ]

        for method in methods:
            try:
                result = method()
                if result is not None:
                    print(f"✓ Success with method: {method.__name__}")
                    print(f"Encoding detected: {self.results['encoding_used']}")
                    return result
            except Exception as e:
                print(f"✗ {method.__name__} failed: {str(e)}")
                continue

        raise ValueError("All loading methods failed")

    def _try_pandas_basic(self):
        """Method 1: Basic Pandas with multiple encodings"""
        for encoding in self.encoding_attempts:
            try:
                df = pd.read_csv(self.file_path, encoding=encoding)
                self.results.update({
                    'successful_method': 'pandas_basic',
                    'encoding_used': encoding,
                    'data_shape': df.shape
                })
                return df
            except:
                continue
        return None

    def _try_pandas_engine(self):
        """Method 2: Pandas with different engines"""
        engines = ['python', 'c']
        for engine in engines:
            for encoding in self.encoding_attempts:
                try:
                    df = pd.read_csv(
                        self.file_path,
                        encoding=encoding,
                        engine=engine,
                        on_bad_lines='skip'
                    )
                    self.results.update({
                        'successful_method': f'pandas_{engine}',
                        'encoding_used': encoding,
                        'data_shape': df.shape
                    })
                    return df
                except:
                    continue
        return None

    def _try_polars(self):
        """Method 3: Polars library attempt"""
        try:
            df = pl.read_csv(self.file_path)
            self.results.update({
                'successful_method': 'polars',
                'encoding_used': 'auto-detected',
                'data_shape': df.shape
            })
            return df.to_pandas()
        except:
            return None

    def _try_raw_python(self):
        """Method 4: Raw Python reading"""
        for encoding in self.encoding_attempts:
            try:
                with open(self.file_path, 'r', encoding=encoding) as file:
                    data = list(csv.reader(file))
                    df = pd.DataFrame(data[1:], columns=data[0])
                    self.results.update({
                        'successful_method': 'raw_python',
                        'encoding_used': encoding,
                        'data_shape': df.shape
                    })
                    return df
            except:
                continue
        return None

    def _try_chardet_method(self):
        """Method 5: Chardet detection"""
        try:
            with open(self.file_path, 'rb') as file:
                raw_data = file.read()
                detected = chardet.detect(raw_data)
                df = pd.read_csv(self.file_path, encoding=detected['encoding'])
                self.results.update({
                    'successful_method': 'chardet',
                    'encoding_used': detected['encoding'],
                    'data_shape': df.shape
                })
                return df
        except:
            return None

    def _try_codecs_method(self):
        """Method 6: Codecs library attempt"""
        for encoding in self.encoding_attempts:
            try:
                with codecs.open(self.file_path, 'r', encoding=encoding) as file:
                    df = pd.read_csv(file)
                    self.results.update({
                        'successful_method': 'codecs',
                        'encoding_used': encoding,
                        'data_shape': df.shape
                    })
                    return df
            except:
                continue
        return None

# Використання:
file_path = '/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv'
decoder = DataDecodingAnalysis(file_path)

try:
    df = decoder.attempt_all_methods()
    print("\nSuccessful Loading Results:")
    print(f"Data Shape: {decoder.results['data_shape']}")
    print(f"Method Used: {decoder.results['successful_method']}")
    print(f"Encoding: {decoder.results['encoding_used']}")
    print("\nFirst few rows of data:")
    print(df.head())
except Exception as e:
    print(f"Final Error: {str(e)}")

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних з підтвердженим методом
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv',
                 encoding='cp1251',
                 sep='\t')

# Видалення технічних рядків та підготовка даних
df = df[df['дата'].notna()]  # Видаляємо рядок з описом колонок
df = df[df['дата'] != 'дата']  # Видаляємо можливі додаткові заголовки

# Розрахунок часу реагування
def calculate_response_time(row):
    try:
        arrival = datetime.strptime(str(row['Время прибытия в формате 09:55:45']), '%H:%M:%S')
        dispatch = datetime.strptime(str(row['Время выезда в формате 09:55:45']), '%H:%M:%S')
        return (arrival - dispatch).total_seconds() / 60
    except:
        return np.nan

df['response_time'] = df.apply(calculate_response_time, axis=1)

# Базова статистика
response_stats = {
    'overall_mean': df['response_time'].mean(),
    'overall_median': df['response_time'].median(),
    'std_dev': df['response_time'].std(),

    # Розподіл за терміновістю
    'urgency_stats': df.groupby('Помощь по диагнозу(Срочная, несрочная).')['response_time'].agg([
        'mean', 'median', 'std', 'count'
    ]),

    # Розподіл за районами
    'district_stats': df.groupby('Район')['response_time'].agg([
        'mean', 'median', 'std', 'count'
    ]),

    # Статистика відповідності нормативам
    'compliance_rate': (df['response_time'] <= 20).mean() * 100
}

# Візуалізація
plt.figure(figsize=(15, 10))
sns.boxplot(data=df, x='Район', y='response_time')
plt.xticks(rotation=45, ha='right')
plt.title('Розподіл часу реагування за районами')
plt.tight_layout()
plt.savefig('response_time_analysis.png')

print("\nСтатистика часу реагування:")
print(f"Середній час реагування: {response_stats['overall_mean']:.2f} хвилин")
print(f"Медіанний час реагування: {response_stats['overall_median']:.2f} хвилин")
print(f"Відповідність нормативу: {response_stats['compliance_rate']:.2f}%")

print("\nСтатистика за терміновістю:")
print(response_stats['urgency_stats'])

print("\nСтатистика за районами:")
print(response_stats['district_stats'])

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних перевіреним методом
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv',
                 encoding='cp1251',
                 sep='\t')

# Спочатку подивимось які колонки є в датафреймі
print("Наявні колонки:")
print(df.columns.tolist())

# Підготовка даних - видалення технічних рядків
df = df.iloc[1:]  # Видаляємо перший рядок з описом

# Розрахунок часу реагування
def calculate_response_time(row):
    try:
        arrival = row['Время прибытия в формате 09:55:45']
        dispatch = row['Время выезда в формате 09:55:45']
        if pd.notna(arrival) and pd.notna(dispatch):
            arrival_time = datetime.strptime(str(arrival), '%H:%M:%S')
            dispatch_time = datetime.strptime(str(dispatch), '%H:%M:%S')
            return (arrival_time - dispatch_time).total_seconds() / 60
    except:
        return np.nan

# Додаємо розрахунок часу реагування
df['response_time'] = df.apply(calculate_response_time, axis=1)

# Базова статистика
response_stats = {
    'overall_stats': {
        'mean': df['response_time'].mean(),
        'median': df['response_time'].median(),
        'std': df['response_time'].std()
    },

    # Розподіл за терміновістю
    'urgency_stats': df.groupby('Помощь по диагнозу(Срочная, несрочная).')['response_time'].agg([
        'count',
        'mean',
        'median',
        'std'
    ]).round(2),

    # Розподіл за районами
    'district_stats': df.groupby('Район')['response_time'].agg([
        'count',
        'mean',
        'median',
        'std'
    ]).round(2)
}

# Виведення результатів
print("\nЗагальна статистика часу реагування:")
print(f"Середній час: {response_stats['overall_stats']['mean']:.2f} хвилин")
print(f"Медіанний час: {response_stats['overall_stats']['median']:.2f} хвилин")
print(f"Стандартне відхилення: {response_stats['overall_stats']['std']:.2f} хвилин")

print("\nСтатистика за терміновістю:")
print(response_stats['urgency_stats'])

print("\nСтатистика за районами:")
print(response_stats['district_stats'])

# Візуалізація
plt.figure(figsize=(15, 10))
sns.boxplot(data=df, x='Район', y='response_time')
plt.xticks(rotation=45, ha='right')
plt.title('Розподіл часу реагування за районами')
plt.tight_layout()
plt.savefig('response_time_analysis.png')

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Завантаження даних з правильним розділювачем
df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv',
                 encoding='cp1251',
                 sep=',')  # Змінили розділювач на кому

# Очищення назв колонок
df.columns = df.columns.str.strip()

# Підготовка часових даних
def clean_time(time_str):
    try:
        # Видаляємо 'AM' та 'PM' якщо вони є
        time_str = time_str.replace(' AM', '').replace(' PM', '')
        return datetime.strptime(time_str, '%H:%M:%S')
    except:
        return np.nan

# Розрахунок часу реагування
def calculate_response_time(row):
    dispatch = row['Время выезда в формате 09:55:45']
    arrival = row['Время прибытия в формате 09:55:45']

    if pd.notna(dispatch) and pd.notna(arrival):
        dispatch_time = clean_time(str(dispatch))
        arrival_time = clean_time(str(arrival))
        if dispatch_time and arrival_time:
            delta = arrival_time - dispatch_time
            return delta.total_seconds() / 60
    return np.nan

# Аналіз часу реагування
df['response_time'] = df.apply(calculate_response_time, axis=1)

# Базова статистика
response_metrics = {
    'overall': {
        'mean': df['response_time'].mean(),
        'median': df['response_time'].median(),
        'std': df['response_time'].std(),
        'count': df['response_time'].count()
    }
}

# Групування за районами
district_stats = df.groupby('Район')['response_time'].agg([
    'count',
    'mean',
    'median',
    'std'
]).round(2)

# Розрахунок відповідності нормативу (20 хвилин)
response_metrics['compliance'] = (df['response_time'] <= 20).mean() * 100

print("\nІндикатор часу реагування ЕМД")
print("-" * 50)
print(f"Загальна кількість викликів: {response_metrics['overall']['count']}")
print(f"Середній час реагування: {response_metrics['overall']['mean']:.2f} хвилин")
print(f"Медіанний час: {response_metrics['overall']['median']:.2f} хвилин")
print(f"Стандартне відхилення: {response_metrics['overall']['std']:.2f} хвилин")
print(f"Відповідність нормативу: {response_metrics['compliance']:.1f}%")

print("\nРозподіл за районами:")
print(district_stats)

# Візуалізація
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Район', y='response_time')
plt.xticks(rotation=45, ha='right')
plt.title('Розподіл часу реагування за районами')
plt.ylabel('Час реагування (хвилини)')
plt.tight_layout()
plt.savefig('response_time_district.png')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class EMSResponseAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        # Завантаження та базова валідація
        self.df = pd.read_csv(self.data_path, encoding='cp1251', sep=',')
        self.df = self.df.iloc[2:]  # Видалення службових рядків

        # Аналіз пропущених значень
        self.missing_analysis = {
            'total_records': len(self.df),
            'missing_by_column': self.df.isnull().sum(),
            'missing_district': self.df['Район'].isnull().sum(),
            'missing_times': {
                'dispatch': self.df['Время выезда в формате 09:55:45'].isnull().sum(),
                'arrival': self.df['Время прибытия в формате 09:55:45'].isnull().sum()
            }
        }

    def calculate_response_metrics(self):
        # Розрахунок часу реагування
        def parse_time(time_str):
            try:
                clean_time = str(time_str).replace(' AM', '').replace(' PM', '')
                parts = clean_time.split(':')
                return int(parts[0]) * 60 + int(parts[1])
            except:
                return np.nan

        self.df['response_time'] = (
            self.df['Время прибытия в формате 09:55:45'].apply(parse_time) -
            self.df['Время выезда в формате 09:55:45'].apply(parse_time)
        )

        # Корекція нічних викликів
        self.df.loc[self.df['response_time'] < -1000, 'response_time'] += 1440

        # Розрахунок квартилів та IQR
        self.response_stats = {
            'overall': {
                'mean': self.df['response_time'].mean(),
                'median': self.df['response_time'].median(),
                'std': self.df['response_time'].std(),
                'q1': self.df['response_time'].quantile(0.25),
                'q3': self.df['response_time'].quantile(0.75),
                'iqr': self.df['response_time'].quantile(0.75) -
                       self.df['response_time'].quantile(0.25)
            }
        }

        # Територіальний аналіз
        self.district_stats = self.df.groupby('Район')['response_time'].agg([
            'count',
            'mean',
            'median',
            'std',
            lambda x: x.quantile(0.25),
            lambda x: x.quantile(0.75)
        ]).round(2)
        self.district_stats.columns = ['count', 'mean', 'median', 'std', 'Q1', 'Q3']
        self.district_stats['IQR'] = self.district_stats['Q3'] - self.district_stats['Q1']

        # Аналіз екстремальних значень
        self.outliers = self.df[
            (self.df['response_time'] >
             self.df['response_time'].quantile(0.75) + 1.5 * self.response_stats['overall']['iqr'])
        ]

    def visualize_distributions(self):
        plt.figure(figsize=(15, 10))

        # Основний графік
        sns.boxplot(data=self.df,
                   x='Район',
                   y='response_time',
                   showfliers=True)

        plt.axhline(y=20, color='r', linestyle='--', label='Норматив (20 хв)')
        plt.xticks(rotation=45, ha='right')
        plt.title('Розподіл часу реагування за районами')
        plt.ylabel('Час реагування (хвилини)')
        plt.legend()

        return plt.gcf()

# Імплементація
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.calculate_response_metrics()

print("\nАналіз якості даних:")
print(f"Загальна кількість записів: {analyzer.missing_analysis['total_records']}")
print(f"Пропущені райони: {analyzer.missing_analysis['missing_district']}")
print(f"Пропущені часи виїзду: {analyzer.missing_analysis['missing_times']['dispatch']}")
print(f"Пропущені часи прибуття: {analyzer.missing_analysis['missing_times']['arrival']}")

print("\nЗагальні статистичні показники:")
print(f"Середній час реагування: {analyzer.response_stats['overall']['mean']:.2f} хв")
print(f"Медіана (Q2): {analyzer.response_stats['overall']['median']:.2f} хв")
print(f"Міжквартильний розмах: {analyzer.response_stats['overall']['iqr']:.2f} хв")
print(f"Стандартне відхилення: {analyzer.response_stats['overall']['std']:.2f} хв")

print("\nТериторіальний розподіл:")
print(analyzer.district_stats)

# Візуалізація
fig = analyzer.visualize_distributions()
plt.savefig('response_time_detailed.png', dpi=300, bbox_inches='tight')

import polars as pl
import numpy as np
from datetime import datetime
import plotnine as p
from plotnine import *

class EMSResponseAnalysis:
    """
    Комплексний аналіз часу реагування ЕМД з використанням
    високопродуктивних бібліотек обробки даних
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.metrics = {}

    def load_data(self):
        """
        Оптимізоване завантаження даних через Polars
        з валідацією структурної цілісності
        """
        try:
            # Завантаження через Polars з автоматичним виявленням схеми
            self.df = pl.read_csv(
                self.data_path,
                encoding='cp1251',
                separator=',',
                skip_rows=2,
                low_memory=True
            )

            # Валідація структури даних
            self.data_quality = {
                'total_records': len(self.df),
                'missing_values': self.df.null_count(),
                'schema_validation': self.df.schema
            }

            return self

        except Exception as e:
            print(f"Помилка завантаження даних: {str(e)}")
            raise

    def calculate_response_time(self):
        """
        Розрахунок часових метрик з використанням
        векторизованих операцій Polars
        """
        def parse_time_polars(s):
            return pl.col(s).str.replace(' AM', '').str.replace(' PM', '')\
                   .str.split(':').list.get(0).cast(pl.Int64) * 60 + \
                   pl.col(s).str.split(':').list.get(1).cast(pl.Int64)

        # Векторизований розрахунок часу реагування
        self.df = self.df.with_columns([
            parse_time_polars('Время выезда в формате 09:55:45')\
                .alias('dispatch_minutes'),
            parse_time_polars('Время прибытия в формате 09:55:45')\
                .alias('arrival_minutes')
        ])

        # Розрахунок різниці з корекцією нічних викликів
        self.df = self.df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))\
                .alias('response_time')
        ])

        self.df = self.df.with_columns([
            pl.when(pl.col('response_time') < -1000)\
              .then(pl.col('response_time') + 1440)\
              .otherwise(pl.col('response_time'))\
              .alias('response_time')
        ])

        return self

    def compute_statistics(self):
        """
        Розрахунок комплексних статистичних показників
        з використанням агрегації Polars
        """
        # Загальні статистичні показники
        self.metrics['overall'] = self.df.select([
            pl.col('response_time').mean().alias('mean'),
            pl.col('response_time').median().alias('median'),
            pl.col('response_time').std().alias('std'),
            pl.col('response_time').quantile(0.25).alias('q1'),
            pl.col('response_time').quantile(0.75).alias('q3')
        ]).collect()

        # Територіальний розподіл
        self.metrics['district'] = self.df.groupby('Район').agg([
            pl.col('response_time').count().alias('n'),
            pl.col('response_time').mean().alias('mean'),
            pl.col('response_time').median().alias('median'),
            pl.col('response_time').std().alias('std'),
            pl.col('response_time').quantile(0.25).alias('q1'),
            pl.col('response_time').quantile(0.75).alias('q3')
        ]).sort('n', descending=True)

        return self

    def visualize(self):
        """
        Статистична візуалізація з використанням plotnine
        для створення публікаційної якості графіків
        """
        # Конвертація в pandas для plotnine
        df_plot = self.df.select(['Район', 'response_time']).to_pandas()

        # Створення візуалізації
        plot = (ggplot(df_plot, aes(x='Район', y='response_time'))
                + geom_violin(alpha=0.6)
                + geom_boxplot(width=0.2, alpha=0.8)
                + theme_minimal()
                + theme(axis_text_x=element_text(angle=45, hjust=1))
                + labs(title='Розподіл часу реагування за районами',
                      x='Район',
                      y='Час реагування (хвилини)')
                + geom_hline(yintercept=20, linetype='dashed',
                           color='red', size=1))

        return plot

# Імплементація аналізу
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.load_data()
analyzer.calculate_response_time()
analyzer.compute_statistics()

# Виведення результатів
print("\nЯкість даних:")
print(f"Загальна кількість записів: {analyzer.data_quality['total_records']}")
print("\nСтатистичні показники за районами:")
print(analyzer.metrics['district'])

# Візуалізація
plot = analyzer.visualize()
plot.save('response_time_distribution.png',
         dpi=300, height=10, width=15)

import polars as pl
import numpy as np
from datetime import datetime
import plotnine as p
from plotnine import *

class EMSResponseAnalysis:
    """
    Методологічний аналіз часу реагування екстреної медичної допомоги
    з використанням високопродуктивних інструментів аналізу даних
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.metrics = {}

    def load_data(self):
        """
        Завантаження даних з валідацією структури
        """
        try:
            # Визначаємо назви колонок перед завантаженням
            self.df = pl.read_csv(
                self.data_path,
                encoding='cp1251',
                separator=',',
                skip_rows=2,
                has_header=True
            )

            # Виводимо наявні колонки для діагностики
            print("Наявні колонки:")
            print(self.df.columns)

            # Базова валідація даних
            self.data_quality = {
                'total_records': len(self.df),
                'missing_values': self.df.null_count(),
                'columns_found': self.df.columns
            }

            return self

        except Exception as e:
            print(f"Помилка завантаження даних: {str(e)}")
            raise

    def calculate_response_time(self):
        """
        Оптимізований розрахунок часових показників
        """
        # Знаходимо правильні назви колонок для часу
        time_columns = [col for col in self.df.columns
                       if 'выезд' in col.lower() or 'прибыт' in col.lower()]

        if len(time_columns) < 2:
            raise ValueError("Не знайдено необхідних часових колонок")

        dispatch_col = time_columns[0]
        arrival_col = time_columns[1]

        def parse_time_polars(s):
            return pl.col(s).str.replace(' AM', '').str.replace(' PM', '')\
                   .str.split(':').list.get(0).cast(pl.Int64) * 60 + \
                   pl.col(s).str.split(':').list.get(1).cast(pl.Int64)

        # Розрахунок з використанням знайдених колонок
        self.df = self.df.with_columns([
            parse_time_polars(dispatch_col).alias('dispatch_minutes'),
            parse_time_polars(arrival_col).alias('arrival_minutes')
        ])

        self.df = self.df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))\
                .alias('response_time')
        ])

        # Корекція нічних викликів
        self.df = self.df.with_columns([
            pl.when(pl.col('response_time') < -1000)\
              .then(pl.col('response_time') + 1440)\
              .otherwise(pl.col('response_time'))\
              .alias('response_time')
        ])

        return self

    def compute_statistics(self):
        """
        Комплексний статистичний аналіз
        """
        district_col = [col for col in self.df.columns if 'район' in col.lower()][0]

        # Загальні метрики
        self.metrics['overall'] = self.df.select([
            pl.col('response_time').mean().alias('mean'),
            pl.col('response_time').median().alias('median'),
            pl.col('response_time').std().alias('std'),
            pl.col('response_time').quantile(0.25).alias('q1'),
            pl.col('response_time').quantile(0.75).alias('q3')
        ]).collect()

        # Територіальний розподіл
        self.metrics['district'] = self.df.groupby(district_col).agg([
            pl.col('response_time').count().alias('n'),
            pl.col('response_time').mean().alias('mean'),
            pl.col('response_time').median().alias('median'),
            pl.col('response_time').std().alias('std'),
            pl.col('response_time').quantile(0.25).alias('q1'),
            pl.col('response_time').quantile(0.75).alias('q3')
        ]).sort('n', descending=True)

        return self

# Імплементація
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.load_data()
print("\nСтруктура даних завантажена успішно")
analyzer.calculate_response_time()
analyzer.compute_statistics()

# Виведення результатів
print("\nСтатистичні показники за районами:")
print(analyzer.metrics['district'])

import polars as pl
import numpy as np
from datetime import datetime
import plotnine as p
from plotnine import *

class EMSResponseTimeAnalysis:
    """
    Методологічний аналіз часових показників реагування ЕМД
    з урахуванням структурних особливостей даних
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.metrics = {}

    def load_and_validate(self):
        """
        Структурована валідація та стандартизація даних

        Методологічні параметри:
        - Кодування: cp1251
        - Пропуск технічних рядків: 2
        - Валідація дублікатів колонок
        """
        # Завантаження з розширеною діагностикою
        self.df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Стандартизація назв колонок
        self.column_mapping = {
            '0:03:54': 'dispatch_time',
            '0:31:15': 'arrival_time',
            'Миколаївський район': 'district'
        }

        # Структурна валідація
        self.data_quality = {
            'total_records': len(self.df),
            'duplicate_columns': [col for col in self.df.columns if '_duplicated_' in col],
            'time_columns': [col for col in self.df.columns if ':' in col]
        }

        print("\nДіагностика структури даних:")
        print(f"Загальна кількість записів: {self.data_quality['total_records']}")
        print("\nЧасові колонки:")
        for col in self.data_quality['time_columns']:
            print(f"- {col}")

        return self

    def process_time_columns(self):
        """
        Спеціалізована обробка часових показників

        Методологічні особливості:
        - Видалення суфіксів AM/PM
        - Стандартизація формату часу
        - Валідація часових інтервалів
        """
        def standardize_time(time_str):
            if isinstance(time_str, str):
                time_str = time_str.replace(' AM', '').replace(' PM', '')
                try:
                    hours, minutes = map(int, time_str.split(':')[:2])
                    return hours * 60 + minutes
                except:
                    return None
            return None

        # Ідентифікація релевантних часових колонок
        dispatch_col = '0:03:54'  # Визначено з структури даних
        arrival_col = '0:31:15'   # Визначено з структури даних

        # Конвертація часових показників
        self.df = self.df.with_columns([
            pl.col(dispatch_col).map_elements(standardize_time).alias('dispatch_minutes'),
            pl.col(arrival_col).map_elements(standardize_time).alias('arrival_minutes')
        ])

        # Розрахунок часу реагування
        self.df = self.df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes')).alias('response_time')
        ])

        # Корекція нічних викликів
        self.df = self.df.with_columns([
            pl.when(pl.col('response_time') < -1000)
              .then(pl.col('response_time') + 1440)
              .otherwise(pl.col('response_time'))
              .alias('response_time')
        ])

        return self

# Імплементація
analyzer = EMSResponseTimeAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.load_and_validate()
analyzer.process_time_columns()

# Розрахунок базових статистик
response_stats = analyzer.df.select([
    pl.col('response_time').mean().alias('mean_response'),
    pl.col('response_time').median().alias('median_response'),
    pl.col('response_time').std().alias('std_response'),
    pl.col('response_time').quantile(0.25).alias('q1'),
    pl.col('response_time').quantile(0.75).alias('q3')
]).collect()

print("\nСтатистичні показники часу реагування:")
print(response_stats)

import polars as pl
import numpy as np
from datetime import datetime
import plotnine as p
from plotnine import *

class EMSResponseAnalysis:
    """
    Комплексний аналіз часових параметрів екстреної медичної допомоги
    з валідацією структурної цілісності даних (N=167,550)

    Методологічні параметри:
    - Темпоральна стратифікація
    - Географічна кластеризація
    - Статистична валідація
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.metrics = {}

    def load_and_validate(self):
        """
        Структурована валідація даних з акцентом на темпоральні характеристики
        """
        # Завантаження даних
        self.df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Ідентифікація та валідація часових колонок
        time_columns = [col for col in self.df.columns if ':' in str(col)]

        # Діагностика структури
        self.validation_metrics = {
            'sample_size': len(self.df),
            'time_columns': time_columns,
            'temporal_completeness': self.df.select(time_columns).null_count()
        }

        return self

    def process_temporal_data(self):
        """
        Спеціалізована обробка часових показників з валідацією
        """
        def standardize_time(time_str: str) -> float:
            """
            Стандартизація часових форматів з валідацією

            Параметри:
            - time_str: Часовий показник у string форматі

            Повертає:
            - float: Стандартизований час у хвилинах
            """
            try:
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                if ':' not in time_str:
                    return None
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return None

        # Ідентифікація ключових часових колонок
        dispatch_col = '0:03:54'  # Час виїзду
        arrival_col = '0:31:15'   # Час прибуття

        # Конвертація з валідацією
        self.df = self.df.with_columns([
            pl.col(dispatch_col)
              .map_elements(standardize_time, return_dtype=pl.Float64)
              .alias('dispatch_minutes'),
            pl.col(arrival_col)
              .map_elements(standardize_time, return_dtype=pl.Float64)
              .alias('arrival_minutes')
        ])

        # Розрахунок часу реагування
        self.df = self.df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))
            .alias('response_time')
        ])

        # Статистична валідація
        self.temporal_metrics = {
            'valid_records': self.df['response_time'].drop_nulls().len(),
            'mean_response': self.df['response_time'].mean(),
            'median_response': self.df['response_time'].median(),
            'q1': self.df['response_time'].quantile(0.25),
            'q3': self.df['response_time'].quantile(0.75)
        }

        return self

# Імплементація
analysis = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()
analysis.process_temporal_data()

# Виведення результатів
print("\nСтатистична валідація часу реагування ЕМД")
print("=" * 50)
print(f"\nОбсяг вибірки: {analysis.validation_metrics['sample_size']}")
print("\nЧасові показники:")
for metric, value in analysis.temporal_metrics.items():
    print(f"{metric}: {value:.2f}")

print("\nСтруктурна валідація:")
print(f"Валідні записи: {analysis.temporal_metrics['valid_records']}")
print(f"Рівень валідності: {(analysis.temporal_metrics['valid_records']/analysis.validation_metrics['sample_size'])*100:.1f}%")

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSResponseAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_and_process(self):
        # Завантаження та первинна обробка
        self.df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Стандартизація часових показників
        def standardize_time(time_str):
            try:
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return None

        # Обробка часових даних
        self.df = self.df.with_columns([
            pl.col('0:03:54').map_elements(standardize_time, return_dtype=pl.Float64)
            .alias('dispatch_minutes'),
            pl.col('0:31:15').map_elements(standardize_time, return_dtype=pl.Float64)
            .alias('arrival_minutes')
        ])

        # Розрахунок часу реагування
        self.df = self.df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes')).alias('response_time')
        ])

        # Конвертація в pandas для plotnine
        self.pdf = self.df.to_pandas()

        return self

    def create_visualization(self):
        # Базова візуалізація розподілу
        plot = (ggplot(self.pdf)
                # Розподіл часу реагування за районами
                + geom_violin(aes(x='Район', y='response_time', fill='Помощь по диагнозу(Срочная, несрочная).'),
                            alpha=0.6)
                + geom_boxplot(aes(x='Район', y='response_time', fill='Помощь по диагнозу(Срочная, несрочная).'),
                             width=0.2, alpha=0.7)
                # Нормативна лінія
                + geom_hline(yintercept=20, linetype='dashed', color='red')
                # Естетика
                + theme_minimal()
                + theme(axis_text_x=element_text(angle=45, hjust=1))
                + labs(title='Розподіл часу реагування за районами та терміновістю',
                      x='Район',
                      y='Час реагування (хвилини)',
                      fill='Терміновість'))

        return plot

    def calculate_statistics(self):
        # Розрахунок статистик за районами та терміновістю
        stats = self.df.groupby(['Район', 'Помощь по диагнозу(Срочная, несрочная).']).agg([
            pl.col('response_time').mean().alias('mean_time'),
            pl.col('response_time').median().alias('median_time'),
            pl.col('response_time').quantile(0.25).alias('q1'),
            pl.col('response_time').quantile(0.75).alias('q3'),
            pl.col('response_time').count().alias('n_calls')
        ])

        return stats

# Імплементація
analysis = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_process()

# Статистичний аналіз
stats = analysis.calculate_statistics()
print("\nСтатистика за районами та терміновістю:")
print(stats)

# Візуалізація
plot = analysis.create_visualization()
plot.save('ems_response_distribution.png',
         dpi=300, height=10, width=15)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSResponseAnalysis:
   def __init__(self, data_path):
       self.data_path = data_path

   def load_and_process(self):
       # Завантаження та первинна обробка
       df = pl.read_csv(
           self.data_path,
           encoding='cp1251',
           separator=',',
           skip_rows=2
       )

       # Стандартизація часових показників
       def standardize_time(time_str):
           try:
               time_str = str(time_str).replace(' AM', '').replace(' PM', '')
               hours, minutes = map(int, time_str.split(':')[:2])
               return float(hours * 60 + minutes)
           except:
               return None

       # Обробка часових даних
       df = df.with_columns([
           pl.col('0:03:54').map_elements(standardize_time, return_dtype=pl.Float64)
           .alias('dispatch_minutes'),
           pl.col('0:31:15').map_elements(standardize_time, return_dtype=pl.Float64)
           .alias('arrival_minutes')
       ])

       # Розрахунок часу реагування
       df = df.with_columns([
           (pl.col('arrival_minutes') - pl.col('dispatch_minutes')).alias('response_time')
       ])

       # Перетворення в pandas DataFrame для подальшого аналізу
       self.pdf = df.to_pandas()

       return self

   def analyze_and_visualize(self):
       # Розрахунок статистик
       stats = self.pdf.groupby(['Район', 'Помощь по диагнозу(Срочная, несрочная).']).agg({
           'response_time': ['count', 'mean', 'median', 'std',
                           lambda x: x.quantile(0.25),
                           lambda x: x.quantile(0.75)]
       }).round(2)

       stats.columns = ['n_calls', 'mean_time', 'median_time', 'std_time', 'q1', 'q3']

       # Візуалізація
       plot = (ggplot(self.pdf, aes(x='Район', y='response_time',
                                   fill='Помощь по диагнозу(Срочная, несрочная).'))
               + geom_violin(alpha=0.5)
               + geom_boxplot(width=0.2, alpha=0.7)
               + geom_hline(yintercept=20, linetype='dashed', color='red')
               + theme_minimal()
               + theme(axis_text_x=element_text(angle=45, hjust=1))
               + labs(title='Розподіл часу реагування за районами та терміновістю',
                     x='Район',
                     y='Час реагування (хвилини)',
                     fill='Терміновість'))

       return stats, plot

# Імплементація
analysis = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_process()
stats, plot = analysis.analyze_and_visualize()

print("\nСтатистичний аналіз часу реагування за районами та терміновістю:")
print(stats)

# Збереження візуалізації
plot.save('ems_response_analysis.png', dpi=300, height=10, width=15)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSAccessibilityAnalysis:
    """
    Методологічний аналіз територіальної доступності та
    ефективності екстреної медичної допомоги (N=167,550)

    Параметри валідації:
    - Територіальна стратифікація
    - Часова гранулярність
    - Демографічна репрезентативність
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        """
        Структурована валідація даних з акцентом на
        територіальну репрезентативність
        """
        # Імпорт даних з розширеною валідацією
        df = pl.read_csv(
            '/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv',
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Валідація структурної цілісності
        self.validation_metrics['sample_size'] = len(df)
        self.validation_metrics['districts'] = df['Миколаївський район'].unique()

        # Методологічна валідація часових показників
        def standardize_temporal_metrics(time_str):
            try:
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return None

        # Розрахунок часу реагування
        df = df.with_columns([
            pl.col('0:03:54').map_elements(standardize_temporal_metrics,
                                         return_dtype=pl.Float64)
            .alias('dispatch_minutes'),
            pl.col('0:31:15').map_elements(standardize_temporal_metrics,
                                         return_dtype=pl.Float64)
            .alias('arrival_minutes')
        ])

        # Інтеграція територіальних та часових метрик
        df = df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))
            .alias('response_time')
        ])

        # Конвертація для статистичного аналізу
        self.analytical_frame = df.select([
            pl.col('Миколаївський район').alias('district'),
            pl.col('19').alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_statistical_indices(self):
        """
        Розрахунок комплексних статистичних показників
        з територіальною стратифікацією
        """
        # Територіальна агрегація
        district_metrics = self.analytical_frame.groupby(['district', 'urgency']).agg({
            'response_time': [
                'count',          # Обсяг вибірки
                'mean',           # Середній час
                'median',         # Медіанний час
                'std',            # Стандартне відхилення
                lambda x: x.quantile(0.25),  # Q1
                lambda x: x.quantile(0.75)   # Q3
            ]
        }).round(2)

        # Стандартизація метрик
        district_metrics.columns = [
            'n_cases',
            'mean_response',
            'median_response',
            'std_dev',
            'q1_response',
            'q3_response'
        ]

        return district_metrics

    def visualize_territorial_distribution(self):
        """
        Комплексна візуалізація територіального розподілу
        з інтеграцією часових показників
        """
        visualization = (ggplot(self.analytical_frame,
                              aes(x='district',
                                  y='response_time',
                                  fill='urgency'))
                + geom_violin(alpha=0.5, position='dodge')
                + geom_boxplot(width=0.2, alpha=0.7, position='dodge')
                + geom_hline(yintercept=20,
                            linetype='dashed',
                            color='red',
                            alpha=0.8)
                + theme_minimal()
                + theme(
                    axis_text_x=element_text(angle=45, hjust=1),
                    plot_title=element_text(size=12),
                    plot_subtitle=element_text(size=10)
                )
                + labs(
                    title='Територіальна варіабельність доступності ЕМД',
                    subtitle='Стратифікований аналіз часу реагування за районами',
                    x='Територіальна одиниця',
                    y='Час реагування (хвилини)',
                    fill='Терміновість виклику'
                ))

        return visualization

# Імплементація методологічного аналізу
analysis = EMSAccessibilityAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

# Розрахунок статистичних показників
metrics = analysis.compute_statistical_indices()
print("\nТериторіальний розподіл статистичних показників:")
print(metrics)

# Візуалізація результатів
plot = analysis.visualize_territorial_distribution()
plot.save('territorial_accessibility_analysis.png',
         dpi=300, height=12, width=16)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    """
    Комплексний аналіз темпоральних паттернів надання екстреної медичної допомоги
    з акцентом на територіальну варіабельність (N=167,550)
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        """
        Методологічно валідоване завантаження даних з
        інтегрованою перевіркою структурної цілісності
        """
        # Розширена валідація при завантаженні
        df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Діагностика структури даних
        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        # Первинна валідація
        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        # Стандартизація часових показників
        def standardize_time(time_str):
            try:
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return None

        # Ідентифікація часових колонок
        time_cols = [col for col in df.columns if ':' in str(col)]

        # Валідована конвертація часових показників
        df = df.with_columns([
            pl.col('0:03:54').map_elements(standardize_time, return_dtype=pl.Float64)
            .alias('dispatch_minutes'),
            pl.col('0:31:15').map_elements(standardize_time, return_dtype=pl.Float64)
            .alias('arrival_minutes')
        ])

        # Розрахунок часу реагування
        df = df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))
            .alias('response_time')
        ])

        # Підготовка для аналізу
        district_col = df.columns[3]  # Колонка району
        urgency_col = df.columns[18]  # Колонка терміновості

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        """
        Розрахунок комплексних статистичних показників
        """
        # Територіальна стратифікація
        metrics = self.analytical_frame.groupby(['district', 'urgency']).agg({
            'response_time': [
                'count',
                'mean',
                'median',
                'std',
                lambda x: x.quantile(0.25),
                lambda x: x.quantile(0.75)
            ]
        }).round(2)

        metrics.columns = [
            'n_cases',
            'mean_time',
            'median_time',
            'std_dev',
            'q1',
            'q3'
        ]

        return metrics

    def visualize_distribution(self):
        """
        Статистична візуалізація територіального розподілу
        """
        # Базова візуалізація
        plot = (ggplot(self.analytical_frame,
                      aes(x='district',
                          y='response_time',
                          fill='urgency'))
                + geom_violin(alpha=0.5)
                + geom_boxplot(width=0.2, alpha=0.7)
                + geom_hline(yintercept=20,
                            linetype='dashed',
                            color='red')
                + theme_minimal()
                + theme(axis_text_x=element_text(angle=45, hjust=1))
                + labs(title='Територіальна варіабельність часу реагування',
                      x='Район',
                      y='Час реагування (хвилини)',
                      fill='Терміновість'))

        return plot

# Імплементація
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

# Статистичний аналіз
metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

# Візуалізація
plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png',
         dpi=300, height=12, width=16)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return np.nan

        time_cols = [col for col in df.columns if ':' in str(col)]

        for col in time_cols:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('0:31:15') - pl.col('0:03:54')).alias('response_time')
        ])

        df = df.filter(~pl.col('response_time').is_null())

        district_col = df.columns[3]
        urgency_col = df.columns[18]

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)


import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str) or time_str == '':
                    return np.nan
                if 'AM' in time_str or 'PM' in time_str:
                    return datetime.strptime(time_str, '%I:%M:%S %p').hour * 60 + datetime.strptime(time_str, '%I:%M:%S %p').minute
                else:
                    return datetime.strptime(time_str, '%H:%M:%S').hour * 60 + datetime.strptime(time_str, '%H:%M:%S').minute
            except:
                return np.nan

        time_columns = ['Время приёма вызова (создания заявки)', 'Время выезда', 'Время прибытия']

        for col in time_columns:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('Время прибытия') - pl.col('Время выезда')).alias('response_time')
        ])

        df = df.filter((pl.col('response_time').is_not_null()) & (pl.col('response_time') >= 0))

        district_col = 'Район'
        urgency_col = 'Тип выезда'

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)


import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str) or time_str == '':
                    return np.nan
                if 'AM' in time_str or 'PM' in time_str:
                    return datetime.strptime(time_str, '%I:%M:%S %p').hour * 60 + datetime.strptime(time_str, '%I:%M:%S %p').minute
                else:
                    return datetime.strptime(time_str, '%H:%M:%S').hour * 60 + datetime.strptime(time_str, '%H:%M:%S').minute
            except:
                return np.nan

        # Автоматичне визначення колонок часу
        def find_column(keyword):
            return next((col for col in df.columns if keyword.lower() in col.lower()), None)

        time_columns = {
            'call_time': find_column('приёма вызова'),
            'departure_time': find_column('выезда'),
            'arrival_time': find_column('прибытия')
        }

        for key, col in time_columns.items():
            if col:
                df = df.with_columns(
                    pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64).alias(key)
                )

        df = df.with_columns([
            (pl.col('arrival_time') - pl.col('departure_time')).alias('response_time')
        ])

        df = df.filter((pl.col('response_time').is_not_null()) & (pl.col('response_time') >= 0))

        district_col = find_column('район')
        urgency_col = find_column('тип выезда')

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)


import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str) or time_str == '':
                    return np.nan
                return datetime.strptime(time_str, '%H:%M:%S').hour * 60 + datetime.strptime(time_str, '%H:%M:%S').minute
            except:
                return np.nan

        time_columns = {
            'call_time': 'Время приёма вызова (создания заявки) в формате 09:55:45',
            'departure_time': 'Время выезда в формате 09:55:45',
            'arrival_time': 'Время прибытия в формате 09:55:45'
        }

        for key, col in time_columns.items():
            if col in df.columns:
                df = df.with_columns(
                    pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64).alias(key)
                )

        if 'arrival_time' in df.columns and 'departure_time' in df.columns:
            df = df.with_columns([
                (pl.col('arrival_time') - pl.col('departure_time')).alias('response_time')
            ])

        df = df.filter((pl.col('response_time').is_not_null()) & (pl.col('response_time') >= 0))

        self.analytical_frame = df.select([
            pl.col('Район').alias('district'),
            pl.col('Тип выезда').alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)


import polars as pl
import numpy as np
from datetime import datetime
import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

class EMSTemporalAnalysis:
    """
    Enhanced Emergency Medical Services Temporal Analysis Framework

    Methodology:
    - Robust data validation and cleaning
    - Temporal standardization
    - Statistical significance testing
    - Geospatial response time analysis
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}
        self.time_columns = {
            'arrival': 'Время прибытия в формате 09:55:45',
            'departure': 'Время выезда в формате 09:55:45',
            'call': 'Время приёма вызова (создания заявки) в формате 09:55:45'
        }

    def standardize_time(self, time_str):
        """
        Standardizes time strings to minutes since midnight

        Parameters:
        time_str (str): Time in format HH:MM:SS

        Returns:
        float: Minutes since midnight or np.nan if invalid
        """
        try:
            if pd.isna(time_str) or time_str == '':
                return np.nan
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            return time_obj.hour * 60 + time_obj.minute
        except:
            return np.nan

    def load_and_validate(self):
        """
        Loads and validates EMS data with comprehensive error checking
        """
        # Load data with explicit encoding
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        # Data validation metrics
        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count().to_dict()
        }

        # Convert time columns
        for key, col in self.time_columns.items():
            if col in df.columns:
                df = df.with_columns(
                    pl.col(col).map_elements(self.standardize_time).alias(f'{key}_minutes')
                )

        # Calculate response times
        if all(f'{key}_minutes' in df.columns for key in ['arrival', 'departure']):
            df = df.with_columns([
                (pl.col('arrival_minutes') - pl.col('departure_minutes')).alias('response_time')
            ])

        # Filter valid response times
        df = df.filter(
            (pl.col('response_time').is_not_null()) &
            (pl.col('response_time') >= 0) &
            (pl.col('response_time') <= 180)  # Maximum reasonable response time
        )

        # Prepare analytical frame
        self.analytical_frame = df.select([
            pl.col('Миколаївський район').alias('district'),
            pl.col('Терміново').alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        """
        Computes comprehensive statistical metrics for response times
        """
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg({
            'response_time': [
                ('n_cases', 'count'),
                ('mean_time', 'mean'),
                ('median_time', 'median'),
                ('std_dev', 'std'),
                ('q1', lambda x: x.quantile(0.25)),
                ('q3', lambda x: x.quantile(0.75))
            ]
        }).round(2)

        # Calculate IQR and outlier boundaries
        metrics[('response_time', 'iqr')] = metrics[('response_time', 'q3')] - metrics[('response_time', 'q1')]
        metrics[('response_time', 'outliers_pct')] = df.groupby(['district', 'urgency']).apply(
            lambda x: (
                (x['response_time'] < x['response_time'].quantile(0.25) - 1.5 * (x['response_time'].quantile(0.75) - x['response_time'].quantile(0.25))) |
                (x['response_time'] > x['response_time'].quantile(0.75) + 1.5 * (x['response_time'].quantile(0.75) - x['response_time'].quantile(0.25)))
            ).mean() * 100
        ).round(2)

        return metrics

    def visualize_distribution(self):
        """
        Creates advanced visualization of response time distributions
        """
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        # Filter out districts with insufficient data
        min_cases = 10
        df = df[df.groupby('district')['response_time'].transform('count') >= min_cases]

        # Create enhanced visualization
        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5, scale='width')
            + geom_boxplot(width=0.2, alpha=0.7, outlier.alpha=0.4)
            + geom_hline(yintercept=20, linetype='dashed', color='red', alpha=0.7)
            + theme_minimal()
            + theme(
                axis_text_x=element_text(angle=45, hjust=1, size=10),
                plot_title=element_text(size=14, face='bold'),
                plot_subtitle=element_text(size=12)
            )
            + labs(
                title='Територіальна варіабельність часу реагування ШМД',
                subtitle=f'Аналіз на основі {len(df)} викликів',
                x='Район',
                y='Час реагування (хвилини)',
                fill='Терміновість'
            )
            + scale_y_continuous(
                breaks=range(0, int(df['response_time'].max()) + 1, 10)
            )
        )

        return plot

def analyze_ems_data(file_path):
    """
    Comprehensive EMS data analysis pipeline
    """
    analysis = EMSTemporalAnalysis(file_path)
    analysis.load_and_validate()

    # Compute and display metrics
    metrics = analysis.compute_metrics()
    print("\nСтатистичні показники за районами:")
    print(metrics)

    # Generate and save visualization
    plot = analysis.visualize_distribution()
    plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)

    return analysis, metrics, plot

import polars as pl
import numpy as np
from datetime import datetime
import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

# Константи та методологічні параметри
FILE_PATH = '/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv'
TEMPORAL_PARAMETERS = {
    'max_response_time': 180,  # максимальний час реагування у хвилинах
    'min_cases_threshold': 10  # мінімальна кількість випадків для статистичної значущості
}

class EMSTemporalAnalysis:
    """
    Методологічний фреймворк аналізу часових параметрів екстреної медичної допомоги

    Параметри дослідження:
    - Джерело даних: Миколаївська область
    - Часовий період: 2024 рік
    - Методологія: Комплексний статистичний аналіз
    """
    def __init__(self):
        self.validation_metrics = {}
        self.time_columns = {
            'arrival': 'Время прибытия в формате 09:55:45',
            'departure': 'Время выезда в формате 09:55:45',
            'call': 'Время приёма вызова (создания заявки) в формате 09:55:45'
        }

    def standardize_time(self, time_str):
        """
        Стандартизація часових показників

        Методологічні аспекти:
        1. Конвертація до хвилин від опівночі
        2. Валідація форматування
        3. Обробка відсутніх значень
        """
        try:
            if pd.isna(time_str) or time_str == '':
                return np.nan
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            return time_obj.hour * 60 + time_obj.minute
        except:
            return np.nan

    def load_and_validate(self):
        """
        Завантаження та валідація даних з методологічною точністю

        Етапи обробки:
        1. Завантаження даних з визначеним кодуванням
        2. Валідація структури
        3. Стандартизація часових показників
        4. Розрахунок метрик якості даних
        """
        try:
            df = pl.read_csv(FILE_PATH, encoding='cp1251', separator=',', skip_rows=2)

            self.validation_metrics = {
                'total_records': len(df),
                'columns': df.columns,
                'missing_data': df.null_count().to_dict()
            }

            # Темпоральна стандартизація
            for key, col in self.time_columns.items():
                if col in df.columns:
                    df = df.with_columns(
                        pl.col(col).map_elements(self.standardize_time).alias(f'{key}_minutes')
                    )

            # Розрахунок часу реагування
            if all(f'{key}_minutes' in df.columns for key in ['arrival', 'departure']):
                df = df.with_columns([
                    (pl.col('arrival_minutes') - pl.col('departure_minutes')).alias('response_time')
                ])

            # Валідація часових показників
            df = df.filter(
                (pl.col('response_time').is_not_null()) &
                (pl.col('response_time') >= 0) &
                (pl.col('response_time') <= TEMPORAL_PARAMETERS['max_response_time'])
            )

            # Підготовка аналітичного фрейму
            self.analytical_frame = df.select([
                pl.col('Миколаївський район').alias('district'),
                pl.col('Терміново').alias('urgency'),
                pl.col('response_time')
            ]).to_pandas()

            print(f"\nМетодологічна валідація даних:")
            print(f"Загальна кількість записів: {self.validation_metrics['total_records']}")
            print(f"Валідні часові показники: {len(self.analytical_frame)}")

            return self

        except Exception as e:
            print(f"\nМетодологічна помилка при завантаженні даних:")
            print(f"Тип помилки: {type(e).__name__}")
            print(f"Опис помилки: {str(e)}")
            raise

def main():
    """
    Головний процес аналізу з методологічним контролем якості
    """
    try:
        analysis = EMSTemporalAnalysis()
        analysis.load_and_validate()

        print("\nСтатус виконання: Успішно завершено первинну валідацію даних")
        return analysis

    except Exception as e:
        print("\nКритична помилка в процесі аналізу:")
        print(f"Опис: {str(e)}")
        return None

if __name__ == "__main__":
    analysis = main()

import polars as pl
import numpy as np
from datetime import datetime
import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

class EMSDataValidation:
    """
    Методологічний фреймворк валідації даних екстреної медичної допомоги

    Параметри валідації:
    - Структурна цілісність даних
    - Часова узгодженість
    - Географічна відповідність
    - Клінічна релевантність
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.validation_metrics = {}
        self.data_quality_indicators = {}

    def validate_file_structure(self):
        """
        Первинна валідація структури файлу з розширеною діагностикою помилок

        Повертає:
        dict: Метрики якості даних та діагностичні показники
        """
        try:
            # Спроба читання з розширеними параметрами обробки помилок
            df = pl.read_csv(
                self.file_path,
                encoding='cp1251',
                separator=',',
                skip_rows=2,
                truncate_ragged_lines=True,
                ignore_errors=True
            )

            self.validation_metrics = {
                'total_records': len(df),
                'columns_detected': len(df.columns),
                'null_percentage': df.null_count().mean() / len(df) * 100
            }

            return df

        except Exception as e:
            raise ValueError(f"Методологічна помилка при валідації даних: {str(e)}")

class EMSTemporalAnalysis:
    """
    Комплексний аналіз часових патернів екстреної медичної допомоги

    Методологічні компоненти:
    1. Валідація вхідних даних
    2. Стандартизація часових показників
    3. Статистичний аналіз
    4. Візуалізація результатів
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.validator = EMSDataValidation(data_path)
        self.time_columns = {
            'arrival': 'Время прибытия в формате 09:55:45',
            'departure': 'Время выезда в формате 09:55:45',
            'call': 'Время приёма вызова (создания заявки) в формате 09:55:45'
        }

    def load_and_validate(self):
        """
        Завантаження та валідація даних з розширеною обробкою помилок
        """
        print("\nІніціалізація процесу валідації даних...")

        try:
            # Первинна валідація структури
            df = self.validator.validate_file_structure()

            print("\nСтруктурна валідація даних:")
            print(f"Кількість записів: {len(df)}")
            print(f"Виявлені колонки: {df.columns}")

            # Валідація часових показників
            for key, col in self.time_columns.items():
                if col in df.columns:
                    df = df.with_columns(
                        pl.col(col)
                        .map_elements(lambda x: self._standardize_time(x))
                        .alias(f'{key}_minutes')
                    )

            # Розрахунок часу реагування
            if all(f'{key}_minutes' in df.columns for key in ['arrival', 'departure']):
                df = df.with_columns([
                    (pl.col('arrival_minutes') - pl.col('departure_minutes'))
                    .alias('response_time')
                ])

            # Фільтрація валідних значень
            df = df.filter(
                (pl.col('response_time').is_not_null()) &
                (pl.col('response_time') >= 0) &
                (pl.col('response_time') <= 180)
            )

            # Підготовка аналітичного фрейму
            self.analytical_frame = df.select([
                pl.col('Миколаївський район').alias('district'),
                pl.col('Терміново').alias('urgency'),
                pl.col('response_time')
            ]).to_pandas()

            print("\nРезультати валідації:")
            print(f"Валідні записи для аналізу: {len(self.analytical_frame)}")

            return self

        except Exception as e:
            print("\nКритична помилка в процесі аналізу:")
            print(f"Опис: {str(e)}")
            raise

    def _standardize_time(self, time_str):
        """
        Стандартизація часових значень з валідацією
        """
        try:
            if pd.isna(time_str) or time_str == '':
                return np.nan
            time_obj = datetime.strptime(time_str, '%H:%M:%S')
            return time_obj.hour * 60 + time_obj.minute
        except:
            return np.nan

def analyze_ems_data(file_path):
    """
    Комплексний аналіз даних ЕМД з розширеною валідацією
    """
    try:
        print("\nПочаток аналізу даних ЕМД...")
        analysis = EMSTemporalAnalysis(file_path)
        analysis.load_and_validate()

        return analysis

    except Exception as e:
        print("\nМетодологічна помилка при завантаженні даних:")
        print(f"Тип помилки: {type(e).__name__}")
        print(f"Опис помилки: {str(e)}")
        return None

import polars as pl
import numpy as np
from datetime import datetime
import pandas as pd
from plotnine import *
import warnings
warnings.filterwarnings('ignore')

class EMSAnalyticalFramework:
    """
    Comprehensive analytical framework for Emergency Medical Services data
    with integrated validation and statistical analysis capabilities.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.validation_metrics = {}
        self.analytical_frames = {}

    def load_and_validate(self):
        """
        Multi-stage data loading and validation process with comprehensive error handling
        """
        try:
            # Initial data loading with enhanced error detection
            df = pl.read_csv(
                self.file_path,
                encoding='cp1251',
                separator=',',
                skip_rows=2,
                truncate_ragged_lines=True
            )

            # Standardize column names and handle encoding issues
            df.columns = [col.strip() for col in df.columns]

            # Time-based calculations
            time_columns = {
                'call_time': 'Время приёма вызова (создания заявки) в формате 09:55:45',
                'dispatch_time': 'Время выезда в формате 09:55:45',
                'arrival_time': 'Время прибытия в формате 09:55:45',
                'hospital_time': 'Время госпитализации в формате 09:55:45'
            }

            # Standardize time values
            for key, col in time_columns.items():
                if col in df.columns:
                    df = df.with_columns(
                        pl.col(col)
                        .map_elements(lambda x: self._standardize_time(x))
                        .alias(f'{key}_minutes')
                    )

            # Calculate response intervals
            df = df.with_columns([
                (pl.col('arrival_time_minutes') - pl.col('dispatch_time_minutes'))
                .alias('response_time'),
                (pl.col('dispatch_time_minutes') - pl.col('call_time_minutes'))
                .alias('dispatch_interval')
            ])

            # Create analytical subframes
            self.analytical_frames['temporal'] = df.select([
                pl.col('Миколаївський район').alias('district'),
                pl.col('Терміново').alias('urgency'),
                pl.col('response_time'),
                pl.col('dispatch_interval'),
                pl.col('МКХ-10').alias('icd_code')
            ]).to_pandas()

            # Validation metrics
            self.validation_metrics = {
                'total_records': len(df),
                'valid_response_times': df['response_time'].null_count().item(),
                'mean_response_time': df['response_time'].mean().item()
            }

            return self

        except Exception as e:
            raise ValueError(f"Critical error in data processing: {str(e)}")

    def _standardize_time(self, time_str):
        """
        Standardized time conversion with enhanced error handling
        """
        try:
            if pd.isna(time_str) or time_str == '':
                return np.nan
            time_obj = datetime.strptime(str(time_str).strip(), '%H:%M:%S')
            return time_obj.hour * 60 + time_obj.minute
        except:
            return np.nan

    def compute_response_metrics(self):
        """
        Calculate comprehensive response time metrics with statistical significance
        """
        df = self.analytical_frames['temporal']

        # Filter valid records
        df = df[df['response_time'].notna()]

        # Compute district-level metrics
        metrics = df.groupby(['district', 'urgency']).agg({
            'response_time': ['count', 'mean', 'std', 'median'],
            'dispatch_interval': ['mean', 'median']
        }).round(2)

        # Add confidence intervals
        metrics['response_time', 'ci_95'] = metrics.apply(
            lambda x: 1.96 * x[('response_time', 'std')] / np.sqrt(x[('response_time', 'count')]),
            axis=1
        ).round(2)

        return metrics

    def visualize_response_distribution(self):
        """
        Generate comprehensive response time visualization
        """
        df = self.analytical_frames['temporal']
        df = df[df['response_time'].notna()]

        # Filter for statistical significance
        df = df[df.groupby('district')['response_time'].transform('count') > 10]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7, outlier_size=2)
            + geom_hline(yintercept=20, linetype='dashed', color='red', alpha=0.5)
            + theme_minimal()
            + theme(
                axis_text_x=element_text(angle=45, hjust=1),
                figure_size=(12, 8)
            )
            + labs(
                title='Territorial Response Time Distribution Analysis',
                x='District',
                y='Response Time (minutes)',
                fill='Urgency Level'
            )
        )

        return plot

import polars as pl
import pandas as pd
import numpy as np
from datetime import datetime

def analyze_ems_data(file_path):
    """
    Basic EMS data analysis framework

    Parameters:
    file_path (str): Path to the CSV file

    Returns:
    dict: Analysis results
    """
    try:
        # Initial data loading with basic error handling
        df = pl.read_csv(
            file_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2
        )

        # Print initial validation
        print(f"\nTotal records: {len(df)}")
        print(f"Columns detected: {len(df.columns)}")

        # Time columns mapping
        time_columns = {
            'dispatch': 'Время выезда в формате 09:55:45',
            'arrival': 'Время прибытия в формате 09:55:45'
        }

        # Convert time columns to minutes
        for key, col in time_columns.items():
            if col in df.columns:
                df = df.with_columns(
                    pl.col(col)
                    .map_elements(lambda x: standardize_time(x))
                    .alias(f'{key}_minutes')
                )

        # Calculate response time
        df = df.with_columns([
            (pl.col('arrival_minutes') - pl.col('dispatch_minutes'))
            .alias('response_time')
        ])

        # Basic analysis frame
        analysis_df = df.select([
            pl.col('Миколаївський район').alias('district'),
            pl.col('response_time'),
            pl.col('Терміново').alias('urgency')
        ]).to_pandas()

        # Remove invalid response times
        analysis_df = analysis_df[
            (analysis_df['response_time'].notna()) &
            (analysis_df['response_time'] > 0) &
            (analysis_df['response_time'] < 180)  # 3 hours max
        ]

        print(f"\nValid records for analysis: {len(analysis_df)}")

        # Basic statistics
        stats = analysis_df.groupby('district')['response_time'].agg([
            'count',
            'mean',
            'median'
        ]).round(2)

        print("\nResponse time statistics by district:")
        print(stats)

        return analysis_df

    except Exception as e:
        print(f"\nError in analysis: {str(e)}")
        return None

def standardize_time(time_str):
    """
    Convert time string to minutes from midnight
    """
    try:
        if pd.isna(time_str) or time_str == '':
            return np.nan
        time_obj = datetime.strptime(str(time_str).strip(), '%H:%M:%S')
        return time_obj.hour * 60 + time_obj.minute
    except:
        return np.nan

# Usage
if __name__ == "__main__":
    file_path = "/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv"  # Replace with your file path
    results = analyze_ems_data(file_path)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}
        self.analytical_frames = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        # Збереження повного датафрейму для подальшого аналізу
        self.full_df = df

        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return np.nan

        time_cols = [col for col in df.columns if ':' in str(col)]

        for col in time_cols:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('0:31:15') - pl.col('0:03:54')).alias('response_time')
        ])

        df = df.filter(~pl.col('response_time').is_null())

        district_col = df.columns[3]
        urgency_col = df.columns[18]

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_response_metrics(self):
        """Базова метрика часу реагування"""
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def analyze_disease_distribution(self):
        """Аналіз розподілу захворювань по районах"""
        df = self.full_df

        # Вибір потрібних колонок
        disease_df = df.select([
            pl.col('Миколаївський район').alias('district'),
            pl.col('МКХ-10').alias('icd_code'),
            pl.col('Значення').alias('diagnosis')
        ]).to_pandas()

        # Розрахунок частоти захворювань
        disease_stats = disease_df.groupby(['district', 'icd_code']).size().reset_index(name='count')
        disease_stats = disease_stats.sort_values(['district', 'count'], ascending=[True, False])

        return disease_stats

    def analyze_workload(self):
        """Аналіз навантаження на підстанції"""
        df = self.full_df

        # Часові інтервали
        workload_df = df.select([
            pl.col('Миколаївський район').alias('district'),
            pl.col('бригада id').alias('team_id'),
            pl.col('0:31:15').alias('arrival_time'),
            pl.col('0:42:32').alias('completion_time')
        ]).to_pandas()

        # Розрахунок навантаження
        workload_stats = workload_df.groupby('district').agg({
            'team_id': 'nunique',
            'arrival_time': 'count'
        }).reset_index()

        workload_stats.columns = ['district', 'unique_teams', 'total_calls']
        workload_stats['calls_per_team'] = (workload_stats['total_calls'] /
                                          workload_stats['unique_teams']).round(2)

        return workload_stats

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
def main():
    file_path = "/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv"
    analysis = EMSTemporalAnalysis(file_path)
    analysis.load_and_validate()

    # Базові метрики часу реагування
    response_metrics = analysis.compute_response_metrics()
    print("\nСтатистика часу реагування:")
    print(response_metrics)

    # Розподіл захворювань
    disease_stats = analysis.analyze_disease_distribution()
    print("\nТоп захворювань по районах:")
    print(disease_stats.head(20))

    # Навантаження на підстанції
    workload_stats = analysis.analyze_workload()
    print("\nНавантаження на бригади:")
    print(workload_stats)

    # Візуалізація
    plot = analysis.visualize_distribution()
    plot.save('ems_analysis.png', dpi=300, height=12, width=16)

if __name__ == "__main__":
    main()

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        # Додано truncate_ragged_lines=True для обробки нерівномірних рядків
        df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2,
            truncate_ragged_lines=True
        )

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return np.nan

        time_cols = [col for col in df.columns if ':' in str(col)]

        for col in time_cols:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('0:31:15') - pl.col('0:03:54')).alias('response_time')
        ])

        df = df.filter(~pl.col('response_time').is_null())

        district_col = df.columns[3]  # Миколаївський район
        urgency_col = df.columns[18]  # Терміново

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class EMSResponseAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        # Завантаження та базова валідація
        self.df = pd.read_csv(self.data_path, encoding='cp1251', sep=',')
        self.df = self.df.iloc[2:]  # Видалення службових рядків

        # Аналіз пропущених значень
        self.missing_analysis = {
            'total_records': len(self.df),
            'missing_by_column': self.df.isnull().sum(),
            'missing_district': self.df['Район'].isnull().sum(),
            'missing_times': {
                'dispatch': self.df['Время выезда в формате 09:55:45'].isnull().sum(),
                'arrival': self.df['Время прибытия в формате 09:55:45'].isnull().sum()
            }
        }

    def calculate_response_metrics(self):
        # Розрахунок часу реагування
        def parse_time(time_str):
            try:
                clean_time = str(time_str).replace(' AM', '').replace(' PM', '')
                parts = clean_time.split(':')
                return int(parts[0]) * 60 + int(parts[1])
            except:
                return np.nan

        self.df['response_time'] = (
            self.df['Время прибытия в формате 09:55:45'].apply(parse_time) -
            self.df['Время выезда в формате 09:55:45'].apply(parse_time)
        )

        # Корекція нічних викликів
        self.df.loc[self.df['response_time'] < -1000, 'response_time'] += 1440

        # Розрахунок статистик по районах
        self.district_stats = self.df.groupby(['Район', 'Терміново'])['response_time'].agg([
            'count',
            'mean',
            'median',
            'std',
            lambda x: x.quantile(0.25),
            lambda x: x.quantile(0.75)
        ]).round(2)

        self.district_stats.columns = ['count', 'mean', 'median', 'std', 'Q1', 'Q3']
        self.district_stats['IQR'] = self.district_stats['Q3'] - self.district_stats['Q1']

    def analyze_disease_distribution(self):
        """Аналіз розподілу захворювань"""
        disease_stats = self.df.groupby(['Район', 'МКХ-10']).size().reset_index(name='count')
        disease_stats = disease_stats.sort_values(['Район', 'count'], ascending=[True, False])
        return disease_stats

    def analyze_workload(self):
        """Аналіз навантаження"""
        workload = self.df.groupby('Район').agg({
            'бригада id': 'nunique',
            'Время приёма вызова (создания заявки) в формате 09:55:45': 'count'
        }).reset_index()

        workload.columns = ['district', 'unique_teams', 'total_calls']
        workload['calls_per_team'] = (workload['total_calls'] / workload['unique_teams']).round(2)
        return workload

# Використання
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.calculate_response_metrics()

print("\nАналіз якості даних:")
print(f"Загальна кількість записів: {analyzer.missing_analysis['total_records']}")
print(f"Пропущені райони: {analyzer.missing_analysis['missing_district']}")
print(f"Пропущені часи виїзду: {analyzer.missing_analysis['missing_times']['dispatch']}")
print(f"Пропущені часи прибуття: {analyzer.missing_analysis['missing_times']['arrival']}")

print("\nСтатистика по районах:")
print(analyzer.district_stats)

# Додаткові метрики
disease_stats = analyzer.analyze_disease_distribution()
print("\nТоп захворювань по районах:")
print(disease_stats.head(20))

workload_stats = analyzer.analyze_workload()
print("\nНавантаження на бригади:")
print(workload_stats)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        df = pl.read_csv(self.data_path, encoding='cp1251', separator=',', skip_rows=2)

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return np.nan

        time_cols = [col for col in df.columns if ':' in str(col)]

        for col in time_cols:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('0:31:15') - pl.col('0:03:54')).alias('response_time')
        ])

        df = df.filter(~pl.col('response_time').is_null())

        district_col = df.columns[3]
        urgency_col = df.columns[18]

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time'),
            pl.col('МКХ-10').alias('icd_code'),
            pl.col('Значення').alias('diagnosis'),
            pl.col('бригада id').alias('team_id')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        """Базові метрики часу реагування"""
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def analyze_diseases(self):
        """Аналіз розподілу захворювань"""
        df = self.analytical_frame
        disease_stats = df.groupby(['district', 'icd_code'])['diagnosis'].count().reset_index()
        disease_stats = disease_stats.sort_values(['district', 'diagnosis'], ascending=[True, False])
        return disease_stats

    def analyze_workload(self):
        """Аналіз навантаження бригад"""
        df = self.analytical_frame
        workload = df.groupby('district').agg({
            'team_id': 'nunique',
            'response_time': 'count'
        }).reset_index()

        workload.columns = ['district', 'teams', 'calls']
        workload['calls_per_team'] = (workload['calls'] / workload['teams']).round(2)
        return workload

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

# Базові метрики часу реагування
metrics = analysis.compute_metrics()
print("\nСтатистичні показники часу реагування за районами:")
print(metrics)

# Розподіл захворювань
diseases = analysis.analyze_diseases()
print("\nРозподіл захворювань за районами:")
print(diseases.head(20))

# Навантаження на бригади
workload = analysis.analyze_workload()
print("\nНавантаження на бригади за районами:")
print(workload)

# Візуалізація
plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)

import polars as pl
import numpy as np
from datetime import datetime
from plotnine import *
import pandas as pd

class EMSTemporalAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.validation_metrics = {}

    def load_and_validate(self):
        # Додаємо truncate_ragged_lines=True для вирішення проблеми з полями
        df = pl.read_csv(
            self.data_path,
            encoding='cp1251',
            separator=',',
            skip_rows=2,
            truncate_ragged_lines=True  # Критичний параметр для успішного завантаження
        )

        print("\nСтруктурна валідація даних:")
        print("Наявні колонки:")
        print(df.columns)

        self.validation_metrics = {
            'total_records': len(df),
            'columns': df.columns,
            'missing_data': df.null_count()
        }

        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).replace(' AM', '').replace(' PM', '')
                hours, minutes = map(int, time_str.split(':')[:2])
                return float(hours * 60 + minutes)
            except:
                return np.nan

        time_cols = [col for col in df.columns if ':' in str(col)]

        for col in time_cols:
            df = df.with_columns(
                pl.col(col).map_elements(standardize_time, return_dtype=pl.Float64)
            )

        df = df.with_columns([
            (pl.col('0:31:15') - pl.col('0:03:54')).alias('response_time')
        ])

        df = df.filter(~pl.col('response_time').is_null())

        district_col = df.columns[3]
        urgency_col = df.columns[18]

        self.analytical_frame = df.select([
            pl.col(district_col).alias('district'),
            pl.col(urgency_col).alias('urgency'),
            pl.col('response_time')
        ]).to_pandas()

        return self

    def compute_metrics(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        metrics = df.groupby(['district', 'urgency']).agg(
            n_cases=('response_time', 'count'),
            mean_time=('response_time', 'mean'),
            median_time=('response_time', 'median'),
            std_dev=('response_time', 'std'),
            q1=('response_time', lambda x: x.quantile(0.25)),
            q3=('response_time', lambda x: x.quantile(0.75))
        ).round(2)

        return metrics

    def visualize_distribution(self):
        df = self.analytical_frame.copy()
        df = df[df['response_time'].notna()]

        df = df[df.groupby('district')['response_time'].transform('count') > 1]

        plot = (
            ggplot(df, aes(x='district', y='response_time', fill='urgency'))
            + geom_violin(alpha=0.5)
            + geom_boxplot(width=0.2, alpha=0.7)
            + geom_hline(yintercept=20, linetype='dashed', color='red')
            + theme_minimal()
            + theme(axis_text_x=element_text(angle=45, hjust=1, size=10))
            + labs(title='Територіальна варіабельність часу реагування',
                   x='Район',
                   y='Час реагування (хвилини)',
                   fill='Терміновість')
        )

        return plot

# Використання
analysis = EMSTemporalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analysis.load_and_validate()

metrics = analysis.compute_metrics()
print("\nСтатистичні показники за районами:")
print(metrics)

plot = analysis.visualize_distribution()
plot.save('ems_response_analysis.png', dpi=300, height=12, width=16)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class EMSResponseAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        self.df = pd.read_csv(self.data_path, encoding='cp1251', sep=',')
        self.df = self.df.iloc[2:]

        self.missing_analysis = {
            'total_records': len(self.df),
            'missing_by_column': self.df.isnull().sum(),
            'missing_district': self.df['Район'].isnull().sum(),
            'missing_times': {
                'dispatch': self.df['Время выезда в формате 09:55:45'].isnull().sum(),
                'arrival': self.df['Время прибытия в формате 09:55:45'].isnull().sum()
            }
        }

    def calculate_response_metrics(self):
        def parse_time(time_str):
            try:
                clean_time = str(time_str).replace(' AM', '').replace(' PM', '')
                parts = clean_time.split(':')
                return int(parts[0]) * 60 + int(parts[1])
            except:
                return np.nan

        # Розрахунок всіх часових інтервалів
        self.df['dispatch_time'] = self.df['Время выезда в формате 09:55:45'].apply(parse_time)
        self.df['arrival_time'] = self.df['Время прибытия в формате 09:55:45'].apply(parse_time)
        self.df['call_time'] = self.df['Время приёма вызова (создания заявки) в формате 09:55:45'].apply(parse_time)
        self.df['hospital_time'] = self.df['Время госпитализации в формате 09:55:45'].apply(parse_time)

        # Різні часові інтервали
        self.df['response_time'] = self.df['arrival_time'] - self.df['dispatch_time']
        self.df['dispatch_interval'] = self.df['dispatch_time'] - self.df['call_time']
        self.df['hospital_interval'] = self.df['hospital_time'] - self.df['arrival_time']

        # Корекція нічних викликів
        for col in ['response_time', 'dispatch_interval', 'hospital_interval']:
            self.df.loc[self.df[col] < -1000, col] += 1440

        # Територіальний аналіз з урахуванням терміновості
        self.district_urgency_stats = self.df.groupby(['Район', 'Терміново'])['response_time'].agg([
            'count',
            'mean',
            'median',
            'std',
            lambda x: x.quantile(0.25),
            lambda x: x.quantile(0.75)
        ]).round(2)

    def analyze_disease_distribution(self):
        """Розподіл захворювань по районах"""
        disease_stats = self.df.groupby(['Район', 'МКХ-10']).size().reset_index(name='count')
        disease_stats['percentage'] = disease_stats.groupby('Район')['count'].transform(
            lambda x: x / x.sum() * 100
        ).round(2)
        return disease_stats.sort_values(['Район', 'count'], ascending=[True, False])

    def analyze_urgency_distribution(self):
        """Розподіл термінових/нетермінових випадків"""
        urgency_stats = self.df.groupby(['Район', 'Терміново']).size().unstack(fill_value=0)
        urgency_stats['total'] = urgency_stats.sum(axis=1)
        urgency_stats['urgent_percentage'] = (
            urgency_stats['Терміново'] / urgency_stats['total'] * 100
        ).round(2)
        return urgency_stats

    def analyze_workload(self):
        """Аналіз навантаження підстанцій"""
        workload = self.df.groupby('Район').agg({
            'бригада id': 'nunique',
            'Время приёма вызова (создания заявки) в формате 09:55:45': 'count'
        }).reset_index()

        workload.columns = ['district', 'teams', 'calls']
        workload['calls_per_team'] = (workload['calls'] / workload['teams']).round(2)
        return workload

    def analyze_call_reasons(self):
        """Розподіл причин викликів"""
        reasons = self.df.groupby(['Район', 'Причина вызова']).size().reset_index(name='count')
        reasons['percentage'] = reasons.groupby('Район')['count'].transform(
            lambda x: x / x.sum() * 100
        ).round(2)
        return reasons.sort_values(['Район', 'count'], ascending=[True, False])

# Імплементація
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')
analyzer.calculate_response_metrics()

# Базова статистика
print("\nАналіз якості даних:")
print(f"Загальна кількість записів: {analyzer.missing_analysis['total_records']}")
print(f"Пропущені райони: {analyzer.missing_analysis['missing_district']}")

# Територіальний розподіл
print("\nТериторіальний розподіл часу реагування:")
print(analyzer.district_urgency_stats)

# Розподіл захворювань
diseases = analyzer.analyze_disease_distribution()
print("\nТоп захворювань по районах:")
print(diseases.head(20))

# Розподіл терміновості
urgency = analyzer.analyze_urgency_distribution()
print("\nРозподіл термінових викликів:")
print(urgency)

# Навантаження
workload = analyzer.analyze_workload()
print("\nНавантаження на бригади:")
print(workload)

# Причини викликів
reasons = analyzer.analyze_call_reasons()
print("\nОсновні причини викликів:")
print(reasons.head(20))

# Візуалізація
fig = analyzer.visualize_distributions()
plt.savefig('response_time_detailed.png', dpi=300, bbox_inches='tight')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class EMSResponseAnalysis:
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_data()

    def load_data(self):
        """
        Методологічно валідоване завантаження даних з інтегрованою
        валідацією структурної цілісності набору даних
        """
        self.df = pd.read_csv(
            self.data_path,
            encoding='cp1251',
            sep=',',
            skiprows=2,  # Пропуск службових рядків
            on_bad_lines='skip'  # Обробка проблемних рядків
        )

        # Валідація якості даних
        self.missing_analysis = {
            'total_records': len(self.df),
            'missing_by_column': self.df.isnull().sum(),
            'missing_district': self.df['Район'].isnull().sum(),
            'missing_times': {
                'dispatch': self.df['Время выезда в формате 09:55:45'].isnull().sum(),
                'arrival': self.df['Время прибытия в формате 09:55:45'].isnull().sum(),
                'hospital': self.df['Время госпитализации в формате 09:55:45'].isnull().sum()
            }
        }

    def calculate_response_metrics(self):
        """
        Комплексний аналіз часових інтервалів реагування з
        інтегрованою валідацією та нормалізацією даних
        """
        def parse_time(time_str):
            try:
                clean_time = str(time_str).replace(' AM', '').replace(' PM', '')
                parts = clean_time.split(':')
                return int(parts[0]) * 60 + int(parts[1])
            except:
                return np.nan

        # Розрахунок часових інтервалів
        for col, new_col in {
            'Время выезда в формате 09:55:45': 'dispatch_time',
            'Время прибытия в формате 09:55:45': 'arrival_time',
            'Время приёма вызова (создания заявки) в формате 09:55:45': 'call_time',
            'Время госпитализации в формате 09:55:45': 'hospital_time'
        }.items():
            self.df[new_col] = self.df[col].apply(parse_time)

        # Розрахунок ключових інтервалів
        self.df['response_time'] = self.df['arrival_time'] - self.df['dispatch_time']
        self.df['call_to_dispatch'] = self.df['dispatch_time'] - self.df['call_time']
        self.df['total_case_time'] = self.df['hospital_time'] - self.df['call_time']

        # Корекція нічних викликів
        for col in ['response_time', 'call_to_dispatch', 'total_case_time']:
            self.df.loc[self.df[col] < -1000, col] += 1440

        # Стратифікований аналіз за районами та терміновістю
        self.response_analysis = self.df.groupby(['Район', 'Терміново']).agg({
            'response_time': ['count', 'mean', 'median', 'std',
                            lambda x: x.quantile(0.25),
                            lambda x: x.quantile(0.75)],
            'call_to_dispatch': ['mean', 'median'],
            'total_case_time': ['mean', 'median']
        }).round(2)

    def analyze_disease_patterns(self):
        """
        Епідеміологічний аналіз структури захворюваності
        з територіальною стратифікацією
        """
        # Розподіл захворювань
        disease_patterns = self.df.groupby(['Район', 'МКХ-10', 'Терміново']).size().reset_index(name='cases')
        disease_patterns['prevalence'] = disease_patterns.groupby('Район')['cases'].transform(
            lambda x: x / x.sum() * 100
        ).round(2)

        return disease_patterns.sort_values(['Район', 'cases'], ascending=[True, False])

    def analyze_workload_distribution(self):
        """
        Аналіз територіального розподілу навантаження
        на бригади екстреної медичної допомоги
        """
        workload = self.df.groupby('Район').agg({
            'бригада id': ['nunique', 'count'],
            'Терміново': lambda x: (x == 'Терміново').mean() * 100
        }).round(2)

        workload.columns = ['unique_teams', 'total_calls', 'urgent_percentage']
        workload['calls_per_team'] = (workload['total_calls'] / workload['unique_teams']).round(2)

        return workload

    def visualize_distributions(self):
        """
        Візуалізація територіальної варіабельності часу реагування
        з інтегрованим аналізом статистичних викидів
        """
        plt.figure(figsize=(15, 10))

        sns.boxplot(data=self.df,
                   x='Район',
                   y='response_time',
                   hue='Терміново',
                   showfliers=True)

        plt.axhline(y=20, color='r', linestyle='--', label='Нормативний час (20 хв)')
        plt.xticks(rotation=45, ha='right')
        plt.title('Територіальна варіабельність часу реагування ЕМД')
        plt.ylabel('Час реагування (хвилини)')
        plt.legend(title='Терміновість виклику')

        return plt.gcf()

# Імплементація
analyzer = EMSResponseAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')

# Розрахунок метрик
analyzer.calculate_response_metrics()

# Виведення результатів
print("\nАналіз якості даних:")
print(f"Загальна кількість записів: {analyzer.missing_analysis['total_records']}")
print(f"Пропущені значення районів: {analyzer.missing_analysis['missing_district']}")
print("\nЧасові показники реагування за районами:")
print(analyzer.response_analysis)

# Аналіз захворювань
disease_patterns = analyzer.analyze_disease_patterns()
print("\nСтруктура захворюваності:")
print(disease_patterns.head(20))

# Аналіз навантаження
workload = analyzer.analyze_workload_distribution()
print("\nРозподіл навантаження на бригади ЕМД:")
print(workload)

# Візуалізація
fig = analyzer.visualize_distributions()
plt.savefig('ems_analysis_detailed.png', dpi=300, bbox_inches='tight', pad_inches=0.5)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class EMSEpidemiologicalAnalysis:
    """
    Методологічний фреймворк комплексного епідеміологічного аналізу
    екстреної медичної допомоги з інтегрованою валідацією даних
    та територіальною стратифікацією (N=167,550)
    """
    def __init__(self, data_path):
        self.data_path = data_path
        self.load_and_validate_data()

    def load_and_validate_data(self):
        """
        Методологічно валідоване завантаження даних з комплексною
        верифікацією структурної цілісності та якості даних
        """
        # Завантаження з коректними параметрами специфікації
        self.df = pd.read_csv(
            self.data_path,
            encoding='cp1251',
            sep=',',
            skiprows=2,  # Пропуск метаданих
            low_memory=False
        )

        # Валідація структурної цілісності
        self.data_quality = {
            'total_records': len(self.df),
            'missing_data': {
                'district': self.df['Район'].isnull().sum(),
                'urgency': self.df['Помощь по диагнозу(Срочная, несрочная).'].isnull().sum(),
                'diagnosis': self.df['МКХ-10'].isnull().sum(),
                'response_times': {
                    'call': self.df['Время приёма вызова (создания заявки) в формате 09:55:45'].isnull().sum(),
                    'dispatch': self.df['Время выезда в формате 09:55:45'].isnull().sum(),
                    'arrival': self.df['Время прибытия в формате 09:55:45'].isnull().sum()
                }
            }
        }

    def analyze_temporal_patterns(self):
        """
        Комплексний аналіз часових патернів з методологічною
        валідацією та нормалізацією темпоральних показників
        """
        def standardize_time(time_str):
            try:
                if pd.isna(time_str):
                    return np.nan
                time_str = str(time_str).strip().replace(' AM', '').replace(' PM', '')
                hours, minutes, seconds = map(int, time_str.split(':'))
                return hours * 60 + minutes  # Конвертація в хвилини
            except:
                return np.nan

        # Розрахунок ключових часових інтервалів
        time_columns = {
            'dispatch': 'Время выезда в формате 09:55:45',
            'arrival': 'Время прибытия в формате 09:55:45',
            'call': 'Время приёма вызова (создания заявки) в формате 09:55:45'
        }

        for key, col in time_columns.items():
            self.df[f'{key}_time'] = self.df[col].apply(standardize_time)

        # Розрахунок інтервалів реагування
        self.df['response_time'] = self.df['arrival_time'] - self.df['dispatch_time']
        self.df['dispatch_delay'] = self.df['dispatch_time'] - self.df['call_time']

        # Корекція нічних викликів
        for col in ['response_time', 'dispatch_delay']:
            self.df.loc[self.df[col] < -1000, col] += 1440

        # Територіальна стратифікація
        self.response_metrics = self.df.groupby(['Район', 'Помощь по диагнозу(Срочная, несрочная).']).agg({
            'response_time': ['count', 'mean', 'median', 'std',
                            lambda x: x.quantile(0.25),
                            lambda x: x.quantile(0.75)],
            'dispatch_delay': ['mean', 'median', 'std']
        }).round(2)

        return self.response_metrics

    def analyze_epidemiological_patterns(self):
        """
        Епідеміологічний аналіз структури захворюваності
        з територіальною та часовою стратифікацією
        """
        # Розподіл захворювань
        disease_patterns = self.df.groupby(['Район', 'МКХ-10']).agg({
            'МКХ-10': 'count',
            'Район': 'count',
            'Помощь по диагнозу(Срочная, несрочная).': lambda x: (x == 'Терміново').mean() * 100
        }).reset_index()

        disease_patterns.columns = ['district', 'icd_code', 'cases', 'total_district_cases', 'urgency_percentage']
        disease_patterns['prevalence'] = (disease_patterns['cases'] /
                                        disease_patterns['total_district_cases'] * 100).round(2)

        return disease_patterns

    def analyze_resource_utilization(self):
        """
        Аналіз використання ресурсів та навантаження
        на систему екстреної медичної допомоги
        """
        workload = self.df.groupby('Район').agg({
            'бригада id': ['nunique', 'count'],
            'Помощь по диагнозу(Срочная, несрочная).': lambda x: (x == 'Терміново').mean() * 100,
            'response_time': ['mean', 'median', 'std']
        }).round(2)

        workload.columns = ['unique_teams', 'total_calls', 'urgent_percentage',
                           'mean_response', 'median_response', 'response_std']
        workload['calls_per_team'] = (workload['total_calls'] / workload['unique_teams']).round(2)

        return workload

# Імплементація
analyzer = EMSEpidemiologicalAnalysis('/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv')

# Аналіз якості даних
print("\nВалідація якості даних:")
print(f"Загальна кількість записів: {analyzer.data_quality['total_records']}")
for key, value in analyzer.data_quality['missing_data'].items():
    if isinstance(value, dict):
        print(f"\nПропущені значення {key}:")
        for sub_key, sub_value in value.items():
            print(f"- {sub_key}: {sub_value}")
    else:
        print(f"Пропущені значення {key}: {value}")

# Часові патерни
temporal_patterns = analyzer.analyze_temporal_patterns()
print("\nТериторіальний розподіл часу реагування:")
print(temporal_patterns)

# Епідеміологічні патерни
disease_patterns = analyzer.analyze_epidemiological_patterns()
print("\nЕпідеміологічний профіль територій:")
print(disease_patterns.sort_values('cases', ascending=False).head(20))

# Використання ресурсів
workload = analyzer.analyze_resource_utilization()
print("\nАналіз навантаження на бригади ЕМД:")
print(workload)

import pandas as pd
import numpy as np
from datetime import datetime
import polars as pl
import csv
from pathlib import Path
import chardet

class EMSDataValidationFramework:
    """
    Методологічний фреймворк валідації даних екстреної медичної допомоги
    з інтегрованою верифікацією структурної цілісності та доступності

    Методологічні компоненти:
    1. Мультимодальна валідація доступу до даних
    2. Структурна верифікація цілісності
    3. Кодування та формат даних
    4. Валідація часових показників
    """
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.validation_results = {
            'file_exists': False,
            'encoding_detected': None,
            'successful_method': None,
            'data_structure': None,
            'row_count': 0,
            'validation_metrics': {}
        }

    def validate_file_existence(self):
        """
        Первинна валідація наявності файлу
        """
        self.validation_results['file_exists'] = self.file_path.exists()
        if not self.validation_results['file_exists']:
            raise FileNotFoundError(f"Файл не знайдено: {self.file_path}")

    def detect_encoding(self):
        """
        Методологічна детекція кодування файлу
        """
        try:
            with open(self.file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                self.validation_results['encoding_detected'] = result
                return result['encoding']
        except Exception as e:
            print(f"Помилка при визначенні кодування: {str(e)}")
            return None

    def attempt_pandas_read(self, encoding=None):
        """
        Спроба зчитування через pandas з валідацією структури
        """
        try:
            encodings = [encoding] if encoding else ['cp1251', 'utf-8', 'latin1']
            for enc in encodings:
                try:
                    df = pd.read_csv(self.file_path, encoding=enc, skiprows=2)
                    self.validation_results['successful_method'] = f'pandas with {enc}'
                    return df, enc
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print(f"Pandas читання не вдалося: {str(e)}")
            return None, None

    def attempt_polars_read(self, encoding=None):
        """
        Спроба зчитування через polars з валідацією структури
        """
        try:
            encodings = [encoding] if encoding else ['cp1251', 'utf-8', 'latin1']
            for enc in encodings:
                try:
                    df = pl.read_csv(
                        self.file_path,
                        encoding=enc,
                        separator=',',
                        skip_rows=2,
                        truncate_ragged_lines=True
                    )
                    self.validation_results['successful_method'] = f'polars with {enc}'
                    return df, enc
                except:
                    continue
        except Exception as e:
            print(f"Polars читання не вдалося: {str(e)}")
            return None, None

    def validate_and_load(self):
        """
        Комплексна валідація та завантаження даних
        """
        print("\nІніціалізація процесу валідації даних...")

        # Перевірка існування файлу
        self.validate_file_existence()
        print("Файл знайдено, починаємо валідацію...")

        # Детекція кодування
        detected_encoding = self.detect_encoding()
        print(f"Виявлене кодування: {detected_encoding}")

        # Спроба читання різними методами
        methods = [
            ('pandas', self.attempt_pandas_read),
            ('polars', self.attempt_polars_read)
        ]

        df = None
        successful_encoding = None

        for method_name, method in methods:
            print(f"\nСпроба читання через {method_name}...")
            result, encoding = method(detected_encoding)
            if result is not None:
                df = result
                successful_encoding = encoding
                print(f"Успішне читання через {method_name} з кодуванням {encoding}")
                break

        if df is not None:
            self.validation_results.update({
                'data_structure': {
                    'columns': len(df.columns),
                    'rows': len(df),
                    'missing_values': df.isnull().sum().sum() if isinstance(df, pd.DataFrame) else df.null_count().sum()
                },
                'row_count': len(df),
                'successful_encoding': successful_encoding
            })

            print("\nРезультати валідації:")
            print(f"Кількість рядків: {self.validation_results['row_count']}")
            print(f"Кількість колонок: {self.validation_results['data_structure']['columns']}")
            print(f"Метод читання: {self.validation_results['successful_method']}")

            return df
        else:
            raise ValueError("Не вдалося прочитати файл жодним методом")

# Використання фреймворку
def analyze_ems_data(file_path):
    """
    Комплексний аналіз даних ЕМД з методологічною валідацією
    """
    validator = EMSDataValidationFramework(file_path)
    df = validator.validate_and_load()

    return df, validator.validation_results

# Імплементація
try:
    file_path = '/content/drive/MyDrive/Colab Notebooks/Mykolaivska_pro_mapping.csv'
    df, validation_results = analyze_ems_data(file_path)

    print("\nДетальні результати валідації:")
    for key, value in validation_results.items():
        print(f"{key}: {value}")

except Exception as e:
    print(f"\nКритична помилка в процесі валідації:")
    print(f"Тип помилки: {type(e).__name__}")
    print(f"Опис помилки: {str(e)}")
