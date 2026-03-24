"""Run long multi-turn sessions (40+ spans) for Deepchecks demo."""

import asyncio
import dotenv

dotenv.load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types
from academic_research.agent import root_agent

# Each session is a list of user messages — multi-turn to generate many spans
SESSIONS = [
    # Session 1: Deep multi-turn on Transformers
    [
        'Analyze "Attention Is All You Need" by Vaswani et al. 2017. Give me a full analysis with all authors, abstract, summary, key innovations, and references.',
        'Now use tool_websearch to find recent papers from 2025 that cite this work.',
        'Can you search again but focus on papers about efficient transformers and linear attention mechanisms?',
        'Now use tool_newresearch to suggest future research directions based on everything we found.',
        'Can you elaborate on direction number 1? Search for more papers related to that specific direction.',
        'Suggest additional research directions but this time focused on transformers for computer vision.',
    ],

    # Session 2: BERT deep dive with multiple searches
    [
        'I want to analyze "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" by Devlin et al. 2019. Full analysis please.',
        'Search for recent papers that cite BERT in the context of healthcare and biomedical NLP.',
        'Now search for papers that cite BERT in the context of multilingual and cross-lingual transfer learning.',
        'Search for papers about BERT fine-tuning techniques and adapter methods from 2025.',
        'Based on all the citing papers we found across healthcare, multilingual, and fine-tuning, suggest comprehensive future research directions.',
        'Can you suggest more research directions specifically about combining BERT with retrieval-augmented generation?',
    ],

    # Session 3: GANs with iterative refinement
    [
        'Analyze "Generative Adversarial Nets" by Goodfellow et al. 2014. Include all details.',
        'Find recent papers citing GANs in image generation and synthesis.',
        'Now search for papers about GANs vs diffusion models comparisons published in 2025.',
        'Search for papers about conditional GANs and their applications in medical imaging.',
        'Suggest future research directions based on all the GAN-related papers we found.',
        'Now search for papers about GAN training stability and mode collapse solutions.',
        'Update the research directions to include what we just found about training stability.',
    ],

    # Session 4: Reinforcement learning exploration
    [
        'Analyze "Human-level control through deep reinforcement learning" by Mnih et al. 2015 (the Nature DQN paper). Full analysis.',
        'Search for recent papers citing this work in robotics applications.',
        'Search for papers about model-based reinforcement learning that cite this work.',
        'Now search for papers about reinforcement learning from human feedback (RLHF) that reference DQN.',
        'Suggest future research directions combining all findings from robotics, model-based RL, and RLHF.',
        'Search for papers about safe reinforcement learning and suggest how it connects to the directions you proposed.',
    ],

    # Session 5: Word embeddings to modern LLMs journey
    [
        'Analyze "Efficient Estimation of Word Representations in Vector Space" (Word2Vec) by Mikolov et al. 2013.',
        'Find recent papers that still cite Word2Vec in 2025.',
        'Now search for papers comparing Word2Vec with modern contextual embeddings from large language models.',
        'Search for papers about word embeddings in low-resource languages from 2025.',
        'Suggest research directions based on the gap between classic word embeddings and modern LLM representations.',
        'Search for papers about embedding spaces and geometric properties of language representations.',
        'Give me a final comprehensive list of all research directions combining everything we discussed.',
    ],
]


async def run_multi_turn_session(messages: list[str], session_index: int):
    print(f"\n{'='*60}")
    print(f"LONG SESSION {session_index+1}/{len(SESSIONS)}")
    print(f"{'='*60}")

    runner = InMemoryRunner(agent=root_agent, app_name="academic-research")
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="demo_user"
    )

    for turn, prompt in enumerate(messages):
        print(f"\n  --- Turn {turn+1}/{len(messages)}: {prompt[:80]}...")
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

    print(f"\n  LONG SESSION {session_index+1} DONE")


async def main():
    for i, messages in enumerate(SESSIONS):
        await run_multi_turn_session(messages, i)
    print(f"\n{'='*60}")
    print("ALL LONG SESSIONS COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
