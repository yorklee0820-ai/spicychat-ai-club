"""Build the static SpicyChat AI Club guide from sourced editorial content."""

import html
import json
import os
import shutil
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).parent
SITE = "https://spicychat-ai.club"
GOOGLE_VERIFICATION = "AeKEHH6iEmkBP6dM4qb5Utq2Jvvng24tKWWkh2YenZo"
GA4_ID = "G-9EQR9R0YQF"
GOOGLE_TAG = f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA4_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', '{GA4_ID}');
  </script>'''
OFFICIAL = "https://spicychat.ai/"
PLAYBOX = "https://www.playbox.com/?ref=eushing"
DESTINATION = os.environ.get("SPICYCHAT_DESTINATION", PLAYBOX)
parsed = urlparse(DESTINATION)
if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
    raise ValueError("SPICYCHAT_DESTINATION must be a full HTTPS URL")
SPONSORED = DESTINATION != OFFICIAL
PLAYBOX_DESTINATION = parsed.hostname in {"playbox.com", "www.playbox.com"}
PROMO_NOTICE = ("Promotional buttons open Playbox, a separate service, through an affiliate link."
                if PLAYBOX_DESTINATION else "Promotional buttons open the destination named on each button.")

SOURCES = {
    "home": ("Official SpicyChat website", "https://spicychat.ai/pages"),
    "plans": ("Official plan feature matrix", "https://support.spicychat.ai/support/solutions/articles/153000260533-plans-and-what-s-included"),
    "premium": ("Official premium feature guide", "https://docs.spicychat.ai/product-guides/premium-features"),
    "memory": ("Official tokens and context guide", "https://docs.spicychat.ai/advanced/tokens-and-context"),
    "manager": ("Official Memory Manager guide", "https://docs.spicychat.ai/product-guides/premium-features/memory-manager"),
    "models": ("Official AI model guide", "https://docs.spicychat.ai/product-guides/premium-features/ai-models"),
    "age": ("Official age verification guidance", "https://support.spicychat.ai/support/solutions/articles/153000260514-why-spicychat-asks-you-to-verify-your-age"),
    "age_steps": ("Official age verification steps", "https://support.spicychat.ai/support/solutions/articles/153000260516-how-to-verify-your-age"),
    "support": ("Official support center", "https://support.spicychat.ai/support/home"),
    "affiliate": ("Official affiliate program", "https://promote.spicychat.ai/"),
}


def source(key):
    label, url = SOURCES[key]
    return f'<a href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">{html.escape(label)}</a>'


def cta(label="Explore SpicyChat AI", extra=""):
    rel = "sponsored nofollow noopener noreferrer" if SPONSORED else "noopener noreferrer"
    if PLAYBOX_DESTINATION:
        label = "Explore Playbox (partner link)"
    return f'<a class="btn btn-primary" href="{html.escape(DESTINATION, quote=True)}" target="_blank" rel="{rel}">{html.escape(label)}</a>{extra}'


def box(title, body):
    return f'<div class="callout"><b>{title}</b> {body}</div>'


def table(headers, rows):
    head = "".join(f"<th scope=\"col\">{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="table-scroll"><table class="compare"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def links(items):
    return '<div class="grid">' + "".join(
        f'<a class="card link-card" href="{slug}.html"><div class="body"><h3>{title} →</h3><p>{description}</p></div></a>'
        for slug, title, description in items
    ) + '</div>'


PAGES = [
    ("index", "SpicyChat AI Guide: Features, Pricing & Safety | SpicyChat AI Club", "Independent guide to SpicyChat AI features, plans, memory, models and safety. Compare the official documentation before you subscribe.", "SpicyChat AI: a clear guide to the platform", "assets/img/hero-home.jpg"),
    ("review", "SpicyChat AI Review: Features and Trade-offs | SpicyChat AI Club", "An independent feature review of SpicyChat AI based on official documentation, with strengths, limits and buying advice.", "SpicyChat AI review: strengths and trade-offs", "assets/img/scene-group.jpg"),
    ("pricing", "SpicyChat AI Pricing and Plan Features | SpicyChat AI Club", "Compare the free, Get A Taste, True Supporter and I'm All In plans. Check current prices at the official checkout.", "SpicyChat AI pricing and plans", "assets/img/scene-models.jpg"),
    ("free-vs-paid", "SpicyChat AI Free vs Paid: Feature Comparison | SpicyChat AI Club", "See which SpicyChat features are available on the free tier and what each paid plan adds.", "Free vs paid: what actually changes", "assets/img/scene-group.jpg"),
    ("characters", "SpicyChat AI Characters and Creation Guide | SpicyChat AI Club", "Learn how the SpicyChat character library works and how to choose or create a character.", "Characters and the community library", "assets/img/cat-anime.jpg"),
    ("models", "SpicyChat AI Models: Availability and Choice | SpicyChat AI Club", "Understand model selection and plan access using SpicyChat's official AI model documentation.", "SpicyChat AI models explained", "assets/img/scene-models.jpg"),
    ("memory", "SpicyChat AI Memory and Context Explained | SpicyChat AI Club", "Compare the 4K, 8K and 16K context tiers, Memory Manager and Semantic Memory 2.0.", "Memory, context and long chats", "assets/img/scene-memory.jpg"),
    ("alternatives", "SpicyChat AI Alternatives: How to Compare | SpicyChat AI Club", "A practical comparison framework for choosing an AI roleplay service without invented scores or outdated prices.", "Alternatives: choose by your priorities", "assets/img/cat-fantasy.jpg"),
    ("is-it-safe", "Is SpicyChat AI Safe? Age and Privacy Basics | SpicyChat AI Club", "Read the official age verification guidance and practical privacy steps before using SpicyChat AI.", "Safety, age checks and privacy", "assets/img/cat-horror.jpg"),
    ("how-it-works", "How SpicyChat AI Works: Getting Started | SpicyChat AI Club", "A straightforward guide to opening the official site, choosing a character and understanding plan limits.", "How to get started", "assets/img/cat-romance.jpg"),
    ("18-plus", "18+ Notice | SpicyChat AI Club", "This independent editorial site discusses an adults-only AI roleplay service.", "18+ notice", "assets/img/cat-slice.jpg"),
    ("sources", "Sources and Editorial Method | SpicyChat AI Club", "Official sources and editorial standards for SpicyChat AI Club.", "Sources and editorial method", "assets/img/scene-memory.jpg"),
    ("contact", "Contact and Corrections | SpicyChat AI Club", "How to submit a correction or report a broken link to SpicyChat AI Club.", "Contact and corrections", "assets/img/cat-slice.jpg"),
    ("sitemap", "Sitemap | SpicyChat AI Club", "Browse all SpicyChat AI Club guides and information pages.", "Sitemap", "assets/img/hero-home.jpg"),
]

NAV = [("review", "Review"), ("pricing", "Pricing"), ("characters", "Characters"), ("models", "Models"), ("memory", "Memory"), ("is-it-safe", "Safety")]


def page(slug, title, description, heading, image, body):
    url = SITE + ("/" if slug == "index" else f"/{slug}.html")
    nav = "".join(f'<a href="{name}.html"{" aria-current=\"page\"" if slug == name else ""}>{label}</a>' for name, label in NAV)
    schema = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "SpicyChat AI Club", "url": SITE + "/", "description": "Independent guide to SpicyChat AI"}, ensure_ascii=False)
    footer_links = links([("sources", "Sources", "Where the facts come from"), ("18-plus", "18+ notice", "Adults only"), ("contact", "Corrections", "Report an error")])
    disclosure = ("Promotional buttons open Playbox, a separate service, through an affiliate link. We may earn a commission."
                  if PLAYBOX_DESTINATION else "Some outbound links may earn a commission." if SPONSORED
                  else "Outbound buttons currently lead to the official SpicyChat website.")
    hero_action = f'<div class="cta-row hero-action">{cta("Explore SpicyChat AI", "<a class=\"btn btn-ghost\" href=\"pricing.html\">Compare plans</a>")}</div>' if slug == "index" else ""
    hero_disclosure = '<p class="promo-note">Playbox is a separate service. This partner link may earn us a commission.</p>' if slug == "index" and PLAYBOX_DESTINATION else ""
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="rating" content="adult">
  <meta name="google-site-verification" content="{GOOGLE_VERIFICATION}">
  <meta name="theme-color" content="#0b0714">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{html.escape(title, quote=True)}">
  <meta property="og:description" content="{html.escape(description, quote=True)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/{image}">
  <meta name="twitter:card" content="summary_large_image">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="style.css">
  {GOOGLE_TAG}
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site"><div class="bar"><a class="logo" href="index.html" aria-label="SpicyChat AI Club home">SpicyChat<span>AI</span> Club</a><nav class="main" aria-label="Main navigation">{nav}</nav></div></header>
  <main id="main">
    <div class="hero-sub"><img class="hero-img" src="{image}" alt="Illustrated AI roleplay scene" fetchpriority="high"><div class="wrap"><div class="eyebrow">Independent guide · Adults 18+</div><h1>{heading}</h1><p class="sub">Independent information about SpicyChat AI. This website does not provide chats or accounts.</p>{hero_action}{hero_disclosure}</div></div>
    {body}
  </main>
  <footer class="site"><div class="wrap"><div class="fgrid"><div class="fcol"><h4>Explore</h4><a href="index.html">Home</a><a href="review.html">Review</a><a href="pricing.html">Pricing</a><a href="free-vs-paid.html">Free vs paid</a></div><div class="fcol"><h4>Guides</h4><a href="characters.html">Characters</a><a href="models.html">Models</a><a href="memory.html">Memory</a><a href="alternatives.html">Alternatives</a></div><div class="fcol"><h4>About</h4><a href="sources.html">Sources</a><a href="is-it-safe.html">Safety</a><a href="18-plus.html">18+ notice</a><a href="contact.html">Corrections</a><a href="sitemap.html">Sitemap</a></div></div><div class="legal"><span class="badge18">18+</span> SpicyChat AI Club is an independent editorial guide. It is not operated, endorsed or affiliated with SpicyChat AI. {disclosure} Product details checked against linked official sources on 28 September 2026; confirm current terms with the provider.</div></div></footer>
</body>
</html>
'''


CONTENT = {}
CONTENT["index"] = f'''<section><div class="wrap"><div class="tldr"><h2>At a glance</h2><p>SpicyChat AI is an adults-only, community-driven AI roleplay service with a free tier and three paid tiers. The main differences between plans are context memory, response length, models and media features. This guide summarizes documented features; it does not claim independent product testing.</p><div class="cta-row">{cta("Explore SpicyChat AI", '<a class="btn btn-ghost" href="pricing.html">Compare the plans</a>')}</div></div></div></section>
<section class="alt"><div class="wrap"><div class="kicker">Start here</div><h2>What is SpicyChat AI?</h2><p class="lede">SpicyChat hosts community-created AI characters for text roleplay. Its official site advertises a library of more than 200,000 chatbots and a free starting option. Character quality varies because creators publish their own bots. {source("home")}</p>{links([("how-it-works", "How it works", "First steps and what to expect"), ("characters", "Characters", "Browse and choose a roleplay character"), ("review", "Feature review", "Strengths and limits from the documented feature set")])}</div></section>
<section><div class="wrap"><div class="kicker">Plans</div><h2>What changes when you pay?</h2>{table(["Plan", "Documented changes"], [["Free", "4,096 context tokens, 180-token reply ceiling, 3 personas"], ["Get A Taste", "No ads, Memory Manager, 10 personas; same context and reply ceiling as free"], ["True Supporter", "8,192 context tokens, 300-token reply ceiling, Semantic Memory 2.0, conversation images and advanced models"], ["I'm All In", "16,384 context tokens, text-to-speech, priority generation and all models including SpicyXL"]])}<p class="src">Feature source: {source("plans")}. Prices vary; check the official subscription screen before paying.</p><div class="cta-row">{cta("View SpicyChat", '<a class="btn btn-ghost" href="free-vs-paid.html">Full comparison</a>')}</div></div></section>
<section class="alt"><div class="wrap"><div class="kicker">Deep dives</div><h2>Questions worth answering before you subscribe</h2>{links([("memory", "Memory", "Why context length is not a guarantee of perfect recall"), ("models", "Models", "What you can choose at each plan level"), ("is-it-safe", "Safety and age checks", "Privacy basics and regional verification")])}</div></section>
<section><div class="wrap narrow"><h2>Frequently asked questions</h2><details class="faq"><summary>Is SpicyChat free?</summary><div class="a">Yes. The official plan matrix lists a free tier with 4,096 context tokens, a 180-token reply ceiling and three personas. Some features require a subscription. {source("plans")}</div></details><details class="faq"><summary>Does a larger context window guarantee better memory?</summary><div class="a">No. Context is the maximum amount of text the model can use for a response, shared across chat history and other inputs. Older messages may fall out as a conversation grows. {source("memory")}</div></details><details class="faq"><summary>Where do I see the current price?</summary><div class="a">Open the official SpicyChat subscription page from your account. This guide compares features and avoids displaying a price that may become stale.</div></details><details class="faq"><summary>Is this the official SpicyChat website?</summary><div class="a">No. This is an independent guide. {PROMO_NOTICE} To visit SpicyChat, use <a href="https://spicychat.ai/">its official website</a>.</div></details></div></section>'''

CONTENT["review"] = f'''<section><div class="wrap narrow"><p class="lede">This is a documented feature review. We have not run controlled chat, memory or model benchmarks, so there are no numerical scores or claims of hands-on testing.</p><h2>Where it stands out</h2><ul><li>A public community character library and character creation on the free tier. {source("home")}</li><li>A meaningful feature ladder: Memory Manager at Get A Taste, larger context and images at True Supporter, and all models with voice on I'm All In. {source("plans")}</li><li>Multiple models let subscribers choose a different writing style. Access depends on the model and plan. {source("models")}</li></ul><h2>Trade-offs to consider</h2><ul><li>Free and Get A Taste have the same 4,096-token context and 180-token reply ceiling. {source("plans")}</li><li>A context window is a limit, not a promise that every older detail will be remembered. {source("memory")}</li><li>The service is for adults, and some locations require age verification to access NSFW content. {source("age")}</li></ul>{box("Our view:", "Start on the free tier to judge the character library yourself. Pay only when you know which specific feature you need. Check the current price on SpicyChat before purchasing.")}<div class="cta-row">{cta("Explore the official site", '<a class="btn btn-ghost" href="pricing.html">Compare plan features</a>')}</div></div></section>'''

CONTENT["pricing"] = f'''<section><div class="wrap narrow"><p class="lede">SpicyChat lists four plan levels: Free, Get A Taste, True Supporter and I'm All In. The official help center confirms the features below. We do not display fixed prices because live checkout prices can change by date, billing term or location. {source("plans")}</p>{table(["Plan", "Context", "Reply ceiling", "Distinct additions"], [["Free", "4,096 tokens", "180 tokens", "3 personas"], ["Get A Taste", "4,096 tokens", "180 tokens", "No ads, Memory Manager, 10 personas"], ["True Supporter", "8,192 tokens", "300 tokens", "Semantic Memory 2.0, images, advanced models, 50 personas"], ["I'm All In", "16,384 tokens", "300 tokens", "Priority generation, text-to-speech, all models, 100 personas"]])}<h2>How to choose</h2><p><b>Free:</b> a sensible place to try characters and basic chat. <b>Get A Taste:</b> useful if ads or manually managing memories bother you, but it does not increase context length. <b>True Supporter:</b> the first tier with a larger context window and conversation images. <b>I'm All In:</b> consider it if you need the longest context, voice or a specific premium model.</p>{box("Before subscribing:", "Confirm the live price, renewal terms and payment options in the official checkout. The figures in your account are authoritative for your purchase.")}<div class="cta-row">{cta("Check plans on SpicyChat", '<a class="btn btn-ghost" href="free-vs-paid.html">Feature matrix</a>')}</div></div></section>'''

CONTENT["free-vs-paid"] = f'''<section><div class="wrap"><p class="lede">This comparison follows SpicyChat's official plan matrix. A higher tier includes lower-tier features. {source("plans")}</p>{table(["Feature", "Free", "Get A Taste", "True Supporter", "I'm All In"], [["Context", "4K", "4K", "8K", "16K"], ["Max reply", "180", "180", "300", "300"], ["Personas", "3", "10", "50", "100"], ["Memory Manager", "—", "Yes", "Yes", "Yes"], ["Semantic Memory 2.0", "—", "—", "Yes", "Yes"], ["Conversation images", "—", "—", "Yes", "Yes, including private characters"], ["Advanced models", "—", "—", "Yes", "All, including SpicyXL"], ["Text-to-speech", "—", "—", "—", "Yes"]])}<p>For context and memory, see <a href="memory.html">our memory guide</a>. For current charges, use SpicyChat's official checkout.</p><div class="cta-row">{cta("Try the official site")}</div></div></section>'''

CONTENT["characters"] = f'''<section><div class="wrap"><p class="lede">SpicyChat's official site describes a library of more than 200,000 community chatbots. That is the provider's published figure, not an independently audited count. {source("home")}</p><div class="grid"><div class="card"><img src="assets/img/cat-anime.jpg" alt="Illustrated anime character" loading="lazy"><div class="body"><h3>Anime</h3><p>Character-led stories and stylized personas.</p></div></div><div class="card"><img src="assets/img/cat-fantasy.jpg" alt="Illustrated fantasy scene" loading="lazy"><div class="body"><h3>Fantasy</h3><p>World building and adventure prompts.</p></div></div><div class="card"><img src="assets/img/cat-romance.jpg" alt="Illustrated romantic scene" loading="lazy"><div class="body"><h3>Romance</h3><p>Relationship-led character conversations.</p></div></div><div class="card"><img src="assets/img/cat-horror.jpg" alt="Illustrated suspense scene" loading="lazy"><div class="body"><h3>Horror</h3><p>Mystery and suspense setups.</p></div></div></div><h2>Choosing a character</h2><p>Read the description and opening message before you start. A detailed setup usually gives you more to respond to than a generic greeting. Try several characters on the free tier before judging the platform as a whole. The official site also advertises character creation. {source("home")}</p><div class="cta-row">{cta("Browse official characters")}</div></div></section>'''

CONTENT["models"] = f'''<section><div class="wrap narrow"><p class="lede">SpicyChat documents multiple models. The available choices depend on your plan and can change as models are updated. Use the in-app model selector for the current list. {source("models")}</p><h2>How model selection works</h2><p>In a chat, open the menu, choose Generation Settings, then Inference Model and Change Model. The official model guide describes each model's strengths and tier availability. {source("models")}</p>{table(["Example model", "What the official guide says"], [["SpicyChat Default", "Available to all users; designed for a broad range of roleplay styles"], ["TheSpice", "Available to all users; tends toward shorter responses"], ["Stheno", "Available with a paid plan; described as a versatile storytelling model"], ["Lyra 12B V4", "Available on True Supporter and I'm All In; designed for longer and multilingual stories"], ["SpicyXL", "Included with I'm All In according to the plan matrix"]])}<p class="src">Sources: {source("models")} and {source("plans")}.</p>{box("Practical tip:", "Try the same character with more than one available model. Differences in tone are subjective, so your own test is more useful than an unsourced ranking.")}<div class="cta-row">{cta("Explore official models")}</div></div></section>'''

CONTENT["memory"] = f'''<section><div class="wrap narrow"><p class="lede">Context memory describes how much text the model can use for one reply. The official plan matrix lists 4,096 tokens for Free and Get A Taste, 8,192 for True Supporter, and 16,384 for I'm All In. {source("plans")}</p><h2>Why characters can forget details</h2><p>The context window is shared by chat history and other material. As a conversation grows, older messages may drop out. A larger window can keep more conversation visible, but the exact number of messages depends on their length. SpicyChat's own explanation explicitly says there is no fixed message-count guarantee. {source("memory")}</p><h2>Tools for continuity</h2><p><b>Memory Manager</b> lets eligible subscribers add and edit specific memories. It is available starting at Get A Taste. <b>Semantic Memory 2.0</b> is listed for True Supporter and I'm All In. {source("manager")} {source("plans")}</p>{box("For long stories:", "Keep a short summary of names, locations and plot points. Reintroduce essential details when the story moves to a new scene. Treat memory features as tools, not guarantees.")}<div class="cta-row">{cta("Try SpicyChat", '<a class="btn btn-ghost" href="free-vs-paid.html">Compare memory tiers</a>')}</div></div></section>'''

CONTENT["alternatives"] = f'''<section><div class="wrap narrow"><p class="lede">The right alternative depends on the feature you care about. We have not run side-by-side benchmarks of rival services, so this page provides a decision checklist instead of invented scores or stale competitor prices.</p>{table(["If your priority is…", "What to compare"], [["Character variety", "Size of the public library, search filters and whether creators can publish bots"], ["Long stories", "Context window, manual memory tools and what happens when old messages leave context"], ["Cost", "Live checkout price, renewal term, free-tier limits and payment methods"], ["Privacy", "Current privacy policy, deletion controls and age-verification process"], ["Media", "Whether images, text-to-speech or voice calls are included in the plan you want"]])}<h2>Start with a free session</h2><p>Choose the same type of character and the same short scenario on each service. Compare response style, speed and how easy it is to change settings. For SpicyChat's documented features, see <a href="free-vs-paid.html">free vs paid</a> and <a href="models.html">models</a>.</p><div class="cta-row">{cta("Explore SpicyChat AI")}</div></div></section>'''

CONTENT["is-it-safe"] = f'''<section><div class="wrap narrow"><p class="lede">SpicyChat is an adults-only service. Its official support site says some countries and US states require age verification before NSFW content becomes available. The covered locations can change; check the official guidance for your region. {source("age")}</p><h2>Practical account safety</h2><ul><li>Use the official <a href="https://spicychat.ai/" rel="noopener noreferrer">spicychat.ai</a> domain for sign-in and payment.</li><li>Do not put sensitive personal information into a character conversation.</li><li>Read the provider's current privacy policy and payment terms before sharing data or subscribing.</li><li>If age verification is required, follow the steps in the official support center. {source("age_steps")}</li></ul><p>We do not independently audit SpicyChat's security or make claims about unreported incidents. For product support, use the {source("support")}.</p><div class="cta-row">{cta("Visit the official site")}</div></div></section>'''

CONTENT["how-it-works"] = f'''<section><div class="wrap narrow"><div class="steps"><div class="step"><div class="n">01</div><h2>Open the official site</h2><p>Visit <a href="https://spicychat.ai/">spicychat.ai</a> directly for SpicyChat. {PROMO_NOTICE}</p></div><div class="step"><div class="n">02</div><h2>Choose a character</h2><p>Browse the community library and read a character's description and opening message.</p></div><div class="step"><div class="n">03</div><h2>Try the free tier</h2><p>Use basic chat first. Review the <a href="free-vs-paid.html">feature matrix</a> if you later need memory or media features.</p></div></div><p>Availability of adult content can depend on regional age verification. {source("age")}</p><div class="cta-row">{cta("Explore SpicyChat AI")}</div></div></section>'''

CONTENT["18-plus"] = f'''<section><div class="wrap narrow"><p class="lede">This guide discusses an adult AI roleplay platform and is intended for people aged 18 or older. It does not host AI chats, explicit content or user accounts.</p><p>SpicyChat may require age verification for NSFW access in certain regions. The official requirements are maintained by the provider. {source("age")}</p><p>If you are under 18, do not use this site to access SpicyChat. For product-specific safety questions, see the {source("support")}.</p></div></section>'''

CONTENT["sources"] = f'''<section><div class="wrap narrow"><p class="lede">We checked the product descriptions against first-party sources on 28 September 2026. This is a guide to documented features, not a hands-on product test. Prices and features may change.</p><h2>Primary sources</h2><ul>{''.join(f'<li>{source(key)}</li>' for key in SOURCES)}</ul><h2>Editorial rules</h2><ul><li>We do not publish invented user counts, review scores or test results.</li><li>Plan descriptions are attributed to SpicyChat; they are not independent performance guarantees.</li><li>Current prices should be confirmed in the provider's checkout.</li><li>If a referral URL is added, outbound links are marked as sponsored and disclosed in the footer.</li></ul></div></section>'''

CONTENT["contact"] = f'''<section><div class="wrap narrow"><p class="lede">Found an outdated feature, broken link or incorrect statement? Open a public issue in the site's GitHub repository and include the page URL plus a supporting source.</p><p><a class="btn btn-primary" href="https://github.com/yorklee0820-ai/spicychat-ai-club/issues/new" target="_blank" rel="noopener noreferrer">Submit a correction on GitHub</a></p><p>Issues are public. Do not include passwords, payment details or other private information. For account and billing support, contact the {source("support")} directly.</p></div></section>'''

CONTENT["sitemap"] = '<section><div class="wrap narrow"><p class="lede">All pages on this guide.</p><ul>' + ''.join(f'<li><a href="{slug}.html">{heading}</a></li>' for slug, _, _, heading, _ in PAGES if slug not in ("index", "sitemap")) + '</ul></div></section>'


for slug, title, description, heading, image in PAGES:
    (ROOT / f"{slug}.html").write_text(page(slug, title, description, heading, image, CONTENT[slug]), encoding="utf-8")

(ROOT / "404.html").write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | SpicyChat AI Club</title><link rel="stylesheet" href="/style.css">{GOOGLE_TAG}</head><body><main class="wrap error-page"><p class="eyebrow">404</p><h1>Page not found</h1><p>That page may have moved.</p><a class="btn btn-primary" href="/">Return home</a></main></body></html>''', encoding="utf-8")
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /404.html\nSitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8")
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE + ("/" if slug == "index" else "/" + slug + ".html")}</loc></url>\n' for slug, *_ in PAGES) + '</urlset>\n', encoding="utf-8")
DIST = ROOT / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()
for filename in ("style.css", "_headers", "robots.txt", "sitemap.xml"):
    shutil.copy2(ROOT / filename, DIST / filename)
for file in ROOT.glob("*.html"):
    shutil.copy2(file, DIST / file.name)
shutil.copytree(ROOT / "assets", DIST / "assets")
print(f"Built {len(PAGES)} pages for {SITE}; outbound destination: {parsed.netloc}")
