# bloveland-OOP_FinalProject
Final project for OOP with Ben, Liam, and Dillon

Our project will be a web app hosted on Github Pages that allows a user to play Connect 4 against ChatGPT.
We will use the ChatGPT API to send the current board state to the LLM, and interpret its response as a game action.
For more project details check the Write-Abstract folder and the 4+1_Views folder.

How to Run:
Copy the repository to your local machine, then navigate to the connect_four folder in terminal. Testing
and documentation generation is run with 'make all', and if you want to run the project use 'make run'.
After the flask application is running you can navigate to http://localhost:5000/ in a web browser to
see the project. Initially you may get some errors about the AI functionality, pip install whatever
OpenAI api stuff is required by the terminal error and it should run smoothly. The flask and openai
requirements are also detailed in requirements.txt.

Disclaimer:
The project will not successfully place player 2's moves (ChatGPT) without an API key from
Benjamin Loveland. If you need that functionality please email him. The game will still technically
work, but the AI functionality won't and it will only play Connect 4 with one player.