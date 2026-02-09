from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core.models import Skill, Question, Attempt


class Command(BaseCommand):
    help = "Seed the database with sample skills, questions, and attempts."

    def handle(self, *args, **options):
        User = get_user_model()

        # Create or get a demo user
        user, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"},
        )

        # Create skills
        skill_names = [
            "Data Structures",
            "Algorithms",
            "System Design",
            "Behavioral",
        ]
        skills = {}
        for name in skill_names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill

        # Create questions (50+ high‑leverage questions across skills)
        questions_data = [
            # Data Structures (DSA)
            (
                "Explain the difference between arrays and linked lists. When would you choose one over the other?",
                "Data Structures",
                "easy",
            ),
            (
                "Describe how a hash table works, including how collisions are handled and typical time complexities.",
                "Data Structures",
                "medium",
            ),
            (
                "What is the difference between a stack and a queue? Give a real‑world example of each.",
                "Data Structures",
                "easy",
            ),
            (
                "Compare binary search trees, AVL trees, and red‑black trees in terms of balancing and performance.",
                "Data Structures",
                "medium",
            ),
            (
                "Explain how a binary heap is implemented and how it supports priority queue operations.",
                "Data Structures",
                "medium",
            ),
            (
                "What is the difference between depth‑first search (DFS) and breadth‑first search (BFS) on graphs?",
                "Data Structures",
                "easy",
            ),
            (
                "How would you detect a cycle in a linked list? Discuss time and space complexity.",
                "Data Structures",
                "medium",
            ),
            (
                "Explain the concept of dynamic arrays (array lists). How do they grow and what is the amortized cost of insertion?",
                "Data Structures",
                "medium",
            ),
            (
                "Design a data structure to implement an LRU (Least Recently Used) cache.",
                "Data Structures",
                "hard",
            ),
            (
                "How would you represent a graph in memory? Compare adjacency matrix and adjacency list.",
                "Data Structures",
                "easy",
            ),
            (
                "What is a trie (prefix tree) and when is it useful?",
                "Data Structures",
                "medium",
            ),
            (
                "Explain the difference between shallow copy and deep copy for complex data structures.",
                "Data Structures",
                "easy",
            ),
            (
                "How do you find the kth smallest element in an unsorted array? Describe at least two approaches.",
                "Data Structures",
                "hard",
            ),
            (
                "What are union‑find (disjoint set) data structures and where are they used?",
                "Data Structures",
                "medium",
            ),
            (
                "Explain the concept of a segment tree and one problem it can solve efficiently.",
                "Data Structures",
                "hard",
            ),

            # Algorithms
            (
                "Given a sorted array, how would you implement binary search? What is its time complexity?",
                "Algorithms",
                "easy",
            ),
            (
                "Compare time and space complexity of merge sort, quicksort, and bubble sort.",
                "Algorithms",
                "medium",
            ),
            (
                "Explain the two‑pointer technique and give an example problem where it is useful.",
                "Algorithms",
                "easy",
            ),
            (
                "What is dynamic programming? Explain with an example such as Fibonacci or knapsack.",
                "Algorithms",
                "medium",
            ),
            (
                "How would you detect if a string is a permutation of a palindrome?",
                "Algorithms",
                "medium",
            ),
            (
                "Describe Dijkstra’s algorithm for shortest paths. What are its time complexities with different data structures?",
                "Algorithms",
                "hard",
            ),
            (
                "Explain the difference between greedy algorithms and dynamic programming.",
                "Algorithms",
                "medium",
            ),
            (
                "How would you check if a binary tree is height‑balanced?",
                "Algorithms",
                "medium",
            ),
            (
                "Given an array, find the maximum subarray sum. Describe Kadane’s algorithm.",
                "Algorithms",
                "easy",
            ),
            (
                "What is backtracking? Explain with an example such as generating permutations or solving N‑Queens.",
                "Algorithms",
                "medium",
            ),
            (
                "Explain big‑O, big‑Theta, and big‑Omega notation with examples.",
                "Algorithms",
                "easy",
            ),
            (
                "How would you detect if two line segments intersect in 2D space?",
                "Algorithms",
                "hard",
            ),

            # Python‑specific
            (
                "Explain the difference between lists, tuples, sets, and dictionaries in Python and when to use each.",
                "Behavioral",
                "easy",
            ),
            (
                "How does Python’s list slicing work, and what is its complexity?",
                "Behavioral",
                "medium",
            ),
            (
                "What is a list comprehension in Python and how does it differ from a normal for‑loop?",
                "Behavioral",
                "easy",
            ),
            (
                "Explain how Python’s garbage collection and reference counting work at a high level.",
                "Behavioral",
                "medium",
            ),
            (
                "What are decorators in Python and when might you use them?",
                "Behavioral",
                "medium",
            ),
            (
                "Describe the difference between `@staticmethod`, `@classmethod`, and instance methods.",
                "Behavioral",
                "medium",
            ),
            (
                "How would you handle exceptions in Python? Explain `try/except/else/finally`.",
                "Behavioral",
                "easy",
            ),
            (
                "Explain the concept of generators in Python and how they differ from normal functions.",
                "Behavioral",
                "medium",
            ),
            (
                "What are virtual environments in Python and why are they important?",
                "Behavioral",
                "easy",
            ),
            (
                "How does Python’s GIL (Global Interpreter Lock) affect multithreading?",
                "Behavioral",
                "hard",
            ),

            # System Design
            (
                "Design a URL shortener service. What components and data model would you use?",
                "System Design",
                "hard",
            ),
            (
                "How would you design a system like Instagram’s news feed?",
                "System Design",
                "hard",
            ),
            (
                "Explain how you would design a rate limiter for an API.",
                "System Design",
                "medium",
            ),
            (
                "Describe how you would design a distributed caching layer for a web application.",
                "System Design",
                "medium",
            ),
            (
                "What is sharding and how would you shard a large relational database?",
                "System Design",
                "hard",
            ),
            (
                "Explain the difference between vertical and horizontal scaling with examples.",
                "System Design",
                "easy",
            ),

            # Behavioral / General
            (
                "Tell me about a time you had to quickly learn a new technology to deliver a project.",
                "Behavioral",
                "easy",
            ),
            (
                "Describe a challenging bug you fixed. How did you approach debugging it?",
                "Behavioral",
                "medium",
            ),
            (
                "Tell me about a time you disagreed with a teammate or manager. How did you handle it?",
                "Behavioral",
                "medium",
            ),
            (
                "Describe a project where you had to balance short‑term delivery with long‑term code quality.",
                "Behavioral",
                "medium",
            ),
            (
                "Give an example of a time you improved the performance or reliability of a system.",
                "Behavioral",
                "hard",
            ),
        ]

        created_questions = []
        for text, skill_name, difficulty in questions_data:
            question, _ = Question.objects.get_or_create(
                question_text=text,
                skill=skills[skill_name],
                defaults={"difficulty": difficulty},
            )
            created_questions.append(question)

        # Create a few attempts for the demo user
        for idx, question in enumerate(created_questions, start=1):
            Attempt.objects.get_or_create(
                user=user,
                question=question,
                defaults={"score": 60 + idx * 10},
            )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))

