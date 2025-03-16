# adpro_project

Hi, this is us :

Bastien Gobet, mail address: 52255@novasbe.pt

Eloi Lahondé, mail address: 65729@novasbe.pt

Milán Péter Novák, mail address: 67256@novasbe.pt

Tomás Leite Barbosa Oliveira, mail address: 56466@novasbe.pt

Here is the process to run the streamlit app, with the AI system locally: 

  1.First step is to downlaod the githup repo on your computer: 
For installing the packages, all you need to do is downloading the files from this branch to your computer, open the downloaded folder in a terminal, create a new virtual environment, and then run the following prompt: pip install -r requirements.txt

  2.Second step is to download the AI model locally 
Go to https://ollama.com/library and download the AI locally in your folder, in our case : https://ollama.com/library/mistral
Once it has initialized the environment, you need to start running one of the ollama models (in our case it's going to be mistral) in the background, with this prompt: "ollama run mistral &" (for mac/Linux users) or "start /B ollama run mistral" (for Windows users)

If it's up and running in the back, you can give start running the streamlit app with the following prompt: streamlit run streamlit_app.py

If you followed the right steps (and prayed in the meantime for the computer god to not get your things tangled) the app should start running in your browser.
