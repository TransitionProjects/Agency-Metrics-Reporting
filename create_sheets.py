__author__ = "David Katz-Wigmore"
__version__ = ".1"

import pandas as pd
from all_functions import MetricsFunctions


class DepartmentMetric:
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        self.original_services = pd.read_excel(services_file, sheet_name="Service Data")
        self.original_entries = pd.read_excel(entries_file, sheet_name="Report 1")
        self.original_placements = pd.read_excel(placements_file, sheet_name="Placement Data")
        self.original_followups = pd.read_excel(followups_file, sheet_name="Report 1")
        self.output = []

    def print_all(self):
        print(pd.DataFrame(self.output, columns=["Question", "Goal", "Metric"]))

    def return_output(self):
        return pd.DataFrame(self.output, columns=["Question", "Goal", "Metric"])


class Agency(DepartmentMetric):
    def __init__(self, wait_list_file, services_file, entries_file, placements_file, followups_file):
        super(Agency, self).__init__(services_file, entries_file, placements_file, followups_file)
        self.original_wait_list = pd.read_csv(
            wait_list_file,
            delimiter=","
        ).dropna(axis=0, how="any", subset=["Waitlist Name"])

    def process(self):
        af = MetricsFunctions()
        h_perm, h_temp, h_exits = af.exit_destination_by_provider(self.original_entries, "Hansen", "perm temp")
        col_perm, col_temp, col_exits = af.exit_destination_by_provider(self.original_entries, "Columbia", "perm temp")
        sos_perm, sos_temp, sos_exits = af.exit_destination_by_provider(self.original_entries, "SOS", "perm temp")
        wil_perm, wil_temp, wil_exits = af.exit_destination_by_provider(self.original_entries, "Willamette", "perm temp")
        fif_perm, fif_temp, fif_exits = af.exit_destination_by_provider(self.original_entries, "5th", "perm temp")
        cc_perm, cc_temp, cc_exits = af.exit_destination_by_provider(self.original_entries, "Clark Center", "perm temp")
        jp_perm, jp_temp, jp_exits = af.exit_destination_by_provider(self.original_entries, "Jean's", "perm temp")
        dp_perm, dp_temp, dp_exits = af.exit_destination_by_provider(self.original_entries, "Doreen's", "perm temp")
        es_to_perm = (
            len(h_perm.index) + len(col_perm.index) + len(sos_perm.index) + len(wil_perm.index) + len(fif_perm.index)
        )
        es_to_any = (
            len(h_exits.index) + len(col_exits.index) + len(sos_exits.index) + len(wil_exits.index) + len(fif_exits.index)
        )
        res_to_perm = (
            len(cc_perm.index) + len(jp_perm.index) + len(dp_perm.index)
        )
        res_to_any = (
            len(cc_exits.index) + len(jp_exits.index) + len(dp_exits.index)
        )

        self.output = [
            ("184,200 shelter bed nights", 184200, ""),
            af.count_hygiene_services_by_provider(self.original_services, provider="Agency"),
            af.served_by_day_center(self.original_services),
            af.count_shelter_stays(self.original_entries),
            af.small_s_support_services(self.original_services),
            af.count_ongoing_cm_services(self.original_services),
            af.received_application_readiness_assistance(self.original_services),
            af.count_rent_assist(self.original_services),
            af.count_rent_well(self.original_services, "attendence"),
            ("600 participants will access employment services ", 600, ""),
            af.count_all_pp(self.original_placements),
            ("15% of participants will increase their incomes ****", "15%", ""),
            af.count_rent_well(self.original_services, "Graduation"),
            ("300 participants will obtain employment ", 300, ""),
            af.count_provider(self.original_entries, "Ret", 400),
            af.count_rent_well(self.original_services, "attendence"),
            ("600 participants will access employment services ", 600, ""),
            af.count_retention_by_length(self.original_followups, 12, "agency"),
            ("15% of participants will increase their incomes ****", "15%", ""),
            af.count_rent_well(self.original_services, "Graduation"),
            af.count_all_ep(self.original_placements),
            ("Equity Committee will adopt and report on measurable equity goals", "Complete", ""),
            af.poc_served(self.original_services),
            af.percent_placed_are_poc(self.original_placements, self.original_services),
            (
                "Participants of color that are housed will have outcomes greater than or equal to those of white participants (percent of people housed)",
                ">0%",
                ""
             ),
            ("At least 41% of staff will come from communities of color", "41%", ""),
            ("Board of Directors will be at least 33% people of color", "33%", ""),
            ("Agency supports Yes to Affordable Homes initiative", "Completed", ""),
            ("Staff participate in A Home for Everyone", "Completed", ""),
            ("Programs contribute articles and success stories", "Completed", ""),
            ("Publish a homeless snapshot", "Completed", ""),
            ("A Home For Everyone meets or exceeds its goals", "Completed", ""),
            ("# of people in point-in-time count", "", 4177),
            ("Percent of people experiencing homelessness sheltered in Portland", "", "1668/4177 = 39.93%"),
            ("# of people who die on the streets in Multnomah County annually", "", ""),
            af.average_los_in_es_shelter(self.original_entries),
            ("Cost per emergency shelter bed night", "", ""),
            ("Cost per residential program bed night", "", ""),
            af.calculate_average_wait_list_length(self.original_wait_list, waitlist="Men"),
            af.calculate_average_wait_list_length(self.original_wait_list, waitlist="Women"),
            (
                "Percent of residents housed from emergency shelter", "",
                "{}/{} = {}%".format(es_to_perm, es_to_any, 100 * (int(es_to_perm)/int(es_to_any)))
            ),
            (
                "Percent of residents permanently housed from residential programs", "",
                "{}/{} = {}%".format(res_to_perm, res_to_any, 100 * (int(res_to_perm) / int(res_to_any)))
            ),
            af.average_los_in_res_shelter(self.original_entries, cleaned=False),
            (),

            af.count_retention_by_length(self.original_followups, 12)
        ]
        return pd.DataFrame.from_records(self.output)


class ResidentialCM(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(ResidentialCM, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.count_entries_by_provider(self.original_entries, "Residential"),
            af.count_ongoing_cm_services_by_department(self.original_services, "Residential"),
            af.referral_to_ss_by_provider(self.original_services, "Residential"),
            af.referral_to_rw_by_provider(self.original_services, "Residential"),
            af.referral_to_best_by_provider(self.original_services, "Residential"),
            af.res_to_perm_percent(self.original_entries, "perm"),
            (
                "120 from Doreen's Place",
                120,
                af.exit_destination_by_provider(self.original_entries, "Doreen's", "count perm")
            ),
            (
                "120 from Clark Center",
                120,
                af.exit_destination_by_provider(self.original_entries, "Clark Center", "count perm")
            ),
            (
                "90 from Jean's Place",
                90,
                af.exit_destination_by_provider(self.original_entries, "Jean's", "count perm")
            ),
            af.res_to_perm_percent(self.original_entries, "temp"),
            (
                "60 from Doreen's Place",
                60,
                af.exit_destination_by_provider(self.original_entries, "Doreen's", "count temp")
            ),
            (
                "60 from Clark Center",
                60,
                af.exit_destination_by_provider(self.original_entries, "Clark Center", "count temp")
            ),
            (
                "40 from Jean's Place",
                40,
                af.exit_destination_by_provider(self.original_entries, "Jean's", "count temp")
            ),
            af.days_from_id_to_placement(
                self.original_placements,
                self.original_entries,
                "Residential",
                ["Residential CM"]
            ),
            af.count_retention_by_length(self.original_followups, 12, "residential"),
            ("Conduct outreach to 6 culturally specific organizations annually", 6, ""),
            ("Translate intake and grant documents into Spanish", "", ""),
            af.percent_poc_placed_by_provider(self.original_placements, self.original_services, ["Residential CM"]),
            (
                "Housing Retention Rates for people of color are equal to or greater than rates for non-people of color",
                ">=0%",
                ""
            ),
            ("Outreach to 2 new landlords per quarter for improved access to housing", 2, ""),
            ("2 agreements with landlords for first night of refusal for open units", 2, ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class RetentionCM(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(RetentionCM, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.referral_to_ss_by_provider(self.original_services, "Retention"),
            af.referral_to_rw_by_provider(self.original_services, "Retention"),
            af.referral_to_best_by_provider(self.original_services, "Retention"),
            af.count_retention_by_length(self.original_followups, 12, "Retention"),
            ("25% of participants will move from permanent housing to subsidized housing", "25%", ""),
            ("20% of participants will increase their incomes during the year", "20%", ""),
            (
                "Each case manager will attend 2 trainings or events annually pertaining to services for, or working with communities of color",
                2,
                ""
            ),
            (
                "Housing retention rates for people of color are equal to or greater than rates for non-people of color",
                " >=0%",
                ""
            ),
            ("Landlord relationships resulting in first right of refusal for open units", "", ""),
            ("Participation in COmmunity Alliance of Tenants", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class OutreachCM(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(OutreachCM, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.count_entries_by_provider(self.original_entries, "ACCESS"),
            af.count_ongoing_cm_services_by_department(self.original_services, "ACCESS"),
            af.referral_to_ss_by_provider(self.original_services, "ACCESS"),
            af.referral_to_rw_by_provider(self.original_services, "ACCESS"),
            af.referral_to_best_by_provider(self.original_services, "ACCESS"),
            af.count_perm_by_provider(self.original_placements, ["ACCESS"]),
            af.days_from_id_to_placement(self.original_placements, self.original_entries, "ACCESS", ["ACCESS"]),
            af.count_retention_by_length(self.original_followups, 12, "ACCESS"),
            ("Conduct outreach to 6 culturally specific organizations annually", 6, ""),
            ("Translate intake and grant documents into Spanish", "", ""),
            af.percent_poc_placed_by_provider(self.original_placements, self.original_services, ["ACCESS"]),
            (
                "Housing retention rates for people of color are equal to or greater than rates for non-people of color",
                ">0%",
                ""
            ),
            ("Outreach to 2 new landlords per quarter for improved access to housing", 2, ""),
            ("2 agreements with landlords for the first night of refusal for open units", 2, ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]

        return pd.DataFrame.from_records(self.output)


class SSVF(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file, entry_hh_file):
        super(SSVF, self).__init__(services_file, entries_file, placements_file, followups_file)
        self.original_entries_screenings = pd.read_excel(entry_hh_file, sheet_name="Report 1")

    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.count_households_screened(self.original_entries_screenings),
            af.count_ongoing_cm_services_by_department(self.original_services, "SSVF"),
            af.referral_to_ss_by_provider(self.original_services, "SSVF"),
            af.referral_to_rw_by_provider(self.original_services, "SSVF"),
            af.referral_to_best_by_provider(self.original_services, "SSVF"),
            af.count_perm_by_provider(self.original_placements, ["SSVF - TPI"]),
            af.count_ep_by_provider(self.original_placements, ["SSVF - TPI"]),
            ("75 veteran families participants will increase their incomes during the year", 75, ""),
            af.count_legal_barriers_mitigated(self.original_entries, self.original_services, "SSVF"),
            af.percent_of_pt_w_home_visits_by_provider(self.original_services, self.original_entries, "SSVF"),
            ("98% of participants will remain in housing 3 months after entering housing", "98%", ""),
            ("95% of participants will remain in housing 6 months after entering housing", "95%", ""),
            ("90% of participants will remain in housing 12 months after entering housing", "90%", ""),
            af.count_retention_by_length(self.original_followups, 12, "SSVF"),
            ("20% of participants will move from permanent housing to subsidized housing", "20%", ""),
            ("Conduct outreach to 6 culturally-specific providers annually", 6, ""),
            af.poc_served_by_provider(self.original_services, "SSVF"),
            af.percent_poc_placed_by_provider(self.original_placements, self.original_services, ["SSVF - TPI"]),
            (
                "Housing retention rates for people of color are equal to or greater than rates for non-people of color",
                ">=0%",
                ""
            ),
            ("Organize annual veterans stand down", "Complete", "Complete"),
            ("400 veterans attend stand down and are connected to services", 400, ""),
            ("Fewer than 5% HMIS entry/exiit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields are entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class DayCenter(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file, exclusions_file):
        super(DayCenter, self).__init__(services_file, entries_file, placements_file, followups_file)
        self.original_exclusions = pd.read_excel(exclusions_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.count_mailing_services_by_day_center(self.original_services),
            af.count_hygiene_services_by_provider(self.original_services, provider="Day Center"),
            ("2100 Clinic visits", 2100, ""),
            af.count_id_assistance_by_provider(self.original_services, provider="Day Center"),
            af.count_transportation_passes_by_provider(self.original_services),
            ("Provide a safe and orderly service environment", "", ""),
            af.count_services_by_provider(self.original_services, "Day Center"),
            af.count_served_by_provider(self.original_services, "Day Center"),
            af.small_s_support_services(
                self.original_services[self.original_services["Service Provide Provider"].str.contains("Day Center")]
            ),
            af.count_exclusions_by_provider(self.original_exclusions, "Day Center"),
            ("45% of Day Center FT/PT staff are people of color", "", ""),
            af.poc_served_by_provider(self.original_services, "Day"),
            af.percent_poc_w_small_s_support_services_by_provider(self.original_services, "Day Center"),
            ("Reach out to 3 new community partners", 3, ""),
            ("Produce newsletter articles reflecting participant experiences and needs", "", ""),
            ("10 community partners offer services in the day center", 10, ""),
            ("3 articles written informing the community about the day center service environment", 3, ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "< 5%", ""),
            ("Fewer than 5% of services fields are entered incorrectly", "< 5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Housing(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Housing, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("90% occupancy at the Clark Annex", "90%", ""),
            ("94% occupancy at the Barbara Maher", "94%", ""),
            af.referral_to_ss_by_provider(self.original_services, "Clark Annex"),
            af.referral_to_ss_by_provider(self.original_services, "Barbara"),
            af.referral_to_rw_by_provider(self.original_services, "Clark Annex"),
            af.referral_to_rw_by_provider(self.original_services, "Barbara"),
            af.referral_to_best_by_provider(self.original_services, "Clark Annex"),
            af.referral_to_best_by_provider(self.original_services, "Barbara"),
            ("85% of veteran residents exit the Grant & Per Diem program into stable housing", "85%", ""),
            ("70% of corrections residents exitt to stable housing", "70%", ""),
            (
                "80% of residents that exit the Barbara Maher will exit into permanent housing",
                "80%",
                af.exit_destination_by_provider(self.original_entries, "Barbara", "percent perm")
            ),
            ("Staff are trained in Equity and Inclusion, a training offered monthly through the T.P.I.", "", ""),
            af.percent_poc_exiting_to_perm_by_provider(self.original_entries, self.original_services),
            (
                "Housing retention rates for people of color are equal to or greater than ratres for non-people of color",
                ">= 0%",
                ""
             ),
            (
                "Participants who are people of color that exit the program have housing outcomes greater than or equal to those of non-people of color",
                ">= 0%",
                ""
            ),
            ("Update and adhere to Affirmative Fair Housing Marketing Plan", "", "")
        ]
        return pd.DataFrame.from_records(self.output)


class DPCCJP(DepartmentMetric):
    def __init__(self, services_file, entries_file, entries_plus_reason_file, placements_file, followups_file):
        super(DPCCJP, self).__init__(services_file, entries_file, placements_file, followups_file)
        self.original_entries_plus_reason = pd.read_excel(entries_plus_reason_file, sheet_name="Report 1")

    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("32,193 bed nights annually at the Clark Center", 32193, ""),
            ("32,193 bed nights annually at Doreen's Place", 32193, ""),
            ("19,674 bed nights annually at Jean's Place", 19674, ""),
            af.count_shelter_stays(self.original_entries, agency=False),
            af.percent_exits_caused_by_exclusion(self.original_entries_plus_reason, shelter_type="Res"),
            af.count_entries_by_provider(self.original_entries, "Clark Center"),
            af.count_entries_by_provider(self.original_entries, "Doreen's"),
            af.count_entries_by_provider(self.original_entries, "Jean's Place"),
            ("Program orientation will be offered at a minimum of 3 times per week", "", ""),
            af.percent_to_destination_by_shelter(self.original_entries, "Res", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "Res", "temp"),
            af.percent_shelter_stays_less_than_seven_days(self.original_entries, providers=[
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
            ]),
            af.percent_residents_oriented_in_ten_days(self.original_entries, self.original_services, providers=[
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
            ]),
            ("Staff will attend 1 equity training quarterly", "", ""),
            ("41% staff are people of color", "41%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "res"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                "res"
            ),
            ("Fill 10 guest beds per month", "10", ""),
            ("30% of guest beds exit into permanent housing", "30%", "Uncountable"),
            ("Fewer than 5% HMIS entry/exit fields empty", "< 5%", ""),
            ("DP", "< 5%", ""),
            ("CC", "< 5%", ""),
            ("JP", "< 5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "< 5%", ""),
            ("DP", "< 5%", ""),
            ("CC", "< 5%", ""),
            ("JP", "< 5%", "")
        ]

        return pd.DataFrame.from_records(self.output)


class Columbia(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Columbia, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("26353 bed nights annually", 26353, ""),
            af.count_entries_by_provider(self.original_entries, provider=["col", "h", "sos", "wc"]),
            af.count_entries_by_provider(self.original_entries, "Columbia"),
            af.referral_to_ss_by_provider(self.original_services, "Columbia"),
            af.percent_to_destination_by_shelter(self.original_entries, "Columbia", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "Columbia", "stable"),
            af.count_retention_by_length(self.original_followups, 12, "Columbia"),
            ("Outreach to 4 culturally specific programs annually", 4, ""),
            ("40% of staff are people of color", "40%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "Columbia"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                ["Transition Projects (TPI) - Columbia Shelter(5857)"]
            ),
            ("Participate in domestic violence continuum of services", "", ""),
            ("Participate in veterans continuum of care", "", ""),
            ("Participants have better access to services", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class WillametteCenter(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(WillametteCenter, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("41610 bed nights annually", 41610, ""),
            af.count_entries_by_provider(self.original_entries, provider=["col", "h", "sos", "wc"]),
            af.count_entries_by_provider(self.original_entries, "Wil"),
            af.referral_to_ss_by_provider(self.original_services, "Wil"),
            af.percent_to_destination_by_shelter(self.original_entries, "Wil", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "Wil", "stable"),
            af.count_retention_by_length(self.original_followups, 12, provider="Wil"),
            ("Outreach to 4 culturally specific programs annually", 4, ""),
            ("40% of staff are people of color", "40%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "Willamette"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                ["Transition Projects (TPI) - Willamette Center(5764)"]
            ),
            ("Participate in domestic violence continuum of services", "", ""),
            ("Participate in veterans continuum of care", "", ""),
            ("Participants have better access to services", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Hansen(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Hansen, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("69350 bed nights annually", 69350, ""),
            af.count_entries_by_provider(self.original_entries, provider=["col", "h", "sos", "wc"]),
            af.count_entries_by_provider(self.original_entries, "Han"),
            af.referral_to_ss_by_provider(self.original_services, "Hans"),
            af.percent_to_destination_by_shelter(self.original_entries, "Hans", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "Hans", "stable"),
            af.count_retention_by_length(self.original_followups, 12, "Hansen"),
            ("Outreach to 4 culturally specific programs annually", 4, ""),
            ("40% of staff are people of color", "40%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "Hansen"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                ["Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)"]
            ),
            ("Participate in domestic violence continuum of services", "", ""),
            ("Participate in veterans continuum of care", "", ""),
            ("Participants have better access to services", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class SoS(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(SoS, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("24272 bed nights annually", 24272, ""),
            af.count_entries_by_provider(self.original_entries, provider=["col", "h", "sos", "wc"]),
            af.count_entries_by_provider(self.original_entries, "SOS"),
            af.referral_to_ss_by_provider(self.original_services, "SOS"),
            af.percent_to_destination_by_shelter(self.original_entries, "SOS", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "SOS", "stable"),
            af.count_retention_by_length(self.original_followups, 12, "SOS"),
            ("Outreach to 4 culturally specific programs annually", 4, ""),
            ("40% of staff are people of color", "40%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "SOS"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                ["Transition Projects (TPI) - SOS Shelter(2712)"]
            ),
            ("Participate in domestic violence continuum of services", "", ""),
            ("Participate in veterans continuum of care", "", ""),
            ("Participants have better access to services", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Fifth(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Fifth, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            ("XXXXX bed nights annually", "", ""),
            af.count_entries_by_provider(self.original_entries, provider=["col", "h", "sos", "wc"]),
            af.count_entries_by_provider(self.original_entries, "5th"),
            af.referral_to_ss_by_provider(self.original_services, "5th"),
            af.percent_to_destination_by_shelter(self.original_entries, "5th", "perm"),
            af.percent_to_destination_by_shelter(self.original_entries, "5th", "stable"),
            # uncomment the row below and remove
            # af.count_retention_by_length(self.original_followups, 12, "5th"),
            ("12 Mo Post Subsidy Retention Data", "N/A", "Impossible until Q1 2018-2019"),
            ("Outreach to 4 culturally specific programs annually", 4, ""),
            ("40% of staff are people of color", "40%", ""),
            af.poc_utilizing_shelter_by_provider(self.original_entries, self.original_services, "5th"),
            af.percent_poc_placed_vs_percent_white_placed_by_shelter(
                self.original_entries,
                self.original_services,
                ["Transition Projects (TPI) - 5th Avenue Shelter(6281)"]
            ),
            ("Participate in domestic violence continuum of services", "", ""),
            ("Participate in veterans continuum of care", "", ""),
            ("Participants have better access to services", "", ""),
            ("Fewer than 5% HMIS entry/exit fields empty", "<5%", ""),
            ("Fewer than 5% of services fields entered incorrectly", "<5%", "")
        ]
        return pd.DataFrame.from_records(self.output)


class SevereWeather(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(SevereWeather, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        self.output = [
            ("2000 bed nights", 2000, ""),
            ("Up to 200 people have a safe place to sleep each night", 200, ""),
            ("Staff are have attended an Equity and Inclusion training", "", ""),
            ("Outreach to ensure communities of color know about severe weather options", "", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Mentor(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Mentor, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        self.output = [
            ("Mentors provide 4000 hours of peer support to internal programs", 4000, ""),
            ("Mentors provide co-facilitation to 400 groups", 400, ""),
            ("At least 1000 participants will have contact with a mentor", 1000, ""),
            ("Peer support specialist training provided to 45 formerly homeless individuals per year", 45, ""),
            ("90% of graduates retain housing one year post-graduation", "90%", ""),
            ("85% of mentors graduate with a peer support specialist certificate", "85%", ""),
            ("55% of mentors graduate with a peer support specialist certificate", "55%", ""),
            ("50% of graduates retain employment 6 monts post-hire", "50%", ""),
            ("50% of graduates retain employment post-graduation", "50%", ""),
            ("Recruit 18 mentors per year that identify as people of color", 18, ""),
            ("At least 41% of mentor graduates per year are people of color", "41%", ""),
            ("At least 20% of agency staff will have lived homeless experience", "20%", ""),
            ("Mentor graduates provide agency and homeless education and awareness at 10 events per year", 10, ""),
            ("Mentors participate in peer advisory committee", "", ""),
            ("Community awareness of homeless issues and agency impact", "", ""),
            ("Peer Advisory committee adds participant input to our agency board of directors through quarterly meetings", "", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Advocacy(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Advocacy, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        self.output = [
            ("We will support the passage of Mortgage Interest Dedcution Reform in Oregon ", "", ""),
            ("A Home for Everyone will meet or exceed its goals", "", ""),
            ("We will launch a campaign to increase housing placements from low barrier shelter", "", "")
        ]
        return pd.DataFrame.from_records(self.output)


class Equity(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(Equity, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.poc_served(self.original_services),
            af.percent_placed_are_poc(self.original_placements, self.original_services),
            (
                "Participants of color that are housed will have outcomes greater than or equal to those of white participants (percent of people housed)",
                ">0%",
                ""
            ),
            (
                "Maintain greater than 41% people of color representation on staff",
                "41%",
                ""
            )
        ]
        return pd.DataFrame.from_records(self.output)


class RentWell(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(RentWell, self).__init__(services_file, entries_file, placements_file, followups_file)

    def process(self):
        self.output = [
            ("400 enrolled TPI participants", 400, ""),
            ("Standardized enrolement guidelines for TPI Case Managers", "", ""),
            ("Enrolled Participants will have support outside the classroom", "", ""),
            ("200 participants will graduate from TPI's RentWell classes", "", ""),
            ("Conduct 4 trainings for Multnomah County case managers", 4, ""),
            ("Conduct 4 trainings for Multnomah County instructors", 4, ""),
            ("Create standardized data recording guidelines for Multnomah Country partner agencies", "", ""),
            ("Hold 4 listening sessions for providers", 4, ""),
            (
                "75% of Multnomah County providers will adopt a data recording structure by the end of the year",
                "75%",
                ""
            ),
            ("35% of FY 17-18 graduates of ")
        ]
        return pd.DataFrame.from_records(self.output)


class CoordinatedAccess(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(CoordinatedAccess, self).__init__(services_file, entries_file, placements_file, followups_file)


    def process(self):
        af = MetricsFunctions()
        self.output = [
            (),
            (),
            (),
            af.count_pts_with_barrier_mitigation_and_doc_prep(self.original_services, provider="(CHAT)"),
            (),
            (
                "Outreach to 10 culturally specific organizations that we have no previous connection to",
                10,
                ""
            )
        ]
        return pd.DataFrame.from_records(self.output)


class WellnessAccess(DepartmentMetric):
    def __init__(self, services_file, entries_file, entries_plus_reason_file, placements_file, followups_file):
        super(WellnessAccess, self).__init__(services_file, entries_file, placements_file, followups_file)
        self.original_needs = pd.read_excel(services_file, sheet_name="Need Data")
        self.original_entries_plus_reason = pd.read_excel(entries_plus_reason_file, sheet_name="Report 1")

    def process(self):
        af = MetricsFunctions()
        self.output = [
            af.count_referrals_resulting_in_connections(
                self.original_services,
                self.original_needs,
                "Wellness",
                ["Referral - Eye Care", "Referral - Dental Care", "Referral - Medical Care"],
                "med count"
            ),
            af.count_latinos_served_by_provider(self.original_services),
            af.count_referrals_resulting_in_connections(
                self.original_services,
                self.original_needs,
                "Wellness",
                [
                    "Referral - A&D Support",
                    "Referral - DV Support",
                    "Referral - Mental Health Care",
                    "Referral - MH Support"
                ],
                "mh sud count"
            ),
            af.count_referrals_resulting_in_connections(
                self.original_services,
                self.original_needs,
                "Wellness",
                ["Referral - Eye Care", "Referral - Dental Care", "Referral - Medical Care"],
                "percent med"
            ),
            af.count_referrals_resulting_in_connections(
                self.original_services,
                self.original_needs,
                "Wellness",
                [
                    "Referral - A&D Support",
                    "Referral - DV Support",
                    "Referral - Mental Health Care",
                    "Referral - MH Support"
                ],
                "percent mh sud"
            ),
            af.referral_to_sud_treatment_during_iap(self.original_entries, self.original_services),
            ("Create education groups for mental health and addictions", "", ""),
            ("Support groups for SUD recovery, PTSD, and mental health", "", ""),
            af.percent_iap_successful(self.original_entries_plus_reason),
            (
                "Participants who engage in Wellness Access groups have higher placement rate in housing",
                "",
                ""
            ),
            (
                "Decrease in exits from residential programs due to SUD violations",
                "<= 0%",
                ""
            ),
            ("Café Y Pan Group", "", ""),
            ("Connection to culturally -specific community partners", "", ""),
            ("Education and support groups to create connection to services and community support", "", ""),
            ("Education and support groups to create connection to services and community support", "", ""),
            ("Referral to Mentor Program for training and employment opportunities for participants", "", ""),
            af.poc_served_by_provider(self.original_services, "Wellness"),
            ("At least 40% of staff will come from communities of color", "40%", ""),
            ("HADIN meetings will occur once per week", "", ""),
            ("Outreach will occur to mental health, SUD, or health providers", "", ""),
            ("Increased access to services for participants", "", "")
        ]
        return pd.DataFrame.from_records(self.output)


class StrategicInitiative(DepartmentMetric):
    def __init__(self, services_file, entries_file, placements_file, followups_file):
        super(StrategicInitiative, self).__init__(services_file, entries_file, placements_file, followups_file)
    def process(self):
        af = MetricsFunctions()
        self.output = [
            tuple([
                "20% of Hansen participants exit to permanent housing",
                "20%",
                af.exit_destination_by_provider(self.original_entries, "Hansen", "percent perm")
            ]),
            tuple([
                "20% of Hansen participants exit to stable housing",
                "20%",
                af.exit_destination_by_provider(self.original_entries, "Hansen", "percent temp")
            ]),
            af.percent_exits_from_low_barrier_to_service_intensive(self.original_entries, "Hansen"),
            af.percent_low_barrier_to_perm(self.original_entries),
            af.percent_low_barrier_to_stable(self.original_entries),
            af.percent_low_barrier_in_groups(self.original_entries, self.original_services),
            af.count_shelter_to_perm_w_group(self.original_entries, self.original_services, True),
            af.count_shelter_to_perm_w_group(self.original_entries, self.original_services, False),
            af.percent_placed_are_poc(self.original_placements, self.original_services)
        ]

        return pd.DataFrame.from_records(self.output, columns=["Metric", "Goal", "Quarter Result"])

"""
if __name__ == "__main__":

    # uncomment this to run semi-quarterly strategic initiative numbers for Matt

    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfilename
    import pandas as pd

    services = askopenfilename(title="Services")
    entries = askopenfilename(title="Entries")
    placements = askopenfilename(title="Placements")
    followups = askopenfilename(title="Follow-ups")

    a = StrategicInitiative(services, entries, placements, followups)
    data = a.process()
    writer = pd.ExcelWriter(asksaveasfilename(title="StrategicInitiative Save As"), engine="xlsxwriter")
    data.to_excel(writer, sheet_name="Strategic Initiative")
    writer.save()
"""

"""
    # uncomment this to run the wellness access numbers for sanjay to keep him up to date on his team

    from tkinter.filedialog import askopenfilename
    from tkinter.filedialog import asksaveasfilename
    import pandas as pd

    services = askopenfilename(title="Services Plus Needs")
    entries = askopenfilename(title="Entries")
    entries_plus = askopenfilename(title="Entries Plus Reason")
    placements = askopenfilename(title="Placements")
    followups = askopenfilename(title="Follow-ups")

    a = WellnessAccess(services, entries, entries_plus, placements, followups)
    data = a.process()
    writer = pd.ExcelWriter(asksaveasfilename(title="StrategicInitiative Save As"), engine="xlsxwriter")
    data.to_excel(writer, sheet_name="Wellness Access")
    writer.save()
"""