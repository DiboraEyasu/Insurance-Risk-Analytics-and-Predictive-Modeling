import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import tabulate
import numpy as np

class EDAAnalyzer:
    def __init__(self, df):
        self.df = df
    
    def plot_histograms(self, columns=None, figsize=(15, 10)):
        """
        Create histograms for numeric columns.
        
        Parameters:
        -----------
        columns : list, optional
            Specific columns to plot. If None, plots all numeric columns.
        figsize : tuple
            Figure size for the subplot grid
        """
        if columns is None:
            numeric_cols = self.df.select_dtypes(include=['number']).columns
        else:
            # Validate columns exist
            numeric_cols = [col for col in columns if col in self.df.columns]
            if len(numeric_cols) == 0:
                print("No valid numeric columns found!")
                return
        
        print(f"Plotting histograms for {len(numeric_cols)} numeric columns")
        
        # Calculate grid dimensions
        n_cols = 3
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        # Create figure with subplots
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for idx, col in enumerate(numeric_cols):
            if idx < len(axes):
                ax = axes[idx]
                
                # Plot histogram with KDE
                sns.histplot(data=self.df, x=col, kde=True, ax=ax, bins=30)
                
                # Calculate statistics
                mean_val = self.df[col].mean()
                median_val = self.df[col].median()
                skewness = self.df[col].skew()
                
                # Add statistics to plot
                stats_text = f"Mean: {mean_val:.2f}\nMedian: {median_val:.2f}\nSkew: {skewness:.2f}"
                ax.text(0.95, 0.95, stats_text, transform=ax.transAxes,
                       fontsize=8, verticalalignment='top',
                       horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
                ax.set_title(f'Distribution of {col}', fontsize=11, fontweight='bold')
                ax.set_xlabel(col)
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
        
        # Hide empty subplots
        for idx in range(len(numeric_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Histogram Analysis of Numeric Variables', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()
        
        # Print summary statistics
        self._print_distribution_summary(numeric_cols)
    
    def _print_distribution_summary(self, columns):
        """Print distribution statistics for columns"""
        print("\n" + "="*70)
        print("DISTRIBUTION SUMMARY STATISTICS")
        print("="*70)
        
        summary_data = []
        for col in columns:
            data = self.df[col].dropna()
            if len(data) > 0:
                summary_data.append({
                    'Column': col,
                    'Count': len(data),
                    'Mean': data.mean(),
                    'Std': data.std(),
                    'Min': data.min(),
                    '25%': data.quantile(0.25),
                    'Median': data.median(),
                    '75%': data.quantile(0.75),
                    'Max': data.max(),
                    'Skew': data.skew(),
                    'Missing %': (self.df[col].isnull().sum() / len(self.df)) * 100
                })
        
        summary_df = pd.DataFrame(summary_data)
        print(tabulate(summary_df, headers='keys', tablefmt='grid', floatfmt=".2f"))
    
    def bar_plot_categorical(self, columns=None, max_categories=10):
        """
        Create bar plots for categorical columns with safety checks.
        
        Parameters:
        -----------
        columns : list, optional
            Specific columns to plot. If None, plots common insurance categorical columns.
        max_categories : int
            Maximum number of categories to display per column
        """
        # Define default insurance categorical columns
        default_columns = ["Gender", "Province", "VehicleType", 
                          "MaritalStatus", "CoverType", "Bodytype"]
        
        if columns is None:
            columns_to_plot = default_columns
        else:
            columns_to_plot = columns
        
        # Filter to columns that actually exist
        existing_cols = [col for col in columns_to_plot if col in self.df.columns]
        missing_cols = [col for col in columns_to_plot if col not in self.df.columns]
        
        if missing_cols:
            print(f"Warning: The following columns were not found: {missing_cols}")
        
        if not existing_cols:
            print("No valid categorical columns found to plot!")
            return
        
        print(f"Plotting bar charts for: {existing_cols}")
        
        # Create subplot grid
        n_cols = 3
        n_rows = (len(existing_cols) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, n_rows*4))
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for idx, col in enumerate(existing_cols):
            if idx < len(axes):
                ax = axes[idx]
                
                # Get value counts
                value_counts = self.df[col].value_counts()
                
                # If too many categories, keep top N
                if len(value_counts) > max_categories:
                    top_categories = value_counts.head(max_categories)
                    other_count = value_counts.iloc[max_categories:].sum()
                    value_counts = pd.concat([top_categories, 
                                            pd.Series([other_count], index=['Other'])])
                
                # Create color palette
                colors = plt.cm.Set3(np.linspace(0, 1, len(value_counts)))
                
                # Create horizontal bar chart for better readability
                bars = ax.barh(range(len(value_counts)), value_counts.values, 
                              color=colors, edgecolor='black')
                
                # Customize plot
                ax.set_yticks(range(len(value_counts)))
                ax.set_yticklabels(value_counts.index)
                ax.invert_yaxis()  # Highest count at top
                
                ax.set_title(f'{col} Distribution', fontsize=12, fontweight='bold')
                ax.set_xlabel('Count')
                
                # Add value labels on bars
                for i, (bar, count) in enumerate(zip(bars, value_counts.values)):
                    width = bar.get_width()
                    percentage = (count / value_counts.sum()) * 100
                    label_x = width + (ax.get_xlim()[1] * 0.01)  # Slight offset
                    ax.text(label_x, bar.get_y() + bar.get_height()/2,
                           f'{count:,} ({percentage:.1f}%)',
                           va='center', ha='left', fontsize=9)
                
                # Add grid
                ax.grid(True, axis='x', alpha=0.3)
        
        # Hide empty subplots
        for idx in range(len(existing_cols), len(axes)):
            axes[idx].set_visible(False)
        
        plt.suptitle('Categorical Variable Distributions - Insurance Portfolio', 
                     fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        plt.show()
        
        # Print categorical summary
        self._print_categorical_summary(existing_cols)
    
    def _print_categorical_summary(self, columns):
        """Print summary statistics for categorical columns"""
        print("\n" + "="*70)
        print("CATEGORICAL VARIABLES SUMMARY")
        print("="*70)
        
        for col in columns:
            if col in self.df.columns:
                print(f"\n{col}:")
                print("-" * 40)
                
                value_counts = self.df[col].value_counts(dropna=False)
                total = len(self.df[col])
                
                # Show top 10 categories
                top_categories = value_counts.head(10)
                
                for category, count in top_categories.items():
                    percentage = (count / total) * 100
                    print(f"  {category}: {count:,} ({percentage:.1f}%)")
                
                # Show summary
                unique_count = value_counts.count()
                if unique_count > 10:
                    print(f"  ... and {unique_count - 10} more categories")
                
                # Missing values
                missing = self.df[col].isnull().sum()
                if missing > 0:
                    missing_pct = (missing / total) * 100
                    print(f"  Missing values: {missing:,} ({missing_pct:.1f}%)")
                    return self.df

# Usage example:
"""
df = pd.read_csv('insurance_data.csv')  # Load your data here
analyzer = EDAAnalyzer(df)s

# Plot all numeric histograms
analyzer.plot_histograms()
analyzer.plot_histograms(columns=['TotalPremium', 'TotalClaims', 'CustomValueEstimate', 'SumInsured'])
analyzer.bar_plot_categorical()
analyzer.bar_plot_categorical(columns=['Gender', 'Province', 'CoverType', 'LegalType', 'Product'])


# Plot specific financial columns
analyzer.plot_histograms(columns=['TotalPremium', 'TotalClaims', 'CustomValueEstimate', 'SumInsured'])

# Plot categorical distributions
analyzer.bar_plot_categorical()

# Plot specific categorical columns
analyzer.bar_plot_categorical(columns=['Gender', 'Province', 'CoverType', 'LegalType', 'Product'])
"""