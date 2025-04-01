import streamlit as st
from openai import OpenAI

# Set up OpenAI client using your secret key
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Nonprofit Marketing Strategy Builder", layout="centered")
st.title("🧠 Nonprofit Marketing Strategy Builder")
st.markdown("Answer the questions below to generate a personalized, strategic nonprofit marketing plan.")

# Use a form to group inputs
with st.form("strategy_form"):
    org_name = st.text_input("Organization Name")
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

if submitted:
    with st.spinner("Generating your strategy..."):

        prompt = f'''
        You are a nonprofit marketing strategist, channel optimization expert, and fractional CMO for mission-driven organizations.

        You have deep experience with:
        - Google Ad Grant (structure, limitations, optimization, scaling to full $10K)
        - Donation conversion strategies (UX, platforms, recurring giving, storytelling)
        - Email, Meta Ads, SEO, Direct Mail, and multi-channel donor journeys

        Based on the information below, write a strategic analysis that includes:

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
        - Recommend Classy, Givebutter, RaiseDonors — but justify why
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
        Homepage Copy: {homepage_copy}
        '''

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nonprofit marketing strategist."},
                {"role": "user", "content": prompt}
            ]
        )

        strategy = response.choices[0].message.content
        st.subheader("🎯 Your Custom Strategy")
        st.markdown(strategy)
        st.download_button("Download Strategy", strategy, file_name="nonprofit_strategy.txt")
