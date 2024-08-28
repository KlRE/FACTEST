import json


def read_ds_file(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data["conversations"]


def make_chatgpt_ds(file, save_path=None):
    """
    Create dataset in this format:
    {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?"}]}
{"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters."}]}
    """
    ds = read_ds_file(file)
    # create new dataset in the same directory called _chatgpt
    save_path = save_path if save_path else file.replace(".json", "_chatgpt.jsonl")
    # validation set

    num_ds = 400
    num_val = 0

    with open(save_path, "w") as f:
        for conv in ds[:num_ds]:
            num_ds -= 1
            output = f"new_path = {conv['output']}"

            obj = json.dumps({"messages": [{"role": "system",
                                            "content": "You are a highly efficient and capable planner designed to solve 2D mazes. Given the positions of obstacles, the start point, and the end goal, you are tasked with determining the optimal path from the start to the goal while avoiding obstacles. You must evaluate the maze layout, identify possible routes, and select the most efficient path, considering factors such as distance, direction, and potential dead ends. Your objective is to find a clear and direct path."},
                                           {"role": "user", "content": conv["input"]},
                                           {"role": "assistant", "content": output}]})
            # remove new lines
            obj = obj.replace("\n", "")
            f.write(obj + "\n")

    with open(save_path.replace(".jsonl", "_val.jsonl"), "w") as f:
        for conv in ds[-num_val:]:
            output = f"new_path = {conv['output']}"
            obj = json.dumps({"messages": [{"role": "system",
                                            "content": "You are a highly efficient and capable planner designed to solve 2D mazes. Given the positions of obstacles, the start point, and the end goal, you are tasked with determining the optimal path from the start to the goal while avoiding obstacles. You must evaluate the maze layout, identify possible routes, and select the most efficient path, considering factors such as distance, direction, and potential dead ends. Your objective is to find a clear and direct path."},
                                           {"role": "user", "content": conv["input"]},
                                           {"role": "assistant", "content": output}]})
            # remove new lines
            obj = obj.replace("\n", "")
            f.write(obj + "\n")


def custom_ds():
    ds_full_path = "datasets/synthetic_ds2.json"
    ds_feedback_path = "../tests/random_env/conversation_pairs_2024-08-28.json"
    ds_feedback = read_ds_file(ds_feedback_path)
    ds_full = read_ds_file(ds_full_path)
    ds_feedback.sort(key=lambda x: -len(x["response"]))
    ds_feedback = list(map(lambda x: {"input": x["input"], "output": x["response"]}, ds_feedback))
    # view_len = map(len, [x["response"] for x in ds_feedback])
    # print(list(view_len))
    interactions = {"conversations": ds_full[:200] + ds_feedback[:200]}
    ds_file_path = "datasets/mixed_ds_400.json"
    json.dump(interactions, open(ds_file_path, 'w'), indent=4)


if __name__ == '__main__':
    # custom_ds()
    make_chatgpt_ds("datasets/mixed_ds_400.json")
