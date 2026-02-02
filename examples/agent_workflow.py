#!/usr/bin/env python3
"""
DONGOL Agent Workflow Example

Demonstrates how AI agents can use DONGOL for complex reasoning tasks.
"""
import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Chunk, Task, Priority


class AgentReasoning:
    """
    Simulated AI Agent using DONGOL for parallel reasoning
    """
    
    def __init__(self, engine: DongolEngine):
        self.engine = engine
        self.thoughts: List[Dict] = []
        
    async def analyze_problem(self, problem: str) -> Dict[str, Any]:
        """
        Multi-perspective parallel analysis of a problem
        """
        print(f"\n🤖 Agent analyzing: {problem[:60]}...")
        
        # Define multiple thinking strategies
        perspectives = [
            ("systematic", "Analyze systematically: breakdown components, identify dependencies"),
            ("creative", "Think creatively: consider novel approaches, lateral thinking"),
            ("critical", "Critical analysis: identify risks, constraints, edge cases"),
            ("historical", "Historical context: similar problems and their solutions"),
            ("futures", "Future impact: long-term consequences and scalability"),
        ]
        
        async def perspective_handler(chunk: Chunk) -> Dict:
            """Process each perspective in parallel"""
            perspective_type, prompt = chunk.content
            
            # Simulate LLM reasoning (replace with actual LLM call)
            await asyncio.sleep(0.05)
            
            insights = self._generate_insights(perspective_type, prompt, problem)
            
            return {
                "perspective": perspective_type,
                "insights": insights,
                "confidence": 0.7 + (hash(perspective_type) % 20) / 100,
                "reasoning_chain": [prompt, f"Analysis from {perspective_type} view"]
            }
        
        self.engine.register_handler("perspective", perspective_handler)
        
        # Create parallel thinking task
        task = Task(
            name="Multi-Perspective Analysis",
            chunks=[
                Chunk(content=p, tags={"perspective", p[0]}, priority=priority)
                for p, priority in zip(perspectives, [
                    Priority.HIGH, Priority.NORMAL, Priority.HIGH, 
                    Priority.NORMAL, Priority.NORMAL
                ])
            ],
            parallel_mode=True,
            max_workers=len(perspectives)
        )
        
        self.engine.tasks[task.id] = task
        
        # Execute all perspectives in parallel
        result = await self.engine.execute_task(task.id, "perspective")
        
        # Synthesize results
        synthesis = self._synthesize_thoughts(result.results)
        
        return {
            "task_id": task.id,
            "problem": problem,
            "perspectives": result.results,
            "synthesis": synthesis,
            "duration_ms": result.duration_ms,
            "recommendation": synthesis.get("recommended_approach", "unknown")
        }
    
    def _generate_insights(self, perspective: str, prompt: str, problem: str) -> List[str]:
        """Generate insights for a perspective (simulated)"""
        insights_map = {
            "systematic": [
                "Problem decomposes into 3 core components",
                "Dependencies exist between modules A and B",
                "Sequential execution required for critical path"
            ],
            "creative": [
                "Consider unconventional data structure",
                "Borrow pattern from biological systems",
                "Invert the problem constraints"
            ],
            "critical": [
                "Risk of data inconsistency under load",
                "Memory usage scales exponentially",
                "Edge case: empty input handling"
            ],
            "historical": [
                "Similar to graph traversal problems",
                "Pattern matches distributed consensus",
                "Previous solutions used caching layers"
            ],
            "futures": [
                "Will need horizontal scaling in 6 months",
                "API design impacts future integrations",
                "Consider migration path for v2"
            ]
        }
        return insights_map.get(perspective, ["General insight"])
    
    def _synthesize_thoughts(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize multiple perspectives into coherent recommendation"""
        all_insights = []
        avg_confidence = 0
        
        for chunk_id, result in results.items():
            if isinstance(result, dict):
                all_insights.extend(result.get("insights", []))
                avg_confidence += result.get("confidence", 0)
        
        avg_confidence /= len(results) if results else 1
        
        # Generate synthesis
        return {
            "total_insights": len(all_insights),
            "average_confidence": round(avg_confidence, 2),
            "key_themes": ["scalability", "reliability", "maintainability"],
            "recommended_approach": "Hybrid approach combining systematic decomposition with creative caching",
            "risk_mitigation": "Implement circuit breakers and graceful degradation",
            "all_insights": all_insights
        }
    
    async def recursive_thinking(self, problem: str, depth: int = 2) -> Dict:
        """
        Recursive thinking - break down problems into sub-problems
        """
        if depth == 0:
            return await self.analyze_problem(problem)
        
        print(f"\n🔄 Recursive thinking at depth {depth}: {problem[:50]}...")
        
        # First, decompose the problem
        sub_problems = await self._decompose_problem(problem)
        
        # Analyze each sub-problem in parallel
        sub_results = []
        for sub in sub_problems:
            result = await self.recursive_thinking(sub, depth - 1)
            sub_results.append(result)
        
        # Synthesize sub-results
        return {
            "problem": problem,
            "depth": depth,
            "sub_problems": sub_results,
            "synthesis": self._merge_sub_results(sub_results)
        }
    
    async def _decompose_problem(self, problem: str) -> List[str]:
        """Decompose a problem into sub-problems"""
        # Simulated decomposition
        return [
            f"Sub-problem 1: Core logic of {problem[:30]}",
            f"Sub-problem 2: Data flow for {problem[:30]}",
            f"Sub-problem 3: Error handling for {problem[:30]}",
        ]
    
    def _merge_sub_results(self, results: List[Dict]) -> Dict:
        """Merge results from sub-problems"""
        return {
            "total_sub_problems": len(results),
            "aggregated_confidence": sum(
                r.get("synthesis", {}).get("average_confidence", 0) 
                for r in results
            ) / len(results) if results else 0,
            "status": "completed"
        }


async def main():
    """Demonstrate agent workflows"""
    print("🧠 DONGOL - Agent Workflow Demonstration")
    print("=" * 60)
    
    # Initialize engine
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    # Create agent
    agent = AgentReasoning(engine)
    
    # Example 1: Multi-perspective analysis
    problem = "How to design a fault-tolerant distributed task queue?"
    result = await agent.analyze_problem(problem)
    
    print("\n" + "=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    print(f"Problem: {result['problem']}")
    print(f"Duration: {result['duration_ms']:.2f}ms")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nSynthesis:")
    for key, value in result['synthesis'].items():
        if key != "all_insights":
            print(f"  {key}: {value}")
    
    # Example 2: Recursive thinking
    print("\n" + "=" * 60)
    print("RECURSIVE THINKING")
    print("=" * 60)
    
    complex_problem = "Design a self-healing microservices architecture"
    recursive_result = await agent.recursive_thinking(complex_problem, depth=2)
    
    print(f"\nRecursive analysis complete!")
    print(f"Total sub-problems analyzed: {recursive_result['synthesis']['total_sub_problems']}")
    print(f"Aggregated confidence: {recursive_result['synthesis']['aggregated_confidence']:.2f}")
    
    # Cleanup
    await engine.stop()
    
    print("\n" + "=" * 60)
    print("Agent workflow demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
