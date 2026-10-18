"""Tests for the keyless SEC path.

`sec_fundamentals.py` parses SEC XBRL facts into the same model inputs the FMP path builds, so
these pin the parser against a frozen facts payload, the mapping from XBRL tags to concepts, and
the claim that both sources render the model through the same code. They need no key and no
network.
"""
import importlib.util
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(REPO, "skills", "dcf-model", "scripts", "sec_fundamentals.py")


def load_module():
    spec = importlib.util.spec_from_file_location("sec_fundamentals", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sec = load_module()


def gaap(units, form="10-K", start="2023-01-01", end="2023-12-31", val=100.0):
    fact = {"form": form, "end": end, "val": val}
    if start:
        fact["start"] = start
    return {"units": {"USD": [fact]}}


class TestAnnual(unittest.TestCase):
    def test_quarterly_facts_are_dropped_and_order_is_oldest_first(self):
        facts = {"Revenues": {"units": {"USD": [
            {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K", "val": 100.0},
            {"start": "2022-01-01", "end": "2022-12-31", "form": "10-K", "val": 90.0},
            {"start": "2023-04-01", "end": "2023-06-30", "form": "10-Q", "val": 40.0},
        ]}}}
        series, tag = sec.annual(facts, "revenue")
        self.assertEqual([v for _, v in series], [90.0, 100.0])
        self.assertEqual(tag, "Revenues")

    def test_preferred_tag_wins_when_both_are_filed(self):
        facts = {"RevenueFromContractWithCustomerExcludingAssessedTax": gaap(None),
                 "Revenues": gaap(None, val=999.0)}
        series, tag = sec.annual(facts, "revenue")
        self.assertEqual(tag, "RevenueFromContractWithCustomerExcludingAssessedTax")
        self.assertEqual([v for _, v in series], [100.0])

    def test_fallback_tag_is_used_when_the_preferred_one_is_missing(self):
        facts = {"RevenueFromContractWithCustomerIncludingAssessedTax": gaap(None, val=77.0)}
        series, tag = sec.annual(facts, "revenue")
        self.assertEqual(tag, "RevenueFromContractWithCustomerIncludingAssessedTax")
        self.assertEqual([v for _, v in series], [77.0])

    def test_balance_sheet_items_with_no_start_date_are_kept(self):
        facts = {"CashAndCashEquivalentsAtCarryingValue": gaap(None, start=None, val=5.0)}
        series, _ = sec.annual(facts, "cash")
        self.assertEqual(series, [("2023-12-31", 5.0)])

    def test_a_duration_outside_one_year_is_dropped(self):
        # A transition period or a stub year is not comparable to a full year.
        facts = {"Revenues": {"units": {"USD": [
            {"start": "2023-07-01", "end": "2023-12-31", "form": "10-K", "val": 50.0},
            {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K", "val": 100.0},
        ]}}}
        series, _ = sec.annual(facts, "revenue")
        self.assertEqual([v for _, v in series], [100.0])

    def test_amendments_and_restatements_leave_one_value_per_year(self):
        facts = {"Revenues": {"units": {"USD": [
            {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K/A", "val": 100.0},
            {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K", "val": 90.0},
        ]}}}
        series, _ = sec.annual(facts, "revenue")
        self.assertEqual(len(series), 1)
        self.assertEqual(series[0][0], "2023-12-31")

    def test_a_concept_with_no_filed_tag_returns_nothing(self):
        self.assertEqual(sec.annual({"Revenues": gaap(None)}, "short_inv"), ([], None))

    def test_share_counts_use_the_shares_unit(self):
        facts = {"WeightedAverageNumberOfDilutedSharesOutstanding": {"units": {"shares": [
            {"start": "2023-01-01", "end": "2023-12-31", "form": "10-K", "val": 1_000_000}]}}}
        series, _ = sec.annual(facts, "shares")
        self.assertEqual([v for _, v in series], [1_000_000.0])


class TestSharedPath(unittest.TestCase):
    """The docstring promises the SEC path renders through the FMP path's code, so the two
    sources cannot print different-looking models. That promise is a join, not a copy."""

    def test_report_is_the_fmp_script_s_function(self):
        self.assertEqual(sec.report.__module__, "fmp_dcf")
        self.assertTrue(sec.report.__code__.co_filename.endswith("fmp_dcf.py"))

    def test_terminal_growth_at_or_above_the_discount_rate_exits_before_any_request(self):
        # Nothing is fetched before this check, so the test stays offline.
        with self.assertRaises(SystemExit) as caught:
            sec.run("UBER", 0.09, 0.09, 5, None)
        self.assertIn("must stay below", str(caught.exception.code))


if __name__ == "__main__":
    unittest.main()
