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
        You are a senior nonprofit marketing strategist with deep expertise in channels like Google Ad Grants, digital fundraising, and donor journey optimization. You’re analyzing a nonprofit's setup based on discovery inputs from a strategist or sales rep. 

        You must:
        - Be confident and bold in your advice
        - Challenge poor practices (e.g., PayPal-only donation pages)
        - Provide better platform/tool recommendations
        - Think like a CMO who has helped 100+ nonprofits grow

        Include the following:

        🔍 Strategic Summary
        - Call out the core growth opportunity or risk
        - Frame it in tension: “They are doing X but missing Y. If they do Z...”
        - Prioritize the ONE lever with highest upside

        💡 Key Insights
        - What are they underutilizing?
        - Where are they inefficient or outdated?
        - Be blunt about problems (like poor UX, generic campaigns, PayPal redirects, weak messaging, poor Ad Grant usage)

        🚀 90-Day Marketing Plan
        - What 3–5 things should they implement now?
        - Focus on speed, lift, and ROI

        🌱 6–12 Month Growth Roadmap
        - Milestone-based path from cleanup to scaling
        - Show how to compound impact across channels

        📊 Google Ad Grant Deep Dive (if applicable)
        - Are they underutilizing their $10K/mo? How?
        - Suggest landing pages, high-intent keywords, content buckets, funnel improvements
        - Mention 5% CTR requirement, ad structure, and conversion goals

        🧪 Donation Page Critique
        - If using PayPal, GoFundMe, or other weak UX: flag it and recommend Classy, Givebutter, RaiseDonors, etc.
        - Suggest frictionless forms, storytelling, recurring options, branding

        ❓ Follow-Up Discovery Questions
        - What else would you ask to unlock deeper strategy?

        ---
        Input:

        Org Name: {org_name}
        Mission: {mission}
        Revenue: {revenue}
        Donation Mix: {donation_mix}
        Marketing Budget: {marketing_budget}
        Channels: {', '.join(channels_used)}
        Google Ad Grant Spend: {ad_grant_spend}
        Email List: {email_list_size}
        CRM: {crm}
        Team Size: {team_size}
        Tech Stack: {marketing_tools}
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
