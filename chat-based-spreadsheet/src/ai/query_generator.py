class QueryGenerator:
    def __init__(self, llm):
        self.llm = llm

    def generate_query(self, user_input, table_schema):
        prompt = self.create_prompt(user_input, table_schema)
        sql_query = self.llm.generate(prompt)
        return sql_query

    def create_prompt(self, user_input, table_schema):
        schema_description = self.describe_schema(table_schema)
        prompt = f"Based on the following table schema:\n{schema_description}\n\n" \
                 f"Generate an SQL query for the following request:\n{user_input}"
        return prompt

    def describe_schema(self, table_schema):
        description = ""
        for column in table_schema:
            description += f"Column: {column['name']}, Type: {column['type']}\n"
        return description.strip()