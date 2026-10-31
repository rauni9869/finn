import re
from typing import Dict, Any, Tuple
from app.models.schemas import AnnouncementCategory, PriorityLevel

# Regex keyword mapping for instant, 0-latency rule-based classification
CATEGORY_RULES = [
    (AnnouncementCategory.RESULTS, [
        r"financial\s+result", r"un-?audited\s+result", r"audited\s+result", 
        r"quarterly\s+result", r"outcome\s+of\s+board\s+meeting.*(result|financial)",
        r"statement\s+of\s+accounts", r"q[1-4]\s+fy\d+", r"half\s+yearly\s+result"
    ]),
    (AnnouncementCategory.MA, [
        r"merger", r"demerger", r"amalgamation", r"acquisition", r"joint\s+venture",
        r"scheme\s+of\s+arrangement", r"investing\s+in\s+subsidiary", r"stake\s+sale",
        r"divestment", r"slump\s+sale", r"takeover"
    ]),
    (AnnouncementCategory.MANAGEMENT_CHANGE, [
        r"resignation\s+of", r"appointment\s+of", r"change\s+in\s+director",
        r"managing\s+director", r"chief\s+executive\s+officer", r"chief\s+financial\s+officer",
        r"key\s+managerial\s+personnel", r"kmp", r"superannuation", r"retirement\s+of\s+cfo",
        r"resignation\s+of\s+cfo", r"appointment\s+of\s+ceo"
    ]),
    (AnnouncementCategory.LITIGATION, [
        r"lawsuit", r"litigation", r"regulatory\s+order", r"penalty", r"fine\s+imposed",
        r"income\s+tax\s+search", r"search\s+and\s+seizure", r"us\s+fda", r"form\s+483",
        r"warning\s+letter", r"import\s+alert", r"show\s+cause\s+notice", r"insolvency",
        r"nclt\s+petition", r"cirp"
    ]),
    (AnnouncementCategory.FUND_RAISE, [
        r"qip", r"qualified\s+institutions\s+placement", r"rights\s+issue",
        r"preferential\s+allotment", r"buyback", r"commercial\s+paper",
        r"issuance\s+of\s+ncds", r"debenture", r"fund\s+raising", r"warrants"
    ]),
    (AnnouncementCategory.CAPEX, [
        r"capex", r"capital\s+expenditure", r"greenfield", r"brownfield",
        r"new\s+plant", r"manufacturing\s+facility", r"capacity\s+expansion",
        r"setting\s+up\s+of\s+unit", r"expansion\s+project"
    ]),
    (AnnouncementCategory.DIVIDEND, [
        r"dividend", r"interim\s+dividend", r"final\s+dividend", r"special\s+dividend",
        r"record\s+date\s+for\s+dividend"
    ]),
    (AnnouncementCategory.BONUS_SPLIT, [
        r"bonus\s+issue", r"bonus\s+shares", r"sub-?division\s+of\s+shares",
        r"stock\s+split", r"split\s+of\s+nominal\s+value"
    ]),
    (AnnouncementCategory.INSIDER_TRADING, [
        r"regulation\s+7\(2\)", r"sebi\s+\(pit\)", r"insider\s+trading",
        r"promoter\s+acquisition", r"disposal\s+of\s+shares", r"form\s+c"
    ]),
    (AnnouncementCategory.PLEDGING, [
        r"pledge", r"encumbrance", r"release\s+of\s+pledge", r"creation\s+of\s+pledge",
        r"regulation\s+31\(1\)", r"regulation\s+31\(2\)"
    ]),
    (AnnouncementCategory.CREDIT_RATING, [
        r"credit\s+rating", r"crisil", r"icra", r"care\s+rating", r"india\s+ratings",
        r"rating\s+upgrade", r"rating\s+downgrade", r"reaffirmation\s+of\s+rating"
    ]),
    (AnnouncementCategory.EARNINGS_CALL, [
        r"earnings\s+call", r"conference\s+call", r"concall", r"transcript\s+of\s+call",
        r"audio\s+recording", r"investor\s+presentation.*earnings"
    ]),
    (AnnouncementCategory.INVESTOR_MEETINGS, [
        r"schedule\s+of\s+analyst", r"investor\s+meeting", r"institutional\s+investor",
        r"investor\s+conference", r"one-on-one\s+meeting"
    ]),
    (AnnouncementCategory.POSTAL_BALLOT, [
        r"postal\s+ballot", r"remote\s+e-voting", r"scrutinizer.*report"
    ]),
    (AnnouncementCategory.AGM_EGM, [
        r"annual\s+general\s+meeting", r"extraordinary\s+general\s+meeting",
        r"agm", r"egm", r"proceedings\s+of\s+agm", r"notice\s+of\s+agm"
    ]),
    (AnnouncementCategory.PRESS_RELEASE, [
        r"press\s+release", r"media\s+release", r"order\s+win", r"bagged\s+contract",
        r"partnership", r"collaboration", r"clarification\s+on\s+spurt"
    ]),
]

# Priority Matrix as specified in plan.md
PRIORITY_MAP = {
    AnnouncementCategory.RESULTS: PriorityLevel.HIGH,
    AnnouncementCategory.MA: PriorityLevel.HIGH,
    AnnouncementCategory.MANAGEMENT_CHANGE: PriorityLevel.HIGH,
    AnnouncementCategory.LITIGATION: PriorityLevel.HIGH,
    AnnouncementCategory.FUND_RAISE: PriorityLevel.HIGH,
    AnnouncementCategory.CAPEX: PriorityLevel.HIGH,
    
    AnnouncementCategory.INSIDER_TRADING: PriorityLevel.MEDIUM,
    AnnouncementCategory.PLEDGING: PriorityLevel.MEDIUM,
    AnnouncementCategory.CREDIT_RATING: PriorityLevel.MEDIUM,
    AnnouncementCategory.DIVIDEND: PriorityLevel.MEDIUM,
    AnnouncementCategory.BONUS_SPLIT: PriorityLevel.MEDIUM,
    AnnouncementCategory.EARNINGS_CALL: PriorityLevel.MEDIUM,
    AnnouncementCategory.PRESS_RELEASE: PriorityLevel.MEDIUM,
    
    AnnouncementCategory.INVESTOR_MEETINGS: PriorityLevel.LOW,
    AnnouncementCategory.POSTAL_BALLOT: PriorityLevel.LOW,
    AnnouncementCategory.AGM_EGM: PriorityLevel.LOW,
    AnnouncementCategory.UNCLASSIFIED: PriorityLevel.LOW,
}


class FilingClassifier:
    """Classifies exchange filings into the 17 taxonomy categories with priority rating."""

    def classify(self, headline: str, details: str = "") -> Tuple[AnnouncementCategory, PriorityLevel, str]:
        text = f"{headline} {details}".lower()

        # Check for unclassified routine paperwork first
        if any(re.search(p, text) for p in [
            r"loss\s+of\s+share\s+certificate", r"duplicate\s+share\s+certificate",
            r"regulation\s+7\(3\)", r"regulation\s+40\(9\)", r"esop", r"esos",
            r"allotment\s+of\s+equity\s+shares.*exercise\s+of\s+options",
            r"secretarial\s+compliance", r"newspaper\s+publication"
        ]):
            category = AnnouncementCategory.UNCLASSIFIED
            priority = PriorityLevel.LOW
            summary = "Routine regulatory compliance or share certificates administrative filing."
            return category, priority, summary

        # Iterate through taxonomy rules
        for cat, patterns in CATEGORY_RULES:
            for pattern in patterns:
                if re.search(pattern, text):
                    category = cat
                    priority = PRIORITY_MAP.get(category, PriorityLevel.LOW)
                    summary = self._generate_dense_summary(headline, category)
                    return category, priority, summary

        category = AnnouncementCategory.UNCLASSIFIED
        priority = PriorityLevel.LOW
        summary = "Standard corporate filing or compliance paperwork."
        return category, priority, summary

    def _generate_dense_summary(self, headline: str, category: AnnouncementCategory) -> str:
        clean = headline.strip()
        words = clean.split()
        if len(words) <= 14:
            return clean
        return " ".join(words[:14]) + "..."


classifier = FilingClassifier()

