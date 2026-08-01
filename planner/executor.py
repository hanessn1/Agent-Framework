from agent.agent import Agent
from planner.plan import Plan
import logging

logger=logging.getLogger(__name__)


class Executor:
    def __init__(self, agent:Agent):
        self.agent=agent

    def execute_plan(self,plan:Plan)->str:
        logger.info(f"Executing Plan for Goal: '{plan.goal}'")
        print(f"\n==========================================")
        print(f"🎯 GOAL: {plan.goal}")
        print(f"📋 Total Steps: {len(plan.steps)}")
        print(f"==========================================")

        logger.info(f"\n==========================================")
        logger.info(f"🎯 GOAL: {plan.goal}")
        logger.info(f"📋 Total Steps: {len(plan.steps)}")
        logger.info(f"==========================================")

        final_summary=[]

        while not plan.is_complete():
            step=plan.get_next_step()
            if not step:
                break

            step.status="running"
            print(f"\n⏳ [Step {step.id}/{len(plan.steps)}] {step.description}...")
            logger.info(f"\n⏳ [Step {step.id}/{len(plan.steps)}] {step.description}...")

            # Pass the step to existing agent ReAct loop
            step_prompt=(
                f"Overall Goal: `{plan.goal}`."
                f"Your current task is step {step.id}: `{step.description}`."
            )
            result=self.agent.run(step_prompt)

            step.status="completed"
            step.result=str(result)
            final_summary.append(f"Step {step.id} ({step.description}):\n{result}")
            print(f"✅ [Step {step.id}] Completed!")
            logger.info(f"✅ [Step {step.id}] Completed!")

        print(f"\n🎉 All steps completed successfully!\n")
        logger.info(f"\n🎉 All steps completed successfully!\n")
        return "\n\n".join(final_summary)