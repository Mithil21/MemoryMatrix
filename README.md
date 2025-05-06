This is a RAG model developed from scratch using FIASS vector DB. This web app is used for unnecessary developing code from scratch. In an organization where we have to focus on Quality, testing is very important and major rounds of testing requires a lot of time. However, same functionality built in some other application can be reused and hence we can lessen the testing time and improve the quality.

How this works: -
Simple enough,
1. You have a use case document where you have to develop a functionality (consider login)
2. You upload the use case, and boom, our AI model does the magic.
3. The magic is it can provide you the extact code from the past applications which are tried and tested so you dont have to keep on writing the same code over and over again.

Major Files Used: -
1. Main.py ==> This is the main file for the backend to work
2. app.py ==> This is the main file for the UI to work

NOTE: - We use streamlit and flask as our primary for frontend and backend respectively.
crawler.py ==> used to fetching code from the repo
file_parser.py ==> can part files like txt, docx, etc
extract_dataset.py ==> Creates the dataset snippets.json
code_retriever.py ==> calls the fiass DB to fetch the necessary resources
build_index.py ==> used to build indexes (code_index.fiass and code_metadata.json)
