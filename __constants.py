LIKE_EMOJI="\U0001f44d"
CHECK_EMOJI="\u2705"
UNCHECK_EMOJI="\u274e"
CROSS_EMOJI="\u274c"
RIGHT_ARROW="\u27a1\ufe0f"
MAIL_EMOJI="\U0001f4e7"

# enter everything in lower case
NON_STUDENT_MAILS=[
    "sac@iiitb.org",
    "abc@iiitb.org"
]
LENGTH = 16
REGEX = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
DOMAIN = "iiitb.org"
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
#Any greeting shouldn't contain '#'
_GREETINGS="#"
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