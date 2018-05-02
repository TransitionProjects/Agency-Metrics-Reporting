"""

"""

__author__ = "David Katz-Wigmore"
__version__ = ".2.3"

import create_sheets as cs
import pandas as pd
import tkinter as tk

from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename


def wait_list_open():
    file = askopenfilename()
    wait_list_path.set(file)

def service_open():
    file = askopenfilename()
    services_path.set(file)

def exclusions_open():
    file = askopenfilename()
    exclusions_path.set(file)

def entries_open():
    file = askopenfilename()
    entries_path.set(file)

def placements_open():
    file = askopenfilename()
    placements_path.set(file)

def followups_open_a():
    file = askopenfilename()
    followups_path_a.set(file)

def followups_open_res():
    file = askopenfilename()
    followups_path_res.set(file)

def followups_open_ret():
    file = askopenfilename()
    followups_path_ret.set(file)

def followups_open_acc():
    file = askopenfilename()
    followups_path_acc.set(file)

def followups_open_col():
    file = askopenfilename()
    followups_path_col.set(file)

def followups_open_han():
    file = askopenfilename()
    followups_path_han.set(file)

def followups_open_shelt():
    file = askopenfilename()
    followups_path_shelt.set(file)

def followups_open_sos():
    file = askopenfilename()
    followups_path_sos.set(file)

def followups_open_ssvf():
    file = askopenfilename()
    followups_path_ssvf.set(file)

def followups_open_will():
    file = askopenfilename()
    followups_path_will.set(file)

def followups_open_fifth():
    file = askopenfilename()
    followups_path_fifth.set(file)

def entries_hh_open():
    file = askopenfilename()
    entries_hh_path.set(file)

def entries_reason_open():
    file = askopenfilename()
    entries_plus_reason_path.set(file)

def services_need_open():
    file = askopenfilename()
    services_plus_needs_path.set(file)

def process_all():
    waitlist = wait_list_path.get()
    services = services_path.get()
    entries = entries_path.get()
    placements = placements_path.get()
    follow_ups_a = followups_path_a.get()
    follow_ups_res = followups_path_res.get()
    follow_ups_ret = followups_path_ret.get()
    follow_ups_acc = followups_path_acc.get()
    follow_ups_col = followups_path_col.get()
    follow_ups_han = followups_path_han.get()
    follow_ups_shelt = followups_path_shelt.get()
    follow_ups_sos = followups_path_sos.get()
    follow_ups_ssvf = followups_path_ssvf.get()
    follow_ups_will = followups_path_will.get()
    follow_ups_fifth = followups_path_fifth.get()
    entries_hh = entries_hh_path.get()
    entries_reason = entries_plus_reason_path.get()
    services_need = services_plus_needs_path.get()
    exclusions = exclusions_path.get()

    agency = cs.Agency(waitlist, services, entries, placements, follow_ups_a).process()
    res_cm = cs.ResidentialCM(services, entries, placements, follow_ups_res).process()
    ret_cm = cs.RetentionCM(services, entries, placements, follow_ups_ret).process()
    acc_cm = cs.OutreachCM(services, entries, placements, follow_ups_acc).process()
    ssvf_cm = cs.SSVF(services, entries, placements, follow_ups_ssvf, entries_hh).process()
    day = cs.DayCenter(services, entries, placements, follow_ups_a, exclusions).process()
    bm_ca = cs.Housing(services, entries, placements, follow_ups_a).process()
    col = cs.Columbia(services, entries, placements, follow_ups_col).process()
    will = cs.WillametteCenter(services, entries, placements, follow_ups_will).process()
    han = cs.Hansen(services, entries, placements, follow_ups_han).process()
    sos = cs.SoS(services, entries, placements, follow_ups_sos).process()
    fifth = cs.Fifth(services, entries, placements, follow_ups_fifth).process()
    severe = cs.SevereWeather(services, entries, placements, follow_ups_a).process()
    mentor = cs.Mentor(services, entries, placements, follow_ups_a).process()
    advocacy = cs.Advocacy(services, entries, placements, follow_ups_a).process()
    equity = cs.Equity(services, entries, placements, follow_ups_a).process()
    rentwell = cs.RentWell(services, entries, placements, follow_ups_a).process()
    coord = cs.CoordinatedAccess(services, entries, placements, follow_ups_a).process()
    well = cs.WellnessAccess(services_need, entries, entries_reason, placements, follow_ups_a).process()
    strat = cs.StrategicInitiative(services, entries, placements, follow_ups_a).process()
    res_shelt = cs.DPCCJP(services, entries, entries_reason, placements, follow_ups_shelt).process()

    writer = pd.ExcelWriter(asksaveasfilename(), engine="xlsxwriter")
    agency.to_excel(writer, sheet_name="Agency", index=False)
    res_cm.to_excel(writer, sheet_name="Residential CM", index=False)
    ret_cm.to_excel(writer, sheet_name="Retention CM", index=False)
    acc_cm.to_excel(writer, sheet_name="Outreach", index=False)
    ssvf_cm.to_excel(writer, sheet_name="SSVF", index=False)
    coord.to_excel(writer, sheet_name="Coordinated Access", index=False)
    day.to_excel(writer, sheet_name="Day Center", index=False)
    mentor.to_excel(writer, sheet_name="Mentor Program", index=False)
    rentwell.to_excel(writer, sheet_name="RentWell", index=False)
    well.to_excel(writer, sheet_name="Wellness Access", index=False)
    res_shelt.to_excel(writer, sheet_name="DP, JP, CC", index=False)
    bm_ca.to_excel(writer, sheet_name="BM & Annex", index=False)
    fifth.to_excel(writer, sheet_name="5th Ave.", index=False)
    col.to_excel(writer, sheet_name="Columbia", index=False)
    han.to_excel(writer, sheet_name="Hansen", index=False)
    sos.to_excel(writer, sheet_name="SoS", index=False)
    will.to_excel(writer, sheet_name="Willamette", index=False)
    severe.to_excel(writer, sheet_name="Severe Weather", index=False)
    advocacy.to_excel(writer, sheet_name="Advocacy", index=False)
    equity.to_excel(writer, sheet_name="Equity", index=False)
    strat.to_excel(writer, sheet_name="Strategic Initiative", index=False)
    writer.save()

root = tk.Tk()
root.title("Quarterly Metrics Reporting")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

wait_list_path = tk.StringVar()
services_path = tk.StringVar()
entries_path = tk.StringVar()
placements_path = tk.StringVar()
followups_path_a = tk.StringVar()
followups_path_res= tk.StringVar()
followups_path_ret = tk.StringVar()
followups_path_acc = tk.StringVar()
followups_path_col = tk.StringVar()
followups_path_han = tk.StringVar()
followups_path_shelt = tk.StringVar()
followups_path_sos = tk.StringVar()
followups_path_ssvf = tk.StringVar()
followups_path_will = tk.StringVar()
followups_path_fifth = tk.StringVar()
entries_hh_path = tk.StringVar()
entries_plus_reason_path = tk.StringVar()
services_plus_needs_path = tk.StringVar()
exclusions_path = tk.StringVar()

ttk.Label(mainframe, text="Wait-list Report:").grid(column=1, row=1, sticky="W")
ttk.Label(mainframe, text="Services Report:").grid(column=1, row=2, sticky="W")
ttk.Label(mainframe, text="Entries Report:").grid(column=1, row=3, sticky="W")
ttk.Label(mainframe, text="Placement Agency Report:").grid(column=1, row=4, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Agency Report:").grid(column=1, row=5, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Access Report:").grid(column=1, row=6, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Columbia Report:").grid(column=1, row=7, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Residential Shelter Report:").grid(column=1, row=8, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Hansen Report:").grid(column=1, row=9, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Res CM Report:").grid(column=1, row=10, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Ret CM Report:").grid(column=1, row=11, sticky="W")
ttk.Label(mainframe, text="Follow-Ups SOS Report:").grid(column=1, row=12, sticky="W")
ttk.Label(mainframe, text="Follow-Ups SSVF Report:").grid(column=1, row=13, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Willamette Report:").grid(column=1, row=14, sticky="W")
ttk.Label(mainframe, text="Follow-Ups Fifth Report:").grid(column=1, row=15, sticky="W")
ttk.Label(mainframe, text="Entries + HoH Report:").grid(column=1, row=16, sticky="W")
ttk.Label(mainframe, text="Entries + Reason Report:").grid(column=1, row=17, sticky="W")
ttk.Label(mainframe, text="Services + Need Report:").grid(column=1, row=18, sticky="W")
ttk.Label(mainframe, text="Exclusions by Provider Report:").grid(column=1, row=19, sticky="W")

ttk.Entry(mainframe, textvariable=wait_list_path, width=100).grid(column=2, row=1, sticky="E")
ttk.Entry(mainframe, textvariable=services_path, width=100).grid(column=2, row=2, sticky="E")
ttk.Entry(mainframe, textvariable=entries_path, width=100).grid(column=2, row=3, sticky="E")
ttk.Entry(mainframe, textvariable=placements_path, width=100).grid(column=2, row=4, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_a, width=100).grid(column=2, row=5, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_acc, width=100).grid(column=2, row=6, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_col, width=100).grid(column=2, row=7, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_shelt, width=100).grid(column=2, row=8, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_han, width=100).grid(column=2, row=9, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_res, width=100).grid(column=2, row=10, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_ret, width=100).grid(column=2, row=11, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_sos, width=100).grid(column=2, row=12, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_ssvf, width=100).grid(column=2, row=13, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_will, width=100).grid(column=2, row=14, sticky="E")
ttk.Entry(mainframe, textvariable=followups_path_fifth, width=100).grid(column=2, row=15, sticky="E")
ttk.Entry(mainframe, textvariable=entries_hh_path, width=100).grid(column=2, row=16, sticky="E")
ttk.Entry(mainframe, textvariable=entries_plus_reason_path, width=100).grid(column=2, row=17, sticky="E")
ttk.Entry(mainframe, textvariable=services_plus_needs_path, width=100).grid(column=2, row=18, sticky="E")
ttk.Entry(mainframe, textvariable=exclusions_path, width=100).grid(column=2, row=19, sticky="E")

ttk.Button(mainframe, text="Open", command=wait_list_open).grid(column=3, row=1, sticky="E")
ttk.Button(mainframe, text="Open", command=service_open).grid(column=3, row=2, sticky="E")
ttk.Button(mainframe, text="Open", command=entries_open).grid(column=3, row=3, sticky="E")
ttk.Button(mainframe, text="Open", command=placements_open).grid(column=3, row=4, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_a).grid(column=3, row=5, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_acc).grid(column=3, row=6, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_col).grid(column=3, row=7, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_shelt).grid(column=3, row=8, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_han).grid(column=3, row=9, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_res).grid(column=3, row=10, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_ret).grid(column=3, row=11, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_sos).grid(column=3, row=12, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_ssvf).grid(column=3, row=13, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_will).grid(column=3, row=14, sticky="E")
ttk.Button(mainframe, text="Open", command=followups_open_fifth).grid(column=3, row=15, sticky="E")
ttk.Button(mainframe, text="Open", command=entries_hh_open).grid(column=3, row=16, sticky="E")
ttk.Button(mainframe, text="Open", command=entries_reason_open).grid(column=3, row=17, sticky="E")
ttk.Button(mainframe, text="Open", command=services_need_open).grid(column=3, row=18, sticky="E")
ttk.Button(mainframe, text="Open", command=exclusions_open).grid(column=3, row=19, sticky="E")
ttk.Button(mainframe, text="Run All", command=process_all).grid(column=3, row=20, sticky="E")

root.mainloop()