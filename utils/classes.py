from os import environ

class Config:
    """ bot token and jishaku configuration """

    TOKEN: str = "MTAzNjI0MDA1MDAzMzI3OTA0Ng.GKcG4j.eBC9fCuhscAaQnbKzLwZ0awdtY60WIVo0pblWg"
    api_key: str = "AIzaSyDNph0kx8Iw1K6wWxNeYrhJjP1bsNlr_nM"
    environ["JISHAKU_NO_UNDERSCORE"] = "True"
    environ["JISHAKU_FORCE_PAGINATOR"] = "True"


class Emojis:
    """ emojis used for the bot """

    desktop: str = "🖥️"
    mobile: str = "📱"
    web: str = "🕸️"
    mod: str = "<:mod:1058102336507084880>"

    success: str = "<:success:938545247074525215>"
    error: str = "<:fail:938545235187875890>"
    warning: str = "<:wrn:938545245824626749>"
    loading: str = "<a:loading:938545251105243147>"

    ticket: str = "<:ticket:1058818747995000832>"
    btc: str = "<:btc:969622967640268870>"
    eth: str = "<:eth:969622140309622885>"
    usdt: str = "<:Cusdt:969622012878270544>"
    paypal: str = "<:paypal:1072509136996151306>"
    cashapp: str = "<:cashapp:1072511568211890216>"
    boost: str = "<:boostheart:906898503773597696>"
    money: str = "<a:Money:924657421438316554>"

    stop: str = "<:stop:1058805071200129054>"
    next_page: str = "<:nextpage:1058805078477254707> "
    previous_page: str = "<:previouspage:1058808343034069042>"
    first_page: str = "<:firstpage:1058805074001932420>"
    last_page: str = "<:lastpage:1058805076052934817>"

    cpu: str = "<:cpu:1058102220018688100>"
    memory: str = "<:memory:1058102231943086142>"
    latency: str = "<:latency:1058102224519172176>"
    system: str = "<:ubuntu:938545244704755762>"
    commands: str = "<:commands:938545232675496027>"
    lines: str = "<:vsCode:938545239969366178>"
    system: str = "<:Bbot:970262956371746818>"

    koin: str = "<:koin:1077954962325250118>"
    roblox: str = "<:roblox:1059207597544190032>"
    soundcloud: str = "<:soundcloud:1058121029186236486>"


class ColourCodes:
    """ colours used for the bot """

    theme_colour: int = int("ff7dc9", 16)
    invisible_colour: int = int("2E3235", 16)

    spotify_colour: int = int("1DB954", 16)
    soundcloud_colour: int = int("e74c0d", 16)
    booster_colour: int = int("fe89ff", 16)
    roblox_colour: int = int("d8d5d5", 16)

    success_colour: int = int("3cff8f", 16)
    warning_colour: int = int("ffbc3c", 16)
    error_colour: int = int("d80000", 16)


class EconomyList:
    """ for the beg command in the economy module """

    roles: dict = {
        "overlord": 2500000,
        "master": 750000,
        "average": 250000,
        "rookie": 100000
    }

    celebs: list = [
        "Marilyn Monroe",
        "Abraham Lincoln",
        "Nelson Mandela",
        "John F. Kennedy",
        "Martin Luther King",
        "Queen Elizabeth II",
        "Winston Churchill",
        "Donald Trump",
        "Bill Gates",
        "Muhammad Ali",
        "Mahatma Gandhi",
        "Mother Teresa",
        "Christopher Columbus",
        "Charles Darwin",
        "Elvis Presley",
        "Albert Einstein",
        "Paul McCartney",
        "Queen Victoria",
        "Pope Francis",
        "Jawaharlal Nehru",
        "Leonardo da Vinci",
        "Vincent Van Gogh",
        "Franklin D. Roosevelt",
        "Pope John Paul II",
        "Thomas Edison",
        "Rosa Parks",
        "Lyndon Johnson",
        "Ludwig Beethoven",
        "Oprah Winfrey",
        "Indira Gandhi",
        "Eva Peron",
        "Benazir Bhutto",
        "George Orwell",
        "Desmond Tutu",
        "Dalai Lama",
        "Walt Disney",
        "Neil Armstrong",
        "Peter Sellers",
        "Barack Obama",
        "Malcolm X",
        "J.K.Rowling",
        "Richard Branson",
        "Pele",
        "Angelina Jolie",
        "Jesse Owens",
        "John Lennon",
        "Henry Ford",
        "Haile Selassie",
        "Joseph Stalin",
        "Lord Baden Powell",
        "Michael Jordon",
        "George Bush Jnr",
        "Vladimir Lenin",
        "Ingrid Bergman",
        "Fidel Castro",
        "Leo Tolstoy",
        "Greta Thunberg",
        "Pablo Picasso",
        "Oscar Wilde",
        "Coco Chanel",
        "Charles de Gaulle",
        "Amelia Earhart",
        "John M Keynes",
        "Louis Pasteur",
        "Mikhail Gorbachev",
        "Plato",
        "Adolf Hitler",
        "Sting",
        "Mary Magdalene",
        "Alfred Hitchcock",
        "Michael Jackson",
        "Madonna",
        "Mata Hari",
        "Cleopatra",
        "Grace Kelly",
        "Steve Jobs",
        "Ronald Reagan",
        "Lionel Messi",
        "Babe Ruth",
        "Bob Geldof",
        "Roger Federer",
        "Sigmund Freud",
        "Woodrow Wilson",
        "Mao Zedong",
        "Katherine Hepburn",
        "Audrey Hepburn",
        "David Beckham",
        "Tiger Woods",
        "Usain Bolt",
        "Carl Lewis",
        "Prince Charles",
        "Jacqueline Kennedy Onassis",
        "C.S. Lewis",
        "Billie Holiday",
        "J.R.R. Tolkien",
        "Billie Jean King",
        "Margaret Thatcher",
        "Anne Frank",
        "More famous people",
        "Simon Bolivar",
        "Marie Antoinette",
        "Cristiano Ronaldo",
        "Emmeline Pankhurst",
        "Emile Zatopek",
        "Lech Walesa",
        "Julie Andrews",
        "Florence Nightingale",
        "Marie Curie",
        "Stephen Hawking",
        "Tim Berners Lee",
        "Aung San Suu Kyi",
        "Lance Armstrong",
        "Shakira",
        "Jon Stewart",
        "Wright Brothers  Orville",
        "Ernest Hemingway",
        "Roman Abramovich",
        "Tom Cruise",
        "Rupert Murdoch",
        "Al Gore",
        "Sacha Baron Cohen",
        "George Clooney",
        "Paul Krugman",
        "Jimmy Wales",
        "Brad Pitt",
        "Kylie Minogue",
        "Stephen King"
    ]

    jobs: list = [
        "professional esexer",
        "pornstar",
        "male stripper",
        "stripper",
        "teacher",
        "doctor",
        "police officer",
        "chef",
        "firefighter",
        "bus driver",
        "scientist",
        "vet",
        "artist",
        "pilot",
        "nurse",
        "baker",
        "builder",
        "judge",
        "farmer",
        "waiter",
        "waitress",
        "butcher",
        "cashier",
        "astronaut",
        "football player",
        "car mechanic",
        "musician",
        "taxi driver",
        "barber",
        "hairdresser",
        "pharmacist",
        "business man",
        "office worker",
        "maid",
        "soldier",
        "sailor",
        "plumber",
        "photographer",
        "reporter",
        "director",
        "software developer",
        "architect",
        "optician",
        "surgeon",
        "detective"
    ]
