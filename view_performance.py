#!/usr/bin/env python3
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Performance report viewer - Analyze and visualize performance test results.

Usage:
    python view_performance.py performance_public_pages.json
    python view_performance.py performance_*.json  # Compare multiple reports
"""
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def load_report(filepath: str) -> Dict[str, Any]:
    """Load a performance report from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def print_summary(report: Dict[str, Any], filename: str):
    """Print a summary of the performance report."""
    summary = report.get('summary', {})
    test_run = report.get('test_run', 'Unknown')
    
    print(f"\n{'='*70}")
    print(f"📊 Performance Report: {filename}")
    print(f"{'='*70}")
    print(f"Test Run: {test_run}")
    print(f"Pages Measured: {summary.get('total_pages_measured', 0)}")
    print(f"Average Load Time: {summary.get('average_load_time', 0):.2f}ms")
    print(f"Min Load Time: {summary.get('min_load_time', 0)}ms")
    print(f"Max Load Time: {summary.get('max_load_time', 0)}ms")
    print(f"Slowest Page: {summary.get('slowest_page', 'N/A')}")
    print(f"{'='*70}\n")


def print_detailed_metrics(report: Dict[str, Any]):
    """Print detailed metrics for each page."""
    metrics = report.get('metrics', [])
    
    print(f"{'Page':<30} {'Total':<10} {'DNS':<8} {'TCP':<8} {'Request':<10} {'DOM':<10}")
    print(f"{'-'*30} {'-'*10} {'-'*8} {'-'*8} {'-'*10} {'-'*10}")
    
    for metric in metrics:
        page_name = metric.get('page_name', 'Unknown')[:28]
        total = metric.get('total_time', 0)
        dns = metric.get('dns_lookup_time', 0)
        tcp = metric.get('tcp_connection_time', 0)
        request = metric.get('request_time', 0)
        dom = metric.get('dom_processing_time', 0)
        
        print(f"{page_name:<30} {total:<10} {dns:<8} {tcp:<8} {request:<10} {dom:<10}")
    
    print()


def print_slow_pages(report: Dict[str, Any], threshold_ms: int = 3000):
    """Print pages that exceed the threshold."""
    metrics = report.get('metrics', [])
    slow_pages = [m for m in metrics if m.get('total_time', 0) > threshold_ms]
    
    if slow_pages:
        print(f"⚠️  Pages exceeding {threshold_ms}ms threshold:")
        for page in slow_pages:
            print(f"   - {page['page_name']}: {page['total_time']}ms")
        print()
    else:
        print(f"✅ All pages load under {threshold_ms}ms\n")


def compare_reports(reports: List[tuple]):
    """Compare multiple performance reports."""
    print(f"\n{'='*70}")
    print(f"📈 Performance Comparison")
    print(f"{'='*70}\n")
    
    print(f"{'Report':<40} {'Avg Load':<15} {'Slowest Page':<15}")
    print(f"{'-'*40} {'-'*15} {'-'*15}")
    
    for filename, report in reports:
        summary = report.get('summary', {})
        avg = summary.get('average_load_time', 0)
        slowest = summary.get('slowest_page', 'N/A')[:13]
        
        print(f"{filename:<40} {avg:<15.2f} {slowest:<15}")
    
    print()


def print_breakdown(report: Dict[str, Any], page_name: str = None):
    """Print detailed breakdown for a specific page or all pages."""
    metrics = report.get('metrics', [])
    
    if page_name:
        metrics = [m for m in metrics if m['page_name'] == page_name]
        if not metrics:
            print(f"❌ Page '{page_name}' not found in report")
            return
    
    for metric in metrics:
        print(f"\n{'='*70}")
        print(f"🔍 Detailed Breakdown: {metric['page_name']}")
        print(f"{'='*70}")
        print(f"URL: {metric['url']}")
        print(f"Timestamp: {metric['timestamp']}")
        print(f"\nTiming Breakdown:")
        print(f"  DNS Lookup:           {metric['dns_lookup_time']:>6}ms")
        print(f"  TCP Connection:       {metric['tcp_connection_time']:>6}ms")
        print(f"  Request Time:         {metric['request_time']:>6}ms")
        print(f"  Response Time:        {metric['response_time']:>6}ms")
        print(f"  DOM Processing:       {metric['dom_processing_time']:>6}ms")
        print(f"  DOM Interactive:      {metric['dom_interactive_time']:>6}ms")
        print(f"  DOM Content Loaded:   {metric['dom_content_loaded_time']:>6}ms")
        print(f"  {'─'*40}")
        print(f"  Total Page Load:      {metric['total_time']:>6}ms")
        print(f"\nRedirects: {metric['redirect_count']}")
        print(f"{'='*70}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python view_performance.py <report.json> [report2.json ...]")
        print("\nOptions:")
        print("  --detailed              Show detailed metrics for all pages")
        print("  --breakdown [page]      Show detailed breakdown for specific page")
        print("  --threshold <ms>        Set slow page threshold (default: 3000ms)")
        print("\nExamples:")
        print("  python view_performance.py performance_public_pages.json")
        print("  python view_performance.py performance_*.json")
        print("  python view_performance.py report.json --detailed")
        print("  python view_performance.py report.json --breakdown 'Landing Page'")
        sys.exit(1)
    
    # Parse arguments
    files = []
    detailed = False
    breakdown_page = None
    threshold = 3000
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--detailed':
            detailed = True
        elif arg == '--breakdown':
            i += 1
            breakdown_page = sys.argv[i] if i < len(sys.argv) else None
        elif arg == '--threshold':
            i += 1
            threshold = int(sys.argv[i]) if i < len(sys.argv) else 3000
        elif not arg.startswith('--'):
            files.append(arg)
        i += 1
    
    if not files:
        print("❌ No report files specified")
        sys.exit(1)
    
    # Load reports
    reports = []
    for filepath in files:
        try:
            report = load_report(filepath)
            filename = Path(filepath).name
            reports.append((filename, report))
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {filepath}")
            sys.exit(1)
    
    # Display reports
    if len(reports) == 1:
        filename, report = reports[0]
        print_summary(report, filename)
        
        if breakdown_page:
            print_breakdown(report, breakdown_page)
        elif detailed:
            print_detailed_metrics(report)
            print_breakdown(report)
        else:
            print_detailed_metrics(report)
        
        print_slow_pages(report, threshold)
    else:
        # Compare multiple reports
        for filename, report in reports:
            print_summary(report, filename)
        
        compare_reports(reports)


if __name__ == '__main__':
    main()
