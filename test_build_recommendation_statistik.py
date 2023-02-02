from unittest import TestCase

from build_recommendation_statistik import Code, build

class Test(TestCase):

    # Test unique codenames in recommendations
    def test_do_build_unique_codename(self):
        codes = [Code("windows", "x"), Code("windows", "x"),
                 Code("ubuntu", "x"), Code("ubuntu", "x"),
                 Code("osx", "x"), Code("windows", "x")]

        recommendations = build(codes)
        self.assertEqual(3, len(recommendations))
        codenames = list()
        codenames.append(recommendations[0].codename)
        codenames.append(recommendations[1].codename)
        codenames.append(recommendations[2].codename)

        self.assertIn("windows", codenames)
        self.assertIn("ubuntu", codenames)
        self.assertIn("osx", codenames)

    # Test maximal 3 torecodes in recommendation
    def test_do_build_max_torecodes(self):
        codes = [Code("windows", "Software1"), Code("windows", "Software3"), Code("windows", "Software4"),
                 Code("windows", "Software5")]

        recommendations = build(codes)
        self.assertEqual(3, len(recommendations[0].torecodes))

    # Test order torecodes in recommendation. Count descending
    def test_do_build_order_torecodes(self):
        codes = [Code("windows", "SystemSoftware"),
                 Code("windows", "Software"), Code("windows", "Software"), Code("windows", "Software"),
                 Code("windows", "OperationSystem"), Code("windows", "OperationSystem"),
                 ]

        recommendations = build(codes)
        windows = recommendations[0]

        # expected: windows:[Software, OperationSystem, SystemSoftware]
        self.assertEqual(windows.torecodes[0], "Software")
        self.assertEqual(windows.torecodes[1], "OperationSystem")
        self.assertEqual(windows.torecodes[2], "SystemSoftware")

    def test_code_arguments(self):
        with self.assertRaises(ValueError) as context:
            Code("", "x")
        with self.assertRaises(ValueError) as context:
            Code("x", "")
        with self.assertRaises(ValueError) as context:
            Code(1, "")
        with self.assertRaises(ValueError) as context:
            Code("", 1)