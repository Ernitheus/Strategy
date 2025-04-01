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

        prompt = f'''
        You are a senior nonprofit marketing strategist and growth advisor. 

        You’ve been hired to analyze a nonprofit’s marketing performance and craft a personalized growth strategy based on the following inputs from their sales team.

        Your response must include:

        🔍 Strategic Summary
        - Bold TL;DR: What’s the one major opportunity or risk this org must address?
        - State the tension clearly: “X is happening... but they could achieve Y if they do Z.”
        - Prioritize the #1 most important action.

        💡 Key Insights
        - Highlight gaps or underleveraged assets (e.g. large email list, unused donor journey, inefficient ads).
        - Be confident and blunt — don’t restate obvious things.
        - Call out risks and opportunity costs (“If they don’t fix this, they’ll keep losing X.”)

        🚀 90-Day Marketing Plan
        - Focus on speed and ROI.
        - Prioritize 3–5 specific initiatives. Include tactics, channels, and goals.
        - Write like you’re briefing their head of marketing.

        🌱 6–12 Month Growth Roadmap
        - Paint the vision: Where are they headed? What maturity stages will they reach?
        - Include milestones and pivots. Call out dependencies or constraints.

        🧪 Homepage / Donation Page Feedback (if provided)
        - Review their pasted homepage + donation copy. Analyze clarity, emotional resonance, and conversion flow.
        - Suggest 2–3 CRO or storytelling upgrades.

        ❓ Follow-Up Questions for Client Discovery
        - Ask 4–5 sharp questions to clarify what’s missing, vague, or misaligned.
        - Your goal is to deepen strategic understanding.

        Input Data:

        Organization Name: {org_name}
        Revenue: {revenue}
        Budget: {marketing_budget}
        Channels: {', '.join(channels_used)}
        Email List Size: {email_list_size}
        CRM: {crm}
        Team Size: {team_size}
        Goals: {main_goals}
        Challenges: {current_challenges}
        Donor Journey: {donor_journey}
        Audience Segments: {audience_segments}
        Worked with Agency: {past_agency}
        Ad Performance: {ads_performance}
        Best Campaign: {campaign_highlight}
        Internal Tools: {internal_tools}
        Homepage + Donation Copy: {homepage_copy}
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
