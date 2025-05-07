import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Nonprofit Marketing Strategy Builder", layout="centered")

if "strategy_output" not in st.session_state:
    st.session_state.strategy_output = ""

st.title("🧠 Nonprofit Marketing Strategy Builder")
st.markdown("Answer the questions below to generate a personalized, strategic nonprofit marketing plan.")

# ROI Sidebar Calculator
st.sidebar.header("💸 ROI Simulator")
st.sidebar.markdown("Adjust sliders to forecast how improving key metrics can impact your donation revenue.")

open_rate = st.sidebar.slider("Email Open Rate (%)", 10, 60, 20)
ctr = st.sidebar.slider("Email Click-Through Rate (%)", 0, 25, 3)
conversion_rate = st.sidebar.slider("Donation Page Conversion (%)", 1, 25, 8)
traffic_conversion = st.sidebar.slider("Website Traffic-to-Donation Conversion (%)", 1, 25, 4)
avg_donation = st.sidebar.slider("Average Donation Size ($)", 10, 200, 35)
recurring_rate = st.sidebar.slider("Recurring Donor Conversion (%)", 1, 50, 10)
monthly_email_volume = st.sidebar.number_input("Emails Sent per Month", min_value=1000, value=20000)
website_visitors = st.sidebar.number_input("Website Visitors per Month", min_value=1000, value=10000)

# ROI Estimate
email_clicks = monthly_email_volume * (open_rate / 100) * (ctr / 100)
email_donations = email_clicks * (conversion_rate / 100)
traffic_donations = website_visitors * (traffic_conversion / 100)
total_donations = email_donations + traffic_donations
monthly_revenue = total_donations * avg_donation
recurring_revenue = total_donations * (recurring_rate / 100) * avg_donation
total_monthly = monthly_revenue + recurring_revenue

st.sidebar.markdown(f"**Estimated Monthly Revenue: ${total_monthly:,.0f}**")
st.sidebar.markdown("This estimate combines email and website strategies. Adjust sliders to simulate results.")

# Form input
with st.form("strategy_form"):
    org_name = st.text_input("Organization Name")
    website_url = st.text_input("Organization Website (URL)")
    mission = st.text_area("What is your mission in one sentence?")
    revenue = st.selectbox("Annual Revenue", ["< $100k", "$100k - $500k", "$500k - $1M", "$1M - $5M", ">$5M"])
    donation_mix = st.text_input("% of revenue from individual donors vs grants vs events")
    marketing_budget = st.selectbox("Annual Marketing Budget", ["< $10k", "$10k - $50k", "$50k - $100k", ">$100k"])
    channels_used = st.multiselect(
        "Active Marketing Channels",
        ["Google Ad Grant", "Google Paid Ads", "Meta Ads", "Email", "SEO", "Events", "Organic Social", "Direct Mail"]
    )
    ad_grant_spend = st.text_input("How much of your $10K Google Ad Grant do you currently spend per month (if applicable)?")
    email_list_size = st.text_input("Email List Size & Avg Open Rate (if known)")
    crm = st.text_input("CRM / Email Tool Used")
    team_size = st.slider("Marketing Team Size", 1, 20, 3)
    marketing_tools = st.text_input("Other Marketing Tech Stack (e.g., CMS, analytics, automation tools)")
    audience_segments = st.text_area("Top 1–2 Donor Personas / Audience Segments")
    goals = st.text_area("Top 1–2 Marketing Goals for Next 6–12 Months")
    challenges = st.text_area("Biggest Bottlenecks or Challenges in Your Marketing")
    past_fails = st.text_area("What's one marketing effort that didn’t work recently — and why?")
    donor_journey = st.selectbox("Do you have a mapped donor journey?", ["Yes", "Somewhat", "No"])
    paid_ads_results = st.text_area("Have you run paid ads before? Share results if known.")
    donation_platform = st.text_input("What donation platform or form are you using (e.g., PayPal, Classy, Givebutter, etc.)?")
    homepage_copy = st.text_area("Paste homepage and/or donation page copy (optional)", height=250)

    submitted = st.form_submit_button("Generate Strategy")

# Call GPT-4 with detailed prompt
if submitted:
    with st.spinner("Generating your strategy..."):

        prompt = f'''
You are a nonprofit marketing strategist, channel optimization expert, and growth advisor.

First, research this organization using ONLY the following fields:
- Organization Name: {org_name}
- Website: {website_url}
- Homepage Copy: {homepage_copy}

Simulate a web search and IRS lookup using this info. Use your training data and inference to make realistic assumptions.

---
🔎 Organizational Research Summary
- Who is this organization?
- What do they do?
- What is their likely size and audience?
- How are they likely raising money now?
- Any major programs or fundraising campaigns you can infer?

---

Then, based on their answers and your simulated research, provide a strategic marketing analysis:

🔍 Strategic Summary
- What is the single biggest missed opportunity?
- Frame the challenge: “They are doing X, but they’re missing Y. If they do Z...”

📊 Channel Scorecard
- For each marketing channel (Email, Ad Grant, Meta, etc.):
    - Is it used well, underused, or not used?
    - Give specific guidance to improve ROI or test appropriately

🚀 90-Day Strategic Action Plan
- List 4–6 high-impact initiatives with tactical recommendations
- Include platform-level fixes (e.g., build X more Ad Grant campaigns, test Meta retargeting)

📈 6–12 Month Vision
- Map a full-funnel nonprofit growth journey from awareness to recurring giving
- Include digital infrastructure suggestions (donor journey, CRM, automations)

🧪 Donation Platform Feedback
- Analyze the platform mentioned
- If PayPal or GoFundMe, call out friction and lost trust/data
- Recommend Classy, Givebutter, RaiseDonors — and justify why
- Show how platform choice affects recurring giving, branding, and long-term value

💡 Google Ad Grant Breakdown
- If spending <$10K/mo, give detailed steps to increase spend:
  - Expand keywords, create new campaigns/ad groups
  - Build dedicated landing pages, improve CTR, add value-focused calls-to-action
  - Comply with structure (2 ads/ad group, 2 ad groups/campaign) and use extensions

🧠 Big-Picture Insight
- What is this org doing that’s holding them back strategically?
- If you were CMO, what would you change first?

❓ Follow-Up Questions
- Ask 4–6 smart questions to deepen your strategic direction

---
Org Name: {org_name}
Mission: {mission}
Revenue: {revenue}
Donation Mix: {donation_mix}
Marketing Budget: {marketing_budget}
Channels: {', '.join(channels_used)}
Ad Grant Spend: {ad_grant_spend}
Email List: {email_list_size}
CRM: {crm}
Team Size: {team_size}
Tools: {marketing_tools}
Audience Segments: {audience_segments}
Goals: {goals}
Challenges: {challenges}
Failed Effort: {past_fails}
Donor Journey Mapped: {donor_journey}
Paid Ads Results: {paid_ads_results}
Donation Platform: {donation_platform}
Homepage Copy: {homepage_copy[:1000] if homepage_copy else "Not provided"}
Website: {website_url}
'''

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nonprofit marketing strategist."},
                {"role": "user", "content": prompt}
            ]
        )

        st.session_state.strategy_output = response.choices[0].message.content

# Display the result
if st.session_state.strategy_output:
    st.subheader("🎯 Your Custom Strategy")
    st.markdown(st.session_state.strategy_output)
    st.download_button("Download Strategy", st.session_state.strategy_output, file_name="nonprofit_strategy.txt")
