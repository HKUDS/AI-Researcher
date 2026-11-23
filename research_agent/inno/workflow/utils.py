from typing import Dict
import json
from research_agent.inno.workflow import Graph
from litellm import completion

def transfer_fschema_to_dict(fschema: Dict) -> Dict:
    """
    Transfer the fschema to a dictionary.

    Returns:
        A dictionary to input to workflow graph.
    """
    graph_dict = {}
    graph_dict['nodes'] = []
    graph_dict['edges'] = []
    node_id_name_map = {}
    fschema_data = fschema['data']
    for node in fschema_data['nodes']:
        graph_dict['nodes'].append({'agent_name': node['type'], "agent_tools": [], "input": "", "output": "", "is_start": node['type'] == 'start', "is_end": node['type'] == 'end'}.copy())
        node_id_name_map[node['key']] = node['type']
    for edge in fschema_data['connections']:
        graph_dict['edges'].append({'start': node_id_name_map[edge['from']], 'end': node_id_name_map[edge['to']]}.copy())
    return graph_dict

def complete_workflow(workflow: Dict, description: str) -> Dict:
    """
    Complete the workflow to a more detailed workflow graph.
    """
    workflow_prompt = \
f"""
You are a workflow designer which can complete the workflow graph I give you to a more detailed workflow graph.
"""
    user_prompt = \
f"""
I have a workflow: {json.dumps(workflow, indent=4)}
The description of the workflow is: {description}
You should complete the workflow graph in the following way: 
1. Add "agent_tools" in each node only based on the description.
2. Add "input" and "output" in each node to make the workflow more clear.
3. Make sure other fields of the workflow keep the same.
"""
    messages=[{"role": "system", "content": workflow_prompt}, {"role": "user", "content": user_prompt}]
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "graph",
            "schema": {
                "type": "object",
                "properties": {
                    "nodes": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "agent_name": {"type": "string"},
                                "agent_tools": {"type": "array", "items": {"type": "string"}}, 
                                "input": {"type": "string"},
                                "output": {"type": "string"},
                                "is_start": {"type": "boolean"},
                                "is_end": {"type": "boolean"}
                            },
                            "required": ["agent_name", "agent_tools", "input", "output", "is_start", "is_end"],
                            "additionalProperties": False
                        }
                    },
                    "edges": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string"},
                                "end": {"type": "string"},
                                "description": {"type": "string"}
                            },
                            "required": ["start", "end", "description"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["nodes", "edges"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
    response = completion(model='gpt-4o-2024-08-06', messages=messages, response_format=response_format)
    return json.loads(response.choices[0].message.content)
if __name__ == '__main__':
    with open('/Users/tangjiabin/Documents/reasoning/metachain/chaingraph/common_ragflow-2024.json', 'r') as f:
        fschema = json.load(f)
    graph_dict = transfer_fschema_to_dict(fschema)
    g = Graph.from_dict(graph_dict)
    g.visualize()
    description = "The workflow is a common workflow for the RAG system. It consists of Query Rewriter Agent, Retriever Agent, Reranker Agent, and Generator Agent. The input of the workflow is a user query, the path of target document is given by the user. Retriever Agent have `save_to_vectordb` tool to save the document to the vector database, and have `retrieve_from_vectordb` tool to retrieve the document from the vector database. Reranker Agent have `rerank` tool to rerank the retrieved documents."
    graph_dict = complete_workflow(graph_dict, description)
    print(json.dumps(graph_dict, indent=4))