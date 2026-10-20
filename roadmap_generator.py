ROADMAP_TOPICS = {
    "python": "Practice Python fundamentals, functions, OOP, file handling, and problem solving.",
    "java": "Learn Java syntax, OOP concepts, collections, exception handling, and basic projects.",
    "c++": "Practice C++ syntax, OOP, STL, data structures, and problem solving.",
    "c#": "Learn C# fundamentals, OOP, .NET basics, and application development.",
    "javascript": "Learn JavaScript fundamentals, DOM manipulation, ES6, and asynchronous programming.",
    "sql": "Learn SELECT queries, filtering, joins, aggregation, subqueries, and database design.",
    "mysql": "Practice database creation, CRUD operations, joins, indexes, and normalization using MySQL.",
    "postgresql": "Learn PostgreSQL queries, joins, indexes, constraints, and database design.",
    "mongodb": "Learn NoSQL concepts, document design, CRUD operations, aggregation, and MongoDB queries.",
    "excel": "Practice formulas, pivot tables, charts, lookup functions, and data cleaning in Excel.",
    "power bi": "Build dashboards, create data models, use DAX basics, and design business reports.",
    "tableau": "Learn Tableau dashboards, calculated fields, filters, parameters, and data storytelling.",
    "pandas": "Practice data loading, cleaning, grouping, merging, and analysis using Pandas.",
    "numpy": "Learn arrays, vectorized operations, broadcasting, and numerical calculations using NumPy.",
    "machine learning": "Study supervised learning, unsupervised learning, evaluation metrics, and model validation.",
    "deep learning": "Learn neural networks, backpropagation, CNNs, RNNs, and deep learning workflows.",
    "scikit-learn": "Build classification and regression models using scikit-learn and evaluate them properly.",
    "tensorflow": "Learn TensorFlow tensors, neural networks, model training, and deployment basics.",
    "pytorch": "Practice PyTorch tensors, datasets, neural networks, training loops, and model evaluation.",
    "nlp": "Learn text cleaning, tokenization, vectorization, classification, and language-model basics.",
    "transformers": "Study attention, transformer architecture, fine-tuning, and transformer-based NLP tasks.",
    "hugging face": "Practice using Hugging Face pipelines, tokenizers, datasets, and pretrained models.",
    "llm": "Learn large language model concepts, prompting, embeddings, fine-tuning, and evaluation.",
    "rag": "Learn embeddings, vector databases, retrieval, chunking, and Retrieval-Augmented Generation.",
    "opencv": "Practice image loading, transformations, filtering, edge detection, and object detection basics.",
    "cnn": "Learn convolutional neural networks, image classification, pooling, and transfer learning.",
    "yolo": "Learn YOLO object detection, dataset labeling, model training, inference, and evaluation.",
    "fastapi": "Build REST APIs, define endpoints, validate input with Pydantic, and test API responses.",
    "flask": "Learn Flask routing, templates, request handling, REST APIs, and basic deployment.",
    "docker": "Learn Docker images, containers, Dockerfiles, volumes, networks, and container deployment.",
    "aws": "Learn cloud basics, IAM, EC2, S3, deployment workflows, and security fundamentals.",
    "azure": "Learn Azure fundamentals, virtual machines, storage, app services, and cloud deployment.",
    "mlflow": "Practice experiment tracking, model logging, model registry, and reproducible ML workflows.",
    "git": "Learn Git add, commit, branch, merge, pull, push, and collaborative workflows.",
    "github": "Create repositories, use pull requests, manage issues, and publish project documentation.",
    "apis": "Learn REST API principles, HTTP methods, JSON, authentication, and API integration.",
}


def generate_roadmap(missing_skills):
    """
    Generate a weekly roadmap based on missing skills.

    Each missing skill gets one suggested learning week.
    """
    roadmap = []

    for week_number, skill in enumerate(missing_skills, start=1):
        learning_topic = ROADMAP_TOPICS.get(
            skill.lower(),
            f"Learn the fundamentals of {skill.title()} and create a small practice project.",
        )

        roadmap.append(
            {
                "week": week_number,
                "skill": skill,
                "learning_topic": learning_topic,
            }
        )

    return roadmap