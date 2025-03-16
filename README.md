# adpro_project

Bastien Gobet, mail address: 52255@novasbe.pt

Eloi Lahondé, mail address: 65729@novasbe.pt

Milán Péter Novák, mail address: 67256@novasbe.pt

Tomás Leite Barbosa Oliveira, mail address: 56466@novasbe.pt


For installing the packages, all you need to do is downloading the files from this branch to your computer, open the downloaded folder in a terminal, create a new virtual environment, and then run the following prompt: pip install -r requirements.txt

Once it has initialized the environment, you need to start running one of the ollama models (in our case it's going to be mistral) in the background, with this prompt: ollama run mistral &
If it's up and running in the back, you can give start running the streamlit app with the following prompt: streamlit run streamlit_app.py

If you followed the right steps (and prayed in the meantime for the computer god to not get your things tangled) the app should start running in your browser.
