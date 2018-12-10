import json
import nltk


class Query:
    def __init__(self):
        self.setup_questions()

    # Load the KB file
    def setup_questions(self):
        with open("data/qa.json") as fin:
            self.questions = json.load(fin)

    # iterate over all question and find the question with smallest distance to 'question'
    def match_question(self, question):
        num_questions = len(self.questions)
        min_dist = float("inf")
        min_id = -1
        for i in range(num_questions):
            curr_q = self.questions[i]["question"]

            dist = nltk.jaccard_distance(set(curr_q), set(question))

            if dist < min_dist:
                min_id = i
                min_dist = dist

        return min_id

    # Get answer from KB after matching question
    def get_answer(self, question):
        matched_qid = match_question(question)
        query = get_query(matched_qid)
        answer = query_dictionary(query)
        return answer

    def get_query(self, q_id):
        return self.questions[q_id]["answer"]

    def get_question(self, q_id):
        return self.questions[q_id]["question"]


if __name__ == "__main__":
    query = Query()

    # Start Test
    my_quest = "What's Bilbo Baggins book called?"
    j = query.match_question(my_quest)
    print("matched q: %s real q: %s" % (query.get_question(j), my_quest))
    print(query.get_query(j))
    print("\n")

    my_quest = "What species are the Orcs?"
    j = query.match_question(my_quest)
    print("matched q: %s real q: %s" % (query.get_question(j), my_quest))
    print(query.get_query(j))
    print("\n")

    my_quest = "Where do Saruman and Gandalf meet?"
    j = query.match_question(my_quest)
    print("matched q: %s real q: %s" % (query.get_question(j), my_quest))
    print(query.get_query(j))
    # End Test
