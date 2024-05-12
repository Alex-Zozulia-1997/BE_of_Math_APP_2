# Mind Games

Here is the link to the deployed project: https://mind-games.onrender.com/l (it might lag for 50 sec, as I was using a free version of elphantSQL, which goes to sleep if not interacted with in 15 mins)

The app includes 3 games - mental addition/subtraction, mental multiplication, blindfold chess puzzles.
The project allows you to practice, compare yourself to other users and store your results.

This is the Backend Part of the project, you can find FE in this repo as well.

Here is a video of how it functions at the moment: https://www.loom.com/share/5b327bffcf6145df9b6223ce586edc9f?sid=b13fccdf-2ad9-45b5-8b41-01fb842fc408

## Preparation

As we are using Flask, run pip3 install -r requirements.txt.
You will have to reset the db url to the remote one by setting an env variable named DATABASE_URL, otherwise it will go to sqlite:///data.db.
Run flask db init.
Also, you will need to create a variable named "SK" for secret key. That can be done by running secrets.py in the util folder. It will print you the key and you can copy it as an env variable.

If you opt to copy the project - first make sure that you load the db with the chess puzzles from lichess.org db, which is available here: https://database.lichess.org/

You can run file called lichess.py, but make sure that you indicate the correct path of the downloaded file in line 56.

Once that is done, you should try running the app (flask run) and test it by typing pytest in tthe command line.

There are also docker settings, so you might want to download docker and run it through there.

If you would like to test the functionality of the enpoints, you can run pytest in your terminal. For the e2e tests, you will need to download the FE repo. You will find the tests in "e2e" folder: https://github.com/Alex-Zozulia-1997/frontend_mind_games

Also, here in the test folder you can find the insomnia collection exported to json, there you can conviniently test both on local machine and on the live webpage.
