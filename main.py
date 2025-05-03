from flask import Flask, request, jsonify
from file_parser import parse_file
from code_retriever import CodeRetriever
from flask_cors import CORS
import traceback
import os

app = Flask(__name__)
CORS(app)  # Allows CORS for all routes

retriever = CodeRetriever()
# retriever.load_data()

@app.route('/search', methods=['POST'])
def startSearch():
    try:
        # Retrieve the uploaded file
        file = request.files.get("file")

        if file is None:
            print("No file provided.")
            return jsonify({"error": "No file provided."}), 400

        # Parse the file content
        use_case_text = parse_file(file)

        # Perform the search
        results = retriever.search(use_case_text)

        if not results:
            print("No relevant code snippets found.")
            return jsonify({"message": "No relevant code snippets found."}), 404

        # Format the results
        formatted_results = [
            {
                # "score": res.get("score", 0),
                "link": res.get("link", "N/A"),
                "code": res.get("code", "N/A")
            }
            for res in results
        ]

        return jsonify({"results": formatted_results}), 200

    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({"error": "An internal error occurred.", "details": str(e)}), 500
    
@app.route('/generate', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        usecase = data.get("usecase", "").strip()

        if not usecase:
            return jsonify({"error": "Use case is empty."}), 400

        retriever = CodeRetriever()
        results = retriever.search(usecase)

        if not results:
            return jsonify({"message": "No relevant code snippets found."}), 404

        # Choose the top result (highest ranked snippet)
        top_result = results[0]

        return jsonify({
            "code": top_result.get("code", ""),
            "link": top_result.get("link", "No Repo Info"),
            "score": top_result.get("score", 0)
        }), 200

    except Exception as e:
        print("An error occurred:", traceback.format_exc())
        return jsonify({"error": "Internal server error.", "details": str(e)}), 500
    
# @app.on_event("startup")
# def regenerate_index():
#     os.system("python build_index.py")

if __name__ == '__main__':
    app.run(debug=True)
