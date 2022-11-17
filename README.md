# STEPS TO REPRODUCE THE OUTPUT FILES
 - Clone the repo: git clone https://github.com/michaeliyke/pandas-questions.git
 - Change to the directory: cd pandas-questions
 - Make three folders: files, files/pages, out
 
### ACTUAL COMMANDS
 - python fetch.py
 - python extract.py
 - python generate-typos.py
 - python make_csv.py

Once all these execute successfully, your out directory contains two files:
 1. questions-data-typos.csv (input.csv)
 2. questions-data.csv (responses.csv)
 
Your files directory contains the following:
 1. answers-data.json (for insights)
 2. questions-data.json (for generating responses file)
 3. questions-data-typos.json (for generating input file)
 4. tagged-pandas-1.html (seed page 1)
 5. tagged-pandas-2.html (seed page 2)
 
Your files/pages directory now contains 100 HTML files. These HTML files and the ones above are merely for caching.
This avoids re-fetching the data for each run. These seed pages are two for now but can be increased to any number.
Each seed page contains exactly 50 questions or less. 

[PandaApp](https://colab.research.google.com/drive/1oCSWlX3d9NFa51OXvfk3jEfCbxq3MAaD?usp=sharing)
[markdown guide](https://www.markdownguide.org/cheat-sheet)