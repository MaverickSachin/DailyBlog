import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from decouple import config
from datetime import datetime


engine = create_engine(config("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    with open("posts.json", "r") as file:
        reader = json.load(file)
        for post in reader:
            db.execute("INSERT INTO posts (title, date_posted, content, user_id) "
                       "VALUES (:title, :date_posted, :content, :user_id)",
                       {"title": post['title'], "date_posted": datetime.utcnow(),
                        "content": post['content'], "user_id": post['user_id']})

            print(f"Added post from {post['user_id']} titled {post['title']}.")

        db.commit()


if __name__ == "__main__":
    main()
