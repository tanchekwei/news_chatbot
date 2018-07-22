import wikipedia
from difflib import SequenceMatcher
from stanfordcorenlp import StanfordCoreNLP

def main(*request):
    result = []
    ratio = []
    nlp_result = ""
    topic = ""
    while True:
        # if not request:
        #     request = input("What you want to know? ")

        nlp = StanfordCoreNLP(r'D:\stanford-corenlp-full-2018-02-27')
        nlp_result = nlp.pos_tag(str(request))
        nlp.close()

        print(nlp_result)

        count = 0
        for i in nlp_result:
            if 'NN' in i[1]:
                if count == 0:
                    topic += i[0]
                else:
                    topic += " " + i[0]
                count += 1

        print(topic)

        if topic == "":
            question_list = ["tell me", "what is", "definition of"]
            for q in question_list:
                if q in request:
                    print("yes")

        if topic == "":
            return False, None
        # nlp = StanfordCoreNLP('http://localhost', 9000, timeout=30000)
        # print(request)
        # print(nlp.pos_tag(request))


        search_result = wikipedia.search(topic, results=5, suggestion=True)

        print(search_result)
        for i in enumerate(search_result[0]):
            # print(i)
            seq = SequenceMatcher(None, topic.lower(), i[1].lower())
            result.append(i[1])
            ratio.append(seq.ratio() * 100)

        if ratio != []:
            if max(ratio) > 70:
                i = ratio.index(max(ratio))
                print(i)
                try:
                    summary = wikipedia.summary(result[i], sentences=1, chars=0)
                    print(summary)
                    return True, summary
                except wikipedia.exceptions as e:
                    return False, None
        else:
            return False, None

        request = ""
        topic = ""
        summary = ""
        result = []
        ratio = []

        # try:
        #     page = wikipedia.summary(str, sentences=0, chars=0, auto_suggest=True, redirect=True)
        #     return True, page
        # except wikipedia.exceptions as e:
        #     return False, None

            # i = 1
            # page = "Which of the following do you mean?<br />"
            # for option in enumerate(e.options):
            #     page += str(i) + ". " + option[1] + "<br />"
            #
            #     if i == 5:
            #         break
            #     i += 1
            #
            # result = (False, page)
            # print(page)


if __name__ == "__main__":
    main()