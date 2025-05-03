import os
import json
import shutil
from git import Repo
from tqdm import tqdm

# Relevant extensions to extract
TARGET_EXTENSIONS = {
    ".java": "java",
    ".ts": "typescript",
    ".html": "html",
    ".css": "css",
    ".xml": "xml",
    ".ftl": "freemarker"
}

OUTPUT_PATH = "data/snippets.json"
REPO_DIR = "repos"

def extract_tags_from_code(code: str) -> list:
    tags = []

    # Java Design Pattern Detection (Basic Heuristics)
    if "implements" in code or "@Override" in code:
        tags.append("interface")

    if "abstract class" in code:
        tags.append("abstract")

    if "private static" in code and "getInstance" in code:
        tags.append("singleton")

    if "new " in code and "(" in code and ")" in code:
        tags.append("factory")

    if "instanceof" in code or "switch" in code:
        tags.append("strategy")

    if "Observable" in code or "notifyObservers" in code:
        tags.append("observer")

    if "proxy" in code.lower():
        tags.append("proxy")

    if "SpringBootApplication" in code or "RestController" in code or "@Autowired" in code:
        tags.append("spring")

    if "dynamic" in code.lower():
        tags.append("dynamic")

    return list(set(tags))  # remove duplicates

def extract_code_from_repo(repo_path, repo_name, snippets):
    for root, _, files in os.walk(repo_path):
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext in TARGET_EXTENSIONS:
                try:
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8") as f:
                        code = f.read().strip()
                        if code:
                            tags = extract_tags_from_code(code)
                            snippets.append({
                                "repo_name": repo_name,
                                "language": TARGET_EXTENSIONS[ext],
                                "code": code,
                                "path": os.path.relpath(full_path, start=repo_path),
                                "tags": tags
                            })
                except Exception as e:
                    print(f"⚠️ Error reading {file}: {e}")

def crawl_repos(repo_urls):
    os.makedirs(REPO_DIR, exist_ok=True)
    os.makedirs("data", exist_ok=True)

    snippets = []

    for url in tqdm(repo_urls, desc="Cloning & crawling repos"):
        repo_name = url.rstrip("/").split("/")[-1]
        local_path = os.path.join(REPO_DIR, repo_name)

        try:
            print(f"🚀 Cloning {repo_name}")
            Repo.clone_from(url, local_path, depth=1)
            extract_code_from_repo(local_path, repo_name, snippets)
        except Exception as e:
            print(f"❌ Failed to clone {url}: {e}")
        finally:
            shutil.rmtree(local_path, ignore_errors=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(snippets, f, indent=2)

    print(f"\n✅ Done! Extracted {len(snippets)} code snippets into {OUTPUT_PATH}")

if __name__ == "__main__":
    repo_list = [
        # 🔸 Java Repos
        "https://github.com/spring-projects/spring-petclinic",
        "https://github.com/iluwatar/java-design-patterns",
        "https://github.com/eugenp/tutorials",
        "https://github.com/spring-guides/gs-spring-boot",
        "https://github.com/ThorbenJ/dynamic-spring-security",

        # 🔸 Angular / Frontend Repos
        "https://github.com/angular/components",
        "https://github.com/gothinkster/angular-realworld-example-app",
        "https://github.com/akveo/nebular",
        "https://github.com/NG-ZORRO/ng-zorro-antd",

        # 🔸 Full-stack Java + Angular
        "https://github.com/amigoscode/spring-boot-fullstack-professional",
        "https://github.com/bezkoder/angular-11-spring-boot-crud",
        "https://github.com/wandri/chat-spring-kafka-angular-react-vue",
        "https://github.com/in28minutes/full-stack-with-angular-and-spring-boot",

"https://github.com/56duong/angular-springboot-blog-webapp",

"https://github.com/PSAMEERKHAN/HealthCare-Appointment",

"https://github.com/RameshMF/Angular-10-Spring-Boot-CRUD-Full-Stack-App",

"https://github.com/iluwatar/java-design-patterns",
"https://github.com/springframeworkguru/sfg-pet-clinic",
"https://github.com/darbyluv2code/fullstack-angular-and-springboot",
"https://github.com/mechero/full-reactive-stack",
"https://github.com/bfwg/angular-spring-starter",
"https://github.com/wkrzywiec/kanban-board",
"https://github.com/in28minutes/spring-boot-angular-fullstack-examples",
"https://github.com/Java-Techie-jt/springboot-docker-ecs",
"https://github.com/in28minutes/spring-boot-to-cloud"
    ]

    crawl_repos(repo_list)
