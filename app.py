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
        ["Google Ads", "Meta Ads", "Email", "SEO", "Events", "Organic Social", "Direct Mail"]
    )
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
    donation_platform = st.text_input("What donation platform or form are you using?")
    homepage_copy = st.text_area("Paste homepage and/or donation page copy (optional)", height=250)

    submitted = st.form_submit_button("Generate Strategy")

if submitted:
    with st.spinner("Generating your strategy..."):

        prompt = f'''
        You are a senior nonprofit marketing strategist and growth advisor. Your job is to analyze the inputs below and deliver a sharp, confident strategy.

        Your output must include:

        🔍 Strategic Summary
        - Bold TL;DR of the org's biggest risk or opportunity
        - State the tension: “They are doing X, but they could achieve Y if they fix/change Z.”
        - Prioritize their #1 growth lever

        💡 Key Insights
        - Point out underleveraged assets (email list, tools, audiences)
        - Flag any poor practices or platform choices (e.g., PayPal links, missing journey, weak stack)
        - Recommend better tools or fixes with real names (e.g., "Move from PayPal to Classy or Givebutter")

        🚀 90-Day Action Plan
        - Focus on 3–5 specific high-impact marketing actions
        - Write like you're advising their Director of Marketing

        🌱 6–12 Month Growth Roadmap
        - Break into phases or quarters if helpful
        - Build maturity over time — from basic cleanup to high-performance loops

        🧪 Homepage / Donation Page Feedback (if provided)
        - Review clarity, donation experience, storytelling, conversion friction
        - Be brutally honest — recommend layout, tools, and storytelling changes

        ❓ Follow-Up Questions
        - Ask 3–5 clarifying questions that would deepen strategy or uncover blockers

        ---
        Input:

        Org Name: {org_name}
        Mission: {mission}
        Revenue: {revenue}
        Donation Mix: {donation_mix}
        Marketing Budget: {marketing_budget}
        Channels: {', '.join(channels_used)}
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
