#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import numpy as np

from src.multiple_graphs import main


class MultipleGraphs(unittest.TestCase):

    def test_first(self):
        with patch("src.multiple_graphs.plt.show") as pshow, \
             patch("src.multiple_graphs.plt.plot") as pplot, \
             patch("src.multiple_graphs.plt.xlabel") as pxlabel, \
             patch("src.multiple_graphs.plt.ylabel") as pylabel:
            main()
            pshow.assert_called_once()
            pxlabel.assert_called_once()
            pylabel.assert_called_once()
            self.assertGreater(pplot.call_count, 0, msg="You should have called plt.plot!")
            self.assertLess(pplot.call_count, 3, msg="You should have called plt.plot at most two times!")
            if pplot.call_count == 2:
                np.testing.assert_array_equal(pplot.call_args_list[0][0][0], [2, 4, 6, 7], err_msg="Wrong parameters to plot!")
                np.testing.assert_array_equal(pplot.call_args_list[0][0][1], [4, 3, 5, 1], err_msg="Wrong parameters to plot!")
                np.testing.assert_array_equal(pplot.call_args_list[1][0][0], [1, 2, 3, 4], err_msg="Wrong parameters to plot!")
                np.testing.assert_array_equal(pplot.call_args_list[1][0][1], [4, 2, 3, 1], err_msg="Wrong parameters to plot!")
            else:
                np.testing.assert_array_equal(
                    pplot.call_args_list[0][0], ([2, 4, 6, 7], [4, 3, 5, 1], [1, 2, 3, 4], [4, 2, 3, 1]),
                    err_msg="Parameters to the plt.plot command were wrong")

    def test_labels_are_strings(self):
        with patch("src.multiple_graphs.plt.show"), \
             patch("src.multiple_graphs.plt.plot"), \
             patch("src.multiple_graphs.plt.xlabel") as pxlabel, \
             patch("src.multiple_graphs.plt.ylabel") as pylabel:
            main()
            xlabel_arg = pxlabel.call_args[0][0] if pxlabel.call_args and pxlabel.call_args[0] else None
            ylabel_arg = pylabel.call_args[0][0] if pylabel.call_args and pylabel.call_args[0] else None
            self.assertIsInstance(
                xlabel_arg, str,
                msg="plt.xlabel should be called with a string label. Got %r." % (xlabel_arg,))
            self.assertIsInstance(
                ylabel_arg, str,
                msg="plt.ylabel should be called with a string label. Got %r." % (ylabel_arg,))

    def test_xlabel_and_ylabel_are_different(self):
        with patch("src.multiple_graphs.plt.show"), \
             patch("src.multiple_graphs.plt.plot"), \
             patch("src.multiple_graphs.plt.xlabel") as pxlabel, \
             patch("src.multiple_graphs.plt.ylabel") as pylabel:
            main()
            xlabel_arg = pxlabel.call_args[0][0] if pxlabel.call_args and pxlabel.call_args[0] else None
            ylabel_arg = pylabel.call_args[0][0] if pylabel.call_args and pylabel.call_args[0] else None
            self.assertNotEqual(
                xlabel_arg, ylabel_arg,
                msg="plt.xlabel and plt.ylabel were both called with %r - they should label "
                    "different axes, not be a copy-pasted duplicate." % (xlabel_arg,))


if __name__ == '__main__':
    unittest.main()
