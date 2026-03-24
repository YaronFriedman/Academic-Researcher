"""Run 8 medium multi-turn sessions (2-3 turns) with varying performance."""

import asyncio
import dotenv

dotenv.load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types
from academic_research.agent import root_agent

SESSIONS = [
    # 1 - GOOD: clean 3-turn on a real paper
    [
        'Analyze "Dropout: A Simple Way to Prevent Neural Networks from Overfitting" by Srivastava et al. 2014.',
        'Find recent papers citing Dropout and suggest future research directions.',
        'Which of these directions has the most potential for practical impact?',
    ],

    # 2 - BAD: user gives wrong info, agent may hallucinate
    [
        'Analyze the paper "GPT-5: Scaling Laws Beyond Reason" by OpenAI, 2024. Give me all details.',
        'Find papers citing it and suggest directions.',
    ],

    # 3 - GOOD: well-known paper, 2 turns
    [
        'Analyze "Long Short-Term Memory" by Hochreiter and Schmidhuber 1997.',
        'Search for recent papers citing LSTM and suggest new research directions.',
    ],

    # 4 - BAD: contradictory / confusing multi-turn
    [
        'Analyze "Attention Is All You Need" by Vaswani et al. 2017.',
        'Actually never mind that paper. Instead analyze "BERT" by Devlin. But also keep the transformer analysis.',
        'Now find papers that cite both of them together and suggest directions.',
    ],

    # 5 - GOOD: specific and focused, 3 turns
    [
        'Analyze "Mastering the Game of Go with Deep Neural Networks and Tree Search" by Silver et al. 2016 (AlphaGo paper).',
        'Find recent papers citing AlphaGo in the context of protein folding or drug discovery.',
        'Suggest research directions at the intersection of game-playing AI and scientific discovery.',
    ],

    # 6 - BAD: user is unhelpful / gives minimal info
    [
        'analyze a paper',
        'the one about neural networks',
        'just find some papers I guess',
    ],

    # 7 - MEDIUM: real paper but niche, might get sparse results
    [
        'Analyze "Connectionist Temporal Classification" by Graves et al. 2006. Full analysis.',
        'Find recent 2025 papers citing CTC in speech recognition and suggest future research.',
    ],

    # 8 - GOOD but CHALLENGING: cross-domain request
    [
        'Analyze "Deep Learning" by LeCun, Bengio, and Hinton, Nature 2015. This is the famous review paper.',
        'Find recent papers that cite this review specifically in the context of climate science and weather prediction.',
        'Suggest research directions for applying deep learning to environmental sustainability based on what you found.',
    ],
]


async def run_session(messages: list[str], index: int):
    print(f"\n{'='*60}")
    print(f"SESSION {index+1}/{len(SESSIONS)}: {messages[0][:70]}...")
    print(f"{'='*60}")

    runner = InMemoryRunner(agent=root_agent, app_name="academic-research")
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="demo_user"
    )

    for turn, prompt in enumerate(messages):
        print(f"\n  --- Turn {turn+1}: {prompt[:80]}...")
        msg = types.Content(parts=[types.Part(text=prompt)])
        try:
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=msg,
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if part.text:
                            preview = part.text[:120].replace("\n", " ")
                            print(f"    [{event.author}] {preview}...")
        except Exception as e:
            print(f"    ERROR: {e}")

    print(f"\n  SESSION {index+1} DONE")


async def main():
    for i, messages in enumerate(SESSIONS):
        await run_session(messages, i)
    print(f"\n{'='*60}")
    print("ALL 8 SESSIONS COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
