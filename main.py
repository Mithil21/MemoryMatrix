from flask import Flask, request, jsonify
from file_parser import parse_file
from code_retriever import CodeRetriever
from flask_cors import CORS
import traceback
from summarizer import Summarizer
from code_explainer import CodeExplainer  # Import the code explainer

app = Flask(__name__)
CORS(app)  # Allows CORS for all routes

# Initialize models
retriever = CodeRetriever()
summarize = Summarizer()
explainer = CodeExplainer()  # Initialize code explainer

@app.route('/search', methods=['POST'])
def startSearch():
    try:
        file = request.files.get("file")

        if file is None:
            print("No file provided.")
            return jsonify({"error": "No file provided."}), 400

        # Parse and summarize the file
        use_case_text = parse_file(file)
        summarized_text = summarize.summarize(use_case_text)
        print("Summarized text:", summarized_text)

        # Retrieve relevant code snippets based on summarized text
        retrieved_snippets = retriever.search(summarized_text)

        if not retrieved_snippets:
            print("No relevant code snippets found.")
            return jsonify({"message": "No relevant code snippets found."}), 404

        formatted_results = [
    {
        "link": res.get("link", "N/A"),
        "code": res.get("code", "N/A"),
        "language": res.get("language", "Unknown"),
        "explanation": res.get("explanation", "No explanation available.")
    }
    for res in retrieved_snippets
]

        return jsonify({
            "results": formatted_results,
            "summarized_use_case": summarized_text
        }), 200


    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)