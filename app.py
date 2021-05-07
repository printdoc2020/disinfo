import streamlit as st
import pandas as pd
import json


def get_num_words(text, key_words, return_keys):
	count = 0
	key_res = []
	if (not text) or (not key_words):
		return count
	text_list = text.split(" ")
	for key in key_words:
		if key in text_list:
			key_res.append(key)
			count+=1
			continue

	if return_keys:
		return ", ".join(k for k in key_res)
	else:
		return count



@st.cache
def read_data(n_tops):
	df = pd.read_csv("data/df_res_2.csv")
	df = df[ [f"top{i+1}" for i in range(n_tops)] + [f"score{i+1}" for i in range(n_tops)] + ["tweetid"]  ]
	df["tweet_account"] = df.tweetid.map(lambda x: x.split("/status/")[0].split("/")[-1])

	df_tweet = pd.read_csv("data/tweet_parse_all_text_cols_and_processed_2cols.csv")

	with open('data/keywords.json') as json_file:
		topics_dict = json.load(json_file)

	return df, df_tweet, topics_dict


st.set_page_config(
	 page_title="Topics Dictionary",
	 page_icon="random",
	 layout="wide",
	 initial_sidebar_state="expanded",
 )



st.title('Topics Using Dictionary')
st.write("Last Updated: May 7, 2021") 



ALL="--- ALL ---"
NO_SORT= "--- not selected ---"
n_tweets = 1000



# link is the column with hyperlinks
# df['tweetid'] = df['tweetid'].apply(make_clickable,1)
# st.write(df.to_html(escape=False, index=False, show_dimensions=True), unsafe_allow_html=True)


n_tops = st.sidebar.selectbox('Get top...',(1,2,3,4,5), 2)
df, df_tweet, topics_dict = read_data(n_tops)

st.sidebar.title('Show...')
topic = st.sidebar.selectbox('Select by Topic',(*df["top1"].unique(), ALL))
account = st.sidebar.selectbox('Select by Account',(*df["tweet_account"].unique(), ALL))

if topic  != ALL:
	df = df[df["top1"] == topic]
if account != ALL:
	df = df[df["tweet_account"] == account]


cols_to_sort_1= [NO_SORT] + [col for col in df.columns if col != "tweetid"] 

first_sort = st.sidebar.selectbox("First, sort by", cols_to_sort_1)

cols_to_sort_2 = [NO_SORT] + [col for col in df.columns if col != "tweetid"] 
if first_sort != NO_SORT:
	cols_to_sort_2.remove(first_sort)
second_sort = st.sidebar.selectbox("Then, sort by", cols_to_sort_2)

ascending = st.sidebar.checkbox("ascending order")





if first_sort != NO_SORT and second_sort != NO_SORT:
	st.write(df.sort_values([first_sort, second_sort], ascending=ascending))
elif first_sort != NO_SORT:
	st.write(df.sort_values([first_sort], ascending=ascending))
else:
	st.write(df)
st.text(f"Show {df.shape[0]} tweets")





tweetid = st.text_input('Looking for tweetid: (ex: https://twitter.com/thetech/status/1299806383303516160)', "")
st.write('tweetid:', tweetid)

target_tweet = df_tweet[df_tweet["tweetid"]==tweetid]

processed_text = target_tweet["all_text_processed"].values[0] if target_tweet["all_text_processed"].values else ""





if tweetid and df[df["tweetid"]==tweetid].shape[0]>0:
	if len(target_tweet)>0:
		st.markdown("**All texts (Tweet content, article content,...) after processing:** " + processed_text)

	for i in range(n_tops):
		st.write("-------")
		st.markdown(f"**Topic {i+1}:** "+ str(df[df["tweetid"]==tweetid][f"top{i+1}"].values[0]))
		all_keywords_in_the_topic = topics_dict[df[df["tweetid"]==tweetid][f"top{i+1}"].values[0]]
		st.markdown("**Keywords appearing:** "+ get_num_words(processed_text, all_keywords_in_the_topic,return_keys=True))
		st.write("-------")














