import streamlit as st
import openai

# Set up OpenAI key (for local dev; don't hardcode in production)
openai.api_key = st.secrets["openai_api_key"]

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

    submitted = st.form_submit_button("Generate Strategy")

if submitted:
    with st.spinner("Generating your strategy..."):
        prompt = f"""
        Act as a nonprofit marketing strategist.
        Based on the following inputs, create a 3-part strategy:
        1. Key insights (pain points and opportunities)
        2. Recommended short-term actions (90-day plan)
        3. Long-term vision (6-12 month marketing roadmap)

        Org Name: {org_name}
        Revenue: {revenue}
        Budget: {marketing_budget}
        Channels: {', '.join(channels_used)}
        Email List Size: {email_list_size}
        CRM: {crm}
        Team Size: {team_size}
        Main Goals: {main_goals}
        Challenges: {current_challenges}
        Donor Journey Mapped: {donor_journey}
        Audience Segments: {audience_segments}
        Past Agency Work: {past_agency}
        Past Ad Performance: {ads_performance}
        Campaign Highlight: {campaign_highlight}
        Internal Tools: {internal_tools}
        """

        response = openai.ChatCompletion.create(
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
