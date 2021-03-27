#Emojies

LIKE_EMOJI="\U0001f44d"
CHECK_EMOJI="\u2705"
UNCHECK_EMOJI="\u274e"
CROSS_EMOJI="\u274c"
RIGHT_ARROW="\u27a1\ufe0f"
MAIL_EMOJI="\U0001f4e7"

# Hardcoded blacklist of mail IDs (In lower case)
#! If required
NON_STUDENT_MAILS=[
    "",
]

# Length of the bcrypt key generated
LENGTH = 16

# Regex used for email validation
REGEX = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

# Allowed domain of the mail IDs
DOMAIN = "iiitb.ac.in"

# List
ROLES=[
    "scholars"
    "imt2016",
    "imt2017",
    "imt2018",
    "mt2019",
    "dt2019",
    "imt2019",
    "mt2020",
    "dt2020",
    "imt2020",
]
ALL_ROLES=[
    "scholars"
    "imt2016",
    "imt2017",
    "imt2018",
    "mt2019",
    "dt2019",
    "imt2019",
    "mt2020",
    "dt2020",
    "imt2020",
    "",
]

#! Greeting shouldn't contain '#'

# Place holder
_GREETINGS="#"

# Greetings list
GREETINGS=[
    f"{_GREETINGS} just landed.",
    f"A wild {_GREETINGS} appeared.",
    f"Welcome {_GREETINGS}. Say hi!",
    f"{_GREETINGS} joined the party.",
    f"{_GREETINGS} is here.",
    f"Welcome, {_GREETINGS}. We hope you brought pizza.",
    f"{_GREETINGS} just slid into the server.",
    f"Yay you made it, {_GREETINGS}.",
]

# CP Logos

CP_LOGOS={
        "codeforces.com":"https://sta.codeforces.com/s/54591/images/codeforces-logo-with-telegram.png",
        "open.kattis.com":"https://open.kattis.com/images/site-logo",
        "www.codechef.com":"https://s3.amazonaws.com/codechef_shared/sites/all/themes/abessive/logo.png",
        "leetcode.com":"https://upload.wikimedia.org/wikipedia/commons/1/19/LeetCode_logo_black.png",
        "binarysearch.com":"https://cdn.dribbble.com/users/913795/screenshots/14724005/media/38309ab447a27bf7311592715b6baeae.png?compress=1&resize=1000x750",
        "topcoder.com":"https://www.topcoder.com/wp-content/media/2016/01/tc_new_logo-300x156.png",
        "atcoder.jp":"https://img.atcoder.jp/assets/logo.png",
    }

# Colors

COLORS=[
    0xFACE53,
    0x1F8ECE,
    0xB73A23,
    0x00ff00,
    0x00ffff,
    0x8000ff,
    0xff0040,
    0xff8000,
    0xffff00
]