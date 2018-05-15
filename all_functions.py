__author__ = "David Katz-Wigmore"
__version__ = ".1"

import pandas as pd
import numpy as np

from datetime import datetime
from dateutil.relativedelta import relativedelta


class MetricsFunctions:
    def average_los_in_es_shelter(self, entries_df, cleaned=False):
        """
        Used For:

        :param entries_df:
        :return:
        """
        stays = entries_df[
            (
                entries_df["Entry Exit Provider Id"].str.contains("Hansen") |
                entries_df["Entry Exit Provider Id"].str.contains("Columbia") |
                entries_df["Entry Exit Provider Id"].str.contains("Willamette") |
                entries_df["Entry Exit Provider Id"].str.contains("SOS") |
                entries_df["Entry Exit Provider Id"].str.contains("5th")
            )
        ]
        stays["Entry Date"] = pd.to_datetime(stays["Entry Exit Entry Date"]).dt.date
        stays["Exit Date"] = pd.to_datetime(stays["Entry Exit Exit Date"]).dt.date
        stays["Exit Date"].fillna(value=datetime(year=2017, month=9, day=30, hour=23, minute=59, second=59))
        stays["LOS"] = (stays["Exit Date"] - stays["Entry Date"]).dt.days
        filtered_stays = stays[["Client Uid", "Entry Date", "Exit Date", "LOS"]]
        total_days = filtered_stays["LOS"].sum()
        total_stays = len(filtered_stays.index)
        un_cleaned_mean = filtered_stays["LOS"].mean()
        cleaned_los_data = filtered_stays[
            np.abs(filtered_stays.LOS - filtered_stays.LOS.mean()) <= (3 * filtered_stays.LOS.std(ddof=0))
        ]
        cleaned_mean = cleaned_los_data.mean()
        if cleaned:
            return tuple(["Length of stay per emergency shelter resident (days)", "", cleaned_mean])
        else:
            return tuple(["Length of stay per emergency shelter resident (days)", "", un_cleaned_mean])

    def average_los_in_res_shelter(self, entries_df, cleaned=False):
        """
        Used For: Agency

        :param entries_df: data frame of all entries report
        :param cleaned: if cleaned == True method will return the mean excluding outliers, which are defined as 3
        standard deviations from the norm
        :return:
        """
        stays = entries_df[
            (
                entries_df["Entry Exit Provider Id"].str.contains("Doreen's") |
                entries_df["Entry Exit Provider Id"].str.contains("Clark Center") |
                entries_df["Entry Exit Provider Id"].str.contains("Jean's")
            )
        ]
        stays["Entry Date"] = pd.to_datetime(stays["Entry Exit Entry Date"]).dt.date
        stays["Exit Date"] = pd.to_datetime(stays["Entry Exit Exit Date"]).dt.date
        stays["Exit Date"].fillna(value=datetime(year=2017, month=9, day=30, hour=23, minute=59, second=59))
        stays["LOS"] = (stays["Exit Date"] - stays["Entry Date"]).dt.days
        filtered_stays = stays[["Client Uid", "Entry Date", "Exit Date", "LOS"]]
        total_days = filtered_stays["LOS"].sum()
        total_stays = len(filtered_stays.index)
        un_cleaned_mean = filtered_stays["LOS"].mean()
        cleaned_los_data = filtered_stays[
            np.abs(filtered_stays.LOS - filtered_stays.LOS.mean()) <= (3 * filtered_stays.LOS.std())
            ]
        cleaned_mean = cleaned_los_data.mean()
        if cleaned:
            return tuple(["Length of stay per residential shelter resident (days)", "", cleaned_mean])
        else:
            return tuple(["Length of stay per residential shelter resident (days)", "", un_cleaned_mean])

    def calculate_average_wait_list_length(self, waitlist_df, waitlist="Men"):
        """
        Used by: Agency

        Used for: LOS on Men's Waitlist; LOS on Women's Waitlist

        :param waitlist: This should be either 'Men' or 'Women'
        :param waitlist_df:
        :return:If there are no values that result from a removal of outlier items (3 standard deviations from the mean)
        then a basic mean will be returned other wise the return value will exclude outliers.
        """

        def check_list(waitlist, data_frame=waitlist_df):
            if waitlist == "Men":
                specific_wait_list = data_frame[data_frame["Waitlist Name"].str.contains(waitlist)]
                return specific_wait_list
            elif waitlist == "Women":
                specific_wait_list = data_frame[
                    (
                        data_frame["Waitlist Name"].str.contains(waitlist) |
                        data_frame["Waitlist Name"].str.contains("Jean's")
                    )
                ]
                return specific_wait_list

        specified = check_list(waitlist, waitlist_df.dropna(axis=0, subset=["Waitlist Name"]))
        specified["Event Date"] = pd.to_datetime(specified["Waitlist Event Date"])
        filtered = specified[["ClientID", "Event Date", "Waitlist Event Code"]]
        filtered["q_start"] = datetime(year=2017, month=10, day=1, hour=0, minute=0, second=0)
        filtered["q_end"] = datetime(year=2017, month=12, day=31, hour=23, minute=59, second=59)
        in_shelter = filtered[
            (
                filtered["Waitlist Event Code"].str.contains("IN") &
                (filtered["Event Date"] >= filtered["q_start"]) &
                (filtered["Event Date"] <= filtered["q_end"])
            )
        ]
        in_shelter["In Date"] = in_shelter["Event Date"]
        in_shelter_clean = in_shelter[["ClientID", "In Date"]]
        new_to_list = filtered[
            (
                filtered["Waitlist Event Code"].str.contains("NEW") &
                filtered["ClientID"].isin(in_shelter["ClientID"])
            )
        ]
        new_to_list_sorted = new_to_list.sort_values(by="Event Date").drop_duplicates(subset="ClientID", keep="first")
        new_to_list_clean = new_to_list_sorted[["ClientID", "Event Date"]]
        merged = in_shelter_clean.merge(new_to_list_clean, on="ClientID", how="left")
        merged["time_on_list"] = (merged["In Date"] - merged["Event Date"]).dt.days
        all_values_mean = merged.time_on_list.mean()
        clean_mean = merged[
            np.abs(merged.time_on_list - merged.time_on_list.mean()) <= (3 * merged.time_on_list.std())
        ].time_on_list.mean()
        if clean_mean:
            return tuple([
                "Length of {}'s shelter waitlist (in days)".format(waitlist),
                "",
                "{} Days".format(clean_mean)
            ])
        else:
            return tuple([
                "Length of {}'s shelter waitlist (in days)".format(waitlist),
                "",
                "{} Days".format(all_values_mean)
            ])

    def count_access_employment_services(self, services_df, staff_on_team, direct=False):
        """
        prior to 7/1/2017 = ["Charles Oneill(7792)"]
        from 7/1/2017 - 10/1/2017 = ["Karla Smith(8044)", "Charles Oneill(7792)"]
        post 10/1/2017 = ["Randell Phillips(7727)", "Karla Smith(8044)", "Charles Oneill(7792)"]

        Numbers from this report for the quarters run separately then merged and de-duplicated are not matching numbers
        run for multiple quarters.  This is strange and seems to indicate an error somewhere.  Set unit tests and
        investigate.

        Currently, due to staffing changes during the previous quarter I am running this for multiple quarters using the
        direct=True parameter, assigning the output for each quarter's data to a different variable.  I am then merging
        the variables on the Client Uid column as an 'outer' merge, de-duplicating, and returning the len of the
        resulting data frame's index.

        :param services_df:
        :param staff_on_team:
        :return:
        """
        if direct == True and type(staff_on_team) == list:
            return services_df[
                services_df["Service User Creating"].isin(staff_on_team) &
                services_df["Service Provide Provider"].str.contains("Support")
            ].drop_duplicates(subset="Client Uid")

        elif direct == True and type(staff_on_team) == str:
            return services_df[
                services_df["Service User Creating"].str.contains(staff_on_team) &
                services_df["Service Provide Provider"].str.contains("Support")
            ].drop_duplicates(subset="Client Uid")
        elif type(staff_on_team) == list:
            served = services_df[
                services_df["Service User Creating"].isin(staff_on_team) &
                services_df["Service Provide Provider"].str.contains("Support")
            ].drop_duplicates(subset="Client Uid")
            return tuple(["600 participants will access employment services", 600, len(served.index)])
        elif type(staff_on_team) == str:
            served = services_df[
                (services_df["Service User Creating"] == staff_on_team) &
                services_df["Service Provide Provider"].str.contains("Support")
            ].drop_duplicates(subset="Client Uid")
            return tuple(["600 participants will access employment services", 600, len(served.index)])
        else:
            return tuple(["Error", "Error", "Error"])

    def count_employment_services(self, employment_df, start_date, end_date, metric):
        """
        Currently this method uses some rather flawed data for reporting individuals served.  Instead please used the
        count_access_employment_services  method to report on this metric.

        The end date should be the last day of the quarter or reporting period.

        :param employment_df: A data-frame made from the employment tracker access datasheet available on tprojects.info
        on the support services page.
        :param start_date: date string using the standard U.S. mm/dd/YYYY format
        :param end_date: date string using the standard U.S. mm/dd/YYYY format
        :return: An integer indidcating the number of unique individuals served by the employment a
        """

        start = datetime.strptime(start_date, "%m/%d/%Y")
        end = datetime.strptime(end_date, "%m/%d/%Y")
        employment_df["Start Date"] = start
        employment_df["End Date"] = end
        if metric.lower() == "served":
            in_period_access = employment_df[
                (
                    (employment_df["Start Date"] <= employment_df["Created"]) &
                    (employment_df["Created"] <= employment_df["End Date"])
                ) |
                (
                    employment_df["Date Income Changed"].notna() &
                        (
                            (employment_df["Start Date"] <= employment_df["Date Income Changed"]) &
                            (employment_df["Date Income Changed"] <= employment_df["End Date"])
                        )
                )
            ]
            served = len(in_period_access.drop_duplicates(subset="PT ID").index)
            return tuple(["600 participants will access employment services", 600, served])
        elif metric.lower() == "employment":
            in_period_gained = employment_df[
                employment_df["Employment Gained"].notna() &
                (
                    (employment_df["Start Date"] <= employment_df["Employment Gained"]) &
                    (employment_df["Employment Gained"] <= employment_df["End Date"])
                )
                ]
            gained = len(in_period_gained.drop_duplicates(subset="PT ID").index)
            return tuple(["","", gained])
        elif metric.lower() == "income":
            in_period_gained = employment_df[
                employment_df["Date Income Changed"].notna() &
                (
                    (employment_df["Start Date"] <= employment_df["Employment Gained"]) &
                    (employment_df["Date Income Changed"] <= employment_df["End Date"])
                )
                ]
            gained = len(in_period_gained.drop_duplicates(subset="PT ID").index)
            return tuple(["15% of participants will increase their incomes ****", "15%", gained])
        else:
            return tuple(["Error", "Error", "Error"])

    def count_employment_services_by_provider(self, employment_df, entries_df, provider):

        entries = entries_df[
            entries_df["Entry Exit Provider Id"].str.contains(provider)
        ].drop_duplicates(subset="Client Uid")
        employment = employment_df[["PT ID", "Employment Gained", "Date Income Changed", "Employment Lost"]]
        merged = entries.merge(employment, left_on="Client Uid", right_on="PT ID", how="left")
        cleaned = merged[
            (
                merged["Employment Gained"].notna() &
                (merged["Entry Exit Entry Date"] <= merged["Employment Gained"]) &
                (merged["Employment Gained"] <= merged["Entry Exit Exit Date"])
            ) |
            (
                merged["Date Income Changed"].notna() &
                (merged["Entry Exit Entry Date"] <= merged["Date Income Changed"]) &
                (merged["Date Income Changed"] <= merged["Entry Exit Exit Date"])
            )
        ]
        return tuple([
            "",
            "",
            "{} / {} = {}%".format(
                len(cleaned.index), len(entries.index), 100 * (len(cleaned.index) / len(entries.index))
            )
        ])

    def count_all_ep(self, placements_df):
        """
        Used by: Agency

        :param placements_df:
        :return:
        """
        ep_placements = placements_df[
                placements_df["Intervention Type (TPI)(8745)"] == "Eviction Prevention"
            ]
        de_duplicated_ep = len(ep_placements.drop_duplicates(subset="Client Uid").index)

        return tuple(["124 participants will have their evictions prevented", 124, de_duplicated_ep])

    def count_all_pp(self, placements_df):
        """
        Used by: Agency

        :param placements_df:
        :return:
        """
        pp_placements = placements_df[
            placements_df["Intervention Type (TPI)(8745)"].notnull &
            placements_df["Intervention Type (TPI)(8745)"].str.contains("Permanent")
                ]
        de_duplicated_pp = len(pp_placements.drop_duplicates(subset="Client Uid").index)

        return tuple(["1,065 participants will be permanently housed*", 1065, de_duplicated_pp])

    def count_all_placed(self, placements_df):
        """

        :param placements_df:
        :return:
        """
        return placements_df.drop_duplicates(subset="Client Uid")

    def count_all_placed_by_provider(
            self,
            placements_df,
            provider=["ACCESS", "SSVF - TPI", "Retention", "Residential CM"]
    ):
        """
        Used By: ACCESS, SSVF, Retention, Residential CM
        :param placements_df:
        :param provider:
        :return:
        """
        de_duplicated = placements_df[
            placements_df["Department Placed From(3076)"].isin(provider)
        ].drop_duplicates(subset="Client Uid")
        return len(de_duplicated.index)

    def count_entries_by_provider(self, entries_df, provider):
        """
        Used By:

        :param entries_df:
        :param provider:
        :return:
        """
        if type(provider) == str:
            count = len(entries_df[
                            entries_df["Entry Exit Provider Id"].str.contains(provider)
                        ].drop_duplicates(subset="Client Uid", keep="first").index)

            if provider == "Residential":
                return tuple(["Engage 900 participants in case management", 900, count])
            elif provider == "Retention":
                pass
            elif provider == "SSVF":
                pass
            elif provider == "ACCESS":
                return tuple(["Engage 1200 participants in case management", 1200, count])
            elif provider.lower() == "columbia":
                return tuple(["700 unduplicated participants have a safe place to sleep", 700, count])
            elif provider.lower() == "wil":
                return tuple(["1000 unduplicated participants have a safe place to sleep", 1000, count])
            elif provider.lower() == "5th":
                return tuple(["700 unduplicated participants have a safe place to sleep", 700, count])
            elif provider.lower() == "han":
                return tuple(["1000 unduplicated participants have a safe place to sleep", 1000, count])
            elif provider.lower() == "sos":
                return tuple(["700 unduplicated participants have a safe place to sleep", 700, count])
            elif (provider.lower() == "clark center") or (provider.lower() == "doreen's"):
                return tuple([
                        "550 unduplicated participants have a safe place to sleep at {}".format(provider),
                        550,
                        count
                    ])
            elif provider.lower() == "jean's place":
                return tuple([
                    "350 unduplicated participants have a safe place to sleep at Jean's Place",
                    350,
                    count
                ])

        elif type(provider) == list:
            full_provider_name = {
                "cc": "Transition Projects (TPI) - Clark Center - SP(25)",
                "col": "Transition Projects (TPI) - Columbia Shelter(5857)",
                "dp": "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "h": "Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)",
                "jp": "Transition Projects (TPI) - Jean's Place L1 - SP(29)",
                "sos": "Transition Projects (TPI) - SOS Shelter(2712)",
                "dpgpd": "Transition Projects (TPI) - VA Grant Per Diem (inc. Doreen's Place GPD) - SP(3189)",
                "wc": "Transition Projects (TPI) - Willamette Center(5764)",
                "access": "Transition Projects (TPI) - ACCESS - CM(5471)",
                "res": "Transition Projects (TPI) - Residential - CM(5473)",
                "ret": "Transition Projects (TPI) - Retention - CM(5472)",
                "ca": "Transition Projects (TPI) Housing - Clark Annex PSH - SP(2858)",
                "cagpd": "Transition Projects (TPI) Housing - Clark Annex GPD - SP(4259)"
            }
            provider_list = []

            for dept in provider:
                name = full_provider_name[dept.lower()]
                provider_list.append(name)

            count = len(entries_df[
                            entries_df["Entry Exit Provider Id"].isin(provider_list)
                        ].drop_duplicates(subset="Client Uid", keep="first").index)

            return tuple([
                "1850 unduplicated participants in all emergency shelters will have a safe place to sleep",
                1850,
                count
            ])

    def count_exit_destination_by_shelter_group(self, entries_df, shelter_group):
        low_barrier = [
            "Transition Projects (TPI) - SOS Shelter(2712)",
            "Transition Projects (TPI) - Willamette Center(5764)",
            "Transition Projects (TPI) - Columbia Shelter(5857)",
            "Transition Projects (TPI) - 5th Avenue Shelter(6281)",
            "Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)",
        ]
        residential = [
            "Transition Projects(TPI) - Clark Center - SP(25)",
            "Transition Projects(TPI) - VA Grant Per Diem(inc.Doreen's Place GPD) - SP(3189)",
            "Transition Projects(TPI) - Jean's Place L1 - SP(29)",
            "Transition Projects(TPI) - Doreen's Place - SP(28)",
            "Transition Projects(TPI) - Jean’s Place VA Grant Per Diem(GPD) - SP(3362)"
        ]
        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]
        temp_destination = [
            # "Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)",
            "Hospital or other residential non-psychiatric medical facility (HUD)",
            "Hotel or motel paid for without emergency shelter voucher (HUD)",
            "Jail, prison or juvenile detention facility (HUD)",
            "Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)",
            "Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)",
            "Transitional housing for homeless persons (including homeless youth) (HUD)",
            "Moved from one HOPWA funded project to HOPWA TH (HUD)",
            "Substance abuse treatment facility or detox center (HUD)",
            "Psychiatric hospital or other psychiatric facility (HUD)"
        ]
        if shelter_group.lower() == "res":
            perm = entries_df[
                entries_df["Entry Exit Provider Id"].isin(residential) &
                entries_df["Entry Exit Destination"].notna() &
                entries_df["Entry Exit Destination"].isin(perm_destination)
            ].drop_duplicates(subset="Client Uid")
            temp = entries_df[
                entries_df["Entry Exit Provider Id"].isin(residential) &
                entries_df["Entry Exit Destination"].notna() &
                entries_df["Entry Exit Destination"].isin(temp_destination)
            ].drop_duplicates(subset="Client Uid")
            all = entries_df[
                entries_df["Entry Exit Provider Id"].isin(residential) &
                entries_df["Entry Exit Exit Date"].notna()
            ].drop_duplicates(subset="Client Uid")
            return (len(perm.index), len(temp.index), len(all.index))
        elif shelter_group.lower() == "low":
            perm = entries_df[
                entries_df["Entry Exit Provider Id"].isin(low_barrier) &
                entries_df["Entry Exit Destination"].notna() &
                entries_df["Entry Exit Destination"].isin(perm_destination)
            ].drop_duplicates(subset="Client Uid")
            temp = entries_df[
                entries_df["Entry Exit Provider Id"].isin(low_barrier) &
                entries_df["Entry Exit Destination"].notna() &
                entries_df["Entry Exit Destination"].isin(temp_destination)
            ].drop_duplicates(subset="Client Uid")
            all = entries_df[
                entries_df["Entry Exit Provider Id"].isin(low_barrier) &
                entries_df["Entry Exit Exit Date"].notna()
            ].drop_duplicates(subset="Client Uid")
            return (len(perm.index), len(temp.index), len(all.index))
        else:
            pass

    def count_households_screened(self, entries_hh_df):
        """
        Used By:

        :param entries_hh_df:
        :return:
        """
        screened = len(entries_hh_df[
            entries_hh_df["Entry Exit Provider Id"].str.contains("Screening")
        ].drop_duplicates(subset="Household Uid", keep="first").index)
        return tuple(["Screen 784 veteran families for services", 784, screened])

    def count_hygiene_services_by_provider(self, services_df, provider="Day Center"):
        """
        Use for: Agency, Day Center

        Question: participants will receive hygiene services

        Warning: Do not update the services_1 list to include the newer service code description of
        "Personal Goods/Services" as this will cause the module to return a count including non-hygiene services that
        are sharing this same service code description

        :return: a count of unique participants receiving any hygiene service
        """
        services_1 = [
            "Bathing Facilities",
            "Personal/Grooming Supplies",
            "Hairdressing/Nail Care"
        ]
        services_2 = [
            "Shower",
            "Showers",
            "Laundry Supplies",
            "Clothing",
            "Hairdressing/Nail Care",
            "Personal Grooming Supplies"
        ]
        if provider == "Day Center":
            services = services_df[
                ((services_df["Service Code Description"].isin(services_1)) | (
                services_df["Service Provider Specific Code"].isin(services_2))) &
                services_df["Service Provide Provider"].str.contains(provider)
            ]
            services_provided = services[
                services["Service Provide Provider"].str.contains("Day Center")
            ]
            return tuple(["40,000 hygiene services provided", 40000, len(services_provided.index)])
        elif provider == "Agency":
            services = services_df[
                    ((services_df["Service Code Description"].isin(services_1)) | (
                    services_df["Service Provider Specific Code"].isin(services_2)))
                ]
            de_duped = services.drop_duplicates(subset="Client Uid", inplace=False)
            return tuple(["7,500 participants will receive hygiene services", 7500, len(de_duped.index)])

    def count_id_assistance_by_provider(self, services_df, provider="Day Center"):
        """
        Used by: Day Center

        :param services_df:
        :param provider:
        :return:
        """
        id_assistance = ["Birth Certificate", "Driver's License/State ID Card"]
        served = services_df[
            services_df["Service Provide Provider"].str.contains(provider) & services_df[
                "Service Provider Specific Code"].isin(id_assistance)
        ].drop_duplicates(subset="Client Uid")
        return tuple(["1500 individuals received assistance obtaining ID documents", 1500, len(served.index)])

    def count_mailing_services_by_day_center(self, services_df):
        """
        Used For: Day Center

        :param services_df:
        :return:
        """
        mail_services = len(services_df[
                       services_df["Service Code Description"] == "Temporary Mailing Address"
                   ].index)
        return tuple(["43,000 mailing services provided", 43000, mail_services])

    def count_ongoing_cm_services(self, services_df):
        """
        Used For: Agency

        Issues: Currently, regardless of the method name, this method counts unique individuals served with a CM service
        ignoring department.  This could cause false counts when the wrong service is selected by a non-cm provider and
        does not truly show ongoing services as defined by the agency data dictionary.

        :param services_df:
        :return:
        """

        cm_services = [
            "Case Management - Office Visit",
            "Case Management - Other",
            "Case Management - Phone Meeting",
            "Case Management - Home Visit",
            "Case Management Meeting - Home Visit",
            "Case Management Meeting - Office Visit",
            "Case Management Meeting - Phone"
        ]
        receiving = len(services_df[
                            services_df["Service Provider Specific Code"].isin(cm_services)
                        ].drop_duplicates(subset="Client Uid", inplace=False).index)

        return tuple(["2,100 participants served through case management", 2100, receiving])

    def count_ongoing_cm_services_by_department(self, services_df, provider="SSVF"):
        """
        Used For: Residential CM, Retention, SSVF

        Question: Provide ongoing case management to X participants

        :param services_df:
        :param provider:
        :return:
        """
        cm_services = [
            "Case Management - Office Visit",
            "Case Management - Other",
            "Case Management - Phone Meeting",
            "Case Management - Home Visit",
            "Case Management Meeting - Home Visit",
            "Case Management Meeting - Office Visit",
            "Case Management Meeting - Phone"
        ]
        in_provider = services_df[
            services_df["Service Provide Provider"].str.contains(provider)
        ]
        receiving = in_provider[
            in_provider["Service Provider Specific Code"].isin(cm_services)
        ]
        ongoing = receiving.groupby(by="Client Uid").count()
        output = len(ongoing[ongoing["Service Provider Specific Code"] >= 2].index)

        if provider == "Residential":
            return tuple(["Provide ongoing case management to 700 participants", 700, output])
        elif provider == "Retention":
            return tuple(["Provide ongoing case management to 800 participants", 800, output])
        elif provider == "SSVF":
            return tuple(["Provide ongoing case management to 450 participants", 450, output])
        elif provider == "ACCESS":
            return tuple(["Provide ongoing case management to 800 participants", 800, output])
        else:
            return tuple(["PROVIDERERROR", "PROVIDERERROR", "PROVIDERERROR"])

    def count_perm_by_provider(self, placements_df, provider=["ACCESS", "SSVF - TPI", "Retention", "Residential CM"]):
        """
        Used For: Outreach, SSVF, Retention CM, Residential CM

        :param placements_df:
        :param provider:
        :return:
        """
        placements = len(placements_df[
            (placements_df["Department Placed From(3076)"].isin(provider)) & (
            placements_df["Intervention Type (TPI)(8745)"] == "Permanent Placement")
        ].drop(
            [
                "Client First Name",
                "Client Last Name",
                "Department Placed From(3076)",
                "Placement Case Manager(3075)",
                "Placement Grant(8743)",
                "Reporting Program (TPI)(8748)"
            ],
            axis=1
        ).index)
        if (len(provider) == 1) and (provider[0] == "ACCESS"):
            return tuple(["415 participants move into permanent housing", 415, placements])
        elif (len(provider) == 1) and (provider[0] == "SSVF - TPI"):
            return tuple(["262 veteran families will move into permanent housing", 262, placements])
        else:
            return "Error: Empty Provider List"

    def count_pts_with_barrier_mitigation_and_doc_prep(self, services_df, provider="CHAT"):
        """
        Used by: Coordinated Access (CHAT)

        :param services_df: Use the standard services spread sheet.
        :param provider:
        :return:
        """
        services = [
            "Housing Barrier Resolution",
            "Birth Certificate",
            "DD214",
            "Driver's License/State ID Card",
            "General Form Assistance",
            "Notary Service"
        ]

        served = len(services_df[
            services_df["Service Provide Provider"].str.contains(provider) &
            services_df["Service Provider Specific Code"].isin(services)
        ].drop_duplicates(subset="Client Uid", inplace=False).index)

        return tuple([
            "Provide barrier mitigation and document prep to 150 individuals",
            150,
            served
        ])

    def count_ep_by_provider(self, placements_df, provider=["ACCESS", "SSVF - TPI", "Retention", "Residential CM"]):
        """
        Used For: Outreach, SSVF, Retention CM, Residential CM

        :param placements_df:
        :param provider:
        :return:
        """
        placements = placements_df[
            (placements_df["Department Placed From(3076)"].isin(provider)) & (
                placements_df["Intervention Type (TPI)(8745)"] == "Eviction Prevention")
            ].drop(
            [
                "Client First Name",
                "Client Last Name",
                "Department Placed From(3076)",
                "Placement Case Manager(3075)",
                "Placement Grant(8743)",
                "Reporting Program (TPI)(8748)"
            ],
            axis=1
        )
        if (len(provider) == 1) and (provider[0] == "SSVF - TPI"):
            return tuple(["56 veteran families will have evictions prevented", 56, len(placements.index)])
        else:
            return tuple(["", "", len(placements.index)])

    def count_exclusions_by_provider(self, exclusions_df, provider):
        exclusions = exclusions_df[
            exclusions_df["Infraction Provider"].str.contains(provider) &
            exclusions_df["Infraction Banned Code"].notna() &
            (exclusions_df["Infraction Banned Code"] != "Warning") &
            (exclusions_df["Infraction Banned Code"] != "Safety Alert") &
            (exclusions_df["Infraction Banned Code"] != "Other")
        ]

        return tuple([
            "20% reduction in participant exclusions",
            "20%",
            "{} <--- Must be divided by last quarter's numbers -(last quarter/ this quarter)".format(
                len(exclusions.index)
            )
        ])

    def count_latinos_served_by_provider(self, services_df, provider="Wellness Access"):
        """
        Used For: Wellness Access

        Use: Standard All Services Report

        :param services_df:
        :param provider:
        :return:
        """
        original = services_df
        cleaned = original[
            (
                original["Service Provide Provider"].str.contains(provider) &
                (original["Ethnicity (Hispanic/Latino)(896)"].str.contains("Hispanic/Latino"))
            )
        ].drop_duplicates(subset="Client Uid")
        return tuple(["80 Latino participants outreached to per year", 80, len(cleaned.index)])

    def count_legal_barriers_mitigated(self, entries_df, services_df, provider):
        """
        Used For: SSVF

        Needs to be modified to look at the version of the all services report which includes needs outcomes.

        :param cm_provider:
        :param services_df:
        :param entries_df:
        :return: a count of the participants
        """
        no_na = entries_df.dropna(axis=0, subset=["Entry Exit Provider Id"])
        entries = no_na[no_na["Entry Exit Provider Id"].str.contains(provider)]
        in_provider_list = entries["Client Uid"].tolist()
        legal_services = len(services_df[
            (
                (services_df["Service Code Description"] == "Legal Services") &
                (services_df["Client Uid"].isin(in_provider_list))
            )
        ].drop_duplicates(subset="Client Uid").index)
        return tuple(["50 veteran families will have legal barriers mitigated", 50, legal_services])

    def count_poc_placed(self, placements_df, services_df):
        """
        Used For: Agency

        :param placements_df:
        :return:
        """
        poc_placements = len(placements_df[
            placements_df["Client Uid"].isin(self.return_poc_list(services_df))
                ].drop_duplicates(subset="Client Uid").index)
        return poc_placements

    def count_poc_placed_by_provider(
            self,
            placements_df,
            services_df,
            provider=["ACCESS", "SSVF - TPI", "Retention", "Residential CM"]
    ):
        """
        Used For:

        :param placements_df:
        :param services_df:
        :param provider:
        :return:
        """
        poc_placements = placements_df[
            (
                (placements_df["Client Uid"].isin(self.return_poc_list(services_df))) &
                (placements_df["Department Placed From(3076)"].isin(provider))
            )
                ]
        return len(poc_placements.drop_duplicates(subset="Client Uid").index)

    def count_provider(self, entries_df, cm_provider, goal):
        """
        Used For: Agency

        :param entries_df:
        :param cm_provider:
        :param goal:
        :return:
        """

        provider_ee = len(entries_df[
              entries_df["Entry Exit Provider Id"].str.contains(cm_provider)
        ].drop_duplicates(subset="Client Uid", keep="first").index)

        return tuple(["{} participants served by {}".format(goal, cm_provider), goal, provider_ee])

    def count_referrals_resulting_in_connections(self, services_df, needs_df, provider, referrals, metric):
        """
        Used by: Wellness Access

        Method of the method: First remove rows from the services data frame which were not created by the provider and
        were not in the list of referral services.

        Then, remove rows from the needs data frame where the Client Uid is not in the Client Uid column of the services
        data frame and the need status is not fully met.

        Merge left the needs data frame into the services data frame using Client Uid from both data frames as well as
        Need Creation Date from the need data frame (right) and the service creation data from the services data frame
        (left).  This will be done using the pd.merge method and entering the columns as lists of strings in the
        left_on and right_on params.

        medical_referrals = ["Referral - Eye Care", "Referral - Dental Care", "Referral - Medical Care"]
        mh_referrals = [
        "Referral - A&D Support", "Referral - DV Support", "Referral - Mental Health Care", "Referral - MH Support"
        ]

        :param provider:
        :param services_df:
        :param needs_df:
        :param referrals: provide a list of strings or this will return an error
        :param metric: enter one of the following strings - 'med count', 'mh sud count', 'percent med', 'percent mh sud'
        :return:
        """

        services = services_df[
            services_df["Service Provide Provider"].str.contains(provider) &
            services_df["Service Provider Specific Code"].isin(referrals)
        ]
        needs = needs_df[
            needs_df["Client Uid"].isin(services["Client Uid"].tolist()) &
            (needs_df["Need Status"] == "Closed") &
            (needs_df["Need Outcome"] == "Fully Met")
        ]

        served = pd.merge(
            services,
            needs,
            how="left",
            left_on=["Client Uid", "Service Provide Start Date"],
            right_on=["Client Uid", "Need Date Set"]
        )

        if metric == "med count":
            return tuple([
                "200 connections to medical care per year",
                200,
                len(served.index)
            ])
        elif metric == "mh sud count":
            return tuple([
                "700 connections to mental health or SUD services per year",
                700,
                len(served.index)
            ])
        elif metric == "percent med":
            all = len(served.index)
            clean = served.dropna(axis=0, how="any", subset=["Need Uid"])
            success = len(clean.index)
            return tuple([
                "50% of referrals result in connection to medical care provider",
                "50%",
                "{}/{} = {}%".format(success, all, 100*(success/all))
            ])
        elif metric == "percent mh sud":
            all = len(served.index)
            success = len(served.dropna(axis=0, how="any", subset=["Need Uid"]).index)
            return tuple([
                "50% of referrals result in connection to mental health and/or SUD services",
                "50%",
                "{}/{} = {}%".format(success, all, 100 * (success / all))
            ])
        else:
            return "Param Error: metric's value was not among the list of used values"

    def count_rent_assist(self, services_df):
        """
        Use by: Agency

        Question: participants will receive rent assistance

        :return: a count of unique participants receiving any rent assistance service
        """
        rent_services = [
            "Rent Payment Assistance",
            "Rental Application Fee Payment Assistance",
            "Rental Deposit Assistance"
        ]

        rent_service_2 = [
            "Application Fee",
            "Arrears / Property Debt",
            "Deposit",
            "Rent Payment Assistance"
        ]

        services = services_df[
            (services_df["Service Code Description"].isin(rent_services)) | (
                services_df["Service Provider Specific Code"].isin(rent_service_2))
            ]

        unique = len(services.drop_duplicates(
            subset="Client Uid",
            keep="first",
            inplace=False
        ).index)
        return tuple(["900 participants will receive rent assistance", 900, unique])

    def count_rent_well(self, services_df, type):
        """
        Used by: Agency, RentWell

        This method will identify the participants who either had at least a
        single service by TPI RentWell or a graduation service during the
        reporting period.

        :param services_df:
        :return:
        """

        if type.lower() == "attendance":
            attended = services_df[
                services_df["Service Provider Specific Code"].notna() &
                (
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Attendence") |
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Graduation")
                )
            ].drop_duplicates(subset="Client Uid")
            return tuple(["400 participants will enroll in Rent Well ", 400, len(attended.index)])
        elif type.lower() == "graduation":
            graduated = services_df[
                services_df["Service Provider Specific Code"].notna() &
                services_df["Service Provider Specific Code"].str.contains("RentWell - Graduation")
            ].drop_duplicates(subset="Client Uid")
            return tuple(["240 Participants will graduate RentWell", 240, len(graduated.index)])
        elif type.lower() == "services":
            services = services_df[
                services_df["Service Provider Specific Code"].notna() &
                (
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Attendence") |
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Graduation")
                )
                ]
            return tuple(["", "", len(services.index)])
        elif type.lower() == "all served":
            attended = services_df[
                services_df["Service Provider Specific Code"].notna() &
                (
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Attendence") |
                    services_df["Service Provider Specific Code"].str.contains("RentWell - Graduation")
                )
            ].drop_duplicates(subset="Client Uid")
            return attend[["Client Uid", "Service Provide Start Date"]]
        elif type.lower() == "all graduates":
            graduated = services_df[
                services_df["Service Provider Specific Code"].notna() &
                services_df["Service Provider Specific Code"].str.contains("RentWell - Graduation")
            ].drop_duplicates(subset="Client Uid")
            return graduated[["Client Uid", "Service Provide Start Date"]]
        else:
            return tuple(["ERROR", "ERROR", "ERROR"])

    def count_retention_by_length(self, retention_df, length, provider="agency"):
        """
        Used by: Agency

        For this to work you need to add a Months Post Subsidy column to the follow ups report.  The column must be filled down with the following formula:
        =IF(ISBLANK(B2),"",DATEDIF(B2,C2,"M"))

        :param length: int: 1-12
        :return:
        """
        no_na = retention_df.dropna(axis=0, subset=["Months Post Subsidy"])
        fu_of_duration = no_na[
            (
                (no_na["Months Post Subsidy"] >= length - 1) &
                (no_na["Months Post Subsidy"] <= length + 1)
            )
        ]
        fu_positive = len(fu_of_duration[fu_of_duration["Is Client Still in Housing?(2519)"] == "Yes (HUD)"].index)
        # print(len(retention_df.index), len(no_na.index), fu_positive, len(fu_of_duration.index))
        if provider.lower() == "agency":
            return tuple([
                "80% participants retain their housing for 12 months post-subsidy*",
                "80%",
                "{}/{} = {}%".format(
                    fu_positive,
                    len(fu_of_duration.index),
                    100 * (fu_positive / len(fu_of_duration.index))
                )
            ])
        elif provider.lower() == "ssvf":
            return tuple([
                "90% of participants will remain in housing 12 months after entering housing",
                "90%",
                "{}/{}={}".format(fu_positive, len(fu_of_duration.index), 100*(fu_positive/len(fu_of_duration.index)))
            ])
        else:
            if len(fu_of_duration.index) > 0:
                return tuple([
                    "80% participants retain their housing for 12 months post-subsidy*",
                    "80%",
                    "{}/{} = {}%".format(
                        fu_positive,
                        len(fu_of_duration.index),
                        100 * (fu_positive / len(fu_of_duration.index))
                    )
                ])

            else:
                return tuple([
                    "80% participants retain their housing for 12 months post-subsidy*",
                    "80%",
                    "{}/{} = {}%".format(
                        fu_positive,
                        len(fu_of_duration.index),
                        "N/A"
                    )
                ])


    def count_served_by_provider(self, services_df, provider=""):
        """
        Used For: Day Center

        :param services_df:
        :param provider:
        :return:
        """
        served = len(services_df[
                         services_df["Service Provide Provider"].str.contains(provider)
                     ].drop_duplicates(subset="Client Uid").index)

        if provider != "Day Center":
            return served
        else:
            return tuple([
                "7000 unduplicated participants received services through the day center*",
                7000,
                served
            ])

    def count_services_by_provider(self, services_df, provider):
        """
        USed For: Day Center

        :param services_df:
        :param provider:
        :return:
        """
        services = len(services_df[services_df["Service Provide Provider"].str.contains(provider)].index)
        return tuple(["85000 total services in the {}".format(provider), 85000, services])

    def count_shelter_stays(self, entries_df, agency=True):
        """
        Used For: Agency, Residential Shelters

        :param entries_df:
        :return:
        """
        if agency:
            entries = entries_df[
                (entries_df["Entry Exit Provider Id"].str.contains("Clark Center")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Jean's Place L1")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Doreen's")) | (
                entries_df["Entry Exit Provider Id"].str.contains("SOS")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Hansen")) |(
                entries_df["Entry Exit Provider Id"].str.contains("Peace 2")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Columbia")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Willamette")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Maher")) | (
                entries_df["Entry Exit Provider Id"].str.contains("5th")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Clark Annex"))
            ]

            de_duped = len(entries.drop_duplicates(subset="Client Uid", inplace=False).index)

            return tuple(["2,850 participants will have a safe place to sleep at night*", 2850, de_duped])
        else:
            entries = entries_df[
                (entries_df["Entry Exit Provider Id"].str.contains("Clark Center")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Doreen's")) | (
                entries_df["Entry Exit Provider Id"].str.contains("Jean's Place L1"))
            ]
            de_duped = len(entries.drop_duplicates(subset="Client Uid", inplace=False).index)

            return tuple(["1,000 participants will have a safe place to sleep", 1000, de_duped])

    def count_shelter_to_perm_w_group(self, entries_df, services_df, low_barrier=True):
        """
        Used For: Strategic Initiative

        Current Issue: need to check for zero in denominator of output and return 0 instead of attempting illegal
        division

        :param entries_df:
        :param services_df:
        :param low_barrier:
        :return:
        """
        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]
        if low_barrier:
            attended = self.percent_low_barrier_in_groups(entries_df, services_df, True, False)
        else:
            attended = self.percent_low_barrier_in_groups(entries_df, services_df, False, False)

        exited = entries_df[
            entries_df["Client Uid"].isin(attended) &
            entries_df["Entry Exit Exit Date"].notnull()
            ]
        perm = exited[exited["Entry Exit Destination"].isin(perm_destination)]

        if low_barrier and len(exited.index) > 0:
            return tuple([
                "10% increase in housing placements for participants who attend groups",
                "10%",
                "{}/{} = {}% for current quarter.  Please subtract from number from previous quarter".format(
                    len(perm.index),
                    len(exited.index),
                    100*(len(perm.index)/len(exited.index))
                )
            ])
        elif len(exited.index) == 0:
            return tuple([
                "10% increase in housing placements for participants who attend groups",
                "10%",
                "Error: Denominator == 0"
            ])
        else:
            return tuple([
                "10% increase in service-intensive shelter placements for participants who attend groups",
                "10%",
                "{}/{} = {}% for current quarter.  Please subtract from number from previous quarter".format(
                    len(perm.index),
                    len(exited.index),
                    100 * (len(perm.index) / len(exited.index))
                )
            ])

    def count_transportation_passes_by_provider(self, services_df, provider="Day Center"):
        """
        Used For: Day Center

        :param services_df:
        :param provider:
        :return:
        """
        served = services_df[
            services_df["Service Provide Provider"].str.contains(provider) & (
            services_df["Service Code Description"] == "Transportation Passes")
        ].drop_duplicates(subset="Client Uid")
        return tuple(["1300 individuals received local transit passes", 1300, len(served.index)])

    def days_from_id_to_placement(self, placements_df, entries_df, cm_provider, placement_provider):
        """
        Used For:

        :param entries_df:
        :param placements_df:
        :param cm_provider: just use the short name for the provider
        :param placement_provider: Use one of the following options Retention: ACCESS, Residential CM, Clark Center,
        SSVF - TPI, Doreen's Place, Hansen, Willamette Center
        :return: the mean of the days from id to placement column
        """
        clean_placements = placements_df.dropna(axis=0, how="any", subset=["Department Placed From(3076)"])
        placement_df = clean_placements[clean_placements["Department Placed From(3076)"].isin(placement_provider)]
        entry_dates = entries_df[entries_df["Entry Exit Provider Id"].str.contains(cm_provider)]
        pd.to_datetime(placement_df["Placement Date(3072)"])
        pd.to_datetime(entry_dates["Entry Exit Entry Date"])
        entry_dates = entry_dates[["Client Uid", "Entry Exit Entry Date"]]
        merged = pd.merge(placement_df, entry_dates, on="Client Uid", how="left")
        merged["Days from ID to Placement"] = placement_df["Placement Date(3072)"] - merged["Entry Exit Entry Date"]

        return tuple([
            "Number of days from identification to placement <90*",
            "<90",
            merged["Days from ID to Placement"].mean().days
        ])

    def exit_destination_by_shelter_type(self, entries_df, shelter_group):
        low_barrier_shelters = [
            "Transition Projects (TPI) - Willamette Center(5764)",
            "Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)",
            "Transition Projects (TPI) - Columbia Shelter(5857)",
            "Transition Projects (TPI) - SOS Shelter(2712)",
            "Transition Projects (TPI) - 5th Avenue Shelter(6281)"
        ]
        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]
        temp_destination = [
            # "Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)",
            "Hospital or other residential non-psychiatric medical facility (HUD)",
            "Hotel or motel paid for without emergency shelter voucher (HUD)",
            "Jail, prison or juvenile detention facility (HUD)",
            "Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)",
            "Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)",
            "Transitional housing for homeless persons (including homeless youth) (HUD)",
            "Moved from one HOPWA funded project to HOPWA TH (HUD)",
            "Substance abuse treatment facility or detox center (HUD)",
            "Psychiatric hospital or other psychiatric facility (HUD)"
        ]
        entries = entries_df[entries_df["Entry Exit Provider Id"].isin(low_barrier_shelters)]
        exits = entries[entries["Entry Exit Exit Date"].notna()]
        positive = exits[
            exits["Entry Exit Destination"].isin(temp_destination) | exits["Entry Exit Destination"].isin(
                perm_destination)
        ].drop_duplicates(subset="Client Uid")
        perm = exits[
            exits["Entry Exit Destination"].isin(perm_destination)
        ].drop_duplicates(subset="Client Uid")
        temp = exits[
            exits["Entry Exit Destination"].isin(temp_destination)
        ].drop_duplicates(subset="Client Uid")
        return tuple([
            "% all low barrier shelter to stable or perm",
            "15%",
            "{}/{}={}%".format(
                len(positive.index),
                len(exits.drop_duplicates(subset="Client Uid").index),
                100 * (len(positive.index) / len(exits.drop_duplicates(subset="Client Uid").index))
            ),
            len(perm.index),
            len(temp.index)

        ])
    def exit_destination_by_provider(self, entries_df, provider, exit_type="perm temp"):
        """
        Used For: Strategic Initiative, Low-Barrier Shelters

        :param entries_df:
        :param provider:
        :param exit_type:
        :return:
        """
        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]

        temp_destination = [
            # "Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)",
            "Hospital or other residential non-psychiatric medical facility (HUD)",
            "Hotel or motel paid for without emergency shelter voucher (HUD)",
            "Jail, prison or juvenile detention facility (HUD)",
            "Staying or living with family, temporary tenure (e.g., room, apartment or house)(HUD)",
            "Staying or living with friends, temporary tenure (e.g., room apartment or house)(HUD)",
            "Transitional housing for homeless persons (including homeless youth) (HUD)",
            "Moved from one HOPWA funded project to HOPWA TH (HUD)",
            "Substance abuse treatment facility or detox center (HUD)",
            "Psychiatric hospital or other psychiatric facility (HUD)"
        ]

        entries = entries_df[entries_df["Entry Exit Provider Id"].str.contains(provider)]
        exits = entries.dropna(axis=0, subset=["Entry Exit Exit Date"])
        perm = exits[exits["Entry Exit Destination"].isin(perm_destination)]
        temp = exits[exits["Entry Exit Destination"].isin(temp_destination)]

        if exit_type == "all":
            return entries, perm, temp, exits
        elif exit_type == "perm temp":
            return perm, temp, exits
        elif exit_type == "perm":
            return perm, exits
        elif exit_type == "temp":
            return temp, exits
        elif exit_type == "count perm":
            return len(perm.index)
        elif exit_type == "count temp":
            return len(temp.index)
        elif exit_type == "count exits":
            return len(exits.index)
        elif exit_type == "count entries":
            return len(entries.index)
        elif exit_type == "percent perm":
            return "{}/{} = {}%".format(len(perm), len(exits), 100*(len(perm)/len(exits)))
        elif exit_type == "percent temp":
            return "{}/{} = {}%".format(len(temp), len(exits), 100*(len(temp)/len(exits)))
        elif exit_type == "perm and temp percent":
            entries = entries_df[entries_df["Entry Exit Provider Id"].str.contains(provider)]
            exits = entries.dropna(axis=0, subset=["Entry Exit Exit Date"])
            perm_or_temp = exits[
                exits["Entry Exit Destination"].isin(perm_destination) |
                exits["Entry Exit Destination"].isin(temp_destination)
            ].drop_duplicates(subset="Client Uid")
            all = exits.drop_duplicates(subset="Client Uid")
            return "{} / {} = {} %".format(len(perm_or_temp.index),len(all.index), 100*(len(perm_or_temp)/len(all)))

    def percent_exits_from_low_barrier_to_service_intensive(self, entries_df, low_barrier_provider):
        """
        Used For: Strategic Initiative

        :param entries_df:
        :param low_barrier_provider:
        :return:
        """

        count = 0
        intensive_entries = entries_df[
            entries_df["Entry Exit Provider Id"].str.contains("Clark Center") |
            entries_df["Entry Exit Provider Id"].str.contains("Doreen's Place") |
            entries_df["Entry Exit Provider Id"].str.contains("Jean's Place")
        ]
        intensive_entries["Start"] = pd.to_datetime(intensive_entries["Entry Exit Entry Date"]).dt.date
        intensive = intensive_entries[["Client Uid", "Start"]]
        exiting_shelter = entries_df[
            entries_df["Entry Exit Provider Id"].str.contains(low_barrier_provider) &
            entries_df["Entry Exit Exit Date"].notnull()
        ]
        exiting_shelter["Exit"] = pd.to_datetime(exiting_shelter["Entry Exit Exit Date"]).dt.date

        for row in exiting_shelter.index:
            client = exiting_shelter.loc[row, "Client Uid"]
            exit = exiting_shelter.loc[row, "Exit"]
            entry_data = intensive[intensive["Client Uid"] == client]
            for e_row in entry_data.index:
                if exit >= (entry_data.loc[e_row, "Start"] + relativedelta(days=-5)):
                    count += 1
                else:
                    pass

        exit_count = len(exiting_shelter.index)
        to_intensive_percent = 100*(count/exit_count)
        return tuple([
            "16% of Hansen participants move to a services-intensive shelter",
            "16%",
            "{} / {} = {}%".format(count, exit_count, to_intensive_percent)
        ])

    def percent_exits_caused_by_exclusion(self, entries_df_plus_reason, shelter_type):
        """
        Used For: Service Intensive Shelters

        :param entries_df_plus_reason:
        :param shelter_type:
        :return:
        """
        if shelter_type.lower() == "res":
            leavers = entries_df_plus_reason[
                entries_df_plus_reason["Entry Exit Exit Date"].notnull() & (
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Doreen's") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Jean's") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Clark Center")
                )
            ]
        else:
            leavers = entries_df_plus_reason[
                entries_df_plus_reason["Entry Exit Exit Date"].notnull() & (
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Columbia") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Hansen") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("SoS") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("5th") |
                    entries_df_plus_reason["Entry Exit Provider Id"].str.contains("Willamette")
                )
            ]
        excluded = leavers[leavers["Entry Exit Reason Leaving"] == "Non-compliance with program"]
        leaver_count = len(leavers.index)
        excluded_count = len(excluded.index)
        percent_excluded = 100 * (excluded_count / leaver_count)
        return tuple([
            "15% decrease in behavior based exclusions",
            "<= -15%",
            "{} / {} = {} <--- Don't forget to subtract this from the previous quarters numbers".format(excluded_count,
                                                                                                        leaver_count,
                                                                                                        percent_excluded)
        ])

    def percent_iap_successful(self, entries_plus_df):
        """
        Used For: Wellness Access

        :param entries_plus_df:
        :return:
        """

        all_entries = entries_plus_df[
            (
                entries_plus_df["Entry Exit Provider Id"].str.contains("IAP") |
                entries_plus_df["Entry Exit Provider Id"].str.contains("PIAP")
            )
        ]
        entry_count = len(all_entries.index)
        successful = len(all_entries[
            all_entries["Entry Exit Exit Date"].notnull() &
            all_entries["Entry Exit Reason Leaving"].str.contains("Completed")
                         ].index)
        any_exit = len(all_entries[all_entries["Entry Exit Exit Date"].notnull()].index)
        return tuple([
            "60% of IAPs will be successfully completed by participants",
            "60%",
            "{}/{} = {}%".format(successful, any_exit, 100*(successful/any_exit))
        ])

    def percent_low_barrier_in_groups(self, entries_df, services_df, low_barrier=True, direct=True):
        """
        Used For: Strategic Initiative

        Potential Issue: If a participant does not have an end date for their shelter stay this method will provide an
        end date of the current day.  This will lead to services outside of the reporting quarter being counted as
        acceptable.  This will likely need to be rectified prior to releasing related numbers.

        :param entries_df:
        :param services_df:
        :param low_barrier:
        :param direct:
        :return:
        """

        low_barrier_shelters = [
            "Transition Projects (TPI) - Willamette Center(5764)",
            "Transition Projects (TPI) - Hansen Emergency Shelter - SP(5588)",
            "Transition Projects (TPI) - Columbia Shelter(5857)",
            "Transition Projects (TPI) - SOS Shelter(2712)",
            "Transition Projects (TPI) - 5th Avenue Shelter(6281)"
        ]
        service_intensive = [
            "Transition Projects (TPI) - Clark Center - SP(25)",
            "Transition Projects (TPI) - Doreen's Place - SP(28)",
            "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
        ]
        if low_barrier:
            entries = entries_df[entries_df["Entry Exit Provider Id"].isin(low_barrier_shelters)]
        else:
            entries = entries_df[entries_df["Entry Exit Provider Id"].isin(service_intensive)]

        conditions = [entries["Entry Exit Exit Date"].isnull(),entries["Entry Exit Exit Date"].notnull()]
        choices = [datetime.now().date(), pd.to_datetime(entries["Entry Exit Exit Date"]).dt.date]
        entries["End"] = np.select(conditions, choices, default=datetime.now().date())
        entries["Start"] = pd.to_datetime(entries["Entry Exit Entry Date"]).dt.date
        pt_list = entries["Client Uid"].tolist()

        attendees = services_df[
            services_df["Service Provider Specific Code"].str.contains("Group") &
            services_df["Client Uid"].isin(pt_list)
        ]
        attendees["Service Date"] = pd.to_datetime(attendees["Service Provide Start Date"]).dt.date

        participants = {pt: 0 for pt in list(set(pt_list))}

        for row in entries.index:
            e_client = entries.loc[row, "Client Uid"]
            e_entry = entries.loc[row, "Start"]
            e_exit = entries.loc[row, "End"]
            for s_row in attendees.index:
                s_client = attendees.loc[s_row, "Client Uid"]
                s_date = attendees.loc[s_row, "Service Date"]
                if (s_client == e_client) and (e_entry <= s_date <= e_exit):
                    participants[e_client] += 1
                else:
                    pass

        all_pt = len(list(set(pt_list)))
        final_data = pd.DataFrame.from_dict(participants, orient="index")
        served = len(final_data[final_data[0] != 0].index)

        if direct:
            return tuple([
                "35% of shelter residents attend on-site groups or activities",
                "35%",
                "{} / {} = {}%".format(served, all_pt, 100*(served/all_pt))
            ])
        else:
            return  final_data[final_data[0] != 0].index.tolist()

    def percent_low_barrier_to_perm(self, entries_df):
        """
        Used For: Strategic Initiative

        :param entries_df:
        :return:
        """

        h_perm, h_all = self.exit_destination_by_provider(entries_df, "Hansen", "perm")
        w_perm, w_all = self.exit_destination_by_provider(entries_df, "Willamette", "perm")
        s_perm, s_all = self.exit_destination_by_provider(entries_df, "SOS", "perm")
        c_perm, c_all = self.exit_destination_by_provider(entries_df, "Columbia", "perm")
        f_perm, f_all = self.exit_destination_by_provider(entries_df, "5th", "perm")
        all_perm = len(h_perm.index) + len(w_perm.index) + len(s_perm.index) + len(c_perm.index) + len(f_perm.index)
        all_exits = len(h_all.index) + len(w_all.index) + len(s_all.index) + len(c_all.index) + len(f_all.index)
        return tuple([
            "15% of participants exit to permanent housing",
            "15%",
            "{} / {} = {}%".format(all_perm, all_exits, 100*(all_perm/all_exits))
        ])

    def percent_low_barrier_to_stable(self, entries_df):
        """
        Used For: Strategic Initiative

        :param entries_df:
        :return:
        """

        h_temp, h_all = self.exit_destination_by_provider(entries_df, "Hansen", "temp")
        w_temp, w_all = self.exit_destination_by_provider(entries_df, "Will", "temp")
        s_temp, s_all = self.exit_destination_by_provider(entries_df, "SOS", "temp")
        c_temp, c_all = self.exit_destination_by_provider(entries_df, "Columbia", "temp")
        f_temp, f_all = self.exit_destination_by_provider(entries_df, "5th", "temp")
        all_temp = len(h_temp.index) + len(w_temp.index) + len(s_temp.index) + len(c_temp.index) + len(f_temp.index)
        all_exits = len(h_all.index) + len(w_all.index) + len(s_all.index) + len(c_all.index) + len(f_all.index)
        return tuple([
            "15% of participants exit to stable housing",
            "15%",
            "{} / {} = {}%".format(all_temp, all_exits, 100*(all_temp/all_exits))
        ])

    def percent_non_poc_exiting_to_perm_by_provider(
            self,
            entries_df,
            services_df,
            provider,
            direct=True
    ):
        """
        Used For:

        :param entries_df:
        :param services_df:
        :param provider:
        :param direct:
        :return:
        """
        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]
        exited = entries_df[
            entries_df["Entry Exit Exit Date"].notna() &
            entries_df["Entry Exit Provider Id"].isin(provider) &
            ~entries_df["Client Uid"].isin(self.return_poc_list(services_df))
            ]
        perm = len(exited[exited["Entry Exit Destination"].isin(perm_destination)])
        if direct:
            return tuple([
                "Participants housed are at least 40% people of color",
                "40%",
                "{}/{} = {}%".format(perm, len(exited), 100*(perm/len(exited)))
            ])
        else:
            return perm, len(exited.index)

    def percent_poc_exiting_to_perm_by_provider(
            self,
            entries_df,
            services_df,
            providers=[
                "Transition Projects (TPI) Housing - Clark Annex GPD - SP(4259)",
                "Transition Projects (TPI) Housing - Clark Annex PSH - SP(2858)",
                "Transition Projects (TPI) Housing - Barbara Maher Apartments PSH - SP(3018)"
            ],
            direct=True
    ):
        """
        Used For:

        :param entries_df:
        :param services_df:
        :param providers:
        :param direct:
        :return:
        """

        perm_destination = [
            "Owned by client, no ongoing housing subsidy (HUD)",
            "Owned by client, with ongoing housing subsidy (HUD)",
            "Permanent housing for formerly homeless persons (HUD)",
            "Rental by client, no ongoing housing subsidy (HUD)",
            "Rental by client, with other ongoing housing subsidy (HUD)",
            "Rental by client, with VASH subsidy (HUD)",
            "Staying or living with family, permanent tenure (HUD)",
            "Staying or living with friends, permanent tenure (HUD)",
            "Foster care home or foster care group home (HUD)",
            "Rental by client, with GPD TIP subsidy (HUD)",
            "Permanent housing (other than RRH) for formerly homeless persons (HUD)",
            "Moved from one HOPWA funded project to HOPWA PH (HUD)",
            "Long-term care facility or nursing home (HUD)",
            "Residential project or halfway house with no homeless criteria (HUD)"
        ]

        exited = entries_df[
            entries_df["Entry Exit Exit Date"].notna() &
            entries_df["Entry Exit Provider Id"].isin(providers) &
            entries_df["Client Uid"].isin(self.return_poc_list(services_df))
        ]
        perm = len(exited[exited["Entry Exit Destination"].isin(perm_destination)])
        if direct:
            if len(exited) > 0:
                return tuple([
                    "Participants housed are at least 40% people of color",
                    "40%",
                    "{}/{} = {}%".format(perm, len(exited), 100*(perm/len(exited)))
                ])
            else:
                return tuple([
                    "Participants housed are at least 40% people of color",
                    "40%",
                    "{}/{} = {}%".format(perm, len(exited), "N/A")

                ])
        else:
            return perm, len(exited.index)

    def percent_of_pt_w_home_visits_by_provider(self, services_df, entries_df, provider):
        """
        Used by: SSVF

        :param services_df:
        :param entries_df:
        :param provider:
        :return:
        """
        hv_services = [
            "Case Management Meeting - Home Visit"
        ]
        hv_serviced = len(
            services_df[
                (services_df["Service Provider Specific Code"].isin(hv_services)) &
                (services_df["Service Provide Provider"].str.contains(provider))
            ].drop_duplicates(subset="Client Uid").index
        )

        all_w_entry = len(entries_df[
            entries_df["Entry Exit Provider Id"].str.contains(provider)
        ].drop_duplicates(subset="Client Uid").index)
        output = "{} / {} = {}%".format(hv_serviced, all_w_entry, 100 * (hv_serviced / all_w_entry))
        return tuple(["25% of participants will have quarterly home visits", "25%", output])

    def percent_placed_are_poc(self, placements_df, services_df):
        """
        Used For: Agency

        :param placements_df:
        :param services_df:
        :return:
        """

        poc = self.count_poc_placed(placements_df, services_df)
        all = len(self.count_all_placed(placements_df).index)
        return tuple([
            "Participants housed are at least 41% participants of color",
            "41%",
            "{}/{} = {}%".format(poc, all, 100*(poc/all))
        ])

    def percent_poc_placed_by_provider(self, placements_df, services_df, provider):
        """
        Used For: SSVF

        :param placements_df:
        :param services_df:
        :param provider:
        :return:
        """

        poc_placed = self.count_poc_placed_by_provider(placements_df, services_df, provider)
        all_by_provider = self.count_all_placed_by_provider(placements_df, provider)

        if provider == ["SSVF - TPI"]:
            return tuple([
                "Veterans housed are at least 25% people of color",
                "25%",
                "{}/{} = {}%".format(poc_placed, all_by_provider, 100 * (poc_placed / all_by_provider))
            ])
        else:
            return tuple([
                "Participants housed are at least 41% people of color",
                "41%",
                "{}/{} = {}%".format(poc_placed, all_by_provider, 100 * (poc_placed / all_by_provider))
            ])

    def percent_poc_placed_vs_percent_white_placed_by_shelter(self, entries_df, services_df, provider):
        """
        Used For: Service Intensive Shelters

        :param entries_df:
        :param services_df:
        :param provider:
        :return:
        """
        if provider == "res":
            poc_perm, poc_all = self.percent_poc_exiting_to_perm_by_provider(
                entries_df,
                services_df,
                providers=[
                    "Transition Projects (TPI) - Doreen's Place - SP(28)",
                    "Transition Projects (TPI) - Clark Center - SP(25)",
                    "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
                ],
                direct=False
            )

            perm, all = self.percent_non_poc_exiting_to_perm_by_provider(entries_df, services_df, [
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
            ], False)

            poc_perm = poc_perm
            poc_all = poc_all
            perm = perm
            all_served = all

            return tuple([
                "Participants who are people of color that exit the program have housing outcomes greater than or equal to those of non-people of color",
                ">= 0%",
                "({}/{})-({}/{})={}%".format(
                    poc_perm,
                    poc_all,
                    perm,
                    all_served,
                    100*((poc_perm / poc_all) - (perm / all_served))
                )
            ])

        else:
            poc_perm, poc_all = self.percent_poc_exiting_to_perm_by_provider(
                entries_df,
                services_df,
                providers=provider,
                direct=False
            )
            perm, all = self.percent_non_poc_exiting_to_perm_by_provider(entries_df, services_df, provider, False)

            return tuple([
                "Participants who are people of color that exit the program have housing outcomes greater than or equal to those of non-people of color",
                ">= 0%",
                "({}/{})-({}/{})={}%".format(
                    poc_perm,
                    poc_all,
                    perm,
                    all,
                    100*((poc_perm / poc_all) - (perm / all))
                )
            ])

    def percent_poc_w_small_s_support_services_by_provider(self, services_df, provider):
        """
        Used by: Day Center

        :param services_df:
        :param provider:
        :return:
        """
        poc_list = self.return_poc_list(services_df)

        services_1 = [
            "Bathing Facilities",
            "Personal/Grooming Supplies",
            "Hairdressing/Nail Care"
        ]
        services_2 = [
            "Shower",
            "Showers",
            "Laundry Supplies",
            "Clothing",
            "Hairdressing/Nail Care",
            "Personal Grooming Supplies"
        ]
        services = services_df[
            ~(
             (services_df["Service Code Description"].isin(services_1)) |
             (services_df["Service Provider Specific Code"].isin(services_2))
             ) &
            services_df["Service Provide Provider"].str.contains("Day") &
            services_df["Client Uid"].isin(poc_list)
        ]
        small_s_de_duped = services.drop_duplicates(subset="Client Uid", inplace=False)
        served_by_day = services_df[
            services_df["Service Provide Provider"].str.contains("Day") &
            services_df["Client Uid"].isin(poc_list)
        ].drop_duplicates(subset="Client Uid")

        poc_ss_served = len(small_s_de_duped.index)
        all_served = len(served_by_day.index)
        percent = 100*(poc_ss_served/all_served)

        return tuple([
            "50% of people of color served by the Day Center access a supportive service",
            ">= 50%",
            "{}/{} = {}%".format(poc_ss_served, all_served, percent)
        ])

    def percent_residents_oriented_in_ten_days(self, entries_df, services_df, providers):
        """
        Used For: Service Intensive Shelters

        Future Improvement Idea: Add a way to break out individual shelter data to make this metric more useful to
        each of the shelter managers.

        :param entries_df:
        :param services_df:
        :param providers:
        :return:
        """

        orientation_services = ["Shelter Orientation", "Orientation - Residential Program"]

        entry_to_providers = entries_df[
            entries_df["Entry Exit Provider Id"].isin(providers)
        ]
        entry_to_providers["Entry Date"] = pd.to_datetime(entry_to_providers["Entry Exit Entry Date"]).dt.date
        entry_date = entry_to_providers.filter(["Client Uid", "Entry Date"], axis=1)

        orientation_services = services_df[
            services_df["Service Provider Specific Code"].isin(orientation_services)
        ]
        orientation_services["Service Date"] = pd.to_datetime(orientation_services["Service Provide Start Date"]).dt.date
        orient_date = orientation_services.filter(["Client Uid", "Service Date"])

        merged = entry_date.merge(orient_date, on="Client Uid", how="left")
        conditions = [merged["Service Date"].notnull(), merged["Service Date"].isnull()]
        choices = [((merged["Service Date"] - merged["Entry Date"]).dt.days), np.nan]
        merged["Days to Orientation"] = np.select(conditions, choices, default=np.nan)
        not_na = merged[merged["Days to Orientation"].notna()]

        oriented_in_seven_days = len(
            not_na[
                (not_na["Days to Orientation"].astype(float) <= 10)
            ].index
        )
        all_entries = len(merged.index)

        return tuple([
            "95% of participants will attend orientation within the first 10 days",
            ">= 95%",
            "{} / {} = {}".format(oriented_in_seven_days, all_entries, 100*(oriented_in_seven_days/all_entries))
        ])

    def percent_shelter_stays_less_than_seven_days(self, entries_df, providers):
        """
        Use For: Service Intensive Shelters

        :param entries_df:
        :param providers:
        :return:
        """
        exits = entries_df[
            entries_df["Entry Exit Exit Date"].notnull() &
            entries_df["Entry Exit Provider Id"].isin(providers)
        ]

        exits["Entry Date"] = pd.to_datetime(exits["Entry Exit Entry Date"]).dt.date
        exits["Exit Date"] = pd.to_datetime(exits["Entry Exit Exit Date"]).dt.date
        exits["LOS"] = (exits["Exit Date"] - exits["Entry Date"]).dt.days

        all_exits = len(exits.index)
        short_exits = len(exits[exits["LOS"] <= 7])

        return tuple([
            "10% decrease in participants leaving prior to 7 days",
            "10%",
            "{} / {} = {}% <----- must subtract last quarters numbers from this".format(
                short_exits,
                all_exits,
                100*(short_exits/all_exits)
            )
        ])

    def percent_rent_well_housed(self, services_df, placements_df):
        grads = self.count_rent_well(services_df, "all graduates")
        placed = placements_df[
            placements_df["Client Uid"].isin(grads["Client Uid"])
        ]
        merged = pd.merge(placed, grads, how="outer", on="Client Uid")
        merged = merged[
            (merged["Service Provide Start Date"] < merged["Placement Date(3072)"]) |
            (merged["Service Provide Start Date"] == merged["Placement Date(3072)"])
        ]
        if len(merged.index > 0):
            return tuple([
                "35% of FY 17-18 graduates of TPI RentWell classes will gain housing",
                "35%",
                "{}/{}={}%".format(
                    len(merged.index),
                    len(grads.index),
                    100*(len(merged.index)/len(grads.index))
                )
            ])

        else:
            return tuple([
                "35% of FY 17-18 graduates of TPI RentWell classes will gain housing",
                "35%",
                "0%"
            ])

    def percent_to_destination_by_shelter(self, entries_df, provider, type):
        """
        Used For: Columbia, Hansen, SOS, 5th Ave., Willamette, Residential Shelters

        :param entries_df: The entry exit data dataframe
        :param provider: use Res to indicate the residential shelters.  For the low barrier shelters simply use the
        first three letters of the shelter's name
        :param type: Select either perm or temp
        :return:
        """
        es_list = ["columbia", "wil", "sos", "hans", "5th"]

        if provider.lower() == "res":
            perm_d, temp_d, all_d = self.exit_destination_by_provider(entries_df, "Doreen's")
            perm_c, temp_c, all_c = self.exit_destination_by_provider(entries_df, "Clark Center")
            perm_j, temp_j, all_j = self.exit_destination_by_provider(entries_df, "Jean's")
            total_perm = len(perm_d.index) + len(perm_c.index) + len(perm_j.index)
            total_temp = len(temp_d.index) + len(temp_c.index) + len(temp_j.index)
            all_exits = len(all_d.index) + len(all_c.index) + len(all_j.index)
        elif provider.lower() in es_list:
            perm, temp, all = self.exit_destination_by_provider(entries_df, provider, "perm temp")
            total_perm = len(perm.index)
            total_temp = len(temp.index)
            all_exits = len(all.index)
        else:
            return TypeError

        if (provider.lower() in es_list) and (type == "perm"):
            return tuple([
                "5% of participants will move from residential programs into permanent housing",
                "5%",
                "{}/{} = {}%".format(total_perm, all_exits, 100 * (total_perm / all_exits))
            ])
        elif (provider.lower() in es_list) and (type == "stable"):
            return tuple([
                "15% of participants will move from residential programs into permanent housing",
                "15%",
                "{}/{} = {}%".format(total_temp, all_exits, 100 * (total_temp / all_exits))
            ])
        elif type == "perm":
            return tuple([
                "35% of all participants in the residential programs will move into permanent housing",
                "35%",
                "{} / {} = {}".format(total_perm, all_exits, 100*(total_perm/all_exits))
            ])
        elif type == "temp":
            return tuple([
                "15% of all the participants in the residential programs will move into stable housing",
                "15%",
                "{} / {} = {}".format(total_temp, all_exits, 100*(total_temp/all_exits))
            ])
        else:
            pass

    def poc_served(self, services_df):
        """
        Used For: Agency

        :param services_df:
        :return:
        """
        poc_list = self.return_poc_list(services_df)
        all_served = services_df.drop_duplicates(subset="Client Uid")
        poc = all_served[all_served["Client Uid"].isin(poc_list)].drop_duplicates(subset="Client Uid")

        return tuple([
            "Participants served are at least 41% participants of color ",
            "41%",
            "{}/{} = {}%".format(len(poc.index), len(all_served.index), 100*(len(poc.index)/len(all_served.index)))
        ])

    def poc_served_by_provider(self, services_df, provider):
        """
        Used For: Agency, SSVF, Day Center

        !Important Question!

        :param services_df:
        :return:
        """
        poc_list = self.return_poc_list(services_df)
        if provider.lower() == "res":
            provider_list = [
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - VA Grant Per Diem (inc. Doreen's Place GPD) - SP(3189)",
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
            ]
            all_served = services_df[
                services_df["Service Provide Provider"].isin(provider_list)
            ].drop_duplicates(subset="Client Uid")
            poc = all_served[
                all_served["Client Uid"].isin(poc_list) &
                all_served["Service Provide Provider"].isin(provider_list)
                ]
        else:
            all_served = services_df[
                services_df["Service Provide Provider"].str.contains(provider)
            ].drop_duplicates(subset="Client Uid")
            poc = all_served[
                all_served["Client Uid"].isin(poc_list) &
                all_served["Service Provide Provider"].str.contains(provider)
            ]
        if provider == "SSVF":
            return tuple([
                "Veterans served are at least 25% participants of color ",
                "25%",
                "{}/{} = {}%".format(len(poc.index), len(all_served.index), 100*(len(poc.index)/len(all_served.index)))
            ])
        elif provider.lower() == "day":
            return tuple([
                "Participants 40% people of color",
                "40%",
                "{}/{} = {}%".format(len(poc.index), len(all_served.index),
                100 * (len(poc.index) / len(all_served.index)))
            ])
        else:
            return tuple([
                "Participants served are at least 40% people of color",
                "40%",
                "{}/{} = {}%".format(len(poc.index), len(all_served.index),
                100 * (len(poc.index) / len(all_served.index)))
            ])

    def poc_utilizing_shelter_by_provider(self, entries_df, services_df, provider):
        poc_list = self.return_poc_list(services_df)
        if provider.lower() == "res":
            provider_list = [
                "Transition Projects (TPI) - Clark Center - SP(25)",
                "Transition Projects (TPI) - Doreen's Place - SP(28)",
                "Transition Projects (TPI) - VA Grant Per Diem (inc. Doreen's Place GPD) - SP(3189)",
                "Transition Projects (TPI) - Jean's Place L1 - SP(29)"
            ]
            all_entered = entries_df[
                entries_df["Entry Exit Provider Id"].isin(provider_list)
            ].drop_duplicates(subset="Client Uid")
            poc = all_entered[
                all_entered["Client Uid"].isin(poc_list)
            ]
        else:
            all_entered = entries_df[
                entries_df["Entry Exit Provider Id"].str.contains(provider)
            ].drop_duplicates(subset="Client Uid")
            poc = all_entered[
                all_entered["Client Uid"].isin(poc_list)
            ]

        return tuple([
            "Participants 40% people of color",
            "40%",
            "{}/{} = {}%".format(len(poc.index), len(all_entered.index),
            100 * (len(poc.index) / len(all_entered.index)))
        ])

    def received_application_readiness_assistance(self, services_df):
        """
        Use For: Agency

        Question: participants will receive application readiness assistance (identification, birth certificates,
                  debt reduction, etc.)

        :return:
        """

        services = [
            "Credit Check",
            "Background/Credit Check",
            "Background Check",
            "Birth Certificate",
            "Driver's License/State ID Card",
            "Arrears / Property Debt",
            "Sex Offender Registration Relief",
            "Consumer Debt Legal Services",
            "Records/License/Permits Fee Assistance",
            "RentWell - Attendence",
            "Rent Well - Study Hall / Lab",
            "RentWell - Graduation",
            "Rent Well - Graduation",
            "Rent Well - One-on-One",
            "Group - Housing - Application Session",
            "Debt Reduction",
            "Housing Barrier Resolution",
            "Housing Search Assistance",
            "Consumer Debt Legal Services",
            "Records/License/Permits Fee Assistance",
            "Expungement"
        ]

        services_2 = [
            "Tenant Readiness Education Programs",
            "Certificates/Forms Assistance",
            "Debt Reduction Funds",
            "Housing Counseling"
        ]

        served = len(services_df[
            (
                (services_df["Service Provider Specific Code"].isin(services)) | (
                    services_df["Service Code Description"].isin(services_2))
            )
        ].drop_duplicates(subset="Client Uid").index)

        return tuple([
            "300 participants will receive application readiness assistance (identification, birth certificates, debt reduction, etc.)",
            300,
            served
            ])

    def referral_to_best_by_provider(self, services_df, provider="ACCESS"):
        """
        Used For: Residential CM, Retention, ACCESS, SSVF

        :param services_df:
        :param provider:
        :return:
        """
        all_served = self.count_served_by_provider(services_df, provider)

        """
        # What is this section providing data to?  Artifact?  Remove?  Investigate this further.

        referrals_list = [
            "Referral - Support Services",
            "Referral - Support Services - Employment",
            "Referral - Support Services - Finances",
            "Referral - Support Services - RentWell"
        ]

        referred = services_df[services_df["Service Provider Specific Code"].isin(referrals_list)]
        referred_by_provider = referred[referred["Service Provide Provider"].str.contains(provider)]
        """

        in_dept = services_df[services_df["Service Provide Provider"].str.contains(provider)]
        referred_to_best = len(in_dept[
            (in_dept["Service Provider Specific Code"] == "Referral - Support Services - Finances")  | (
                in_dept["Service Provider Specific Code"] == "Referral - BEST") | (
                in_dept["Service Provider Specific Code"] == "Referral - Support Services - Employment")
        ].drop_duplicates(subset="Client Uid").index)

        if provider == "Residential":
            return tuple(["300 to employment or benefits advocacy", 300, referred_to_best])
        elif provider == "Retention":
            return tuple([
                "50% to employment or benefits advocacy",
                "50%",
                "{}/{} = {}%".format(referred_to_best, all_served, 100*(referred_to_best/all_served))
            ])
        elif provider == "ACCESS":
            return tuple(["200 to benefits advocacy", 200, referred_to_best])
        elif provider == "SSVF":
            return tuple(["200 to employment or benefits advocacy", 200, referred_to_best])
        else:
            return tuple(["X to employment or benefits advocacy", "X", referred_to_best])

    def referral_to_rw_by_provider(self, services_df, provider):
        """
        Used For: Residential CM, Retention, ACCESS, SSVF

        :param services_df:
        :param provider:
        :return:
        """
        all_served = self.count_served_by_provider(services_df, provider)
        referrals_list = [
            "Referral - Support Services",
            "Referral - Support Services - Employment",
            "Referral - Support Services - Finances",
            "Referral - Support Services - RentWell"
        ]

        referred = services_df[services_df["Service Provider Specific Code"].isin(referrals_list)]
        referred_by_provider = referred[referred["Service Provide Provider"].str.contains(provider)]
        referred_to_rent_well = len(referred_by_provider[
            referred_by_provider["Service Provider Specific Code"] == "Referral - Support Services - RentWell"
        ].drop_duplicates(subset="Client Uid").index)

        if provider == "Residential":
            return tuple(["100 to RentWell", 100, referred_to_rent_well])
        elif provider == "Retention":
            return tuple([
                "10% to RentWell",
                "10%",
                "{}/{} = {}".format(referred_to_rent_well, all_served, 100*(referred_to_rent_well/all_served))
            ])
        elif provider == "ACCESS":
            return tuple(["65 to RentWell", 65, referred_to_rent_well])
        elif provider == "SSVF":
            return tuple(["150 to RentWell", 150, referred_to_rent_well])
        else:
            return tuple(["X to RentWell", "X", referred_to_rent_well])

    def referral_to_ss_by_provider(self, services_df, provider="ACCESS"):
        """
        Used For: Outreach CM, Residential CM, Retention CM, SSVF

        :param services_df:
        :param provider:
        :return:
        """
        referrals_list = [
            "Referral - Support Services",
            "Referral - Support Services - Employment",
            "Referral - Support Services - Finances",
            "Referral - Support Services - RentWell"
        ]

        referred = services_df[services_df["Service Provider Specific Code"].isin(referrals_list)]
        referred_by_provider = referred[referred["Service Provide Provider"].str.contains(provider)]

        in_dept = services_df[services_df["Service Provide Provider"].str.contains(provider)]

        served_by_dept = len(in_dept.drop_duplicates(subset="Client Uid").index)
        referred_to_ss = len(referred_by_provider.drop_duplicates(subset="Client Uid").index)

        if provider.lower() in ["columbia", "wil", "5th", "sos", "hans"]:
            return tuple([
                "10% of participants will be connected to Supportive Services",
                "10%",
                "{}/{} = {}".format(referred_to_ss, served_by_dept, 100*(referred_to_ss / served_by_dept))
            ])
        elif (provider == "Clark Annex") or (provider == "Barbara"):
            return tuple([
                "50% of participants will be referred to Supportive Services, including:",
                "50%",
                "{}/{} = {}%".format(referred_to_ss, served_by_dept, "X")
            ])
        else:
            return tuple([
                "50% of participants will be referred to Supportive Services, including:",
                "50%",
                "{}/{} = {}%".format(referred_to_ss, served_by_dept, 100*(referred_to_ss / served_by_dept))
            ])

    def referral_to_sud_treatment_during_iap(self, entries_df, services_df, provider="IAP"):
        """
        Used For: Wellness Access

        :param entries_df:
        :param services_df:
        :param provider: Default IAP
        :return:
        """

        entries = entries_df[
            (
                entries_df["Entry Exit Provider Id"].str.contains(provider)
            )
        ]
        entries["Start"] = entries["Entry Exit Entry Date"].dt.date
        entries["End"] = entries["Entry Exit Exit Date"].dt.date
        iaps = entries[["Client Uid", "Start", "End"]]

        referral_services = "Referral - A&D Support"


        services = services_df[
            (
                # services_df["Service Provide Provider"].str.contains(provider) &
                services_df["Service Provider Specific Code"].notna() &
                services_df["Service Provider Specific Code"].str.contains(referral_services)
            )
        ]

        services["Served Date"] = services["Service Provide Start Date"].dt.date
        referred = services[["Client Uid", "Served Date"]]

        joined = pd.merge(iaps, referred, how="left", on="Client Uid")
        connected = joined[
            (joined["Start"] <= joined["Served Date"]) &
            (joined["Served Date"] <= joined["End"])
        ]
        return tuple(["600 engagements and linkages to treatment through IAP", 600, len(connected.index)])

    def res_to_perm_percent(self, entries_df, exit_type):
        """
        Used For:

        :param entries_df:
        :param exit_type:
        :return:
        """

        dp_perm, dp_temp, dp_all = self.exit_destination_by_provider(entries_df, "Doreen's", "perm temp")
        cc_perm, cc_temp, cc_all = self.exit_destination_by_provider(entries_df, "Clark Center", "perm temp")
        jp_perm, jp_temp, jp_all = self.exit_destination_by_provider(entries_df, "Jean's", "perm temp")

        total_perm = len(dp_perm.index) + len(jp_perm.index)  + len(cc_perm.index)
        total_temp = len(dp_temp.index) + len(jp_temp.index) + len(cc_temp.index)
        all_exits = len(dp_all.index) + len(jp_all.index) + len(cc_all.index)

        if exit_type == "perm":
            return tuple([
                "35% of participants will move from residential programs into permanent housing",
                "35%",
                "{}/{} = {}".format(total_perm, all_exits, 100*(total_perm/all_exits))
                ])
        elif exit_type == "temp":
            return tuple([
                "15% of participants will move from residential programs to stable housing",
                "15%",
                "{}/{} = {}".format(total_temp, all_exits, 100*(total_temp/all_exits))
            ])
        else:
            pass

    def return_chronic_list(self, entry_plus_ude_df):
        homeless = [
            "Place not meant for habitation (HUD)",
            "Emergency shelter, including hotel or motel paid for with emergency shelter voucher (HUD)",
            "Safe Haven (HUD)",
            "Interim Housing"
        ]

        data = entry_plus_ude_df

        chronic = [
            ((data["Does the client have a disabling condition?(1212)"] == "Yes (HUD)") &
            data["Residence Prior to Project Entry(43)"].isin(homeless)) &
            (
                (
                    data["Residence Prior to Project Entry(43)"].isin(homeless) &
                    (data["Length of Stay in Previous Place(1211)"] == "One year or longer (HUD)")
                ) |
                (
                    (data["Regardless of where they stayed last night - Number of times the client has been on the streets, in ES, or SH in the past three years including today(8361)"] == "Four or more times (HUD)") &
                    (data["Total number of months homeless on the street, in ES or SH in the past three years(8822)"].str.contains("12"))
                )
            )
        ]
        return chronic["Client Uid"].tolist()

    def return_poc_list(self, services_df):
        """
        Used For: Agency

        :param services_df:
        :return:
        """
        poc_race = [
            "American Indian or Alaska Native (HUD)",
            "Black or African American (HUD)",
            "Native Hawaiian or Other Pacific Islander (HUD)",
            "Other Multi-Racial",
            "Asian (HUD)"
        ]
        poc_ethnicity = ["Hispanic/Latino (HUD)"]
        poc = services_df[
            (
                (services_df["Race(895)"].isin(poc_race)) |
                (services_df["Race-Additional(1213)"].isin(poc_race)) |
                (services_df["Ethnicity (Hispanic/Latino)(896)"].isin(poc_ethnicity))
            )
        ]

        poc_de_duplicated = poc.drop_duplicates(subset="Client Uid", keep="first")

        return poc_de_duplicated["Client Uid"].tolist()

    def served_by_day_center(self, services_df):
        """
        Used For: Agency

        :param services_df:
        :return:
        """
        day_center = services_df[
            services_df["Service Provide Provider"] == "Transition Projects (TPI) - Day Center - SP(26)"
        ]

        de_duped = len(day_center.drop_duplicates(subset="Client Uid").index)
        return tuple(["7,000 participants will access day center", 7000, de_duped])

    def small_s_support_services(self, services_df):
        """
        Used For: Agency, Day Center

        Needs to be renamed to 'percent_to_small_s_support_services' then the create_sheets.py will need to be modified
        to call this method correctly again.  This is only to make the name line up with the established naming schema
        and not important in any other way.

        :param services_df:
        :return:
        """
        services_1 = [
            "Bathing Facilities",
            "Personal/Grooming Supplies",
            "Hairdressing/Nail Care"
        ]
        services_2 = [
            "Shower",
            "Showers",
            "Laundry Supplies",
            "Clothing",
            "Hairdressing/Nail Care",
            "Personal Grooming Supplies"
        ]
        services = services_df[
            ((~services_df["Service Code Description"].isin(services_1)) & (
            ~services_df["Service Provider Specific Code"].isin(services_2)))
        ]
        de_duped = len(services.drop_duplicates(subset="Client Uid", inplace=False).index)
        all_served = len(services_df.drop_duplicates(subset="Client Uid", inplace=False).index)

        return tuple([
            "50% of participants will be connected to supportive services ",
            "50%",
            "{}/{} = {}%".format(de_duped, all_served, 100*(de_duped / all_served))
        ])
