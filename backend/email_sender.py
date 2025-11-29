# Replace with real provider (SendGrid/Mailgun). This shows how to build tracked links.
def build_email_html(sim_subject: str, sim_content: str, link_slug: str, delivery_id: int, api_base="http://localhost:8000"):
    track_open_url = f"{api_base}/o/{delivery_id}"
    tracked_link = f"{api_base}/t/{link_slug}?d={delivery_id}"
    return f"""
    <html>
      <body>
        <p>{sim_content}</p>
        <p><a href="{tracked_link}">View details</a></p>
        <img src="{track_open_url}" width="1" height="1" />
      </body>
    </html>
    """

# Use your provider to send: subject, to email, html body
