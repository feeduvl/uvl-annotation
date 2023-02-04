from unittest import TestCase

from build_recommendation_statistik import Code, build, Recommendation
import jsonpickle
import json


class Test(TestCase):

    # Test Code Class construction, no empty Arguments allowed, only strings allowed
    def test_code_arguments(self):
        with self.assertRaises(ValueError) as context:
            Code("", "x")
        with self.assertRaises(ValueError) as context:
            Code("x", "")
        with self.assertRaises(ValueError) as context:
            Code(1, "")
        with self.assertRaises(ValueError) as context:
            Code("", 1)

    # Test unique codenames in recommendations
    def test_do_build_unique_codename(self):
        codes = [Code("windows", "x"), Code("windows", "x"),
                 Code("ubuntu", "x"), Code("ubuntu", "x"),
                 Code("osx", "x"), Code("windows", "x")]

        recommendations = build(codes)
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
        self.assertEqual(len(recommendations[0].torecodes), Recommendation.MAX_TORE_CODES)

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

    # Test encode Recommendation
    def test_encoding(self):
        recommendations_expected_json_dumps = json.dumps([{"codename": "windows", "torecodes": ["x"]}])
        codes = [Code("windows", "x")]
        recommendations = build(codes)
        recommendations_p_u_false = jsonpickle.encode(recommendations, unpicklable=False)
        self.assertEqual(recommendations_expected_json_dumps, recommendations_p_u_false)

    # Test Recommendation Class construction
    def test_recommendation_arguments(self):
        with self.assertRaises(ValueError) as context:
            Recommendation("", ["x"])
        with self.assertRaises(ValueError) as context:
            Recommendation(1, ["x"])
        with self.assertRaises(ValueError) as context:
            Recommendation("windows", [])
        with self.assertRaises(ValueError) as context:
            Recommendation("windows", "")
        with self.assertRaises(ValueError) as context:
            Recommendation("windows", ["1", "2", "3", "4"])
        with self.assertRaises(ValueError) as context:
            Recommendation("windows", "hund")
