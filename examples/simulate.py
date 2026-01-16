from amp.models import UserInput, DecisionContext
from amp.agent import amp_agent_flow

user_input = UserInput(
    text="Devo partire per un viaggio di lavoro con solo uno zaino piccolo",
    context=DecisionContext(proximity_score=0.9),
)

print(amp_agent_flow(user_input))
