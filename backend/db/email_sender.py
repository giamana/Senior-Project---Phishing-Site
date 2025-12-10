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

    extra_templates = [
        # Aircraft Maintenance & Support (10)
        ("Maintenance Schedule Update", "Updated AMM Procedure Discussion – Action Required", "Dear {name},\n\nYou were marked absent from Monday’s AMM revision meeting. Several procedures regarding part 2B inspections were updated, and your acknowledgment is required before tomorrow’s shift.\nPlease review the updated documentation and confirm your understanding using the link below.\n\n[Review AMM Update]\n", "complex", "Aircraft Maintenance and Support", "Missed meeting lure, urgency, fake AMM link", 1),
        ("Parts Recall Verification", "URGENT: Verify Lot Numbers for Recent Parts Delivery", "Dear {name},\n\nQuality Control reported potential defects in the last shipment of hydraulic pumps delivered Friday. Your assigned lot numbers are currently under review and may require immediate grounding.\nConfirm whether your workbench inventory contains any affected units.\n\n[Verify Part Numbers]\n", "complex", "Aircraft Maintenance and Support", "Fake QC recall, fear tactic", 1),
        ("Safety Inspection Follow-Up", "Pending Inspection Report – Your Action Needed", "Dear {name},\n\nDuring yesterday’s walk-through, your inspection notes for Aircraft 7NQ were marked incomplete. Compliance needs your corrected report submitted before the afternoon audit session.\nUse the portal below to upload the revised details.\n\n[Upload Inspection Report]\n", "complex", "Aircraft Maintenance and Support", "Fake compliance deadline, upload portal", 1),
        ("Tool Calibration Error", "Calibration Failure Detected – Technician Review Required", "Dear {name},\n\nAutomated logs show irregular calibration values for torque wrench set #A391 assigned to your station. These discrepancies could lead to grounding if left unresolved.\nPlease review the anomaly report immediately.\n\n[View Calibration Report]\n", "complex", "Aircraft Maintenance and Support", "Fake calibration error, urgency", 1),
        ("Unexpected Badge Scan Activity", "Security Alert: Unauthorized Hangar Access Attempt", "Dear {name},\n\nSecurity monitoring flagged an unsuccessful badge scan attributed to your ID at Hangar 4 late last night. Access will remain restricted until you verify the activity.\nSubmit your verification to avoid suspension from secure areas.\n\n[Verify Badge Activity]\n", "complex", "Aircraft Maintenance and Support", "Fake security alert, fear pressure", 1),
        ("Maintenance Log Error Notification", "Incorrect MEL Entry – Correction Needed", "Dear {name},\n\nDispatch identified an inconsistency in your recent MEL entry for Aircraft 92L. The reported discrepancy impacts the clearance for tomorrow’s early route.\nPlease review and resubmit the corrected entry.\n\n[Correct MEL Entry]\n", "complex", "Aircraft Maintenance and Support", "Technical jargon lure, false MEL issue", 1),
        ("FAA Compliance Reminder", "FAA Bulletin Review Required Before Next Shift", "Dear {name},\n\nA new FAA safety bulletin affecting ground-level inspection protocols has been released. All maintenance personnel must acknowledge receipt before clocking in tomorrow.\nUse the link below to confirm your review.\n\n[Review FAA Bulletin]\n", "complex", "Aircraft Maintenance and Support", "Fake FAA bulletin, urgency", 1),
        ("Fuel System Maintenance Notice", "Fuel Valve Check Required – Immediate Attention", "Dear {name},\n\nFuel system monitoring detected an anomaly associated with last week’s maintenance logs. A re-check of the valve assembly is required and must be documented promptly.\nSubmit confirmation after reviewing the updated instructions.\n\n[View Instructions]\n", "complex", "Aircraft Maintenance and Support", "Fake anomaly report, urgency", 1),
        ("Shift Compliance Warning", "Non-Compliance Flagged in Shift Turnover Report", "Dear {name},\n\nYour name was flagged in last night’s turnover report due to missing certification on a task you signed off on. This must be validated to avoid forced retraining.\nConfirm your credentials using the portal below.\n\n[Confirm Credentials]\n", "complex", "Aircraft Maintenance and Support", "Threat of discipline, fake credential portal", 1),
        ("Emergency Work Order Request", "New High-Priority WO: Immediate Review Needed", "Dear {name},\n\nA high-priority work order was assigned to you following an irregular vibration report during taxi operations. Dispatch requires your diagnostic assessment within the hour.\nAccess the WO details through the link below.\n\n[Open Work Order]\n", "complex", "Aircraft Maintenance and Support", "High-pressure work order, fake dispatch link", 1),
        # At the Airport (10)
        ("Gate Reassignment Follow-Up", "Action Needed: Gate Change Review for Morning Departures", "Dear {name},\n\nYou were marked absent from Monday’s gate-operations briefing where the updated gate rotation policies were discussed. Several flights assigned to your shift have been reallocated and require your acknowledgment before tomorrow’s roster is finalized.\n\nPlease review the updated Gate Assignment Sheet here:\n[Review Gate Updates]", "complex", "At the Airport", "Missed meeting, urgency, fake operations portal", 1),
        ("Baggage Irregularity Audit", "Urgent Review: Baggage Incident Logged on Your Shift", "Dear {name},\n\nA passenger filed a delayed baggage complaint tied to a loading discrepancy during your assigned timeframe. Operations requires your confirmation of the handling log to finalize the investigation.\n\nSubmit your handling statement below:\n[Submit Statement]", "complex", "At the Airport", "Fear-based tactic, fake audit link", 1),
        ("Security Badge Failure Notice", "Immediate Verification Required: Badge Scan Failure", "Dear {name},\n\nSecurity recorded repeated failed scans from your badge at Entry Point C. Due to an increase in unauthorized access attempts, we must temporarily suspend your badge until you validate the activity.\n\nRestore your badge access:\n[Validate Badge Activity]", "complex", "At the Airport", "Security impersonation, urgency, suspension threat", 1),
        ("Lost Item Claim Verification", "Passenger Lost Item Report Requires Your Review", "Dear {name},\n\nA passenger submitted a lost-item claim referencing your gate zone. Please verify whether the item was logged, as this impacts the handling resolution deadline.\n\nVerify item record below:\n[Verify Claim]", "complex", "At the Airport", "Fake claims portal, invokes responsibility", 1),
        ("Ramp Safety Reminder", "Mandatory Update: Revised Ramp Safety Guidelines", "Dear {name},\n\nSafety & Compliance updated several ramp procedures after an issue identified last Monday. Since you were marked absent from the safety review session, your acknowledgment is required before returning to active duty areas.\n\nAccess revised safety procedures:\n[Review Safety Update]", "complex", "At the Airport", "Fake safety link, urgency but calm tone", 1),
        ("Flight Delay Compensation Logs", "Compensation Forms Missing for Delay Event #2934", "Dear {name},\n\nThe compensation report for last Saturday’s delay from your gate has missing staff input. Passenger Relations cannot proceed without your confirmation of delay cause and handling notes.\n\nSubmit final delay notes:\n[Submit Compensation Data]", "complex", "At the Airport", "Fake compensation workflow, pressure to comply", 1),
        ("Employee Parking Violation Alert", "Parking Access Suspended Pending Confirmation", "Dear {name},\n\nA vehicle registered under your badge ID triggered an alert for unauthorized parking zone access. Please review the incident before airport security escalates the matter.\n\nView parking incident:\n[Open Violation Report]", "complex", "At the Airport", "Fake traffic/parking violation, scare tactic", 1),
        ("Gate Equipment Malfunction Report", "Follow-Up Required: Jetbridge Malfunction Log", "Dear {name},\n\nMaintenance identified inconsistent reports regarding a jetbridge malfunction during your gate’s operational window. Before filing the FAA equipment log, they require your operator confirmation.\n\nConfirm operator details:\n[Confirm Jetbridge Log]", "complex", "At the Airport", "Uses FAA terminology, fake technical review", 1),
        ("Catering Delivery Discrepancy", "Action Needed: Catering Cart Miscount", "Dear {name},\n\nCatering Services reported a miscount during loading at your gate, and your acknowledgment is required to prevent a service quality escalation. Please review the corrected service cart manifest.\n\nReview manifest:\n[Check Catering Count]", "complex", "At the Airport", "Operational urgency, fake manifest link", 1),
        ("Terminal Access Training Expired", "Training Expiration: Renew Terminal Movement Certification", "Dear {name},\n\nYour Terminal Movement certification has expired, and system access will be restricted unless renewed immediately. This update was discussed in the Monday airport ops meeting which you were marked absent for.\n\nRenew your terminal certification:\n[Renew Certification]", "complex", "At the Airport", "Fake certification portal, high pressure", 1),
        # Corporate (10)
        ("Missed Executive Sync", "Action Needed: Summary From Monday Corporate Alignment Meeting", "Dear {name},\n\nYou were not present during Monday’s corporate alignment call where we finalized new compliance and communication protocols for Q4 operations. All department heads must review and acknowledge the updated directives to avoid delays in policy rollout.\n\nPlease open the meeting summary and confirm your understanding.\n\n[Review Summary]", "complex", "Corporate", "Missed meeting urgency, vague compliance details, link to 'review summary'", 1),
        ("Travel Spend Over Review", "Corporate Travel Expense Threshold Exceeded – Verification Required", "Dear {name},\n\nOur automated audit system flagged your most recent flight-related travel receipts for exceeding the approved spending threshold. This may prevent reimbursement if not resolved before the monthly finance closeout.\n\nVerify the receipts and submit clarification if needed.\n\n[Review Receipts]", "complex", "Corporate", "Finance impersonation, fear of losing reimbursement, vague audit system", 1),
        ("New Corporate Device Policy", "Mandatory Acceptance: Updated Corporate Device & Security Policy", "Dear {name},\n\nIT Security has released a revised device usage policy affecting all corporate-issued laptops and tablets. The document outlines new monitoring procedures discussed in last Friday’s security forum.\n\nYou must acknowledge these updates before retaining system access.\n\n[Acknowledge Policy]", "complex", "Corporate", "Policy update, implied loss of access, unclear sender identity", 1),
        ("Unusual Login Pattern", "Security Alert: Attempted Login From Overseas Location", "Dear {name},\n\nCorporate Security detected an attempted login associated with your employee credentials from a non-whitelisted region. System access has been temporarily restricted until verification is completed.\n\nValidate this activity to restore functionality.\n\n[Verify Login Attempt]", "complex", "Corporate", "Fear tactic, generic greeting, pressure to click", 1),
        ("Benefits Review Required", "Updated Corporate Benefits for Aviation Staff – Action Required", "Dear {name},\n\nAs part of our yearly aviation workforce realignment, several corporate benefits have been modified. HR requires all employees to confirm their selections to ensure proper enrollment before the new cycle begins.\n\nReview your updated benefits package below.\n\n[Verify Benefits]", "complex", "Corporate", "Benefits urgency, vague realignment term, link", 1),
        ("Corporate Compliance Incident", "URGENT: Review Required for Potential Compliance Irregularity", "Dear {name},\n\nYour corporate credentials were logged in a document review cycle that was missing proper authorization tagging. This may trigger an internal compliance review unless confirmed as intentional.\n\nPlease confirm the authorization status immediately.\n\n[Confirm Authorization]", "complex", "Corporate", "Fear tactic, vague incident details, urgency", 1),
        ("Quarterly Strategy Template", "Submit Your Q3 Strategy Alignment Template", "Dear {name},\n\nCorporate Strategy is preparing the final alignment report for Q3. Several departments have already submitted their templates, but our system indicates yours is still pending. Failure to submit may delay inter-department planning.\n\nUpload your completed form below.\n\n[Upload Template]", "complex", "Corporate", "Fake urgency, upload link, no real reference info", 1),
        ("Executive Town Hall Follow-Up", "Action Items From Friday’s Executive Town Hall", "Dear {name},\n\nDuring Friday’s town hall, we launched the new corporate culture initiatives and outlined employee expectations for the upcoming audit cycle. Several employees missed the attendance log submission.\n\nPlease review the action items and confirm attendance retroactively.\n\n[Confirm Attendance]", "complex", "Corporate", "Fake attendance requirement, link, vague initiatives", 1),
        ("Storage Quota Exceeded", "Corporate Drive Update: Storage Limit Reached", "Dear {name},\n\nYour corporate drive has surpassed its allotted storage capacity, putting several shared documents at risk of corruption. IT requires that users validate their archives and approve automated cleanup.\n\nStart your verification below.\n\n[Start Verification]", "complex", "Corporate", "Fear of data loss, urgency, suspicious cleanup request", 1),
        ("Corporate Survey With Incentive", "Complete Corporate Productivity Survey – Incentives Available", "Dear {name},\n\nCorporate Leadership is gathering feedback on operational efficiency across airline departments. Completing this 3-minute survey helps refine next quarter’s initiatives and qualifies you for a small participation reward.\n\nTake the survey below.\n\n[Begin Survey]", "complex", "Corporate", "Incentive lure, vague leadership reference, external-looking link", 1),
        # Customer Solutions (10)
        ("Escalated Case Review Required", "Tier-3 Escalation: Immediate Review Required for Passenger Case #44289", "Dear {name},\nOur records indicate you missed yesterday’s escalation sync regarding Case #44289. The passenger dispute involves time-sensitive travel credit reissues. Please review the summary notes and acknowledge your corrective action.\nFailure to respond may delay compensation processing.\n[Review Case Summary]", "complex", "Customer Solutions", "Urgency, fake case number, impersonation of QA manager, link to review", 1),
        ("Customer Refund Audit Discrepancy", "Refund Verification Needed — Mismatch Found in Audit", "Dear {name},\nFinance flagged a mismatch between your processed refund and the system-calculated value for PNR 84JQ9D. We need to verify your adjustment to proceed with reimbursement.\nPlease confirm the correct amount using the link below.\n[Verify Refund Adjustment]", "complex", "Customer Solutions", "Fake finance audit, vague authority, pressure to correct error", 1),
        ("Lounge Access Complaint Follow-Up", "Urgent: Passenger Lounge Complaint Assigned to You", "Dear {name},\nA premium passenger filed a complaint regarding denied lounge entry during yesterday’s operational disruption. Since you were assigned to this route, Quality needs your feedback ASAP.\nReview details and submit your response before today’s closeout.\n[Respond to Complaint]", "complex", "Customer Solutions", "Emotional manipulation, fear of blame, fake QA request", 1),
        ("Customer Voucher Activation Issue", "Voucher Activation Failure — Customer Waiting for Support", "Dear {name},\nA customer reported that the travel voucher issued after their delay is not activating in the online portal. Please verify the original voucher settings and confirm if manual override is needed.\nUse the link below to access the voucher file.\n[Open Voucher Details]", "complex", "Customer Solutions", "Downloadable voucher file, fake support system", 1),
        ("Case Backlog Reduction Assignment", "Backlog Reduction Initiative — New Cases Assigned to You", "Dear {name},\nCustomer Care leadership assigned additional cases to your queue as part of this week’s backlog reduction plan. Please review the added items and mark priority levels before noon.\nCustomers affected have time-sensitive travel itineraries.\n[View Assigned Cases]", "complex", "Customer Solutions", "Unverified leadership directive, productivity pressure", 1),
        ("Customer Name Verification Error", "ID Mismatch — Passenger Verification Required", "Dear {name},\nA passenger’s ID verification failed due to inconsistencies in the name formatting during your case intake. Before the ticket can be re-issued, please review the system logs and confirm accuracy.\nReview the flagged data at the link below.\n[Verify Passenger Info]", "complex", "Customer Solutions", "Sensitive passenger data request, impersonation of fraud team", 1),
        ("Disruption Response Protocol Update", "New Customer Disruption Protocol — Acknowledgment Needed", "Dear {name},\nDuring Monday’s meeting (which you were marked absent for), we reviewed the new customer disruption response workflow for large-scale delays. All representatives must acknowledge the new process by end of day.\nAccess your copy below.\n[Review Updated Protocol]", "complex", "Customer Solutions", "Missed-meeting pressure, fake PDF link, corporate authority tone", 1),
        ("Feedback Score Reduction Warning", "Low Satisfaction Score Detected — Review Your Metrics", "Dear {name},\nYour customer satisfaction metrics for the past week show an unexpected decline. Before this is escalated to your supervisor, please review recent feedback entries and submit your improvement plan.\nBegin by reviewing your flagged interactions.\n[View Feedback Metrics]", "complex", "Customer Solutions", "Fear tactic, fake performance dashboard", 1),
        ("Compensation Miscalculation Alert", "Error Detected in Customer Compensation Amount", "Dear {name},\nCompensation issued for a recent flight irregularity appears to exceed approved limits. Systems require you to verify whether this was intentional or system-generated before Finance reverses the claim.\nCheck the compensation logs here.\n[Open Compensation Report]", "complex", "Customer Solutions", "Fake finance audit, unusual request to verify limit exceed", 1),
        ("Customer Privacy Escalation", "Privacy Concern Raised — Immediate Review Required", "Dear {name},\nA customer has submitted a complaint alleging improper handling of their contact information during your case interaction. Compliance needs you to review the documented steps and confirm adherence to policy.\nSubmit your response using the link below.\n[Review Compliance Notes]", "complex", "Customer Solutions", "Privacy panic, compliance impersonation, mandatory response link", 1),
        # Digital Technology (10)
        ("System Configuration Drift Alert", "Critical: Configuration Drift Detected on Your Workstation", "Dear {name},\n\nOur automated monitoring system identified unexpected changes in your workstation’s configuration after Monday’s update window. We discussed in the Tuesday tech sync how this could impact secure access to internal airline systems.\n\nPlease review the drift report and reapply compliant settings.\n\n[Open Drift Report]", "complex", "Digital Technology", "IT jargon, configuration warning, urgency, suspicious link", 1),
        ("API Token Expiration Notice", "Your Access Token for Flight Operations API Expires Tonight", "Dear {name},\n\nYour developer API token used for accessing the FlightOps Scheduling Microservice is expiring due to policy revisions announced earlier this week. Failure to renew may break your integration pipelines.\n\nRenew your token using the secure gateway.\n\n[Renew Access Token]", "complex", "Digital Technology", "Token renewal pressure, impersonating internal tools", 1),
        ("Internal Git Repository Merge Conflict Review", "Action Required: Merge Conflict Found in Your Repository", "Dear {name},\n\nA merge conflict was detected in the Aircraft Routing Automation repository while syncing code changes from Monday’s sprint. This must be resolved before tomorrow’s deployment window.\n\nPlease review the conflict details and approve the automated fix.\n\n[Resolve Conflict]", "complex", "Digital Technology", "Fake Git alert, vague automated fix option", 1),
        ("High-Risk Vulnerability Patch", "CVE-2025-4982 Patch Required for Airline Systems", "Dear {name},\n\nSecurity Operations flagged your workstation as unpatched for a high-severity vulnerability discussed in this morning’s cross-department cyber briefing. Immediate remediation is required.\n\nDownload the urgent patch below.\n\n[Download Patch Installer]", "complex", "Digital Technology", "Fake CVE, fake patch, malware lure, extreme urgency", 1),
        ("MFA Token Sync Failure", "Multi-Factor Authentication Token Out-of-Sync", "Dear {name},\n\nYour MFA token failed synchronization during Sunday’s authentication server refresh. You may lose dashboard access unless you resync manually.\n\nResync your token below.\n\n[Sync MFA Token]", "complex", "Digital Technology", "IT impersonation, fake MFA sync link", 1),
        ("Server Load Alert – Resource Overutilization", "Warning: Overload Detected on Your Assigned Compute Cluster", "Dear {name},\n\nOur monitoring agents detected high CPU usage on Cluster-G12, which your team was assigned during the Monday performance meeting. Please validate your workloads and acknowledge the alert.\n\n[View Load Report]", "complex", "Digital Technology", "Fake monitoring alert, fake data report", 1),
        ("Software License Autopay Failure", "URGENT: Airline IT License Renewal Failed", "Dear {name},\n\nThe automated renewal for your JetStream Analytics license failed due to an internal billing mismatch. This tool is required for tonight’s data refresh.\n\nUpdate your license credentials to avoid service interruption.\n\n[Update License]", "complex", "Digital Technology", "Fake billing issue, finance + IT confusion", 1),
        ("Unauthorized Access Attempt (DevOps Portal)", "Security Alert: Suspicious Login Attempt on DevOps Console", "Dear {name},\n\nOur system flagged an unusual login attempt from an unrecognized device to your DevOps deployment console. Access is temporarily restricted until you confirm the activity.\n\nConfirm whether this was you.\n\n[Review Login Attempt]", "complex", "Digital Technology", "Fear tactic, fake security alert, credential validation", 1),
        ("Outdated Build Agent Detected", "ALERT: Your Build Agent Version Is No Longer Supported", "Dear {name},\n\nDuring the Monday CI/CD pipeline review, we noted several outdated build agents—including yours—that must be updated to support the new Aircraft Routing features deploying next week.\n\nInstall the required update package:\n\n[Update Build Agent]", "complex", "Digital Technology", "Fake CI/CD update, software download lure", 1),
        ("Cloud Storage Permission Conflict", "Access Revoked: Conflicting Permissions on Shared Airline Bucket", "Dear {name},\n\nA permission mismatch was detected on the shared cloud bucket you used for uploading route optimization models. Until this is resolved, your access remains restricted.\n\nReview and confirm updated permission settings.\n\n[Review Permissions]", "complex", "Digital Technology", "Fake cloud platform link, vague permission error", 1),
        # Customer Service (10)
        ("Rebooking Error Notice", "URGENT: Customer Rebooking Failed — Action Required", "Dear {name},\n\nA rebooking attempt for passenger James R. on Flight 443 did not process correctly and is stuck in the pending queue. Please review the request and approve the correct routing before the system auto-cancels it.\n\n[Resolve Rebooking]\n", "complex", "Customer Service", "Urgency, fake system queue, false passenger info", 1),
        ("Refund Authorization Request", "Refund Request #99213 Requires Your Confirmation", "Dear {name},\n\nA refund submission flagged for manual approval has been assigned to your desk. Customer is waiting for confirmation due to a missed connection. Review the supporting documents and submit approval.\n\n[Open Refund File]\n", "complex", "Customer Service", "Financial lure, impersonation of refund tool", 1),
        ("Complaint Escalation Follow-Up", "Customer Filed a Tier-3 Complaint — Immediate Review", "Dear {name},\n\nA Tier-3 customer complaint cites service delay and unresolved ticket status. Management requires your written summary and resolution plan by end of day. Please log in and acknowledge.\n\n[Review Complaint]\n", "complex", "Customer Service", "High-pressure escalation, fake management oversight", 1),
        ("Loyalty Program Issue", "Frequent Flyer Account Unable to Sync — Assistance Needed", "Dear {name},\n\nA loyalty account belonging to a Platinum member failed to sync with their reservation. Customer expects updated mileage before travel tonight. Review and trigger a manual correction.\n\n[Fix Mileage Sync]\n", "complex", "Customer Service", "Fake loyalty account system link", 1),
        ("Service Quality Rating Audit", "Low Performance Rating Logged — Review Required", "Dear {name},\n\nA recent service rating associated with your shift scored below threshold and was flagged for audit. Management requests your statement and action review.\n\n[Submit Statement]\n", "complex", "Customer Service", "Fear tactic, fake HR oversight", 1),
        ("Lost Baggage Follow-Up", "Customer Baggage Case Needs Verification", "Dear {name},\n\nCase #55781 for missing luggage requires your verification of compensation eligibility. Customer claims the tracking status has not updated since Monday. Review details and escalate if needed.\n\n[Verify Case]\n", "complex", "Customer Service", "Fake case ID, fake link", 1),
        ("Ticketing Policy Update", "New Ticketing Rule Effective Immediately — Please Acknowledge", "Dear {name},\n\nWe discussed the new ticket change fee policy in Monday’s meeting, but records show you did not acknowledge the updated procedures. You must review and confirm understanding to maintain compliance.\n\n[Review Policy]\n", "complex", "Customer Service", "Meeting guilt-lure, policy impersonation", 1),
        ("Customer Information Verification", "Passenger Data Validation Pending", "Dear {name},\n\nA customer attempted to update their personal information, but validation failed due to mismatched loyalty data. Approve changes manually to avoid account lock.\n\n[Validate Account]\n", "complex", "Customer Service", "Sensitive data request, fake validation portal", 1),
        ("Service Disruption Coordination", "Weather Delay Response Required for Affected Customers", "Dear {name},\n\nDue to severe weather, multiple flights require coordinated customer outreach. You have been assigned five passengers needing rebooking or compensation review. Please sign into the response console.\n\n[Open Disruption Console]\n", "complex", "Customer Service", "Disaster urgency, fake operations portal", 1),
        ("Customer Payment Dispute", "Payment Reversal Inquiry Assigned to You", "Dear {name},\n\nA payment dispute involving travel extras (priority boarding + baggage) needs your review. Customer claims unauthorized charge on their invoice. Confirm transaction history.\n\n[View Transaction]\n", "complex", "Customer Service", "Flattery lure, finance tie-in, fake portal", 1),
        # Finance (10)
        ("Fuel Vendor Discrepancy Notice", "URGENT: Fuel Vendor Invoice Mismatch – Action Needed", "Dear {name},\n\nDuring yesterday’s reconciliation of airport fueling logs, an unexpected mismatch was detected in the amount billed versus the amount reported by ramp services. We discussed this briefly in Monday’s operations meeting, and your team was assigned verification of invoice #22984.\nPlease review the updated invoice summary and confirm whether the fuel variance is valid.\n\n[Verify Invoice Details]\n", "complex", "Finance", "Invoice mismatch, urgency to click, fake attachment", 1),
        ("Overtime Processing Delay", "Payroll Alert: Overtime Hours Not Processed", "Dear {name},\n\nOur automated payroll system flagged missing verification for your department’s overtime entries for the past pay period. This issue was raised during today’s HR-finance sync, and you were listed as the final approver.\nFailure to confirm these hours may cause delays for multiple employees.\nPlease review the pending hours below.\n\n[Review Overtime Sheet]\n", "complex", "Finance", "Payroll discrepancy lure", 1),
        ("Purchase Order Verification", "PO Review Required: Aircraft Parts Order 7782", "Dear {name},\n\nYour approval is required for a pending aircraft parts PO submitted by the maintenance team early this morning. The vendor stated pricing changes that were not reflected in our original agreement.\nKindly review this updated PO and confirm cost authorization before procurement closes.\n\n[Open Purchase Order]\n", "complex", "Finance", "Fake vendor request", 1),
        ("Tax Compliance Confirmation", "Immediate Attention: Quarterly Tax Filing Flagged", "Dear {name},\n\nOur internal audit tool reported incomplete confirmation for the airline’s quarterly tax filing related to airport service charges. This might be due to a missing digital signature on your part.\nComplete the compliance check below to prevent filing penalties.\n\n[Complete Compliance Check]\n", "complex", "Finance", "Fear tactic & fake compliance portal", 1),
        ("ACH Transfer Verification", "Verify ACH Transfer to New Vendor Account", "Dear {name},\n\nA new ACH transfer request was submitted this morning for vendor SkyTech Repairs. Normally this would require two-step validation, but our system shows only one approval recorded.\nPlease confirm the updated banking information before funds are released.\n\n[Validate Transfer]\n", "complex", "Finance", "Fake ACH verification", 1),
        ("Travel Reimbursement Timeout", "Reimbursement Request Timed Out – User Action Required", "Dear {name},\n\nThe system automatically timed out a reimbursement request linked to flight crew layover expenses in Atlanta. Normally these reset, but the claimant reports delays due to missing your final authorization.\nPlease re-open the claim using the link below.\n\n[Reopen Reimbursement]\n", "complex", "Finance", "Broken system urgency", 1),
        ("Route Budget Reallocation", "Budget Review Needed for New Route Changes", "Dear {name},\n\nFollowing yesterday's airline network planning meeting, financial allocations for several modified routes need reassessment. Your department is responsible for validating the adjusted flight operating costs.\nPlease review the updated route budget sheets.\n\n[Review Route Costs]\n", "complex", "Finance", "Route planning lure", 1),
        ("Corporate Card Suspension", "Corporate Card Will Be Suspended in 48 Hours", "Dear {name},\n\nOur expense auditing system detected unusual activity on your corporate purchasing card during an airport transaction sweep. As a precaution, the card has been set for suspension unless reviewed.\nConfirm the recent charges below.\n\n[Validate Transactions]\n", "complex", "Finance", "Corporate card fraud lure", 1),
        ("Dashboard Access Expiring", "Financial Insights Portal Access Renew Now", "Dear {name},\n\nWe noticed that your authentication token for the Finance Insights Dashboard is set to expire. This might restrict your ability to approve budgetary items for your department.\nRenew your access below to avoid interruptions.\n\n[Renew Access]\n", "complex", "Finance", "Token expiration lure", 1),
        ("Internal Audit Follow-Up", "Action Needed: Audit Findings Need Your Review", "Dear {name},\n\nDuring last Monday’s compliance audit discussion, your name appeared under outstanding documentation for payroll variance checks. These need acknowledgment before the quarter closes.\nOpen the summarized findings below and submit your comment.\n\n[Review Audit Findings]\n", "complex", "Finance", "Audit urgency", 1),
        # Flight Attendant (10)
        ("Crew Briefing Follow-Up", "Important: Summary of Missed Monday Crew Briefing", "Dear {name},\n\nYou were marked absent from Monday’s inflight crew briefing. We discussed several new safety procedures, updates to beverage service protocols, and a passenger handling standard that must be acknowledged. Please review the meeting notes and confirm you understand the new workflows.\n\n[Review Briefing Notes]", "complex", "Flight Attendant", "Urgent requirement, unfamiliar link, claims you missed a meeting", 1),
        ("Passenger Service Update Notice", "Updated Inflight Meal Service Policy for Next Week", "Dear {name},\n\nCatering has issued a revised meal distribution guideline for international flights. Please review the updated allergy declaration steps and new crew responsibilities before your next rotation. Failure to comply may result in service delays.\n\n[View Updated Guidelines]", "complex", "Flight Attendant", "Unverified catering update, vague authority, link to guidelines", 1),
        ("Uniform Compliance Warning", "Immediate Attention Required: Uniform Standard Violation", "Dear {name},\n\nOur system flagged a uniform compliance variance during your last flight segment. The uniform audit team requires you to confirm your measurements and submit a photo of your current uniform for verification. Your next roster assignment may be delayed until processed.\n\n[Submit Verification]", "complex", "Flight Attendant", "Fake compliance audit, photo upload request", 1),
        ("Crew Lounge Badge Access Issue", "Your Badge Access Failed – Action Needed", "Dear {name},\n\nA badge access failure was recorded at the Crew Lounge entry gate. Security needs you to validate your identity to avoid temporary suspension of lounge access privileges. Please complete the check below urgently.\n\n[Validate Identity]", "complex", "Flight Attendant", "Security-themed scare tactic, fake validation link", 1),
        ("Passenger Complaint Regarding Service", "Complaint Filed: Response Required Within 24 Hours", "Dear {name},\n\nA passenger from Flight 812 submitted a service-related complaint that references your name. The Customer Relations team requires your written clarification before the complaint escalates. Please review the summary and upload your statement.\n\n[Review Complaint]", "complex", "Flight Attendant", "Fear appeal, impersonation of customer relations, upload request", 1),
        ("Missing Safety Training Module", "URGENT: Incomplete Safety Module Recorded", "Dear {name},\n\nOur Learning Management System shows that your Safety Module Part 3 was not completed, even though your last submission indicated ‘finished’. The audit team needs confirmation so your compliance record isn’t flagged.\n\n[Re-Verify Completion]", "complex", "Flight Attendant", "Fake LMS link, urgent compliance tone", 1),
        ("Crew Rest Accommodation Change", "Layover Hotel Adjusted – Confirm ASAP", "Dear {name},\n\nDue to unexpected booking conflicts, your layover hotel for Flight 227 has been changed. You must confirm your updated check-in details before 6 PM today to avoid cancellation penalties.\n\n[Confirm New Hotel Booking]", "complex", "Flight Attendant", "Travel urgency, fake hotel confirmation", 1),
        ("Medical Readiness Document Update", "Action Needed: Updated Health Readiness Form Available", "Dear {name},\n\nYour medical readiness file requires a new signature due to procedure updates from Crew Health Services. Please review the revised policies and re-sign the document so your flight clearance remains active.\n\n[Review and Sign]", "complex", "Flight Attendant", "Fake medical form, electronic signature request", 1),
        ("Beverage Cart Inventory Irregularity", "Inventory Discrepancy – Verification Required", "Dear {name},\n\nStock Control found an inconsistency between your beverage cart log and the recorded post-flight inventory. You must verify the discrepancy to avoid a potential audit notation.\n\n[Verify Inventory Records]", "complex", "Flight Attendant", "Fake inventory audit, subtle pressure", 1),
        ("Crew Portal Reauthentication", "Your Crew Portal Session Will Expire – Renew Access", "Dear {name},\n\nYour crew scheduling portal authentication token is set to expire in 48 hours. Renew your access now to prevent loss of visibility into upcoming flight assignments and roster changes.\n\n[Renew Access]", "complex", "Flight Attendant", "Fake portal reauthentication, time pressure", 1),
        # HR (10)
        ("Benefits Coverage Verification Required", "IMPORTANT: Confirm Your Updated Benefits Coverage Before Processing", "Dear {name},\n\nDuring Monday’s HR sync, we reviewed several updates to this year’s benefits coverage. Our records show your acknowledgment form is still missing. If this is not completed before the deadline, coverage may be temporarily paused.\n\nPlease review the updated benefits summary and confirm your selections using the link below.\n\n[Review Benefits Summary]", "complex", "HR", "Deadline pressure, impersonation of HR, fake link", 1),
        ("Timesheet Correction Needed", "Timesheet Discrepancy Detected – Review Immediately", "Dear {name},\n\nPayroll identified an overtime discrepancy from last week’s logs. This issue was discussed in Monday’s HR meeting, and we must verify your entries before payroll closes. You may experience delayed payment if this isn’t corrected.\n\nPlease review and approve your corrected timesheet:\n\n[View Timesheet Adjustment]", "complex", "HR", "Payroll scare tactic, fake HR portal, urgency", 1),
        ("Conduct Policy Update – Signature Needed", "Updated Conduct & Ethics Policy – Digital Signature Required", "Dear {name},\n\nOur HR compliance team recently updated the employee conduct policy after several internal audits. You were listed as one of the employees who missed the discussion in Monday’s session. Please sign the acknowledgment to maintain compliance eligibility.\n\n[Sign Policy Acknowledgment]", "complex", "HR", "Fake compliance domain, urgent action", 1),
        ("Salary Adjustment Review", "Notice: Pending Salary Adjustment – Employee Confirmation Required", "Dear {name},\n\nDuring the quarterly review cycle, a pending salary adjustment was flagged for your profile. HR cannot proceed without your digital confirmation. This must be completed before Friday or your adjustment will be postponed.\n\nPlease confirm your adjustment details:\n\n[Confirm Salary Adjustment]", "complex", "HR", "Sensitive salary detail lure, urgency, fake HR login", 1),
        ("Training Completion Verification", "Compliance Training Incomplete – Immediate Attention Required", "Dear {name},\n\nOur system shows that you missed the final portion of your mandatory compliance training. This training was highlighted during Monday’s compliance briefing and must be completed before audit review begins.\n\nAccess your remaining module here:\n\n[Continue Training]", "complex", "HR", "Fake LMS link, compliance pressure", 1),
        ("Employee Benefits Audit Request", "HR Audit: Verify Your Employment & Benefits Information", "Dear {name},\n\nAs part of our annual HR audit cycle, we need you to verify your personal and benefits information. Several records appear incomplete due to a system sync issue earlier today.\n\nPlease verify your details below:\n\n[Verify Information]", "complex", "HR", "Vague audit request, fake form link", 1),
        ("Leave Hours Reset Warning", "Time-Off Balance Reset Soon – Confirm Remaining Hours", "Dear {name},\n\nYour current leave hours will reset next Monday as part of our policy update. You must confirm your remaining hours to ensure no time is lost. This was discussed during the HR Monday planning meeting.\n\nCheck your balance here:\n\n[View Leave Hours]", "complex", "HR", "Fake HR portal, urgency, lure of losing benefits", 1),
        ("Performance Review Summary Available", "Your Performance Review Summary Is Ready for Download", "Dear {name},\n\nThe HR Performance Team has finalized your mid-cycle evaluation. Please review your summary before it is archived. Failure to acknowledge may delay your eligibility for internal opportunities.\n\nDownload the summary below:\n\n[Download Review Summary]", "complex", "HR", "Fake document download, career implication pressure", 1),
        ("Direct Deposit Verification", "Your Direct Deposit Details Require Urgent Verification", "Dear {name},\n\nA mismatch was detected between your payroll file and your banking information. This may disrupt your upcoming paycheck if not resolved promptly.\n\nVerify your deposit information securely:\n\n[Verify Banking Details]", "complex", "HR", "Financial lure, sensitive info request, impersonation of payroll", 1),
        ("HR Meeting Follow-Up", "Missed Monday HR Sync – Action Items Assigned to You", "Dear {name},\n\nYou were marked absent during this week’s HR sync where we discussed major updates to workplace conduct, benefits, and training schedules. Action items were assigned to your profile and require acknowledgment.\n\nPlease review your action list:\n\n[View Assigned Items]", "complex", "HR", "Fear of missing responsibilities, fake HR portal", 1),
        # IT Support (10)
        ("Unauthorized Login Lockout", "ALERT: Suspicious Login Attempt — Action Needed", "Dear {name},\n\nOur system detected a login attempt from an unrecognized device accessing your airline IT profile earlier this morning. For security reasons, your account has been temporarily restricted until you verify your identity. Please review the access details and confirm whether this activity was performed by you.\n\n[Review Access Attempt]\n\nSender Style: Urgent IT tone.", "complex", "IT Support", "Urgency, fear tactic, fake IT alert, suspicious domain", 1),
        ("Helpdesk Ticket Verification Needed", "Unfamiliar IT Ticket Opened Under Your Name", "Dear {name},\n\nA helpdesk request was submitted under your ID regarding system slowdown issues on your workstation. Since our records show no previous report, we require confirmation. Please check the ticket summary and verify whether this request is legitimate.\n\n[View Ticket]\n\nSender Style: Professional but vague.", "complex", "IT Support", "Unexpected ticket, fake portal, urgency", 1),
        ("Mandatory Cybersecurity Patch", "Immediate Action Required: Install Critical Security Patch", "Dear {name},\n\nIT Security has released a critical patch following a recently identified vulnerability affecting airline crew and staff devices. Your device has not yet installed the patch. Failure to update may result in restricted system access.\n\n[Install Patch]\n\nSender Style: Formal corporate IT tone.", "complex", "IT Support", "Fake patch link, urgency, malware risk", 1),
        ("Password Expiration Reminder", "Your Password Will Expire at Midnight", "Dear {name},\n\nThis is a reminder that your login credentials for the Airline Employee Dashboard are expiring tonight due to recent system updates. To prevent access interruption, please reset your password by using the secure link below.\n\n[Reset Password]\n\nSender Style: Overly polite, almost flattering.", "complex", "IT Support", "Unverified sender, fake password reset", 1),
        ("System Outage Prevention Step", "Action Needed to Prevent Loss of Access", "Dear {name},\n\nWe identified a misconfiguration in your workstation that may cause disruption during tomorrow’s scheduled outage window. To prevent forced logout or data loss, please apply the configuration fix provided in the link below.\n\n[Apply Configuration Update]\n\nSender Style: Technical, authoritative.", "complex", "IT Support", "Fake configuration link, false urgency", 1),
        ("MFA Token Failure", "Multi-Factor Authentication Token Failure – Immediate Reset Required", "Dear {name},\n\nOur logs show repeated failures in generating your MFA token for secure login to the airline systems. To avoid being locked out of critical tools, please complete the MFA reset procedure.\n\n[Reset MFA Now]\n\nSender Style: Robotic, system-generated.", "complex", "IT Support", "Fake MFA portal, urgency", 1),
        ("IT Security Audit Prep", "Upcoming Network Security Audit – Your Review Required", "Dear {name},\n\nAhead of the internal IT compliance audit, your system has been flagged for missing documentation related to recent network access logs. Please review your audit checklist and upload the required files using the secure form.\n\n[Review Checklist]\n\nSender Style: Formal, compliance-focused.", "complex", "IT Support", "Fake audit request, upload lure", 1),
        ("New Software Deployment Notification", "New Airline Operations Tool — Installation Required", "Dear {name},\n\nIT has deployed a new internal software update that enhances crew communication and task routing. Your system shows the update as 'pending installation.' Complete the install before logging into tomorrow's shift.\n\n[Install Software]\n\nSender Style: Professional IT announcement.", "complex", "IT Support", "Fake software installer", 1),
        ("Cloud Backup Interruption", "Your Cloud Backup Failed Overnight", "Dear {name},\n\nYour scheduled cloud backup did not complete successfully during the overnight cycle. This may impact recovery of essential files used in operations. Please re-run the backup using the link below.\n\n[Resume Backup]\n\nSender Style: Gentle, supportive IT tone.", "complex", "IT Support", "Fake cloud portal, subtle urgency", 1),
        ("Device Enrollment Requirement", "Your Device Must Be Re-Enrolled in Security System", "Dear {name},\n\nRecent system upgrades require all employee laptops to be re-enrolled into the new Mobile Device Management (MDM) framework. Systems not updated will be disconnected from the Wi-Fi network. Complete enrollment now.\n\n[Enroll Device]\n\nSender Style: Strict IT directive.", "complex", "IT Support", "MDM impersonation, fake enrollment page", 1),
        # Pilot Operations (10)
        ("Flight Plan Revision", "URGENT: Updated Flight Plan Due to Weather System", "Dear {name},\n\nDispatch identified a rapidly developing weather front along your assigned corridor for tomorrow’s 0640 departure. A revised flight plan has been generated and must be acknowledged before crew pairing is finalized. Failure to confirm may delay cockpit readiness.\n\n[Review Updated Plan]\n\nThank you,\nOps Control", "complex", "Pilot Operations", "Urgency, unrealistic weather advisory, forced confirmation link", 1),
        ("Missed Flight Briefing Summary", "Action Needed: Monday Operational Briefing Summary Available", "Dear {name},\n\nIt appears you were marked absent from Monday’s operational briefing. Several new procedures regarding RNAV transitions and in-route fuel calculations were covered. Please review the summary and acknowledge the action items before your next assignment.\n\n[Open Briefing Summary]", "complex", "Pilot Operations", "Blaming tone, link to summary, vague sender identity", 1),
        ("Medical Certificate Warning", "Immediate Notice: Medical Certificate Verification", "Dear {name},\n\nYour Class 1 medical certificate shows an irregular expiration entry in our system after the recent sync update. To avoid automatic removal from active duty roster, verify the certificate details below. This step is required for flight eligibility.\n\n[Verify Certificate]", "complex", "Pilot Operations", "Threat of removal, credential harvest attempt", 1),
        ("Fuel Report Discrepancy", "Fuel Usage Irregularity Detected – Clarification Required", "Dear {name},\n\nOur analytics flagged an inconsistency in the fuel burn calculations for Flight 2841. The deviation exceeds the tolerance threshold established last quarter. Please confirm whether manual adjustments were applied by reviewing the detailed report.\n\n[Review Fuel Data]", "complex", "Pilot Operations", "Technical jargon to appear legitimate, false analytics", 1),
        ("Crew Pairing Update", "New Crew Pairing Assignment Available – Confirmation Needed", "Dear {name},\n\nA system update generated a revised crew pairing schedule impacting tomorrow’s rotation. Review your new pairing to avoid duty hour conflicts. Confirmation is necessary to finalize operations planning.\n\n[Confirm Pairing]", "complex", "Pilot Operations", "Scheduling urgency, generic ops wording", 1),
        ("Automation Patch Notice", "Cockpit Automation Suite Patch – Mandatory Installation", "Dear {name},\n\nA critical stability patch was released for the cockpit automation suite installed on your assigned fleet type. Pilots are required to install this module ahead of upcoming flights to ensure proper FMS alignment. Download the patch from the internal system below.\n\n[Download Patch]", "complex", "Pilot Operations", "Fake software update, malicious file link", 1),
        ("Safety Compliance Follow-Up", "Action Required: Incomplete Post-Flight Debrief", "Dear {name},\n\nThe automated post-flight reporting service indicates your debrief for Flight 619 is incomplete. This prevents proper incident logging and FAA-related audit closure. Please finalize the missing section at your earliest convenience.\n\n[Complete Debrief]", "complex", "Pilot Operations", "FAA audit scare, urgency", 1),
        ("Duty Time Irregularity", "Review Needed: Duty Hours Logged Incorrectly", "Dear {name},\n\nYour last recorded duty period appears to exceed the allowable threshold under crew rest regulations. This may impact your upcoming flight assignments. Verify the recorded hours and submit correction if applicable.\n\n[Verify Duty Log]", "complex", "Pilot Operations", "Regulation threat, credential capture", 1),
        ("Performance Notice", "Aircraft Performance Update – Review Required", "Dear {name},\n\nMaintenance uploaded new aircraft weight and balance reference numbers after a morning calibration failure. These updates may impact takeoff trim calculations for the next departure. Review the new figures as soon as possible.\n\n[View Updated Performance Data]", "complex", "Pilot Operations", "Technical details to seem credible, fake maintenance link", 1),
        ("Dispatch Callback", "Immediate Dispatcher Callback Required – Routing Change", "Dear {name},\n\nDispatch made an unexpected reroute adjustment for your evening flight following an ATC advisory. They were unable to reach you by phone. Confirm receipt and review the updated routing documentation below before preflight briefing.\n\n[Open Routing Update]", "complex", "Pilot Operations", "Urgency, ATC reference, no official identifiers", 1),
        # Training & Development (10)
        ("LMS Recertification Required", "URGENT: Training Recertification Deadline Approaching", "Dear {name},\n\nOur Learning Management System indicates you have not fully completed your annual recertification modules. This includes new FAA training updates reviewed in Monday’s training leadership meeting. Please finish the remaining sections and acknowledge the action items summarised in the portal.\n\n[Complete Recertification]", "complex", "Training & Development", "Urgency, impersonation of LMS, incorrect spelling of summarised", 1),
        ("Workshop Attendance Required", "Follow-Up Required: Monday Skills Workshop Summary", "Dear {name},\n\nYou were marked absent for the Monday skills enhancement workshop where we reviewed updated crew interaction procedures and compliance expectations. Please review the attached summary and confirm your understanding before your next shift.\n\n[Review Summary]", "complex", "Training & Development", "Attendance record pressure, vague attachment reference", 1),
        ("Instructor Evaluation", "Please Complete Your Instructor Evaluation Form", "Dear {name},\n\nAs part of our quarterly development cycle, all employees must complete evaluations for their assigned instructors. The system shows your evaluation is still pending and will affect your certification progress if left incomplete.\n\n[Submit Evaluation]", "complex", "Training & Development", "Fake evaluation link, pressure tactic", 1),
        ("Training Compliance Notice", "Training Compliance Alert – Immediate Review Needed", "Dear {name},\n\nOur records show an inconsistency between your logged flight training hours and your recorded module completion times. This discrepancy was discussed in today’s compliance meeting and requires your immediate review.\n\n[Verify Training Records]", "complex", "Training & Development", "Claims of discrepancies, fear tactic", 1),
        ("Procedure Update", "New Training Module Released for Updated Procedures", "Dear {name},\n\nA new procedure update regarding passenger handling and onboard protocol was released this morning. All staff must review the revised steps and acknowledge the update in the training portal.\n\n[Access Updated Module]", "complex", "Training & Development", "Fake portal link, urgency implied", 1),
        ("Exam Scheduling Required", "Schedule Your Annual Certification Exam", "Dear {name},\n\nYour certification exam window opens today and must be scheduled this week to maintain operational eligibility. Please select your exam time using the scheduling portal below.\n\n[Schedule Exam]", "complex", "Training & Development", "Fake scheduling link, time pressure", 1),
        ("Training Access Expiration", "Training Portal Access Token Expiring Soon", "Dear {name},\n\nYour access token to the LMS dashboard will expire within the next 48 hours due to a security update applied by the IT training systems team. Renew your token to avoid interruption.\n\n[Renew Access Token]", "complex", "Training & Development", "Fake IT/training system change, technical jargon misuse", 1),
        ("FAA Revision Module", "New FAA Compliance Training Revision Released", "Dear {name},\n\nThe FAA has issued updated compliance guidelines that were reviewed in the Monday aviation training committee meeting. All airline staff must complete the revision module to maintain certification alignment.\n\n[Open Compliance Module]", "complex", "Training & Development", "Authority mimicry, urgency, misdirection", 1),
        ("Learning Path Update", "Your Assigned Learning Path Has Been Updated", "Dear {name},\n\nBased on recent performance and department-wide development goals, your training sequence has been adjusted. Please log into the development portal to review the new required modules.\n\n[View Updated Learning Path]", "complex", "Training & Development", "Fake portal, personalized manipulation", 1),
        ("Training Incident Review", "Action Needed: Training Incident Review Pending", "Dear {name},\n\nDuring yesterday’s simulation session, an incident was flagged in your training log that requires clarification. Please review the logged event and submit your corrective action steps.\n\n[Review Training Incident]", "complex", "Training & Development", "Fear-based urgency, ambiguous incident reference", 1),
        # Student / Early Career / Intern (10)
        ("Intern Orientation Follow-Up – Action Required", "Action Needed: Missing Onboarding Checklist Items", "Dear {name},\n\nOur records show you were marked absent for Monday’s onboarding sync. Several required documents—ID verification, project placement forms, and confidentiality acknowledgment—are still missing. Please review the orientation recap and confirm next steps using the link below.\n\n[Complete Onboarding Checklist]", "complex", "Student/Early Career", "Claims of missing forms, urgency, fake onboarding portal", 1),
        ("Updated Project Assignment Available", "Your Internship Project Assignment Has Been Updated", "Dear {name},\n\nDue to shifting department priorities, your assigned internship project has changed. Review your new mentor details and first-week deliverables in the updated plan. Completion acknowledgment is required within 24 hours.\n\n[View Updated Assignment]", "complex", "Student/Early Career", "Unexpected assignment change, forced acknowledgment, suspicious link", 1),
        ("Mentor Evaluation Request", "Complete Required Mentor Evaluation Form", "Dear {name},\n\nAs part of your early-career program, a brief evaluation of your assigned mentor is required. Failure to submit before the deadline may affect your completion status. Access the evaluation portal below.\n\n[Submit Evaluation]", "complex", "Student/Early Career", "Fake survey portal, deadline pressure", 1),
        ("Intern Payroll Notice", "Stipend Adjustment – Verification Required", "Dear {name},\n\nA discrepancy was detected in your recorded hours for last week’s internship schedule. To avoid payment delay, confirm your time entries and verify your stipend information immediately using the secure link below.\n\n[Verify Hours]", "complex", "Student/Early Career", "Payroll impersonation, urgent verification request", 1),
        ("Flight Shadowing Program Invitation", "Confirm Participation in Cockpit Shadow Experience", "Dear {name},\n\nYou have been selected for a special intern shadowing session with one of our flight crews. Due to limited spots, confirmation is required today. View the schedule and required briefing packet below.\n\n[Confirm Participation]", "complex", "Student/Early Career", "High-value opportunity lure, false sense of exclusivity", 1),
        ("Security Badge Registration Incomplete", "URGENT: Your Intern Badge Has Not Been Activated", "Dear {name},\n\nSecurity notified us that your access badge registration was left incomplete during onboarding. Without activation, building entry will be suspended starting tomorrow. Complete registration immediately at the link below.\n\n[Activate Badge]", "complex", "Student/Early Career", "Badge access urgency, fake security domain", 1),
        ("Supervisor Feedback Summary", "Intern Performance Summary Available", "Dear {name},\n\nYour supervisor submitted a mid-rotation feedback summary. To prepare for next week’s performance review, please read and acknowledge the comments provided. The document is accessible below.\n\n[View Feedback Summary]", "complex", "Student/Early Career", "Emotional manipulation, fake HR document portal", 1),
        ("Housing Support Update", "Reminder: Submit Housing Verification Documents", "Dear {name},\n\nWe noticed you have not completed the housing verification form required for relocation assistance. Submit your documentation immediately to avoid disqualification from the stipend program.\n\n[Submit Documents]", "complex", "Student/Early Career", "Financial lure, urgent documentation request", 1),
        ("Certification Training Deadline", "Mandatory Early-Career Training Module Overdue", "Dear {name},\n\nYour introductory safety and compliance training remains incomplete. This module is required for interns working in operational areas. Complete the training before your access expires.\n\n[Complete Training]", "complex", "Student/Early Career", "Fake LMS portal, expiry warning", 1),
        ("Career Fair Registration Error", "Important: Your Registration Could Not Be Processed", "Dear {name},\n\nYour registration for the Airline Early-Career Networking Fair failed due to incomplete profile data. Spots are limited, so you must update your registration immediately using the portal below.\n\n[Fix Registration]", "complex", "Student/Early Career", "FOMO lure, fake event portal", 1),
    ]
    templates.extend(extra_templates)

    complex_plus_templates = [
        ("Component Variance Report Follow-Up", "Technical Variance Review Required – Immediate Confirmation", "Dear {name},\n\nDuring last week’s component audit, our Quality Assurance division identified inconsistencies between the torque parameters submitted on Form 19A and the automated readings logged in the AMOS system. While this may be a syncing delay, your signature is required to validate the corrected entry. If unresolved by end of shift, maintenance records will be flagged for compliance review.\n\nAccess your pre-filled variance report below and approve the adjusted parameters.\n\n[Open Variance Report]", "complex+", "Aircraft Maintenance and Support", "Deep technical jargon, subtle compliance pressure, false AMOS sync alert", 1),
        ("FAA Non-Compliance Crosscheck", "Urgent: FAA Crosscheck Flag on Recent Maintenance Entry", "Dear {name},\n\nAn automated FAA audit sweep flagged an anomaly connected to your recent inspection logs on aircraft N482JP. The discrepancy is minor, likely tied to batch sequencing, but requires your acknowledgment before the database is finalized tonight. Failure to validate could trigger a manual review of associated tasks.\n\nPlease verify the updated compliance status through the temporary portal below.\n\n[Review Compliance Status]", "complex+", "Aircraft Maintenance and Support", "References FAA audits, aircraft tail numbers, realistic but falsified compliance urgency", 1),
        ("Engine Diagnostics Sync Failure", "Engine Diagnostics File Not Synced – Manual Upload Requested", "Dear {name},\n\nYesterday’s post-flight engine diagnostic package did not sync correctly from the onboard ECTM system into our ground analytics server. This creates a gap in the predictive maintenance model for the next flight rotation. To prevent forecasting errors, we require manual verification of the diagnostic bundle associated with Flight 771A.\n\nPlease use the secure portal below to confirm or re-upload the missing log files.\n\n[Upload Diagnostics Bundle]", "complex+", "Aircraft Maintenance and Support", "Highly technical aviation terminology, realistic system sync failure", 1),
        ("TSA Access Review Required", "Critical: TSA Secure Area Audit Found Badge Irregularities", "Dear {name},\n\nA TSA compliance sweep detected unusual swipe patterns associated with your badge ID over the past three operational days. While this is often caused by gate reassignments or shift overlaps, TSA requires verification from affected staff as part of the routine investigation. Your confirmation must be filed within 12 hours to avoid temporary access suspension.\n\nSubmit your access review using the secure form below.\n\n[Submit Access Verification]", "complex+", "At the Airport", "References TSA, badge logs, operational timing—very realistic", 1),
        ("Ramp Safety Rebrief Required", "Mandatory Review: Ramp Incident Safety Rebriefing", "Dear {name},\n\nFollowing Monday’s airside equipment incident, the Ramp Safety Office is coordinating a rapid rebrief for all personnel assigned to Zones B–D during the last rotation block. Although you were not directly involved, your shift overlap requires that you acknowledge updated procedures. The incident details and corrective steps have been uploaded for your review.\n\nPlease access the rebriefing packet below and sign the acknowledgment.\n\n[View Safety Packet]", "complex+", "At the Airport", "Mentions zones, rotations, incident follow-up—extremely believable", 1),
        ("Gate Resource Scheduling Conflict", "URGENT: Gate Resource Conflict Requires Your Confirmation", "Dear {name},\n\nA scheduling conflict was detected between your assigned gate operations for Flights 1190 and 2203. This appears to be a dispatch tool caching issue, but the operations desk requires immediate confirmation from you to prevent cascading delays. Affected gate teams have already been notified, and your action will finalize the corrected coverage sequence.\n\nPlease confirm the updated assignment timeline below.\n\n[Review Updated Gate Schedule]", "complex+", "At the Airport", "Uses dispatch vocabulary, flight numbers, operational urgency", 1),
        ("Executive Policy Brief Acknowledgment", "Required: Review Updates to Executive Compliance Brief", "Dear {name},\n\nDuring Monday’s leadership alignment meeting, several adjustments were made to the corporate governance framework, including revisions to data retention expectations and interdepartmental approval routing. Attendance records indicate you were marked absent, so the system has flagged your acknowledgment as incomplete. Please review the updated brief before quarterly certification begins.\n\nAccess document: [Open Compliance Brief]", "complex+", "Corporate", "High-level policy language, governance terminology, realistic meeting reference", 1),
        ("Data Risk Exposure Review", "Risk Advisory: Potential Exposure Requires Confirmation", "Dear {name},\n\nOur automated compliance engine detected irregular workflow patterns tied to your file access timestamps last Thursday. While this is likely related to cross-departmental collaboration, risk mitigation procedures require employees to confirm whether any shared documents included sensitive material. This review must be completed before system recalibration tonight.\n\nPlease validate your exposure status using the secure portal.\n\n[Validate Access Logs]", "complex+", "Corporate", "Deeply corporate risk language, feels internal and official", 1),
        ("Strategic Initiative Sync", "Follow-Up Needed: Strategic Plan Sync Notes Incomplete", "Dear {name},\n\nThe recap document from the quarterly Strategic Initiatives Sync indicates missing acknowledgment from several participants, including yourself. Since this briefing outlines cross-functional directives for the upcoming fiscal cycle, the Strategy Office requires confirmation from all listed collaborators. Delays in acknowledgment may impact resource allocation planning.\n\nPlease review and sign off on the recap below.\n\n[Review Strategic Summary]", "complex+", "Corporate", "References fiscal cycles, alignment meetings, strategy offices—very realistic", 1),
        ("Core System Integrity Notice", "Immediate Verification Required: Core System Integrity Review Pending", "Dear {name},\n\nOur monitoring system detected a cascading replication delay inside the internal cloud cluster supporting the OpsDash dashboard. While the issue appears isolated, engineering requires each user to validate their stored API tokens to ensure no cross-tenant corruption occurred. Your account was specifically flagged due to inconsistent session signatures logged during Sunday’s maintenance window.\n\nTo proceed, review your encrypted token summary and approve the automated reset protocol. Failure to acknowledge by EOD will suspend dashboard write-access to prevent further propagation.\n\nPlease complete your validation below:\n[Review Token Summary]", "complex+", "Digital Technology", "Highly technical language, fake system event, fear + urgency, credential reset trap", 1),
        ("Container Deployment Rollback Required", "Action Required: Unexpected Deployment Behavior in v2.9.4 Patch", "Dear {name},\n\nDuring automated testing of Build v2.9.4, a discrepancy was discovered in your assigned microservice container—specifically around the environment variable injection layer. The orchestration logs show that your deployment signature did not match the last approved version, causing the staging pipeline to freeze.\n\nTo finalize the rollback and unblock the CI/CD process, DevSecOps needs you to review your container diff report and confirm the corrected configuration values. If no action is taken, your service will be auto-removed from the next deployment cycle due to integrity mismatch.\n\nAccess your diff below:\n[Open Container Diff Report]", "complex+", "Digital Technology", "Impersonated DevSecOps, technical jargon, fake CI/CD pipeline urgency", 1),
        ("Encrypted Credential Rotation Audit", "Confidential: Credential Rotation Audit — Verification Needed", "Dear {name},\n\nAs part of the quarterly Infrastructure Security Review, your encrypted credential history was selected for random audit. Recent irregularities in the authentication ledger suggest that your last MFA-binding event failed to propagate to the secondary verification node.\n\nSecurity engineering requires you to manually validate the checksum of your credential package to ensure it has not been altered during transit between identity providers. Because your profile is tagged for production access, delays may trigger an account quarantine under zero-trust protocol.\n\nComplete your checksum verification here:\n[Validate Credential Package]", "complex+", "Digital Technology", "Overly technical security details, fake compliance audit, high-pressure tone", 1),
        ("Passenger Escalation Chain Review Required", "Tier-3 Escalation Audit: Customer Interaction Summary Needed", "Dear {name},\n\nA recent passenger escalation was automatically routed to Tier-3 Quality Review due to mismatched timestamps between your case notes and system-generated logs. The discrepancy suggests that one of your updates may not have synced with the central case-handling queue.\n\nTo finalize the review, Customer Ops requires you to validate the interaction summary that has been temporarily reconstructed using the backup log stream. Please note: unresolved discrepancies may result in temporary account restriction to prevent further data contamination.\n\nReview the reconstructed summary below:\n[Open Escalation Summary]", "complex+", "Customer Solutions", "Fake escalation notice, fear appeal, false data integrity issue", 1),
        ("Service Recovery Workflow Validation", "Service Recovery Protocol Update — Immediate Employee Validation Needed", "Dear {name},\n\nOur automated service-recovery engine flagged inconsistent adherence to compensation rules for disrupted passengers on Flight 771. According to the records, your approval path deviated from the updated recovery policy implemented last Monday.\n\nTo ensure compliance, Operations has generated a personalized workflow validation package outlining your last seven recovery actions. Please confirm the updated flow and acknowledge the revised approval matrix before tomorrow’s audit cycle begins.\n\nAccess your validation package here:\n[Review Workflow Update]", "complex+", "Customer Solutions", "False personalized audit, fake compensation rules, urgency tied to compliance", 1),
        ("Customer Data Handling Breach Verification", "Restricted Notice: Potential Data Misclassification Involving Your Cases", "Dear {name},\n\nDuring a random compliance review, automated classification models detected unusual metadata attached to three of your recent customer cases. The anomaly suggests that sensitive passenger information may have been incorrectly tagged, resulting in a potential data-handling breach.\n\nRegulations require you to review and confirm the corrected classification labels before Compliance forwards the report to oversight committees. If this verification is not submitted within 24 hours, your account will be restricted pending investigation.\n\nBegin your classification review below:\n[Begin Verification]", "complex+", "Customer Solutions", "Strong compliance scare, fake regulatory requirement, forced urgency", 1),
        ("Disrupted Passenger Resolution Transcript Audit", "Quality Control Flag — Review Your Recorded Passenger Interaction", "Dear {name},\n\nA technical sync issue during yesterday’s disrupted-flight response caused several recorded passenger interactions to be partially corrupted. One of the affected logs was tied to a conversation you handled during the cancellation surge.\n\nTo restore data integrity, Quality Review reconstructed a transcript based on AI-assisted audio parsing, but it requires your manual confirmation before it can be certified as accurate. Please review the document and approve or correct the flagged statements.\n\nFailure to verify may result in the ticket remaining unresolved in the central system.\n[Review Transcript]", "complex+", "Customer Service", "AI reconstruction claim, compliance tone, oddly realistic reconstruction story", 1),
        ("Customer Compensation Eligibility Reassessment", "Urgent: Passenger Compensation Eligibility Mismatch Detected", "Dear {name},\n\nOur compensation algorithm flagged an inconsistency between your service notes and the auto-generated disruption code for Passenger ID #884219. This mismatch prevents the system from releasing the appropriate refund or voucher.\n\nYour confirmation is required to finalize the eligibility recalculation before the nightly batch process begins. Please review the recalculated values and approve the recommended resolution.\n[Open Eligibility Report]", "complex+", "Customer Service", "Fabricated algorithm mismatch, nightly batch urgency, impersonation of QA systems", 1),
        ("Customer Priority Queue Handling Review", "Priority Handling Irregularity — Action Needed Before Queue Refresh", "Dear {name},\n\nA system review identified that one of your customers in the Priority Queue was incorrectly assigned a lower-level service tier after your final update. The issue appears to stem from the queue refresh failure during Monday’s high-volume period.\n\nTo correct the issue, Operations generated a corrected customer profile snapshot that requires your verification. If it is not approved, the customer may be rerouted to general support, affecting SLA metrics for your team.\n\nApprove the updated profile here:\n[Verify Customer Profile]", "complex+", "Customer Service", "SLA manipulation pressure, fake queue refresh, urgent fix requirement", 1),
        ("Quarterly Ledger Discrepancy Review – Finance Oversight Required", "URGENT: Q2 Ledger Variance Requires Senior Review", "Dear {name},\n\nDuring the internal audit of Q2 ledgers, a recurring mismatch was detected in the vendor credit reconciliation sheet tied to your department’s cost center. Since the variance spans multiple regional accounts, Finance Oversight has flagged your profile for priority verification. We need confirmation on whether the adjusted totals reflect your final submissions or if the automated sync failed.\n\nPlease download the consolidated report and validate the updated line items before the file locks for compliance export.\n\n[Download Consolidated Ledger Report]\n\nThank you for addressing this promptly.", "complex+", "Finance", "Complex audit terminology, urgent reconciliation, attachment lure, impersonation of Finance Oversight", 1),
        ("International Transfer Held Due to Compliance Update", "Compliance Review Required: Pending International Wire Transfer", "Dear {name},\n\nOur cross-border settlement system detected missing verification metadata in a wire transfer initiated under your regional queue. Due to new AML procedural changes, all international transfers flagged as ‘Unverified Routing Origin’ must be manually approved before processing. The transfer is currently paused and will auto-cancel if the correct approval token is not submitted.\n\nYou are required to authenticate the transfer details and upload a confirmation note to release funds.\n\n[Review Transfer Documentation]\n\nYour immediate attention is appreciated.", "complex+", "Finance", "AML terminology, realistic wire transfer language, urgency, compliance impersonation", 1),
        ("ERP Finance Module Failure – Manual Override Needed", "Critical: ERP Failure Interrupted Finance Batch Processing", "Dear {name},\n\nThe enterprise ERP system encountered an unexpected failure during tonight’s batch posting cycle, and several of your financial entries have been rerouted to the manual override queue. This typically occurs when a profile’s authentication token expires mid-cycle or when a macro-generated document fails integrity checks. To avoid downstream errors impacting next week’s payroll, please verify the affected documents and reauthorize your credentials.\n\nA temporary dashboard has been created for affected users only.\n\n[Access ERP Override Dashboard]\n\nFailure to respond may delay payroll postings.", "complex+", "Finance", "Deep technical ERP terminology, believable system failure, urgent payroll implication", 1),
        ("Updated Cabin Safety Protocol – Immediate Review Required", "Mandatory: New Safety Procedure Revision for Crew", "Dear {name},\n\nFollowing an FAA advisory issued this morning, cabin crew safety procedures for turbulence-related incidents have been revised. Several inflight response steps—including passenger restraint checks and beverage cart lockdown requirements—have been modified. Flight Operations has requested that all currently scheduled attendants review the new digital manual and acknowledge compliance before their next duty period.\n\nPlease confirm your understanding by accessing the updated revision notes.\n\n[Open Safety Protocol Revision Document]\n\nFailure to acknowledge may result in roster suspension.", "complex+", "Flight Attendant", "Highly realistic FAA procedure update, mention of roster suspension, authoritative tone", 1),
        ("Crew Accommodation Discrepancy", "Layover Accommodation System Error – Manual Confirmation Needed", "Dear {name},\n\nAn unexpected error in the Crew Accommodation Portal caused several layover hotel assignments, including yours, to be logged under an outdated vendor contract. This means your upcoming overnight stay may not have a confirmed reservation unless manually validated. Crew Logistics has asked all affected attendants to verify their details, including check-in time and room assignment.\n\nPlease review the updated details and confirm your acceptance to prevent on-arrival delays.\n\n[Review Layover Assignment]\n\nThank you for your cooperation.", "complex+", "Flight Attendant", "Hotel reservation issue, logistics terminology, believable crew workflow", 1),
        ("Inflight Service Audit Findings – Crew Response Required", "Action Required: Pending Review of Service Quality Compliance", "Dear {name},\n\nOur post-flight compliance audit detected inconsistencies in the inflight service logs from routes you recently staffed. These include missing timestamps for service initiation and incomplete allergen disclosure forms submitted via the EFB. Before these findings are escalated to Quality Assurance, you are required to review the flagged items and acknowledge whether the entries were system-generated errors.\n\nPlease verify the logs using the secure link below.\n\n[Verify Service Compliance Logs]\n\nYour timely response will prevent unnecessary escalation.", "complex+", "Flight Attendant", "Audit terminology, quality assurance escalation, fake EFB log review", 1),
        ("Workplace Conduct Policy – Addendum Review Required", "MANDATORY: Conduct Policy Addendum Pending Employee Signature", "Dear {name},\n\nAs part of our annual ethics review, HR has issued an addendum addressing interpersonal conduct, remote-work professionalism, and data confidentiality expectations for all airline personnel. Your previous acknowledgment does not cover the updated clauses, and your profile has been automatically queued for secondary verification. The system will record non-acknowledgment as non-compliant during the upcoming HR audit.\n\nPlease review and sign the addendum via the secure acknowledgment portal.\n\n[Sign Conduct Addendum]\n\nThank you for your cooperation.", "complex+", "HR", "Legal language, HR compliance pressure, policy signature request", 1),
        ("Compensation Band Rebalancing – Review Your Updated Grade", "HR Notice: Salary Band Adjustment Pending Verification", "Dear {name},\n\nFollowing a broad restructuring of pay grades across the organization, HR Compensation has flagged several employee profiles for salary band review—including yours. Before adjustments are finalized in payroll, you must verify whether your current classification matches your documented experience and department assignment. This step ensures compliance with federal pay transparency regulations.\n\nAccess your updated compensation summary below.\n\n[View Updated Compensation Summary]\n\nYour prompt review is required.", "complex+", "HR", "Pay transparency compliance, believable HR restructuring scenario", 1),
        ("Health Coverage Vendor Integration Failure – Manual Confirmation Needed", "URGENT: Insurance Enrollment Info Not Synced", "Dear {name},\n\nDuring our vendor transition to a new healthcare provider, several employee coverage files—including yours—failed to sync due to missing enrollment metadata. This means your health insurance may show as inactive during claims processing unless manually confirmed in the system. HR Benefits has created a temporary portal for affected employees to validate their dependents and coverage tier.\n\nPlease confirm your information immediately.\n\n[Confirm Health Coverage Details]\n\nWe apologize for the inconvenience.", "complex+", "HR", "Healthcare system sync failure, fake benefits verification portal", 1),
        ("Critical Encryption Rollback Alert", "URGENT: Device Encryption Reverted Due to Sync Conflict", "Dear {name},\n\nOur endpoint monitoring system detected that your workstation's encryption status reverted after a failed overnight sync with the airline security server. This issue typically occurs when configuration files become desynchronized during Wi-Fi handover at an airport terminal.\n\nTo avoid mandatory device quarantine, please review the synchronization log and apply the corrective rollback patch. The security team must validate your update before 18:00 today.\n\n[View Sync Log & Apply Patch]\n\nThank you for your immediate cooperation.\nIT Security Operations", "complex+", "IT Support", "Highly technical jargon, unexpected encryption failure claim, urgent corrective action, fake security portal", 1),
        ("Multi-Factor Device Trust Failure", "Action Required: Identity Trust Reset for Network Device", "Dear {name},\n\nA recent trust-score evaluation flagged inconsistencies between your MFA token and your workstation ID signature. This mismatch can occur after prolonged VPN sessions or when tokens fail to refresh during travel between regional hubs.\n\nFor continued access to corporate systems—including email, crew scheduling tools, and maintenance dashboards—you must complete the identity re-binding process through our automated verification console.\n\nPlease complete the required verification within the next 4 hours.\n\n[Re-Bind Device Identity]\n\nIT Zero Trust Management", "complex+", "IT Support", "Zero-trust jargon, identity mismatch claim, sophisticated impersonation of internal security", 1),
        ("Compromised Certificate Chain Investigation", "Security Advisory: Certificate Chain Compromise Under Review", "Dear {name},\n\nOur SOC detected an anomaly in certificate-chain validation affecting devices recently logged in from airport lounges. One of the intermediate certificates associated with your profile appears to have been re-issued unexpectedly, triggering an internal investigation.\n\nUntil the certificate lineage is verified, you are required to generate a temporary validation key to maintain system access. Failure to do so may result in automatic off-boarding from secure airline networks.\n\n[Generate Temporary Validation Key]\n\nThank you for your prompt attention.\nCybersecurity Certificate Authority Team", "complex+", "IT Support", "Highly specialized PKI terminology, certificate compromise scare, urgent key generation request", 1),
        ("Emergency Flight Path Compliance Override", "Immediate Review Required: Automated FAA Routing Override Triggered", "Dear {name},\n\nDuring the automated routing alignment update, your assigned flight path generated an FAA compliance override due to new transcontinental airspace restrictions issued earlier this morning. Your prior approval may no longer be valid, and dispatch is requesting immediate confirmation of your revised approach windows.\n\nThe review includes airspace altitude adjustments, crosswind recalculations, and emergency diversion protocols. Your prompt acknowledgment ensures no delays in pre-flight clearance.\n\n[Review Updated FAA Routing Packet]\n\nDispatch Compliance Office", "complex+", "Pilot Operations", "Highly technical operational context, FAA compliance scare, realistic flight operations terminology", 1),
        ("Cockpit EFB Firmware Mismatch Report", "Required Action: EFB Firmware Mismatch Detected During Pre-Flight Sync", "Dear {name},\n\nA discrepancy was detected in your cockpit EFB firmware during the auto-sync cycle with the central avionics database. This mismatch can cause delay in retrieving MEL updates, turbulence advisories, and automated takeoff performance calculations.\n\nBefore your next assigned leg, you must validate the firmware hash and perform a corrective sync. Dispatch cannot finalize your load sheet without successful confirmation.\n\n[Validate EFB Firmware Hash]\n\nAvionics Technical Support", "complex+", "Pilot Operations", "Deep avionics terminology, credible operational chain, mandatory verification lure", 1),
        ("Crew Fatigue Compliance Audit", "Immediate Acknowledgment Needed: Fatigue Risk Index Inconsistency Found", "Dear {name},\n\nOur Fatigue Risk Management System detected irregularities between your logged rest periods and the automated layover tracking feed. This inconsistency requires pilot acknowledgment before your next duty assignment can be approved.\n\nYou will need to review your rest log, confirm biometric fatigue indicators recorded by your issued device, and validate your next duty window. Failure to confirm may result in temporary removal from the duty roster.\n\n[Review Fatigue Compliance Log]\n\nFlight Safety & Regulation Team", "complex+", "Pilot Operations", "Uses real fatigue management terminology, invokes safety auditing, urgent compliance check", 1),
        ("Competency Reassessment Requirement", "Annual Re-Evaluation: Competency Metrics Flagged for Review", "Dear {name},\n\nA recalculation of your competency metrics—based on instructor evaluations, LMS module analytics, and cross-departmental performance indicators—shows an inconsistency requiring reassessment. This reassessment ensures compliance with updated airline training standards.\n\nYou must review your personalized development matrix, acknowledge new expectations, and complete the associated micro-assessment before it locks at 23:59 today.\n\n[Access Competency Matrix]\n\nTraining Quality Assurance Division", "complex+", "Training & Development", "Complex HR/training jargon, false performance data, urgent compliance reminder", 1),
        ("Certification Validity Integrity Check", "Action Needed: Certification Integrity Check Failed During System Merge", "Dear {name},\n\nOur training platform recently migrated to a unified credentialing system. During the merge, your certificate IDs did not align with the expected validation schema, suggesting a possible integrity mismatch.\n\nThis requires immediate revalidation to avoid temporary revocation of your operational training status. Review the mismatched credential set and confirm authenticity.\n\n[Validate Certification Records]\n\nAirline Workforce Development", "complex+", "Training & Development", "Credential mismatch scare, impersonates formal training systems, urgency", 1),
        ("Instructor Feedback Reconciliation Task", "Review Required: Inconsistency in Multi-Instructor Evaluation Report", "Dear {name},\n\nWe identified a disparity between multiple instructors’ evaluations logged across different training modules. This discrepancy affects your progression scoring, which determines eligibility for next-quarter advancement opportunities.\n\nYou are required to reconcile the evaluations, acknowledge corrected comments, and submit a confirmation report for audit.\n\n[Review Consolidated Evaluation Report]\n\nProfessional Skills Assessment Team", "complex+", "Training & Development", "Complex evaluation terminology, performance pressure, fake audit requirement", 1),
        ("Internship Compliance Verification Packet", "Action Required: Missing Compliance Items in Your Internship File", "Dear {name},\n\nYour internship file is undergoing a quarterly audit, and several documents—mentor evaluation notes, onboarding confirmations, and rotation availability forms—appear unverified in the system. This discrepancy may delay credit approval for your current cycle.\n\nPlease review the flagged documents and submit the required acknowledgments to maintain active status.\n\n[Open Compliance Verification Packet]\n\nEarly Career Program Office", "complex+", "Student/Early Career", "Administrative audit terminology, missing document scare, formal tone", 1),
        ("Rotation Assignment Adjustment Notice", "Important: Rotation Reassignment Pending Confirmation", "Dear {name},\n\nProgram scheduling identified overlapping rotations between your assigned department and operations support. To avoid conflicts during peak flight hours, your rotation may be reassigned pending your acknowledgement.\n\nReview the proposed rotation changes and confirm your availability before the adjustment is finalized.\n\n[Review Rotation Proposal]\n\nIntern Development Services", "complex+", "Student/Early Career", "Scheduling conflict scare, operational terminology, formal but urgent tone", 1),
        ("Mentor Session Accountability Log", "Follow-Up Required: Missing Mentor Session Logs", "Dear {name},\n\nOur system shows that your last three mentor check-in sessions were logged without attached notes, preventing accurate tracking of your development progress for this quarter. These logs must be reconciled for performance evaluation.\n\nPlease review all pending mentor logs and provide required confirmations.\n\n[Update Mentor Session Notes]\n\nCareer Pathways Review Team", "complex+", "Student/Early Career", "Fake missing logs, believable corporate structure, high-pressure evaluation tone", 1),
    ]
    templates.extend(complex_plus_templates)

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
