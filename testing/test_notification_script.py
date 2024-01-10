import sys
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '..'))

from scripts.NotificationScript import broken_support, broken_resistance
import unittest
from unittest.mock import patch, ANY

class TestNotificationScript(unittest.TestCase):

    @patch('scripts.NotificationScript.get_support_resistance_values')
    @patch('scripts.NotificationScript.yf.download')
    @patch('scripts.NotificationScript.get_current_price')
    @patch('scripts.NotificationScript.update_value')
    def test_broken_support(self, mock_update_value, mock_get_current_price, mock_yf_download, mock_get_sr):
        """
        Test the 'broken_support' function in NotificationScript.py.
        """

        # Mock values
        symbol = 'AAPL'
        old_value = 55.0
        sr_filtered_mock = [50.0, 52.0, 55.0, 60.0]
        mock_get_sr.return_value = sr_filtered_mock

        # Test function
        broken_support(symbol, old_value)

        # Support and resistance assertions
        mock_update_value.assert_any_call(ANY, symbol, 'support', 52.0)
        mock_update_value.assert_any_call(ANY, symbol, 'resistance', 55.0)

    @patch('scripts.NotificationScript.get_support_resistance_values')
    @patch('scripts.NotificationScript.yf.download')
    @patch('scripts.NotificationScript.get_current_price')
    @patch('scripts.NotificationScript.update_value')
    def test_broken_resistance(self, mock_update_value, mock_get_current_price, mock_yf_download, mock_get_sr):
        
        """
        Test the 'broken_resistance' function in NotificationScript.py.
        """

        # Mock values
        symbol = 'AAPL'
        old_value = 55.0
        sr_filtered_mock = [50.0, 52.0, 55.0, 60.0]
        mock_get_sr.return_value = sr_filtered_mock

        # Test function
        broken_resistance(symbol, old_value)

        # Support and resistance assertions
        mock_update_value.assert_any_call(ANY, symbol, 'support', 55.0)
        mock_update_value.assert_any_call(ANY, symbol, 'resistance', 60.0)
        
if __name__ == '__main__':
    unittest.main()
    