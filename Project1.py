import streamlit as st
from googleapiclient.discovery import build
import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import mysql.connector
import psycopg2




# SQL configuration

def migrate_data_to_sql():
   
    client = MongoClient("mongodb+srv://suriyav:Suriya27@cluster0.ojlkvew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client.Youtubeharvesting
    records=db.Task1
   

    # Connect to SQL database
    sql_connection = psycopg2.connect(
        host="localhost",
        user="root",
        password="suri123",
        database="youtubedata"
    )
    sql_cursor = sql_connection.cursor()

    # Fetch data from MongoDB
    cursor = MongoClient.find()
    for document in cursor:
       
        data = tuple(document.values())

        # Insert data into SQL table
        sql_insert_query = f"INSERT INTO {'tabledata1'} VALUES %s"
        sql_cursor.execute(sql_insert_query, (data,))
        sql_connection.commit()

    # Close connections
    sql_cursor.close()
    sql_connection.close()
    client.close()

if __name__ == "__main__":
    migrate_data_to_sql()




# Set up the necessary scopes for the YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Set the path to your API key file
API_KEY_FILE = "AIzaSyDL2rkLVb7HBQPPbL4Kg4M9i3w3ZCbuteI"  
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = API_KEY_FILE


# MongoDB configuration
uri = "mongodb+srv://suriyav:<password>@cluster0.ojlkvew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  
#DB_NAME = "Youtubeharvesting"          
CHANNELS_COLLECTION = "channels" 
VIDEOS_COLLECTION = "videos"     

client = MongoClient("mongodb+srv://suriyav:Suriya27@cluster0.ojlkvew.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.Youtubedataharvesting
records=db.Youtube_Videos

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Function to fetch YouTube channel data

def get_channel_data(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)
    response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        channel_name = item['snippet']['title']
        channel_id = item['id']
        subscribers = item['statistics']['subscriberCount']
        channel_views = item['statistics']['viewCount']
        channel_description = item['snippet']['description']

        # Fetching the playlist ID (you might need to implement this part based on your specific use case)
        playlist_id = "UUueYcgdqos0_PzNOq81zAFg"

        channel_data = {
            "Channel_Name": {
                "Channel_Name": channel_name,
                "Channel_Id": channel_id,
                "Subscription_Count": int(subscribers),
                "Channel_Views": int(channel_views),
                "Channel_Description": channel_description,
                "Playlist_Id": playlist_id
            }
        }

        return channel_data
    return None

# Streamlit app
def main():
    st.title("YouTube Channel Data Retrieval")
    api_key = 'UCueYcgdqos0_PzNOq81zAFg'

    # Input field to enter channel ID
    channel_id = st.text_input("Enter YouTube Channel ID:")
    if st.button("Get Channel Data"):
        if channel_id:
            channel_data = get_channel_data(api_key, channel_id)
            if channel_data:
                st.text("Channel Details in JSON Format:")
                st.text(json.dumps(channel_data, indent=2))
            else:
                st.write("Channel data not found. Please check the channel ID.")
        else:
            st.write("Please enter a valid YouTube Channel ID.")

if __name__ == "__main__":
    main()

