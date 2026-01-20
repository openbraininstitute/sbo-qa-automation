# Copyright (c) 2025 Open Brain Institute
# SPDX-License-Identifier: Apache-2.0
"""
Performance tracking utility for measuring page load times and navigation metrics.
"""
import json
import time
from datetime import datetime
from typing import Dict, Any


class PerformanceTracker:
    """Track and report page performance metrics using Navigation Timing API."""
    
    def __init__(self, browser, logger):
        self.browser = browser
        self.logger = logger
        self.metrics = []
    
    def capture_metrics(self, page_name: str) -> Dict[str, Any]:
        """
        Capture performance metrics for the current page.
        
        Args:
            page_name: Identifier for the page being measured
            
        Returns:
            Dictionary containing performance metrics
        """
        try:
            # Get Navigation Timing API data
            timing_data = self.browser.execute_script("""
                var timing = window.performance.timing;
                var navigation = window.performance.navigation;
                return {
                    navigationStart: timing.navigationStart,
                    domainLookupStart: timing.domainLookupStart,
                    domainLookupEnd: timing.domainLookupEnd,
                    connectStart: timing.connectStart,
                    connectEnd: timing.connectEnd,
                    requestStart: timing.requestStart,
                    responseStart: timing.responseStart,
                    responseEnd: timing.responseEnd,
                    domLoading: timing.domLoading,
                    domInteractive: timing.domInteractive,
                    domContentLoadedEventStart: timing.domContentLoadedEventStart,
                    domContentLoadedEventEnd: timing.domContentLoadedEventEnd,
                    domComplete: timing.domComplete,
                    loadEventStart: timing.loadEventStart,
                    loadEventEnd: timing.loadEventEnd,
                    navigationType: navigation.type,
                    redirectCount: navigation.redirectCount
                };
            """)
            
            # Calculate meaningful metrics
            nav_start = timing_data['navigationStart']
            metrics = {
                'page_name': page_name,
                'url': self.browser.current_url,
                'timestamp': datetime.now().isoformat(),
                'dns_lookup_time': timing_data['domainLookupEnd'] - timing_data['domainLookupStart'],
                'tcp_connection_time': timing_data['connectEnd'] - timing_data['connectStart'],
                'request_time': timing_data['responseStart'] - timing_data['requestStart'],
                'response_time': timing_data['responseEnd'] - timing_data['responseStart'],
                'dom_processing_time': timing_data['domComplete'] - timing_data['domLoading'],
                'dom_interactive_time': timing_data['domInteractive'] - nav_start,
                'dom_content_loaded_time': timing_data['domContentLoadedEventEnd'] - nav_start,
                'page_load_time': timing_data['loadEventEnd'] - nav_start,
                'total_time': timing_data['loadEventEnd'] - nav_start,
                'redirect_count': timing_data['redirectCount']
            }
            
            self.metrics.append(metrics)
            self._log_metrics(metrics)
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to capture performance metrics for {page_name}: {e}")
            return {}
    
    def _log_metrics(self, metrics: Dict[str, Any]):
        """Log performance metrics in a readable format."""
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"Performance Metrics: {metrics['page_name']}")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"URL: {metrics['url']}")
        self.logger.info(f"Total Page Load Time: {metrics['total_time']}ms")
        self.logger.info(f"DNS Lookup: {metrics['dns_lookup_time']}ms")
        self.logger.info(f"TCP Connection: {metrics['tcp_connection_time']}ms")
        self.logger.info(f"Request Time: {metrics['request_time']}ms")
        self.logger.info(f"Response Time: {metrics['response_time']}ms")
        self.logger.info(f"DOM Processing: {metrics['dom_processing_time']}ms")
        self.logger.info(f"DOM Interactive: {metrics['dom_interactive_time']}ms")
        self.logger.info(f"DOM Content Loaded: {metrics['dom_content_loaded_time']}ms")
        self.logger.info(f"{'='*60}\n")
    
    def save_report(self, filename: str = "performance_report.json"):
        """Save all collected metrics to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'test_run': datetime.now().isoformat(),
                    'metrics': self.metrics,
                    'summary': self._generate_summary()
                }, f, indent=2)
            self.logger.info(f"Performance report saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save performance report: {e}")
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics from collected metrics."""
        if not self.metrics:
            return {}
        
        total_times = [m['total_time'] for m in self.metrics if 'total_time' in m]
        
        return {
            'total_pages_measured': len(self.metrics),
            'average_load_time': sum(total_times) / len(total_times) if total_times else 0,
            'min_load_time': min(total_times) if total_times else 0,
            'max_load_time': max(total_times) if total_times else 0,
            'slowest_page': max(self.metrics, key=lambda x: x.get('total_time', 0))['page_name'] if self.metrics else None
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics without saving to file."""
        return self._generate_summary()
