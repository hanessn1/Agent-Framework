from llm.chat import ChatLLM
from planner.plan import Plan, TaskStep
from agent.messages import MessageHistory
import logging
import json

logger = logging.getLogger(__name__)


class Planner:
    def __init__(self, llm: ChatLLM):
        self.llm = llm

    def create_plan(self, goal: str) -> Plan:
        logger.debug(f"Generating plan for goal: `{goal}`")

        system_prompt = (
            "You are a Strategic Task Planner. "
            "Your job is to deconstruct user goals into a logical sequence of step-by-step instructions. "
            "Respond ONLY in valid JSON matching the requested schema."
        )
        history=MessageHistory(system_prompt=system_prompt)

        user_prompt = f"""Deconstruct the following goal into a sequence of steps.

Goal: "{goal}"

Respond ONLY with a valid JSON object matching this schema:
{{
    "goal": "{goal}",
    "steps": [
        "Step 1 description",
        "Step 2 description"
    ]
}}"""

        history.add_user(user_prompt)

        response = self.llm.complete(
            messages=history,
            stream=False
        )

        try:
            content = response.content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1].split("```")[0].strip()
            elif content.startswith("```"):
                content = content.split("```")[1].split("```")[0].strip()

            data = json.loads(content)
            steps_list = data.get("steps") or data.get("Steps") or []
            steps = [
                TaskStep(id=i + 1, description=desc)
                for i, desc in enumerate(steps_list)
            ]

            # Fallback when llm creates 0 steps
            if len(steps) == 0:
                logger.warning("Planner returned 0 steps. Using default fallback steps.")
                steps = [
                    TaskStep(id=1, description=f"Gather information to achieve: {goal}"),
                    TaskStep(id=2, description="Analyze results and provide final answer."),
                ]
            
            plan = Plan(goal=goal, steps=steps)
            logger.debug(plan)
            logger.info(f"Plan created with {len(steps)} step(s).")
            return plan
        except Exception as e:
            logger.warning(
                f"Failed to parse JSON plan: {e}. Falling back to single step."
            )
            return Plan(goal=goal, steps=[TaskStep(id=1, description=goal)])
