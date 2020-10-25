from flask import Flask, flash, redirect, render_template, request, session, abort
from random import randint
 
app = Flask(__name__)
 
@app.route("/")
@app.route("/index")
def yes():
    import pandas as pd
    import numpy as np

    train_data = pd.read_csv(r"C:\Users\ryjar_000\Desktop\Scripts\Train_Set.csv")

    raw_words = train_data.loc[:,'word']
    words = np.asarray(list(set(train_data.loc[:,'word'])))

    raw_category = train_data.loc[:,'category']
    category = sorted(list(set(train_data.loc[:,'category'])))

    from sklearn.model_selection import train_test_split
    X, y = raw_words,raw_category
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size = 0)

    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.naive_bayes import MultinomialNB

    clf = Pipeline([('vectorizer', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', MultinomialNB())])
    clf = clf.fit(X,y)        

    import os
    test_docs = []
    test_data_path = r"C:\\Users\\ryjar_000\Desktop\Scripts\Clean"
    file_number = 0

    for text_file in os.listdir(test_data_path):
        temp_docs = []
        text_file = open(test_data_path + "\\" + str(file_number) + ".txt", encoding="ascii", errors="ignore")
        text = text_file.read()
        temp_docs.append(text.rstrip('\n'))
        test_docs.extend(temp_docs)
        file_number = file_number + 1

    test_docs_proba = clf.predict_proba(test_docs)

    test_docs_proba_arranged = np.flip(np.sort(test_docs_proba,axis=1),axis=1).tolist()
    test_docs_probability_ac = [prob[0:5] for prob in test_docs_proba_arranged] #Change the probability here

    test_docs_rank_arranged = np.flip(np.argsort(test_docs_proba, axis=1),axis=1).tolist()
    test_docs_rank = [rank[0:5] for rank in test_docs_rank_arranged] #Change the ranking here

    counter=0
    flask = []
    for topic, labels in zip(test_docs, test_docs_rank):
        topics = []
        topic_probability = []
        display = []
        i = 0
        for topic_number in test_docs_rank[counter]:
            topics.append(category[topic_number])
        for probability in test_docs_probability_ac[counter]:
            topic_probability.append(str(round((probability * 100), 4)) + "%")
            
        display.append("<table>") 
        
        while i <= 4:
            display.append("<tr>")
            display.append("<td>"+ str(topics[i]) +"</td>")
            display.append("<td>"+ str(topic_probability[i]) +"</td>")
            display.append("</tr>")
            
            i += 1
            
        display.append("</table>") 
        
        import matplotlib.pyplot as plt
        
        x = topics
        y = reversed(topic_probability)
        
        
        fig, ax = plt.subplots() 
        
        for i, v in enumerate(y):
            plt.text(v, i, " "+str(v), color='blue', va='center', fontweight='bold')
        
        width = 0.75 # the width of the bars 
        ind = np.arange(len(y))  # the x locations for the groups
        ax.barh(ind, y, width, color="blue")
        ax.set_yticks(ind+width/2)
        ax.set_yticklabels(x, minor=False)     
        """
        
        axis.plot(x, y)
        canvas = FigureCanvas(fig)
        output = io.BytesIO()
        canvas.print_png(output)
        response = make_response(output.getvalue())
        response.mimetype = 'image/png'
        """
        plt.savefig(r"C:\Users\ryjar_000\Desktop\Scripts\Graphs\\" + str(counter) + ".png", dpi=300, format='png', bbox_inches='tight') # use format='svg' or 'pdf' for vectorial pictures
        
        flask.append("<b>Result " + str(counter+1) + ":</b><br/>" + topic + "<br/><br/><b>Possible Topics: </b>" + ' '.join(display))
        
        counter+=1

    print('\n\n '.join(flask))
    return('<br/><br/>  '.join(flask))
 
if __name__ == "__main__":
    app.run()
