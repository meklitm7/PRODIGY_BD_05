import re
from datetime import date, timedelta


class QueryParser:
     
    ROOM_TYPES = {
        "single": "SINGLE",
        "double": "DOUBLE",
        "suite": "SUITE",
        "family": "FAMILY",
        # Synonyms
        "deluxe": "SUITE",
        "luxury": "SUITE",
        "apartment": "SUITE",
    }

    PRICE_WORDS = {
    "cheap": "cheap",
    "budget": "cheap",
    "economy": "cheap",
    "affordable": "cheap",
    "low cost": "cheap",

    "expensive": "expensive",
    "luxury": "expensive",
    "premium": "expensive",
}

    LOCATIONS = [
        "addis ababa",
        "addis",
        "hawassa",
        "bahir dar",
        "adama",
        "mekelle",
        "gondar",
        "jimma",
    ]

    @staticmethod
    def extract_guests(query):
         
        match = re.search(
            r"(\d+)\s*(guest|guests|person|people)",
            query,
        )

        if match:
            return int(match.group(1))

        return None
    
    @staticmethod
    def extract_price(query):
         
        under = re.search(
            r"(under|below|less than)\s+(\d+)",
            query,
        )

        if under:
            return (
                "max",
                int(under.group(2)),
            )

        over = re.search(
            r"(over|above|more than)\s+(\d+)",
            query,
        )

        if over:
            return (
                "min",
                int(over.group(2)),
            )

        return None
    @staticmethod
    def extract_nights(query):
         
        match = re.search(
            r"(\d+)\s*night",
            query,
        )

        if match:
            return int(match.group(1))

        return None

    @staticmethod
    def extract_dates(query):
         
        today = date.today()

         
        if "today" in query:
            return today, today + timedelta(days=1)

         
        if "tomorrow" in query:
            tomorrow = today + timedelta(days=1)
            return tomorrow, tomorrow + timedelta(days=1)

         
        if "this weekend" in query:

            days_until_saturday = (5 - today.weekday()) % 7

            saturday = today + timedelta(days=days_until_saturday)

            monday = saturday + timedelta(days=2)

            return saturday, monday

         
        if "next weekend" in query:

            days_until_saturday = ((5 - today.weekday()) % 7) + 7

            saturday = today + timedelta(days=days_until_saturday)

            monday = saturday + timedelta(days=2)

            return saturday, monday

        return None, None

    @staticmethod
    def parse(query):
         
        query = query.lower().strip()

        filters = {}

        # Room type
        for word, room in QueryParser.ROOM_TYPES.items():
            if word in query:
                filters["room_type"] = room
                break

        # Price
        for word, value in QueryParser.PRICE_WORDS.items():
            if word in query:
                filters["price"] = value
                break

        # Location
        for location in QueryParser.LOCATIONS:
            if location in query:
                filters["location"] = location.title()
                break

        # Guests
        guests = QueryParser.extract_guests(query)

        if guests is not None:
            filters["guests"] = guests

        # Price amount
        price = QueryParser.extract_price(query)

        if price is not None:
            filters["price_range"] = price

         
        # Dates
        check_in, check_out = QueryParser.extract_dates(query)

        nights = QueryParser.extract_nights(query)

        if check_in is not None:

            if nights is not None:
                check_out = check_in + timedelta(days=nights)

            filters["check_in"] = check_in
            filters["check_out"] = check_out

        return filters