from flask import Flask, request, render_template, redirect, url_for, flash
from processor.pipeline import build_pipeline
from processor.types import State
import nest_asyncio
import os
from langchain_core.runnables.graph import MermaidDrawMethod

app = Flask(__name__)
app.secret_key = os.urandom(24)
nest_asyncio.apply()

# Get both compiled pipeline and builder to access .get_graph()
pipeline, builder = build_pipeline()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note")
        if not note.strip():
            flash("Please enter a clinical note.", "error")
            return redirect(url_for("index"))

        result = pipeline.invoke({"note": note})

        # FIXED – get the graph first, then call draw_mermaid_png without parameters
        graph = pipeline.get_graph()
        img_bytes = graph.draw_mermaid_png()

        # Create static directory if it doesn't exist
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        
        graph_output_path = os.path.join(static_dir, "langgraph.png")
        with open(graph_output_path, "wb") as f:
            f.write(img_bytes)

        return render_template("results.html", result=result, graph_path="langgraph.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)