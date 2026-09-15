"""
Populates timetable_entries from the IGDTUW B.Tech 1st-semester PDF.
Simplified for the hackathon demo: parallel lab-group sessions (Gp1/Gp2,
C1/C2 etc.) are collapsed to ONE representative entry per slot, so
conflict detection has a single clean weekly picture per branch instead
of every group's variant. Seeds CSE (Year 1) and Robotics and AI (Year 1)
— extend the lists below for other branches if needed.
"""
from datetime import time
from app.database import SessionLocal, engine, Base
from app.models.timetable import TimetableEntry, Weekday
from app.models.faculty import Faculty, FacultySchedule
from app.utils.faculty_parsing import parse_faculty_field, normalize_name_key

Base.metadata.create_all(bind=engine)
db = SessionLocal()

CSE_YEAR1 = [
    (Weekday.MONDAY, time(9, 0), time(11, 0), None, "BEE Lab", "Ms. Simanjali Sahoo", "E-105", True),
    (Weekday.MONDAY, time(11, 0), time(12, 0), "BCS101", "Programming with C", "Prof. Vibha Pratap", "E-212", False),
    (Weekday.MONDAY, time(12, 0), time(13, 0), "BAS101", "Applied Mathematics", "Prof Shalini Arora", "E-212", False),
    (Weekday.MONDAY, time(13, 0), time(15, 0), "BCS102", "Web Application Development", "Ms. Shilpi", "E-212", False),
    (Weekday.MONDAY, time(15, 0), time(17, 0), "BCS102", "WAD / CS Lab", "Ms. Shilpi", "E-105", True),

    (Weekday.TUESDAY, time(9, 0), time(10, 0), "BAS102", "Applied Physics", "Dr. Shweta Sharma", "E-212", False),
    (Weekday.TUESDAY, time(10, 0), time(11, 0), "BAS101", "Applied Mathematics", "Prof Shalini Arora", "E-212", False),
    (Weekday.TUESDAY, time(11, 0), time(13, 0), None, "BEE Lab", "Ms. Simanjali Sahoo", "E-105", True),
    (Weekday.TUESDAY, time(13, 0), time(15, 0), "BCS101", "Programming with C Lab", "Prof. Vibha Pratap", "E-105", True),

    (Weekday.WEDNESDAY, time(11, 0), time(13, 0), "BCS101", "Programming with C Lab", "Prof. Vibha Pratap", "E-105", True),
    (Weekday.WEDNESDAY, time(13, 0), time(14, 0), "BAS102", "Applied Physics", "Dr. Shweta Sharma", "E-212", False),
    (Weekday.WEDNESDAY, time(14, 0), time(15, 0), "BAS101", "Applied Mathematics", "Prof Shalini Arora", "E-212", False),
    (Weekday.WEDNESDAY, time(15, 0), time(17, 0), "BCS102", "WAD / CS Lab", "Ms. Shilpi", "E-105", True),

    (Weekday.THURSDAY, time(9, 0), time(10, 0), "BAS102", "Applied Physics", "Dr. Shweta Sharma", "E-212", False),
    (Weekday.THURSDAY, time(11, 0), time(13, 0), "BAS102", "Applied Physics Lab", "Prof Dinesh Ganotra", "E-201", True),
    (Weekday.THURSDAY, time(13, 0), time(15, 0), "BCS101", "Programming with C", "Prof. Vibha Pratap", "E-212", False),

    (Weekday.FRIDAY, time(9, 0), time(11, 0), "BAS102", "Applied Physics Lab", "Prof Dinesh Ganotra", "E-201", True),
    (Weekday.FRIDAY, time(12, 0), time(13, 0), "BAS101", "Applied Mathematics", "Prof Shalini Arora", "E-212", False),
    (Weekday.FRIDAY, time(13, 0), time(14, 0), "BCS101", "Programming with C", "Prof. Vibha Pratap", "E-212", False),
    (Weekday.FRIDAY, time(14, 0), time(15, 0), None, "BEE", "Ms. Simanjali Sahoo", "E-212", False),
]

RAIE_YEAR1 =[
    (Weekday.TUESDAY, time(9, 0), time(10, 0), "BAS-103", "Probability and Statistics", "Km. Ranjana", "LH-05", False),
    (Weekday.TUESDAY, time(11, 0), time(13, 0), "BMA103", "Engineering Mechanics Lab", "Prof. N.R. Chauhan", "M-105A", True),
    (Weekday.TUESDAY, time(13, 0), time(15, 0), "BMA112", "Computer Aided Engineering Graphics", "Prof. N.R. Chauhan", "M-108", True),
    (Weekday.TUESDAY, time(15, 0), time(17, 0), "BMA112", "Computer Aided Engineering Graphics", "Prof. N.R. Chauhan", "M-108", True),

    (Weekday.WEDNESDAY, time(10, 0), time(11, 0), "BAS104", "Environmental Sciences", "Dr Sanjeev", "LH-05", False),
    (Weekday.WEDNESDAY, time(11, 0), time(13, 0), "BMA103", "Engineering Mechanics", "Prof. N.R. Chauhan", "LH-05", False),
    (Weekday.WEDNESDAY, time(13, 0), time(15, 0), "BMA112", "Computer Aided Engineering Graphics", "Prof. N.R. Chauhan", "LH-05", True),
    (Weekday.WEDNESDAY, time(15, 0), time(16, 0), "BAS-103", "Probability and Statistics", "Km. Ranjana", "LH-05", False),

    (Weekday.THURSDAY, time(12, 0), time(13, 0), "BMA103", "Engineering Mechanics", "Prof. N.R. Chauhan", "LH-05", False),
    (Weekday.THURSDAY, time(13, 0), time(14, 0), "BEC101", "Basics Electrical Engineering", "Dr Abhay Krishan", "LH-05", False),
    (Weekday.THURSDAY, time(15, 0), time(16, 0), "BMA112", "Computer Aided Engineering Graphics", "Prof. N.R. Chauhan", "LH-05", True),

    (Weekday.FRIDAY, time(9, 0), time(11, 0), "BEC101", "Basics Electrical Engineering Lab", "Dr Abhay Krishan", "LH-05", True),
    (Weekday.FRIDAY, time(13, 0), time(14, 0), "BMA112", "Computer Aided Engineering Graphics", "Prof. N.R. Chauhan", "LH-05", False),
    (Weekday.FRIDAY, time(15, 0), time(17, 0), "BMA103", "Engineering Mechanics Lab", "Prof. N.R. Chauhan", "M-105A", True),

    (Weekday.SATURDAY, time(9, 0), time(11, 0), "BAS104", "Environmental Sciences Lab", "Dr Sanjeev", "C-113", True),
    (Weekday.SATURDAY, time(11, 0), time(12, 0), "BAS104", "Environmental Sciences", "Dr Sanjeev", "LH-05", False),
    (Weekday.SATURDAY, time(13, 0), time(15, 0), "BAS104", "Environmental Sciences Lab", "Dr Sanjeev", "C-113", True),
    (Weekday.SATURDAY, time(15, 0), time(17, 0), "HMC-101", "Communication Skills", "Dr Prachi Behrani", "LH-05", False),
]
# --- ECE (Year 1) ---
# Source: "B.Tech ECE First Semester (2026-2027)" table.
# NOTE: THUR and FRI rows in the source PDF use overlapping/spanning cells
# (parallel group labs shown two-per-cell, e.g. "FES LAB GP2" + "EW LAB GP1"
# in the same slot) that cannot be confidently split into single time
# ranges from the extracted text — those two days are intentionally NOT
# seeded. MON/TUES/WED below only include slots where the number of listed
# items cleanly divides the 8 time columns.
ECE_YEAR1 = [
    (Weekday.MONDAY, time(9, 0), time(11, 0), "BAI104", "Programming Fundamentals Lab GP1", "Ms. Shreya Biswas", "E109 A ECE Block", True),
    (Weekday.MONDAY, time(11, 0), time(12, 0), "BEC103", "Electronics Workshop (EW)", "Ms. Khushboo and Ms Trapti", "E307", False),
    (Weekday.MONDAY, time(12, 0), time(13, 0), "BAS101", "Applied Mathematics", "Prof Jyoti Sinha", "E307", False),
    (Weekday.MONDAY, time(13, 0), time(14, 0), "BAI104", "Programming Fundamentals (PF)", "Ms. Shreya Biswas", "E-308 ECE Block II Floor", False),
    (Weekday.MONDAY, time(14, 0), time(15, 0), "BAI104", "Programming Fundamentals (PF)", "Ms. Shreya Biswas", "E307", False),
    (Weekday.MONDAY, time(15, 0), time(17, 0), "BEC-102", "Signals & Systems (SS)", "Ms Astha Sharma", "E307", False),

    (Weekday.TUESDAY, time(9, 0), time(11, 0), None, "Communication Skills (CS) Lab GP2", "Mr Priyank", "106 Old Sciences Block", True),
    (Weekday.TUESDAY, time(11, 0), time(12, 0), "HMC-110", "Communication Skills (CS)", "Mr Priyank", "E-308 ECE Block II Floor", False),
    (Weekday.TUESDAY, time(13, 0), time(14, 0), "BEC103", "Electronics Workshop (EW)", "Ms. Khushboo and Ms Trapti", "E-308 ECE Block II Floor", False),
    (Weekday.TUESDAY, time(15, 0), time(17, 0), "BEC105", "Fundamentals of Electrical Sciences (FES) Lab GP1", "Prof Pankaj Gupta", "E210 ECE Block", True),

    (Weekday.WEDNESDAY, time(9, 0), time(11, 0), "BEC-102", "Signals & Systems (SS) Lab GP1", "Ms Astha Sharma", "E109 A ECE Block", True),
    (Weekday.WEDNESDAY, time(11, 0), time(13, 0), "BAI104", "Programming Fundamentals (PF) Lab GP2", "Ms. Shreya Biswas", "E109 A ECE Block", True),
    (Weekday.WEDNESDAY, time(13, 0), time(14, 0), "HMC-110", "Communication Skills (CS)", "Mr Priyank", "E-308 ECE Block II Floor", False),
    (Weekday.WEDNESDAY, time(14, 0), time(15, 0), "BAS101", "Applied Mathematics", "Prof Jyoti Sinha", "E-308 ECE Block II Floor", False),
]

# --- MAE (I) Year 1 ---
# Source: "B.Tech MAE (I) First Semester (2026-2027)" table.
# NOTE: MON, WED, THUR, FRI rows use two-line/overlapping cells (e.g. a
# "WP GP2" line stacked with "CS LAB GP2" in what looks like one slot,
# LUNCH position shifting per day) that don't cleanly resolve to single
# time ranges from the extracted text. Only TUESDAY is unambiguous.
MAE_YEAR1 = [
    (Weekday.TUESDAY, time(9, 0), time(11, 0), "BAI-104", "Programming Fundamentals Lab GP1", "Ms. Manju Kumari", "M-205 (CAD Lab) MAE Block I Floor", True),
    (Weekday.TUESDAY, time(11, 0), time(12, 0), "BMA 107", "WP: Workshop Practice", "Dr. Tina Chaudhary", "M-201 MAE Block I Floor", False),
    (Weekday.TUESDAY, time(13, 0), time(14, 0), "BAS104", "Applied Physics", "Dr Renu Kumari", "M-201 MAE Block I Floor", False),
    (Weekday.TUESDAY, time(15, 0), time(17, 0), "BAS101", "Applied Mathematics", "Dr Neha", "M-201 MAE Block I Floor", False),
]

# --- IT (Year 1, Section 1 — from "B.Tech IT-1 First Semester") ---
# NOTE: MON row is ambiguous (spanning cells). Only TUESDAY is unambiguous.
# IT-2 (Section 2) grid is too ambiguous across all days in this pass —
# not seeded at all; see note to user.
IT_YEAR1_SECTION1 = [
    (Weekday.TUESDAY, time(9, 0), time(10, 0), "BAS102", "Applied Physics", "Dr Ravinder Pal", "Room No. 211 IT Block Second Floor", False),
    (Weekday.TUESDAY, time(10, 0), time(12, 0), "BAS102", "Applied Physics Lab GP2", "Prof. Chhaya Ravi Kant & Ms Soumya Rai", "E-201, ECE Block First Floor", True),
    (Weekday.TUESDAY, time(13, 0), time(14, 0), "BAS101", "Applied Mathematics", "Dr. Jyoti", "Room No. 211 IT Block Second Floor", False),
    (Weekday.TUESDAY, time(15, 0), time(17, 0), "BAI104", "Programming with Python Lab Gr. 2", "Prof. Arun Sharma", "Software Engineering Lab IT-209", True),
]
# ============================================================
# AI-ML — Year 1
# ============================================================

AI_ML_YEAR1 = [

    # MON
    ("MON", "09:00", "10:00", "HMC-101",
     "Communication Skills (CS)", "Ms Palak Dawar",
     "IT Block-104", False),

    ("MON", "10:00", "11:00", "BAI-101",
     "Programming with Python", "Dr Anoop Giridhar",
     "IT Block-104", False),

    ("MON", "11:00", "13:00", "BAI-101 / BCS-102",
     "Programming with python (AI/ML) LAB Gr. 2 / "
     "Web Application Development Lab Gr. 1 (AI/ML)",
     "Dr Anoop Giridhar / Dr Mohana Ghosh",
     "IT-301 / IT-212", True),

    ("MON", "13:00", "15:00", "BAS-104",
     "Environmental Sciences Lab GP1",
     "Prof Ranu Gadi & Ms Khushbu",
     "C-113 IT Block Ground Floor", True),

    ("MON", "15:00", "16:00", "BAS-104",
     "Environmental Sciences Lab GP2",
     "Prof Ranu Gadi & Ms Khushbu",
     "C-113 IT Block Ground Floor", True),

    ("MON", "16:00", "17:00", "BAI102",
     "IT Workshop Lab Gp1",
     "Ms Pooja Jamar",
     "Cyber Security Lab IT 213 IT Block II floor", True),


    # TUES
    ("TUES", "09:00", "10:00", "HMC-101",
     "Communication Skills (CS)", "Ms Palak Dawar",
     "IT Block-104", False),

    ("TUES", "10:00", "12:00", "BAI-101",
     "Programming with Python", "Dr Anoop Giridhar",
     "IT Block-104", False),

    ("TUES", "12:00", "14:00", "BAS-104",
     "Environmental Sciences", "Prof Ranu Gadi",
     "IT Block-104", False),

    ("TUES", "15:00", "17:00", "BAS-103 / HMC-101",
     "Probability and Statistics Gr. 1 / Communication Skills G2",
     "Ms Sarita & Ms Amisha / Ms Palak Dawar, Ms Shikha Singh",
     "IT301 / IT310", True),


    # WED
    ("WED", "09:00", "11:00", "BAS-103 / HMC-101",
     "Probability and Statistics Gr. 2 / Communication Skills G1",
     "Ms Manisha & Ms Mansi / Ms Palak Dawar, Ms Shikha Singh",
     "IT401 / IT209", True),

    ("WED", "11:00", "13:00", "BAI102",
     "IT Workshop", "Ms Jaya Yadav",
     "IT Block-104", False),


    # THUR
    ("THUR", "09:00", "11:00", "BAI102",
     "IT Workshop Lab Gp2",
     "Ms Divya",
     "Cyber Security Lab IT 213 IT Block II floor", True),

    ("THUR", "11:00", "13:00", "BAI-101 / BCS-102",
     "Programming with Python Lab Gr. 1 / "
     "Web Application Development Lab Gr. 2",
     "Dr Anoop Giridhar / Dr Mohana Ghosh",
     "IT310 / IT212", True),

    ("THUR", "13:00", "15:00", "BAS-103",
     "Probability and Statistics (PS)",
     "Mr Navin Kumar Sharma",
     "E308", False),


    # FRI
    ("FRI", "09:00", "11:00", "BCS-102",
     "Web Application Development", "Dr Shweta a",
     "IT Block-104", False),

    ("FRI", "11:00", "12:00", "BAS-104",
     "Environmental Sciences", "Prof Ranu Gadi",
     "IT Block-104", False),

    ("FRI", "13:00", "14:00", "BAS-103",
     "Probability and Statistics (PS)",
     "Mr Navin Kumar Sharma",
     "E308", False),
]

# ============================================================
# CSE-AI — Year 1 — Section I
# ============================================================

CSE_AI_I_YEAR1 = [

    ("MON", "10:00", "11:00", "BAS-104",
     "Environmental Sciences", "Dr Shuchi", "LH-04 New Building", False),

    ("MON", "11:00", "13:00", "BAI-102",
     "IT Workshop Lab", "Ms Ashish Dabbas",
     "Computer Centre", True),

    ("MON", "13:00", "15:00", "BAI-102",
     "IT Workshop", "Ms Ashish Dabbas",
     "LH-04 New Building", False),

    ("MON", "15:00", "17:00", "BEC101",
     "Basics of Electrical and Electronics Engineering Lab",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("TUES", "09:00", "10:00", "BAS-103",
     "Probability and Statistics (PS)", "Dr. Kanchan Jangra",
     "E308", False),

    ("TUES", "10:00", "11:00", "HMC-101",
     "Communication Skills (CS)", "Dr Bhavya",
     "LH-04 New Building", False),

    ("TUES", "11:00", "13:00", "HMC-101",
     "Communication Skills Lab G2",
     "Dr Bhavya and Ms Shambhavi",
     "106 Old Sciences Block", True),

    ("TUES", "13:00", "15:00", "BAI-101",
     "Programming with Python (PP)", "Dr. D.K. Dhir",
     "LH-04 New Building", False),

    ("TUES", "15:00", "17:00", "BAS-103",
     "Probability and Statistics Lab",
     "Prof. Shalini Arora & Ms. Sakshi Dhruv / "
     "Prof. Shalini Arora & Ms. Aastha Jain",
     "Computer Centre", True),

    ("WED", "09:00", "10:00", "BAI-102",
     "IT Workshop (ITW)", "Ms. Ashish Dabbas",
     "LH-04 New Building", False),

    ("WED", "10:00", "11:00", "HMC-101",
     "Communication Skills (CS)", "Dr Bhavya",
     "LH-04 New Building", False),

    ("WED", "11:00", "13:00", "BEC101",
     "Basics of Electrical and Electronics Engineering Lab",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("WED", "13:00", "14:00", "BAI-101",
     "Programming with Python (PP)", "Dr. D.K. Dhir",
     "LH-04 New Building", False),

    ("WED", "14:00", "15:00", "BAS-104",
     "Environmental Sciences", "Dr Shuchi",
     "LH-04 New Building", False),

    ("WED", "15:00", "17:00", "BAI-101",
     "Programming with Python (PP) Lab",
     "Dr. D.K. Dhir",
     "Computer Centre", True),

    ("THUR", "09:00", "11:00", "BAS-104",
     "Environmental Sciences Lab GP1",
     "Prof Ranu Gadi / Dr Shuchi / Dr Tripti",
     "C-113 IT Block Ground Floor", True),

    ("THUR", "11:00", "13:00", "HMC-101",
     "Communication Skills Lab GP1",
     "Dr Bhavya and Ms Shambhavi",
     "106 Old Sciences Block", True),

    ("THUR", "11:00", "13:00", "BAS-104",
     "Environmental Sciences Lab GP2",
     "Prof Ranu Gadi / Ms Khushbu",
     "C-113 IT Block Ground Floor", True),

    ("FRI", "09:00", "11:00", "BAI-101",
     "Programming with Python Lab",
     "Dr. D.K. Dhir",
     "Computer Centre", True),

    ("FRI", "11:00", "12:00", "BEC101",
     "Basics of Electrical and Electronics Engineering",
     "Ms. B. Jyothi",
     "IT312", False),

    ("FRI", "13:00", "14:00", "BAS-103",
     "Probability and Statistics (PS)", "Dr. Kanchan Jangra",
     "LH-04 New Building", False),
]

# ============================================================
# CSE-AI — Year 1 — Section II
# ============================================================

CSE_AI_II_YEAR1 = [

    ("MON", "09:00", "11:00", "BAS-103",
     "Probability and Statistics Lab",
     "Prof. Shalini Arora & Ms. Sarita GP1 / "
     "Dr. Geeta Sachdev & Ms. Sakshi Dhruv GP2",
     "Room No. Computer Centre Ground floor", True),

    ("MON", "11:00", "13:00", "BAS-104 / HMC-101",
     "Environmental Sciences Lab GP2 & Communication Skills Lab G1",
     "Prof Ranu Gadi Ms Khushbu / Dr Bhavya and Ms Niharkana Dhar",
     "C-113 IT Block Ground Floor / 106 Old Sciences Block", True),

    ("MON", "14:00", "16:00", "BAS-103",
     "Probability and Statistics (PS)", "Dr. Kanchan Jangra",
     "LH-04 New Building", False),

    ("MON", "16:00", "17:00", "HMC-101",
     "Communication Skills (CS)", "Ms Niharkana Dhar",
     "LH-04 New Building", False),

    ("TUES", "09:00", "10:00", "HMC-101",
     "Communication Skills (CS)", "Ms Niharkana Dhar",
     "LH-04 New Building", False),

    ("TUES", "11:00", "12:00", "BAS-103",
     "Probability and Statistics (PS)", "Dr. Kanchan Jangra",
     "LH-04 New Building", False),

    ("TUES", "12:00", "13:00", "BAI-110",
     "Programming with Python (PWP)", "Dr. D.K. Dhir",
     "LH-04 New Building", False),

    ("TUES", "13:00", "15:00", "HMC-101",
     "Communication Skills Lab GP2",
     "Dr Bhavya and Ms Niharkana Dhar",
     "106 Old Sciences Block", True),

    ("TUES", "15:00", "17:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering (BEEE)",
     "Ms. B. Jyothi",
     "LH-04 New Building", False),

    ("WED", "09:00", "11:00", "BAS-104",
     "Environmental Sciences Lab GP1",
     "Dr Sweety / Ms Aarshiya",
     "C-113 IT Block Ground Floor", True),

    ("WED", "11:00", "13:00", "BAI-108",
     "Information Technology Workshop (ITW)",
     "Ms. Ashish Dabbas",
     "LH-04 New Building", False),

    ("WED", "13:00", "15:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering Lab GP1",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("WED", "15:00", "17:00", "BAI-108",
     "Information Technology Workshop (ITW) Lab",
     "Ms. Ashish Dabbas",
     "Room No. Computer Centre Ground floor", True),

    ("THUR", "09:00", "10:00", "BAS-104",
     "Environmental Sciences", "Dr Saurav Kumar",
     "LH-04 New Building", False),

    ("THUR", "10:00", "11:00", "BAI-110",
     "Programming with Python (PWP)", "Dr. D.K. Dhir",
     "LH-04 New Building", False),

    ("THUR", "11:00", "13:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering Lab GP2",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("THUR", "13:00", "15:00", "BAI-110",
     "Programming with Python (PWP) Lab",
     "Dr. D.K. Dhir",
     "Room No. Computer Centre Ground floor", True),

    ("FRI", "12:00", "13:00", "BAI-110",
     "Programming with Python (PWP)", "Dr. D.K. Dhir",
     "LH-04 New Building", False),

    ("FRI", "13:00", "15:00", "BAS-104",
     "Environmental Sciences", "Dr Saurav Kumar",
     "LH-04 New Building", False),
]

# ============================================================
# CSE-AI — Year 1 — Section III
# ============================================================

CSE_AI_III_YEAR1 = [

    ("MON", "10:00", "11:00", "BAI-110",
     "Programming with Python (PWP)", "Dr. D.K. Dhir",
     "LH-05 New Building", False),

    ("MON", "11:00", "13:00", "BAS-103",
     "Probability and Statistics (PS)", "Km. Ranjana",
     "LH-05 New Building", False),

    ("MON", "13:00", "15:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering Lab GP1",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("TUES", "10:00", "11:00", "BAS-103",
     "Probability and Statistics (PS)", "Km. Ranjana",
     "LH-05 New Building", False),

    ("TUES", "11:00", "13:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering",
     "Ms. B. Jyothi",
     "IT312", False),

    ("TUES", "13:00", "15:00", "BEC-101",
     "Basics of Electrical and Electronics Engineering Lab GP2",
     "Ms. B. Jyothi, Ms Swati Rawat",
     "E-210, CSE Block First Floor", True),

    ("TUES", "15:00", "17:00", "BAI-108",
     "Information Technology Workshop (ITW) Lab",
     "Ms. Ashish Dabbas",
     "Room No. Computer Centre Ground floor", True),

    ("WED", "09:00", "11:00", "BAS-104",
     "Environmental Sciences", "Dr Dheeraj",
     "E309", False),

    ("WED", "11:00", "13:00", "BAS-104",
     "Environmental Sciences Lab GP1",
     "Dr Sanjeev / Dr Dheeraj / Ms Aarshiya / Dr Neeru",
     "C-113 IT Block Ground Floor", True),

    ("WED", "13:00", "15:00", "HMC-101",
     "Communication Skills Lab G2",
     "Dr Bhavya and Ms Mallika Katoch",
     "106 Old Sciences Block", True),

    ("WED", "15:00", "17:00", "BAI-110",
     "Programming with Python (PWP) Lab",
     "Dr. D.K. Dhir",
     "Room No. Computer Centre Ground floor", True),

    ("THUR", "09:00", "10:00", "BAS-104",
     "Environmental Sciences", "Dr Dheeraj",
     "LH-05 New Building", False),

    ("THUR", "10:00", "11:00", "HMC-101",
     "Communication Skills (CS)", "Dr Bhavya",
     "LH-05 New Building", False),

    ("THUR", "11:00", "13:00", "BAI-110",
     "Programming with Python (PWP)", "Dr. D.K. Dhir",
     "LH-05 New Building", False),

    ("THUR", "13:00", "15:00", "HMC-101",
     "Communication Skills Lab G1",
     "Dr Bhavya and Ms Mallika Katoch",
     "106 Old Sciences Block", True),

    ("THUR", "15:00", "16:00", "BAI-108",
     "Information Technology Workshop (ITW)",
     "Ms. Ashish Dabbas",
     "LH-05 New Building", False),

    ("FRI", "09:00", "11:00", "BAS-104",
     "Environmental Sciences Lab GP2",
     "Dr Sanjeev / Dr Dheeraj / Ms Aarshiya / Dr Neeru",
     "C-113 IT Block Ground Floor", True),

    ("FRI", "13:00", "14:00", "HMC-101",
     "Communication Skills (CS)", "Dr Bhavya",
     "LH-05 New Building", False),

    ("FRI", "15:00", "17:00", "BAS-103",
     "Probability and Statistics Lab",
     "Dr. Geeta Sachdev & Ms. Manisha / "
     "Dr. Geeta Sachdev & Ms. Mansi",
     "Computer Centre Ground floor", True),
]

# ============================================================
# ECE-AI — Year 1 — Section I
# ============================================================

ECE_AI_I_YEAR1 = [

    ("MON", "09:00", "10:00", "BAI-104",
     "Programming Fundamentals (PF)", "Ms Jaya Yadav",
     "E213 ECE Block First Floor", False),

    ("MON", "10:00", "11:00", "BAS-101",
     "Applied Mathematics", "Dr Rohit Narang",
     "E213 ECE Block First Floor", False),

    ("MON", "13:00", "15:00", "BEC-103",
     "Electronics Workshop (EW)", "Ms Khushbu Mall",
     "E213 ECE Block First Floor", False),

    ("MON", "15:00", "17:00", "BAI-104",
     "Programming Fundamentals (PF) Lab GP1",
     "Ms Jaya Yadav", "E109 ECE Block", True),

    ("TUES", "09:00", "11:00", "BAS-101",
     "Applied Mathematics", "Dr Rohit Narang",
     "E213 ECE Block First Floor", False),

    ("TUES", "12:00", "13:00", "BAI-104",
     "Programming Fundamentals (PF)", "Ms Jaya Yadav",
     "E213 ECE Block First Floor", False),

    ("TUES", "13:00", "14:00", "HMC-101",
     "Communication Skills (CS)", "Ms Palak Dawar",
     "E307", False),

    ("TUES", "14:00", "15:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("TUES", "15:00", "17:00", "BEC-103",
     "Electronics Workshop (EW) Lab GP1",
     "Ms Khushbu Mall", "E315 ECE Block", True),

    ("WED", "09:00", "11:00", "BAI-104",
     "Programming Fundamentals (PF) Lab GP2",
     "Ms Jaya Yadav", "E106", True),

    ("WED", "11:00", "13:00", "HMC-101",
     "Communication Skills Lab GP2",
     "Ms Palak Dawar / Ms Shambhavi",
     "106 Old Sciences Block", True),

    ("WED", "15:00", "17:00", "BEC-102 / BEC-103",
     "Signals & Systems Lab GP1 / Electronics Workshop Lab GP2",
     "Ms Surbhi Bharti / Ms Khushbu Mall",
     "E109A / E315 ECE Block", True),

    ("THUR", "09:00", "11:00", "HMC-101",
     "Communication Skills Lab GP1",
     "Ms Palak Dawar / Ms Anjali",
     "106 Old Sciences Block", True),

    ("THUR", "11:00", "12:00", "HMC-101",
     "Communication Skills (CS)", "Ms Palak Dawar",
     "E213 ECE Block First Floor", False),

    ("THUR", "12:00", "13:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("THUR", "15:00", "16:00", "BEC-102",
     "Signals & Systems (SS)", "Ms Surbhi Bharti",
     "E307", False),

    ("FRI", "09:00", "11:00", "BEC-105",
     "Fundamentals of Electrical Sciences Lab GP2",
     "Prof Ashwani Kumar / Prof Maria Jamal",
     "E210 ECE Block", True),

    ("FRI", "11:00", "12:00", "BAS-101",
     "Applied Mathematics", "Dr Rohit Narang",
     "E213 ECE Block First Floor", False),

    ("FRI", "12:00", "13:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("FRI", "13:00", "15:00", "BEC-102",
     "Signals & Systems (SS)", "Ms Surbhi Bharti",
     "E307", False),

    ("FRI", "15:00", "17:00", "BEC-105 / BEC-102",
     "Fundamentals of Electrical Sciences Lab GP1 / "
     "Signals & Systems Lab GP2",
     "Prof Maria Jamal / Ms Surbhi Bharti",
     "E210 / E106", True),
]

# ============================================================
# ECE-AI — Year 1 — Section II
# ============================================================

ECE_AI_II_YEAR1 = [

    ("MON", "09:00", "11:00", "HMC-101",
     "Communication Skills Lab GP1",
     "Ms Shivangi Tiwary / Ms Afrida M",
     "106 Old Sciences Block", True),

    ("MON", "11:00", "12:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("MON", "12:00", "13:00", "HMC-101",
     "Communication Skills (CS)", "Ms Shivangi Tiwary",
     "E213 ECE Block First Floor", False),

    ("MON", "15:00", "17:00", "BEC-102",
     "Signals & Systems Lab GP2",
     "Dr Ejaz Lodhi", "E109A ECE Block", True),

    ("TUES", "09:00", "11:00", "BEC-105",
     "Fundamentals of Electrical Sciences Lab GP2",
     "Prof Maria Jamal", "E210 ECE Block", True),

    ("TUES", "11:00", "12:00", "BAS-101",
     "Applied Mathematics", "Dr. Aditi Garg",
     "E213 ECE Block First Floor", False),

    ("TUES", "12:00", "14:00", "BAI-104",
     "Programming Fundamentals Lab GP1",
     "Ms. Shikha Kuchal", "E106", True),

    ("TUES", "14:00", "15:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E307", False),

    ("TUES", "15:00", "17:00", "BAI-104",
     "Programming Fundamentals Lab GP2",
     "Ms. Shikha Kuchal", "E106", True),

    ("WED", "09:00", "11:00", "BEC-103",
     "Electronics Workshop Lab GP1", "Ms Trapti",
     "E315 ECE Block", True),

    ("WED", "11:00", "12:00", "HMC-101",
     "Communication Skills (CS)", "Ms Shivangi Tiwary",
     "E213 ECE Block First Floor", False),

    ("WED", "12:00", "13:00", "BEC-102",
     "Signals & Systems (SS)", "Ms Surbhi Bharti",
     "E213 ECE Block First Floor", False),

    ("WED", "13:00", "15:00", "BEC-102",
     "Signals & Systems Lab GP1",
     "Ms Surbhi Bharti", "E109A ECE Block", True),

    ("WED", "15:00", "17:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("THUR", "09:00", "11:00", "BAI-104",
     "Programming Fundamentals (PF)", "Ms. Shikha Kuchal",
     "E315 ECE Block Second Floor", False),

    ("THUR", "11:00", "13:00", "BAS-101",
     "Applied Mathematics", "Dr. Aditi Garg",
     "E213 ECE Block First Floor", False),

    ("THUR", "13:00", "15:00", "BEC-102",
     "Signals & Systems (SS)", "Ms Surbhi Bharti",
     "E213 ECE Block First Floor", False),

    ("THUR", "15:00", "17:00", "BEC-105",
     "Fundamentals of Electrical Sciences Lab GP1",
     "Prof Maria Jamal", "E210 ECE Block", True),

    ("FRI", "10:00", "11:00", "BEC-105",
     "Fundamentals of Electrical Sciences (FES)",
     "Prof Maria Jamal", "E213 ECE Block First Floor", False),

    ("FRI", "12:00", "13:00", "BAS-101",
     "Applied Mathematics", "Dr. Aditi Garg",
     "E307", False),

    ("FRI", "13:00", "15:00", "BEC-103",
     "Electronics Workshop (EW)", "Ms Trapti",
     "E213 ECE Block First Floor", False),

    ("FRI", "15:00", "17:00", "BEC-103",
     "Electronics Workshop Lab GP2", "Ms Trapti",
     "E315 ECE Block", True),
]

# ============================================================
# MAC — Year 1
# ============================================================

MAC_YEAR1 = [

    # MON
    ("MON", "09:00", "11:00", "BAS-104",
     "Environmental Science Lab GP2",
     "Dr Bhumika / Ms Aarshiya",
     "C-114 EVS Lab IT Ground Floor", True),

    ("MON", "12:00", "14:00", "BEC101",
     "Basics of Electrical Engineering",
     "Mr Basant Tomar", "E-206 CSE Block First Floor", False),

    ("MON", "14:00", "15:00", "BAS-",
     "Calculus", "Dr Geeta Sachdev",
     "E-206 CSE Block First Floor", False),

    ("MON", "15:00", "17:00", "BCS102",
     "WebApplicationDevelopment Lab MAC GP2",
     "Dr. Mohit Ghai",
     "Networking Lab", True),


    # TUES
    ("TUES", "09:00", "11:00", "BAS-104",
     "Environmental Science Lab GP1",
     "Dr Tripti / Dr Bhumika",
     "C-114 EVS Lab IT Ground Floor", True),

    ("TUES", "11:00", "12:00", "BAS-",
     "Calculus", "Dr Geeta Sachdev",
     "E-206 CSE Block First Floor", False),

    ("TUES", "12:00", "14:00", "BCS101",
     "Programming in C Lab (MAC) GP1",
     "Ms. Priyanka Jain",
     "ML DL Lab", True),

    ("TUES", "14:00", "16:00", "HMC101",
     "Communication Skills Lab GP2",
     "Mr Priyank / Ms Anjali",
     "106 Old Sciences Block", True),

    ("TUES", "16:00", "17:00", "BCS102",
     "WebApplicationDevelopment Lab MAC GP1",
     "Dr. Mohit Ghai / Vanshika Nailwal",
     "Networking Lab", True),


    # WED
    ("WED", "09:00", "11:00", "BEC101",
     "Basics Electrical Engineering Lab GP1",
     "Mr Basant Tomar", "E-210, CSE Block First Floor", True),

    ("WED", "11:00", "12:00", "BAS-",
     "Calculus", "Dr Geeta Sachdev",
     "E-206 CSE Block First Floor", False),

    ("WED", "12:00", "13:00", "BAS-104",
     "Environmental Science", "Dr Sweety",
     "E-206 CSE Block First Floor", False),

    ("WED", "13:00", "15:00", "BCS101",
     "Programming in C Lab (MAC) GP2",
     "Ms. Priyanka Jain",
     "DBMS Lab", True),

    ("WED", "15:00", "17:00", "HMC101",
     "Communication Skills (CS)",
     "Mr Priyank", "E212", False),


    # THUR
    ("THUR", "10:00", "11:00", "BCS101",
     "Programming in C", "Ms. Priyanka Jain",
     "E-206 CSE Block First Floor", False),

    ("THUR", "11:00", "12:00", "BAS-",
     "Calculus", "Dr Geeta Sachdev",
     "E-206 CSE Block First Floor", False),

    ("THUR", "12:00", "13:00", "BCS102",
     "WebApplication Development", "Dr. Mohit Ghai",
     "E-206 CSE Block First Floor", False),

    ("THUR", "14:00", "16:00", "BAS-104",
     "Environmental Science", "Dr Sweety",
     "E306", False),


    # FRI
    ("FRI", "09:00", "11:00", "BCS101",
     "Programming in C", "Ms. Priyanka Jain",
     "E-206 CSE Block First Floor", False),

    ("FRI", "11:00", "13:00", "HMC101 / BEC101",
     "Communication Skills Lab GP1 / "
     "Basics Electrical Engineering Lab GP2",
     "Mr Priyank, Dr Mitali Bhattacharya / Mr Basant Tomar",
     "106 Old Sciences Block / E-210 CSE Block First Floor", True),

    ("FRI", "13:00", "15:00", "BEC101",
     "Basics Electrical Engineering Lab GP1",
     "Mr Basant Tomar",
     "E-210, CSE Block First Floor", True),
]

# ============================================================
# Cyber Security — Year 1
# ============================================================

CYBER_SECURITY_YEAR1 = [

    # TUES
    ("TUES", "09:00", "11:00", "BAI-101 / BCS-102",
     "Programming with python (CS) LAB Gr. 1 / "
     "Web Application development Lab Gr. 2 (CS)",
     "Ms. Shrestha (JRF) / Ms Deepshikha Kashayap",
     "IT Block / IT-212", True),

    ("TUES", "13:00", "14:00", "BAI102",
     "IT Workshop", "Ms Ruchi Bhatt",
     "IT Block-305", False),


    # WED
    ("WED", "09:00", "11:00", "BAI102 / BAS-103",
     "IT Workshop LAB Gr. 1 / Probability and Statistics "
     "(CS) 1st year, Gr. 2",
     "Ms Ruchi Bhatt / Dr Rohit Narang & Ms Astha F",
     "IT-301 / IT Block", True),

    ("WED", "11:00", "13:00", "BAS-103",
     "Probability and Statistics (PS)",
     "Prof Jyoti Sinha",
     "IT Block-305", False),

    ("WED", "13:00", "14:00", "BAI-101",
     "Programming with Python",
     "Dr Pratibha Agarwal",
     "IT Block-305", False),


    # THUR
    ("THUR", "09:00", "11:00", "BAI-101",
     "Programming with Python",
     "Dr Pratibha Agarwal",
     "IT Block-305", False),

    ("THUR", "12:00", "13:00", "BAI102",
     "IT Workshop", "Ms Ruchi Bhatt",
     "IT Block-305", False),

    ("THUR", "13:00", "14:00", "BAS-103",
     "Probability and Statistics (PS)",
     "Prof Jyoti Sinha",
     "IT Block-305", False),

    ("THUR", "15:00", "17:00", "BAI-101 / BCS-102",
     "Programming with python (CS) LAB Gr. 2 / "
     "Web Application development Lab Gr. 1 (CS)",
     "Ms. Shrestha (JRF) / Ms Deepshikha Kashayap",
     "IT-209 / IT-301", True),


    # FRI
    ("FRI", "09:00", "10:00", "BAS104",
     "Environmental Sciences", "Dr Maruf",
     "IT Block-305", False),

    ("FRI", "13:00", "14:00", "BCS-102",
     "Web Application Development",
     "Ms Pushkar Gole",
     "IT Block-305", False),

    ("FRI", "14:00", "15:00", "BAI102",
     "IT Workshop", "Ms Ruchi Bhatt",
     "IT Block-305", False),

    ("FRI", "15:00", "17:00", "BAI102 / BAS-103",
     "IT Workshop LAB Gr. 2 / Probability and Statistics "
     "(CS) 1st year, Gr. 1",
     "Ms Ruchi Bhatt / Dr RajKumar Verma & Ms Manisha",
     "IT-401 / IT-313", True),


    # SAT
    ("SAT", "09:00", "11:00", "BAS104",
     "Environmental Sciences", "Dr Maruf",
     "IT Block-305", False),

    ("SAT", "11:00", "13:00", "BAS104 / HMC-101",
     "Environmental Sciences Lab GP1 / Communication Skills Lab Gp2",
     "Dr Maruf / Dr Anagha E, Ms Afrida Masooma",
     "C-113 / 106 Old Sciences Block", True),

    ("SAT", "13:00", "15:00", "HMC-101",
     "Communication Skills (CS)", "Dr Anagha E",
     "IT Block-305", False),

    ("SAT", "15:00", "17:00", "BAS104 / HMC-101",
     "Environmental Sciences Lab GP2 / Communication Skills Lab Gp1",
     "Dr Maruf / Dr Anagha E, Ms Afrida Masooma",
     "C-113 / 106 Old Sciences Block", True),
]

def seed_branch(branch_name: str, year: int, rows, section: str = None):
    """Idempotent per (branch, year, section)."""

    query = db.query(TimetableEntry).filter(
        TimetableEntry.branch == branch_name,
        TimetableEntry.year == year,
    )

    if section is None:
        query = query.filter(TimetableEntry.section.is_(None))
    else:
        query = query.filter(TimetableEntry.section == section)

    existing = query.count()

    if existing > 0:
        print(
            f"{branch_name} (Year {year}, Section {section}) "
            f"already seeded — skipping ({existing} existing rows)."
        )
        return
    day_map={
    "MON": "monday",
    "TUES": "tuesday",
    "WED": "wednesday",
    "THUR": "thursday",
    "FRI": "friday",
    "SAT": "saturday",
}
    for day, start, end, code, name, faculty, venue, is_lab in rows:
        db.add(TimetableEntry(
            branch=branch_name,
            year=year,
            section=section,
            day_of_week=day_map[day],
            start_time=start,
            end_time=end,
            subject_code=code,
            subject_name=name,
            faculty=faculty,
            venue=venue,
            is_lab=is_lab,
            mandatory=True,
           

    ))

    db.commit()

    print(
        f"Seeded {branch_name} (Year {year}, Section {section}): "
        f"{len(rows)} entries."
    )

def get_or_create_faculty(name: str) -> Faculty:
    """
    Create a Faculty record if it does not already exist.

    Faculty names are matched using a normalized key so small formatting
    differences such as:
        Prof Shalini Arora
        Prof. Shalini Arora
    do not create duplicate faculty records.
    """
    key = normalize_name_key(name)

    for faculty in db.query(Faculty).all():
        if normalize_name_key(faculty.name) == key:
            return faculty

    faculty = Faculty(name=name.strip())
    db.add(faculty)
    db.flush()

    return faculty


def seed_faculty_from_timetable():
    """
    Derive Faculty and FacultySchedule records from ALL existing
    TimetableEntry rows.

    The timetable itself remains the single source of truth.
    No PDF is parsed again here.

    Each timetable entry can create one or more FacultySchedule rows,
    allowing co-teaching faculty to share the same timetable entry.
    """

    created = 0

    entries = db.query(TimetableEntry).all()

    for entry in entries:

        # No faculty information -> nothing to derive.
        if not entry.faculty or not entry.faculty.strip():
            continue

        # Get faculty assignments for this timetable entry.
        faculty_parts = parse_faculty_field(entry.faculty)

        for name, group, needs_verification in faculty_parts:

            if not name or not name.strip():
                continue

            faculty = get_or_create_faculty(name)

            # Prevent the exact same FacultySchedule link
            # from being created again.
            already_exists = (
                db.query(FacultySchedule)
                .filter(
                    FacultySchedule.faculty_id == faculty.id,
                    FacultySchedule.timetable_entry_id == entry.id,
                    FacultySchedule.group == group,
                )
                .first()
            )

            if already_exists:
                continue

            db.add(
                FacultySchedule(
                    faculty_id=faculty.id,
                    timetable_entry_id=entry.id,
                    group=group,
                    needs_verification=needs_verification,
                )
            )

            created += 1

    db.commit()

    print(
        f"Faculty schedule derivation complete: "
        f"{created} new faculty-schedule links created."
    )
    


if __name__ == "__main__":
    # ------------------------------------------------------------
    # Student timetable data
    # ------------------------------------------------------------

    seed_branch("CSE", 1, CSE_YEAR1)
    seed_branch("Robotics and AI", 1, RAIE_YEAR1)
    seed_branch("ECE", 1, ECE_YEAR1)
    seed_branch("MAE", 1, MAE_YEAR1)
    seed_branch("IT", 1, IT_YEAR1_SECTION1, section="1")

    seed_branch("AI-ML", 1, AI_ML_YEAR1)

    seed_branch("CSE-AI", 1, CSE_AI_I_YEAR1, section="I")
    seed_branch("CSE-AI", 1, CSE_AI_II_YEAR1, section="II")
    seed_branch("CSE-AI", 1, CSE_AI_III_YEAR1, section="III")

    seed_branch("ECE-AI", 1, ECE_AI_I_YEAR1, section="I")
    seed_branch("ECE-AI", 1, ECE_AI_II_YEAR1, section="II")

    seed_branch("MAC", 1, MAC_YEAR1)
    seed_branch("Cyber Security", 1, CYBER_SECURITY_YEAR1)

     # -----------------------------------------
     # Faculty timetable generation
    # -----------------------------------------
    derive_faculty_schedules(db)

    print("Seeding run complete.")

    db.close()