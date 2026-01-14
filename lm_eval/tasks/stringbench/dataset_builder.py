"""Dataset builder for StringBench.

StringLLM: Understanding the String Processing Capability of Large Language Models
Paper: https://arxiv.org/abs/2410.01208 (ICLR 2025)
Authors: Xilong Wang, Hao Fu, Jindong Wang, Neil Zhenqiang Gong

Data source: https://github.com/wxl-lxw/StringLLM
"""

import json
import os
import re
from typing import List, Dict, Optional


def execute_solution(solution_code: str, variables: Dict) -> str:
    """Execute the Python solution code to get the answer.
    
    The solution code defines 'answer' based on variables.
    """
    # Clean up the code
    code = solution_code.replace('```python', '').replace('```', '').strip()
    
    # Remove print statement if present
    code = re.sub(r'print\s*\(.*\)', '', code).strip()
    
    # Create execution environment with variables
    local_vars = dict(variables)
    
    try:
        exec(code, {}, local_vars)
        return str(local_vars.get('answer', ''))
    except Exception as e:
        return f"ERROR: {e}"


def format_query(query_template: str, variables: Dict) -> str:
    """Format the query template with variable values."""
    result = query_template
    
    for key, value in variables.items():
        # Handle special cases like {x+1}
        result = result.replace(f'{{{key}+1}}', str(value + 1) if isinstance(value, int) else str(value))
        result = result.replace(f'{{{key}}}', str(value))
    
    return result


def load_stringbench(
    string_type: str = "hash",  # "hash", "multilingual", "random_string"
    task_filter: Optional[str] = None,  # Filter by manipulation type
    limit: Optional[int] = None
) -> List[Dict]:
    """Load StringBench dataset.
    
    Args:
        string_type: Type of strings to test on
        task_filter: Optional filter for specific manipulation task
        limit: Optional limit on number of samples
    
    Returns:
        List of dicts with 'prompt' and 'answer' keys
    """
    data_path = f"/home/StringLLM/data/test/{string_type}.json"
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"StringBench data not found: {data_path}")
    
    with open(data_path, 'r') as f:
        raw_data = json.load(f)
    
    samples = []
    for item in raw_data:
        # Filter by task type if specified
        if task_filter:
            if 'manipulations' not in item or task_filter not in item['manipulations']:
                continue
        
        # Use the first query template
        query_template = item['query'][0]
        variables = item['variables']
        
        # Format the prompt
        prompt = format_query(query_template, variables)
        
        # Execute the solution to get the answer
        answer = execute_solution(item['solution'], variables)
        
        samples.append({
            'prompt': prompt,
            'answer': answer,
            'task': item.get('manipulations', ['unknown'])[0] if item.get('manipulations') else 'unknown'
        })
        
        if limit and len(samples) >= limit:
            break
    
    return samples


# Task groupings for easier evaluation
ATOMIC_TASKS = [
    'indexing',    # a[x]
    'slicing',     # a[x:y], a[:y]
    'length',      # len(a)
    'count',       # a.count(x)
    'contain',     # x in a
    'find',        # a.find(x)
    'reverse',     # a[::-1]
    'replace',     # a.replace(x, y)
    'lower',       # a.lower()
    'upper',       # a.upper()
    'startswith',  # a.startswith(x)
    'endswith',    # a.endswith(x)
    'strip',       # a.strip(x)
]

STRING_TYPES = ['hash', 'multilingual', 'random_string']
