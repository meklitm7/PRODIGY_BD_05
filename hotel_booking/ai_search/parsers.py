import re
from datetime import date, timedelta


class QueryParser:
     
    ROOM_TYPES = {
        "single": "SINGLE",
        "double": "DOUBLE",
        "suite": "SUITE",
        "family": "FAMILY",
    }

    PRICE_WORDS = {
        "cheap": "cheap",
        "budget": "cheap",
        "expensive": "expensive",
        "luxury": "expensive",
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
    def extract_dates(query):
         
        today = date.today()

        if "today" in query:
            return today, today + timedelta(days=1)

        if "tomorrow" in query:
            tomorrow = today + timedelta(days=1)
            return tomorrow, tomorrow + timedelta(days=1)

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

        # Dates
        check_in, check_out = QueryParser.extract_dates(query)

        if check_in is not None:
            filters["check_in"] = check_in
            filters["check_out"] = check_out

        return filters