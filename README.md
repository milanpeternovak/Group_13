# adpro_project

Hi, this is us :

Bastien Gobet, mail address: 52255@novasbe.pt

Eloi Lahondé, mail address: 65729@novasbe.pt

Milán Péter Novák, mail address: 67256@novasbe.pt

Tomás Leite Barbosa Oliveira, mail address: 56466@novasbe.pt

**Here is the process to run the streamlit app, with the AI system locally: **

  1.First step is to downlaod the githup repo on your computer: 
For installing the packages, all you need to do is downloading the files from this branch to your computer, open the downloaded folder in a terminal, create a new virtual environment, and then run the following prompt: pip install -r requirements.txt

  2.Second step is to download the AI model locally 
Go to https://ollama.com/library and download the AI locally in your folder, in our case : https://ollama.com/library/mistral
Once it has initialized the environment, you need to start running one of the ollama models (in our case it's going to be mistral) in the background, with this prompt: "ollama run mistral &" (for mac/Linux users) or "start /B ollama run mistral" (for Windows users)

If it's up and running in the back, you can give start running the streamlit app with the following prompt: streamlit run streamlit_app.py

If you followed the right steps (and prayed in the meantime for the computer god to not get your things tangled) the app should start running in your browser.

**Text Classification and Its Contribution to the UN’s Sustainable Development Goals**

Text classification, as applied in this project, has the potential to support the United Nations Sustainable Development Goals (SDGs) by making information processing more efficient, expanding access to knowledge, and driving innovation. One of the key SDGs that can benefit from this technology is Goal 4: Quality Education. AI-powered classification can help organize and filter large amounts of educational content, making it easier for learners to find relevant materials. By using similar techniques to those implemented in this project, AI could assist in sorting and recommending educational resources, research papers, and news articles, ultimately enhancing digital literacy and personalized learning experiences.

Another major area where AI-driven text classification can make a difference is Goal 10: Reduced Inequalities. Language and accessibility barriers often limit the flow of information, especially for marginalized communities. AI can be used to classify, translate, and distribute essential documents, ensuring that critical information reaches those who need it most. Additionally, text classification can help monitor and flag harmful content, such as hate speech and misinformation, fostering a safer and more inclusive online environment. This aligns with the broader aim of promoting equal access to reliable information, regardless of socioeconomic status.

Finally, text classification contributes to Goal 9: Industry, Innovation, and Infrastructure by helping organizations process large volumes of textual data efficiently. In fields like healthcare, law, and environmental research, AI can be used to categorize documents, policies, and case studies, streamlining knowledge management and supporting data-driven decision-making. While this project focuses on movie classification, the same principles can be applied to real-world challenges, demonstrating how AI can enhance productivity and support sustainable development across different industries.
