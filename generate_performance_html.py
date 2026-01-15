#!/usr/bin/env python3
# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Generate HTML report from performance JSON data.

Usage:
    python generate_performance_html.py performance_public_pages.json
"""
import json
import sys
from pathlib import Path
from datetime import datetime


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Report - {test_run}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #f5f5f5;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 28px;
        }}
        .meta {{
            color: #7f8c8d;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .summary-card.green {{
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }}
        .summary-card.orange {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .summary-card.blue {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        .summary-label {{
            font-size: 12px;
            opacity: 0.9;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .summary-value {{
            font-size: 32px;
            font-weight: bold;
        }}
        .summary-unit {{
            font-size: 16px;
            opacity: 0.9;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        th {{
            background: #34495e;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .metric-bar {{
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            position: relative;
        }}
        .metric-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 0.3s ease;
        }}
        .metric-fill.fast {{
            background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%);
        }}
        .metric-fill.slow {{
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        }}
        .page-details {{
            margin-bottom: 40px;
        }}
        .page-card {{
            background: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .page-title {{
            font-size: 20px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .page-url {{
            color: #7f8c8d;
            font-size: 14px;
            margin-bottom: 15px;
            word-break: break-all;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        .metric-item {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .metric-label {{
            font-size: 11px;
            color: #7f8c8d;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Performance Test Report</h1>
        <div class="meta">Generated: {generated_at} | Test Run: {test_run}</div>
        
        <div class="summary">
            <div class="summary-card blue">
                <div class="summary-label">Pages Tested</div>
                <div class="summary-value">{total_pages}</div>
            </div>
            <div class="summary-card green">
                <div class="summary-label">Average Load Time</div>
                <div class="summary-value">{avg_load:.0f}<span class="summary-unit">ms</span></div>
            </div>
            <div class="summary-card">
                <div class="summary-label">Fastest Page</div>
                <div class="summary-value">{min_load}<span class="summary-unit">ms</span></div>
            </div>
            <div class="summary-card orange">
                <div class="summary-label">Slowest Page</div>
                <div class="summary-value">{max_load}<span class="summary-unit">ms</span></div>
            </div>
        </div>
        
        <h2 style="margin-bottom: 20px; color: #2c3e50;">Performance Overview</h2>
        <table>
            <thead>
                <tr>
                    <th>Page</th>
                    <th>Total Time</th>
                    <th>DNS</th>
                    <th>TCP</th>
                    <th>Request</th>
                    <th>Response</th>
                    <th>DOM</th>
                    <th>Visual</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
        
        <h2 style="margin-bottom: 20px; color: #2c3e50;">Detailed Metrics</h2>
        <div class="page-details">
            {page_cards}
        </div>
        
        <div class="footer">
            Generated by OBI Performance Tracker | {generated_at}
        </div>
    </div>
</body>
</html>
"""


def generate_table_row(metric, max_time):
    """Generate a table row for a page metric."""
    total = metric['total_time']
    speed_class = 'fast' if total < 1000 else ('slow' if total > 3000 else '')
    bar_width = (total / max_time * 100) if max_time > 0 else 0
    
    return f"""
        <tr>
            <td><strong>{metric['page_name']}</strong></td>
            <td>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="min-width: 60px;"><strong>{total}ms</strong></span>
                    <div class="metric-bar" style="flex: 1;">
                        <div class="metric-fill {speed_class}" style="width: {bar_width}%;"></div>
                    </div>
                </div>
            </td>
            <td>{metric['dns_lookup_time']}ms</td>
            <td>{metric['tcp_connection_time']}ms</td>
            <td>{metric['request_time']}ms</td>
            <td>{metric['response_time']}ms</td>
            <td>{metric['dom_processing_time']}ms</td>
            <td>{metric['dom_interactive_time']}ms</td>
        </tr>
    """


def generate_page_card(metric):
    """Generate a detailed card for a page."""
    return f"""
        <div class="page-card">
            <div class="page-title">{metric['page_name']}</div>
            <div class="page-url">{metric['url']}</div>
            <div class="metrics-grid">
                <div class="metric-item">
                    <div class="metric-label">Total Time</div>
                    <div class="metric-value">{metric['total_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">DNS Lookup</div>
                    <div class="metric-value">{metric['dns_lookup_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">TCP Connection</div>
                    <div class="metric-value">{metric['tcp_connection_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Request</div>
                    <div class="metric-value">{metric['request_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Response</div>
                    <div class="metric-value">{metric['response_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">DOM Processing</div>
                    <div class="metric-value">{metric['dom_processing_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">DOM Interactive</div>
                    <div class="metric-value">{metric['dom_interactive_time']}ms</div>
                </div>
                <div class="metric-item">
                    <div class="metric-label">Content Loaded</div>
                    <div class="metric-value">{metric['dom_content_loaded_time']}ms</div>
                </div>
            </div>
        </div>
    """


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_performance_html.py <report.json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.json', '.html')
    
    # Load report
    try:
        with open(input_file, 'r') as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in file: {input_file}")
        sys.exit(1)
    
    # Extract data
    summary = report.get('summary', {})
    metrics = report.get('metrics', [])
    test_run = report.get('test_run', 'Unknown')
    
    max_time = max([m['total_time'] for m in metrics]) if metrics else 1
    
    # Generate HTML components
    table_rows = '\n'.join([generate_table_row(m, max_time) for m in metrics])
    page_cards = '\n'.join([generate_page_card(m) for m in metrics])
    
    # Generate HTML
    html = HTML_TEMPLATE.format(
        test_run=test_run,
        generated_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        total_pages=summary.get('total_pages_measured', 0),
        avg_load=summary.get('average_load_time', 0),
        min_load=summary.get('min_load_time', 0),
        max_load=summary.get('max_load_time', 0),
        table_rows=table_rows,
        page_cards=page_cards
    )
    
    # Save HTML
    with open(output_file, 'w') as f:
        f.write(html)
    
    print(f"✅ HTML report generated: {output_file}")
    print(f"   Open in browser: file://{Path(output_file).absolute()}")


if __name__ == '__main__':
    main()
