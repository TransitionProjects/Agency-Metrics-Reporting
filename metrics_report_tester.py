__author__ = "David Katz-Wigmore"
__version__ = ".1"

import create_sheets
import pandas as pd
import unittest

from all_functions import MetricsFunctions as mf
from tkinter.filedialog import askopenfilename

class TestMethods(unittest.TestCase):
    def setUp(self):
        pass

    def test_average_los_in_es_shelter(self):
        """
        Testing for cleaned=True fails because of data set having no outliers.  Make a new data set to test this method
        correctly please.

        :return:
        """
        test_ee_df = pd.read_excel("testing_data\ee_test_data.xlsx", sheet_name="Report 1")
        self.assertEqual(
            mf().average_los_in_es_shelter(test_ee_df),
            tuple(["Length of stay per emergency shelter resident (days)", "", 31])
        )

    def test_calculate_average_wait_list_length(self):
        """
        The test_waitlist file is more complicated than the other testing data files which means the test is going to be
        more accurate.  Other testing data files need to be deepened to look more like this one by which I mean
        including values that will lead to the wrong output if the script is not performing as expected.

        :return:
        """
        test_wait_list = pd.read_csv(askopenfilename(title="Test Waitlist.csv"), delimiter=",", parse_dates=[5, 7, 8, 14], dayfirst=False)
        self.assertEqual(
            mf().calculate_average_wait_list_length(test_wait_list, waitlist="Men"),
            tuple(["Length of Men's shelter waitlist (in days)", "", "31.0 Days"])
        )
        self.assertEqual(
            mf().calculate_average_wait_list_length(test_wait_list, "Women"),
            tuple(["Length of Women's shelter waitlist (in days)", "", "31.0 Days"])
        )

    def test_count_all_ep(self):
        """
        This will need to be updated after all the unit tests that use this file are created and the final value it
        should return has been found.  Failing to do so will result in false positives/failures.

        :return:
        """

        test_placements = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_all_ep(test_placements),
            tuple(["124 participants will have their evictions prevented", 124, 3])
        )

    def test_count_all_pp(self):
        """
        This will need to be updated after all the unit tests that use this file are created and the final value it
        should return has been found.  Failing to do so will result in false positives/failures.

        :return:
        """

        test_placements = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_all_pp(test_placements),
            tuple(["1,065 participants will be permanently housed*", 1065, 2])
        )

    def count_all_placed(self):
        """
        This will need to be updated after all the unit tests that use this file are created and the final value it
        should return has been found.  Failing to do so will result in false positives/failures.

        :return:
        """

        test_placements = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_all_placed(test_placements),
            6
        )

    def count_all_placed_by_provider(self):
        """
        This will need to be updated after all the unit tests that use this file are created and the final value it
        should return has been found.  Failing to do so will result in false positives/failures.

        :return:
        """

        test_placements = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["ACCESS"]),
            2
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["SSVF - TPI"]),
            2
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["Residential CM"]),
            1
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["Retention"]),
            1
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["SSVF - TPI", "Residential CM"]),
            2
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["SSVF - TPI", "Retention"]),
            2
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["SSVF - TPI", "ACCESS"]),
            3
        )
        self.assertEqual(
            mf().count_all_placed_by_provider(test_placements, ["SSVF - TPI", "Residential CM", "Retention", "ACCESS"]),
            5
        )

    def test_entries_by_provider(self):
        """

        :return:
        """
        test_ee_df = pd.read_excel("testing_data\ee_test_data.xlsx", sheet_name="Report 1")
        self.assertEqual(
            mf().count_entries_by_provider(test_ee_df, "Residential"),
            tuple(["Engage 900 participants in case management", 900, 1])
        )
        self.assertEqual(
            mf().count_entries_by_provider(test_ee_df, "ACCESS"),
            tuple(["Engage 1200 participants in case management", 1200, 1])
        )
        self.assertEqual(
            mf().count_entries_by_provider(test_ee_df, "Clark Center"),
            tuple(["550 unduplicated participants have a safe place to sleep at Clark Center", 550, 1])
        )
        self.assertEqual(
            mf().count_entries_by_provider(test_ee_df, "Doreen's"),
            tuple(["550 unduplicated participants have a safe place to sleep at Doreen's", 550, 2])
        )
        self.assertEqual(
            mf().count_entries_by_provider(test_ee_df, "Jean's Place L1"),
            tuple(["350 unduplicated participants have a safe place to sleep at Jean's Place", 350, 1])
        )

    def test_count_households_screened(self):
        """
        No updates should be needed.

        :return:
        """

        test_screened = pd.read_excel("testing_data\All Entries TPI + Household.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_households_screened(test_screened),
            tuple(["Screen 784 veteran families for services", 784, 2])
        )

    def test_count_hygiene_services_by_provider(self):
        """
        This may need to have the third number of the tuple in the assertEqual statement updated as the services chart
        will grow as more unit tests are created.  This growth of the services chart may cause the expected results to
        change, thus the required update.

        :return:
        """
        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_hygiene_services_by_provider(test_service_data, "Day Center"),
            tuple(["40,000 hygiene services provided", 40000, 5])
        )
        self.assertEqual(
            mf().count_hygiene_services_by_provider(test_service_data, "Agency"),
            tuple(["7,500 participants will receive hygiene services", 7500, 9])
        )

    def test_count_id_assistance_by_provider(self):
        """
        May need to be updated after all services related unit tests are created as the
        "All Services (All Agency) Test.xlsx" file may have been altered to accommodate the needs of other tests.

        :return:
        """

        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_id_assistance_by_provider(test_service_data, "Day Center"),
            tuple(["1500 individuals received assistance obtaining ID documents", 1500, 2])
        )

    def test_count_mailing_services_by_day_center(self):
        """
        May need to be updated after all services related unit tests are created as the
        "All Services (All Agency) Test.xlsx" file may have been altered to accommodate the needs of other tests.

        :return:
        """

        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_mailing_services_by_day_center(test_service_data),
            tuple(["43,000 mailing services provided", 43000, 1])
        )

    def test_count_ongoing_cm_services(self):
        """
        May need to be updated after all services related unit tests are created as the
        "All Services (All Agency) Test.xlsx" file may have been altered to accommodate the needs of other tests.

        :return:
        """
        test_service_data = pd.read_excel("testing_data\Count Ongoing CM Services Services Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_ongoing_cm_services(test_service_data),
            tuple(["2,100 participants served through case management", 2100, 6])
        )

    def test_count_ongoing_cm_services_by_department(self):
        """
        May need to be updated after all services related unit tests are created as the
        "All Services (All Agency) Test.xlsx" file may have been altered to accommodate the needs of other tests.

        :return:
        """
        test_service_data = pd.read_excel("testing_data\Count Ongoing CM Services Services Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_ongoing_cm_services_by_department(test_service_data, "SSVF"),
            tuple(["Provide ongoing case management to 450 participants", 450, 1])
        )
        self.assertEqual(
            mf().count_ongoing_cm_services_by_department(test_service_data, "Residential"),
            tuple(["Provide ongoing case management to 700 participants", 700, 0])
        )
        self.assertEqual(
            mf().count_ongoing_cm_services_by_department(test_service_data, "Retention"),
            tuple(["Provide ongoing case management to 800 participants", 800, 1])
        )

    def test_count_perm_by_provider(self):
        """

        :return:
        """
        test_placement_data = pd.read_excel("testing_data\Count Perm By Provider Placements Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_perm_by_provider(test_placement_data, ["ACCESS"]),
            tuple(["415 participants move into permanent housing", 415, 1])
        )
        self.assertEqual(
            mf().count_perm_by_provider(test_placement_data, ["SSVF - TPI"]),
            tuple(["262 veteran families will move into permanent housing", 262, 1])
        )

    def test_count_pts_with_barrier_mitigation_and_doc_prep(self):
        """

        :return:
        """
        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_pts_with_barrier_mitigation_and_doc_prep(test_service_data, "Coordinated"),
            tuple(["Provide barrier mitigation and document prep to 150 individuals", 150, 1])
        )

    def test_count_ep_by_provider(self):
        """

        :return:
        """
        test_placement_data = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_ep_by_provider(test_placement_data, provider=["SSVF - TPI"]),
            tuple(["56 veteran families will have evictions prevented", 56, 1])
        )

    def test_count_latinos_served_by_provider(self):
        """
        Make sure to change the predicted output value as the services chart is altered to test other metrics focused
        upon Race/Ethnicity

        :return:
        """
        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_latinos_served_by_provider(test_service_data, "Wellness Access"),
            1
        )

    def test_count_legal_barriers_mitigated(self):
        """

        :return:
        """
        test_entries = pd.read_excel("testing_data\All Entries TPI Test.xlsx", sheet_name="Sheet1")
        test_service_data = pd.read_excel("testing_data\Count Legal Barriers Mitigated Services Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_legal_barriers_mitigated(test_entries, test_service_data, "SSVF"),
            tuple(["50 veteran families will have legal barriers mitigated", 50, 1])
        )

    def test_count_poc_placed(self):
        """
        The assertEqual statement will need to be updated as more testing methods for poc placements are added.

        :return:
        """
        test_placement_data = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_poc_placed(test_placement_data, test_service_data),
            1
        )

    def test_count_poc_placed_by_provider(self):
        """

        :return:
        """
        test_placement_data = pd.read_excel("testing_data\Placement Report v.3 Test.xls", sheet_name="Sheet1")
        test_service_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_poc_placed_by_provider(test_placement_data, test_service_data),
            1
        )

    def test_count_provider(self):
        """

        :return:
        """
        test_ee_df = pd.read_excel("testing_data\ee_test_data.xlsx", sheet_name="Report 1")
        self.assertEqual(
            mf().count_provider(test_ee_df, "ACCESS", 1),
            tuple(["{} participants served by {}".format(1, "ACCESS"), 1, 1])
        )
        self.assertEqual(
            mf().count_provider(test_ee_df, "Residential", 1),
            tuple(["{} participants served by {}".format(1, "Residential"), 1, 1])
        )
        self.assertEqual(
            mf().count_provider(test_ee_df, "Retention", 1),
            tuple(["{} participants served by {}".format(1, "Retention"), 1, 1])
        )
        self.assertEqual(
            mf().count_provider(test_ee_df, "SSVF", 12),
            tuple(["{} participants served by {}".format(12, "SSVF"), 12, 12])
        )

    def test_count_referrals_resulting_in_connections(self):
        """

        :return:
        """

        test_services_data = pd.read_excel("testing_data\All Services (All Agency) + Need Status.xlsx", sheet_name="Service Data")
        test_needs_data = pd.read_excel("testing_data\All Services (All Agency) + Need Status.xlsx", sheet_name="Need Data")
        self.assertEqual(
            mf().count_referrals_resulting_in_connections(
                test_services_data,
                test_needs_data,
                "Wellness",
                ["Referral - Eye Care", "Referral - Dental Care", "Referral - Medical Care"],
                "med count"
            ),
            tuple([
                "200 connections to medical care per year",
                200,
                2
            ])
        )
        self.assertEqual(
            mf().count_referrals_resulting_in_connections(
                test_services_data,
                test_needs_data,
                "Wellness",
                ["Referral - Eye Care", "Referral - Dental Care", "Referral - Medical Care"],
                "percent med"
            ),
            tuple([
                "50% of referrals result in connection to medical care provider",
                "50%",
                "1/2 = 50.0%"
            ])
        )
        self.assertEqual(
            mf().count_referrals_resulting_in_connections(
                test_services_data,
                test_needs_data,
                "Wellness",
                [
                    "Referral - A&D Support",
                    "Referral - DV Support",
                    "Referral - Mental Health Care",
                    "Referral - MH Support"
                ],
                "mh sud count"
            ),
        tuple([
            "700 connections to mental health or SUD services per year",
            700,
            2
        ])
        )
        self.assertEqual(
            mf().count_referrals_resulting_in_connections(
                test_services_data,
                test_needs_data,
                "Wellness",
                [
                    "Referral - A&D Support",
                    "Referral - DV Support",
                    "Referral - Mental Health Care",
                    "Referral - MH Support"
                ],
                "percent mh sud"
            ),
            tuple([
                "50% of referrals result in connection to mental health and/or SUD services",
                "50%",
                "1/2 = 50.0%"
            ])
        )

    def test_count_rent_assist(self):
        """

        :return:
        """
        test_services_data = pd.read_excel("testing_data\All Services (All Agency) Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_rent_assist(test_services_data),
            tuple(["900 participants will receive rent assistance", 900, 1])
        )

    def test_count_retention_by_length(self):
        """
        The only difference between the agency and departmental output, as defined by the 'provider' parameter is the
        wording of the first element of the tuple.  As such both possible outputs can be tested with a single
        call of assertEqual.

        :return:
        """
        test_follow_up_data = pd.read_excel("testing_data\FollowUps v.1 Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_retention_by_length(test_follow_up_data, 12, "agency"),
            tuple([
                "80% participants retain their housing for 12 months post-subsidy*",
                "80%",
                "{}/{} = {}%".format(1, 2, 100*(1 / 2))
            ])
        )

    def test_count_served_by_provider(self):
        """


        :return:
        """

        test_services_data = pd.read_excel("testing_data\Count Served By Provider Services Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_served_by_provider(test_services_data, "Day"),
            4
        )

    def test_count_services_by_provider(self):
        """

        :return:
        """

        test_services_data = pd.read_excel("testing_data\Count Served By Provider Services Test.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_services_by_provider(test_services_data, "Day"),
            tuple(["85000 total services in the {}".format("Day"), 85000, 6])
        )

    def test_count_shelter_stays(self):
        """

        :return:
        """
        test_ee_df = pd.read_excel("testing_data\ee_test_data.xlsx", sheet_name="Report 1")
        self.assertEqual(
            mf().count_shelter_stays(test_ee_df, True),
            tuple(["2,850 participants will have a safe place to sleep at night*", 2850, 11])
        )
        self.assertEqual(
            mf().count_shelter_stays(test_ee_df, False),
            tuple(["1,000 participants will have a safe place to sleep", 1000, 4])
        )

    def test_count_shelter_to_perm_w_group(self):
        """
        Make a detailed test case for this.  We need to make sure these numbers are coming through extremely accurately
        as they will affect some agency wide decision making.  Revamp test data as needed to ensure accuracy.
        :return:
        """
        test_ee_data = pd.read_excel("testing_data\Count Shelter to Perm w Group Entries.xlsx", sheet_name="Sheet1")
        test_services_data = pd.read_excel("testing_data\Count Shelter to Perm w Group Services.xlsx", sheet_name="Service Data")
        self.assertEqual(
            mf().count_shelter_to_perm_w_group(test_ee_data, test_services_data, True),
            tuple([
                "10% increase in housing placements for participants who attend groups",
                "10%",
                "{}/{} = {}% for current quarter.  Please subtract from number from previous quarter".format(
                    1,
                    1,
                    100 * (1 / 1)
                )
            ])
        )
        self.assertEqual(
            mf().count_shelter_to_perm_w_group(test_ee_data, test_services_data, False),
            tuple([
                "10% increase in service-intensive shelter placements for participants who attend groups",
                "10%",
                "{}/{} = {}% for current quarter.  Please subtract from number from previous quarter".format(
                    1,
                    2,
                    100 * (1 / 2)
                )
            ])
        )

    def test_count_transportation_passes_by_provider(self):
        """

        :return:
        """
        test_services_data = pd.read_excel("testing_data\Day Center Transportation Services.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().count_transportation_passes_by_provider(test_services_data, "Day Center"),
            tuple([
                "1300 individuals received local transit passes",
                1300,
                2
            ])
        )

    def test_days_from_id_to_placement(self):
        """

        :return:
        """
        placements_test = pd.read_excel("testing_data\ID to Placement Placements Test.xlsx", sheet_name="Sheet1")
        entries_test = pd.read_excel("testing_data\ID to Placement Entries Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().days_from_id_to_placement(placements_test, entries_test, "ACCESS", ["ACCESS"]),
            tuple([
                "Number of days from identification to placement <90*",
                "<90",
                24
            ])
        )

    def test_exit_destination_by_provider(self):
        """

        :return:
        """
        entry_test = pd.read_excel("testing_data\Exit Destination By Provider Entries.xlsx", sheet_name="Sheet1")
        entries, perm, temp, exits = mf().exit_destination_by_provider(entry_test, "Hansen", "all")
        self.assertEqual(len(perm.index), 4)
        self.assertEqual(len(entries.index), 10)
        self.assertEqual(len(temp.index), 4)
        self.assertEqual(len(exits.index), 9)

    def test_percent_exits_from_low_barrier_to_service_intensive(self):
        """

        :return:
        """

        entries_test = pd.read_excel("testing_data\Percent Exits to Service Intensive Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_exits_from_low_barrier_to_service_intensive(entries_test, "Hansen"),
            tuple([
                "16% of Hansen participants move to a services-intensive shelter",
                "16%",
                "{} / {} = {}%".format(5, 6, 100*(5/6))
            ])
        )

    def test_percent_exits_caused_by_exclusion(self):
        """

        :return:
        """

        entry_exit_test = pd.read_excel("testing_data\Percent Exits Caused By Exclusions Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_exits_caused_by_exclusion(entry_exit_test, "es"),
            tuple([
                "15% decrease in behavior based exclusions",
                "<= -15%",
                "{} / {} = {} <--- Don't forget to subtract this from the previous quarters numbers".format(5, 10, 50.0)
            ])
        )

    def test_percent_iap_successful(self):
        """


        :return:
        """

        percent_iap_successful_test = pd.read_excel("testing_data\Percent IAP Successful Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_iap_successful(percent_iap_successful_test),
            tuple([
                "60% of IAPs will be successfully completed by participants",
                "60%",
                "{}/{} = {}%".format(5, 9, 100 * (5 / 9))
            ])
        )

    def test_percent_low_barrier_in_groups(self):
        """

        :return:
        """
        percent_in_groups_entries_test = pd.read_excel("testing_data\Percent In Group Entries Test.xlsx", sheet_name="Sheet1")
        percent_in_groups_services_test = pd.read_excel("testing_data\Percent in Groups Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_low_barrier_in_groups(
                percent_in_groups_entries_test,
                percent_in_groups_services_test,
                True,
                True
            ),
            tuple([
                "35% of shelter residents attend on-site groups or activities",
                "35%",
                "{} / {} = {}%".format(2, 10, 100 * (2 / 10))
            ])
        )
        self.assertEqual(
            len(mf().percent_low_barrier_in_groups(
                percent_in_groups_entries_test,
                percent_in_groups_services_test,
                True,
                False
            )),
            2
        )
        self.assertEqual(
            mf().percent_low_barrier_in_groups(
                percent_in_groups_entries_test,
                percent_in_groups_services_test,
                False,
                True
            ),
            tuple([
                "35% of shelter residents attend on-site groups or activities",
                "35%",
                "{} / {} = {}%".format(4, 10, 100 * (4 / 10))
            ])
        )
        self.assertEqual(
            len(mf().percent_low_barrier_in_groups(
                percent_in_groups_entries_test,
                percent_in_groups_services_test,
                False,
                False
            )),
            4
        )

    def test_percent_low_barrier_to_perm(self):
        """
        Pass - These methods are already tested elsewhere.  No further testing required.

        :return:
        """
        pass

    def test_percent_low_barrier_to_stable(self):
        """
        Pass - These methods are already tested elsewhere.  No further testing required.

        :return:
        """
        pass

    def test_percent_non_poc_exiting_to_perm(self):
        """

        :return:
        """
        percent_npoc_to_perm_ee_test = pd.read_excel(
            "testing_data\Percent Non POC Exiting to Perm EE Test.xlsx",
            sheet_name="Sheet1"
        )
        percent_npoc_to_perm_services_test = pd.read_excel(
            "testing_data\Percent Non POC Exiting to Perm Services Test.xlsx",
            sheet_name="Sheet1"
        )
        self.assertEqual(
            mf().percent_non_poc_exiting_to_perm_by_provider(
                percent_npoc_to_perm_ee_test,
                percent_npoc_to_perm_services_test,
                ["Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)"],
                True
            ),
            tuple([
                "Participants housed are at least 40% people of color",
                "40%",
                "{}/{} = {}%".format(1, 1, 100 * (1/ 1))
            ])
        )

    def test_percent_of_pt_w_home_visit_by_provider(self):
        """

        :return:
        """

        services_test = pd.read_excel("testing_data\pt_w_home_visits_services_test.xlsx", sheet_name="Sheet1")
        entries_test = pd.read_excel("testing_data\pt_w_home_visits_entries_test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_of_pt_w_home_visits_by_provider(services_test, entries_test, "SSVF"),
            tuple(["25% of participants will have quarterly home visits", "25%", "1 / 4 = 25.0%"])
        )

    def test_percent_placed_are_poc(self):
        """

        :return:
        """
        placements_test = pd.read_excel("testing_data\Percent Placed POC Placement Test.xlsx", sheet_name="Sheet1")
        services_test = pd.read_excel("testing_data\Percent Placed POC Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_placed_are_poc(placements_test, services_test),
            tuple(["Participants housed are at least 41% participants of color", "41%", "2/5 = 40.0%"])
        )

    def test_percent_poc_placed_by_provider(self):
        """

        :return:
        """
        placements_test = pd.read_excel("testing_data\Percent Placed POC Placement Test.xlsx", sheet_name="Sheet1")
        services_test = pd.read_excel("testing_data\Percent Placed POC Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_poc_placed_by_provider(placements_test, services_test, ["SSVF - TPI"]),
            tuple(["Veterans housed are at least 25% people of color", "25%", "1/2 = 50.0%"])
        )
        self.assertEqual(
            mf().percent_poc_placed_by_provider(placements_test, services_test, ["ACCESS"]),
            tuple(["Participants housed are at least 41% people of color", "41%", "1/3 = {}%".format(100*(1/3))])
        )

    def test_percent_poc_placed_vs_percent_white_placed_by_shelter(self):
        """
        If the script runs correctly but the test fails due to the tuple not asserting as equal then then numbers
        entered in the tuple are probably incorrect.  Recheck the data to make sure that the expected output is correct.
        :return:
        """

        entries_test = pd.read_excel("testing_data\POC vs White Placed by Shelter Entries.xlsx", sheet_name="Sheet1")
        services_test = pd.read_excel("testing_data\POC vs White Placed by Shelter Services.xlsx", sheet_name="Sheet1")

        self.assertEqual(
            mf().percent_poc_placed_vs_percent_white_placed_by_shelter(
                entries_test,
                services_test,
                "res"
            ),
            tuple([
                "Participants who are people of color that exit the program have housing outcomes greater than or equal to those of non-people of color",
                ">= 0%",
                "({}/{})-({}/{})={}".format(1, 2, 2, 4, ((1 / 2) - (2 / 4)))
            ])
        )

        self.assertEqual(
            mf().percent_poc_placed_vs_percent_white_placed_by_shelter(entries_test, services_test, "ACCESS"),
            tuple([
                    "Participants who are people of color that exit the program have housing outcomes greater than or equal to those of non-people of color",
                    ">= 0%",
                    "({}/{})-({}/{})={}".format(1, 2, 2, 4, ((1 / 2) - (2 / 4)))
            ])
        )

    def test_percent_poc_w_small_s_support_services_by_provider(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Percent POC w Small S Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_poc_w_small_s_support_services_by_provider(services_test, "Day"),
            tuple([
                "50% of people of color served by the Day Center access a supportive service",
                ">= 50%",
                "{}/{} = {}%".format(1, 2, 100*(1/2))
            ])
        )

    def test_percent_residents_oriented_in_ten_days(self):
        """

        :return:
        """
        entries_test = pd.read_excel("testing_data\Percent Residents Oriented Entries Test.xlsx", sheet_name="Sheet1")
        services_test = pd.read_excel("testing_data\Percent Residents Oriented Services Test.xlsx", sheet_name="Sheet1")

        self.assertEqual(
            mf().percent_residents_oriented_in_ten_days(
                entries_test, services_test,
                ["Transition Projects (TPI) - Clark Center - SP(25)"]
            ),
            tuple([
                "95% of participants will attend orientation within the first 10 days",
                ">= 95%",
                "{} / {} = {}".format(2, 4, 100 * (2 / 4))
            ])
        )

    def test_percent_shelter_stays_less_than_seven_days(self):
        """

        :return:
        """
        entries_test = pd.read_excel("testing_data\Percent Shelter Stay Short Entries Test.xlsx", sheet_names="Sheet1")
        self.assertEqual(
            mf().percent_shelter_stays_less_than_seven_days(
                entries_test,
                ["Transition Projects (TPI) - Clark Center - SP(25)"]
            ),
            tuple([
                "10% decrease in participants leaving prior to 7 days",
                "10%",
                "{} / {} = {}% <----- must subtract last quarters numbers from this".format(
                    1,
                    2,
                    100 * (1 / 2)
                )
            ])
        )

    def test_percent_to_destination_by_shelter(self):
        """

        :return:
        """
        entry_test = pd.read_excel("testing_data\Percent to Destination by Shelter Entries.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().percent_to_destination_by_shelter(entry_test, "Col", "perm"),
            tuple([
                "5% of participants will move from residential programs into permanent housing",
                "5%",
                "{}/{} = {}%".format(2, 6, 100 * (2 / 6))
            ])
        )
        self.assertEqual(
            mf().percent_to_destination_by_shelter(entry_test, "Col", "stable"),
            tuple([
                "15% of participants will move from residential programs into permanent housing",
                "15%",
                "{}/{} = {}%".format(2, 6, 100 * (2 / 6))
            ])
        )
        self.assertEqual(
            mf().percent_to_destination_by_shelter(entry_test, "res", "perm"),
            tuple([
                "35% of all participants in the residential programs will move into permanent housing",
                "35%",
                "{} / {} = {}".format(3, 10, 100 * (3 / 10))
            ])
        )
        self.assertEqual(
            mf().percent_to_destination_by_shelter(entry_test, "res", "temp"),
            tuple([
                "15% of all the participants in the residential programs will move into stable housing",
                "15%",
                "{} / {} = {}".format(3, 10, 100 * (3 / 10))
            ])
        )

    def test_poc_served(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\POC Served By Provider Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().poc_served(services_test),
            tuple([
                "Participants served are at least 41% participants of color ",
                "41%",
                "{}/{} = {}%".format(7, 10, 100 * (7 / 10))
            ])
        )

    def test_poc_served_by_provider(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\POC Served By Provider Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().poc_served_by_provider(services_test, "SOS"),
            tuple([
                "Participants 40% people of color",
                "40%",
                "{}/{} = {}%".format(5, 7, 100 * (5 / 7))
            ])
        )
        self.assertEqual(
            mf().poc_served_by_provider(services_test, "SSVF"),
            tuple([
                "Veterans served are at least 25% participants of color ",
                "25%",
                "{}/{} = {}%".format(2, 3, 100 * (2 / 3))
            ])
        )

    def test_received_application_readiness_assistance(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Recieved Application Readiness Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().received_application_readiness_assistance(services_test),
            tuple([
                "300 participants will receive application readiness assistance (identification, birth certificates, debt reduction, etc.)",
                300,
                3
            ])
        )

    def test_referral_to_best_by_provider(self):
        """

        :return:
        """
        services_test = pd.read_excel(askopenfilename(title="referrals to best"), sheet_name="Sheet1")
        self.assertEqual(
            mf().referral_to_best_by_provider(services_test, "Residential"),
            tuple([
                "300 to employment or benefits advocacy", 300, 1
            ])
        )
        self.assertEqual(
            mf().referral_to_best_by_provider(services_test, "Retention"),
            tuple([
                "50% to employment or benefits advocacy",
                "50%",
                "{}/{} = {}%".format(1, 2, 100*(1/2))
            ])
        )
        self.assertEqual(
            mf().referral_to_best_by_provider(services_test, "ACCESS"),
            tuple([
                "200 to benefits advocacy", 200, 1
            ])
        )
        self.assertEqual(
            mf().referral_to_best_by_provider(services_test, "SSVF"),
            tuple([
                "200 to employment or benefits advocacy", 200, 1
            ])
        )

    def test_referral_to_rw_by_provider(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Referral to RW Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().referral_to_rw_by_provider(services_test, "Residential"),
            tuple([
                "100 to RentWell", 100, 1
            ])
        )
        self.assertEqual(
            mf().referral_to_rw_by_provider(services_test, "Retention"),
            tuple([
                "10% to RentWell",
                "10%",
                "{}/{} = {}".format(1, 2, 100*(1/2))
            ])
        )
        self.assertEqual(
            mf().referral_to_rw_by_provider(services_test, "ACCESS"),
            tuple([
                "65 to RentWell", 65, 1
            ])
        )
        self.assertEqual(
            mf().referral_to_rw_by_provider(services_test, "SSVF"),
            tuple([
                "150 to RentWell", 150, 1
            ])
        )

    def test_referral_to_ss_by_provider(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Referral to SS Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().referral_to_ss_by_provider(services_test, "Col"),
            tuple([
                "10% of participants will be connected to Supportive Services",
                "10%",
                "{}/{} = {}".format(1, 2, 100 * (1 / 2))

            ])
        )
        self.assertEqual(
            mf().referral_to_ss_by_provider(services_test, "Residential"),
            tuple([
                "50% of participants will be referred to Supportive Services, including:",
                "50%",
                "{}/{} = {}%".format(1, 2, 100 * (1 / 2))

            ])
        )

    def test_referral_to_sud_treatment_during_iap(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Referral to SUD Treatment Services Test.xlsx", sheet_name="Sheet1")
        entries_test = pd.read_excel("testing_data\Referral to SUD Treatment Entries Test.xlsx", sheet_name="Sheet1")

        self.assertEqual(
            mf().referral_to_sud_treatment_during_iap(entries_test, services_test),
            tuple(["600 engagements and linkages to treatment through IAP", 600, 2])
        )

    def test_res_to_perm_percent(self):
        entries_test = pd.read_excel("testing_data\Res to Perm Entries Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().res_to_perm_percent(entries_test, "perm"),
            tuple([
                "35% of participants will move from residential programs into permanent housing",
                "35%",
                "{}/{} = {}".format(3, 8, 100 * (3 / 8))
            ])
        )
        self.assertEqual(
            mf().res_to_perm_percent(entries_test, "temp"),
            tuple([
                "15% of participants will move from residential programs to stable housing",
                "15%",
                "{}/{} = {}".format(3, 8, 100 * (3 / 8))
            ])
        )

    def test_return_poc_list(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Return POC List Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            len(mf().return_poc_list(services_test)),
            6
        )

    def test_served_by_day_center(self):
        services_test = pd.read_excel("testing_data\Small S Support Services Test.xlsx")
        self.assertEqual(
            mf().served_by_day_center(services_test),
            tuple(["7,000 participants will access day center", 7000, 2])
        )

    def test_small_s_support_services(self):
        """

        :return:
        """
        services_test = pd.read_excel("testing_data\Small S Support Services Test.xlsx", sheet_name="Sheet1")
        self.assertEqual(
            mf().small_s_support_services(services_test),
            tuple([
                "50% of participants will be connected to supportive services ",
                "50%",
                "{}/{} = {}%".format(1, 3, 1 / 3)
            ])
        )


if __name__ == "__main__":
    unittest.main()
