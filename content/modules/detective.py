import os
import glob

class Detective:
    """
    Scans the local directory to synthesize brand context.
    """
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.brand_context = {}

    def analyze(self):
        # Scan for markdown files in root and findings/ docs/
        context_files = [
            os.path.join(self.root_dir, "project-instructions.md"),
            os.path.join(self.root_dir, "findings/site_snapshot.md"),
            os.path.join(self.root_dir, "docs/OPERATIONAL_GUIDE.md")
        ]
        
        full_text = ""
        for file_path in context_files:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    full_text += f"\n--- Source: {os.path.basename(file_path)} ---\n"
                    full_text += f.read()
        
        # Hardcoded extraction for now (in a real scenario, this could be an LLM summary)
        self.brand_context['name'] = "Benefills"
        self.brand_context['website'] = "benefills.com"
        self.brand_context['colors'] = ["Purple", "White"]
        self.brand_context['topics'] = ["Thyroid Health", "Functional Foods", "Metabolism", "Energy"]
        self.brand_context['raw_data'] = full_text
        
        return self.brand_context

if __name__ == "__main__":
    detective = Detective(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    print(detective.analyze()['name'])
