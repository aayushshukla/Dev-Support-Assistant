import time


class QueryStats:

    def __init__(self):

        self.start_time = time.time()

        self.vector_start = 0
        self.vector_end = 0

        self.llm_start = 0
        self.llm_end = 0

    def start_vector(self):

        self.vector_start = time.time()

    def end_vector(self):

        self.vector_end = time.time()

    def start_llm(self):

        self.llm_start = time.time()

    def end_llm(self):

        self.llm_end = time.time()

    def get_metrics(self):

        vector_time = (
            self.vector_end -
            self.vector_start
        ) * 1000

        llm_time = (
            self.llm_end -
            self.llm_start
        ) * 1000

        total_time = (
            self.llm_end -
            self.start_time
        ) * 1000

        return {
            "vector_time_ms": round(vector_time, 2),
            "llm_time_ms": round(llm_time, 2),
            "total_time_ms": round(total_time, 2)
        }