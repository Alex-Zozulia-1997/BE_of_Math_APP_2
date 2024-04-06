# Mind Games

The app includes 3 games - mental addition/subtraction, mental multiplication, blindfold chess puzzles.
The project allows you to practice, compare yourself to other users and store your results.

This is the Backend Part of the project, you can find FE in this repo as well.

Here is a video of how it functions at the moment: https://www.loom.com/share/5b327bffcf6145df9b6223ce586edc9f?sid=b13fccdf-2ad9-45b5-8b41-01fb842fc408

## Preparation

As we are using Flask, run pip3 install -r requirements.txt.
You will have to reset the db url to the remote one by setting an env variable named DATABASE_URL, otherwise it will go to sqlite:///data.db.
Run flask db init.
Also, you will need to create a variable named "SK" for secret key. That can be done by running secrets.py in the util folder.

If you opt to copy the project - first make sure that you load the db with the chess puzzles from lichess.org db, which is available here: https://database.lichess.org/

You can run file called lichess.py, but make sure that you indicate the correct path of the downloaded file in line 56.

once that is done, you should try running the app (flask run) and test it by typing pytest in tthe command line.

There are also docker settings, so you might want to download docker and run it through there.
