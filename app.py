from msilib.schema import Component
import pickle
from turtle import width
import requests
import streamlit as st
import hashlib
import sqlite3
import webbrowser
import streamlit.components.v1 as components



# Security
#passlib,hashlib,bcrypt,scrypt

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + str(poster_path)
    return full_path

def recommend(movie):
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('similarity.pkl','rb'))
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:13]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def style_button_row(clicked_button_ix, n_buttons):
    def get_button_indices(button_ix):
        return {
            'nth_child': button_ix,
            'nth_last_child': n_buttons - button_ix + 1
        }

    clicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        border-color: rgb(255, 75, 75);
        color: rgb(255, 75, 75);
        box-shadow: rgba(255, 75, 75, 0.5) 0px 0px 0px 0.2rem;
        outline: currentcolor none medium;
    }
    """
    unclicked_style = """
    div[data-testid*="stHorizontalBlock"] > div:nth-child(%(nth_child)s):nth-last-child(%(nth_last_child)s) button {
        pointer-events: none;
        cursor: not-allowed;
        opacity: 0.65;
        filter: alpha(opacity=65);
        -webkit-box-shadow: none;
        box-shadow: none;
    }
    """
    style = ""
    for ix in range(n_buttons):
        ix += 1
        if ix == clicked_button_ix:
            style += clicked_style % get_button_indices(ix)
        else:
            style += unclicked_style % get_button_indices(ix)
    st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)

def main():
    primary_clr = st.get_option("theme.primaryColor")
    st.set_page_config(page_title="Movie Suggester",layout="wide",initial_sidebar_state="auto", page_icon="favicon")
    
    st.sidebar.title("Simple Login App")

    menu = ["Home","Login","SignUp","Talk to Chatbot"]
    choice = st.sidebar.radio("Menu",menu)

    if choice == "Home":
        st.sidebar.subheader("Home")
        st.sidebar.info("Recommender System is a system that seeks to predict or filter preferences according to the user's choices. ... Content-based filtering methods are totally based on a description of the item and a profile of the user's preferences. It recommends items based on the user's past preferences.")
        st.sidebar.info("Matrix factorization is a class of collaborative filtering algorithms used in recommender systems. This family of methods became widely known during the Netflix prize challenge due to how effective it was")


    elif choice == "Login":
        st.sidebar.subheader("Login Section")

        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password",type='password')
        if st.sidebar.button("Login", on_click=style_button_row):
            # if password == '12345':
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(username,check_hashes(password,hashed_pswd))
            if result:
                st.sidebar.success("Logged In as {}".format(username)) 




            else:
                st.sidebar.warning("Incorrect Username/Password")

            

    elif choice == "Talk to Chatbot":
        st.sidebar.subheader("Friendly Chatbot")
        with st.sidebar:
            html_string = '''
    

            <iframe src='https://webchat.botframework.com/embed/qnabotmovierecommender-bot?s=s80pY5GbSn0.DYHzNtN3aLw53QxNfGxeh5_EGbUt-0ilTrKsBna6i_U'  style='height:400px;width:300px'></iframe>

    
            '''
            components.html(html_string,height=430)  
        

    elif choice == "SignUp":
        st.sidebar.subheader("Create New Account")
        new_user = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password",type='password')

        if st.sidebar.button("Signup", on_click=style_button_row):
            create_usertable()
            add_userdata(new_user,make_hashes(new_password))
            st.sidebar.success("You have successfully created a valid Account")
            st.sidebar.info("Go to Login Menu to login")
    
    




    st.sidebar.title("ABOUT US")

    col1, col2, col3 = st.sidebar.columns([1, 1, 1])


    with col1:
    
        if st.button("✉Mail", on_click=style_button_row, kwargs={
            'clicked_button_ix': 1, 'n_buttons': 4
            }):
            webbrowser.open_new_tab("manimarangv2001@gmail.com")

    with col2:
        if st.button("Linkedin", on_click=style_button_row, kwargs={
            'clicked_button_ix': 2, 'n_buttons': 4
            }):
            webbrowser.open_new_tab("https://www.linkedin.com/in/manimaran-govindaraj")

    with col3:
        if st.button("Github", on_click=style_button_row, kwargs={
        'clicked_button_ix': 3, 'n_buttons': 4
            }):
            webbrowser.open_new_tab("https://github.com/ManimaranGv")

    


    st.header('Movie Recommender System')
    st.subheader("Type or select a movie from the dropdown")
    movies = pickle.load(open('movie_list.pkl','rb'))
    similarity = pickle.load(open('movie_list.pkl','rb'))


    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "",
        movie_list
    )

    if st.button('Show Recommendation', on_click=style_button_row):
        recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
        st.subheader("Hello Some related movies")

        for i in range(0,12,4):
            col = st.columns(4)
            with col[0]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])
            with col[1]:
                st.text(recommended_movie_names[i+1])
                st.image(recommended_movie_posters[i+1])
            with col[2]:
                st.text(recommended_movie_names[i+2])
                st.image(recommended_movie_posters[i+2])
            with col[3]:
                st.text(recommended_movie_names[i+3])
                st.image(recommended_movie_posters[i+3])





    #components.iframe("<iframe src='https://webchat.botframework.com/embed/qnabotmovierecommender-bot?s=s80pY5GbSn0.DYHzNtN3aLw53QxNfGxeh5_EGbUt-0ilTrKsBna6i_U'  style='min-width: 400px; width: 100%; min-height: 500px;'></iframe>")
    





if __name__ == '__main__':
	main()

#<h1>HTML string in RED</h1>
#<script language="javascript">
 #   document.querySelector("h1").style.color = "red";
  #  console.log("Streamlit runs JavaScript");
   # alert("Streamlit runs JavaScript");
 #   </script>