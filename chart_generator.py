#!/usr/bin/env python3
"""
Sprint Effort Estimation Chart Generator
Generates publication-ready charts from benchmark results
"""

import json
import os
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SprintChartGenerator:
    def __init__(self, benchmark_file=None, csv_file=None):
        """Initialize with benchmark data"""
        if benchmark_file is None:
            benchmark_file = "results/benchmark_summary.json"
        if csv_file is None:
            csv_file = "results/model_outputs.csv"
            
        self.benchmark_file = benchmark_file
        self.csv_file = csv_file
        
        # Load data
        with open(benchmark_file, 'r') as f:
            self.summary = json.load(f)
        
        self.df = pd.read_csv(csv_file)
        
        # Create output directory
        self.charts_dir = 'charts'
        os.makedirs(self.charts_dir, exist_ok=True)
        
        print(f"Loaded benchmark data from {benchmark_file}")
        print(f"Loaded CSV data from {csv_file}")
        print(f"Total stories: {len(self.summary['stories'])}")
        print(f"Global mean: {self.summary['global']['mean']:.2f}")

    def create_estimation_accuracy_chart(self):
        """Create estimation accuracy comparison chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Sprint Effort Estimation Analysis', fontsize=16, fontweight='bold')
        
        # Parse estimates from CSV
        estimates = []
        story_ids = []
        for _, row in self.df.iterrows():
            # Parse from raw_output if estimate is null
            if pd.notna(row["estimate"]) and row["estimate"] != "":
                try:
                    estimates.append(float(row["estimate"]))
                    story_ids.append(int(row["story_id"]))
                except:
                    pass
            else:
                # Parse from raw_output
                raw = row["raw_output"]
                try:
                    import json
                    if "```json" in raw:
                        start = raw.find("```json") + 7
                        end = raw.find("```", start)
                        json_str = raw[start:end].strip()
                    else:
                        json_str = raw
                    parsed = json.loads(json_str)
                    if "estimate" in parsed:
                        estimates.append(float(parsed["estimate"]))
                        story_ids.append(int(row["story_id"]))
                except:
                    pass
        
        # 1. Distribution of estimates
        if len(estimates) > 0:
            # Use integer bins for story points (1-10)
            min_est = int(min(estimates))
            max_est = int(max(estimates))
            bins = list(range(min_est, max_est + 2))
            ax1.hist(estimates, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
            ax1.axvline(np.mean(estimates), color='red', linestyle='--', linewidth=2,
                       label=f'Mean: {np.mean(estimates):.2f}')
            ax1.set_xlabel('Story Points')
            ax1.set_ylabel('Frequency')
            ax1.set_title('Distribution of LLM Estimates')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        else:
            ax1.text(0.5, 0.5, 'No valid estimates found', ha='center', va='center', 
                    transform=ax1.transAxes, fontsize=12)
            ax1.set_title('Distribution of LLM Estimates')
        
        # 2. Per-story consistency
        story_means = []
        story_stds = []
        story_labels = []
        
        for story_id, stats in self.summary['stories'].items():
            if stats['mean'] is not None:
                story_means.append(stats['mean'])
                story_stds.append(stats['std'] if stats['std'] is not None else 0)
                story_labels.append(f'Story {story_id}')
        
        bars = ax2.bar(story_labels, story_means, yerr=story_stds, 
                      capsize=5, alpha=0.7, color='lightcoral')
        ax2.set_ylabel('Mean Story Points')
        ax2.set_title('Per-Story Estimates with Standard Deviation')
        ax2.grid(True, alpha=0.3)
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
        
        plt.tight_layout()
        plt.savefig(f'{self.charts_dir}/estimation_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Created estimation accuracy chart")

    def create_consistency_heatmap(self):
        """Create consistency analysis heatmap"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Prepare data for heatmap
        story_ids = []
        consistency_scores = []
        mean_estimates = []
        
        for story_id, stats in self.summary['stories'].items():
            if stats['mean'] is not None:
                story_ids.append(f'Story {story_id}')
                consistency_scores.append(stats['consistency_within_±1'])
                mean_estimates.append(stats['mean'])
        
        # Create heatmap data
        heatmap_data = np.array([consistency_scores, mean_estimates]).T
        
        # Create heatmap
        im = ax.imshow(heatmap_data, cmap='RdYlBu_r', aspect='auto')
        
        # Set labels
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Consistency\n(within ±1)', 'Mean Estimate'])
        ax.set_yticks(range(len(story_ids)))
        ax.set_yticklabels(story_ids)
        
        # Add text annotations
        for i in range(len(story_ids)):
            for j in range(2):
                text = ax.text(j, i, f'{heatmap_data[i, j]:.2f}',
                             ha="center", va="center", color="black", fontweight='bold')
        
        ax.set_title('Story Consistency and Mean Estimates Heatmap', fontsize=14, fontweight='bold')
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Score', rotation=270, labelpad=20)
        
        plt.tight_layout()
        plt.savefig(f'{self.charts_dir}/consistency_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Created consistency heatmap")

    def create_performance_metrics_chart(self):
        """Create performance metrics visualization"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Sprint Effort Estimation Performance Metrics', fontsize=16, fontweight='bold')
        
        # 1. Response time distribution
        response_times = self.df['response_time'].dropna()
        ax1.hist(response_times, bins=15, alpha=0.7, color='lightgreen', edgecolor='black')
        ax1.axvline(response_times.mean(), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {response_times.mean():.2f}s')
        ax1.set_xlabel('Response Time (seconds)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('LLM Response Time Distribution')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Global statistics
        global_stats = self.summary['global']
        metrics = ['Mean', 'Std Dev', 'Median', 'P90']
        values = [global_stats['mean'], global_stats['std'], 
                 global_stats['p50'], global_stats['p90']]
        
        bars = ax2.bar(metrics, values, color=['blue', 'orange', 'green', 'red'], alpha=0.7)
        ax2.set_ylabel('Story Points')
        ax2.set_title('Global Statistics')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{value:.2f}', ha='center', va='bottom')
        
        # 3. Consistency analysis
        consistency_scores = [stats['consistency_within_±1'] for stats in self.summary['stories'].values() 
                             if stats['consistency_within_±1'] is not None]
        
        ax3.hist(consistency_scores, bins=8, alpha=0.7, color='purple', edgecolor='black')
        ax3.axvline(np.mean(consistency_scores), color='red', linestyle='--', linewidth=2,
                   label=f'Mean: {np.mean(consistency_scores):.2f}')
        ax3.set_xlabel('Consistency Score')
        ax3.set_ylabel('Number of Stories')
        ax3.set_title('Consistency Distribution')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Story complexity vs estimates
        story_complexity = []
        story_estimates = []
        
        for story_id, stats in self.summary['stories'].items():
            if stats['mean'] is not None:
                # Simple complexity based on story ID (can be enhanced)
                complexity = int(story_id)  # Use story ID as complexity proxy
                story_complexity.append(complexity)
                story_estimates.append(stats['mean'])
        
        ax4.scatter(story_complexity, story_estimates, alpha=0.7, s=100, color='darkblue')
        ax4.set_xlabel('Story Complexity (arbitrary)')
        ax4.set_ylabel('Mean Estimate')
        ax4.set_title('Story Complexity vs Estimates')
        ax4.grid(True, alpha=0.3)
        
        # Add trend line
        if len(story_complexity) > 1:
            z = np.polyfit(story_complexity, story_estimates, 1)
            p = np.poly1d(z)
            ax4.plot(story_complexity, p(story_complexity), "r--", alpha=0.8)
        
        plt.tight_layout()
        plt.savefig(f'{self.charts_dir}/performance_metrics.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Created performance metrics chart")

    def create_research_summary_chart(self):
        """Create comprehensive research summary chart"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Create a comprehensive summary visualization
        story_ids = list(self.summary['stories'].keys())
        means = [self.summary['stories'][sid]['mean'] for sid in story_ids]
        stds = [self.summary['stories'][sid]['std'] if self.summary['stories'][sid]['std'] is not None else 0 
                for sid in story_ids]
        consistency = [self.summary['stories'][sid]['consistency_within_±1'] 
                      for sid in story_ids]
        
        # Create bar chart with error bars
        x_pos = np.arange(len(story_ids))
        bars = ax.bar(x_pos, means, yerr=stds, capsize=5, alpha=0.7, 
                     color='steelblue', label='Mean Estimate')
        
        # Add consistency as line plot
        ax2 = ax.twinx()
        line = ax2.plot(x_pos, consistency, 'ro-', linewidth=2, markersize=8, 
                       color='red', label='Consistency Score')
        
        # Customize the chart
        ax.set_xlabel('Story ID', fontsize=12)
        ax.set_ylabel('Story Points', fontsize=12, color='steelblue')
        ax2.set_ylabel('Consistency Score', fontsize=12, color='red')
        ax.set_title('Sprint Effort Estimation: LLM Performance Analysis\n'
                    f'Model: qwen2.5-7b-instruct-1m | Global Mean: {self.summary["global"]["mean"]:.2f} ± {self.summary["global"]["std"]:.2f}', 
                    fontsize=14, fontweight='bold')
        
        # Set x-axis labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f'Story {sid}' for sid in story_ids])
        
        # Add grid
        ax.grid(True, alpha=0.3)
        
        # Add legends
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        # Add value labels on bars
        for i, (bar, mean, std) in enumerate(zip(bars, means, stds)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + std + 0.1,
                   f'{mean:.1f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{self.charts_dir}/research_summary.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("Created research summary chart")

    def generate_all_charts(self):
        """Generate all charts"""
        print("Generating sprint effort estimation charts...")
        
        self.create_estimation_accuracy_chart()
        self.create_consistency_heatmap()
        self.create_performance_metrics_chart()
        self.create_research_summary_chart()
        
        print(f"\nAll charts generated successfully in '{self.charts_dir}/' directory:")
        print("- estimation_analysis.png (Estimation accuracy and consistency)")
        print("- consistency_heatmap.png (Consistency analysis)")
        print("- performance_metrics.png (Performance metrics)")
        print("- research_summary.png (Comprehensive research summary)")


def main():
    """Generate all charts"""
    try:
        generator = SprintChartGenerator()
        generator.generate_all_charts()
        
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Please run the sprint project first to generate data:")
        print("python main.py")
    except Exception as e:
        print(f"ERROR: Failed to generate charts: {e}")


if __name__ == "__main__":
    main()
