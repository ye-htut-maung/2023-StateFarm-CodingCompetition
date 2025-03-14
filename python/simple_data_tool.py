import json
import math
import operator

from statistics import mean



class SimpleDataTool:

    AGENTS_FILEPATH = 'data/sfcc_2023_agents.json'
    CLAIM_HANDLERS_FILEPATH = 'data/sfcc_2023_claim_handlers.json'
    CLAIMS_FILEPATH = 'data/sfcc_2023_claims.json'
    DISASTERS_FILEPATH = 'data/sfcc_2023_disasters.json'

    REGION_MAP = {
        'west': 'Alaska,Hawaii,Washington,Oregon,California,Montana,Idaho,Wyoming,Nevada,Utah,Colorado,Arizona,New Mexico',
        'midwest': 'North Dakota,South Dakota,Minnesota,Wisconsin,Michigan,Nebraska,Iowa,Illinois,Indiana,Ohio,Missouri,Kansas',
        'south': 'Oklahoma,Texas,Arkansas,Louisiana,Kentucky,Tennessee,Mississippi,Alabama,West Virginia,Virginia,North Carolina,South Carolina,Georgia,Florida',
        'northeast': 'Maryland,Delaware,District of Columbia,Pennsylvania,New York,New Jersey,Connecticut,Massachusetts,Vermont,New Hampshire,Rhode Island,Maine'
    }

    def __init__(self):
        self.__agent_data = self.load_json_from_file(self.AGENTS_FILEPATH)
        self.__claim_handler_data = self.load_json_from_file(
            self.CLAIM_HANDLERS_FILEPATH)
        self.__claim_data = self.load_json_from_file(self.CLAIMS_FILEPATH)
        self.__disaster_data = self.load_json_from_file(
            self.DISASTERS_FILEPATH)

    # Helper Methods

    def load_json_from_file(self, filename):
        data = None

        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def get_agent_data(self):
        return self.__agent_data

    def get_claim_handler_data(self):
        return self.__claim_handler_data

    def get_disaster_data(self):
        return self.__disaster_data

    def get_claim_data(self):
        return self.__claim_data

    # Unit Test Methods

    # region Test Set One

    def get_num_closed_claims(self):
        """Calculates the number of claims where that status is "Closed"

        Returns:
            int: number of closed claims
        """
        claim_file = self.get_claim_data()
        closed_counter = 0

        for i in range(len(claim_file)):
            if(claim_file[i].get("status") == "Closed"):
                    closed_counter += 1
        return closed_counter


    def get_num_claims_for_claim_handler_id(self, claim_handler_id):
        """Calculates the number of claims assigned to a specific claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            int: number of claims assigned to claim handler
        """

        file = self.get_claim_data()
        claim_counter = 0
        for i in range(len(file)):
            if (file[i].get("claim_handler_assigned_id") == claim_handler_id):
                claim_counter += 1

        return claim_counter

    def get_num_disasters_for_state(self, state):
        """Calculates the number of disasters for a specific state

        Args:
            state (string): name of a state in the United States of America,
                            including the District of Columbia

        Returns:
            int: number of disasters for state
        """
        file = self.get_disaster_data()
        disaster_counter = 0
        for i in range(len(file)):
            if (file[i].get("state") == state):
                disaster_counter += 1
        return disaster_counter


    # endregion

    # region Test Set Two

    def get_total_claim_cost_for_disaster(self, disaster_id):
        """Sums the estimated cost of a specific disaster by its claims

        Args:
            disaster_id (int): id of disaster

        Returns:
            float | None: estimate cost of disaster, rounded to the nearest hundredths place
                          returns None if no claims are found
        """
        file = self.get_claim_data()
        sum_of_estimate_cost = 0.0
        is_found = False

        for i in range(len(file)):
            if(file[i].get("disaster_id") == disaster_id):
                is_found = True
                sum_of_estimate_cost += file[i].get("estimate_cost")

        if not is_found:
            return None

        
        return sum_of_estimate_cost





    def get_average_claim_cost_for_claim_handler(self, claim_handler_id):
        """Gets the average estimated cost of all claims assigned to a claim handler

        Args:
            claim_handler_id (int): id of claim handler

        Returns:
            float | None : average cost of claims, rounded to the nearest hundredths place
                           or None if no claims are found
        """

        file = self.get_claim_data()
        total_estimate_cost = 0.0
        total_handler = 0
        is_found = False

        for i in range(len(file)):
            if file[i].get("claim_handler_assigned_id") == claim_handler_id:
                is_found = True
                total_estimate_cost += file[i].get("estimate_cost")
                total_handler += 1

        if not is_found: 
            return None
        
        average_cost = round(total_estimate_cost / total_handler, 2)

        return average_cost






    def get_state_with_most_disasters(self):
        """Returns the name of the state with the most disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Jersey and Delaware both have the highest number of disasters at
                 12 disasters each. Then, this method would return "Delaware" since "D"
                 comes before "N" in the alphabet. 

        Returns:
            string: single name of state
        """
        number_of_disasters_by_state = dict()

        file = self.get_disaster_data()

        for i in range(len(file)):
            state_name = file[i].get("state")
            if state_name in number_of_disasters_by_state:
                number_of_disasters_by_state[state_name] += 1
            else:
                number_of_disasters_by_state[state_name] = 1
        
        list_num_of_disasters = number_of_disasters_by_state.values()
        max_disaster = max(list_num_of_disasters)
        list_max_disaster_states = list()

        for state, num_disasters in number_of_disasters_by_state.items():
            if num_disasters == max_disaster:
                list_max_disaster_states.append(state)
        
        list_max_disaster_states.sort()
        return list_max_disaster_states[0]

    def get_state_with_least_disasters(self):
        """Returns the name of the state with the least disasters based on disaster data

        If two states have the same number of disasters, then sort by alphabetical (a-z)
        and take the first.

        Example: Say New Mexico and West Virginia both have the least number of disasters at
                 1 disaster each. Then, this method would return "New Mexico" since "N"
                 comes before "W" in the alphabet. 

        Returns:
            string: single name of state
        """
        number_of_disasters_by_state = dict()

        file = self.get_disaster_data()

        for i in range(len(file)):
            state_name = file[i].get("state")
            if state_name in number_of_disasters_by_state:
                number_of_disasters_by_state[state_name] += 1
            else:
                number_of_disasters_by_state[state_name] = 1
        
        list_num_of_disasters = number_of_disasters_by_state.values()
        max_disaster = min(list_num_of_disasters)
        list_max_disaster_states = list()

        for state, num_disasters in number_of_disasters_by_state.items():
            if num_disasters == max_disaster:
                list_max_disaster_states.append(state)
        
        list_max_disaster_states.sort()
        return list_max_disaster_states[0]


    
    def get_most_spoken_agent_language_by_state(self, state):
        """Returns the name of the most spoken language by agents (besides English) for a specific state

        Args:
            state (string): name of state

        Returns:
            string: name of language
                    or empty string if state doesn't exist
        """

        file = self.get_agent_data()
        num_of_agent_by_language = dict()

        for i in range(len(file)):
            state_name = file[i].get("state")
            language = file[i].get("secondary_language")
            if state_name == state:
                if language in num_of_agent_by_language:
                    num_of_agent_by_language[language] += 1
                else:
                    num_of_agent_by_language[language] = 1

        if len(num_of_agent_by_language) == 0:
            return ""

        list_num_of_language = num_of_agent_by_language.values()
        max_language = max(list_num_of_language)
        list_max_language = list()

        for language, num_langage in num_of_agent_by_language.items():
            if num_langage == max_language:
                list_max_language.append(language)
        
        list_max_language.sort()
        return list_max_language[0]


    def get_num_of_open_claims_for_agent_and_severity(self, agent_id, min_severity_rating):
        """Returns the number of open claims for a specific agent and for a minimum severity level and higher

        Note: Severity rating scale for claims is 1 to 10, inclusive.
        
        Args:
            agent_id (int): ID of the agent
            min_severity_rating (int): minimum claim severity rating

        Returns:
            int | None: number of claims that are not closed and have minimum severity rating or greater
                        -1 if severity rating out of bounds
                        None if agent does not exist, or agent has no claims (open or not)
        """

        file = self.get_claim_data()
        claim_counter = 0
        is_found = False
        
        if min_severity_rating < 1 or min_severity_rating > 10:
            return -1
        
        for i in range(len(file)):
            status = file[i].get("status")
            agent_id_from_file = file[i].get("agent_assigned_id")
            severity_rating = file[i].get("severity_rating")

            if agent_id_from_file == agent_id and status != "Closed" and severity_rating >= min_severity_rating:
                claim_counter += 1
                is_found = True

        print(claim_counter)

        if not is_found:
            return None
        if claim_counter == 0:
            return None
        return claim_counter

    # endregion

    # region TestSetThree

    def get_num_disasters_declared_after_end_date(self):
        """Gets the number of disasters where it was declared after it ended

        Returns:
            int: number of disasters where the declared date is after the end date
        """

        file = self.get_disaster_data()
        disaster_counter = 0


        for i in range(len(file)):
            end_date = file[i].get("end_date")
            declared_date = file[i].get("declared_date")
            list_end_date = end_date.split("-")
            list_declared_date = declared_date.split("-")

            for j in range(len(list_declared_date)):

                if int(list_end_date[j]) == int(list_declared_date[j]):
                    continue
                if int(list_end_date[j]) > int(list_declared_date[j]):
                    break 
                if int(list_end_date[j]) < int(list_declared_date[j]):

                    disaster_counter += 1
                    break
            
        return disaster_counter


    def build_map_of_agents_to_total_claim_cost(self):
        """Builds a map of agent and their total claim cost

        Hints:
            An agent with no claims should return 0
            Invalid agent id should have a value of None
            You should round your total_claim_cost to the nearest hundredths

        Returns:
            dict: key is agent id, value is total cost of claims associated to the agent
        """
        file = self.get_claim_data()
        agent_cost_dict = dict()

        for i in range(100):
            agent_cost_dict[i+1] = 0
        print(agent_cost_dict)

        for i in range(len(file)):
            agent_id = file[i].get("agent_assigned_id")
            claim_cost = file[i].get("estimate_cost")

            if agent_id in agent_cost_dict:
                agent_cost_dict[agent_id] += claim_cost
                agent_cost_dict[agent_id] = round(agent_cost_dict[agent_id],2)
            else:
                agent_cost_dict[agent_id] = None

        print(agent_cost_dict)

        return agent_cost_dict

    def calculate_disaster_claim_density(self, disaster_id):
        """Calculates density of a diaster based on the number of claims and impact radius

        Hints:
            Assume uniform spacing between claims
            Assume disaster impact area is a circle

        Args:
            disaster_id (int): id of diaster

        Returns:
            float: density of claims to disaster area, rounded to the nearest thousandths place
                   None if disaster does not exist
        """
        pi = math.pi

        claim_file = self.get_claim_data()
        numbers_of_claim = 0 
        disaster_radius = 0

        for i in range(len(claim_file)):
            if disaster_id == claim_file[i].get("disaster_id"):
                numbers_of_claim += 1

        disaster_file = self.get_disaster_data()
        
        for i in range(len(disaster_file)):
            if disaster_id == disaster_file[i].get("id"):
                disaster_radius = disaster_file[i].get("radius_miles")
        disaster_area = pi  * disaster_radius *disaster_radius

        if disaster_area == 0:
            return None

        density = round( numbers_of_claim / disaster_area, 5)

        return density

    # endregion

    # region TestSetFour

    def get_top_three_months_with_highest_num_of_claims_desc(self):
        """Gets the top three months with the highest total claim cost

        Hint:
            Month should be full name like 01 is January and 12 is December
            Year should be full four-digit year
            List should be in descending order

        Returns:
            list: three strings of month and year, descending order of highest claims
        """
        

        pass

    # endregion
