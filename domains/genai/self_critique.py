class SelfCritique:
    """
    Uses the LLM to critique its own answer.
    """

    def build_critique_prompt(self, question, answer, context):
        return f"""
You are a strict evaluator.

Question:
{question}

Context:
{context}

Answer:
{answer}

Evaluate strictly:
If the answer contains hallucinations or is unsupported, respond ONLY with: UNSAFE
Otherwise respond ONLY with: SAFE
"""

    def evaluate(self, llm_model, question, answer, context):
        critique_prompt = self.build_critique_prompt(
            question,
            answer,
            context
        )

        critique_text = llm_model.generate(
            critique_prompt,
            temperature=0.1
        )

        critique_text_upper = critique_text.upper()

        # Balanced logic: only explicit UNSAFE fails
        is_safe = "UNSAFE" not in critique_text_upper

        return {
            "critique_text": critique_text,
            "is_safe": is_safe
        }
