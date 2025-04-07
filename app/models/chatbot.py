from datetime import datetime
from local_llm import LocalLLM

class Chatbot:
    def __init__(self):
        self.llm = LocalLLM()
        self.current_year = datetime.now().year
        self.fact_guide = {
            "president of india": {
                "current": "Droupadi Murmu",
                "2022": "Ram Nath Kovind",
                "2017": "Ram Nath Kovind",
                "2012": "Pranab Mukherjee"
            },
            "prime minister of india": {
                "current": "Narendra Modi",
                "2020": "Narendra Modi",
                "2014": "Narendra Modi",
                "2004": "Manmohan Singh"
            }
        }

    def get_response(self, input_text):
        if not input_text.strip():
            return "Please ask a complete question."

        # Extract year from question if specified
        year = self._extract_year(input_text)
        query = input_text.lower()

        # Handle time-specific queries
        for position, data in self.fact_guide.items():
            if position in query:
                if year:
                    return self._get_historical_answer(position, year, query)
                return f"The current {position} is {data['current']} (as of {self.current_year})."

        # Generic LLM response for other queries
        return self._get_llm_response(input_text)

    def _extract_year(self, text):
        # Extract 4-digit years
        for word in text.split():
            if word.isdigit() and len(word) == 4:
                return word
        return None

    def _get_historical_answer(self, position, year, query):
        data = self.fact_guide.get(position, {})
        closest_year = str(max(
            (int(y) for y in data.keys() 
             if y != "current" and int(y) <= int(year)),
            default=None
        ))
        
        if closest_year:
            person = data[closest_year]
            return f"The {position} in {year} was {person}."
        return f"I don't have data about {position} for {year}."

    def _get_llm_response(self, prompt):
        # Enhanced prompt for better responses
        enhanced_prompt = (
            f"Today is {datetime.now().strftime('%B %d, %Y')}. "
            f"Provide a concise and accurate response to: {prompt}\n"
            "Answer:"
        )
        response = self.llm.generate_response(enhanced_prompt)
        
        # Post-processing
        response = response.split("Answer:")[-1].strip()
        response = response.split("\n")[0].strip()
        return response if response else "I couldn't generate a proper response."

