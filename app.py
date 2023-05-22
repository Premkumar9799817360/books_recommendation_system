from flask import Flask, render_template ,request
import pickle
import numpy as np
import pandas

popular_df = pickle.load(open("popular.pkl", "rb"))
pt = pickle.load(open("pt.pkl","rb"))
books = pickle.load(open("books.pkl","rb"))
similarity_scores = pickle.load(open("similarity_score.pkl","rb"))
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                            book_name=list(popular_df['Book-Title'].values),
                              votes=list(popular_df['num_rating'].values),
                              rating=list(popular_df['avg_rating'].values),
                              image=list(popular_df['Image-URL-L'].values),
                             author=list(popular_df['Book-Author'].values),
                              year=list(popular_df['Year-Of-Publication'].values)

                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
        if request.method == 'POST':
            user_input = request.form.get('user_input')
            try:
                index = np.where(pt.index==user_input)[0][0]
                similar_item = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1], reverse =True)[1:9]
                
                data = []
                for i in similar_item:
                    item = []
                    temp_df = books[books['Book-Title']==pt.index[i[0]]]
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))
                    item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
                    
                    data.append(item)
            
                return render_template('recommend.html',data=data)
            except:
                return render_template('final.html')
if __name__ == "__main__":
    app.run(debug=False)
