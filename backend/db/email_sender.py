import sqlite3
from datetime import datetime, timedelta
import random

from backend.db.email_scheduler import send_email

# Connect to (or create) the database file in the same directory
connection = sqlite3.connect("database.db")
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
    "easy", "IT Support", "Fake survey link, minimal red flags", 1),]

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
        SELECT se.id, se.user_id, et.subject, et.body, u.email
        FROM scheduled_emails se
        JOIN email_templates et ON se.template_id = et.id
        JOIN users u ON se.user_id = u.id
        WHERE se.scheduled_time <= ? AND se.sent = 0
    ''', (now,))
    
    emails_to_send = cursor.fetchall()
    
    for email_id, user_id, subject, from_addr, body, recipient_email in emails_to_send:
        
        # Send email (use actual email service)
        send_email(recipient_email, subject, from_addr, body)
        
        # Create simulation record
        cursor.execute('''
            INSERT INTO simulations (user_id, email_content, simulation_type) 
            VALUES (?, ?, 'phishing_test')
        ''', (user_id, body))
        
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