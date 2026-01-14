import asyncio
from src.core.requirement_parser import RequirementParser
from src.core.llm_engine import LLMEngine

async def main():
    # 1. Test Parsing (Create a dummy file first)
    with open("test_reqs.txt", "w") as f:
        f.write("The system shall allow users to login with email and password. Password must be 8 chars.")
    
    parser = RequirementParser()
    doc = await parser.parse("test_reqs.txt")
    print(f"✅ Parsed: {doc.filename} ({doc.char_count} chars)")
    
    # 2. Test LLM
    llm = LLMEngine()
    tests = await llm.generate_test_cases(doc.content)
    print(f"✅ Generated {len(tests)} Test Cases:")
    print(tests[0])

if __name__ == "__main__":
    asyncio.run(main())
