import sqlite3
from datetime import datetime, timedelta
import random
import os
import sys
from backend.db.email_scheduler import send_email

"""
Utility helpers for seeding the email_templates table and sending outbound
simulation emails from the CLI. The bulk of this file is seed data.
"""

# Ensure project root is importable when run as a script
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)



DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

# Connect once at import time; this module mainly seeds templates and fires emails.
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

def add_default_email_templates():
    """
    Insert default phishing-style email templates for different airline departments.
    Only inserts if the email_templates table is currently empty (prevents duplicates).
    """
    cursor.execute("SELECT COUNT(*) FROM email_templates;")
    count = cursor.fetchone()[0]
    if count > 0:
        print("email_templates already populated; skipping default insert.")
        return

    templates = [
        # === CORPORATE (10) ===
    ("Corporate Policy Update",
    "Mandatory Company Policy Review – Action Required",
    "Dear Team,\n\nCorporate Compliance has released an updated policy regarding international travel reimbursements. Please review and acknowledge before Friday using the secure link below.\n\n[Review Policy]\n\nThank you,\nCorporate Affairs",
    "medium", "Corporate", "Generic greeting, external link, urgency", 1),

    ("Leadership Webinar Invite",
    "Exclusive Invite: Leadership Insights 2025 Webinar",
    "Join our executive leadership team for a live webinar on strategic growth this quarter. Confirm your attendance below.\n\n[Confirm Attendance]\n\nSeats are limited!",
    "easy", "Corporate", "Unverified sender domain, vague event details, link", 1),

    ("Corporate Device Sync Alert",
    "Company Device Security Verification Needed",
    "Your corporate device has been flagged for a pending security verification. Please log in to re-sync and verify access.\n\n[Verify Device Access]",
    "hard", "Corporate", "Impersonation of IT, login link, urgency", 1),

    ("Expense Reimbursement Error",
    "Expense Claim Declined – Verification Needed",
    "Dear Employee,\n\nYour last reimbursement claim was flagged due to a missing approval code. Re-submit your form using the secure link below.\n\n[Re-Submit Form]",
    "medium", "Corporate", "Finance impersonation, urgency, fake link", 1),

    ("Quarterly Report Access",
    "Access Restricted: Q3 Corporate Report Locked",
    "Hi Team,\n\nYour access to the latest Q3 financial report is pending confirmation. Verify credentials to unlock.\n\n[Unlock Report]",
    "hard", "Corporate", "Fake report link, credential harvest", 1),

    ("Travel Approval Notice",
    "Travel Request Approved – Review Details",
    "Your corporate travel to Dallas has been approved. Download your itinerary here:\n\n[Download Itinerary]",
    "easy", "Corporate", "Fake travel link, file attachment", 1),

    ("Account Activity Notification",
    "Unusual Login Detected from New Location",
    "Security Alert: Your corporate account was accessed from an unknown location. Confirm this was you:\n\n[Confirm Login]",
    "hard", "Corporate", "Impersonation of IT, fake alert, fear tactic", 1),

    ("Corporate Survey",
    "Help Shape Company Strategy – 2-Minute Survey",
    "Take a quick survey to help shape next quarter's strategic goals.\n\n[Take Survey]",
    "easy", "Corporate", "External domain, incentive appeal", 1),

    ("Cloud Storage Limit Reached",
    "Corporate Drive Full – Renew Storage Plan",
    "Your corporate OneDrive has reached 95% capacity. Increase storage immediately to avoid file loss.\n\n[Renew Storage]",
    "medium", "Corporate", "Impersonation of Microsoft, urgency", 1),

    ("Policy Compliance Suspension",
    "Non-Compliance Detected: Account Suspension Warning",
    "Our records show your compliance training certificate has expired. Renew access within 24 hours:\n\n[Renew Compliance Access]",
    "hard", "Corporate", "Fake HR/IT domain, urgency, fear tactic", 1),

    # === HR (10) ===
    ("Annual Benefits Enrollment",
    "Open Enrollment: Confirm Your Benefits Selection",
    "It’s time to review your 2025 benefits. Access the secure portal to confirm your selections before October 15.\n\n[Access HR Portal]",
    "medium", "HR", "External link, deadline pressure, impersonation of HR", 1),

    ("Salary Adjustment Notice",
    "Salary Review Notification",
    "Dear Employee,\n\nYour salary record indicates an adjustment pending confirmation. Please verify your payment details immediately.\n\n[Verify Details]",
    "hard", "HR", "Sensitive data request, urgency, fake payroll domain", 1),

    ("Staff Survey Incentive",
    "Complete HR Survey – Win a $50 Gift Card!",
    "Help us improve! Take our quick HR engagement survey for a chance to win a gift card.\n\n[Take Survey]",
    "easy", "HR", "External domain, incentive lure, no official branding", 1),

    ("Leave Balance Alert",
    "Vacation Days Reset Reminder",
    "Your remaining leave days will reset next week. Confirm your balance before it’s too late.\n\n[View Balance]",
    "medium", "HR", "Urgency, fake HR portal", 1),

    ("Employee Policy Acknowledgment",
    "New Workplace Conduct Policy – Please Sign",
    "We’ve updated our workplace conduct policy. Please log in to sign acknowledgment.\n\n[Sign Policy]",
    "medium", "HR", "Fake document signature request", 1),

    ("Payroll Verification",
    "Payroll Update: Confirm Bank Account Details",
    "We detected a mismatch in your direct deposit info. Confirm details immediately to prevent delay.\n\n[Confirm Info]",
    "hard", "HR", "Fake payroll, sensitive data request", 1),

    ("Training Portal Login",
    "HR Training Portal Access Required",
    "Complete your mandatory annual HR training by logging into the portal:\n\n[Access Portal]",
    "easy", "HR", "Fake learning system login", 1),

    ("Health Insurance Reminder",
    "Health Plan Renewal – Action Required",
    "Your company health insurance coverage expires this week. Renew now:\n\n[Renew Coverage]",
    "medium", "HR", "Fake healthcare domain, urgency", 1),

    ("Promotion Eligibility Review",
    "Congratulations! You’re Eligible for Internal Promotion",
    "Review your updated eligibility status here:\n\n[View Eligibility]",
    "easy", "HR", "Emotional lure, fake form link", 1),

    ("Performance Appraisal",
    "2025 Performance Review Document Available",
    "Access your performance review summary now:\n\n[View Appraisal]",
    "medium", "HR", "Fake HR domain, credential request", 1),

    # === DIGITAL TECHNOLOGY (10) ===
    ("Git Repository Access Alert",
    "Security Update: Repository Access Reset Required",
    "Due to recent changes, all Git repository users must reset access credentials.\n\n[Reset Repository Access]",
    "hard", "Digital Technology", "IT impersonation, credential reset, suspicious domain", 1),

    ("System Patch Required",
    "Critical Security Patch – Install Immediately",
    "A vulnerability was detected in your workstation. Please install the urgent patch below.\n\n[Download Patch Installer]",
    "medium", "Digital Technology", "Fake patch file, download link, urgency", 1),

    ("Azure Access Expiring",
    "Action Needed: Azure Access Will Expire Soon",
    "Your access to the airline Azure environment will expire in 24 hours. Click below to renew permissions.\n\n[Renew Access]",
    "hard", "Digital Technology", "External domain, fake Microsoft sender, urgency", 1),

    ("VPN Certificate Renewal",
    "VPN Access Expiring in 2 Days",
    "Renew your VPN certificate to avoid network disconnection.\n\n[Renew VPN]",
    "medium", "Digital Technology", "Fake IT certificate, urgency", 1),

    ("System Maintenance Alert",
    "Scheduled Maintenance – Reauthentication Required",
    "Reauthenticate your credentials after maintenance to prevent service interruption.\n\n[Reauthenticate]",
    "medium", "Digital Technology", "Fake IT portal, credential request", 1),

    ("Password Expiration Notice",
    "Password Will Expire in 1 Day",
    "Update your password before losing access.\n\n[Reset Password]",
    "easy", "Digital Technology", "Impersonation, urgency, fake link", 1),

    ("Security Incident Report",
    "Incident Detected on Your Account",
    "Anomalous behavior detected in your corporate account. Log in to review activity.\n\n[View Report]",
    "hard", "Digital Technology", "Fake alert, login page, fear", 1),

    ("System Upgrade Notification",
    "Upgrade to Latest Airline Systems Dashboard",
    "The airline IT dashboard has been upgraded. Log in to test your new interface.\n\n[Access Dashboard]",
    "easy", "Digital Technology", "Fake update link", 1),

    ("Two-Factor Authentication Setup",
    "Mandatory MFA Setup – Required by IT Security",
    "Set up two-factor authentication immediately:\n\n[Setup MFA]",
    "medium", "Digital Technology", "Fake IT security domain", 1),

    ("Server Downtime Compensation",
    "Outage Credit Approval Pending",
    "IT Systems is offering service credit for recent downtime. Claim your approval here:\n\n[Claim Credit]",
    "easy", "Digital Technology", "Fake compensation request", 1),

    # === AIRCRAFT MAINTENANCE AND SUPPORT (10) ===
    ("Maintenance Alert",
    "Updated Maintenance Manual – Required Download",
    "The latest aircraft maintenance manual (AMM) revision is now available. Please download and review before your next shift.\n\n[Download Manual]",
    "medium", "Aircraft Maintenance and Support", "Download link, fake sender, urgency", 1),

    ("Tool Calibration Report",
    "Calibration Report Submission Missing",
    "Our records show your calibration report for aircraft tools is missing. Upload it before end of day.\n\n[Upload Report]",
    "easy", "Aircraft Maintenance and Support", "Fake QA address, upload link, false urgency", 1),

    ("Safety Bulletin",
    "URGENT: New FAA Safety Bulletin for Mechanics",
    "Please review the attached safety bulletin concerning recent FAA inspection changes.\n\n[View Bulletin]",
    "hard", "Aircraft Maintenance and Support", "Attachment, urgency, external domain", 1),

    ("Equipment Recall Notice",
    "Urgent Recall – Verify Equipment Lot Number",
    "A recall has been issued for equipment lot #2345. Verify if your tools are affected.\n\n[Verify Lot]",
    "medium", "Aircraft Maintenance and Support", "Fake recall link", 1),

    ("Shift Roster Change",
    "Maintenance Crew Roster Updated",
    "Shift timings for maintenance crews have been updated. View the revised schedule:\n\n[View Schedule]",
    "easy", "Aircraft Maintenance and Support", "Fake roster portal", 1),

    ("Audit Checklist Upload",
    "Audit Preparation Checklist Pending Upload",
    "Submit your maintenance compliance checklist today.\n\n[Upload Now]",
    "medium", "Aircraft Maintenance and Support", "Fake audit request", 1),

    ("Inspection Violation Alert",
    "Non-Conformance Found During Inspection",
    "Review inspection results and submit corrective action plan.\n\n[Review Findings]",
    "hard", "Aircraft Maintenance and Support", "Fake compliance domain", 1),

    ("Certification Renewal",
    "Mechanic Certification Renewal Due",
    "Renew your maintenance certification before deadline.\n\n[Renew License]",
    "easy", "Aircraft Maintenance and Support", "Fake FAA renewal site", 1),

    ("Part Replacement Approval",
    "Part Request Approval Needed",
    "Approve new part request before procurement cutoff.\n\n[Approve Request]",
    "medium", "Aircraft Maintenance and Support", "Fake part ordering portal", 1),

    ("Maintenance Training Invite",
    "New Maintenance System Training Available",
    "Attend the new training session for AMM updates.\n\n[Join Training]",
    "easy", "Aircraft Maintenance and Support", "Fake training link", 1),

    # === CUSTOMER SOLUTIONS (10) ===
    ("Customer Complaint Follow-Up",
    "Pending Customer Case Review",
    "You have one pending case requiring review. Click below to access the customer portal and respond.\n\n[Access Case]",
    "medium", "Customer Solutions", "Fake portal link, customer case lure", 1),

    ("Service Quality Audit",
    "Quality Assurance Review: Immediate Response Required",
    "An audit of recent customer feedback has flagged a discrepancy in your service records. Please verify within 24 hours.\n\n[Verify Records]",
    "hard", "Customer Solutions", "Fake audit, urgency, fear appeal", 1),

    ("Customer Data Update",
    "Customer Account Access Verification",
    "To comply with new security policies, please verify your login credentials for the customer database.\n\n[Verify Access]",
    "medium", "Customer Solutions", "Credential harvest, fake IT domain", 1),

    ("Refund Confirmation",
    "Refund Approved – Confirm Bank Details",
    "Dear Agent,\n\nYour recent refund has been approved. Confirm payout details:\n\n[Confirm Details]",
    "medium", "Customer Solutions", "Fake refund scam, finance mimicry", 1),

    ("Survey Results Available",
    "New Customer Feedback Available",
    "New NPS survey results are available for your review.\n\n[View Feedback]",
    "easy", "Customer Solutions", "Fake feedback portal", 1),

    ("Compliance Violation",
    "Customer Data Handling Violation Logged",
    "Your recent customer handling process violated internal policies. Review the details:\n\n[Review Violation]",
    "hard", "Customer Solutions", "Fake compliance report", 1),

    ("Ticketing System Login",
    "CRM Login Expiring Soon",
    "Re-activate your CRM login to continue customer support operations.\n\n[Re-Activate Now]",
    "medium", "Customer Solutions", "Fake CRM portal", 1),

    ("Customer Outreach Approval",
    "Marketing Outreach Requires Authorization",
    "Approve new marketing outreach to proceed:\n\n[Approve Outreach]",
    "easy", "Customer Solutions", "Fake marketing email", 1),

    ("Complaint Escalation Notice",
    "High-Priority Complaint Requires Immediate Review",
    "Customer complaint escalated to Tier 3. Resolve within 6 hours.\n\n[Resolve Now]",
    "hard", "Customer Solutions", "Fake escalation urgency", 1),

    ("Rewards Program Update",
    "New Customer Rewards Platform – Activate Now",
    "Activate your rewards platform credentials here:\n\n[Activate Access]",
    "medium", "Customer Solutions", "Fake customer reward phishing", 1),

    # === AT THE AIRPORT (10) ===
    ("Gate Schedule Change",
    "Gate Assignment Update for Flight 234",
    "Attention staff: Gate assignments for Flight 234 have changed. View the latest update below.\n\n[View Schedule]",
    "easy", "At the Airport", "Fake ops domain, gate number lure", 1),

    ("Badge Access Suspension",
    "Security Notice: Badge Access Suspended",
    "Due to irregular activity, your employee badge has been temporarily suspended. Restore access immediately below.\n\n[Restore Access]",
    "hard", "At the Airport", "Urgency, fear, fake badge recovery link", 1),

    ("Parking Permit Renewal",
    "Employee Parking Permit Renewal",
    "Please renew your parking permit before it expires on Monday. Use the form below to submit your renewal.\n\n[Renew Permit]",
    "medium", "At the Airport", "Fake form link, false deadline", 1),

    ("Tarmac Incident Report",
    "Incident Logged – Employee Statement Needed",
    "An incident was logged near your shift. Submit your statement now.\n\n[Submit Report]",
    "hard", "At the Airport", "Fake report request, urgency", 1),

    ("Flight Crew Meeting",
    "Mandatory Pre-Flight Safety Briefing",
    "Attend your mandatory safety briefing before departure.\n\n[Join Briefing]",
    "easy", "At the Airport", "Fake meeting link", 1),

    ("Luggage Mishandling Notice",
    "Baggage Claim Report Missing Signature",
    "You have one missing document for baggage claim #9821. Sign it here:\n\n[Sign Form]",
    "medium", "At the Airport", "Fake claim form", 1),

    ("Gate Access Approval",
    "Restricted Area Access Request Pending",
    "Approve restricted gate area access before security closes review.\n\n[Approve Access]",
    "medium", "At the Airport", "Fake access portal", 1),

    ("Lost Badge Replacement",
    "Order Replacement for Lost ID Badge",
    "We noticed your badge inactivity for 72 hours. Order replacement:\n\n[Request Badge]",
    "easy", "At the Airport", "Fake ID recovery portal", 1),

    ("Flight Delay Compensation",
    "Compensation Notice for Delayed Flight",
    "Your recent flight delay qualifies for compensation. Review claim:\n\n[View Claim]",
    "medium", "At the Airport", "Fake compensation email", 1),

    ("Runway Access Suspension",
    "Immediate Action Required – Runway Access Locked",
    "Your runway clearance badge has been disabled. Restore immediately.\n\n[Unlock Access]",
    "hard", "At the Airport", "Fear-based urgency, fake IT portal", 1),

    # === FLIGHT ATTENDANT (10) ===
    ("Crew Schedule Update",
    "Schedule Change – Action Required",
    "Your flight schedule for next week has been updated. Please confirm your new roster using the secure link below.\n\n[Confirm Schedule]",
    "medium", "Flight Attendant", "Fake crew portal, urgency, link", 1),

    ("Uniform Replacement",
    "crew-support@airlineuniforms.com",
    "We’re rolling out new uniforms this quarter. Please log in below to confirm your size and delivery details.\n\n[Confirm Details]",
    "easy", "Flight Attendant", "Fake supplier link, login form, fake rebranding", 1),

    ("Training Compliance Reminder",
    "Mandatory Safety Training Reminder",
    "You have one incomplete safety module due by Friday. Access your training dashboard below.\n\n[Access Dashboard]",
    "hard", "Flight Attendant", "Deadline pressure, fake academy domain", 1),

    ("Hotel Accommodation Notice",
    "Crew Hotel Booking Confirmation",
    "Dear Crew Member,\n\nConfirm your layover hotel booking using the secure link:\n\n[Confirm Booking]",
    "medium", "Flight Attendant", "Fake travel portal", 1),

    ("Expense Reimbursement Request",
    "Crew Meal Allowance Claim – Pending Approval",
    "Submit your meal claim receipts here:\n\n[Submit Claim]",
    "medium", "Flight Attendant", "Fake airline finance link", 1),

    ("Health Declaration Form",
    "Health Check – Required Before Departure",
    "Please complete your pre-flight health declaration.\n\n[Complete Form]",
    "easy", "Flight Attendant", "Fake form link", 1),

    ("Passenger Complaint Follow-Up",
    "Passenger Feedback Requires Response",
    "A passenger filed a complaint regarding your flight service. Review it here:\n\n[View Feedback]",
    "hard", "Flight Attendant", "Fake HR complaint portal", 1),

    ("Layover Itinerary",
    "Layover Location Updated – Confirm ASAP",
    "Your layover location has been updated. Confirm your availability:\n\n[Confirm Layover]",
    "medium", "Flight Attendant", "Fake travel notice", 1),

    ("Crew Portal Login",
    "Crew Portal Authentication Expiring Soon",
    "Your crew account credentials will expire within 48 hours. Renew below to maintain access.\n\n[Renew Access]",
    "medium", "Flight Attendant", "Fake login portal", 1),

    ("Inflight Service Update",
    "New Inflight Service Procedures – Review Required",
    "New inflight procedures have been released. Review them here:\n\n[View Update]",
    "medium", "Flight Attendant", "Fake training doc link", 1),
    
    # === PILOT OPERATIONS (10) ===
    ("Flight Plan Update",
    "URGENT: Revised Flight Plan for Tomorrow’s Departure",
    "Dear Captain,\n\nThe flight plan for tomorrow’s departure has been updated due to new weather conditions. Review and confirm immediately.\n\n[View Updated Plan]",
    "medium", "Pilot Operations", "Urgency, fake ops link, impersonation of dispatch", 1),

    ("Simulator Training Schedule",
    "Mandatory Simulator Session – Confirm Attendance",
    "Your simulator session for next week has been scheduled. Confirm attendance below.\n\n[Confirm Session]",
    "easy", "Pilot Operations", "Fake training domain, urgency", 1),

    ("Pilot Medical Renewal",
    "Medical Certificate Expiration Warning",
    "Your Class 1 medical certificate expires in 5 days. Renew now to maintain flight eligibility.\n\n[Renew Certificate]",
    "hard", "Pilot Operations", "Fake aviation authority link, urgency", 1),

    ("Weather Alert Briefing",
    "Critical Weather Advisory for Route 1542",
    "Severe weather systems detected along your route. Review updated safety procedures.\n\n[View Briefing]",
    "medium", "Pilot Operations", "Fake dispatch alert", 1),

    ("Fuel Efficiency Audit",
    "Fuel Usage Review – Immediate Action Required",
    "A discrepancy was found in your recent flight fuel report. Please verify your data.\n\n[Verify Report]",
    "hard", "Pilot Operations", "Fake audit, fear tactic", 1),

    ("Pilot Roster Adjustment",
    "Updated Crew Pairing Released",
    "New pairing assignments are live. Check your updated schedule:\n\n[View Pairing]",
    "medium", "Pilot Operations", "Fake scheduling portal", 1),

    ("Incident Report Form",
    "Follow-Up Required: Post-Flight Debrief",
    "Submit your debrief report for Flight 8921 using the form below.\n\n[Submit Report]",
    "easy", "Pilot Operations", "Fake internal link", 1),

    ("Cockpit System Update",
    "Avionics Software Upgrade Required",
    "The cockpit EFB requires a mandatory software update before your next flight.\n\n[Download Update]",
    "hard", "Pilot Operations", "Fake update link, malware risk", 1),

    ("Flight Duty Tracker",
    "Duty Hours Logged Incorrectly – Review Needed",
    "System detected irregularities in your duty hour log. Review now:\n\n[Check Log]",
    "medium", "Pilot Operations", "Fake HR/ops domain", 1),

    ("Annual Proficiency Check",
    "License Renewal: Submit Training Records",
    "Submit your latest proficiency check results before the licensing deadline.\n\n[Submit Records]",
    "easy", "Pilot Operations", "Fake pilot registry form", 1),

    # === FINANCE & ACCOUNTING (10) ===
    ("Invoice Payment Notice",
    "Payment Overdue – Immediate Action Required",
    "Your pending invoice #87432 is overdue. Confirm payment below.\n\n[Confirm Payment]",
    "medium", "Finance", "Fake payment link, urgency", 1),

    ("Expense Approval Needed",
    "New Expense Report Pending Review",
    "Approve the attached expense report for immediate processing.\n\n[Approve Now]",
    "easy", "Finance", "Fake attachment link", 1),

    ("Payroll Update Request",
    "Salary Discrepancy Detected",
    "Our system detected inconsistent payroll data for your department. Confirm immediately.\n\n[Review Payroll]",
    "hard", "Finance", "Fake HR impersonation", 1),

    ("Tax Rebate Confirmation",
    "Eligible for 2025 Tax Rebate – Verify Account",
    "Verify your company bank account to receive the rebate.\n\n[Verify Now]",
    "hard", "Finance", "Fake IRS-like scam, urgency", 1),

    ("Budget Allocation Review",
    "Budget Reallocation Pending Sign-Off",
    "Please review updated Q3 budget allocation before approval deadline.\n\n[Review Budget]",
    "medium", "Finance", "Fake finance domain", 1),

    ("Wire Transfer Confirmation",
    "Urgent: Verify Wire Transfer Details",
    "A pending wire transfer to vendor account requires confirmation.\n\n[Confirm Transfer]",
    "hard", "Finance", "Fake vendor impersonation", 1),

    ("Invoice Portal Login",
    "Access Your Vendor Invoice Dashboard",
    "Log in to your finance portal to verify pending invoices.\n\n[Access Portal]",
    "easy", "Finance", "Fake vendor login link", 1),

    ("Audit Report Distribution",
    "Internal Audit Findings Now Available",
    "Download your department’s latest audit report for review.\n\n[Download Report]",
    "medium", "Finance", "Fake internal audit link", 1),

    ("Reimbursement Alert",
    "Expense Claim Auto-Rejected",
    "Your travel expense claim was rejected due to incorrect receipts. Re-upload now.\n\n[Upload Receipts]",
    "medium", "Finance", "Fake travel department domain", 1),

    ("Financial System Downtime",
    "ERP System Maintenance Tonight",
    "The finance ERP portal will be down for maintenance. Login verification required before downtime.\n\n[Verify Account]",
    "easy", "Finance", "Fake maintenance email, login request", 1),

    # === IT SUPPORT & INFRASTRUCTURE (10) ===
    ("Password Reset Request",
    "Reset Your Password Now",
    "A reset request was initiated for your account. Click below if this was you.\n\n[Reset Password]",
    "easy", "IT Support", "Fake IT link, fear appeal", 1),

    ("Helpdesk Ticket Update",
    "Your IT Ticket #59382 Has Been Updated",
    "Log in to view the technician's response.\n\n[View Update]",
    "medium", "IT Support", "Fake helpdesk portal", 1),

    ("VPN Access Restricted",
    "VPN Login Blocked – New Policy",
    "Due to new IT restrictions, VPN access requires MFA re-setup.\n\n[Setup MFA]",
    "hard", "IT Support", "Fake MFA site", 1),

    ("Phishing Awareness Test",
    "Mandatory Cybersecurity Training Available",
    "Complete your phishing awareness course by Friday.\n\n[Start Training]",
    "easy", "IT Support", "Fake training platform", 1),

    ("System Outage Notice",
    "Critical Network Outage – Update Required",
    "Apply the urgent patch below to restore access.\n\n[Apply Update]",
    "medium", "IT Support", "Fake patch file, urgency", 1),

    ("Unauthorized Access Alert",
    "ALERT: Suspicious Login Detected",
    "A login attempt was made from an unrecognized location. Review details now.\n\n[Review Access]",
    "hard", "IT Support", "Fake IT alert, credential theft", 1),

    ("Software License Expiring",
    "License Renewal Due",
    "Renew your Microsoft Office 365 license before expiration.\n\n[Renew License]",
    "medium", "IT Support", "Fake renewal domain", 1),

    ("Cloud Backup Confirmation",
    "Your Backup Was Interrupted",
    "Re-run your cloud backup job using the secure link:\n\n[Resume Backup]",
    "easy", "IT Support", "Fake cloud provider site", 1),

    ("Device Management Enrollment",
    "Enroll Device in New IT Policy",
    "Register your device under the updated IT security framework.\n\n[Enroll Device]",
    "medium", "IT Support", "Fake MDM enrollment page", 1),

    ("IT Service Satisfaction Survey",
    "Rate Your IT Support Experience",
    "Take 1 minute to review our service.\n\n[Take Survey]",
    "easy", "IT Support", "Fake survey link, minimal red flags", 1),

    # === CORPORATE (5 – honorific style) === 
    ("Corporate Excellence Award",
    "Congratulations, Employee of the Month!",
    "Dear Employee of the Month {name},\n\nYou have been shortlisted for our Corporate Excellence Award. To finalize your recognition package, please confirm your details below.\n\n[Confirm Recognition Details]\n\nRegards,\nCorporate Awards Committee",
    "hard", "Corporate", "Unusual award notice, data confirmation, suspicious link", 1),

    ("Esteemed Strategy Contributor",
    "Invitation for Esteemed Contributors to Strategy Roundtable",
    "Dear Esteemed Employee {name},\n\nBased on your outstanding performance, you have been invited to a strategy roundtable with senior leadership. Reserve your exclusive seat here:\n\n[Reserve Your Seat]\n\nThis link is valid for 12 hours.",
    "medium", "Corporate", "Flattery/lure, time-limited link, vague details", 1),

    ("Honored Corporate Ambassador",
    "You Have Been Selected as a Corporate Ambassador",
    "Dear Honored Employee {name},\n\nYou have been selected as a corporate ambassador for our upcoming brand campaign. Please upload your profile details and photo using the portal below.\n\n[Upload Profile]\n\nThank you for representing us.",
    "hard", "Corporate", "Profile upload request, possible file/data exfiltration", 1),

    ("Distinguished Performance Survey",
    "Confidential Survey for Top Performers",
    "Dear Distinguished Staff Member {name},\n\nYou were identified as a top performer in the last quarter. Kindly complete this short confidential survey to help shape leadership initiatives.\n\n[Complete Confidential Survey]",
    "medium", "Corporate", "Flattering language, external survey form", 1),

    ("Valued Culture Champion",
    "Recognition as a Culture Champion – Confirmation Needed",
    "Dear Valued Team Member {name},\n\nYou have been nominated as a 'Culture Champion' in your department. Confirm your profile and acknowledgement below.\n\n[Confirm Nomination]",
    "easy", "Corporate", "Praise + action, vague origin, link click lure", 1),

    # === HR (5 – honorific style) ===
    ("Esteemed Employee Wellness Check",
    "Exclusive Wellness Check-In for Esteemed Employees",
    "Dear Esteemed Employee {name},\n\nAs part of our wellness initiative, you've been selected for a private HR wellness review. Please complete the confidential form below.\n\n[Start Wellness Check]",
    "medium", "HR", "Personal-sounding survey, confidential form, data grab", 1),

    ("Honored Service Milestone",
    "Celebrate Your Upcoming Service Milestone",
    "Dear Honored Employee {name},\n\nOur system shows you are approaching a service milestone. To prepare your recognition package, please verify your personal details.\n\n[Verify Details]",
    "hard", "HR", "Uses recognition as pretext to harvest personal info", 1),

    ("Employee of the Month Follow-Up",
    "Employee of the Month: Tax & Payroll Update",
    "Dear Employee of the Month {name},\n\nDue to your recent award, we must update your payroll and tax records. Confirm your direct deposit information below.\n\n[Update Payroll Info]",
    "hard", "HR", "Award context hiding a sensitive banking data request", 1),

    ("Valued Team Recognition Survey",
    "Share Feedback as a Valued Team Member",
    "Dear Valued Team Member {name},\n\nHR is conducting a short feedback survey for highly-engaged employees. Your participation is requested.\n\n[Take Recognition Survey]",
    "easy", "HR", "Compliment + survey + external form", 1),

    ("Distinguished Diversity Advocate",
    "Diversity Advocate Recognition – Action Required",
    "Dear Distinguished Staff Member {name},\n\nYou have been identified as a potential diversity and inclusion ambassador. Confirm your interest and information:\n\n[Confirm Participation]",
    "medium", "HR", "Recruitment into initiative with data capture", 1),

    # === DIGITAL TECHNOLOGY (5 – honorific style) ===
    ("Esteemed Developer Access",
    "Priority Access for Esteemed Developers",
    "Dear Esteemed Employee {name},\n\nYou have been granted early access to our new internal developer tools dashboard. Activate your account here:\n\n[Activate Dev Access]",
    "medium", "Digital Technology", "Flattery + new tool access, fake dev portal", 1),

    ("Honored Security Champion",
    "Security Champion Program Enrollment",
    "Dear Honored Colleague {name},\n\nYou have been nominated as a Security Champion. To finalize your enrollment, log in and review the onboarding materials.\n\n[Join Security Champion Portal]",
    "hard", "Digital Technology", "Security-themed, login to fake portal, high trust abuse", 1),

    ("Employee of the Month Sandbox",
    "Exclusive Sandbox Environment for Employee of the Month",
    "Dear Employee of the Month {name},\n\nYou have been granted access to a performance sandbox environment with elevated permissions. Sign in to explore features:\n\n[Access Sandbox]",
    "hard", "Digital Technology", "Elevated access lure, high value for attackers", 1),

    ("Valued Power User Beta",
    "Join Beta for Power Users",
    "Dear Valued Team Member {name},\n\nWe invite you, as a power user, to test our new internal dashboard. Use the link below:\n\n[Join Beta Program]",
    "medium", "Digital Technology", "Beta/test lure, fake internal app", 1),

    ("Distinguished Innovator Trial",
    "New Innovation Toolkit Trial for Distinguished Staff",
    "Dear Distinguished Staff Member {name},\n\nYou've been selected to try our innovation toolkit. Sign in with your corporate account:\n\n[Access Innovation Toolkit]",
    "easy", "Digital Technology", "Innovation buzzword + login request", 1),

    # === AIRCRAFT MAINTENANCE AND SUPPORT (5 – honorific style) ===
    ("Esteemed Technician Briefing",
    "Special Briefing for Esteemed Maintenance Technicians",
    "Dear Esteemed Employee {name},\n\nYou have been selected for a targeted safety briefing based on your maintenance record. Access the briefing here:\n\n[View Safety Briefing]",
    "medium", "Aircraft Maintenance and Support", "Safety briefing pretext, fake portal", 1),

    ("Honored Safety Leader",
    "Recognition as a Hangar Safety Leader",
    "Dear Honored Colleague {name},\n\nYour name has been put forward as a Hangar Safety Leader. Confirm your agreement and training preference:\n\n[Confirm Leader Role]",
    "medium", "Aircraft Maintenance and Support", "Leadership hook, link without verification", 1),

    ("Employee of the Month Toolbox",
    "Toolbox Upgrade for Employee of the Month",
    "Dear Employee of the Month {name},\n\nAs part of your recognition, you are eligible for a new digital toolbox license. Activate it here:\n\n[Activate Toolbox License]",
    "hard", "Aircraft Maintenance and Support", "Tooling/software license gimmick, download link", 1),

    ("Valued Line Mechanic Survey",
    "Confidential Line Maintenance Feedback",
    "Dear Valued Team Member {name},\n\nProvide anonymous feedback on line maintenance procedures using this short survey.\n\n[Start Anonymous Survey]",
    "easy", "Aircraft Maintenance and Support", "Anonymous survey, possible external form", 1),

    ("Distinguished Compliance Contributor",
    "Compliance Review for Distinguished Maintenance Staff",
    "Dear Distinguished Staff Member {name},\n\nCompliance has requested a quick confirmation of your last inspection logs. Upload the requested summary:\n\n[Upload Inspection Summary]",
    "hard", "Aircraft Maintenance and Support", "Upload request, could exfiltrate real docs", 1),

    # === CUSTOMER SOLUTIONS (5 – honorific style) ===
    ("Esteemed Customer Care Agent",
    "Exclusive Program for Esteemed Customer Care Agents",
    "Dear Esteemed Employee {name},\n\nYou have been invited to join an advanced customer care excellence track. Log into the portal to begin.\n\n[Join Excellence Track]",
    "medium", "Customer Solutions", "Training/recognition lure, login portal", 1),

    ("Honored Service Specialist",
    "Honored Service Specialist Recognition",
    "Dear Honored Employee {name},\n\nYour name has been highlighted for exceptional service scores. To finalize your recognition, confirm your details.\n\n[Confirm Service Record]",
    "hard", "Customer Solutions", "Uses performance metrics as pretext to gather data", 1),

    ("Employee of the Month Customer Edition",
    "Customer-Driven Employee of the Month Nomination",
    "Dear Employee of the Month {name},\n\nCustomers have rated you as a top performer. Access your customer feedback summary:\n\n[View Feedback Summary]",
    "medium", "Customer Solutions", "Customer praise + link to fake feedback system", 1),

    ("Valued Customer Hero Survey",
    "Short Survey for Customer Heroes",
    "Dear Valued Team Member {name},\n\nWe'd like a quick pulse-check from those with top service ratings. Share your insights:\n\n[Share Insights]",
    "easy", "Customer Solutions", "Survey with flattery, minimal details", 1),

    ("Distinguished Resolution Expert",
    "Confidential Review for Distinguished Resolution Experts",
    "Dear Distinguished Staff Member {name},\n\nA set of high-priority cases resolved under your ID is under confidential review. Access the case summary:\n\n[Open Case Summary]",
    "hard", "Customer Solutions", "High-priority case lure, sensitive data portal", 1),

    # === AT THE AIRPORT (5 – honorific style) ===
    ("Esteemed Airport Agent Brief",
    "Briefing for Esteemed Airport Operations Agents",
    "Dear Esteemed Employee {name},\n\nYou are invited to a focused briefing on new airport operations procedures. Review the materials:\n\n[Review Operations Brief]",
    "medium", "At the Airport", "Ops update pretext, link to fake portal", 1),

    ("Honored Ground Staff Award",
    "Ground Operations Recognition Opportunity",
    "Dear Honored Employee {name},\n\nYou have been nominated for a Ground Operations Recognition Award. Confirm your nomination:\n\n[Confirm Nomination]",
    "easy", "At the Airport", "Award/recognition lure, low detail", 1),

    ("Employee of the Month Ramp Edition",
    "Ramp Operations Employee of the Month",
    "Dear Employee of the Month {name},\n\nAs recognition for your ramp efforts, access your digital badge and certificate:\n\n[Download Digital Badge]",
    "medium", "At the Airport", "Download link in award context", 1),

    ("Valued Gate Agent Survey",
    "Anonymous Feedback Survey for Gate Agents",
    "Dear Valued Team Member {name},\n\nWe're collecting anonymous feedback from gate agents on recent boarding changes.\n\n[Take Gate Feedback Survey]",
    "easy", "At the Airport", "Survey, anonymous pretext, external host", 1),

    ("Distinguished Security Liaison",
    "Security Liaison Role Confirmation",
    "Dear Distinguished Staff Member {name},\n\nSecurity has proposed you as a liaison for your terminal area. Confirm acceptance and contact details:\n\n[Confirm Liaison Role]",
    "hard", "At the Airport", "Security/role hook, data collection", 1),

    # === FLIGHT ATTENDANT (5 – honorific style) ===
    ("Esteemed Cabin Crew Invite",
    "Exclusive Invite for Esteemed Cabin Crew Members",
    "Dear Esteemed Employee {name},\n\nYou are invited to join a closed feedback group for premium cabin service. Access the group portal here:\n\n[Access Feedback Group]",
    "medium", "Flight Attendant", "Exclusive group, login portal", 1),

    ("Honored Service Recognition",
    "In-Flight Service Recognition Opportunity",
    "Dear Honored Employee {name},\n\nYour recent passenger feedback has triggered a service recognition opportunity. Confirm your details to proceed.\n\n[Confirm Recognition]",
    "hard", "Flight Attendant", "Passenger praise used as a hook, data request", 1),

    ("Employee of the Month Cabin Edition",
    "Cabin Crew Spotlight – Employee of the Month",
    "Dear Employee of the Month {name},\n\nDownload your spotlight feature for internal publication below.\n\n[Download Spotlight Profile]",
    "medium", "Flight Attendant", "Download lure disguised as spotlight", 1),

    ("Valued Crew Mentor Program",
    "Join the Crew Mentor Program",
    "Dear Valued Team Member {name},\n\nBased on your record, you're invited to join the crew mentor initiative. Enroll here:\n\n[Enroll as Mentor]",
    "easy", "Flight Attendant", "Mentorship opportunity pretext", 1),

    ("Distinguished Safety Ambassador",
    "Safety Ambassador Role Confirmation",
    "Dear Distinguished Staff Member {name},\n\nYou've been recommended as a safety ambassador for your cabin team. Confirm your interest:\n\n[Confirm Safety Role]",
    "medium", "Flight Attendant", "Safety title flattery, link click", 1),

    # === PILOT OPERATIONS (5 – honorific style) ===
    ("Esteemed Captain Briefing",
    "Special Briefing for Esteemed Captains",
    "Dear Esteemed Employee {name},\n\nYou have been selected for a special briefing on advanced route optimization. Access it here:\n\n[View Special Briefing]",
    "medium", "Pilot Operations", "Exclusive briefing pretext", 1),

    ("Honored Flight Leader",
    "Recognition as Honored Flight Leader",
    "Dear Honored Colleague {name},\n\nYour leadership record has been highlighted. Confirm your details to receive your official note.\n\n[Confirm Leader Profile]",
    "hard", "Pilot Operations", "Leadership/ego appeal, data harvest", 1),

    ("Employee of the Month Captain Edition",
    "Captain of the Month – Performance Summary",
    "Dear Employee of the Month {name},\n\nView your performance dashboard and route statistics here:\n\n[View Performance Dashboard]",
    "medium", "Pilot Operations", "Analytics dashboard lure", 1),

    ("Valued Flight Operations Contributor",
    "Feedback Request from Valued Operations Contributor",
    "Dear Valued Team Member {name},\n\nShare your insights on recent route and fuel-saving changes using the link below.\n\n[Submit Operational Feedback]",
    "easy", "Pilot Operations", "Survey in ops context", 1),

    ("Distinguished Training Participant",
    "Advanced Simulator Slot for Distinguished Pilots",
    "Dear Distinguished Staff Member {name},\n\nYou have priority access to an advanced simulator training slot. Confirm your booking:\n\n[Confirm Simulator Slot]",
    "hard", "Pilot Operations", "Simulator/training opportunity with login", 1),

    # === FINANCE (5 – honorific style) ===
    ("Esteemed Finance Partner",
    "Confidential Briefing for Esteemed Finance Partners",
    "Dear Esteemed Employee {name},\n\nYou are invited to view a confidential financial performance preview for your unit.\n\n[View Performance Preview]",
    "medium", "Finance", "'Confidential' + performance data, fake portal", 1),

    ("Honored Budget Steward",
    "Budget Steward Recognition",
    "Dear Honored Employee {name},\n\nYou have been recognized as a key steward of your department's budget. Confirm your role details:\n\n[Confirm Steward Role]",
    "easy", "Finance", "Recognition title, click lure", 1),

    ("Employee of the Month Finance Edition",
    "Finance Employee of the Month – Tax Notice",
    "Dear Employee of the Month {name},\n\nA special bonus adjustment is being processed. Confirm your tax and payment details below.\n\n[Confirm Payment Details]",
    "hard", "Finance", "Bonus/award pretext hiding financial data request", 1),

    ("Valued Cost Controller Survey",
    "Survey for Valued Cost Controllers",
    "Dear Valued Team Member {name},\n\nHelp evaluate the effectiveness of recent cost-control initiatives.\n\n[Complete Finance Survey]",
    "medium", "Finance", "Survey with internal-sounding topic", 1),

    ("Distinguished Audit Contributor",
    "Internal Audit Contributor Follow-Up",
    "Dear Distinguished Staff Member {name},\n\nAudit has requested a short follow-up from select contributors. Upload your final notes:\n\n[Upload Audit Notes]",
    "hard", "Finance", "Audit pretext, document upload link", 1),

    # === IT SUPPORT (5 – honorific style) ===
    ("Esteemed Security Test Group",
    "Invitation to Esteemed Security Test Group",
    "Dear Esteemed Employee {name},\n\nYou've been selected to join a security test group for advanced phishing detection. Log in here:\n\n[Join Security Test Group]",
    "hard", "IT Support", "Meta-phishing, security context, login portal", 1),

    ("Honored Power User Program",
    "Honored Power User IT Program Enrollment",
    "Dear Honored Employee {name},\n\nIT has identified you as a power user. Confirm your device list to complete enrollment.\n\n[Confirm Devices]",
    "medium", "IT Support", "Device inventory request, potential reconnaissance", 1),

    ("Employee of the Month Cyber Edition",
    "Cyber Hygiene Recognition – Employee of the Month",
    "Dear Employee of the Month {name},\n\nView your latest phishing simulation performance and recommended learning modules.\n\n[View Cyber Hygiene Report]",
    "medium", "IT Support", "Security report pretext + link", 1),

    ("Valued Security Partner",
    "Security Partner Feedback Request",
    "Dear Valued Team Member {name},\n\nProvide feedback on recent MFA and VPN changes.\n\n[Give Security Feedback]",
    "easy", "IT Support", "Security feedback lure, external form", 1),

    ("Distinguished Incident Responder",
    "Incident Simulation Role for Distinguished Staff",
    "Dear Distinguished Staff Member {name},\n\nYou have been assigned a role in our upcoming incident response simulation. Review your role and tasks:\n\n[View IR Role]",
    "hard", "IT Support", "Incident response pretext, fake portal", 1),

    # === CORPORATE (extra personalized 10) ===
    ("Corporate Travel Reminder",
    "Action Required: Updated Travel Policy Acknowledgment",
    "Dear {name},\n\nOur records show you have not yet acknowledged the updated corporate travel policy. Please review and confirm using the link below.\n\n[Review Travel Policy]\n\nThank you,\nCorporate Compliance",
    "medium", "Corporate", "Personalized greeting, policy link, urgency", 1),

    ("Executive Town Hall Invite",
    "Invitation: Executive Town Hall with Leadership",
    "Hi {name},\n\nYou've been invited to our upcoming executive town hall. Reserve your virtual seat below.\n\n[Reserve Seat]\n\nSeats are limited.",
    "easy", "Corporate", "Vague event details, external link", 1),

    ("Remote Work Policy Check",
    "Remote Work Agreement – Signature Needed",
    "Dear {name},\n\nYour remote work agreement is pending digital signature. Please sign before the end of the day.\n\n[Sign Agreement]",
    "medium", "Corporate", "Fake e-signature portal, urgency", 1),

    ("Corporate Card Verification",
    "Corporate Card Transaction Verification",
    "Hi {name},\n\nA recent transaction on your corporate card needs verification. Confirm whether you recognize this charge.\n\n[Verify Transaction]",
    "hard", "Corporate", "Financial scare tactic, credential harvest", 1),

    ("Internal Newsletter Access",
    "View Your Personalized Corporate Newsletter",
    "Dear {name},\n\nYour personalized corporate newsletter for this month is ready. View it at the link below.\n\n[View Newsletter]",
    "easy", "Corporate", "Link to fake content portal", 1),

    ("Confidential Project Access",
    "You've Been Added to Project 'Skyline' Workspace",
    "Hi {name},\n\nYou've been granted access to a confidential strategic project workspace. Log in to review assigned documents.\n\n[Open Workspace]",
    "hard", "Corporate", "Tempting access, fake doc workspace", 1),

    ("Corporate Survey Targeted",
    "Short 3-Question Survey About Your Role",
    "Dear {name},\n\nWe're running a brief survey specific to your position. Your answers will help guide leadership decisions.\n\n[Start Survey]",
    "easy", "Corporate", "Survey lure, external form", 1),

    ("Document Approval Required",
    "Approval Needed: Updated Department Charter",
    "Hi {name},\n\nYou have been listed as an approver for your department's updated charter. Please review and approve.\n\n[Review Charter]",
    "medium", "Corporate", "Fake document sign-off", 1),

    ("Corporate Identity Check",
    "Identity Verification for Internal Systems",
    "Dear {name},\n\nAs part of our quarterly compliance review, please verify your identity to retain access to internal portals.\n\n[Verify Identity]",
    "hard", "Corporate", "Sensitive info request, fake SSO", 1),

    ("Board Meeting Notes",
    "Pre-Release: Board Meeting Notes for Review",
    "Hi {name},\n\nYou have early access to the latest board meeting notes. Download them using the secure link below.\n\n[Download Notes]",
    "medium", "Corporate", "Attachment/download lure, privileged info", 1),

    # === HR (extra personalized 10) ===
    ("Update Emergency Contact",
    "Action Needed: Emergency Contact Information",
    "Dear {name},\n\nYour emergency contact details are incomplete. Please update them through the secure HR form below.\n\n[Update Emergency Contact]",
    "medium", "HR", "Personal data request, fake HR form", 1),

    ("Policy Violation Review",
    "Policy Compliance Review – Response Requested",
    "Hi {name},\n\nA recent activity associated with your account has triggered a policy review. Please provide acknowledgment.\n\n[View Details]",
    "hard", "HR", "Fear, vague violation, login link", 1),

    ("Training Reminder – Diversity",
    "Reminder: Diversity & Inclusion Training Due",
    "Dear {name},\n\nYou still have one pending Diversity & Inclusion module. Complete it here:\n\n[Continue Training]",
    "easy", "HR", "Training portal impersonation", 1),

    ("Emergency Drill Acknowledgment",
    "Mandatory Emergency Drill Confirmation",
    "Hi {name},\n\nConfirm that you've reviewed the emergency drill procedures for your location.\n\n[Confirm Review]",
    "medium", "HR", "Fake HR confirmation, simple CTA", 1),

    ("Attendance Policy Update",
    "Updated Attendance and Remote Work Guidelines",
    "Dear {name},\n\nWe've updated our attendance and hybrid work guidelines. Please review and acknowledge.\n\n[Review Policy]",
    "medium", "HR", "Policy link, fake HR portal", 1),

    ("HR One-on-One Scheduling",
    "Schedule Your HR Check-In",
    "Hi {name},\n\nYou've been selected for a brief HR well-being check-in. Choose a time slot using the scheduler below.\n\n[Schedule Meeting]",
    "easy", "HR", "Fake scheduling app", 1),

    ("Performance Bonus Preview",
    "Preliminary Bonus Estimate Available",
    "Dear {name},\n\nYour preliminary performance bonus estimate is now ready. View it here:\n\n[View Estimate]",
    "hard", "HR", "Money lure, fake login page", 1),

    ("Remote Location Verification",
    "Confirm Remote Work Location",
    "Hi {name},\n\nTo stay compliant with labor regulations, confirm your current work location.\n\n[Confirm Location]",
    "medium", "HR", "Location and personal info request", 1),

    ("Wellness Program Enrollment",
    "Enroll in the New Employee Wellness Program",
    "Dear {name},\n\nSign up for our wellness program and access exclusive benefits.\n\n[Enroll Now]",
    "easy", "HR", "Enrollment lure, external form", 1),

    ("HR Document Signature",
    "Signature Required: Updated Employee Handbook",
    "Hi {name},\n\nPlease sign the updated employee handbook by the end of the week.\n\n[Sign Handbook]",
    "medium", "HR", "Fake document signing portal", 1),

    # === DIGITAL TECHNOLOGY (extra personalized 10) ===
    ("New Device Login Detected",
    "Alert: New Device Logged In to Your Account",
    "Hi {name},\n\nWe detected a new device accessing your corporate account. If this was not you, secure your account now.\n\n[Secure My Account]",
    "hard", "Digital Technology", "Security scare, fake reset link", 1),

    ("API Key Rotation Required",
    "Action Required: Rotate Your API Keys",
    "Dear {name},\n\nYour API keys are due for rotation under new security policy. Complete the rotation here:\n\n[Rotate Keys]",
    "medium", "Digital Technology", "Developer-focused, fake dev portal", 1),

    ("Dev Environment Access",
    "Sandbox Environment Upgrade – Re-Login Needed",
    "Hi {name},\n\nThe development sandbox has been upgraded. Log in to restore your access.\n\n[Log In to Sandbox]",
    "easy", "Digital Technology", "Fake dev environment login", 1),

    ("Code Review Notice",
    "Automated Security Review Flagged Your Commit",
    "Dear {name},\n\nOur automated scanner flagged a recent commit for potential secrets exposure. View details:\n\n[Review Commit]",
    "hard", "Digital Technology", "Code/security lure, link to fake dashboard", 1),

    ("SSO Token Renewal",
    "Single Sign-On Token Expiring",
    "Hi {name},\n\nYour SSO token will expire in 12 hours. Re-authenticate now:\n\n[Re-Authenticate]",
    "medium", "Digital Technology", "SSO impersonation", 1),

    ("DevOps Dashboard Access",
    "You've Been Granted Access to DevOps Insights",
    "Dear {name},\n\nYou now have access to the internal DevOps monitoring dashboard.\n\n[Open Dashboard]",
    "easy", "Digital Technology", "Tempting new access", 1),

    ("Security Scan Results",
    "Vulnerability Scan Report Available",
    "Hi {name},\n\nThe latest vulnerability scan is complete. Download your assigned findings:\n\n[Download Report]",
    "medium", "Digital Technology", "Fake security report", 1),

    ("SSH Key Compliance",
    "SSH Key Format Non-Compliant",
    "Dear {name},\n\nYour registered SSH key does not meet current security standards. Upload a new key:\n\n[Upload SSH Key]",
    "hard", "Digital Technology", "Technical lure, credential-adjacent", 1),

    ("Collaboration Tool Migration",
    "Teams to Slack Migration – Action Needed",
    "Hi {name},\n\nWe are migrating collaboration tools. Confirm your new workspace:\n\n[Confirm Workspace]",
    "easy", "Digital Technology", "Fake tool migration link", 1),

    ("Access Request Auto-Approval",
    "Your Access Request Has Been Auto-Approved",
    "Dear {name},\n\nYour recent permission request was auto-approved. Review and confirm your new permissions.\n\n[View Permissions]",
    "medium", "Digital Technology", "Permission/role lure", 1),

    # === AIRCRAFT MAINTENANCE AND SUPPORT (extra personalized 10) ===
    ("Hangar Access Log Review",
    "Review Required: Hangar Access Activity",
    "Dear {name},\n\nYour hangar access log shows unusual patterns. Please review and confirm activity.\n\n[View Access Log]",
    "hard", "Aircraft Maintenance and Support", "Security/fear tactic, fake portal", 1),

    ("Tool Cage Inventory",
    "Tool Checkout Report Pending Confirmation",
    "Hi {name},\n\nYour recent tool checkout list is pending confirmation. Please verify items:\n\n[Verify Tools]",
    "medium", "Aircraft Maintenance and Support", "Log verification link", 1),

    ("Engine Logbook Update",
    "Engine Log Entry Requires Your Signature",
    "Dear {name},\n\nAn engine maintenance entry has been assigned to you for sign-off.\n\n[Sign Log Entry]",
    "medium", "Aircraft Maintenance and Support", "Fake logbook sign-off", 1),

    ("Maintenance Shift Swap",
    "Shift Swap Request from Colleague",
    "Hi {name},\n\nA colleague has requested a shift swap with you. Review the details and approve or decline.\n\n[Review Swap Request]",
    "easy", "Aircraft Maintenance and Support", "Social lure, fake shift system", 1),

    ("Safety Checklist Update",
    "Updated Pre-Flight Safety Checklist",
    "Dear {name},\n\nThe pre-flight safety checklist has been revised. Download and review before your next shift.\n\n[Download Checklist]",
    "medium", "Aircraft Maintenance and Support", "Fake doc download", 1),

    ("Parts Inventory Discrepancy",
    "Inventory Mismatch Detected",
    "Hi {name},\n\nA mismatch was detected in your parts inventory allocation. Confirm your allocations:\n\n[Review Inventory]",
    "hard", "Aircraft Maintenance and Support", "Fake audit/scare tactic", 1),

    ("Hangar Access Badge Audit",
    "Badge Audit – Confirm Active Mechanics",
    "Dear {name},\n\nAs part of a hangar security audit, confirm which mechanics are assigned under your supervision.\n\n[Confirm Assignments]",
    "medium", "Aircraft Maintenance and Support", "Fake HR/security data collection", 1),

    ("Maintenance Photo Upload",
    "Photo Evidence Missing for Recent Work Order",
    "Hi {name},\n\nPhoto evidence of a completed maintenance task is missing. Upload photos now:\n\n[Upload Photos]",
    "easy", "Aircraft Maintenance and Support", "File upload lure", 1),

    ("Spare Parts Rush Order",
    "Rush Order Requires Your Approval",
    "Dear {name},\n\nA rush order for critical spare parts was placed under your ID. Approve or reject:\n\n[Review Order]",
    "hard", "Aircraft Maintenance and Support", "Financial + operational lure", 1),

    ("Maintenance Training Quiz",
    "Refresher Quiz on Updated Procedures",
    "Hi {name},\n\nComplete this short quiz on updated maintenance procedures to maintain certification.\n\n[Start Quiz]",
    "medium", "Aircraft Maintenance and Support", "Fake LMS/training link", 1),

    # === CUSTOMER SOLUTIONS (extra personalized 10) ===
    ("Customer Call Recording Review",
    "Call Recording Flagged for Quality Review",
    "Dear {name},\n\nOne of your recent customer calls has been flagged for review. Listen and provide feedback.\n\n[Review Call]",
    "hard", "Customer Solutions", "Fake QA portal, fear and curiosity", 1),

    ("Chat Transcript Download",
    "Export of Recent Chat Transcripts Ready",
    "Hi {name},\n\nYour requested chat transcript export is ready for download.\n\n[Download Transcripts]",
    "medium", "Customer Solutions", "File download lure", 1),

    ("Escalation Procedure Update",
    "New Customer Escalation Procedure",
    "Dear {name},\n\nWe've updated our escalation procedure for high-priority cases. Review here:\n\n[Review Procedure]",
    "easy", "Customer Solutions", "Policy/training impersonation", 1),

    ("Customer Satisfaction Warning",
    "Low Satisfaction Score – Action Needed",
    "Hi {name},\n\nYour recent satisfaction scores are below the team average. Review feedback and recommendations.\n\n[View Feedback]",
    "hard", "Customer Solutions", "Fear/emotional pressure", 1),

    ("Outbound Campaign Assignment",
    "You've Been Assigned to a New Customer Campaign",
    "Dear {name},\n\nA new outbound campaign has been assigned to you. Access the campaign details:\n\n[Open Campaign]",
    "medium", "Customer Solutions", "Fake marketing/campaign dashboard", 1),

    ("Knowledge Base Article Draft",
    "Draft Article Assigned for Your Review",
    "Hi {name},\n\nReview and approve the attached customer support article assigned to you.\n\n[Review Article]",
    "easy", "Customer Solutions", "Fake doc link", 1),

    ("Case Ownership Transfer",
    "Case Ownership Request Pending Approval",
    "Dear {name},\n\nAnother agent has requested to transfer a case to you. Approve or decline:\n\n[Manage Transfer]",
    "medium", "Customer Solutions", "Workflow impersonation", 1),

    ("Customer Refund Audit",
    "Refund Approved Under Your ID",
    "Hi {name},\n\nA high-value refund was approved under your ID. Verify that this is correct.\n\n[Verify Refund]",
    "hard", "Customer Solutions", "Financial + accountability scare", 1),

    ("Priority SLA Reminder",
    "Priority Ticket SLA Approaching Breach",
    "Dear {name},\n\nA priority ticket assigned to you is close to breaching its SLA. Update status:\n\n[Update Ticket]",
    "medium", "Customer Solutions", "Fake ticketing system link", 1),

    ("Customer Follow-Up Task",
    "Reminder: Pending Follow-Up with Passenger",
    "Hi {name},\n\nYou have a pending follow-up with a passenger from last week. Log your follow-up notes:\n\n[Log Follow-Up]",
    "easy", "Customer Solutions", "Reminder style, fake CRM link", 1),

    # === AT THE AIRPORT (extra personalized 10) ===
    ("Security Line Staffing",
    "Staffing Adjustment for Security Checkpoint",
    "Dear {name},\n\nYour shift assignment at the security checkpoint has changed. View details below.\n\n[View New Assignment]",
    "medium", "At the Airport", "Fake staffing system", 1),

    ("Ramp Safety Video",
    "New Ramp Safety Video – Please Watch",
    "Hi {name},\n\nWatch this updated ramp safety briefing before your next shift.\n\n[Watch Video]",
    "easy", "At the Airport", "Video/training lure", 1),

    ("Luggage Tagging Audit",
    "Audit: Baggage Tagging Irregularity",
    "Dear {name},\n\nAn irregularity was detected in luggage tagging during your shift. Review and acknowledge.\n\n[Review Irregularity]",
    "hard", "At the Airport", "Fear, fake audit portal", 1),

    ("Gate Change Script",
    "New Passenger Announcement Script",
    "Hi {name},\n\nA new script for gate change announcements has been released. Download and review:\n\n[Download Script]",
    "medium", "At the Airport", "Doc download lure", 1),

    ("Staff Shuttle Update",
    "Airport Staff Shuttle Route Change",
    "Dear {name},\n\nStaff shuttle times and stops have been updated. Check the new schedule.\n\n[View Shuttle Schedule]",
    "easy", "At the Airport", "Operational info lure", 1),

    ("Ramp Access Violation",
    "Unauthorized Ramp Access Logged",
    "Hi {name},\n\nYour badge was used for ramp access outside scheduled hours. Confirm if this was you.\n\n[Confirm Activity]",
    "hard", "At the Airport", "Security scare, fake portal", 1),

    ("Boarding Priority Change",
    "New Boarding Priority Procedure",
    "Dear {name},\n\nBoarding priority procedures have changed. Learn the new order here:\n\n[View Procedure]",
    "medium", "At the Airport", "Policy/training link", 1),

    ("Lost & Found Case Assignment",
    "New Lost Item Case Assigned to You",
    "Hi {name},\n\nYou've been assigned a new lost item case. Access it below:\n\n[Open Case]",
    "easy", "At the Airport", "Fake case management portal", 1),

    ("Security Drill Confirmation",
    "Participation Required: Terminal Security Drill",
    "Dear {name},\n\nConfirm your participation in the upcoming security drill.\n\n[Confirm Participation]",
    "medium", "At the Airport", "Drill/meeting lure", 1),

    ("Gate Signage Issue",
    "Passenger Confusion Report – Gate Signage",
    "Hi {name},\n\nA passenger confusion report was filed regarding gate signage during your shift. Review and respond.\n\n[Review Report]",
    "hard", "At the Airport", "Reputation/emotional pressure", 1),

    # === FLIGHT ATTENDANT (extra personalized 10) ===
    ("Crew Briefing Notes",
    "New Pre-Flight Briefing Notes Available",
    "Dear {name},\n\nUpdated briefing notes for your next rotation are now available.\n\n[View Briefing Notes]",
    "easy", "Flight Attendant", "Training/ops doc lure", 1),

    ("Cabin Service Feedback",
    "Passenger Feedback on Your Recent Flight",
    "Hi {name},\n\nPassenger comments have been logged for your last flight. Review them here:\n\n[View Passenger Feedback]",
    "hard", "Flight Attendant", "Emotional hook, fake HR portal", 1),

    ("Crew Mobile App Update",
    "New Version of Crew Mobile App",
    "Dear {name},\n\nA new version of the crew mobile app is available. Install it now:\n\n[Download App]",
    "medium", "Flight Attendant", "Fake app download", 1),

    ("Meal Service Change",
    "Updated Meal Service Procedure",
    "Hi {name},\n\nWe've updated procedures for premium cabin meal service. Review the changes:\n\n[View Procedure]",
    "easy", "Flight Attendant", "Ops/training link", 1),

    ("Special Assistance Passenger",
    "Passenger Requiring Special Assistance Assigned",
    "Dear {name},\n\nYour next flight includes a passenger requiring special assistance. Review the details:\n\n[View Passenger Details]",
    "medium", "Flight Attendant", "Data/curiosity lure", 1),

    ("Cabin Safety Check",
    "Safety Checklist Confirmation Needed",
    "Hi {name},\n\nConfirm that you've completed the updated cabin safety checklist.\n\n[Confirm Checklist]",
    "medium", "Flight Attendant", "Compliance/training style", 1),

    ("Crew Swap Request",
    "Crew Swap Request Pending Your Approval",
    "Dear {name},\n\nAnother crew member has requested to swap a rotation with you. Review the details below.\n\n[Review Swap]",
    "easy", "Flight Attendant", "Social/workflow lure", 1),

    ("Service Recovery Voucher",
    "Service Recovery Voucher Issued Under Your ID",
    "Hi {name},\n\nA service recovery voucher was issued under your ID. Confirm this is correct.\n\n[Confirm Voucher]",
    "hard", "Flight Attendant", "Financial + accountability scare", 1),

    ("Cabin Announcement Update",
    "New Standard Cabin Announcement Scripts",
    "Dear {name},\n\nNew standardized scripts for cabin announcements are available. Download them here:\n\n[Download Scripts]",
    "medium", "Flight Attendant", "Attachment/doc lure", 1),

    ("Crew Satisfaction Survey",
    "Share Your Feedback About Recent Flight",
    "Hi {name},\n\nTell us about your recent experience with your flight crew.\n\n[Take Survey]",
    "easy", "Flight Attendant", "Survey/link lure", 1),

    # === PILOT OPERATIONS (extra personalized 10) ===
    ("Route Deviation Review",
    "Flight Path Deviation Logged for Review",
    "Dear {name},\n\nATC logs show a minor deviation from the planned route. Review the record:\n\n[View ATC Log]",
    "hard", "Pilot Operations", "Authority/fear tactic, fake ATC log", 1),

    ("Crew Briefing Packet",
    "Updated Briefing Packet for Upcoming Flight",
    "Hi {name},\n\nDownload the latest briefing packet for your assigned route.\n\n[Download Packet]",
    "easy", "Pilot Operations", "Doc download lure", 1),

    ("Runway Change Notice",
    "Runway Change for Departure",
    "Dear {name},\n\nDeparture runway has been updated. Confirm new data in your flight prep.\n\n[View Runway Details]",
    "medium", "Pilot Operations", "Operational change lure", 1),

    ("Fuel Uplift Confirmation",
    "Fuel Uplift Discrepancy Detected",
    "Hi {name},\n\nThe recorded fuel uplift does not match the dispatch estimate. Verify your log:\n\n[Verify Fuel Log]",
    "hard", "Pilot Operations", "Technical plus accountability pressure", 1),

    ("Crew Rest Compliance",
    "Duty and Rest Compliance Check",
    "Dear {name},\n\nConfirm that your duty and rest periods meet regulatory requirements.\n\n[Confirm Compliance]",
    "medium", "Pilot Operations", "Regulatory scare, fake portal", 1),

    ("Route Optimization Trial",
    "Try New Fuel-Saving Route Profile",
    "Hi {name},\n\nYou've been selected to trial a new fuel-efficient route profile.\n\n[View Route Profile]",
    "easy", "Pilot Operations", "Experiment/innovation lure", 1),

    ("Flight Debrief Upload",
    "Debrief Notes Required for Last Sector",
    "Dear {name},\n\nUpload your debrief notes for your previous sector.\n\n[Upload Debrief]",
    "medium", "Pilot Operations", "Upload lure to fake portal", 1),

    ("Simulator Evaluation Results",
    "Simulator Evaluation Summary Available",
    "Hi {name},\n\nYour latest simulator evaluation summary is available to view.\n\n[View Evaluation]",
    "hard", "Pilot Operations", "Performance/emotional hook", 1),

    ("Navigation Database Update",
    "Nav Database Out of Date",
    "Dear {name},\n\nYour navigation database appears out of date. Download the latest cycle here:\n\n[Download NavData]",
    "medium", "Pilot Operations", "Tech update, fake download", 1),

    ("Crew Messaging Platform",
    "New Messaging Feature for Flight Crew",
    "Hi {name},\n\nTest the new internal messaging feature for pilots and crew members.\n\n[Try Messaging]",
    "easy", "Pilot Operations", "New feature lure", 1),

    # === FINANCE (extra personalized 10) ===
    ("Vendor Payment Mismatch",
    "Vendor Payment Amount Mismatch Detected",
    "Dear {name},\n\nA discrepancy was found in a vendor payment processed under your approval. Review details:\n\n[Review Payment]",
    "hard", "Finance", "Fear, financial accountability", 1),

    ("Cost Center Reassignment",
    "Your Cost Center Has Been Updated",
    "Hi {name},\n\nYour assigned cost center has been updated. Confirm the change:\n\n[View Cost Center]",
    "medium", "Finance", "Finance system impersonation", 1),

    ("Travel Expense Policy Reminder",
    "Updated Travel Expense Policy",
    "Dear {name},\n\nPlease review the updated travel expense policy for future claims.\n\n[Review Policy]",
    "easy", "Finance", "Policy link, simple CTA", 1),

    ("Corporate Card Limit Alert",
    "Corporate Card Limit Nearly Reached",
    "Hi {name},\n\nYour corporate card is nearing its monthly limit. View recent charges:\n\n[View Charges]",
    "medium", "Finance", "Finance portal lure", 1),

    ("Budget Overrun Warning",
    "Department Budget Approaching Overrun",
    "Dear {name},\n\nYour department's spend is close to exceeding its current budget.\n\n[Review Budget Usage]",
    "hard", "Finance", "Scare tactic, financial risk", 1),

    ("Tax Document Download",
    "New Year-End Tax Document Available",
    "Hi {name},\n\nYour year-end tax document is ready for download.\n\n[Download Document]",
    "easy", "Finance", "Tax/official doc lure", 1),

    ("Reconciliation Task Assigned",
    "Bank Reconciliation Task Assigned to You",
    "Dear {name},\n\nYou've been assigned to review a bank reconciliation file.\n\n[Open Reconciliation File]",
    "medium", "Finance", "Fake accounting system link", 1),

    ("Invoice Dispute Case",
    "New Invoice Dispute Filed",
    "Hi {name},\n\nA vendor has disputed an invoice under your cost center. Review and respond.\n\n[Review Dispute]",
    "hard", "Finance", "Dispute/pressure tactic", 1),

    ("Finance Portal Maintenance",
    "Planned Downtime – Verify Access",
    "Dear {name},\n\nVerify your login details before the finance portal maintenance window.\n\n[Verify Login]",
    "medium", "Finance", "Fake 'prevent lockout' login", 1),

    ("Internal Chargeback Notice",
    "Internal Chargeback Logged to Your Team",
    "Hi {name},\n\nAn internal chargeback has been logged to your team's account. View the breakdown:\n\n[View Chargeback]",
    "medium", "Finance", "Expense/conflict-triggering lure", 1),

    # === IT SUPPORT (extra personalized 10) ===
    ("Shared Drive Access Request",
    "New Shared Drive Access Requested",
    "Dear {name},\n\nA team member has requested access to a shared drive you manage. Approve or deny below.\n\n[Manage Request]",
    "medium", "IT Support", "Fake helpdesk/approval portal", 1),

    ("Endpoint Detection Alert",
    "Suspicious Activity on Your Device",
    "Hi {name},\n\nOur endpoint protection system detected suspicious activity on your workstation. Review incident details:\n\n[View Incident]",
    "hard", "IT Support", "Security scare, fake SOC link", 1),

    ("Software Install Approval",
    "Software Installation Request Pending",
    "Dear {name},\n\nApprove or deny the pending software install request submitted from your account.\n\n[Review Request]",
    "medium", "IT Support", "Fake IT workflow", 1),

    ("Browser Extension Blocked",
    "Unapproved Browser Extension Disabled",
    "Hi {name},\n\nAn unapproved browser extension was disabled on your device. Review extension details:\n\n[View Extension]",
    "easy", "IT Support", "Fake security notice", 1),

    ("Phishing Simulation Result",
    "Your Phishing Test Results Are Available",
    "Dear {name},\n\nView your latest phishing simulation performance and recommended learning modules.\n\n[View Results]",
    "hard", "IT Support", "Meta-phishing about phishing, login link", 1),

    ("Wi-Fi Certificate Renewal",
    "Corporate Wi-Fi Certificate Expiring",
    "Hi {name},\n\nRenew your Wi-Fi certificate now to avoid connectivity issues.\n\n[Renew Certificate]",
    "medium", "IT Support", "Network/IT impersonation", 1),

    ("Ticket Auto-Closure Warning",
    "IT Ticket Will Auto-Close Soon",
    "Dear {name},\n\nYour open ticket will auto-close in 24 hours. Update status if the issue persists.\n\n[Update Ticket]",
    "easy", "IT Support", "Ticketing workflow lure", 1),

    ("Security Policy Acceptance",
    "New Endpoint Security Policy – Acceptance Required",
    "Hi {name},\n\nAccept the latest endpoint security policy to remain compliant.\n\n[Accept Policy]",
    "medium", "IT Support", "Policy + login prompt", 1),

    ("Password Reuse Alert",
    "Password Reuse Detected on Multiple Systems",
    "Dear {name},\n\nWe detected password reuse across internal systems. Change your password now.\n\n[Change Password]",
    "hard", "IT Support", "Security scare, fake reset portal", 1),

    ("IT Feedback Request",
    "Tell Us About Your Recent IT Support Experience",
    "Hi {name},\n\nComplete this quick survey to rate your recent IT support interaction.\n\n[Complete Survey]",
    "easy", "IT Support", "Survey lure, light red flags", 1),

    # === CORPORATE (extra 10, varied quality) ===
    ("Internal Townhall Stream Link",
    "Today's Virtual Townhall – Updated Stream Link",
    "Hi {name},\n\nThe streaming link for today's virtual townhall with leadership has been updated due to a technical issue. Please use the new link below to join:\n\n[Join Townhall Stream]\n\nDo not share this link outside the company.",
    "medium", "Corporate", "Last-minute link change, urgency, no proper domain mention", 1),

    ("Confidential Route Profit Leak",
    "Confidential: Internal Route Profitability Leak Investigation",
    "Dear {name},\n\nWe are investigating a potential leak of internal route profitability documents. You were on the distribution list. Please confirm which files you accessed using the log below.\n\n[Open Access Log]\n\nThis is confidential, do not forward.",
    "hard", "Corporate", "Fear, confidential investigation, login/log review", 1),

    ("Staff-Only Discount Clarification",
    "Clarification: Staff Travel Discount Misuse",
    "Hi {name},\n\nThere may have been misunderstanding with internal staff travel discount codes. Review the updated policy and confirm you understand it.\n\n[Review Staff Discount Policy]",
    "medium", "Corporate", "Subtle accusation, policy link, generic host", 1),

    ("Internal Newsletter Draft Review",
    "Review Draft: Corporate Newsletter (Unpublished)",
    "Hey {name},\n\nWe accidentally sent you the unpublished draft of the corporate newsletter last week. Please log in and confirm that you've deleted and acknowledged the correct version here:\n\n[Confirm Newsletter Deletion]\n\nThanks,\nComms Team",
    "easy", "Corporate", "Friendly tone, unnecessary login to confirm deletion", 1),

    ("Sustainability Ranking Notification",
    "Your Department's Sustainability Performance Ranking",
    "Dear {name},\n\nOur sustainability team has ranked departments according to fuel, waste and travel footprint. View your department's confidential ranking:\n\n[View Sustainability Rank]",
    "medium", "Corporate", "Appeals to curiosity, 'confidential ranking' + link", 1),

    ("Board Meeting Prep Pack",
    "Confidential: Prep Materials for Next Board Meeting",
    "Dear {name},\n\nYou've been added to the distribution list for board preparation materials by mistake. Please open the secure folder below and confirm you have not downloaded anything.\n\n[Open Secure Folder]\n\nIf you already downloaded, contact us immediately.",
    "hard", "Corporate", "Reverse-psychology: 'don't access', but link right there", 1),

    ("New Airline Branding Teaser",
    "Sneak Peek: New Brand and Livery Concepts",
    "Hi {name},\n\nYou are one of a limited group invited to preview our new livery and branding concepts before public reveal.\n\n[Preview Branding Deck]",
    "easy", "Corporate", "Tempting sneak-peek, vague security, external deck link", 1),

    ("Corporate Phone Directory Verification",
    "Verify Your Contact Details in Corporate Directory",
    "Dear {name},\n\nOur phone and contact directory is outdated. Please verify your number, extension and base location using this quick verification page.\n\n[Verify Contact Info Now]\n\nFailing to update may result in missed important calls.",
    "medium", "Corporate", "Data-harvest form hidden as contact verification", 1),

    ("Important internal notice",
    "IMPORTANT: Internal Matter (Read Fast)",
    "Dear {name},\n\nThis is a urgent internal notice, your department is affected by upcoming changes and you MUST read and sign the attached agreement before today end-of-day.\n\n[Open Internal Agreement]\n\nDo not ignore this or HR will be notified.",
    "hard", "Corporate", "Bad grammar, aggressive tone, fear, vague threat", 1),

    ("Leadership Photo Consent",
    "Photo / Media Consent for Internal & External Use",
    "Hi {name},\n\nYour photo may be used in internal and external airline media materials. Confirm your consent and upload a recent headshot below:\n\n[Confirm & Upload Photo]",
    "medium", "Corporate", "Image upload + consent, possible exfiltration", 1),

    # === HR (extra 10, varied quality) ===
    ("Crew Fatigue Self-Report Form",
    "Mandatory Fatigue Self-Assessment for Airline Staff",
    "Dear {name},\n\nIn preparation for the new schedule, HR requires you to complete a confidential fatigue self-assessment.\n\n[Complete Fatigue Assessment]\n\nYour responses will remain private, but non-completion will be flagged.",
    "medium", "HR", "'Confidential' but with completion threat; health data", 1),

    ("Incorrect bank info detected",
    "We detect wrong bank informations in your payroll",
    "Hello {name},\n\nOur system is showing a error with your bank informations for last payroll deposit. Please fix it now to avoid delay.\n\n[Fix Bank Info]\n\nThis is automatic message, do not ignore.",
    "hard", "HR", "Bad grammar, money urgency, direct banking info request", 1),

    ("Airport Relocation Bonus Survey",
    "Potential Relocation Bonus – Confirmation Needed",
    "Hi {name},\n\nYou may be eligible for a relocation bonus if you move to support a different hub. Confirm your interest and preferred city:\n\n[Confirm Relocation Interest]",
    "medium", "HR", "Enticing relocation bonus with data capture", 1),

    ("Leave Freeze Notification",
    "Temporary Leave Freeze for Operational Reasons",
    "Dear {name},\n\nDue to operational needs, leave approvals may be restricted over the upcoming peak period. Please review the freeze calendar and acknowledge.\n\n[Review Leave Freeze Calendar]",
    "easy", "HR", "Operational-sounding, requires login/acknowledge", 1),

    ("Employee hotline case",
    "Confidential Hotline Report Involving Your Name",
    "Dear {name},\n\nA confidential hotline report has referenced your name. HR needs you to review and acknowledge the summary.\n\n[View Confidential Summary]\n\nDo not discuss this with other employees.",
    "hard", "HR", "Heavy fear/curiosity bait, 'hotline' mention", 1),

    ("Annual medical exam questionnaire",
    "Questionnaire: Annual Medical & Vaccination Status",
    "Hi {name},\n\nPlease fill out the annual medical exam questionnaire for staff working in airport and inflight areas.\n\n[Open Medical Questionnaire]\n\nThis is urgent for compliance reason.",
    "medium", "HR", "Health data, multiple typos, fake compliance angle", 1),

    ("Crew Base Swap Program",
    "Sign Up: Voluntary Crew Base Swap Program",
    "Dear {name},\n\nHR is piloting a voluntary base swap program. If you'd like to trade bases with other staff, register your interest here:\n\n[Register for Base Swap]",
    "easy", "HR", "Interesting opportunity, collects personal preferences", 1),

    ("Unapproved overtime hours",
    "Overtime Discrepancy Detected – Please Confirm",
    "Hello {name},\n\nOur system has flagged unapproved overtime associated with your profile. Confirm whether these hours are valid.\n\n[Confirm Overtime Hours]",
    "hard", "HR", "Accusatory overtime discrepancy, fear + data", 1),

    ("New child travel benefit",
    "Update: Child Flight Benefit & Standby Policy",
    "Hi {name},\n\nWe've updated policies related to staff children flying on discounted or standby tickets. Review and confirm your dependents' details.\n\n[Update Dependent Details]",
    "medium", "HR", "Children/family angle, very sensitive personal data", 1),

    ("Mandatory DEI Webinar Attendance",
    "Mandatory Diversity & Inclusion Webinar – Attendance Check",
    "Dear {name},\n\nYou are required to attend the upcoming DEI webinar. Confirm your preferred session time below:\n\n[Select DEI Session]",
    "easy", "HR", "Mandatory training theme, form link", 1),

    # === DIGITAL TECHNOLOGY (extra 10, varied quality) ===
    ("Pilot iPad Config Profile",
    "New EFB Configuration Profile for Flight Devices",
    "Dear {name},\n\nDownload and install the new EFB configuration profile for pilot iPads before your next duty.\n\n[Download Config Profile]\n\nFailure to update may cause app failures.",
    "hard", "Digital Technology", "Device profile download, high-value tech target", 1),

    ("Crew Chat Beta App",
    "Try the New Internal Crew Chat App",
    "Hi {name},\n\nIT has launched a beta version of a secure crew chat application for easier communication.\n\n[Download Crew Chat Beta]",
    "medium", "Digital Technology", "New app lure, APK/EXE risk", 1),

    ("Weak password found",
    "Security Alert: Weak Password Detected",
    "Dear {name},\n\nOur internal scan showed your password does not meet new airline security policy. Update now:\n\n[Update Password Now]\n\nThis is urgent for your account safety.",
    "hard", "Digital Technology", "Typos, fake security scan, direct password reset", 1),

    ("Data center migration notice",
    "Data Center Migration – Manual Re-Login Required",
    "Hi {name},\n\nAfter data center migration, your account must be revalidated in the internal portal. Please log in once to re-register.\n\n[Revalidate Account]",
    "medium", "Digital Technology", "Infra jargon, revalidation = credential harvest", 1),

    ("GDS Integration Patch",
    "Patch Required for GDS Integration Errors",
    "Dear {name},\n\nWe've identified intermittent failures on GDS integration for certain PNRs. Install the patch to fix these errors.\n\n[Install GDS Patch]",
    "hard", "Digital Technology", "Specific airline tech (GDS, PNR), malicious download", 1),

    ("Bug bounty invite",
    "Invitation: Internal Bug Bounty for Airline Systems",
    "Hi {name},\n\nYou're invited to participate in an internal bug bounty program for our booking and crew systems. Access the portal here:\n\n[Join Bug Bounty Portal]",
    "medium", "Digital Technology", "Security-themed, dev-targeted portal", 1),

    ("Test profile for passengers app",
    "Create Test Profile for Passenger Mobile App",
    "Hello {name},\n\nWe need internal staff to create test profiles in the passenger app for a new feature. Log in and create a dummy profile.\n\n[Create Test Profile Now]",
    "easy", "Digital Technology", "Simple task, uses existing trust in passenger app", 1),

    ("Log archive full",
    "Log Archiving Failed – Storage Full",
    "Dear {name},\n\nLog archiving for your service has failed due to insufficient storage. Download the manual cleanup tool:\n\n[Download Cleanup Tool]",
    "hard", "Digital Technology", "Plausible log/ops tool with malware risk", 1),

    ("Single Sign-on issue for crew",
    "Crew SSO Issue – Temporary Alternate Login Link",
    "Hi {name},\n\nWe're experiencing issues with SSO for crew tools. Use the temporary login link below:\n\n[Temporary Crew Login]",
    "hard", "Digital Technology", "Alt login URL, bypassing SSO is huge red flag", 1),

    ("API sandbox credentials",
    "API Sandbox Credentials Regenerated",
    "Dear {name},\n\nYour sandbox API credentials have been rotated. View the new keys and secrets here:\n\n[View New API Keys]",
    "hard", "Digital Technology", "Directly going after API keys, high-value target", 1),

    # === AIRCRAFT MAINTENANCE AND SUPPORT (extra 10, varied quality) ===
    ("Hangar safety video",
    "New Hangar Safety Video – Must Watch",
    "Hi {name},\n\nWatch this short updated safety video before your next hangar shift.\n\n[Watch Safety Video]\n\nSign-off is required.",
    "easy", "Aircraft Maintenance and Support", "Video lure, sign-off requirement", 1),

    ("Corrosion inspection update",
    "Corrosion Inspection Protocol Change",
    "Dear {name},\n\nCorrosion inspection requirements for certain fleet types have changed. Review the updated protocol.\n\n[Review New Protocol]",
    "medium", "Aircraft Maintenance and Support", "Technical maintenance change, link to fake doc", 1),

    ("Wrong torque value detected",
    "Possible Incorrect Torque Values Submitted",
    "Hello {name},\n\nOur system flagged abnormal torque values on a recent work card under your ID. Confirm the entries below.\n\n[Confirm Torque Values]",
    "hard", "Aircraft Maintenance and Support", "Blaming mechanic, pushing them to click quickly", 1),

    ("Cabin defects backlog list",
    "Cabin Defect Backlog Assigned to Your Team",
    "Hi {name},\n\nA backlog of minor cabin defects has been auto-assigned to your maintenance group.\n\n[View Backlog List]",
    "medium", "Aircraft Maintenance and Support", "Backlog list, ops doc link", 1),

    ("Parts short shipment",
    "Parts Short-Shipment Notice – Action Required",
    "Dear {name},\n\nStores reported a short-shipment on parts requested under your station. Confirm whether this affects your open jobs.\n\n[Review Short-Shipment Details]",
    "medium", "Aircraft Maintenance and Support", "Inventory issue, encourages quick click", 1),

    ("Strange defect photos",
    "Unusual Defect Photos Need Your Review",
    "Hi {name},\n\nQuality control flagged strange defect photo attachments uploaded on your recent tasks. Please log in and review them.\n\n[View Defect Photos]",
    "hard", "Aircraft Maintenance and Support", "Attachment/photo curiosity hook", 1),

    ("Maintenance shift swap",
    "Urgent Maintenance Shift Swap Request",
    "Hello {name},\n\nAnother mechanic has requested to swap tonight's shift with you. Approve or decline now.\n\n[Review Shift Swap Request]",
    "easy", "Aircraft Maintenance and Support", "Common workflow, plausible UI", 1),

    ("Recurrent training overdue",
    "Overdue Recurrent Maintenance Training Module",
    "Dear {name},\n\nOur records show your recurrent training for structural repairs is overdue.\n\n[Complete Training Now]",
    "medium", "Aircraft Maintenance and Support", "Training compliance, urgency", 1),

    ("Unapproved tooling in use",
    "Alert: Unlisted Tooling Used for Task",
    "Hi {name},\n\nA recent work card shows tooling not on the approved list was used. Provide an explanation using the form:\n\n[Explain Tool Usage]",
    "hard", "Aircraft Maintenance and Support", "Compliance fear, form data capture", 1),

    ("Hydraulic leak incident review",
    "Incident Review: Hydraulic Leak Near Gate",
    "Dear {name},\n\nYou have been listed as part of the response team for a hydraulic leak event near your gate. Review the incident log and add comments.\n\n[Review Incident Log]",
    "medium", "Aircraft Maintenance and Support", "Incident review, ops and safety context", 1),

    # === CUSTOMER SOLUTIONS (extra 10, varied quality) ===
    ("Angry VIP passenger email",
    "Escalated: VIP Passenger Complaint Assigned to You",
    "Hi {name},\n\nA VIP passenger complaint has been escalated and assigned to your queue. Respond within the SLA.\n\n[Open VIP Complaint]",
    "hard", "Customer Solutions", "VIP, escalation, time pressure", 1),

    ("Mass delay call script",
    "Updated Script for Mass Weather Delays",
    "Dear {name},\n\nUse this updated script when communicating mass delays to customers due to storms.\n\n[Download New Script]",
    "medium", "Customer Solutions", "Operational script, doc download", 1),

    ("Refund rule reminder",
    "Important Reminder: Refund and Waiver Rules",
    "Hello {name},\n\nWe noticed some refunds may not comply with the latest waiver rules. Review this one-page summary.\n\n[View Refund and Waiver Summary]",
    "medium", "Customer Solutions", "Compliance flavor, hint of blame", 1),

    ("Very important customer escalation",
    "VERY IMPORTANT: Customer Escalation For You",
    "Dear {name},\n\nCustomer is very angry and wrote bad things about airline, you must fix this quickly.\n\n[Open Customer Case NOW]\n\nDo not ignore this message.",
    "hard", "Customer Solutions", "Bad grammar, urgency, emotional pressure", 1),

    ("Chat transcript quality check",
    "Quality Check: Recent Chat Transcripts",
    "Hi {name},\n\nQA has selected random chat transcripts from your interactions for review. Log in to preview and add comments.\n\n[Preview Transcripts]",
    "medium", "Customer Solutions", "QA review, sense of being watched", 1),

    ("Loyalty tier downgrade warning",
    "Warning: Loyalty Tier Downgrade Complaints",
    "Dear {name},\n\nWe received multiple complaints from customers about loyalty tier downgrades handled by your queue. Review the cases urgently.\n\n[Review Downgrade Cases]",
    "hard", "Customer Solutions", "Blaming style, escalated issues, quick click lure", 1),

    ("Overbooking apology voucher list",
    "Voucher List for Overbooking Incident",
    "Hi {name},\n\nDownload the voucher list and instructions used for yesterday's overbooking apology process.\n\n[Download Voucher List]",
    "easy", "Customer Solutions", "Voucher and compensation content", 1),

    ("Multi-lingual call routing",
    "Update Your Language Skills for Call Routing",
    "Hello {name},\n\nWe're updating language-based call routing. Confirm which languages you can handle.\n\n[Update Language Skills]",
    "medium", "Customer Solutions", "Profile update for language, personal info", 1),

    ("Customer survey abuse check",
    "Alert: Possible Abuse of Post-Flight Surveys",
    "Dear {name},\n\nSystem flagged unusual patterns in survey requests sent under your ID. Confirm that all requests were valid.\n\n[Confirm Survey Activity]",
    "hard", "Customer Solutions", "Accusation + request to confirm via link", 1),

    ("New apology email templates",
    "New Email Templates for Service Recovery",
    "Hi {name},\n\nDownload the new apology and service recovery templates for use after disruptions.\n\n[Download Templates]",
    "easy", "Customer Solutions", "Templates resource, benign-looking", 1),

    # === AT THE AIRPORT (extra 10, varied quality) ===
    ("Queue time dashboard",
    "New Real-Time Queue Time Dashboard",
    "Dear {name},\n\nWe've deployed a new dashboard to monitor check-in and security queue times.\n\n[View Queue Dashboard]",
    "medium", "At the Airport", "Monitoring dashboard, operational lure", 1),

    ("Missing boarding pass incident",
    "Incident: Missing Boarding Pass Reprints",
    "Hi {name},\n\nAn incident log shows multiple boarding pass reprints at your gate. Review the event summary.\n\n[Open Event Summary]",
    "hard", "At the Airport", "Security-ish, log review link", 1),

    ("Wrong gate signage",
    "Gate Signage Misalignment Report",
    "Dear {name},\n\nPassengers reported confusion at your gate due to signage changes. Check the attached signage plan.\n\n[Download Signage Plan]",
    "medium", "At the Airport", "Ops + signage doc download", 1),

    ("Standby list error",
    "Standby List Sorting Error – Manual Check Needed",
    "Hi {name},\n\nStandby list for flight yesterday may have been sorted incorrectly. Check the list and confirm no errors.\n\n[Check Standby List]",
    "hard", "At the Airport", "Data issue that seems urgent and plausible", 1),

    ("Tarmac access brief",
    "Brief: Temporary Tarmac Access Paths",
    "Hello {name},\n\nTarmac access paths have been re-routed. Please see brief for updated walking zones.\n\n[Open Tarmac Brief]",
    "medium", "At the Airport", "Misspellings, yet plausible ops content", 1),

    ("Late-night staffing adjustment",
    "Late-Night Staffing Changes for Your Terminal",
    "Dear {name},\n\nDownload the updated staffing plan for late-night operations at your terminal.\n\n[Download Staffing Changes]",
    "easy", "At the Airport", "Staffing doc, operational context", 1),

    ("Passenger flow simulation",
    "Passenger Flow Simulation Trial at Your Gate",
    "Hi {name},\n\nYou've been selected to pilot a passenger flow simulation. View the instructions and heatmaps.\n\n[View Simulation Guide]",
    "medium", "At the Airport", "Simulation/heatmap talk, interesting lure", 1),

    ("Security queue cooperation memo",
    "Memo: Coordination with Security Screening Lanes",
    "Dear {name},\n\nA new memo outlines coordination between gate teams and screening lanes.\n\n[Download Coordination Memo]",
    "easy", "At the Airport", "PDF/memo style, low friction", 1),

    ("Boarding experiment report",
    "Report: New Boarding Group Experiment Results",
    "Hi {name},\n\nRead the initial results of the boarding process experiment run at your station.\n\n[View Experiment Results]",
    "medium", "At the Airport", "Experiment report lure", 1),

    ("Jetbridge safety check",
    "Jetbridge Safety Checklist Confirmation",
    "Dear {name},\n\nJetbridge safety checks at your gates require confirmation of completion.\n\n[Confirm Safety Checklist]",
    "hard", "At the Airport", "Safety + confirmation, high-pressure phish", 1),

    # === FLIGHT ATTENDANT (extra 10, varied quality) ===
    ("New service script for premium",
    "Refined Script for Premium Cabin Announcements",
    "Hi {name},\n\nWe've updated the announcement script for premium cabin passengers. Download the latest wording.\n\n[Download Script]",
    "easy", "Flight Attendant", "Simple doc download, plausible", 1),

    ("Babysitting policy question",
    "Clarification: Child & Infant Handling Policy",
    "Dear {name},\n\nA passenger complaint suggests confusion about child seat and infant handling rules. Review the updated policy.\n\n[Review Policy Now]",
    "medium", "Flight Attendant", "Complaint mention + policy", 1),

    ("Strange passenger video posted",
    "Passenger Video Mentioning Your Flight",
    "Hi {name},\n\nA passenger posted a video referencing your recent flight and crew. Review the clip and internal notes.\n\n[View Passenger Video]",
    "hard", "Flight Attendant", "Social media/fear lure, strong curiosity", 1),

    ("Galley equipment recall",
    "Galley Cart and Equipment Recall Notice",
    "Dear {name},\n\nCertain galley carts and trolleys have been recalled. See if your flight numbers are affected.\n\n[Check Affected Flights]",
    "medium", "Flight Attendant", "Equipment recall theme", 1),

    ("Special passenger recognition",
    "Recognizing You for Special Passenger Handling",
    "Hello {name},\n\nYou've been recognized for handling a special-service passenger on a recent flight. View the note from leadership.\n\n[View Recognition Note]",
    "easy", "Flight Attendant", "Flattery lure + click", 1),

    ("Service flow critique",
    "Feedback: Service Flow on Your Last Flight",
    "Dear {name},\n\nOperational review flagged your flight's service flow timing as 'below target'. See the breakdown.\n\n[View Service Timing Report]",
    "hard", "Flight Attendant", "Negative performance, pushes immediate reaction", 1),

    ("Crew meal menu update",
    "New Crew Meal Menu Options",
    "Hi {name},\n\nCrew meal menus have changed for certain routes. Preview the new options.\n\n[Preview Crew Menu]",
    "easy", "Flight Attendant", "Crew perks/food theme, non-threatening", 1),

    ("Cabin safety quiz",
    "Short Cabin Safety Quiz for All Crew",
    "Dear {name},\n\nTake this 5-question quiz to refresh cabin safety basics.\n\n[Start Safety Quiz]",
    "medium", "Flight Attendant", "Training quiz, link to fake quiz page", 1),

    ("Rude passenger complaint",
    "Passenger Complaint: Tone of Voice",
    "Hi {name},\n\nA complaint was filed about tone of voice used with a passenger. Review the transcript and respond.\n\n[Review Complaint]",
    "hard", "Flight Attendant", "Very emotional/fear-based, strong lure", 1),

    ("New amenity kit instructions",
    "Amenity Kit Distribution Change in Business Class",
    "Dear {name},\n\nBusiness-class amenity kit distribution timing has changed. Review the new flow.\n\n[View Amenity Instructions]",
    "medium", "Flight Attendant", "Product/flow update, simple link", 1),

    # === PILOT OPERATIONS (extra 10, varied quality) ===
    ("Wrong fuel figure question",
    "Fuel Figure Clarification for Recent Flight",
    "Dear {name},\n\nDispatch has a question about fuel figures filed on one of your recent sectors. Review and confirm.\n\n[Check Fuel Figure]",
    "hard", "Pilot Operations", "Dispatch + fuel suspicion, high tension", 1),

    ("ATC phraseology refresher",
    "ATC Phraseology Refresher for Busy Airspace",
    "Hi {name},\n\nA short ATC phraseology refresher is recommended before the upcoming busy traffic period.\n\n[Download Phraseology Guide]",
    "medium", "Pilot Operations", "Pilot-specific training doc", 1),

    ("Landing rate analysis",
    "Landing Rate Metrics for Your Last Month of Flights",
    "Dear {name},\n\nA summary of landing rate metrics (fpm) for your recent flights is ready.\n\n[View Landing Metrics]",
    "medium", "Pilot Operations", "Performance analytics, curiosity lure", 1),

    ("Runway excursion rumor",
    "Internal Note: Runway Excursion Rumor Clarification",
    "Hello {name},\n\nAn internal rumor about a runway excursion on one of your routes is circulating. Read the official clarification.\n\n[Read Clarification]",
    "hard", "Pilot Operations", "Drama/rumor, high emotional pull", 1),

    ("NOTAM quick filter tool",
    "New NOTAM Filter Tool for Preflight Briefing",
    "Hi {name},\n\nTry this internal tool to quickly filter NOTAMs by relevance.\n\n[Try NOTAM Filter]",
    "medium", "Pilot Operations", "Tool for real pain point, attractive", 1),

    ("Unstable approach case",
    "Report: Unstable Approach Flag on Your Flight",
    "Dear {name},\n\nAn unstable approach warning was recorded for one of your recent landings. Review the data.\n\n[Review Flight Data]",
    "hard", "Pilot Operations", "Safety incident theme, heavy pressure", 1),

    ("New SID/STAR visuals",
    "Updated SID/STAR Visual Guides for Hub",
    "Hi {name},\n\nDownload the revised visual guides for departures and arrivals at your hub.\n\n[Download Visual Guides]",
    "easy", "Pilot Operations", "Technical but harmless-looking", 1),

    ("Sim session debrief note",
    "Notes from Your Last Simulator Session",
    "Dear {name},\n\nAdditional notes from your last sim session were added by the instructor.\n\n[View Debrief Notes]",
    "medium", "Pilot Operations", "Sim debrief curiosity", 1),

    ("New EFB checklist app",
    "Try New EFB Checklist Add-On",
    "Hi {name},\n\nWe're testing a new EFB checklist plugin. Install it using the link below.\n\n[Install EFB Add-On]",
    "hard", "Pilot Operations", "Software install onto EFB, dangerous vector", 1),

    ("Weather diversion lessons",
    "Lessons Learned from Recent Weather Diversions",
    "Dear {name},\n\nDispatch compiled lessons learned from several recent weather diversions on your routes.\n\n[Read Lessons Learned]",
    "medium", "Pilot Operations", "Ops/safety doc, strong appeal", 1),

    # === FINANCE (extra 10, varied quality) ===
    ("Airport charge increase note",
    "Airport Charges Increase – Impact to Budget",
    "Dear {name},\n\nRecent changes in airport fees will impact your station's budget. Review the breakdown.\n\n[View Charges Breakdown]",
    "medium", "Finance", "Airport fee theme, doc link", 1),

    ("Fuel card transaction anomaly",
    "Anomaly in Fuel Card Transactions",
    "Hi {name},\n\nUnusual fuel card transactions were detected under your cost center. Confirm whether these are valid.\n\n[Review Transactions]",
    "hard", "Finance", "Fraud/irregularity fear, transaction log lure", 1),

    ("Onboard sales tax error",
    "Onboard Sales Tax Mapping Error",
    "Dear {name},\n\nA mapping error in onboard sales taxes has been discovered. Download the correction sheet.\n\n[Download Correction Sheet]",
    "medium", "Finance", "Technical finance detail, spreadsheet style", 1),

    ("Supplier invoice spam",
    "Invoice Dispute: Catering Supplier Charges",
    "Hello {name},\n\nA catering supplier dispute is pending for invoices linked to your base. Check the invoice copies.\n\n[Open Invoice Copies]",
    "medium", "Finance", "Supplier/invoice theme, doc attachments", 1),

    ("Budget overspend warning",
    "Overspend Warning on Route Promotion Budget",
    "Hi {name},\n\nRoute promotion costs appear above budget for your region. Review the summary.\n\n[View Overspend Summary]",
    "medium", "Finance", "Budget worry, summary link", 1),

    ("Wrong amount in ledger",
    "Wrong Amounts in Ledger Detected",
    "Dear {name},\n\nWe found wrong amounts in ledger relating to airport taxes and fees. Please fix it quickly.\n\n[Fix Ledger Entry]",
    "hard", "Finance", "Bad spelling but context sounds real, strong urgency", 1),

    ("Corporate credit limit reset",
    "Reset of Corporate Credit Limits",
    "Hi {name},\n\nCorporate credit limits for certain vendors have been reset. View which ones are impacted.\n\n[View Vendor Credit Limits]",
    "medium", "Finance", "Vendor/credit theme", 1),

    ("FX rate impact note",
    "Foreign Exchange Rate Impact on Fuel & Lease Costs",
    "Dear {name},\n\nFX swings this quarter have impacted our fuel and aircraft lease costs. Download the short analysis.\n\n[Download FX Impact Note]",
    "medium", "Finance", "FX/hedging style, attractive to finance people", 1),

    ("Cabin upgrade promotion costing",
    "Costing for Cabin Upgrade Promotions",
    "Hello {name},\n\nFinance has prepared a costing sheet for cabin upgrade offers. Please review.\n\n[Review Costing Sheet]",
    "easy", "Finance", "Campaign costing, excel-like doc", 1),

    ("Fraud watch list update",
    "Updated Fraud Watch List for Airline Payments",
    "Hi {name},\n\nOur fraud team updated the watch list for suspicious merchants and accounts.\n\n[View Fraud Watch List]",
    "hard", "Finance", "Security/fraud doc, big lure", 1),

    # === IT SUPPORT (extra 10, varied quality) ===
    ("Crew portal timeout fix",
    "Temporary Fix for Crew Portal Timeouts",
    "Dear {name},\n\nUsers report timeouts when accessing the crew portal. Apply this configuration to mitigate.\n\n[Download Fix Config]",
    "hard", "IT Support", "Config download, techy but malicious", 1),

    ("Password policy FAQ",
    "FAQ: New Password & MFA Policy",
    "Hi {name},\n\nRead the FAQ on our new password and MFA rules.\n\n[Read Password FAQ]",
    "easy", "IT Support", "Security help page, simple click", 1),

    ("Airport wifi guest portal bug",
    "Bug: Guest WiFi Portal Certificate Warning",
    "Hello {name},\n\nReports show certificate warning on airport guest WiFi portal. Open diagnostic page for more details.\n\n[Open WiFi Diagnostic]",
    "medium", "IT Support", "Cert warning mention, diagnostic link", 1),

    ("Strange login attempts",
    "Many Strange Logins From Foreign Country",
    "Dear {name},\n\nWe see many strange logins to your account from foreign country. You must verify NOW if it's you.\n\n[Verify Now]\n\nIf you ignore this, account may be blocked.",
    "hard", "IT Support", "Classic bad-grammar scare phish", 1),

    ("Helpdesk satisfaction stats",
    "Your Helpdesk Satisfaction Scores for Last Month",
    "Hi {name},\n\nA summary of your helpdesk satisfaction ratings is ready.\n\n[View Satisfaction Scores]",
    "medium", "IT Support", "Personal performance stats lure", 1),

    ("New ticket routing rules",
    "Ticket Routing Rules Updated for Airline Systems",
    "Dear {name},\n\nWe updated rules for how tickets related to airline apps and tools are routed.\n\n[View Routing Rules]",
    "easy", "IT Support", "Process document, operational", 1),

    ("Endpoint agent offline",
    "Endpoint Security Agent Offline on Multiple Machines",
    "Hi {name},\n\nMultiple machines at your station appear offline in the security console. Run this script to re-register them.\n\n[Download Re-Register Script]",
    "hard", "IT Support", "Script download disguised as fix", 1),

    ("Zero-day advisory",
    "Advisory: Zero-Day Vulnerability Affecting Airline Systems",
    "Dear {name},\n\nRead this urgent advisory about a new zero-day affecting our stack.\n\n[Read Zero-Day Advisory]",
    "hard", "IT Support", "High-anxiety security news lure", 1),

    ("Printer driver pack",
    "Driver Pack for Boarding Pass / Tag Printers",
    "Hi {name},\n\nInstall the updated driver pack for boarding pass and baggage tag printers.\n\n[Download Driver Pack]",
    "medium", "IT Support", "Printer driver download, very plausible", 1),

    ("Internal phishing test follow-up",
    "Follow-Up to Internal Phishing Test",
    "Dear {name},\n\nYou recently participated in an internal phishing test. View your score and training recommendations.\n\n[View Phishing Test Results]",
    "medium", "IT Support", "Meta-phishing, using security training as hook", 1),

    ]

    insert_sql = '''
    INSERT INTO email_templates
    (template_name, subject, body, difficulty_level, target_department, red_flags, is_phishing)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    '''
    cursor.executemany(insert_sql, templates)
    connection.commit()
    print(f"Inserted {len(templates)} default email templates into email_templates table.")


def send_scheduled_emails():
    """Step 6: Background job runs every hour to send scheduled emails"""
    
    now = datetime.now()
    
    # Find emails ready to send
    cursor.execute('''
        SELECT se.id, se.user_id, et.subject, et.body, u.email, u.name
        FROM scheduled_emails se
        JOIN email_templates et ON se.template_id = et.id
        JOIN users u ON se.user_id = u.id
        WHERE se.scheduled_time <= ? AND se.sent = 0
    ''', (now,))
    
    emails_to_send = cursor.fetchall()
    
    for email_id, user_id, subject, body, recipient_email, recipient_name in emails_to_send:
        
        personalized_body = body.replace("{name}", recipient_name or "Team Member")

        # Send email (use actual email service)
        send_email(recipient_email, subject, personalized_body)
        
        # Create simulation record
        cursor.execute('''
            INSERT INTO simulations (user_id, email_content, simulation_type) 
            VALUES (?, ?, 'phishing_test')
        ''', (user_id, personalized_body))
        
        simulation_id = cursor.lastrowid
        
        # Mark as sent
        cursor.execute('''
            UPDATE scheduled_emails
            SET sent = 1, sent_at = ?
            WHERE id = ?
        ''', (now, email_id))
    
    connection.commit()
    print(f"Sent {len(emails_to_send)} phishing test emails")

# Run the template insert on startup (only if table empty)
add_default_email_templates()

# close connection is intentionally omitted so other functions can use it
# but you can close later if needed
