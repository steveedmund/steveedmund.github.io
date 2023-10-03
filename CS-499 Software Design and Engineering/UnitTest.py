import unittest
import pandas as pd
from CS340_FinalProjectV1 import (
    add_marker_with_popup,
    update_map,
    update_dashboard,
    update_styles,
    update_graphs,
)

# Sample data for testing
sample_data = {
    "col1": [1, 2, 3],
    "col2": ["A", "B", "C"],
    "latitude": [30.75, 31.0, 30.8],
    "longitude": [-97.48, -97.5, -97.6],
}


class TestYourFunctions(unittest.TestCase):

    def setUp(self):
        # Create a sample DataFrame for testing
        self.dff = pd.DataFrame(sample_data)

    def test_add_marker_with_popup_valid(self):
        selected_row = 0
        result = add_marker_with_popup(selected_row, self.dff)
        self.assertIn("Marker(position=(30.75, -97.48), children=", result)

    def test_add_marker_with_popup_invalid(self):
        selected_row = 5  # Index out of range
        result = add_marker_with_popup(selected_row, self.dff)
        self.assertEqual(
            result, "Error: Index out of range - Selected row index is out of range."
        )

    def test_update_map_valid(self):
        selected_rows = [0, 1]
        result = update_map(sample_data, selected_rows, [])
        self.assertIn("dl.Map(style={'width':'1000px', 'height': '500px'}, center=", result[0])

    def test_update_map_empty(self):
        selected_rows = []
        result = update_map(sample_data, selected_rows, [])
        self.assertIn("dl.Map(style={'width':'1000px', 'height': '500px'}, center=", result[0])

    def test_update_dashboard_reset(self):
        filter_type = "RESET"
        data, columns = update_dashboard(filter_type)
        self.assertEqual(len(data), len(self.dff))
        self.assertEqual(columns[0]["name"], "col1")
        self.assertEqual(columns[1]["name"], "col2")

    def test_update_dashboard_invalid_filter(self):
        filter_type = "INVALID_FILTER"
        data, columns = update_dashboard(filter_type)
        self.assertEqual(len(data), 0)
        self.assertEqual(len(columns), 1)
        self.assertEqual(columns[0]["name"], "Error")

    def test_update_styles_valid(self):
        selected_columns = ["col1"]
        styles = update_styles(selected_columns)
        self.assertEqual(len(styles), 1)
        self.assertEqual(styles[0]["if"]["column_id"], "col1")
        self.assertEqual(styles[0]["background_color"], "#D2F3FF")

    def test_update_styles_invalid(self):
        selected_columns = "col1"  # Should be a list
        styles = update_styles(selected_columns)
        self.assertEqual(len(styles), 0)

    def test_update_graphs_valid(self):
        view_data = sample_data
        result = update_graphs(view_data)
        self.assertIn("dcc.Graph(", result[0])

    def test_update_graphs_invalid(self):
        view_data = None
        result = update_graphs(view_data)
        self.assertEqual(result[0], "Error: Invalid data format.")


if __name__ == "__main__":
    unittest.main()
