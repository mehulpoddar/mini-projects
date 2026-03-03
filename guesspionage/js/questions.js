const QUESTIONS_DATA = [
  {
    id: 1,
    category: "Food & Drink 🍵",
    question: "What percentage of Indian households consume Chai (tea) every single day?",
    answer: 80,
    funFact: "Despite the \"third-wave coffee\" trend in metros, India still runs on tea. We consume roughly 1.1 billion kilograms of it annually.",
    source: "ResearchGate / Tea Board of India"
  },
  {
    id: 2,
    category: "Food & Drink 🍟",
    question: "What percentage of urban Indians eat street food or fast food at least once a week?",
    answer: 22,
    funFact: "Panipuri remains the undisputed champion of street food preferences across almost every demographic.",
    source: "ResearchGate (Varanasi Survey 2025)"
  },
  {
    id: 3,
    category: "Digital India 💸",
    question: "What percentage of monthly Indian household spending is now done via UPI?",
    answer: 58,
    funFact: "UPI processed over 18 billion transactions in a single month in 2025. Even your local sabzi-wala is probably more digital than most banks in Europe.",
    source: "IIM Bangalore / NPCI (2025)"
  },
  {
    id: 4,
    category: "Digital India 📱",
    question: "What percentage of Indian WhatsApp users say they receive spam or commercial messages every day?",
    answer: 96,
    funFact: "India is WhatsApp's largest market, but it's also the global capital of \"Good Morning\" messages and \"Hi, are you looking for a job?\" scams.",
    source: "LocalCircles (Feb 2026)"
  },
  {
    id: 5,
    category: "Entertainment 🎬",
    question: "What percentage of the Indian population uses OTT platforms (Netflix, Hotstar, Prime) to watch content?",
    answer: 41,
    funFact: "Nearly half of all streaming in India is now in regional languages, not just Hindi or English.",
    source: "Ormax Media (The OTT Audience Report: 2025)"
  },
  {
    id: 6,
    category: "Society & Lifestyle 💍",
    question: "What percentage of marriages in India are still Arranged Marriages?",
    answer: 90,
    funFact: "Even with the rise of dating apps, the \"Family Approved\" seal of approval remains the dominant way Indians tie the knot.",
    source: "Pew Research / WifiTalents (2026 Reports)"
  },
  {
    id: 7,
    category: "Society & Lifestyle 🏠",
    question: "What percentage of young urban Indians (ages 22–29) live with their parents?",
    answer: 82,
    funFact: "In the West, this is called \"Boomerang Kids\" or \"Failure to Launch.\" In India, it's basically a lifetime subscription to Mummy ke haath ka khana (Mom's cooking) and zero-interest laundry services.",
    source: "CBRE Group / Mint"
  },
  {
    id: 8,
    category: "Digital India 💳",
    question: "What percentage of the Indian population possesses a formal credit card?",
    answer: 5,
    funFact: "While India is a global leader in digital payments (UPI), we are still very \"credit-shy.\" Most Indians prefer \"Buy Now, Pay Now\" via UPI rather than \"Buy Now, Pay Later\" via a credit card. In fact, for every 1 credit card in India, there are roughly 8 to 10 debit cards in circulation!",
    source: "PwC India (Decoding India's Credit Card Market) & RBI Data (2024-2025)"
  },
  {
    id: 9,
    category: "Faith & Culture ✨",
    question: "What percentage of urban Indians say they believe in God or a higher power?",
    answer: 81,
    funFact: "Interestingly, about 43% of urban Indians also believe in the existence of supernatural spirits (ghosts, fairies, or demons).",
    source: "Ipsos Global Advisor (2023/2024)"
  },
  {
    id: 10,
    category: "Household & Assets 🏡",
    question: "What percentage of Indian households own a refrigerator?",
    answer: 48,
    funFact: "While only half the country owns a fridge, 2024 and 2025 saw record-breaking sales due to extreme heatwaves. In many households, the fridge isn't just for food; it's a \"safe house\" for expensive medicines and, occasionally, the TV remote to keep it cool!",
    source: "Data For India (2024) / HCES"
  },
  {
    id: 11,
    category: "Travel & Identity 🛂",
    question: "What percentage of the Indian population currently possesses a valid passport?",
    answer: 6.5,
    funFact: "As of February 2026, the Indian passport has jumped to 75th place in global rankings, now offering visa-free or visa-on-arrival access to 56 destinations. We're traveling more, but clearly, most of us are still \"exploring\" through Instagram Reels.",
    source: "Ministry of External Affairs (Dec 2023)"
  },
  {
    id: 12,
    category: "Household & Assets 🚗",
    question: "What percentage of Indian households own a car?",
    answer: 8,
    funFact: "Despite the low percentage, India is the 3rd largest auto market in the world. Interestingly, the trend has shifted massively from small \"budget\" hatchbacks to SUVs—because if you're going to be stuck in Bengaluru traffic, you might as well do it with high ground clearance.",
    source: "NFHS-5 (National Family Health Survey)"
  },
  {
    id: 13,
    category: "Digital India 📺",
    question: "What percentage of the total Indian population are active YouTube users?",
    answer: 34,
    funFact: "India has the largest YouTube audience in the world. If \"YouTube University\" were a real college, it would be the most populated educational institution in history, with \"How to fix a leaky tap\" and \"Paneer Butter Masala recipe\" as the most popular majors.",
    source: "Couponsly / Statista (2025)"
  },
  {
    id: 14,
    category: "Digital India 📱",
    question: "What percentage of Indian internet users regularly consume short-form videos (like Instagram Reels or YouTube Shorts)?",
    answer: 61,
    funFact: "India is the world's largest consumer of short-form content. The average Indian user spends nearly 30 to 45 minutes a day just scrolling through these \"snackable\" videos. Interestingly, rural India is catching up fast, with short-video consumption growing even quicker in villages than in big cities.",
    source: "IAMAI & Kantar – Internet in India Report 2025"
  },
  {
    id: 15,
    category: "Travel & Identity ✈️",
    question: "According to industry estimates, what percentage of Indians have never flown in an airplane?",
    answer: 90,
    funFact: "While 90% haven't flown, Indian airlines have the largest \"order books\" in history, adding nearly 100 new planes a year. The \"First Flight\" experience is such a milestone in India that it's often celebrated with as much fanfare as a graduation.",
    source: "Director Sid Anand / Smithsonian global estimates"
  },
  {
    id: 16,
    category: "Entertainment 🎥",
    question: "What percentage of urban Indians go to a movie theater at least once a month?",
    answer: 24,
    funFact: "2025 was the biggest year in Indian Box Office history, crossing ₹13,500 crore. Even with OTT platforms everywhere, nothing beats the \"collective gasp\" of a theater audience when the hero makes a slow-motion entry.",
    source: "YouGov (Sept 2023)"
  },
  {
    id: 17,
    category: "Food & Drink 🥦",
    question: "What percentage of the Indian population follows a strictly vegetarian diet?",
    answer: 31,
    funFact: "There is a massive \"gender gap\" in Indian diets—surveys show that Indian men are significantly more likely to eat meat than Indian women, often because men have more opportunities to eat out \"anonymously.\"",
    source: "World Animal Foundation (2026)"
  },
  {
    id: 18,
    category: "Digital India 📰",
    question: "What percentage of Indians rely on social media (WhatsApp, YouTube, FB) as their primary source for news?",
    answer: 49,
    funFact: "Despite the \"Spam Capital\" reputation of WhatsApp, it remains the #1 source for news. In fact, many Indians trust a forwarded message from a \"Family Group\" more than a verified news anchor in a suit.",
    source: "ResearchGate (Jan 2026)"
  }
];
