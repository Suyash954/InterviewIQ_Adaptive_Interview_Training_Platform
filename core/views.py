
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model

from .models import Question, Skill, Attempt

try:
    # Optional: only used if OPENAI_API_KEY is configured.
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled gracefully at runtime
    OpenAI = None


def home(request):
    """
    Home page: lists up to 25 questions, optionally filtered by skill.
    """
    skills = Skill.objects.order_by("name")

    skill_id = request.GET.get("skill")
    active_skill = None

    qs = Question.objects.select_related("skill").order_by("pk")
    if skill_id:
        active_skill = Skill.objects.filter(pk=skill_id).first()
        if active_skill:
            qs = qs.filter(skill=active_skill)

    # Limit to at most 25 questions in the current selection
    questions = list(qs[:25])

    # First question for a "start session" button
    first_question = questions[0] if questions else None

    # --- Simple adaptive summary based on recent attempts ---
    User = get_user_model()
    if request.user.is_authenticated:
        stats_user = request.user
    else:
        stats_user, _ = User.objects.get_or_create(
            username="demo_user",
            defaults={"email": "demo@example.com"},
        )

    recent_attempts = (
        Attempt.objects.filter(user=stats_user)
        .select_related("question__skill")
        .order_by("-created_at")[:50]
    )

    total_attempts = recent_attempts.count()
    avg_score = None
    best_skill_name = None
    weakest_skill_name = None

    if total_attempts:
        total_score = sum(a.score for a in recent_attempts if a.score is not None)
        scored_attempts = [a for a in recent_attempts if a.score is not None]
        if scored_attempts:
            avg_score = total_score / len(scored_attempts)

            # Aggregate by skill
            by_skill = {}
            for a in scored_attempts:
                skill = a.question.skill
                if not skill:
                    continue
                bucket = by_skill.setdefault(skill, [])
                bucket.append(a.score)

            if by_skill:
                # Compute average per skill
                skill_avgs = {
                    skill: (sum(scores) / len(scores))
                    for skill, scores in by_skill.items()
                }
                # Best and weakest based on average score
                best_skill = max(skill_avgs, key=skill_avgs.get)
                weakest_skill = min(skill_avgs, key=skill_avgs.get)
                best_skill_name = best_skill.name
                weakest_skill_name = weakest_skill.name

    # Simple "smart" suggestion: if we have a weakest skill, propose its first question.
    smart_skill = None
    smart_question = None
    if weakest_skill_name:
        smart_skill = Skill.objects.filter(name=weakest_skill_name).first()
        if smart_skill:
            smart_question = (
                Question.objects.filter(skill=smart_skill).order_by("pk").first()
            )

    return render(
        request,
        "home.html",
        {
            "questions": questions,
            "skills": skills,
            "active_skill": active_skill,
            "first_question": first_question,
            "total_attempts": total_attempts,
            "avg_score": avg_score,
            "best_skill_name": best_skill_name,
            "weakest_skill_name": weakest_skill_name,
            "smart_skill": smart_skill,
            "smart_question": smart_question,
        },
    )


def question_detail(request, pk):
    """
    Simple detail page for an individual question, with next-question navigation.
    """
    question = get_object_or_404(Question.objects.select_related("skill"), pk=pk)

    # All questions for this skill, ordered for "next question" navigation.
    same_skill_qs = Question.objects.filter(skill=question.skill).order_by("pk")
    next_q = same_skill_qs.filter(pk__gt=question.pk).first() or same_skill_qs.first()

    ai_feedback = None

    if request.method == "POST":
        action = request.POST.get("action") or "next"

        # Branch 1: ask the AI to critique the answer and stay on this page.
        if action == "ai":
            notes = (request.POST.get("notes") or "").strip()

            api_key = os.getenv("OPENAI_API_KEY")
            if not OpenAI or not api_key:
                ai_feedback = (
                    "AI feedback is not configured yet. "
                    "Set the OPENAI_API_KEY environment variable to enable this feature."
                )
            elif not notes:
                ai_feedback = "Please type your answer in the notes box before asking for AI feedback."
            else:
                try:
                    client = OpenAI(api_key=api_key)
                    prompt = (
                        "You are a senior interview coach. A candidate is practicing an interview question.\n\n"
                        f"Question:\n{question.question_text}\n\n"
                        f"Skill area: {question.skill.name if question.skill else 'General'}\n"
                        f"Difficulty: {question.difficulty}\n\n"
                        "Candidate's rough answer / notes:\n"
                        f"{notes}\n\n"
                        "Give concise, helpful feedback:\n"
                        "- Point out strengths.\n"
                        "- Point out specific gaps or mistakes.\n"
                        "- Suggest how to structure a stronger answer.\n"
                        "- End with a suggested score from 1–10.\n"
                    )

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "You are an honest, constructive interview coach."},
                            {"role": "user", "content": prompt},
                        ],
                    )
                    ai_feedback = response.choices[0].message.content
                except Exception as exc:  # pragma: no cover - defensive
                    ai_feedback = f"Sorry, AI feedback failed: {exc}"

        # Branch 2: normal flow – save score and advance to the next question.
        else:
            # Persist an Attempt so the platform can learn from the user over time.
            score_raw = request.POST.get("score")
            try:
                score = int(score_raw) if score_raw is not None else None
            except (TypeError, ValueError):
                score = None

            if score is not None:
                User = get_user_model()
                if request.user.is_authenticated:
                    user = request.user
                else:
                    # Fallback demo user for anonymous sessions.
                    user, _ = User.objects.get_or_create(
                        username="demo_user",
                        defaults={"email": "demo@example.com"},
                    )

                Attempt.objects.create(user=user, question=question, score=score)

            # Move to the next question in the same skill, or back home if none.
            if next_q and next_q.pk != question.pk:
                return redirect("question_detail", pk=next_q.pk)
            return redirect("home")

    return render(
        request,
        "question_detail.html",
        {
            "question": question,
            "next_question": next_q,
            "ai_feedback": ai_feedback,
        },
    )
