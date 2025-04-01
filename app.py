import streamlit as st
from openai import OpenAI

# Set up OpenAI client using your secret key
client = OpenAI(api_key=st.secrets["openai_api_key"])

st.set_page_config(page_title="Nonprofit Marketing Strategy Builder", layout="centered")
st.title("🧠 Nonprofit Marketing Strategy Builder")
st.markdown("Answer the 15 questions below to generate a personalized marketing strategy for your nonprofit client.")

# Use a form to group inputs
with st.form("strategy_form"):
    org_name = st.text_input("Organization Name")
    revenue = st.selectbox("Annual Revenue", ["< $100k", "$100k - $500k", "$500k - $1M", "$1M - $5M", ">$5M"])
    marketing_budget = st.selectbox("Marketing Budget", ["< $10k", "$10k - $50k", "$50k - $100k", ">$100k"])
    channels_used = st.multiselect(
        "Which channels are you using?",
        ["Google Ads", "Meta Ads", "Email", "Organic Social", "SEO", "Events", "Direct Mail"]
    )
    email_list_size = st.text_input("Email List Size")
    crm = st.text_input("CRM Tool Used")
    team_size = st.slider("How many people are on the marketing team?", 1, 20, 3)
    main_goals = st.text_area("Main goals over the next 12 months")
    current_challenges = st.text_area("Biggest marketing challenges?")
    donor_journey = st.selectbox("Do you have a clear donor journey mapped?", ["Yes", "Somewhat", "No"])
    audience_segments = st.text_area("Describe your key audience segments")
    past_agency = st.selectbox("Worked with agencies before?", ["Yes", "No"])
    ads_performance = st.text_area("Any past ad performance results?")
    campaign_highlight = st.text_area("Biggest campaign success so far")
    internal_tools = st.text_area("Other marketing tools in use (if any)")
    homepage_copy = st.text_area("Paste homepage and donation page copy (optional)", height=250)

    submitted = st.form_submit_button("Generate Strategy")

if submitted:
    with st.spinner("Generating your strategy..."):

        # Improved prompt
        prompt = f"""
        You are a senior nonprofit marketing strategist.

        The goal is to analyze the following client’s data and return a powerful, actionable strategy. Your answer should include:

        1. 🔍 Strategic Summary (2–3 sentence TL;DR that calls out the big insight)
        2. 💡 Key Insights (pain points, gaps, and untapped opportunities)
        3. 🚀 90-Day Action Plan (specific things they should start doing now)
        4. 🌱 Long-Term Roadmap (6–12 month growth strategy with milestones)
        5. ❓ Follow-Up Questions (ask 3–5 clarifying questions to deepen understanding)

        Make the strategy bold, specific, and visionary. Avoid generic advice. Speak like a senior consultant who’s done this 100x. Use confident language, cite frameworks or patterns when helpful, and aim for “aha” moments that would impress a savvy CMO.

        Here is the input from the sales rep:

        Organization Name: {org_name}
        Annual Revenue: {revenue}
        Marketing Budget: {marketing_budget}
        Marketing Channels Used: {', '.join(channels_used)}
        Email List Size: {email_list_size}
        CRM Used: {crm}
        Marketing Team Size: {team_size}
        Main Goals: {main_goals}
        Biggest Challenges: {current_challenges}
        Donor Journey Mapped?: {donor_journey}
        Audience Segments: {audience_segments}
        Worked with Agencies?: {past_agency}
        Ad Performance History: {ads_performance}
        Best Campaign Ever: {campaign_highlight}
        Internal Tools Used: {internal_tools}
        Homepage and Donation Page Copy: {homepage_copy}
        """

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
